#!/usr/bin/env node
const axios = require('axios');

function parseArgs() {
  const args = {};
  for (const arg of process.argv.slice(2)) {
    if (!arg.startsWith('--')) continue;
    const idx = arg.indexOf('=');
    if (idx === -1) {
      args[arg.slice(2)] = true;
    } else {
      args[arg.slice(2, idx)] = arg.slice(idx + 1);
    }
  }
  return args;
}

function midpointFromRectangle(rectangle) {
  if (!rectangle || !rectangle.includes(';')) return null;
  const [p1, p2] = rectangle.split(';');
  const [lng1, lat1] = p1.split(',').map(Number);
  const [lng2, lat2] = p2.split(',').map(Number);
  if ([lng1, lat1, lng2, lat2].some(v => Number.isNaN(v))) return null;
  return {
    lng: (lng1 + lng2) / 2,
    lat: (lat1 + lat2) / 2
  };
}

async function locateByIp(ip) {
  const key = process.env.AMAP_WEBSERVICE_KEY || process.env.AMAP_KEY;
  if (!key) return { error: 'Missing AMAP_WEBSERVICE_KEY (or AMAP_KEY)' };
  if (!ip) {
    return { error: 'Missing --ip. Only use IP locate when you truly have the user IP; otherwise ask user for current location.' };
  }
  try {
    const resp = await axios.get('https://restapi.amap.com/v3/ip', {
      params: { key, ip, output: 'JSON' },
      timeout: 15000
    });
    const data = resp.data;
    if (data.status !== '1') {
      return { error: data.info || 'AMap IP locate failed', raw: data };
    }
    const center = midpointFromRectangle(data.rectangle || '');
    return {
      ip,
      province: data.province || '',
      city: data.city || '',
      district: data.district || '',
      adcode: data.adcode || '',
      rectangle: data.rectangle || '',
      center,
      note: 'IP定位通常只到城市/区域级别，若需要精确起点路线，请继续向用户确认当前位置或具体出发地。'
    };
  } catch (err) {
    return { error: err.message };
  }
}

(async () => {
  const args = parseArgs();
  const result = await locateByIp(args.ip);
  console.log(JSON.stringify(result, null, 2));
  process.exit(result.error ? 2 : 0);
})();
