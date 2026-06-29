#!/usr/bin/env node

import fs from "node:fs";
import fsp from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { execSync } from "node:child_process";
import { randomUUID } from "node:crypto";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const skillRoot = path.resolve(__dirname, "..");
const PUBLISH_ENDPOINT = "http://120.46.7.129:30002/publish";
const PUBLIC_BASE_URL = "http://120.46.7.129:30001";

function readArg(name) {
  const index = process.argv.indexOf(`--${name}`);
  if (index === -1) return undefined;
  return process.argv[index + 1];
}

function hasArg(name) {
  return process.argv.includes(`--${name}`);
}

async function readJson(filePath) {
  return JSON.parse(await fsp.readFile(filePath, "utf8"));
}

function validatePublishId(publishId) {
  if (!/^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$/.test(publishId)) {
    throw new Error(`publishId 不合法: ${publishId}`);
  }
}

async function encodeFile(filePath, encoding) {
  const data = await fsp.readFile(filePath, encoding === "base64" ? undefined : "utf8");
  return encoding === "base64" ? data.toString("base64") : data;
}

async function publishFiles({ publishId, htmlPath, jsonPath, xlsxPath }) {
  const endpoint = process.env.ROADBOOK_PUBLISH_ENDPOINT || PUBLISH_ENDPOINT;
  const files = {
    "index.html": { encoding: "utf8", content: await encodeFile(htmlPath, "utf8") },
    "roadbook.json": { encoding: "utf8", content: await encodeFile(jsonPath, "utf8") }
  };

  if (xlsxPath) {
    files["roadbook.xlsx"] = { encoding: "base64", content: await encodeFile(xlsxPath, "base64") };
  }

  const resp = await fetch(endpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ publishId, files })
  });
  const data = await resp.json().catch(() => ({}));

  if (!resp.ok) {
    throw new Error(`公网发布上传失败：HTTP ${resp.status} ${data.error || resp.statusText}`);
  }

  return { endpoint, ...data };
}

function fallbackRoadbook() {
  return {
    title: "合肥到北京 AI 路书示例",
    origin: "合肥",
    destination: "北京",
    dateRange: "示例：4 天 3 晚",
    assumptions: [
      "这是本地演示数据，真实版本会由高德 API 补全坐标、路线和天气。",
      "酒店暂按海淀区附近处理。"
    ],
    days: [
      {
        id: "day-1",
        title: "抵达北京，入住海淀",
        date: "Day 1",
        weather: "待调用天气 API",
        pace: "relaxed",
        stops: [
          { time: "08:30", name: "合肥南站", type: "railway_station", lng: 117.289, lat: 31.800, note: "建议提前 45 分钟到站。" },
          { time: "13:20", name: "北京南站", type: "railway_station", lng: 116.379, lat: 39.865, note: "抵达后换乘地铁或打车去酒店。" },
          { time: "15:00", name: "海淀住宿区域", type: "hotel_area", lng: 116.306, lat: 39.975, note: "办理入住，晚间轻松活动。" }
        ],
        legs: [
          { from: "合肥南站", to: "北京南站", mode: "rail", durationText: "约 4.5-5 小时", distanceText: "城际", summary: "高铁班次需用户另行确认。" },
          { from: "北京南站", to: "海淀住宿区域", mode: "public_transit", durationText: "约 55-75 分钟", distanceText: "约 20 公里", summary: "优先地铁，行李较多可打车。" }
        ]
      },
      {
        id: "day-2",
        title: "圆明园与海淀慢游",
        date: "Day 2",
        weather: "待调用天气 API",
        pace: "relaxed",
        stops: [
          { time: "09:30", name: "海淀住宿区域", type: "hotel_area", lng: 116.306, lat: 39.975, note: "早餐后出发。" },
          { time: "10:00", name: "圆明园遗址公园", type: "scenic", lng: 116.305, lat: 40.008, note: "建议预留 3-4 小时。" },
          { time: "15:00", name: "中关村书店/咖啡区域", type: "poi_area", lng: 116.316, lat: 39.984, note: "下午安排书店和咖啡。" }
        ],
        legs: [
          { from: "海淀住宿区域", to: "圆明园遗址公园", mode: "public_transit", durationText: "约 20-35 分钟", distanceText: "约 5 公里", summary: "优先地铁或短途打车。" },
          { from: "圆明园遗址公园", to: "中关村书店/咖啡区域", mode: "public_transit", durationText: "约 25-40 分钟", distanceText: "约 6 公里", summary: "下午轻量安排，避免过度赶路。" }
        ]
      },
      {
        id: "day-3",
        title: "环球影城全天游玩",
        date: "Day 3",
        weather: "待调用天气 API",
        pace: "packed",
        stops: [
          { time: "07:30", name: "海淀住宿区域", type: "hotel_area", lng: 116.306, lat: 39.975, note: "建议早出发。" },
          { time: "09:15", name: "北京环球度假区", type: "theme_park", lng: 116.679, lat: 39.858, note: "门票和营业时间需另行确认。" },
          { time: "21:00", name: "海淀住宿区域", type: "hotel_area", lng: 116.306, lat: 39.975, note: "返程时间较长，注意体力。" }
        ],
        legs: [
          { from: "海淀住宿区域", to: "北京环球度假区", mode: "public_transit", durationText: "约 90-120 分钟", distanceText: "约 38 公里", summary: "地铁为主，建议预留充足换乘时间。" },
          { from: "北京环球度假区", to: "海淀住宿区域", mode: "public_transit", durationText: "约 90-120 分钟", distanceText: "约 38 公里", summary: "闭园后客流大，返程建议错峰。" }
        ]
      },
      {
        id: "day-4",
        title: "大兴机场方向离京",
        date: "Day 4",
        weather: "待调用天气 API",
        pace: "balanced",
        stops: [
          { time: "10:00", name: "海淀住宿区域", type: "hotel_area", lng: 116.306, lat: 39.975, note: "退房并预留行李时间。" },
          { time: "12:00", name: "北京大兴国际机场", type: "airport", lng: 116.410, lat: 39.509, note: "建议至少提前 2 小时到达机场。" }
        ],
        legs: [
          { from: "海淀住宿区域", to: "北京大兴国际机场", mode: "public_transit", durationText: "约 90-120 分钟", distanceText: "约 55 公里", summary: "可走地铁/机场线组合，行李多建议打车。" }
        ]
      }
    ]
  };
}

