import fetch from 'node-fetch';
import { Mutex } from 'async-mutex';
import { Region, LOGIN_EXPIRATION, getAwsConfig } from './config.js';
import GigyaApi from './gigyaClient.js';

export const BlueairDeviceSensorDataMap: Record<string, string> = {
    fsp0: 'fanspeed',
    hcho: 'hcho',
    h: 'humidity',
    pm1: 'pm1',
    pm10: 'pm10',
    pm2_5: 'pm2_5',
    t: 'temperature',
    tVOC: 'voc',
    co2: 'co2',
    no2: 'no2',
    o3: 'o3',
    nox: 'noxDensity',
};

export default class BlueairAwsApi {
    public username: string;
    public password: string;
    public region: Region;
    public gigyaApi: GigyaApi;
    public last_login: number;
    private mutex: Mutex;
    public accessToken: string;
    public blueairApiUrl: string;

    constructor(username: string, password: string, region: Region) {
        this.username = username;
        this.password = password;
        this.region = region;
        const config = getAwsConfig(region);
        this.blueairApiUrl = `https://${config.restApiId}.execute-api.${config.awsRegion}.amazonaws.com/prod/c`;
        this.mutex = new Mutex();
        this.gigyaApi = new GigyaApi(username, password, region);
        this.last_login = 0;
        this.accessToken = '';
    }

    static async loginWithAutoDetect(
        username: string,
        password: string
    ): Promise<{ accessToken: string; region: Region; accountUuid: string }> {
        const regions = [Region.US, Region.EU, Region.AU, Region.CN, Region.RU];
        for (const region of regions) {
            try {
                const gigyaApi = new GigyaApi(username, password, region);
                const { token, secret } = await gigyaApi.getGigyaSession();
                const { jwt } = await gigyaApi.getGigyaJWT(token, secret);
                const tempApi = new BlueairAwsApi(username, password, region);
                const { accessToken } = await tempApi.getAwsAccessToken(jwt);
                tempApi.accessToken = accessToken;
                tempApi.last_login = Date.now();
                const devices = await tempApi.getDevices();
                if (!devices || devices.length === 0) continue;
                const accountUuid = devices[0].name;
                const deviceStatus = await tempApi.getDeviceStatus(accountUuid, [devices[0].uuid]);
                if (!deviceStatus || deviceStatus.length === 0) continue;
                return { accessToken, region, accountUuid };
            } catch (error) {
                continue;
            }
        }
        throw new Error('Failed to auto-detect region. Please check credentials or manually set region.');
    }

    async login(): Promise<void> {
        const { token, secret } = await this.gigyaApi.getGigyaSession();
        const { jwt = '' } = await this.gigyaApi.getGigyaJWT(token, secret);
        const { accessToken } = await this.getAwsAccessToken(jwt);
        this.last_login = Date.now();
        this.accessToken = accessToken;
    }

    async checkTokenExpiration(): Promise<void> {
        if (LOGIN_EXPIRATION < Date.now() - this.last_login) {
            await this.login();
        }
    }

    async getDevices(): Promise<any[]> {
        await this.checkTokenExpiration();
        const response = await this.apiCall('/registered-devices', undefined, 'GET');
        if (!response.devices) throw new Error('getDevices error: no devices in response');
        return response.devices;
    }

    async getDeviceStatus(accountUuid: string, uuids: string[]): Promise<any[]> {
        await this.checkTokenExpiration();
        const body: any = {
            deviceconfigquery: uuids.map((uuid) => ({ id: uuid, r: { r: ['sensors'] } })),
            includestates: true,
            eventsubscription: { include: uuids.map((uuid) => ({ filter: { o: `= ${uuid}` } })) },
        };
        const data = await this.apiCall(`/${accountUuid}/r/initial`, body);
        if (!data.deviceInfo) throw new Error('getDeviceStatus error: no deviceInfo in response');
        return data.deviceInfo.map((device: any) => {
            const sensorData: Record<string, any> = {};
            for (const sensor of device.sensordata) {
                const key = BlueairDeviceSensorDataMap[sensor.n];
                if (key) sensorData[key] = sensor.v;
            }
            const state: Record<string, any> = {};
            for (const s of device.states) {
                const value = s.v ?? s.vb;
                if (value !== undefined) state[s.n] = value;
            }
            return { id: device.id, name: device.configuration.di.name, sensorData, state };
        });
    }

    async setDeviceStatus(uuid: string, state: string, value: number | boolean): Promise<any> {
        await this.checkTokenExpiration();
        const body: any = { n: state };
        if (typeof value === 'number') body.v = value;
        else if (typeof value === 'boolean') body.vb = value;
        return await this.apiCall(`/${uuid}/a/${state}`, body);
    }

    async getAwsAccessToken(jwt: string): Promise<{ accessToken: string }> {
        const response = await this.apiCall('/login', undefined, 'POST', {
            Authorization: `Bearer ${jwt}`,
            idtoken: jwt,
        });
        if (!response.access_token) throw new Error('AWS access token error');
        return { accessToken: response.access_token };
    }

    async apiCall(url: string, data?: any, method = 'POST', headers?: any, retries = 3): Promise<any> {
        const release = await this.mutex.acquire();
        try {
            const response = await fetch(`${this.blueairApiUrl}${url}`, {
                method,
                headers: {
                    Authorization: `Bearer ${this.accessToken}`,
                    idtoken: this.accessToken,
                    'Content-Type': 'application/json',
                    ...headers,
                },
                body: data ? JSON.stringify(data) : undefined,
            });
            const json = await (response as any).json();
            if (response.status !== 200) throw new Error(`API error ${response.status}`);
            return json;
        } catch (error) {
            if (retries > 0) return this.apiCall(url, data, method, headers, retries - 1);
            throw error;
        } finally {
            release();
        }
    }
}
