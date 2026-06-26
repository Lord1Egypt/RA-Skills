#!/usr/bin/env node

/**
 * dargue-flag CLI - 达尔盖的旗帜
 * 用于 OpenClaw Agent 调用视频搜索/浏览 API
 * 
 * Usage:
 *   node video-search.js check-key [--api-key sk_xxx]
 *   node video-search.js search --keyword "xxx" [--page 1] [--api-key sk_xxx]
 *   node video-search.js list --category hot [--page 1] [--api-key sk_xxx]
 *   node video-search.js detail --url "view_video.php?viewkey=xxx" [--api-key sk_xxx]
 *   node video-search.js categories [--api-key sk_xxx]
 *   node video-search.js quota [--api-key sk_xxx]
 *   node video-search.js config --api-key sk_xxx [--base-url http://...]
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

// ============ Config ============
const DEFAULT_BASE_URL = 'https://api.4listenapp.com';
const CONFIG_PATH = path.join(process.env.HOME || process.env.USERPROFILE || '/tmp', '.dargue-flag', 'config.json');

function loadConfig() {
  try {
    return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
  } catch (e) {
    return {};
  }
}

function saveConfig(config) {
  const dir = path.dirname(CONFIG_PATH);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2));
}

function getApiKey(args) {
  const idx = args.indexOf('--api-key');
  if (idx !== -1 && args[idx + 1]) return args[idx + 1];
  const config = loadConfig();
  return config.apiKey || '';
}

function getArg(args, name) {
  const idx = args.indexOf(name);
  if (idx !== -1 && args[idx + 1]) return args[idx + 1];
  return null;
}

// ============ HTTP Client ============
function request(method, urlPath, params = {}, apiKey = '') {
  return new Promise((resolve, reject) => {
    const baseUrl = (loadConfig().baseUrl || DEFAULT_BASE_URL).replace(/\/+$/, '');
    const fullUrl = new URL(urlPath, baseUrl);
    
    const isHttps = fullUrl.protocol === 'https:';
    const mod = isHttps ? https : http;
    
    const options = {
      hostname: fullUrl.hostname,
      port: fullUrl.port || (isHttps ? 443 : 80),
      path: fullUrl.pathname + fullUrl.search,
      method: method,
      headers: {
        'X-API-Key': apiKey,
      }
    };

    // Build body
    let body = '';
    if (method === 'POST' && Object.keys(params).length > 0) {
      body = Object.entries(params)
        .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
        .join('&');
      options.headers['Content-Type'] = 'application/x-www-form-urlencoded';
      options.headers['Content-Length'] = Buffer.byteLength(body);
    }

    const req = mod.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          resolve(json);
        } catch (e) {
          reject(new Error(`Invalid JSON response: ${data.substring(0, 200)}`));
        }
      });
    });

    req.on('error', reject);
    req.setTimeout(30000, () => { req.destroy(); reject(new Error('Request timeout')); });
    if (body) req.write(body);
    req.end();
  });
}

// ============ Commands ============

async function checkKey(args) {
  const apiKey = getApiKey(args);
  if (!apiKey) {
    console.log('❌ 未配置 API Key');
    console.log('请运行: node video-search.js config --api-key sk_xxx');
    console.log('获取 API Key: https://t66yskill.com');
    return;
  }
  
  try {
    const result = await request('GET', '/api/video/quota', {}, apiKey);
    if (result.code === 0) {
      const q = result.data;
      console.log(`✅ API Key 有效`);
      console.log(`   配额: ${q.used}/${q.total} (剩余 ${q.remaining})`);
      if (q.expireAt) console.log(`   过期: ${q.expireAt}`);
    } else {
      console.log(`❌ API Key 无效: ${result.message}`);
    }
  } catch (e) {
    console.log(`❌ 验证失败: ${e.message}`);
  }
}

async function search(args) {
  const apiKey = getApiKey(args);
  const keyword = getArg(args, '--keyword') || getArg(args, '-k');
  const page = parseInt(getArg(args, '--page') || '1', 10);
  
  if (!keyword) { console.log('❌ 缺少 --keyword 参数'); return; }
  
  try {
    const result = await request('POST', '/api/video/search', { keyword, page }, apiKey);
    outputList('search', result, { keyword, page });
  } catch (e) {
    console.log(`❌ 搜索失败: ${e.message}`);
  }
}

async function list(args) {
  const apiKey = getApiKey(args);
  const category = getArg(args, '--category') || getArg(args, '-c') || '当前最热';
  const page = parseInt(getArg(args, '--page') || '1', 10);
  
  try {
    const result = await request('POST', '/api/video/list', { category, page }, apiKey);
    outputList('list', result, { category, page });
  } catch (e) {
    console.log(`❌ 获取列表失败: ${e.message}`);
  }
}

async function detail(args) {
  const apiKey = getApiKey(args);
  const url = getArg(args, '--url') || getArg(args, '-u');
  
  if (!url) { console.log('❌ 缺少 --url 参数'); return; }
  
  try {
    const result = await request('POST', '/api/video/detail', { url }, apiKey);
    outputDetail(result);
  } catch (e) {
    console.log(`❌ 获取详情失败: ${e.message}`);
  }
}

async function quota(args) {
  const apiKey = getApiKey(args);
  try {
    const result = await request('GET', '/api/video/quota', {}, apiKey);
    if (result.code === 0) {
      const q = result.data;
      console.log(`📊 配额: ${q.used}/${q.total} (剩余 ${q.remaining})`);
      if (q.expireAt) console.log(`📅 过期: ${q.expireAt}`);
    } else {
      console.log(`❌ ${result.message}`);
    }
  } catch (e) {
    console.log(`❌ 查询失败: ${e.message}`);
  }
}

async function categories(args) {
  const apiKey = getApiKey(args);
  try {
    const result = await request('GET', '/api/video/categories', {}, apiKey);
    if (result.code === 0 && Array.isArray(result.data)) {
      console.log('📁 可用分类:');
      result.data.forEach((f, i) => {
        console.log(`  ${i + 1}. ${f.name}`);
      });
    } else {
      console.log(`❌ ${result.message || '获取分类失败'}`);
    }
  } catch (e) {
    console.log(`❌ 获取分类失败: ${e.message}`);
  }
}

async function config(args) {
  const apiKey = getArg(args, '--api-key');
  const baseUrl = getArg(args, '--base-url');
  
  const cfg = loadConfig();
  if (apiKey) cfg.apiKey = apiKey;
  if (baseUrl) cfg.baseUrl = baseUrl;
  saveConfig(cfg);
  console.log('✅ 配置已保存');
  console.log(`   API Key: ${cfg.apiKey ? cfg.apiKey.substring(0, 7) + '***' : '未设置'}`);
  console.log(`   Base URL: ${cfg.baseUrl || DEFAULT_BASE_URL}`);
}

// ============ Output Formatter ============

function outputList(type, result, ctx) {
  if (result.code !== 0) {
    console.log(`❌ ${result.message || '请求失败'}`);
    return;
  }

  const data = result.data;

  if (!data || (Array.isArray(data) && data.length === 0)) {
    if (type === 'search') {
      console.log(`未找到 "${ctx.keyword}" 相关视频（第${ctx.page}页）`);
    } else {
      console.log(`"${ctx.category}" 第${ctx.page}页暂无视频`);
    }
    return;
  }

  const videos = Array.isArray(data) ? data : (data.list || data.videos || [data]);
  
  if (type === 'search') {
    console.log(`🔍 搜索结果 "${ctx.keyword}"（第${ctx.page}页，共 ${videos.length} 条）\n`);
  } else {
    console.log(`📋 ${ctx.category}（第${ctx.page}页，共 ${videos.length} 条）\n`);
  }

  videos.forEach((v, i) => {
    console.log(`${i + 1}. ${v.title || v.name || '未知标题'}`);
    const parts = [];
    if (v.duration) parts.push(`⏱ ${v.duration}`);
    if (v.views || v.viewCount) parts.push(`👁 ${v.views || v.viewCount}`);
    if (parts.length > 0) console.log(`   ${parts.join(' | ')}`);
    if (v.thumb || v.thumbnail || v.cover) console.log(`   🖼 ${v.thumb || v.thumbnail || v.cover}`);
    if (v.url || v.detail || v.viewkey) console.log(`   🔗 ${v.url || v.detail || v.viewkey}`);
    console.log('');
  });
}

function outputDetail(result) {
  if (result.code !== 0) {
    console.log(`❌ ${result.message || '请求失败'}`);
    return;
  }

  let d = result.data;
  if (!d) {
    console.log('未找到视频详情');
    return;
  }

  // 处理 XVideos 返回格式（嵌套在 data.data.video 里，且 video 是 JSON 字符串）
  let videoData = null;
  let tagsData = null;
  
  if (d.data && typeof d.data === 'object') {
    const inner = d.data;
    if (inner.video) {
      if (typeof inner.video === 'string') {
        try {
          videoData = JSON.parse(inner.video);
        } catch (e) {
          videoData = null;
        }
      } else if (typeof inner.video === 'object') {
        videoData = inner.video;
      }
    }
    if (inner.tags) {
      if (typeof inner.tags === 'string') {
        try {
          tagsData = JSON.parse(inner.tags);
        } catch (e) {
          tagsData = null;
        }
      } else if (Array.isArray(inner.tags)) {
        tagsData = inner.tags;
      }
    }
  }
  
  if (!videoData) {
    videoData = (typeof d === 'object') ? d : {};
  }

  const title = videoData.title || d.title || d.name || '未知标题';
  console.log(`🎬 ${title}\n`);
  
  if (videoData.duration) console.log(`⏱ 时长: ${videoData.duration}`);
  if (videoData.viewed || videoData.views || videoData.viewCount) {
    console.log(`👁 观看: ${videoData.viewed || videoData.views || videoData.viewCount}`);
  }
  
  // 优先展示高清
  const highurl = videoData.highurl;
  const lowurl = videoData.lowurl;
  const hls = videoData.hls;
  
  if (highurl) console.log(`▶️ 高清: ${highurl}`);
  if (lowurl && lowurl !== highurl) console.log(`▶️ 标清: ${lowurl}`);
  if (hls) console.log(`▶️ HLS: ${hls}`);
  
  if (!highurl && !lowurl && !hls) {
    const playUrl = videoData.playUrl || videoData.videoUrl || videoData.url;
    if (playUrl) console.log(`▶️ 播放: ${playUrl}`);
  }
  
  const thumb = videoData.thumb || videoData.thumbnail || videoData.cover;
  if (thumb) console.log(`🖼 封面: ${thumb}`);
  
  if (tagsData && Array.isArray(tagsData)) {
    const tagNames = tagsData.map(t => t.name || '').filter(n => n);
    if (tagNames.length > 0) console.log(`🏷 标签: ${tagNames.join(', ')}`);
  }
}

// ============ Main ============

function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.log('Usage: node video-search.js <command> [options]');
    console.log('Commands: check-key, search, list, detail, categories, quota, config');
    return;
  }

  const cmd = args[0];
  const commands = { 'check-key': checkKey, search, list, detail, categories, quota, config };
  
  if (commands[cmd]) {
    commands[cmd](args).catch(e => console.log(`❌ Error: ${e.message}`));
  } else {
    console.log(`❌ 未知命令: ${cmd}`);
    console.log('可用命令: check-key, search, list, detail, categories, quota, config');
  }
}

main();