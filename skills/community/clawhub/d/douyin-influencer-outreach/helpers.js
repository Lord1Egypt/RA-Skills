/**
 * Douyin Influencer Outreach - Helper Functions
 * 抖音达人拓展辅助函数
 */

// == 达人信息提取 ==

/**
 * 从快照中解析达人列表
 * @param {Array} nodes - ARIA 快照 nodes 数组
 * @returns {Array} 达人信息列表
 */
function parseInfluencerList(nodes) {
  const influencers = [];
  
  for (const node of nodes) {
    // 匹配达人条目 link 元素
    if (node.role === 'link' && node.name?.includes('粉丝')) {
      const match = node.name.match(/(\d+(?:\.\d+)?(?:万)?)[获赞]+(\d+(?:\.\d+)?(?:万)?)[粉丝]+/);
      if (match) {
        influencers.push({
          ref: node.ref,
          name: node.name.split(' ')[0],
          likes: parseNumber(match[1]),
          followers: parseNumber(match[2]),
          engagement: parseNumber(match[1]) / parseNumber(match[2])
        });
      }
    }
  }
  
  return influencers;
}

/**
 * 解析数字（支持"万"单位）
 * @param {string} str - 数字字符串
 * @returns {number}
 */
function parseNumber(str) {
  if (str.includes('万')) {
    return parseFloat(str) * 10000;
  }
  return parseInt(str);
}

/**
 * 筛选符合条件的达人
 * @param {Array} influencers - 达人列表
 * @param {Object} criteria - 筛选条件
 * @returns {Array}
 */
function filterInfluencers(influencers, criteria = {}) {
  const {
    maxFollowers = 2000,
    minEngagement = 3,
    minWorks = 50
  } = criteria;
  
  return influencers.filter(inf => 
    inf.followers <= maxFollowers && 
    inf.engagement >= minEngagement
  );
}

// == 私信相关 ==

/**
 * 输入私信内容
 * @param {string} message - 消息内容
 * @returns {string} JS 函数代码
 */
function generateInputScript(message) {
  return `() => {
    const input = document.querySelector('[contenteditable="true"]');
    if (!input) return 'not found';
    input.focus();
    input.textContent = '${message.replace(/'/g, "\\'")}';
    input.dispatchEvent(new Event('input', {bubbles: true}));
    return 'ok';
  }`;
}

/**
 * 发送私信（按 Enter）
 * @returns {string} JS 函数代码
 */
function generateSendScript() {
  return `() => {
    const input = document.querySelector('[contenteditable="true"]');
    if (!input) return 'not found';
    input.dispatchEvent(new KeyboardEvent('keydown', {
      key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true
    }));
    return 'sent';
  }`;
}

// == 话术模板 ==

const TEMPLATES = {
  // A 类：作品切入
  like: (product) => 
    `嗨～看到你笔记里分享的${product}，看起来很不错！我这边有个省钱团购群，专门组织大家拼单购买，刚好有你提到的这款，价格能便宜不少，要不要一起呀？👇`,
  
  benefit: () =>
    `嗨～看到你经常在网上找好物，我这边有个自用省钱群都是真实买家，官方发货，价格比直接买低不少，有兴趣的话可以拉你进来看看～`,
  
  resonate: () =>
    `你的分享好真实呀！我也是一直在找靠谱的购买渠道，最近建了个小群专门团这类产品，都是自己用着好的才推，不强制购买，想了解的话可以进来看看～`,
  
  // B 类：评论切入
  comment: (video) =>
    `看到你在${video}下的评论～我也是买了很多年，总结了一些靠谱渠道，建了个团购群专门帮大家省钱，想了解的话可以拉你进来看看，不买也没关系！`,
  
  comment_resonate: () =>
    `刷到你的评论，感觉你也是精打细算类型～我这边有个小群都是注重品质的买家，品牌方直发，有需要的话进来看看呀～`,
  
  comment_ask: (product) =>
    `打扰了，看你评论对${product}挺懂的，我想请教下～我这边在组织团购，你平时买这类多吗？有机会可以一起拼单`,
  
  // C 类：通用型
  ask: (field) =>
    `姐妹，我看到你对${field}很有研究呀，能不能请教一下～我这边建了个团购群，想找真正需要的朋友一起拼单，你平时有买这类产品的习惯吗？`,
  
  direct: () =>
    `你好呀，我是一名团长，专门帮大家找品牌团购价，不需要自己囤货，下单后我这边统一跟供应商谈更低价，有兴趣的话可以加我拉你进群～`,
  
  benefit2: () =>
    `嗨～看到你也在找靠谱购买渠道，我这边刚建了个团购群，都是用过觉得好才推荐的品牌，有兴趣的话可以拉你进来看看，不强求～`,
  
  simple: () =>
    `你好，我这边有个省钱团购群，专门帮大家对接品牌团购价，都是官方发货，有需要可以拉你进来看看～`
};

// 模板选择策略
const STRATEGY = {
  // 达人发了具体产品笔记 → 点赞切入
  product_post: 'like',
  // 达人作品丰富、内容真实 → 共鸣切入
  authentic_content: 'resonate',
  // 从评论区找到的人 → 评论延伸
  from_comment: 'comment',
  // 不确定对方情况 → 简洁型
  unknown: 'simple',
  // 对方是女性/年轻用户 → 求教切入
  female_young: 'ask'
};

/**
 * 生成个性化私信
 * @param {string} type - 模板类型（like/benefit/resonate/comment/comment_resonate/comment_ask/ask/direct/benefit2/simple）
 * @param {Object} vars - 变量替换 {product, field, video}
 * @returns {string}
 */
function generateMessage(type, vars = {}) {
  const template = TEMPLATES[type];
  if (!template) {
    console.warn(`Unknown template type: ${type}, using simple`);
    return TEMPLATES.simple();
  }
  
  // 根据模板类型传入对应变量
  switch(type) {
    case 'like':
      return template(vars.product || '好物');
    case 'comment':
      return template(vars.video || '那个视频');
    case 'comment_ask':
      return template(vars.product || '这个');
    case 'ask':
      return template(vars.field || '护肤');
    default:
      return template();
  }
}

/**
 * 根据场景选择最佳模板
 * @param {string} scenario - 场景类型
 * @param {Object} vars - 变量
 * @returns {string}
 */
function chooseTemplate(scenario, vars = {}) {
  const type = STRATEGY[scenario] || 'simple';
  return generateMessage(type, vars);
}

// == 工具函数 ==

/**
 * 延迟等待
 * @param {number} ms - 毫秒
 * @returns {Promise}
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * 记录达人信息到日志
 * @param {Object} info - 达人信息
 */
function logInfluencer(info) {
  console.log(JSON.stringify({
    timestamp: new Date().toISOString(),
    ...info
  }));
}

module.exports = {
  parseInfluencerList,
  filterInfluencers,
  generateInputScript,
  generateSendScript,
  generateMessage,
  chooseTemplate,
  STRATEGY,
  TEMPLATES
};
