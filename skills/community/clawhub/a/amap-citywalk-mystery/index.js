/**
 * AI CityWalk 剧本杀 - 核心模块
 * 基于高德开放平台 Web Service API
 */

const axios = require('axios');
const fs = require('fs');
const path = require('path');

const BASE_URL = 'https://restapi.amap.com/v3';

/**
 * 加载配置（API Key）
 */
function loadConfig() {
  // 优先从环境变量读取
  if (process.env.AMAP_WEBSERVICE_KEY) {
    return { AMAP_WEBSERVICE_KEY: process.env.AMAP_WEBSERVICE_KEY };
  }
  // 从 config.json 读取
  const configPath = path.join(__dirname, 'config.json');
  if (fs.existsSync(configPath)) {
    return JSON.parse(fs.readFileSync(configPath, 'utf-8'));
  }
  // 从 config.example.json 读取
  const examplePath = path.join(__dirname, 'config.example.json');
  if (fs.existsSync(examplePath)) {
    const config = JSON.parse(fs.readFileSync(examplePath, 'utf-8'));
    if (config.AMAP_WEBSERVICE_KEY && config.AMAP_WEBSERVICE_KEY !== 'your_amap_web_service_key_here') {
      return config;
    }
  }
  console.error('错误：未找到高德 API Key，请配置 config.json 或设置环境变量 AMAP_WEBSERVICE_KEY');
  process.exit(1);
}

/**
 * 解析命令行参数（支持 --key=value 格式）
 */
function parseArgs() {
  const args = {};
  process.argv.slice(2).forEach(arg => {
    const [key, ...valueParts] = arg.replace(/^--/, '').split('=');
    args[key] = valueParts.join('=') || true;
  });
  return args;
}

/**
 * POI 关键词搜索
 * @param {Object} options
 * @param {string} options.keywords - 搜索关键词
 * @param {string} options.city - 城市名称
 * @param {string} [options.types] - POI 类型编码
 * @param {string} [options.location] - 中心点坐标 "经度,纬度"
 * @param {number} [options.radius] - 搜索半径（米）
 * @param {number} [options.page] - 页码
 * @param {number} [options.offset] - 每页数量
 */
async function searchPOI(options) {
  const config = loadConfig();
  const params = {
    key: config.AMAP_WEBSERVICE_KEY,
    keywords: options.keywords,
    city: options.city || '',
    types: options.types || '',
    location: options.location || '',
    radius: options.radius || 3000,
    page: options.page || 1,
    offset: options.offset || 25,
    output: 'json',
    extensions: 'all'
  };
  // 移除空值
  Object.keys(params).forEach(k => { if (!params[k]) delete params[k]; });

  const response = await axios.get(`${BASE_URL}/place/text`, { params });
  const data = response.data;

  if (data.status !== '1') {
    throw new Error(`POI 搜索失败: ${data.info} (infocode: ${data.infocode})`);
  }

  return {
    count: parseInt(data.count),
    pois: (data.pois || []).map(poi => ({
      id: poi.id,
      name: poi.name,
      type: poi.type,
      typecode: poi.typecode,
      address: poi.address,
      location: poi.location,
      tel: poi.tel,
      distance: poi.distance,
      biz_ext: poi.biz_ext,
      photos: poi.photos || [],
      rating: poi.biz_ext?.rating,
      cost: poi.biz_ext?.cost
    }))
  };
}

/**
 * 地理编码（地址转坐标）
 */
async function geocode(address, city) {
  const config = loadConfig();
  const response = await axios.get(`${BASE_URL}/geocode/geo`, {
    params: {
      key: config.AMAP_WEBSERVICE_KEY,
      address,
      city: city || '',
      output: 'json'
    }
  });

  const data = response.data;
  if (data.status !== '1' || !data.geocodes || data.geocodes.length === 0) {
    throw new Error(`地理编码失败: ${data.info}`);
  }

  const geo = data.geocodes[0];
  return {
    formatted_address: geo.formatted_address,
    province: geo.province,
    city: geo.city,
    district: geo.district,
    location: geo.location,
    level: geo.level
  };
}

