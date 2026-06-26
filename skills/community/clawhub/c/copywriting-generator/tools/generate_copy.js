#!/usr/bin/env node
/**
 * 文案生成工具
 * 支持多种平台风格的营销文案创作
 */

const fs = require('fs');
const path = require('path');

// 文案生成配置
const PLATFORM_STYLES = {
  'xiaohongshu': {
    name: '小红书',
    features: ['种草风', 'emoji 丰富', '真实感', '标题党'],
    maxLength: 1000,
    emojiSet: ['✨', '💕', '🔥', '😍', '👍', '💯', '🎁', '📦', '💰', '⏰'],
  },
  'douyin': {
    name: '抖音',
    features: ['口播稿', '节奏快', '前 3 秒抓人', '互动性强'],
    maxLength: 300,
    emojiSet: ['🎬', '🎵', '🔥', '💥', '👀', '❤️', '📱'],
  },
  'taobao': {
    name: '淘宝',
    features: ['卖点清晰', '促销信息', '转化导向', '信任背书'],
    maxLength: 5000,
    emojiSet: ['🏆', '✅', '💰', '🎁', '📦', '⚡', '🔥'],
  },
  'wechat': {
    name: '公众号',
    features: ['深度内容', '故事性', '价值输出', '专业感'],
    maxLength: 10000,
    emojiSet: ['📝', '💡', '🎯', '📊', '🔍', '✨'],
  },
  '朋友圈': {
    name: '朋友圈',
    features: ['短小精悍', '生活化', '软广', '真实分享'],
    maxLength: 200,
    emojiSet: ['😊', '💕', '✨', '👍', '🎉'],
  },
};

// 标题生成模板
const TITLE_TEMPLATES = [
  '{痛点}后不{行动}，真的会{后果}！😱',
  '空瓶{次数}次才敢推荐的{产品}✨',
  '{人群}也能用的{产品}！亲测有效',
  '{领域}{时间}年，终于找到{解决方案}了',
  '平价替代！¥{价格}搞定大牌同款效果',
  '{人群}必备！{效果}',
  '成分党深扒：{产品}凭什么卖爆？',
  '{时间}天实测，{效果}真的{结果}了！',
  '{人群}冲！{价格区间}{产品}天花板',
  '别乱买{品类}了，看这篇就够了',
];

// CTA 模板
const CTA_TEMPLATES = [
  '限时优惠，点击领取¥{discount}券！',
  '库存不多，先到先得～',
  '点击链接，查看真实用户评价',
  '现在下单送{gift}，仅限今天！',
  '加入购物车，享受满减优惠',
  '前{num}名下单立减¥{discount}！',
  '扫码添加客服，获取专属优惠',
];

/**
 * 生成标题
 */
function generateTitles(product, count = 10, style = 'xiaohongshu') {
  const titles = [];
  const platform = PLATFORM_STYLES[style] || PLATFORM_STYLES.xiaohongshu;
  
  for (let i = 0; i < count; i++) {
    let template = TITLE_TEMPLATES[i % TITLE_TEMPLATES.length];
    let title = template
      .replace('{痛点}', '25 岁')
      .replace('{行动}', '涂这个')
      .replace('{后果}', '老')
      .replace('{次数}', Math.floor(Math.random() * 5) + 1)
      .replace('{产品}', product || '好物')
      .replace('{人群}', ['敏感肌', '学生党', '熬夜党', '成分党'][Math.floor(Math.random() * 4)])
      .replace('{领域}', '护肤')
      .replace('{时间}', Math.floor(Math.random() * 10) + 1)
      .replace('{解决方案}', '本命' + (product || '产品'))
      .replace('{价格}', (Math.floor(Math.random() * 5) + 1) * 100)
      .replace('{效果}', ['第二天脸不垮了', '细纹淡了', '皮肤亮了'][Math.floor(Math.random() * 3)])
      .replace('{结果}', ['明显', '惊人', '看得见'][Math.floor(Math.random() * 3)])
      .replace('{价格区间}', ['百元', '平价', '学生党'][Math.floor(Math.random() * 3)])
      .replace('{品类}', product || '产品');
    
    titles.push(title);
  }
  
  return titles;
}

/**
 * 生成正文框架
 */
function generateContent(product, sellingPoints = []) {
  return `【痛点引入】
你是不是也这样：${getPainPoint(product)}...

【产品介绍】
这${getClassifier(product)}我用了${getUsageTime()}，最明显的感受是...

【卖点展示】
${sellingPoints.map((p, i) => `${i + 1}. ${p}`).join('\n')}

【成分/特点分析】
核心${getFeatureType(product)}是 XX，主打 XX 功效，适合 XX 肤质...

【使用感受】
质地是 XX 的，上脸 XX，吸收速度 XX...

【效果展示】
用了 30 天后，最明显的变化是...

【购买建议】
适合人群：XX
不适合：XX
购买渠道：XX`;
}

