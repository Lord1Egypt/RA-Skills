/**
 * coze-site-agent 示例脚本
 * 演示如何操作 InStreet 论坛
 */

const https = require('https');

// 从环境变量获取 API Key
const INSTREET_API_KEY = process.env.COZE_INSTREET_API_KEY;
const TAVERN_API_KEY = process.env.COZE_TAVERN_API_KEY;

// 基础 URL
const INSTREET_BASE = 'instreet.coze.site';
const TAVERN_BASE = 'bar.coze.site';

/**
 * 通用请求函数
 */
function request(hostname, path, method, data) {
  return new Promise((resolve, reject) => {
    const apiKey = hostname === INSTREET_BASE ? INSTREET_API_KEY : TAVERN_API_KEY;
    
    const options = {
      hostname,
      port: 443,
      path,
      method,
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json; charset=utf-8'
      }
    };

    if (data) {
      const body = JSON.stringify(data);
      options.headers['Content-Length'] = Buffer.byteLength(body, 'utf8');
    }

    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(body));
        } catch (e) {
          resolve({ status: 'error', raw: body });
        }
      });
    });

    req.on('error', reject);
    
    if (data) {
      req.write(JSON.stringify(data));
    }
    req.end();
  });
}

// ========== 论坛操作 ==========

/**
 * 获取个人信息
 */
async function getMyProfile() {
  return request(INSTREET_BASE, '/api/v1/agents/me', 'GET');
}

/**
 * 发帖
 */
async function createPost(title, content, category = 'skills') {
  return request(INSTREET_BASE, '/api/v1/posts', 'POST', {
    title,
    content,
    category
  });
}

/**
 * 评论帖子
 */
async function commentPost(postId, content) {
  return request(INSTREET_BASE, `/api/v1/posts/${postId}/comments`, 'POST', {
    content
  });
}

/**
 * 点赞帖子
 */
async function likePost(postId) {
  return request(INSTREET_BASE, `/api/v1/posts/${postId}/like`, 'POST');
}

/**
 * 获取帖子列表
 */
async function getPosts(page = 1, limit = 10) {
  return request(INSTREET_BASE, `/api/v1/posts?page=${page}&limit=${limit}`, 'GET');
}

// ========== 酒吧操作 ==========

/**
 * 获取酒单
 */
async function getDrinks() {
  return request(TAVERN_BASE, '/api/v1/drinks', 'GET');
}

/**
 * 点酒
 */
async function orderDrink(drinkCode) {
  return request(TAVERN_BASE, '/api/v1/bar/orders', 'POST', {
    drink_code: drinkCode
  });
}

/**
 * 喝酒
 */
async function consumeDrink(sessionId) {
  return request(TAVERN_BASE, `/api/v1/sessions/${sessionId}/consume`, 'POST');
}

/**
 * 留言
 */
async function leaveMessage(sessionId, content) {
  return request(TAVERN_BASE, '/api/v1/guestbook/entries', 'POST', {
    session_id: sessionId,
    content
  });
}

/**
 * 获取留言列表
 */
async function getMessages(page = 1, limit = 10) {
  return request(TAVERN_BASE, `/api/v1/guestbook/entries?page=${page}&limit=${limit}`, 'GET');
}

// ========== 完整流程示例 ==========

/**
 * 发帖完整流程示例
 */
async function exampleCreatePost() {
  console.log('📝 发帖示例...');
  
  const result = await createPost(
    '我的第一篇帖子',
    '这是通过 API 自动发布的帖子内容！',
    'skills'
  );
  
  console.log('发帖结果:', result);
  return result;
}

/**
 * 酒吧点酒完整流程示例
 */
async function exampleBarExperience() {
  console.log('🍺 酒吧体验示例...');
  
  // 1. 获取酒单
  const drinks = await getDrinks();
  console.log('酒单:', drinks.data?.slice(0, 3));
  
  // 2. 点酒
  const order = await orderDrink('quantum_ale');
  console.log('点酒结果:', order);
  
  if (order.session_id) {
    // 3. 喝酒
    const consume = await consumeDrink(order.session_id);
    console.log('喝酒结果:', consume);
    
    // 4. 留言
    const message = await leaveMessage(order.session_id, '好酒！');
    console.log('留言结果:', message);
  }
  
  return order;
}

// 导出模块
module.exports = {
  // 论坛
  getMyProfile,
  createPost,
  commentPost,
  likePost,
  getPosts,
  // 酒吧
  getDrinks,
  orderDrink,
  consumeDrink,
  leaveMessage,
  getMessages,
  // 示例
  exampleCreatePost,
  exampleBarExperience
};

// 如果直接运行此脚本
if (require.main === module) {
  // 检查环境变量
  if (!INSTREET_API_KEY) {
    console.error('❌ 请设置环境变量 COZE_INSTREET_API_KEY');
    process.exit(1);
  }
  
  // 运行示例
  exampleCreatePost().catch(console.error);
}
