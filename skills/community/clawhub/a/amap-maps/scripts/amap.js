#!/usr/bin/env node
/**
 * 高德地图 Skill 命令行工具
 * 通过 Streamable HTTP MCP 调用高德地图服务
 *
 * 使用方法:
 *   node amap.js <command> [options]
 *
 * 命令列表:
 *   weather <city>                    - 查询天气
 *   geo encode <address> [city]       - 地址转坐标
 *   geo decode <location>             - 坐标转地址
 *   search text <keywords> [city]     - 关键词搜索
 *   search around <loc> <kw> [radius] - 周边搜索
 *   search detail <poi_id>            - POI 详情
 *   route driving <o> <d>             - 驾车路线
 *   route walking <o> <d>             - 步行路线
 *   route bicycling <o> <d>           - 骑行路线
 *   route transit <o> <d> <c> <cd>    - 公交路线
 *   distance <o> <d> [type]           - 距离测量
 *   ip-location <ip>                  - IP 定位
 *   navi <lon> <lat>                  - 导航 Schema
 *   taxi <dlon> <dlat> <dname>        - 打车 Schema
 */

import fetch from 'node-fetch';

const AMAP_KEY = process.env.AMAP_KEY;
const MCP_URL = 'https://mcp.amap.com/mcp';

if (!AMAP_KEY) {
    console.error('错误：未设置 AMAP_KEY 环境变量');
    console.error('请执行：export AMAP_KEY="你的高德Key"');
    process.exit(1);
}

/**
 * 调用 MCP 工具
 */
