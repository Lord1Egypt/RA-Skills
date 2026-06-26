import fetch from 'node-fetch';
import { getGigyaConfig } from './config.js';
export default class GigyaApi {
    username;
    password;
    api_key;
    gigyaApiUrl;
    constructor(username, password, region) {
        this.username = username;
        this.password = password;
        const config = getGigyaConfig(region);
        this.api_key = config.apiKey;
        this.gigyaApiUrl = `https://accounts.${config.gigyaRegion}.gigya.com`;
    }
    async getGigyaSession() {
        const params = new URLSearchParams({
            apiKey: this.api_key,
            loginID: this.username,
            password: this.password,
            targetEnv: 'mobile',
        });
        const response = await this.apiCall('/accounts.login', params.toString());
        if (!response.sessionInfo) {
            throw new Error(`Gigya session error: sessionInfo in response: ${JSON.stringify(response)}`);
        }
        return {
            token: response.sessionInfo.sessionToken,
            secret: response.sessionInfo.sessionSecret,
        };
    }
    async getGigyaJWT(token, secret) {
        const params = new URLSearchParams({
            oauth_token: token,
            secret: secret,
            targetEnv: 'mobile',
        });
        const response = await this.apiCall('/accounts.getJWT', params.toString());
        if (!response.id_token) {
            throw new Error(`Gigya JWT error: no id_token in response: ${JSON.stringify(response)}`);
        }
        return {
            jwt: response.id_token,
        };
    }
    async apiCall(url, data, retries = 3) {
        const maxRetries = retries;
        try {
            const response = await fetch(`${this.gigyaApiUrl}${url}?${data}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    Accept: '*/*',
                },
            });
            const json = await response.json();
            if (response.status !== 200) {
                throw new Error(`API call error with status ${response.status}: ${JSON.stringify(json)}`);
            }
            return json;
        }
        catch (error) {
            if (retries > 0) {
                return this.apiCall(url, data, retries - 1);
            }
            else {
                throw new Error(`API call failed after ${maxRetries} retries: ${error}`);
            }
        }
    }
}
