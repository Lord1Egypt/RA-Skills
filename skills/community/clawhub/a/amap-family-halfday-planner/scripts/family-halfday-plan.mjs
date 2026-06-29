#!/usr/bin/env node

const args = parseArgs(process.argv.slice(2));
const key = process.env.AMAP_API_KEY || process.env.AMAP_WEBSERVICE_KEY || "";

if (!key) {
  console.error("Missing AMAP_API_KEY. Set AMAP_API_KEY or AMAP_WEBSERVICE_KEY before running this skill.");
  process.exit(1);
}

const form = {
  origin: args.origin || "杭州西湖文化广场",
  city: args.city || inferCity(args.origin || "") || "杭州市",
  age: args.age || "4-6岁",
  mode: args.mode || "步行为主",
  intensity: args.intensity || "轻松",
  needs: splitList(args.needs || "推车友好,午餐需求"),
  preferences: splitList(args.preferences || "自然探索,博物馆,游乐互动,午餐友好"),
};

try {
  const plan = await buildPlan(form);
  printPlan(plan);
} catch (error) {
  console.error(`Failed to generate family half-day plan: ${error.message}`);
  process.exit(1);
}

async function buildPlan(form) {
  const geo = await amapGet("/v3/geocode/geo", {
    address: normalizeAddressForCity(form.origin, form.city),
    city: form.city,
  });
  const location = geo.geocodes?.[0]?.location;
  const city = geo.geocodes?.[0]?.city || form.city || "";

  if (!location) {
    throw new Error(`Cannot geocode origin: ${form.origin}`);
  }

  const searchTasks = [
    ["park", ["公园", "绿地", "广场"]],
    ["museum", ["博物馆", "科技馆", "展览馆"]],
    ["lunch", ["餐厅", "亲子餐厅", "简餐"]],
    ["playground", ["儿童乐园", "游乐场", "亲子活动"]],
  ];

  const found = {};
  for (const [id, keywords] of searchTasks) {
    found[id] = await searchAround(location, keywords, city);
  }

  const stops = [
    makeStop(found.park, "09:30", "公园探秘：寻找大树朋友", "找到三种不同树叶，给大树朋友拍张照。", "早上空气清新，适合慢慢走，注意防晒和补水。"),
    makeStop(found.museum, "10:20", "博物馆小侦探", "找出恐龙、星球或城市模型，完成一枚发现徽章。", "室内凉爽，适合避暑和恢复体力。"),
    makeStop(found.lunch, "11:30", "能量补给站：美味小冒险", "尝试一种新口味，为美食打个小星星。", "优先选择儿童餐、洗手间和座位充足的餐厅。"),
    makeStop(found.playground, "12:35", "活力充电站", "玩一次最喜欢的滑梯或游乐项目，完成今日能量充电。", "家长可在旁休息，注意滑梯口和湖边安全。"),
  ];

  const legs = await buildLegs(stops);
  const totalMeters = legs.reduce((sum, leg) => sum + leg.distance, 0);

  return {
    ...form,
    city,
    stops,
    legs,
    totalMeters,
    duration: form.intensity === "挑战" ? "约4.5小时" : "约4小时",
  };
}

async function searchAround(location, keywords, city) {
  const candidates = Array.isArray(keywords) ? keywords : [keywords];

  for (const keyword of candidates) {
    try {
      const data = await amapGet("/v5/place/around", {
        location,
        keywords: keyword,
        city,
        radius: 8000,
        page_size: 10,
        show_fields: "business",
      });

      const pois = data.pois || [];
      const poi = pois.find((item) => item.location && item.name) || pois[0] || null;
      if (poi) {
        return poi;
      }
    } catch (_error) {
      // Try the next keyword; some category queries can return engine data errors.
    }
  }

  return null;
}

function makeStop(poi, time, fallbackTitle, mission, parentNote) {
  return {
    time,
    title: poi?.name ? `${fallbackTitle.split("：")[0]}：${poi.name}` : fallbackTitle,
    mission,
    parentNote,
    address: Array.isArray(poi?.address) ? poi.address.join("") : poi?.address || "暂无地址",
    location: poi?.location || "",
    type: poi?.type || "",
  };
}

async function buildLegs(stops) {
  const legs = [];
  for (let index = 1; index < stops.length; index += 1) {
    const prev = stops[index - 1];
    const next = stops[index];
    let distance = 0;
    let duration = 0;
    if (prev.location && next.location) {
      const data = await amapGet("/v5/direction/walking", {
        origin: prev.location,
        destination: next.location,
      });
      const path = data.route?.paths?.[0];
      distance = Number(path?.distance || 0);
      duration = Number(path?.duration || 0);
    }
    legs.push({ from: prev.title, to: next.title, distance, duration });
  }
  return legs;
}