/**
 * 从以下来源解析 Key，按优先级：
 *   1. Shell 环境变量 (process.env)
 *   2. ~/.openclaw/openclaw.json → skills.entries.amap-roadbook.env
 */
function resolveKey(name) {
  // 1. 环境变量
  let key = process.env[name] || '';
  if (key) return key;

  // 2. openclaw.json
  const configPath = path.resolve(process.env.HOME || '', '.openclaw/openclaw.json');
  try {
    if (!fs.existsSync(configPath)) {
      console.warn(`  ⚠️  ${name}: 配置文件 ${configPath} 不存在，跳过。`);
      return '';
    }
    const raw = fs.readFileSync(configPath, 'utf8');
    const config = JSON.parse(raw);
    key = config?.skills?.entries?.['amap-roadbook']?.env?.[name] || '';
    if (!key) {
      console.warn(`  ⚠️  ${name}: 在 ${configPath} 中未找到 skills.entries.amap-roadbook.env.${name}`);
    }
    return key;
  } catch (err) {
    console.warn(`  ⚠️  ${name}: 读取 ${configPath} 失败 - ${err.message}`);
    return '';
  }
}

function resolveApiKey() {
  return resolveKey('AMAP_JS_API_KEY');
}

async function enrichWithPOI(source) {
  const webKey = resolveKey('AMAP_WEB_SERVICE_KEY');
  if (!webKey) {
    console.warn('⚠️  AMAP_WEB_SERVICE_KEY 未设置，跳过 POI 数据补充。');
    return;
  }

  const days = source.days || [];
  let total = 0, found = 0;

  for (let di = 0; di < days.length; di++) {
    const stops = days[di].stops || [];
    for (let si = 0; si < stops.length; si++) {
      const stop = stops[si];
      const name = stop.name || '';
      // Skip very short or obviously non-POI names (stations, hotels with parens, dining, rest)
      if (name.length < 2) continue;

      total++;
      try {
        const params = new URLSearchParams({
          key: webKey,
          keywords: name,
          city_limit: 'false',
          show_fields: 'business,photos',
          page_size: '1'
        });
        const url = `https://restapi.amap.com/v5/place/text?${params}`;
        const resp = await fetch(url);
        const data = await resp.json();

        if (data.status === '1' && data.pois && data.pois.length > 0) {
          const poi = data.pois[0];
          const biz = poi.business || {};
          stop.poiPhotos = (poi.photos || []).map(p => ({
            title: p.title || '',
            url: p.url
          }));
          if (biz.rating) stop.poiRating = biz.rating;
          if (biz.tel) stop.poiTel = biz.tel;
          if (biz.opentime_today) stop.poiHours = biz.opentime_today;
          if (biz.keytag) stop.poiTag = biz.keytag;
          if (biz.rectag) stop.poiRecTag = biz.rectag;
          found++;
        }
      } catch (err) {
        // Silently skip failed lookups
      }
    }
  }

  if (total > 0) {
    console.log(`ℹ️  POI 数据补充：${found}/${total} 个地点匹配成功`);
  }
}

