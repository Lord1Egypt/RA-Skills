#!/usr/bin/env node
/**
 * 每日神价推送 - 双数据源版本
 * 数据源：什么值得买 + 识货网
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

// 飞书配置
const FEISHU_CONFIG = {
  appId: 'cli_a9f044d41d381cc7',
  appSecret: 'sD6iG2RlWbjaNjeCdMuLSggR6a3HpvJT',
  receiveId: 'ou_74526227694bedc4c182fe1ccd6c3253',
  receiveIdType: 'open_id'
};

// 获取飞书 token
async function getFeishuToken() {
  const data = JSON.stringify({ app_id: FEISHU_CONFIG.appId, app_secret: FEISHU_CONFIG.appSecret });
  return new Promise((resolve, reject) => {
    const req = https.request('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', {
      method: 'POST', headers: { 'Content-Type': 'application/json', 'Content-Length': data.length }
    }, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => resolve(JSON.parse(body).tenant_access_token));
    });
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

// 推送飞书
async function pushToFeishu(content) {
  const token = await getFeishuToken();
  const payload = {
    receive_id: FEISHU_CONFIG.receiveId,
    msg_type: 'text',
    content: JSON.stringify({ text: content })
  };
  return new Promise((resolve, reject) => {
    const req = https.request(
      `https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=${FEISHU_CONFIG.receiveIdType}`,
      { method: 'POST', headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' } },
      (res) => {
        let body = '';
        res.on('data', chunk => body += chunk);
        res.on('end', () => {
          const result = JSON.parse(body);
          result.code === 0 ? resolve(result) : reject(new Error(result.msg));
        });
      }
    );
    req.write(JSON.stringify(payload));
    req.end();
  });
}

// 解析什么值得买 snapshot
function parseSMZDM(snapshotText) {
  const deals = [];
  const lines = snapshotText.split('\n');
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (line.includes('option') || (line.includes('link') && line.includes('/p/'))) {
      const urlMatch = line.match(/\/url:\s*https:\/\/www\.smzdm\.com\/p\/(\d+)\//);
      let title = '';
      let price = '';
      
      for (let j = i; j < Math.min(i + 5, lines.length); j++) {
        const nextLine = lines[j];
        if (nextLine.includes('generic [ref=') && !nextLine.includes('[')) {
          const textMatch = nextLine.match(/:\s*(.+)$/);
          if (textMatch && textMatch[1].includes('元')) {
            price = textMatch[1].trim();
          } else if (textMatch && textMatch[1].length > 10 && textMatch[1].length < 100) {
            title = textMatch[1].trim();
          }
        }
      }
      
      if (urlMatch && title && price) {
        const pid = urlMatch[1];
        let platform = '什么值得买';
        if (title.includes('京东')) platform = '京东';
        else if (title.includes('拼多多') || title.includes('百亿补贴')) platform = '拼多多';
        else if (title.includes('天猫')) platform = '天猫';
        
        deals.push({
          title: title.replace(/\s+/g, ' '),
          price,
          platform,
          source: 'smzdm',
          url: `https://www.smzdm.com/p/${pid}/`
        });
      }
    }
  }
  
  return deals.slice(0, 10);
}

// 解析热度数值（如"1.72w"→17200）
function parseHeatNum(tag) {
  if (!tag) return 0;
  const match = tag.match(/([\d.]+)w/);
  if (match) return parseFloat(match[1]) * 10000;
  const numMatch = tag.match(/(\d+)/);
  return numMatch ? parseInt(numMatch[1]) : 0;
}

// 判断是否有折扣标签
function hasDiscount(tag) {
  if (!tag) return false;
  return tag.includes('补贴') || tag.includes('低价') || tag.includes('好价');
}

// 判断价格等级
function getPriceLevel(price) {
  if (!price) return 'unknown';
  const num = parseFloat(price.replace(/[¥,]/g, ''));
  if (num < 100) return '低价';      // 100 元以下
  if (num < 500) return '平价';      // 100-500 元
  if (num < 2000) return '中价';     // 500-2000 元
  if (num < 10000) return '高价';    // 2000-10000 元
  return '超高价';                    // 10000 元以上
}

// 判断是否是神价（折扣 + 价格综合判断）
function isGoodDeal(deal) {
  const hasDiscountTag = hasDiscount(deal.tag);
  const heat = parseHeatNum(deal.tag);
  const priceLevel = getPriceLevel(deal.price);
  
  // 有折扣标签 → 直接判定为神价
  if (hasDiscountTag) return true;
  
  // 超高热度（10w+ 人付款）→ 即使无折扣也是神价
  if (heat >= 100000) return true;
  
  // 低价商品（100 元以下）+ 中等热度（1w+）→ 神价
  if (priceLevel === '低价' && heat >= 10000) return true;
  
  // 其他情况 → 需要高热度（5w+）
  return heat >= 50000;
}

// 计算综合得分（折扣 + 热度 + 价格）
function calcScore(deal) {
  const heat = parseHeatNum(deal.tag);
  const priceLevel = getPriceLevel(deal.price);
  
  // 基础分：热度
  let score = heat;
  
  // 折扣加成：有折扣标签 +5 万
  if (hasDiscount(deal.tag)) score += 50000;
  
  // 价格加成：低价商品更容易入手
  if (priceLevel === '低价') score += 10000;
  else if (priceLevel === '平价') score += 5000;
  
  // 超高价商品需要更高热度
  if (priceLevel === '超高价' && heat < 10000) score -= 30000;
  
  return score;
}

// 解析识货网 snapshot
function parseSHIHUO(snapshotText) {
  const deals = [];
  const lines = snapshotText.split('\n');
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (line.includes('/page/pcGoodsDetail')) {
      const urlMatch = line.match(/goodsId=(\d+)&styleId=(\d+)/);
      let title = '';
      let price = '';
      let tag = '';
      
      // 向后查找标题、价格、标签
      for (let j = i + 1; j < Math.min(i + 6, lines.length); j++) {
        const nextLine = lines[j];
        if (nextLine.includes('heading')) {
          const titleMatch = nextLine.match(/heading\s+"([^"]+)"/);
          if (titleMatch) title = titleMatch[1];
        }
        if (nextLine.includes('generic:') && nextLine.includes('¥')) {
          const priceMatch = nextLine.match(/¥([\d,]+)/);
          if (priceMatch) price = `¥${priceMatch[1]}`;
        }
        if (nextLine.includes('generic:') && (nextLine.includes('人付款') || nextLine.includes('补贴') || nextLine.includes('低价'))) {
          const tagMatch = nextLine.match(/generic:\s*(.+)$/);
          if (tagMatch) tag = tagMatch[1].trim();
        }
      }
      
      if (urlMatch && title && price) {
        deals.push({
          title: title.substring(0, 60),
          price,
          platform: '识货',
          source: 'shihuo',
          tag,
          url: `https://www.shihuo.cn/page/pcGoodsDetail?goodsId=${urlMatch[1]}&styleId=${urlMatch[2]}`,
          score: 0 // 稍后计算
        });
      }
    }
  }
  
  // 筛选神价
  const goodDeals = deals.filter(d => isGoodDeal(d));
  
  // 计算综合得分并排序
  goodDeals.forEach(d => { d.score = calcScore(d); });
  goodDeals.sort((a, b) => b.score - a.score);
  
  // 返回前 10 个神价
  return goodDeals.slice(0, 10);
}

// 生成报告
function generateReport(smzdmDeals, shihuoDeals) {
  const today = new Date().toISOString().split('T')[0];
  const weekday = new Date().toLocaleDateString('zh-CN', { weekday: 'long' });
  
  let report = `🔥 每日神价日报 ${today} ${weekday}\n\n`;
  report += `📊 数据来源：什么值得买 + 识货网\n\n`;
  
  // 什么值得买部分
  if (smzdmDeals.length > 0) {
    report += `【什么值得买】📦\n`;
    smzdmDeals.slice(0, 5).forEach((deal, i) => {
      report += `${i + 1}. ${deal.title}\n`;
      report += `   💰 ${deal.price} | 🛒 ${deal.platform}\n`;
      report += `   🔗 ${deal.url}\n\n`;
    });
  }
  
  // 识货网部分
  if (shihuoDeals.length > 0) {
    report += `【识货网】👟\n`;
    shihuoDeals.slice(0, 5).forEach((deal, i) => {
      // 突出显示折扣标签
      let tagDisplay = deal.tag || '热销';
      const priceLevel = getPriceLevel(deal.price);
      
      // 神价标识
      let dealIcon = '💎'; // 默认神价
      if (hasDiscount(deal.tag)) {
        tagDisplay = '🔥 ' + tagDisplay;
        dealIcon = '🔥'; // 有折扣
      } else if (parseHeatNum(deal.tag) >= 100000) {
        dealIcon = '⭐'; // 超高热度
      }
      
      report += `${i + 1}. ${dealIcon} ${deal.title}\n`;
      report += `   💰 ${deal.price} (${priceLevel}) | 🏷️ ${tagDisplay}\n`;
      report += `   🔗 ${deal.url}\n\n`;
    });
  }
  
  report += `📊 今日统计：\n`;
  report += `- 什么值得买：${smzdmDeals.length} 个\n`;
  report += `- 识货网：${shihuoDeals.length} 个\n`;
  report += `- 总计：${smzdmDeals.length + shihuoDeals.length} 个神价\n\n`;
  
  report += `💡 购物建议：\n`;
  report += `1. 拼多多百亿补贴需验货\n`;
  report += `2. 京东注意保价政策\n`;
  report += `3. 识货显示付款人数参考热度\n\n`;
  report += `⚠️ 免责声明：仅供参考`;
  
  return report;
}

// 主函数
async function main() {
  console.log('🚀 每日神价推送 - 双数据源版\n');
  
  // 读取什么值得买 snapshot
  const smzdmPath = path.join(__dirname, '../assets/smzdm-snapshot.txt');
  let smzdmDeals = [];
  if (fs.existsSync(smzdmPath)) {
    console.log('📡 解析什么值得买...');
    const snapshotText = fs.readFileSync(smzdmPath, 'utf8');
    smzdmDeals = parseSMZDM(snapshotText);
    console.log(`✅ 什么值得买：${smzdmDeals.length} 个商品`);
  }
  
  // 读取识货网 snapshot
  const shihuoPath = path.join(__dirname, '../assets/shihuo-snapshot.txt');
  let shihuoDeals = [];
  if (fs.existsSync(shihuoPath)) {
    console.log('📡 解析识货网...');
    const snapshotText = fs.readFileSync(shihuoPath, 'utf8');
    shihuoDeals = parseSHIHUO(snapshotText);
    console.log(`✅ 识货网：${shihuoDeals.length} 个商品`);
  }
  
  // 如果都没有，使用预设数据
  if (smzdmDeals.length === 0 && shihuoDeals.length === 0) {
    console.log('⚠️  无 snapshot 文件，使用预设数据');
    smzdmDeals = [
      { title: '酷态科 10 号电能棒 10000 毫安 120W 快充', price: '119 元', platform: '拼多多', url: 'https://www.smzdm.com/p/170981835/' },
      { title: '中兴 AX3000 巡天版 千兆 Mesh 路由器', price: '100.58 元', platform: '京东', url: 'https://www.smzdm.com/p/170985487/' }
    ];
    shihuoDeals = [
      { title: 'iPhone 17 Pro Max 5G 手机', price: '¥9399', tag: '国家补贴 1.72w 人付款', url: 'https://www.shihuo.cn/page/pcGoodsDetail?goodsId=7929864' },
      { title: 'Nike Air Force 1 空军一号', price: '¥475', tag: '67.51w 人付款', url: 'https://www.shihuo.cn/page/pcGoodsDetail?goodsId=134' }
    ];
  }
  
  console.log(`\n📝 生成报告...`);
  const report = generateReport(smzdmDeals, shihuoDeals);
  
  // 保存
  const reportPath = path.join(__dirname, '../assets/daily-report.txt');
  fs.writeFileSync(reportPath, report);
  console.log(`📄 保存：${reportPath}\n`);
  
  // 推送
  console.log('📱 推送飞书...');
  await pushToFeishu(report);
  console.log('✅ 完成！\n');
  
  console.log('--- 预览 ---');
  console.log(report);
}

main().catch(console.error);
