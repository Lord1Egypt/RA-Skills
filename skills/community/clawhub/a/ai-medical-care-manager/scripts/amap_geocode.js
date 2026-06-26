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

async function geocode(address, city) {
  const key = process.env.AMAP_WEBSERVICE_KEY || process.env.AMAP_KEY;
  if (!key) {
    return { error: 'Missing AMAP_WEBSERVICE_KEY (or AMAP_KEY)' };
  }
  if (!address) {
    return { error: 'Missing --address' };
  }

  try {
    const resp = await axios.get('https://restapi.amap.com/v3/geocode/geo', {
      params: {
        key,
        address,
        city: city || undefined,
        output: 'JSON'
      },
      timeout: 15000
    });
    const data = resp.data;
    if (data.status !== '1' || !Array.isArray(data.geocodes) || data.geocodes.length === 0) {
      return {
        error: data.info || 'AMap geocode failed',
        raw: data
      };
    }
    const gc = data.geocodes[0];
    const [lng, lat] = String(gc.location || '').split(',').map(Number);
    return {
      address,
      city: city || '',
      formatted_address: gc.formatted_address || address,
      province: gc.province || '',
      district: gc.district || '',
      adcode: gc.adcode || '',
      location: gc.location,
      lng,
      lat
    };
  } catch (err) {
    return { error: err.message };
  }
}

(async () => {
  const args = parseArgs();
  const result = await geocode(args.address, args.city);
  console.log(JSON.stringify(result, null, 2));
  process.exit(result.error ? 2 : 0);
})();