function downsamplePoints(points, maxPoints) {
  if (points.length <= maxPoints) return points;
  var step = Math.ceil(points.length / maxPoints);
  var result = [];
  for (var i = 0; i < points.length; i += step) {
    result.push(points[i]);
  }
  if (result[result.length - 1] !== points[points.length - 1]) {
    result.push(points[points.length - 1]);
  }
  return result;
}

function addPolyline(polylineStr, points) {
  if (!polylineStr) return;
  var coords = polylineStr.split(';');
  for (var i = 0; i < coords.length; i++) {
    if (coords[i]) {
      var ll = coords[i].split(',');
      var lng = parseFloat(ll[0]), lat = parseFloat(ll[1]);
      if (!isNaN(lng) && !isNaN(lat)) {
        points.push([lng, lat]);
      }
    }
  }
}

function formatDuration(seconds) {
  var n = Number(seconds);
  if (!Number.isFinite(n) || n <= 0) return '';
  var minutes = Math.max(1, Math.round(n / 60));
  if (minutes < 60) return `约${minutes}分钟`;
  var hours = Math.floor(minutes / 60);
  var rest = minutes % 60;
  return rest ? `约${hours}小时${rest}分钟` : `约${hours}小时`;
}

function formatDistance(meters) {
  var n = Number(meters);
  if (!Number.isFinite(n) || n <= 0) return '';
  if (n < 1000) return `约${Math.round(n)}米`;
  return `约${(n / 1000).toFixed(n < 10000 ? 1 : 0)}公里`;
}

function normalizeName(value) {
  return String(value || '')
    .replace(/[（(].*?[）)]/g, '')
    .replace(/[\/／].*$/g, '')
    .replace(/住宿|酒店|青旅|附近|区域|大街|公园|博物院/g, '')
    .replace(/\s+/g, '')
    .trim();
}

function namesMatch(a, b) {
  if (!a || !b) return false;
  if (a === b) return true;
  var na = normalizeName(a);
  var nb = normalizeName(b);
  if (!na || !nb) return false;
  return na === nb || na.includes(nb) || nb.includes(na);
}

function findStopForLeg(stops, name) {
  if (!name) return null;
  for (var i = 0; i < stops.length; i++) {
    if (stops[i].name === name) return { ...stops[i], routeResolvedBy: 'stop-exact' };
  }
  for (var j = 0; j < stops.length; j++) {
    if (namesMatch(stops[j].name, name)) return { ...stops[j], routeResolvedBy: 'stop-fuzzy' };
  }
  return null;
}

function readAdcode(value) {
  if (!value) return '';
  if (typeof value === 'string') return '';
  return value.adcode || value.citycode || '';
}

function readCityLabel(value) {
  if (!value) return '';
  if (typeof value === 'string') return value;
  return value.label || value.name || value.city || '';
}

function parseLocation(value) {
  if (!value || typeof value !== 'string') return null;
  var parts = value.split(',');
  if (parts.length < 2) return null;
  var lng = Number(parts[0]);
  var lat = Number(parts[1]);
  if (!Number.isFinite(lng) || !Number.isFinite(lat)) return null;
  return { lng, lat };
}

