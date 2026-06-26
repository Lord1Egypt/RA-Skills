/**
 * OpenClaw 资讯自动推送脚本
 * 用法: node push-news.js [关键词] [条数] [字数限制]
 */
const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const GATEWAY_URL = 'http://127.0.0.1:18789';
const GATEWAY_TOKEN = '30176f5d9e3d3372a70cefc8c1cf34248e5abc5888ec5519';
const ACCOUNT_ID = 'erbai';
const DEFAULT_TARGET = 'ou_56cdb528c6356bf5e344d2da35e98dad';
const SENT_CACHE_FILE = path.join(__dirname, '.sent-news.json');

// 读取已推送的资讯 ID
function loadSentIds() {
  try {
    if (fs.existsSync(SENT_CACHE_FILE)) {
      const data = JSON.parse(fs.readFileSync(SENT_CACHE_FILE, 'utf-8'));
      return new Set(data.ids || []);
    }
  } catch (error) {
    console.error('读取缓存失败:', error.message);
  }
  return new Set();
}

// 保存已推送的资讯 ID
function saveSentIds(ids) {
  try {
    // 最多保留 1000 条记录
    const idsArray = Array.from(ids).slice(-1000);
    fs.writeFileSync(SENT_CACHE_FILE, JSON.stringify({ ids: idsArray, updated: new Date().toISOString() }, null, 2));
  } catch (error) {
    console.error('保存缓存失败:', error.message);
  }
}

// 获取资讯原始数据
function fetchNewsRaw(keyword = 'openclaw', count = 5, maxChars = 500) {
  const scriptPath = path.join(__dirname, 'new.js');
  try {
    const result = execSync(`node "${scriptPath}" "${keyword}" ${count} ${maxChars}`, {
      encoding: 'utf-8',
      timeout: 30000
    });
    return result.trim();
  } catch (error) {
    console.error('获取资讯失败:', error.message);
    return null;
  }
}

// 格式化资讯
function formatNews(items, keyword = 'openclaw') {
  const today = new Date();
  const dateStr = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;
  
  let formatted = `📰 【${keyword}】 资讯快报 | ${dateStr}\n`;
  formatted += `━━━━━━━━━━━━━━━━━━\n`;
  
  if (!Array.isArray(items) || items.length === 0) {
    return null;
  }
  
  const numberEmoji = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟'];
  
  items.forEach((item, index) => {
    if (index >= 10) return;
    
    // 标题（将链接挂在标题上）
    if (item.link) {
      // 使用 Markdown 链接格式，兼容飞书富文本
      formatted += `${numberEmoji[index]} [${item.title}](${item.link})\n`;
    } else {
      formatted += `${numberEmoji[index]} ${item.title}\n`;
    }
    
  // 日期 (格式: 2026-03-12 17:49:11 → 3月12日 17时49分)
  if (item.create_time) {
    const dateTimeMatch = item.create_time.match(/(\d{4})-(\d{1,2})-(\d{1,2})(?:\s+(\d{1,2}):(\d{1,2}))/);
    if (dateTimeMatch) {
      const month = parseInt(dateTimeMatch[2]);
      const day = parseInt(dateTimeMatch[3]);
      const hour = parseInt(dateTimeMatch[4]);
      const minute = parseInt(dateTimeMatch[5]);
      formatted += `📅 ${month}月${day}日 ${hour}时${minute}分\n`;
    } else {
      const dateMatch = item.create_time.match(/(\d{4})-(\d{1,2})-(\d{1,2})/);
      if (dateMatch) {
        const month = parseInt(dateMatch[2]);
        const day = parseInt(dateMatch[3]);
        formatted += `📅 ${month}月${day}日\n`;
      }
    }
  }
    
    // 摘要 (截取内容)
    if (item.content) {
      // 移除 "BlockBeats 消息，" 前缀
      let summary = item.content.replace(/^BlockBeats\s*消息，?\s*/i, '');
      // 移除开头类似 "3 月 13 日，" 的日期前缀
      summary = summary.replace(/^\s*\d{1,2}\s*月\s*\d{1,2}\s*日[，,]\s*/u, '');
      // 截取前 150 字符
      const maxLen = 150;
      if (summary.length > maxLen) {
        summary = summary.substring(0, maxLen) + '...';
      }
      // 在摘要前增加摘要图标
      formatted += `📝 ${summary}\n`;
    }
    
    // // 链接
    // if (item.link) {
    //   formatted += `🔗 ${item.link}\n`;
    // }
  });
  
  formatted += `━━━━━━━━━━━━━━━━━━\n`;
  formatted += `自动推送`;
  
  return formatted;
}

// 发送消息
async function sendMessage(message, target = DEFAULT_TARGET) {
  const response = await fetch(`${GATEWAY_URL}/tools/invoke`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${GATEWAY_TOKEN}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      tool: 'message',
      args: {
        action: 'send',
        channel: 'feishu',
        accountId: ACCOUNT_ID,
        target: target,
        message: message
      }
    })
  });
  
  const result = await response.json();
  
  if (!result.ok) {
    throw new Error(result.error?.message || JSON.stringify(result.error));
  }
  
  return result.result;
}

// 主函数
async function main() {
  const keyword = process.argv[2] || 'openclaw';
  const count = parseInt(process.argv[3]) || 5;
  const maxChars = parseInt(process.argv[4]) || 500;
  const target = process.argv[5] || DEFAULT_TARGET;
  
  console.log(`[${new Date().toISOString()}] 开始获取 ${keyword} 资讯...`);
  
  const rawNews = fetchNewsRaw(keyword, count, maxChars);
  
  if (!rawNews) {
    console.log('未获取到资讯');
    process.exit(0);
  }
  
  // 解析资讯
  let items;
  try {
    items = JSON.parse(rawNews);
  } catch (error) {
    console.error('解析资讯失败:', error.message);
    process.exit(0);
  }
  
  if (!Array.isArray(items) || items.length === 0) {
    console.log('暂无资讯');
    process.exit(0);
  }
  
  // 去重
  const sentIds = loadSentIds();
  const newItems = items.filter(item => {
    // 用链接作为唯一标识
    const id = item.link || item.title;
    return !sentIds.has(id);
  });
  
  if (newItems.length === 0) {
    console.log('没有新资讯，跳过推送');
    process.exit(0);
  }
  
  console.log(`发现 ${newItems.length} 条新资讯`);
  
  // 格式化资讯
  const formattedNews = formatNews(newItems, keyword);
  
  if (!formattedNews) {
    console.log('格式化失败');
    process.exit(0);
  }
  
  try {
    await sendMessage(formattedNews, target);
    console.log('消息发送成功');
    
    // 记录已推送的资讯
    newItems.forEach(item => {
      const id = item.link || item.title;
      sentIds.add(id);
    });
    saveSentIds(sentIds);
    
    process.exit(0);
  } catch (error) {
    console.error('消息发送失败:', error.message);
    process.exit(1);
  }
}

main();