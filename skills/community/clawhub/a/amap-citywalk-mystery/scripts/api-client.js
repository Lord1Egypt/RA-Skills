#!/usr/bin/env node

/**
 * CityWalk API 客户端
 * 
 * 封装所有线上服务调用，供 AI Skill 使用
 * 
 * 用法：
 *   node api-client.js <command> [options]
 * 
 * 命令：
 *   location              - 获取定位链接
 *   weather <city>        - 查询天气
 *   poi <keywords> <city> - 搜索 POI
 *   route <origin> <destination> - 规划路线
 *   map <data>            - 生成地图
 *   questions <poiIds>    - 查询题库
 *   upload-questions <data> - 上传题目
 *   verify <questionId> <answer> - 校验答案
 *   checkin <poiName> <lat> <lng> - 创建打卡
 */

const axios = require('axios');
const fs = require('fs');
const path = require('path');

const BASE_URL = 'https://www.701study.com/app/citywalk-service';
const SESSION_FILE = path.join(__dirname, '.location-session');

// 工具函数：保存 sessionId
function saveSessionId(sessionId) {
  fs.writeFileSync(SESSION_FILE, sessionId, 'utf8');
}

// 工具函数：读取 sessionId
function loadSessionId() {
  if (fs.existsSync(SESSION_FILE)) {
    return fs.readFileSync(SESSION_FILE, 'utf8').trim();
  }
  return null;
}

// 工具函数：发起 HTTP 请求
async function request(method, path, data) {
  const url = `${BASE_URL}${path}`;
  const resp = await axios({
    method,
    url,
    data: method === 'POST' ? data : undefined,
    params: method === 'GET' ? data : undefined,
    headers: { 'Content-Type': 'application/json' }
  });
  return resp.data;
}