async function amapGet(endpoint, params) {
  const url = new URL(`https://restapi.amap.com${endpoint}`);
  url.searchParams.set("key", key);
  for (const [name, value] of Object.entries(params)) {
    if (value !== undefined && value !== null && value !== "") {
      url.searchParams.set(name, String(value));
    }
  }

  let lastError = null;
  for (let attempt = 0; attempt < 4; attempt += 1) {
    if (attempt > 0) {
      await delay(900 * attempt);
    }

    const response = await fetch(url, { headers: { Accept: "application/json" } });
    if (!response.ok) {
      lastError = new Error(`Amap API HTTP ${response.status}`);
      continue;
    }

    const data = await response.json();
    if (!data.status || data.status === "1") {
      return data;
    }

    lastError = new Error(data.info || "Amap API returned an error");
    if (!isRetryableAmapError(data.info)) {
      break;
    }
  }

  throw lastError || new Error("Amap API returned an error");
}

function delay(ms) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

function isRetryableAmapError(info) {
  return ["CUQPS_HAS_EXCEEDED_THE_LIMIT", "ENGINE_RESPONSE_DATA_ERROR"].includes(info);
}

function printPlan(plan) {
  const km = plan.totalMeters > 0 ? `${(plan.totalMeters / 1000).toFixed(1)}公里` : "待高德路线返回";

  console.log(`# 亲子半日游方案：小小探险家的一天\n`);
  console.log(`## 家庭画像\n`);
  console.log(`- 出发地：${plan.origin}`);
  if (plan.city) console.log(`- 城市：${plan.city}`);
  console.log(`- 孩子年龄：${plan.age}`);
  console.log(`- 出行方式：${plan.mode}`);
  console.log(`- 步行强度：${plan.intensity}`);
  console.log(`- 偏好：${plan.preferences.join("、")}`);
  console.log(`- 需求：${plan.needs.join("、")}\n`);

  console.log(`## 路线总览\n`);
  console.log(`- 推荐时长：${plan.duration}`);
  console.log(`- 步行负担：${km}`);
  console.log(`- 路线结构：自然探索 → 室内学习 → 午餐补给 → 游乐放电\n`);

  console.log(`## 路线故事\n`);
  plan.stops.forEach((stop, index) => {
    const leg = index > 0 ? plan.legs[index - 1] : null;
    const walk = leg?.distance ? `，上一站步行约${Math.round(leg.distance)}米` : "";
    console.log(`${index + 1}. ${stop.time} ${stop.title}${walk}`);
    console.log(`   - 小任务：${stop.mission}`);
    console.log(`   - 地址：${stop.address}`);
    console.log(`   - 家长备注：${stop.parentNote}\n`);
  });

  console.log(`## 行程表\n`);
  console.log(`| 时间 | 安排 | 亲子目的 | 家长关注 |`);
  console.log(`| --- | --- | --- | --- |`);
  plan.stops.forEach((stop) => {
    console.log(`| ${stop.time} | ${stop.title} | ${stop.mission} | ${stop.parentNote} |`);
  });
  console.log("");

  console.log(`## 家庭出行准备清单\n`);
  const checklist = [
    "推车：低龄孩子建议携带，优先选择推车友好路线。",
    "午餐：建议 11:30 左右错峰用餐。",
    "洗手间：每一段路线前后都预留洗手间检查。",
    "补水：每 45-60 分钟安排一次补水或休息。",
    "防晒防雨：建议带帽子、雨伞和轻便外套。",
    plan.needs.includes("避开人流高峰") ? "人流：已优先考虑避开热门高峰。" : "人流：周末热门点位 10-11 点可能排队。",
    "安全：湖边、路口和游乐设施出口需要重点看护。",
  ];
  checklist.forEach((item) => console.log(`- ${item}`));
  console.log("");

  console.log(`## 调用的高德能力\n`);
  console.log(`- 地理编码：将「${plan.origin}」转换为经纬度。`);
  console.log(`- 周边搜索：搜索公园、博物馆、亲子餐饮、儿童乐园等 POI。`);
  console.log(`- 步行路径规划：估算相邻站点之间的步行距离。\n`);

  console.log(`## 下一步建议\n`);
  console.log(`把这条路线导入高德地图 App，出发前再检查天气、营业时间和临时闭园信息。`);
}

function parseArgs(argv) {
  const parsed = {};
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (!token.startsWith("--")) continue;
    const key = token.slice(2);
    const value = argv[index + 1] && !argv[index + 1].startsWith("--") ? argv[++index] : "true";
    parsed[key] = value;
  }
  return parsed;
}

function splitList(value) {
  return String(value)
    .split(/[,，、]/)
    .map((item) => item.trim())
    .filter(Boolean);
}

function inferCity(origin) {
  const cityMap = [
    ["北京", "北京市"],
    ["上海", "上海市"],
    ["广州", "广州市"],
    ["深圳", "深圳市"],
    ["杭州", "杭州市"],
    ["成都", "成都市"],
    ["南京", "南京市"],
    ["武汉", "武汉市"],
    ["西安", "西安市"],
    ["苏州", "苏州市"],
    ["重庆", "重庆市"],
    ["天津", "天津市"],
  ];

  const match = cityMap.find(([keyword]) => origin.includes(keyword));
  return match?.[1] || "";
}

function normalizeAddressForCity(origin, city) {
  if (!city) return origin;
  const cityShort = city.replace(/市$/, "");
  return origin.startsWith(cityShort) ? origin.slice(cityShort.length) : origin;
}
