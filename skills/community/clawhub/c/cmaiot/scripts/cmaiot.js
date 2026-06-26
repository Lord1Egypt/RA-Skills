#!/usr/bin/env node

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const log = console.log;

const base_url = 'https://iot-api.heclouds.com';
const config_file = path.join(__dirname, 'config.json');

let config;

function readConfig() {
    if (!fs.existsSync(config_file)) {
        return { "products": [] };
    }
    const data = fs.readFileSync(config_file, 'utf8');
    return JSON.parse(data);
}

function getAccessKey(productId) {
    return config.products.find(p => p.productId === productId).accessKey;
}

function addProduct(productId, accessKey) {
    if (!productId || !accessKey) {
        showHelp();
        return false;
    }

    const exist = config.products.find(p => p.productId === productId);
    if (exist) {
        return false;
    }

    config.products.push({ productId, accessKey });
    fs.writeFileSync(config_file, JSON.stringify(config, null, 2));
    return true;
}

function generateToken(res, accessKey) {
    const method = 'sha256';
    const version = '2018-10-31';
    const et = Math.floor(Date.now() / 1000) + 24 * 60 * 60;

    const org = `${et}\n${method}\n${res}\n${version}`;
    const key = Buffer.from(accessKey, 'base64');
    const hmac = crypto.createHmac(method, key);
    hmac.update(org);
    const sign = hmac.digest('base64');

    const encodedRes = encodeURIComponent(res);
    const encodedSign = encodeURIComponent(sign);

    return `version=${version}&res=${encodedRes}&et=${et}&method=${method}&sign=${encodedSign}`;
}

async function http_get(url, token) {
    const response = await fetch(base_url + url, {
        method: 'GET',
        headers: {
            'authorization': token,
            'Content-Type': 'application/json'
        }
    });
    const data = await response.json();
    log('recieve:', JSON.stringify(data, null, 2));
}

