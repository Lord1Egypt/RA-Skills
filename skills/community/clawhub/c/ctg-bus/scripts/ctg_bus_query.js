#!/usr/bin/env node
/**
 * 中旅巴士 API 查票脚本
 * 用法: node ctg_bus_query.js <日期YYYY-MM-DD> <出发城市> <到达城市> [上车站] [下车站]
 * 示例: node ctg_bus_query.js 2026-05-30 香港 深圳 旺角維景酒店 深圳灣口岸
 */

const https = require('https');

const BASE = 'https://wechat.hkctgbus.com/ctb';

// 城市 code → CityNo 映射
const CITY_MAP = {
  '香港':   { code: '810000', cityNo: 'G1095' },
  '澳門':   { code: '820000', cityNo: 'K1146' },
  '深圳':   { code: '440300', cityNo: 'K1096' },
  '廣州':   { code: '440100', cityNo: 'N1097' },
  '珠海':   { code: '440400', cityNo: 'K1121' },
  '佛山':   { code: '440600', cityNo: 'N1131' },
  '江門':   { code: '440700', cityNo: 'N1133' },
  '中山':   { code: '442000', cityNo: 'N1135' },
  '東莞':   { code: '441900', cityNo: 'N1105' },
  '肇慶':   { code: '441200', cityNo: 'N1137' },
};

// 常用站点: siteCode → { stationNumber, cityNumber }
// cityNumber 是查询班次时用的 CityNo
// stationNumber 是 OnStationCode / OffStationCode
const SITE_MAP = {
  // 香港
  '旺角維景酒店':     { siteCode: 'H1324', stationNumber: '1315', cityNo: 'G1095' },
  '太子榮利':         { siteCode: 'H1358', stationNumber: '1980', cityNo: 'G1095' },
  '尖沙咀中港城':     { siteCode: 'H1323', stationNumber: '1304', cityNo: 'G1095' },
  '灣仔':             { siteCode: 'H1326', stationNumber: '1310', cityNo: 'G1095' },
  '上環':             { siteCode: 'H1330', stationNumber: '1341', cityNo: 'G1095' },
  '觀塘':             { siteCode: 'H1325', stationNumber: '1868', cityNo: 'G1095' },
  '鑽石山':           { siteCode: 'H1344', stationNumber: '1866', cityNo: 'G1095' },
  '屯門':             { siteCode: 'H1331', stationNumber: '1325', cityNo: 'G1095' },
  '荃灣':             { siteCode: 'H1332', stationNumber: '1316', cityNo: 'G1095' },
  '北角匯':           { siteCode: 'H2753', stationNumber: '2753', cityNo: 'G1095' },
  '香港機場':         { siteCode: 'H1319', stationNumber: '1319', cityNo: 'G1095' },
  '港珠澳大橋香港口岸': { siteCode: 'H2095', stationNumber: '2095', cityNo: 'G1095' },
  '深圳灣口岸(香港段)': { siteCode: 'H1327', stationNumber: '1328', cityNo: 'G1095' },
  // 深圳
  '深圳灣口岸':       { siteCode: 'H1327', stationNumber: '1328', cityNo: 'K1096' },
  '皇崗口岸':         { siteCode: 'H1334', stationNumber: '1329', cityNo: 'K1096' },
  '寶安機場':         { siteCode: 'H1336', stationNumber: '1326', cityNo: 'K1096' },
};

function get(url) {
  return new Promise((resolve, reject) => {
    const req = https.get(url, { timeout: 15000 }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch (e) { reject(new Error('JSON parse error: ' + data.substring(0, 200))); }
      });
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('timeout')); });
  });
}

// 从站点树 API 查找站点编号
async function findSiteStation(cityCode, siteName) {
  const url = `${BASE}/generator/bacity/getCitySitesOptionalNew?fromCityCode=${cityCode}`;
  const res = await get(url);
  if (res.code !== 0 && res.code !== '0') return null;

  // 可能是出发城市树 (data) 或到达城市树 (toCities)
  const cities = res.data || [];
  for (const city of (Array.isArray(cities) ? cities : [cities])) {
    for (const area of (city.areaSite || [])) {
      for (const site of (area.siteList || [])) {
        if (site.siteName === siteName || site.siteName.includes(siteName)) {
          return { siteCode: site.siteCode, refSites: site.refSites };
        }
      }
    }
  }
  return null;
}

// 从到达城市站点树查找
async function findToSiteStation(fromCityCode, fromSiteCode, toCityCode, siteName) {
  const url = `${BASE}/generator/bacity/getCitySitesOptionalNew?fromCityCode=${fromCityCode}&fromSiteCode=${fromSiteCode}`;
  const res = await get(url);
  if (res.code !== 0 && res.code !== '0') return null;

  // toCities 是到达城市 code 列表, 需要再取站点
  // 实际数据可能在 data 字段里
  const data = res.data;
  if (!data) return null;

  const cities = Array.isArray(data) ? data : [data];
  for (const city of cities) {
    if (city.cityCode !== toCityCode) continue;
    for (const area of (city.areaSite || [])) {
      for (const site of (area.siteList || [])) {
        if (site.siteName === siteName || site.siteName.includes(siteName)) {
          return { siteCode: site.siteCode, refSites: site.refSites };
        }
      }
    }
  }
  return null;
}

