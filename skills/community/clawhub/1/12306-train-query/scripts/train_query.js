#!/usr/bin/env node
/**
 * 12306火车票查询脚本
 * 用法: node train_query.js [出发站] [到达站] [日期]
 * 示例: node train_query.js 长沙 北京 2026-03-16
 */

const https = require('https');
const http = require('http');
const { URL } = require('url');

// 默认查询参数
let fromStation = process.argv[2] || '长沙';
let toStation = process.argv[3] || '北京';
let date = process.argv[4] || new Date().toISOString().split('T')[0];

function getStations() {
    return new Promise((resolve, reject) => {
        const url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js';
        
        https.get(url, { rejectUnauthorized: false }, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                const stations = {};
                // 格式: @bji|北京|BJP|...
                const regex = /@[^|]+\|([^|]+)\|([^|]+)\|/g;
                let match;
                while ((match = regex.exec(data)) !== null) {
                    stations[match[1]] = match[2];
                }
                resolve(stations);
            });
        }).on('error', reject);
    });
}

function queryTickets(date, fromCode, toCode) {
    return new Promise((resolve, reject) => {
        const url = `https://kyfw.12306.cn/otn/leftTicket/queryG?leftTicketDTO.train_date=${date}&leftTicketDTO.from_station=${fromCode}&leftTicketDTO.to_station=${toCode}&purpose_codes=ADULT`;
        
        const options = {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Referer': 'https://www.12306.cn/mormhweb/',
                'Cookie': 'JSESSIONID=test123; BIGipServerotn=123456'
            },
            rejectUnauthorized: false
        };

        function fetch(url, opts, callback) {
            const client = url.startsWith('https') ? https : http;
            client.get(url, opts, (res) => {
                if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
                    const newUrl = new URL(res.headers.location, url).toString();
                    fetch(newUrl, opts, callback);
                } else {
                    let data = '';
                    res.on('data', chunk => data += chunk);
                    res.on('end', () => callback(data));
                }
            }).on('error', e => {
                console.log('Fetch Error:', e.message);
                resolve([]);
            });
        }

        fetch(url, options, (data) => {
            try {
                const json = JSON.parse(data);
                if (json.httpstatus === 200 && json.data && json.data.result) {
                    const decodedResults = json.data.result.map(item => {
                        try {
                            return decodeURIComponent(item);
                        } catch {
                            return item;
                        }
                    });
                    resolve(decodedResults);
                } else {
                    resolve([]);
                }
            } catch (e) {
                resolve([]);
            }
        });
    });
}

function parseTrain(result) {
    if (!result) return null;
    
    const items = result.split('|');
    
    const seatMap = {
        32: '商务座',
        31: '特等座', 
        30: '一等座',
        29: '二等座',
        28: '高级软卧',
        26: '软卧',
        23: '硬卧',
        21: '硬座',
        22: '无座'
    };
    
    const seats = {};
    for (const [pos, name] of Object.entries(seatMap)) {
        const idx = parseInt(pos);
        if (idx < items.length && items[idx] && items[idx] !== '无' && items[idx] !== '*') {
            seats[name] = items[idx];
        }
    }
    
    return {
        trainNo: items[3] || '',
        fromCode: items[6] || '',
        toCode: items[7] || '',
        startTime: items[8] || '--:--',
        arriveTime: items[9] || '--:--',
        duration: items[10] || '--:--',
        seats: seats
    };
}

function formatOutput(tickets, stationMap, fromName, toName) {
    if (!tickets || tickets.length === 0) {
        console.log('未查询到列车信息');
        return;
    }

    const codeToStation = {};
    for (const [name, code] of Object.entries(stationMap)) {
        codeToStation[code] = name;
    }

    console.log('\n' + '='.repeat(60));
    console.log(`🚄 ${fromName} → ${toName} 火车票查询结果`);
    console.log('='.repeat(60) + '\n');

    let count = 0;
    for (const result of tickets) {
        const info = parseTrain(result);
        if (!info || !info.trainNo) continue;

        count++;
        const from = codeToStation[info.fromCode] || info.fromCode;
        const to = codeToStation[info.toCode] || info.toCode;

        console.log(`【${info.trainNo}】${from} → ${to}`);
        console.log(`  发车: ${info.startTime}  到达: ${info.arriveTime}  历时: ${info.duration}`);
        
        if (Object.keys(info.seats).length > 0) {
            const seatStr = Object.entries(info.seats)
                .map(([name, num]) => `${name}: ${num}`)
                .join(', ');
            console.log(`  余票: ${seatStr}`);
        } else {
            console.log('  余票: 暂无');
        }
        console.log();
    }

    console.log(`共查询到 ${count} 趟列车\n`);
}

async function main() {
    try {
        console.log(`📅 查询日期: ${date}`);
        console.log(`🚉 出发站: ${fromStation}  到达站: ${toStation}`);
        console.log('-'.repeat(50));

        // 获取车站代码
        const stations = await getStations();
        const fromCode = stations[fromStation];
        const toCode = stations[toStation];

        if (!fromCode || !toCode) {
            console.log(`错误: 找不到车站代码 - ${fromStation}: ${fromCode}, ${toStation}: ${toCode}`);
            console.log('请检查车站名称是否正确');
            return;
        }

        // 查询车票
        const results = await queryTickets(date, fromCode, toCode);
        
        // 输出结果
        formatOutput(results, stations, fromStation, toStation);
        
    } catch (e) {
        console.error('Error:', e.message);
    }
}

main();