async function http_post(url, token, body) {
    log('send:', body);
    const response = await fetch(base_url + url, {
        method: 'POST',
        headers: {
            'authorization': token,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    });
    const data = await response.json();
    log('recieve:', JSON.stringify(data, null, 2));
}

function showHelp() {
    log(`Usage: cmaiot <cmd> [<target>] [<jsonString>]`);
    log(`以下命令中的部分参数使用/分隔，每个参数均为必传`);
    log(`cmaiot help                                            显示帮助`);
    log(`cmaiot add productId/accessKey                         添加产品ID和访问密钥`);
    log(`cmaiot model productId                                 查询物模型数据格式`);
    log(`cmaiot detail productId                                查询产品详情`);
    log(`cmaiot detail productId/deviceName                     查询设备详情`);
    log(`cmaiot live productId/deviceName/deviceSn              获取视频设备的直播地址`);
    // log(`cmaiot ability productId/deviceName/deviceSn           获取视频设备的本地AI能力列表`);
    // log(`cmaiot algo productId/deviceName/deviceSn              获取视频设备的云端AI能力列表`);
    log(`cmaiot ls                                              列出已添加的产品`);
    log(`cmaiot ls productId                                    列出产品下的设备`);
    log(`cmaiot ls productId/deviceName                         读取设备缓存的最新属性`);
    log(`cmaiot ls productId/deviceName/propertyId              读取设备实时属性`);
    log(`cmaiot create productId/deviceName                     在产品下创建设备`);
    log(`cmaiot call productId/deviceName/serviceId jsonString  调用设备服务`);
    log(`cmaiot set productId/deviceName jsonString             设置设备属性`);
    log(`cmaiot enable productId/deviceName                     启用设备`);
    log(`cmaiot disable productId/deviceName                    禁用设备`);
    log(`cmaiot enable productId/deviceName/imeiValue           启用LwM2M设备`);
    log(`cmaiot disable productId/deviceName/imeiValue          禁用LwM2M设备`);
}
async function main() {
    const cmd = process.argv[2];
    const target = process.argv[3];
    const jsonString = process.argv[4];

    if (!cmd) {
        showHelp();
        return;
    }

    config = readConfig();

    let productId, accessKey, deviceName, identifier, res, token;

    if (target && cmd !== 'add') {
        [productId, deviceName, identifier] = target.split('/');
        accessKey = getAccessKey(productId);

        res = `products/${productId}`;
        token = generateToken(res, accessKey);
    }

    enableValue = false;

    switch (cmd) {
    case 'help':
        showHelp();
        break;
    case 'add':
        const separatorIndex = target.indexOf('/');
        const newProductId = target.substring(0, separatorIndex);
        const newAccessKey = target.substring(separatorIndex + 1);
        addProduct(newProductId, newAccessKey);
        break;
    case 'model':
        await http_get(`/thingmodel/query-thing-model?product_id=${productId}`, token);
        break;
    case 'detail':
        if (deviceName) {
            await http_get(`/device/detail?product_id=${productId}&device_name=${deviceName}`, token);
        } else {
            await http_get(`/product/detail?product_id=${productId}`, token);
        }
        break;
    case 'live':
        log('tips: 获取直播地址成功后，可以使用VLC播放器，也可以使用ffmpeg截图')
        log('ffmpeg截图命令: ffmpeg -i ${data.url} -ss 00:00:01 -vframes 1 ${deviceName}.jpg')
        await http_post(`/video/device/live/url?pid=${productId}`, token, {deviceSn: identifier,urlType: 2,dataType: 1});
        break;
    case 'ability':
        await http_post(`/video/device/ai/ability`, token, {deviceSn: identifier});
        break;
    case 'algo':
        await http_post(`/video/aitask/algo-list-query`, token, {deviceSn: identifier});
        break;
    case 'service':
        await http_post(`/video/device/service`, token, {deviceSn: identifier});
        break;
    case 'ls':
        if (target) {
            if (deviceName) {
                if(identifier) {
                    await http_post(`/thingmodel/query-device-property-detail`, token, {product_id: productId,device_name: deviceName,params: [identifier]});
                }
                else {
                    log("tips: 如果没有value字段，表示设备没有上传过数据")
                    await http_get(`/thingmodel/query-device-property?product_id=${productId}&device_name=${deviceName}`, token);
                }
            } else {
                log('tips: 最多列出100个设备')
                log('status数值含义: 0 离线 1 在线 2 未激活')
                log('intelligent_way 智能化方式 1 设备接入 2 产品智能化')
                log('access_pt 接入协议 0 子设备 1 其他 2 MQTT 3 CoAP 4 LwM2M 5 HTTP 51 视频设备 101 卫星')
                log('data_pt 数据协议 1 OneJson 2 IPSO 3 透传/自定义 4 数据流')
                log('LwM2M设备的imei不为空')
                log('视频设备的viot_device_sn为设备Sn')
                await http_get(`/device/list?product_id=${productId}&device_name=&offset=0&limit=100`, token);
            }
        } else {
            for (const product of config.products) {
                log(`${product.productId}`);
            }
        }
        break;
    case 'create':
            if (!deviceName) {
                showHelp();
            }
            await http_post(`/device/create`, token, {product_id: productId,device_name: deviceName} );
        break;
    case 'call':
        if (!jsonString) {
            log('请提供JSON参数');
        }
        await http_post(`/thingmodel/call-service`, token, {product_id: productId,device_name: deviceName,identifier: serviceId,params: JSON.parse(jsonString)});
        break;
    case 'set':
        if (!jsonString) {
            log('请提供JSON参数');
        }
        await http_post(`/thingmodel/set-device-property`, token, {product_id: productId,device_name: deviceName,params: JSON.parse(jsonString)});
        break;
    case 'enable':
        enableValue = true;
    case 'disable':
        if (identifier) {
            await http_post(`/device/enable`, token, {imei: identifier,enable: enableValue});
        } else {
            await http_post(`/device/enable`, token, {product_id: productId,device_name: deviceName,enable: enableValue});
        }
        break;
    }
}

if (require.main === module) {
    main().catch(() => {
        showHelp();
    });
}