// 查询班次
async function queryTrains(departureCityNo, arrivalCityNo, date, onStationCode, offStationCode) {
  const dateStr = date.replace(/-/g, '');
  const url = `${BASE}/sys/ticket/getTraininfo?DepartureCityNo=${departureCityNo}&ArrivalCityNo=${arrivalCityNo}&DepartureDate=${dateStr}&OnStationCode=${onStationCode}&OffStationCode=${offStationCode}`;
  const res = await get(url);

  if (res.code !== 0 && res.code !== '0') {
    throw new Error('查询失败: ' + (res.msg || JSON.stringify(res)));
  }

  // 响应是三层嵌套 JSON
  let data = res.data;
  if (typeof data === 'string') data = JSON.parse(data);
  if (data && typeof data.data === 'string') data = JSON.parse(data.data);

  return data;
}

function parsePrice(ticketPriceStr) {
  // 格式: "成人-4-港币-2-60.0-60,成人-4-人民币-1-55.0-55"
  const parts = ticketPriceStr.split(',');
  const prices = {};
  for (const part of parts) {
    const fields = part.split('-');
    const typeName = fields[0];
    const currency = fields[2];
    const price = fields[4];
    if (!prices[typeName]) prices[typeName] = {};
    prices[typeName][currency] = price;
  }
  return prices;
}

function formatTime(timeInt) {
  const s = String(timeInt);
  if (s.length <= 2) return '00:' + s.padStart(2, '0');
  return s.slice(0, -2).padStart(2, '0') + ':' + s.slice(-2);
}

async function main() {
  const args = process.argv.slice(2);
  const date = args[0];
  const fromCityName = args[1];
  const toCityName = args[2];
  const fromSiteName = args[3] || '';
  const toSiteName = args[4] || '';

  if (!date || !fromCityName || !toCityName) {
    console.error('用法: node ctg_bus_query.js <日期YYYY-MM-DD> <出发城市> <到达城市> [上车站] [下车站]');
    process.exit(1);
  }

  const fromCity = CITY_MAP[fromCityName];
  const toCity = CITY_MAP[toCityName];
  if (!fromCity) { console.error('未知出发城市:', fromCityName, '可用:', Object.keys(CITY_MAP).join('/')); process.exit(1); }
  if (!toCity) { console.error('未知到达城市:', toCityName, '可用:', Object.keys(CITY_MAP).join('/')); process.exit(1); }

  // 确定站点编号
  let fromSite, toSite;

  if (fromSiteName && SITE_MAP[fromSiteName]) {
    fromSite = SITE_MAP[fromSiteName];
  } else {
    // 查找
    const found = await findSiteStation(fromCity.code, fromSiteName);
    if (!found) {
      console.error('未找到出发站点:', fromSiteName);
      console.error('常用站点:', Object.keys(SITE_MAP).join('、'));
      process.exit(1);
    }
    fromSite = {
      siteCode: found.siteCode,
      stationNumber: found.refSites[0]?.stationNumber,
      cityNo: found.refSites[0]?.cityNumber,
    };
  }

  if (toSiteName && SITE_MAP[toSiteName]) {
    toSite = SITE_MAP[toSiteName];
  } else {
    const found = await findToSiteStation(fromCity.code, fromSite.siteCode || fromSite.stationNumber, toCity.code, toSiteName);
    if (!found) {
      console.error('未找到到达站点:', toSiteName);
      process.exit(1);
    }
    toSite = {
      siteCode: found.siteCode,
      stationNumber: found.refSites[0]?.stationNumber,
      cityNo: found.refSites[0]?.cityNumber,
    };
  }

  // 查询班次
  const deCityNo = fromSite.cityNo || fromCity.cityNo;
  const arCityNo = toSite.cityNo || toCity.cityNo;

  console.error(`[查询] ${fromSiteName || fromCityName} → ${toSiteName || toCityName} (${date})`);
  console.error(`[参数] DepartureCityNo=${deCityNo} ArrivalCityNo=${arCityNo} OnStation=${fromSite.stationNumber} OffStation=${toSite.stationNumber}`);

  const data = await queryTrains(deCityNo, arCityNo, date, fromSite.stationNumber, toSite.stationNumber);

  const buses = data?.BusInfoList || [];
  const total = data?.TotalClassNum || buses.length;

  if (buses.length === 0) {
    console.log(JSON.stringify({ error: '该日期暂无班次', date, from: fromSiteName, to: toSiteName }));
    return;
  }

  // 输出 JSON
  const result = {
    date,
    from: fromSiteName || fromCityName,
    to: toSiteName || toCityName,
    total,
    buses: buses.map(b => ({
      time: formatTime(b.DepartureTime),
      date: b.DepartureDate,
      busNo: b.BusNo,
      from: b.DepartureCityName,
      to: b.ArrivalCityName,
      via: b.ViaPort,
      price: parsePrice(b.TicketPriceStr),
      surplus: b.SurplusTicket,
      discount: b.DiscountMsg,
      remark: b.BusRemark,
      stations: b.ViaStations,
      isDirect: b.isDirect,
    }))
  };

  console.log(JSON.stringify(result, null, 2));
}

main().catch(e => { console.error(e.message); process.exit(1); });