/**
 * 路径规划
 * @param {Object} options
 * @param {string} options.type - 出行方式：walking/driving/riding/transfer
 * @param {string} options.origin - 起点 "经度,纬度"
 * @param {string} options.destination - 终点 "经度,纬度"
 * @param {string} [options.waypoints] - 途经点
 * @param {string} [options.city] - 城市（公交规划必需）
 */
async function planRoute(options) {
  const config = loadConfig();
  const typeMap = {
    walking: '/direction/walking',
    driving: '/direction/driving',
    riding: '/direction/bicycling',
    transfer: '/direction/transit/integrated'
  };

  const apiPath = typeMap[options.type] || typeMap.walking;
  const params = {
    key: config.AMAP_WEBSERVICE_KEY,
    origin: options.origin,
    destination: options.destination,
    output: 'json'
  };

  if (options.waypoints) params.waypoints = options.waypoints;
  if (options.city) params.city = options.city;
  if (options.type === 'driving') params.strategy = 10; // 躲避拥堵

  const response = await axios.get(`${BASE_URL}${apiPath}`, { params });
  const data = response.data;

  if (data.status !== '1') {
    throw new Error(`路径规划失败: ${data.info} (infocode: ${data.infocode})`);
  }

  const route = data.route;
  const firstPath = route.paths[0];

  return {
    origin: route.origin,
    destination: route.destination,
    distance: firstPath.distance,
    duration: firstPath.duration,
    steps: (firstPath.steps || []).map(step => ({
      instruction: step.instruction,
      road: step.road,
      distance: step.distance,
      duration: step.duration,
      action: step.action,
      polyline: step.polyline
    })),
    type: options.type,
    totalDistance: `${(parseInt(firstPath.distance) / 1000).toFixed(1)}km`,
    totalDuration: `${Math.ceil(parseInt(firstPath.duration) / 60)}分钟`
  };
}

/**
 * 生成地图可视化链接
 * @param {Array} mapData - 地图数据数组
 * @returns {string} 地图链接
 */
function generateMapLink(mapData) {
  const encoded = encodeURIComponent(JSON.stringify(mapData));
  return `https://a.amap.com/jsapi_demo_show/static/openclaw/travel_plan.html?data=${encoded}`;
}

/**
 * 生成 CityWalk 剧本杀的地图数据
 * @param {Array} storyLocations - 故事地点数组
 * @param {Array} routes - 路线数组
 */
function generateCityWalkMapData(storyLocations, routes) {
  const mapData = [];

  // 添加故事地点
  storyLocations.forEach((loc, index) => {
    mapData.push({
      type: 'poi',
      lnglat: loc.location.split(',').map(Number),
      sort: `第${index + 1}站`,
      text: loc.name,
      remark: loc.clue || loc.description || ''
    });
  });

  // 添加路线
  if (routes && routes.length > 0) {
    routes.forEach(route => {
      mapData.push({
        type: 'route',
        routeType: route.type || 'walking',
        start: route.origin.split(',').map(Number),
        end: route.destination.split(',').map(Number),
        remark: (route.totalDistance && route.totalDuration) ? `${route.totalDistance} / ${route.totalDuration}` : `步行路线`
      });
    });
  }

  return mapData;
}

/**
 * 天气查询
 */
async function getWeather(city) {
  const config = loadConfig();
  const response = await axios.get(`${BASE_URL}/weather/weatherInfo`, {
    params: {
      key: config.AMAP_WEBSERVICE_KEY,
      city,
      output: 'json',
      extensions: 'base'
    }
  });

  const data = response.data;
  if (data.status !== '1' || !data.lives || data.lives.length === 0) {
    throw new Error(`天气查询失败: ${data.info}`);
  }

  return data.lives[0];
}

// 导出所有功能
module.exports = {
  searchPOI,
  geocode,
  planRoute,
  generateMapLink,
  generateCityWalkMapData,
  getWeather,
  loadConfig,
  parseArgs
};