// 命令实现
const commands = {
  // 创建位置会话并返回定位链接
  location: async () => {
    const result = await request('POST', '/api/checkin/create-location');
    saveSessionId(result.sessionId);
    console.log(`LINK=${BASE_URL}/checkin/location?sessionId=${result.sessionId}`);
  },

  // 查询位置结果（自动读取上次保存的 sessionId）
  'location-result': async () => {
    const sessionId = loadSessionId();
    if (!sessionId) {
      console.log('❌ 没有定位会话，请先执行 location 命令');
      return;
    }
    const result = await request('GET', `/api/checkin/location/${sessionId}`);
    if (result.status === 'completed') {
      console.log(`✅ 定位成功！\n城市：${result.city}\n区域：${result.district}\n省份：${result.province}\n纬度：${result.lat}\n经度：${result.lng}\n精度：${result.accuracy || '未知'} 米`);
    } else if (result.status === 'waiting') {
      console.log('⏳ 等待中，用户还未完成定位');
    } else {
      console.log('❌ 会话不存在或已过期，请重新获取定位链接');
    }
  },

  // 查询天气
  weather: async (city) => {
    const result = await request('GET', `/api/amap/weather?city=${encodeURIComponent(city)}`);
    if (result.status === '1' && result.lives) {
      const live = result.lives[0];
      console.log(JSON.stringify({
        city: live.city,
        weather: live.weather,
        temperature: live.temperature + '°C',
        wind: live.windpower + '级 ' + live.winddirection + '风',
        humidity: live.humidity + '%'
      }, null, 2));
    } else {
      console.error('天气查询失败:', result);
    }
  },

  // 搜索 POI
  poi: async (keywords, city, types) => {
    const result = await request('POST', '/api/amap/poi/search', {
      keywords,
      city,
      types: types || ''
    });
    if (result.status === '1' && result.pois) {
      console.log(JSON.stringify(result.pois.slice(0, 10).map(p => ({
        id: p.id,
        name: p.name,
        address: p.address,
        location: p.location,
        type: p.type
      })), null, 2));
    } else {
      console.error('POI 搜索失败:', result);
    }
  },

  // 规划路线
  route: async (origin, destination) => {
    const result = await request('POST', '/api/amap/route/walking', {
      origin,
      destination
    });
    if (result.status === '1' && result.route) {
      const route = result.route.paths[0];
      console.log(JSON.stringify({
        distance: (route.distance / 1000).toFixed(2) + ' km',
        duration: Math.round(route.duration / 60) + ' min',
        steps: route.steps.map(s => ({
          instruction: s.instruction,
          distance: s.distance + 'm'
        }))
      }, null, 2));
    } else {
      console.error('路径规划失败:', result);
    }
  },

  // 生成地图
  map: async (data) => {
    const result = await request('POST', '/api/amap/map/generate', JSON.parse(data));
    console.log(result.mapUrl);
  },

  // 生成地图可视化页面（返回链接）
  'map-view': async (data) => {
    const parsed = JSON.parse(data);
    // 通过 POST 请求获取地图页面 URL
    const result = await request('POST', '/api/amap/map/generate', parsed);
    console.log(result.mapUrl);
  },

  // 查询题库
  questions: async (poiIds) => {
    const result = await request('GET', `/api/questions/batch?poiIds=${poiIds}`);
    console.log(JSON.stringify(result, null, 2));
  },

  // 上传题目
  'upload-questions': async (data) => {
    const result = await request('POST', '/api/questions/batch', JSON.parse(data));
    console.log(JSON.stringify(result, null, 2));
  },

  // 校验答案
  verify: async (questionId, answer, photoVerified) => {
    const result = await request('POST', '/api/questions/verify', {
      questionId,
      userAnswer: answer,
      photoVerified: photoVerified !== 'false'
    });
    console.log(JSON.stringify(result, null, 2));
  },

  // 创建打卡
  checkin: async (poiName, lat, lng) => {
    const result = await request('POST', '/api/checkin/sessions', {
      poiName,
      poiLat: parseFloat(lat),
      poiLng: parseFloat(lng)
    });
    if (result.sessionId) {
      const checkinUrl = `${BASE_URL}/checkin/${result.sessionId}`;
      console.log(JSON.stringify({
        sessionId: result.sessionId,
        checkinUrl: checkinUrl
      }, null, 2));
    } else {
      console.error('创建打卡失败:', result);
    }
  },

  // 剧本管理：请求剧本
  'story-request': async (city, theme, duration) => {
    const result = await request('POST', '/api/story/request', { city, theme, duration });
    if (result.found) {
      console.log(`✅ 找到预置剧本！`);
      console.log(`剧本ID: ${result.storyId}`);
      console.log(`进度ID: ${result.progressId}`);
      console.log(`标题: ${result.title}`);
      console.log(`背景: ${result.background}`);
      console.log(`当前站: ${result.currentStation?.name || '无'}`);
    } else {
      console.log(`📝 未找到预置剧本，需要 AI 生成`);
      console.log(`城市: ${result.city}`);
      console.log(`主题: ${result.theme}`);
      console.log(`建议 POI:`);
      (result.suggestedPOIs || []).forEach((poi, i) => {
        console.log(`  ${i + 1}. ${poi.name} - ${poi.address} (${poi.lat},${poi.lng})`);
      });
    }
  },

  // 剧本管理：创建剧本
  'story-create': async (jsonFile) => {
    if (!jsonFile) {
      console.error('请提供剧本 JSON 文件路径');
      return;
    }
    const storyData = JSON.parse(fs.readFileSync(jsonFile, 'utf8'));
    const result = await request('POST', '/api/story/create', storyData);
    console.log(`✅ 剧本创建成功！`);
    console.log(`剧本ID: ${result.storyId}`);
    console.log(`进度ID: ${result.progressId}`);
    console.log(`站点数: ${result.stationsCount}`);
  },

  // 剧本管理：获取当前站
  'story-current': async (storyId, progressId) => {
    const result = await request('GET', `/api/story/${storyId}/current?progressId=${progressId}`);
    if (result.completed) {
      console.log('🎉 剧本已完成！');
    } else {
      console.log(`📍 当前站: ${result.name}`);
      console.log(`地址: ${result.address}`);
      console.log(`坐标: ${result.lat},${result.lng}`);
      console.log(`剧情: ${result.storyText}`);
      console.log(`任务: ${result.task}`);
      console.log(`拍照要求: ${result.photoRequirement || '无'}`);
      console.log(`分值: ${result.score}分 (加分任务: ${result.bonusScore}分)`);
    }
  },

  // 剧本管理：打卡验证
  'story-checkin': async (storyId, progressId, stationId) => {
    const locationSession = loadSessionId();
    if (!locationSession) {
      console.error('请先执行 location 命令获取位置');
      return;
    }
    const locationResult = await request('GET', `/api/checkin/location/${locationSession}`);
    if (locationResult.status !== 'completed') {
      console.error('位置信息未完成，请先完成定位');
      return;
    }
    const result = await request('POST', `/api/story/${storyId}/checkin`, {
      progressId,
      stationId,
      lat: locationResult.lat,
      lng: locationResult.lng
    });
    if (result.passed) {
      console.log(`✅ ${result.message}`);
    } else {
      console.log(`❌ ${result.message}`);
    }
  },

  // 剧本管理：提交答案
  'story-answer': async (storyId, progressId, stationId, answer) => {
    const result = await request('POST', `/api/story/${storyId}/answer`, {
      progressId,
      stationId,
      textAnswer: answer
    });
    console.log(result.feedback);
    console.log(`得分: +${result.scoreEarned}`);
    console.log(`总分: ${result.totalScore}`);
    if (!result.correct && result.retries < result.maxRetries) {
      console.log(`重试次数: ${result.retries}/${result.maxRetries}`);
    }
    if (result.revealed) {
      console.log('答案已揭晓，进入下一站');
    }
  },

  // 剧本管理：进入下一站
  'story-next': async (storyId, progressId) => {
    const result = await request('POST', `/api/story/${storyId}/next`, { progressId });
    if (result.completed) {
      console.log(`🎉 剧本完成！`);
      console.log(`总分: ${result.totalScore}/${result.maxScore}`);
      console.log(`评级: ${result.rating.grade} - ${result.rating.name}`);
    } else {
      console.log(`📍 下一站: ${result.name}`);
      console.log(`地址: ${result.address}`);
      console.log(`坐标: ${result.lat},${result.lng}`);
      console.log(`剧情: ${result.storyText}`);
      console.log(`任务: ${result.task}`);
    }
  },

  // 剧本管理：获取结果
  'story-result': async (storyId, progressId) => {
    const result = await request('GET', `/api/story/${storyId}/result?progressId=${progressId}`);
    console.log(`🏆 通关成绩卡`);
    console.log(`标题: ${result.title}`);
    console.log(`总分: ${result.totalScore}/${result.maxScore}`);
    console.log(`评级: ${result.rating.grade} - ${result.rating.name}`);
    console.log(`时长: ${result.duration}`);
    console.log(`\n各站详情:`);
    result.stations.forEach((s, i) => {
      console.log(`  ${i + 1}. ${s.name}: ${s.score}/${s.maxScore}分 ${s.passed ? '✅' : '❌'} ${s.correct ? '✅' : '❌'}`);
    });
  }
};