async function resolveRouteEndpoint({ webKey, name, source, cache }) {
  if (!name) return null;
  if (cache.has(name)) return cache.get(name);

  var city = readCityLabel(source.destination) || readCityLabel(source.origin);
  var adcode = readAdcode(source.destination) || readAdcode(source.origin);
  var candidates = [];
  if (name.includes('住宿') || name.includes('酒店') || name.includes('青旅')) {
    var areaName = name.replace(/住宿|酒店|青旅|附近|区域/g, '').trim();
    if (areaName) candidates.push(areaName);
    var lodgingArea = source.lodging && (source.lodging.area || source.lodging.name || source.lodging.address);
    if (lodgingArea) candidates.push(String(lodgingArea));
  }
  candidates.push(name);

  for (var ci = 0; ci < candidates.length; ci++) {
    var keyword = candidates[ci];
    try {
      var placeParams = new URLSearchParams({
        key: webKey,
        keywords: keyword,
        city: adcode || city,
        city_limit: 'false',
        page_size: '1',
        output: 'json'
      });
      var placeResp = await fetch(`https://restapi.amap.com/v5/place/text?${placeParams}`);
      var placeData = await placeResp.json();
      if (placeData.status === '1' && placeData.pois && placeData.pois.length > 0) {
        var poi = placeData.pois[0];
        var loc = parseLocation(poi.location);
        if (loc) {
          var resolvedPoi = {
            name,
            lng: loc.lng,
            lat: loc.lat,
            routeResolvedBy: 'poi',
            routeResolvedName: poi.name || keyword
          };
          cache.set(name, resolvedPoi);
          return resolvedPoi;
        }
      }
    } catch {}

    try {
      var geoParams = new URLSearchParams({
        key: webKey,
        address: city ? `${city}${keyword}` : keyword,
        city: adcode || city,
        output: 'json'
      });
      var geoResp = await fetch(`https://restapi.amap.com/v3/geocode/geo?${geoParams}`);
      var geoData = await geoResp.json();
      if (geoData.status === '1' && geoData.geocodes && geoData.geocodes.length > 0) {
        var geo = geoData.geocodes[0];
        var geoLoc = parseLocation(geo.location);
        if (geoLoc) {
          var resolvedGeo = {
            name,
            lng: geoLoc.lng,
            lat: geoLoc.lat,
            routeResolvedBy: 'geocode',
            routeResolvedName: geo.formatted_address || keyword
          };
          cache.set(name, resolvedGeo);
          return resolvedGeo;
        }
      }
    } catch {}
  }

  cache.set(name, null);
  return null;
}

async function queryStandardRoute({ webKey, apiType, originStop, destStop }) {
  const params = new URLSearchParams({
    key: webKey,
    origin: `${originStop.lng},${originStop.lat}`,
    destination: `${destStop.lng},${destStop.lat}`,
    output: 'json'
  });
  const url = `https://restapi.amap.com/v3/direction/${apiType}?${params}`;
  const resp = await fetch(url);
  const data = await resp.json();

  if (data.status !== '1' || !data.route || !data.route.paths || data.route.paths.length === 0) {
    return { ok: false, error: data.info || data.infocode || 'no route path' };
  }

  const routePath = data.route.paths[0];
  const steps = routePath.steps || [];
  var points = [];
  for (var i = 0; i < steps.length; i++) {
    addPolyline(steps[i].polyline, points);
  }

  if (points.length < 2) {
    return { ok: false, error: 'empty route polyline' };
  }

  return {
    ok: true,
    routePoints: downsamplePoints(points, apiType === 'walking' ? 120 : 100),
    durationText: formatDuration(routePath.duration),
    distanceText: formatDistance(routePath.distance)
  };
}

async function queryTransitRoute({ webKey, originStop, destStop, city, cityd }) {
  const params = new URLSearchParams({
    key: webKey,
    origin: `${originStop.lng},${originStop.lat}`,
    destination: `${destStop.lng},${destStop.lat}`,
    city,
    cityd,
    output: 'json',
    extensions: 'all'
  });
  const url = `https://restapi.amap.com/v3/direction/transit/integrated?${params}`;
  const resp = await fetch(url);
  const data = await resp.json();

  if (data.status !== '1' || !data.route || !data.route.transits || data.route.transits.length === 0) {
    return { ok: false, error: data.info || data.infocode || 'no transit route' };
  }

  const transit = data.route.transits[0];
  const segs = transit.segments || [];
  var points = [];
  for (var tsi = 0; tsi < segs.length; tsi++) {
    var seg = segs[tsi];
    if (seg.walking && seg.walking.steps) {
      for (var ws = 0; ws < seg.walking.steps.length; ws++) {
        addPolyline(seg.walking.steps[ws].polyline, points);
      }
    }
    if (seg.bus && seg.bus.buslines) {
      for (var bl = 0; bl < seg.bus.buslines.length; bl++) {
        addPolyline(seg.bus.buslines[bl].polyline, points);
      }
    }
    if (seg.railway && seg.railway.polyline) {
      addPolyline(seg.railway.polyline, points);
    }
  }

  if (points.length < 2) {
    return { ok: false, error: 'empty transit polyline' };
  }

  return {
    ok: true,
    routePoints: downsamplePoints(points, 160),
    durationText: formatDuration(transit.duration),
    distanceText: formatDistance(transit.distance)
  };
}

