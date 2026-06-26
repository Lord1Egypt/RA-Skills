#!/usr/bin/env node
const {
  walkingRoute,
  drivingRoute,
  ridingRoute,
  transitRoute,
  generateMapLink
} = require('./vendor/amap_index');

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

function toMapTask(routeType, originLng, originLat, destLng, destLat, remark, city) {
  const task = {
    type: 'route',
    routeType,
    start: [originLng, originLat],
    end: [destLng, destLat],
    remark
  };
  if (city && routeType === 'transfer') task.city = city;
  return task;
}

function formatDistance(m) {
  if (m == null) return '未知';
  if (Number(m) >= 1000) return `${(Number(m) / 1000).toFixed(1)} km`;
  return `${m} m`;
}

function formatDuration(sec) {
  if (sec == null) return '未知';
  const s = Number(sec);
  const h = Math.floor(s / 3600);
  const m = Math.round((s % 3600) / 60);
  return h > 0 ? `${h}小时${m}分钟` : `${m}分钟`;
}

async function main() {
  const args = parseArgs();
  const mode = args.mode || 'driving';
  const origin = args.origin || (args.originLng && args.originLat ? `${args.originLng},${args.originLat}` : '');
  const destination = args.destination || (args.destLng && args.destLat ? `${args.destLng},${args.destLat}` : '');
  const originName = args.originName || '起点';
  const destName = args.destName || '终点';
  const city = args.city || args.region || '';

  if (!origin || !destination) {
    console.log(JSON.stringify({ error: 'Missing origin/destination. Use --origin=经度,纬度 and --destination=经度,纬度' }, null, 2));
    process.exit(2);
  }

  const [originLng, originLat] = origin.split(',').map(Number);
  const [destLng, destLat] = destination.split(',').map(Number);
  let data;
  let summary = {};

  try {
    if (mode === 'walking') {
      data = await walkingRoute({ origin, destination });
      const path = data?.route?.paths?.[0];
      summary = {
        distance_m: path?.distance ? Number(path.distance) : null,
        duration_s: path?.duration ? Number(path.duration) : null,
        routes_count: data?.route?.paths?.length || 0
      };
    } else if (mode === 'riding') {
      data = await ridingRoute({ origin, destination });
      const path = data?.data?.paths?.[0];
      summary = {
        distance_m: path?.distance ? Number(path.distance) : null,
        duration_s: path?.duration ? Number(path.duration) : null,
        routes_count: data?.data?.paths?.length || 0
      };
    } else if (mode === 'transfer') {
      if (!city) {
        console.log(JSON.stringify({ error: 'Transit mode requires --city or --region' }, null, 2));
        process.exit(2);
      }
      data = await transitRoute({ origin, destination, city, strategy: args.strategy ? Number(args.strategy) : 0 });
      const transit = data?.route?.transits?.[0];
      summary = {
        distance_m: transit?.distance ? Number(transit.distance) : null,
        duration_s: transit?.duration ? Number(transit.duration) : null,
        routes_count: data?.route?.transits?.length || 0,
        cost: transit?.cost ? Number(transit.cost) : null,
        walking_distance_m: transit?.walking_distance ? Number(transit.walking_distance) : null
      };
    } else {
      data = await drivingRoute({ origin, destination, strategy: args.strategy ? Number(args.strategy) : 10 });
      const path = data?.route?.paths?.[0];
      summary = {
        distance_m: path?.distance ? Number(path.distance) : null,
        duration_s: path?.duration ? Number(path.duration) : null,
        routes_count: data?.route?.paths?.length || 0,
        tolls: path?.tolls ? Number(path.tolls) : 0,
        traffic_lights: path?.traffic_lights ? Number(path.traffic_lights) : 0
      };
    }

    if (!data) {
      console.log(JSON.stringify({ error: 'Route planning failed' }, null, 2));
      process.exit(2);
    }

    const mapLink = generateMapLink([
      toMapTask(mode, originLng, originLat, destLng, destLat, `${originName} → ${destName}`, city)
    ]);

    const output = {
      mode,
      origin_name: originName,
      dest_name: destName,
      origin,
      destination,
      ...summary,
      distance_text: formatDistance(summary.distance_m),
      duration_text: formatDuration(summary.duration_s),
      amap_link: mapLink,
      note: '点击 amap_link 可在 Web 中查看路线结果。经纬度顺序为“经度,纬度”。'
    };

    console.log(JSON.stringify(output, null, 2));
  } catch (err) {
    console.log(JSON.stringify({ error: err.message }, null, 2));
    process.exit(2);
  }
}

main();