// 主函数
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (!command || !commands[command]) {
    console.log(`用法: node api-client.js <command> [options]
    
命令:
  location                        - 获取定位链接
  location-result                 - 查询位置结果
  weather <city>                  - 查询天气
  poi <keywords> <city> [types]   - 搜索 POI
  route <origin> <destination>    - 规划路线
  map <data>                      - 生成地图
  questions <poiIds>              - 查询题库
  upload-questions <data>         - 上传题目
  verify <questionId> <answer>    - 校验答案
  checkin <poiName> <lat> <lng>   - 创建打卡
  story-request <city> <theme> <duration> - 请求剧本
  story-create <jsonFile>         - 创建剧本
  story-current <storyId> <progressId> - 获取当前站
  story-checkin <storyId> <progressId> <stationId> - 打卡验证
  story-answer <storyId> <progressId> <stationId> <answer> - 提交答案
  story-next <storyId> <progressId> - 进入下一站
  story-result <storyId> <progressId> - 获取结果

示例:
  node api-client.js location
  node api-client.js weather 杭州
  node api-client.js poi 博物馆 杭州
  node api-client.js story-request 杭州 悬疑 1小时`);
    process.exit(1);
  }

  try {
    await commands[command](...args.slice(1));
  } catch (error) {
    console.error('请求失败:', error.message);
    process.exit(1);
  }
}

main();