async function enrichWithRoutes(source) {
  const webKey = resolveKey('AMAP_WEB_SERVICE_KEY');
  if (!webKey) {
    console.warn('⚠️  AMAP_WEB_SERVICE_KEY 未设置，跳过路线规划。');
    return;
  }

  const days = source.days || [];
  let total = 0, done = 0, fallbackDone = 0, skipped = 0, failed = 0;
  const city = readAdcode(source.destination) || readAdcode(source.origin);
  const cityd = readAdcode(source.destination) || city;
  const endpointCache = new Map();

  for (let di = 0; di < days.length; di++) {
    const legs = days[di].legs || [];
    for (let li = 0; li < legs.length; li++) {
      const leg = legs[li];
      const mode = (leg.mode || '').toLowerCase();

      let apiType = null;
      if (mode === 'walk') apiType = 'walking';
      else if (mode === 'taxi' || mode === 'drive' || mode === 'driving') apiType = 'driving';
      else if (mode === 'bike' || mode === 'bicycling') apiType = 'bicycling';
      else if (mode === 'public_transit') apiType = 'transit';

      if (!apiType) {
        leg.routeStatus = 'skipped';
        leg.routeSource = mode === 'rail' || mode === 'flight' ? 'intercity' : 'unsupported-mode';
        skipped++;
        continue;
      }

      var stops = days[di].stops || [];
      var originStop = findStopForLeg(stops, leg.from) || await resolveRouteEndpoint({ webKey, name: leg.from, source, cache: endpointCache });
      var destStop = findStopForLeg(stops, leg.to) || await resolveRouteEndpoint({ webKey, name: leg.to, source, cache: endpointCache });

      if (!originStop || !destStop) {
        leg.routeStatus = 'failed';
        leg.routeSource = 'missing-stop';
        failed++;
        continue;
      }
      if (!Number.isFinite(originStop.lng) || !Number.isFinite(originStop.lat) || !Number.isFinite(destStop.lng) || !Number.isFinite(destStop.lat)) {
        leg.routeStatus = 'failed';
        leg.routeSource = 'missing-coordinate';
        failed++;
        continue;
      }

      total++;
      try {
        var result = null;
        if (apiType === 'transit') {
          result = await queryTransitRoute({ webKey, originStop, destStop, city, cityd });
          if (!result.ok) {
            result = await queryStandardRoute({ webKey, apiType: 'driving', originStop, destStop });
            if (result.ok) {
              result.routeSource = 'driving-fallback';
              result.routeStatus = 'fallback';
            }
          }
        } else {
          result = await queryStandardRoute({ webKey, apiType, originStop, destStop });
          if (!result.ok && apiType === 'walking') {
            result = await queryStandardRoute({ webKey, apiType: 'driving', originStop, destStop });
            if (result.ok) {
              result.routeSource = 'driving-fallback';
              result.routeStatus = 'fallback';
            }
          }
        }

        if (result && result.ok) {
          leg.routePoints = result.routePoints;
          leg.routeStatus = result.routeStatus || 'ok';
          leg.routeSource = result.routeSource || apiType;
          leg.routeOriginName = originStop.name;
          leg.routeDestinationName = destStop.name;
          leg.routeOriginResolvedBy = originStop.routeResolvedBy || 'stop';
          leg.routeDestinationResolvedBy = destStop.routeResolvedBy || 'stop';
          if (originStop.routeResolvedName) leg.routeOriginResolvedName = originStop.routeResolvedName;
          if (destStop.routeResolvedName) leg.routeDestinationResolvedName = destStop.routeResolvedName;
          if (result.durationText) leg.durationText = result.durationText;
          if (result.distanceText) leg.distanceText = result.distanceText;
          if (leg.routeStatus === 'fallback') fallbackDone++;
          else done++;
        } else {
          leg.routeStatus = 'failed';
          leg.routeSource = apiType;
          leg.routeError = result?.error || 'route query failed';
          failed++;
        }
      } catch (err) {
        leg.routeStatus = 'failed';
        leg.routeSource = apiType;
        leg.routeError = err.message || 'route query error';
        failed++;
      }
    }
  }

  if (total > 0) {
    console.log(`ℹ️  路线规划：${done}/${total} 段真实线路，${fallbackDone} 段道路形态兜底，${failed} 段失败，${skipped} 段跳过`);
  }
}