function getPainPoint(product) {
  const points = [
    '25 岁后皮肤状态断崖式下跌',
    '用了很多产品都没效果',
    '预算有限但想要好效果',
    '敏感肌不敢乱用产品',
    '熬夜后状态特别差',
  ];
  return points[Math.floor(Math.random() * points.length)];
}

function getClassifier(product) {
  const classifiers = ['瓶', '款', '个', '套'];
  return classifiers[Math.floor(Math.random() * classifiers.length)];
}

function getUsageTime() {
  const times = ['3 个月', '2 周', '1 个月', '半年', '30 天'];
  return times[Math.floor(Math.random() * times.length)];
}

function getFeatureType(product) {
  const types = ['成分', '特点', '技术', '配方'];
  return types[Math.floor(Math.random() * types.length)];
}

/**
 * 生成 CTA
 */
function generateCTAs(count = 5) {
  const ctas = [];
  
  for (let i = 0; i < count; i++) {
    let template = CTA_TEMPLATES[i % CTA_TEMPLATES.length];
    let cta = template
      .replace('{discount}', (Math.floor(Math.random() * 5) + 1) * 10)
      .replace('{gift}', ['同款小样', '精美礼品', '优惠券', '包邮'][Math.floor(Math.random() * 4)])
      .replace('{num}', [10, 20, 50, 100][Math.floor(Math.random() * 4)]);
    
    ctas.push(cta);
  }
  
  return ctas;
}

/**
 * 生成优化建议
 */
function generateSuggestions() {
  return [
    '加入具体数字增强可信度（如"30 天见效"比"快速见效"更有说服力）',
    '使用 emoji 提高阅读体验，但不要过度',
    '加入用户评价增加社会认同',
    '突出独特卖点，与竞品区分开',
    '加入紧迫感（限时、限量）促进转化',
    '使用对比手法突出优势',
    '加入使用场景描述，让用户更容易想象',
  ];
}

/**
 * 主函数
 */
function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
    console.log(`
✍️ 文案生成工具

用法：
  node generate_copy.js <命令> [选项]

命令：
  titles <产品名> [数量] [风格]  - 生成标题
  content <产品名> [卖点...]     - 生成正文
  ctas [数量]                    - 生成 CTA
  full <产品名> [卖点...]        - 生成完整文案
  suggest                        - 生成优化建议

风格选项：
  xiaohongshu, douyin, taobao, wechat, 朋友圈

示例：
  node generate_copy.js titles "抗老精华" 10 xiaohongshu
  node generate_copy.js content "抗老精华" "天然成分" "敏感肌可用" "30 天见效"
  node generate_copy.js full "抗老精华" "天然成分" "敏感肌可用"
`);
    process.exit(0);
  }
  
  const command = args[0];
  
  switch (command) {
    case 'titles': {
      const product = args[1] || '产品';
      const count = parseInt(args[2]) || 10;
      const style = args[3] || 'xiaohongshu';
      
      const titles = generateTitles(product, count, style);
      console.log('📝 标题方案：\n');
      titles.forEach((t, i) => console.log(`${i + 1}. ${t}`));
      break;
    }
    
    case 'content': {
      const product = args[1] || '产品';
      const sellingPoints = args.slice(2);
      
      const content = generateContent(product, sellingPoints);
      console.log('📄 正文框架：\n');
      console.log(content);
      break;
    }
    
    case 'ctas': {
      const count = parseInt(args[1]) || 5;
      
      const ctas = generateCTAs(count);
      console.log('🎯 CTA 方案：\n');
      ctas.forEach((c, i) => console.log(`${i + 1}. ${c}`));
      break;
    }
    
    case 'full': {
      const product = args[1] || '产品';
      const sellingPoints = args.slice(2);
      
      console.log('✍️ 文案生成结果\n');
      console.log('='.repeat(50));
      
      console.log('\n📝 标题方案（10 个）：\n');
      generateTitles(product, 10).forEach((t, i) => console.log(`${i + 1}. ${t}`));
      
      console.log('\n' + '='.repeat(50));
      console.log('\n📄 正文框架：\n');
      console.log(generateContent(product, sellingPoints));
      
      console.log('\n' + '='.repeat(50));
      console.log('\n🎯 CTA 方案（5 个）：\n');
      generateCTAs(5).forEach((c, i) => console.log(`${i + 1}. ${c}`));
      
      console.log('\n' + '='.repeat(50));
      console.log('\n💡 优化建议：\n');
      generateSuggestions().forEach((s, i) => console.log(`${i + 1}. ${s}`));
      
      break;
    }
    
    case 'suggest': {
      console.log('💡 优化建议：\n');
      generateSuggestions().forEach((s, i) => console.log(`${i + 1}. ${s}`));
      break;
    }
    
    default:
      console.error(`未知命令：${command}`);
      console.log('使用 --help 查看帮助');
      process.exit(1);
  }
}

main();