async function callTool(name, args) {
    try {
        const response = await fetch(`${MCP_URL}?key=${AMAP_KEY}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json, text/event-stream'
            },
            body: JSON.stringify({
                jsonrpc: '2.0',
                method: 'tools/call',
                params: {
                    name,
                    arguments: args
                },
                id: 1
            })
        });

        const text = await response.text();

        // 处理可能的 SSE 格式
        let jsonText = text;
        if (text.includes('data:')) {
            const match = text.match(/^data:\s*(.+)/m);
            if (match) {
                jsonText = match[1];
            }
        }

        const result = JSON.parse(jsonText);

        if (result.error) {
            console.error(`MCP 错误：${result.error.message || result.error}`);
            process.exit(1);
        }

        if (result.result?.content?.[0]?.text) {
            try {
                return JSON.parse(result.result.content[0].text);
            } catch {
                return result.result.content[0].text;
            }
        }

        return result;
    } catch (error) {
        console.error(`调用失败：${error.message}`);
        process.exit(1);
    }
}

/**
 * 输出 JSON 结果
 */
function output(data) {
    console.log(JSON.stringify(data, null, 2));
}

// ========== 天气 ==========
async function weather(city) {
    const result = await callTool('maps_weather', { city });
    output(result);
}

// ========== 地理编码 ==========
async function geoEncode(address, city) {
    const args = { address };
    if (city) args.city = city;
    const result = await callTool('maps_geo', args);
    output(result);
}

async function geoDecode(location) {
    const result = await callTool('maps_regeocode', { location });
    output(result);
}

// ========== 搜索 ==========
async function searchText(keywords, city) {
    const args = { keywords };
    if (city) args.city = city;
    const result = await callTool('maps_text_search', args);
    output(result);
}

async function searchAround(location, keywords, radius = '1000') {
    const result = await callTool('maps_around_search', { location, keywords, radius });
    output(result);
}

async function searchDetail(id) {
    const result = await callTool('maps_search_detail', { id });
    output(result);
}

// ========== 路线规划 ==========
async function routeDriving(origin, destination) {
    const result = await callTool('maps_direction_driving', { origin, destination });
    output(result);
}

async function routeWalking(origin, destination) {
    const result = await callTool('maps_direction_walking', { origin, destination });
    output(result);
}

async function routeBicycling(origin, destination) {
    const result = await callTool('maps_direction_bicycling', { origin, destination });
    output(result);
}

async function routeTransit(origin, destination, city, cityd) {
    const result = await callTool('maps_direction_transit_integrated', { origin, destination, city, cityd });
    output(result);
}

// ========== 距离测量 ==========
async function distance(origins, destination, type = '1') {
    const result = await callTool('maps_distance', { origins, destination, type });
    output(result);
}

// ========== IP 定位 ==========
async function ipLocation(ip) {
    const result = await callTool('maps_ip_location', { ip });
    output(result);
}

// ========== Schema 工具 ==========
async function navi(lon, lat) {
    const result = await callTool('maps_schema_navi', { lon, lat });
    output(result);
}

async function taxi(dlon, dlat, dname, slon, slat, sname) {
    const args = { dlon, dlat, dname };
    if (slon) args.slon = slon;
    if (slat) args.slat = slat;
    if (sname) args.sname = sname;
    const result = await callTool('maps_schema_take_taxi', args);
    output(result);
}

// ========== 命令行解析 ==========
function printHelp() {
    console.log(`
高德地图命令行工具

使用方法: node amap.js <command> [options]

命令:
  weather <city>                              查询天气
  geo encode <address> [city]                 地址转坐标
  geo decode <location>                       坐标转地址
  search text <keywords> [city]               关键词搜索
  search around <location> <keywords> [r]     周边搜索
  search detail <poi_id>                      POI 详情
  route driving <origin> <destination>        驾车路线
  route walking <origin> <destination>        步行路线
  route bicycling <origin> <destination>      骑行路线
  route transit <o> <d> <city> <cityd>        公交路线
  distance <origins> <dest> [type]            距离测量 (0=直线，1=驾车，3=步行)
  ip-location <ip>                            IP 定位
  navi <lon> <lat>                            导航 Schema
  taxi <dlon> <dlat> <dname> [slon] [slat]    打车 Schema

示例:
  node amap.js weather 北京
  node amap.js geo encode "北京市朝阳区望京SOHO" 北京
  node amap.js geo decode "116.482384,39.998383"
  node amap.js search text 麦当劳 北京
  node amap.js search around "116.48,39.99" 餐厅 1000
  node amap.js route driving "116.48,39.99" "116.40,39.91"
  node amap.js distance "116.48,39.99" "116.40,39.91" 1
`);
}

const cmd = process.argv[2];

switch (cmd) {
    case 'weather':
        weather(process.argv[3] || '北京');
        break;

    case 'geo':
        if (process.argv[3] === 'encode') {
            geoEncode(process.argv[4], process.argv[5]);
        } else if (process.argv[3] === 'decode') {
            geoDecode(process.argv[4]);
        } else {
            printHelp();
        }
        break;

    case 'search':
        if (process.argv[3] === 'text') {
            searchText(process.argv[4], process.argv[5]);
        } else if (process.argv[3] === 'around') {
            searchAround(process.argv[4], process.argv[5] || '', process.argv[6] || '1000');
        } else if (process.argv[3] === 'detail') {
            searchDetail(process.argv[4]);
        } else {
            printHelp();
        }
        break;

    case 'route':
        if (process.argv[3] === 'driving') {
            routeDriving(process.argv[4], process.argv[5]);
        } else if (process.argv[3] === 'walking') {
            routeWalking(process.argv[4], process.argv[5]);
        } else if (process.argv[3] === 'bicycling') {
            routeBicycling(process.argv[4], process.argv[5]);
        } else if (process.argv[3] === 'transit') {
            routeTransit(process.argv[4], process.argv[5], process.argv[6], process.argv[7]);
        } else {
            printHelp();
        }
        break;

    case 'distance':
        distance(process.argv[3], process.argv[4], process.argv[5] || '1');
        break;

    case 'ip-location':
        ipLocation(process.argv[4]);
        break;

    case 'navi':
        navi(process.argv[3], process.argv[4]);
        break;

    case 'taxi':
        taxi(process.argv[3], process.argv[4], process.argv[5], process.argv[6], process.argv[7], process.argv[8]);
        break;

    default:
        printHelp();
}