async function main() {
  const inputPath = readArg("input");
  const publish = hasArg("publish");
  const publishId = publish ? (readArg("publish-id") || randomUUID()) : null;
  if (publish) validatePublishId(publishId);

  const outputDir = publish
    ? path.resolve(readArg("output-dir") ?? path.join(skillRoot, "output", publishId))
    : path.resolve(readArg("output-dir") ?? path.join(skillRoot, "output"));
  const source = inputPath ? await readJson(path.resolve(inputPath)) : fallbackRoadbook();

  // ========== Key 读取与验证 ==========
  const webKey = resolveKey('AMAP_WEB_SERVICE_KEY');
  const jsKey = resolveKey('AMAP_JS_API_KEY');
  const secCode = resolveKey('AMAP_JS_SECURITY_CODE');

  console.log(`🔑  Key 状态：WEB=${webKey ? '✅' : '❌'}  JS=${jsKey ? '✅' : '❌'}  SECCODE=${secCode ? '✅' : '❌'}`);

  const missingKeys = [];
  if (!webKey) missingKeys.push('AMAP_WEB_SERVICE_KEY');
  if (!jsKey) missingKeys.push('AMAP_JS_API_KEY');
  if (!secCode) missingKeys.push('AMAP_JS_SECURITY_CODE');
  if (missingKeys.length) {
    console.error(`❌ 缺少必填高德 Key：${missingKeys.join(', ')}`);
    console.error('   请配置到 Shell 环境变量或 ~/.openclaw/openclaw.json 的 skills.entries.amap-roadbook.env 中。');
    process.exit(1);
  }

  if (jsKey.length < 30) {
    console.warn(`⚠️  AMAP_JS_API_KEY 长度异常（${jsKey.length} 位），预期为 32 位。可能是脱敏值，请检查。`);
  } else if (/^\*+$/.test(jsKey)) {
    console.error('❌ AMAP_JS_API_KEY 被脱敏符号代替（仅包含星号），请传入真实 Key。');
    process.exit(1);
  }
  if (/^\*+$/.test(secCode)) {
    console.error('❌ AMAP_JS_SECURITY_CODE 被脱敏符号代替（仅包含星号），请传入真实安全密钥。');
    process.exit(1);
  }

  // 补充 POI 数据（图片、评分等）
  await enrichWithPOI(source);
  // 补充路线规划 polyline（驾车/步行实际道路）
  await enrichWithRoutes(source);

  const roadbook = {
    ...source,
    amapKey: jsKey,
    amapSecurityCode: secCode,
    generatedAt: new Date().toISOString()
  };

  await fsp.mkdir(outputDir, { recursive: true });
  const jsonPath = path.join(outputDir, "roadbook.json");
  const htmlSource = path.join(skillRoot, "assets", "roadbook.html");
  const htmlPath = path.join(outputDir, publish ? "index.html" : "roadbook.html");

  await fsp.writeFile(jsonPath, JSON.stringify(roadbook, null, 2), "utf8");
  let html = await fsp.readFile(htmlSource, "utf8");
  html = html.replace("__ROADBOOK_JSON__", JSON.stringify(roadbook).replaceAll("</", "<\\/"));
  await fsp.writeFile(htmlPath, html, "utf8");

  // 可选：同时生成 Excel 路书
  const exportExcel = hasArg("excel");
  let xlsxPath = null;
  if (exportExcel) {
    try {
      const exportScript = path.join(skillRoot, "scripts", "export-excel.mjs");
      xlsxPath = path.join(outputDir, "roadbook.xlsx");
      execSync(
        `node "${exportScript}" --input "${jsonPath}" --output "${xlsxPath}"`,
        { stdio: "inherit", cwd: skillRoot }
      );
    } catch (e) {
      console.warn(`⚠️  Excel 导出失败: ${e.message}`);
    }
  }

  const upload = publish ? await publishFiles({ publishId, htmlPath, jsonPath, xlsxPath }) : null;
  const publicHtmlUrl = upload?.htmlUrl || (publish ? `${PUBLIC_BASE_URL}/${publishId}/` : null);
  const publicExcelUrl = upload?.xlsxUrl || (publish && xlsxPath ? `${PUBLIC_BASE_URL}/${publishId}/roadbook.xlsx` : null);

  console.log(JSON.stringify({
    publishId: upload?.publishId || publishId,
    publicHtmlUrl,
    publicExcelUrl,
    publishEndpoint: upload?.endpoint || null,
    remoteDir: upload?.remoteDir || null,
    outputDir,
    jsonPath,
    htmlPath,
    xlsxPath
  }, null, 2));
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
