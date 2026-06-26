/**
 * AI-Social-Media-Manager 测试文件
 */

const { SocialMediaManager } = require('./index');
const { PlatformAdapter } = require('./platform-adapter');

console.log('🧪 开始测试 AI-Social-Media-Manager...\n');

const smm = new SocialMediaManager();
const platform = new PlatformAdapter();

let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`✅ ${name}`);
    passed++;
  } catch (error) {
    console.error(`❌ ${name}`);
    console.error(`   错误：${error.message}`);
    failed++;
  }
}

async function asyncTest(name, fn) {
  try {
    await fn();
    console.log(`✅ ${name}`);
    passed++;
  } catch (error) {
    console.error(`❌ ${name}`);
    console.error(`   错误：${error.message}`);
    failed++;
  }
}

// 测试内容日历生成
test('生成内容日历', () => {
  const calendar = smm.generateContentCalendar(
    'xiaohongshu',
    new Date(2026, 2, 1),
    '科技产品评测',
    10
  );
  
  if (!calendar.month) throw new Error('缺少 month 字段');
  if (!calendar.calendar) throw new Error('缺少 calendar 字段');
  if (calendar.totalPosts !== 10) throw new Error('帖子数量不正确');
  if (!calendar.summary) throw new Error('缺少 summary 字段');
});

// 测试最佳发布时间
test('获取最佳发布时间 - 小红书', () => {
  const time = smm.getBestPostingTime('xiaohongshu', new Date());
  if (!time.match(/^\d{2}:\d{2}$/)) throw new Error('时间格式不正确');
});

test('获取最佳发布时间 - 微博', () => {
  const time = smm.getBestPostingTime('weibo', new Date());
  if (!time.match(/^\d{2}:\d{2}$/)) throw new Error('时间格式不正确');
});

test('获取最佳发布时间 - Twitter', () => {
  const time = smm.getBestPostingTime('twitter', new Date());
  if (!time.match(/^\d{2}:\d{2}$/)) throw new Error('时间格式不正确');
});

// 测试不支持的平台
test('不支持的平台应抛出错误', () => {
  try {
    smm.getBestPostingTime('invalid_platform', new Date());
    throw new Error('应该抛出错误');
  } catch (error) {
    if (!error.message.includes('不支持的平台')) {
      throw new Error('错误消息不正确');
    }
  }
});

// 测试自动回复
asyncTest('自动生成回复 - 友好专业', async () => {
  const reply = await smm.autoReply('这个产品怎么样？', '友好专业');
  if (!reply.reply) throw new Error('缺少回复内容');
  if (!reply.sentiment) throw new Error('缺少情感分析');
  if (reply.tone !== '友好专业') throw new Error('语气不正确');
});

asyncTest('自动生成回复 - 幽默风趣', async () => {
  const reply = await smm.autoReply('哈哈，太有趣了！', '幽默风趣');
  if (!reply.reply) throw new Error('缺少回复内容');
  if (reply.sentiment !== 'positive') throw new Error('情感分析不正确');
});

asyncTest('自动生成回复 - 简洁直接', async () => {
  const reply = await smm.autoReply('质量太差了！', '简洁直接');
  if (!reply.reply) throw new Error('缺少回复内容');
  if (reply.sentiment !== 'negative') throw new Error('情感分析不正确');
});

// 测试表现分析
test('分析表现数据', () => {
  const posts = [
    { likes: 500, comments: 80, shares: 120, views: 8000, contentType: '评测' },
    { likes: 300, comments: 50, shares: 80, views: 5000, contentType: '教程' },
    { likes: 800, comments: 150, shares: 200, views: 12000, contentType: '种草' }
  ];
  
  const analysis = smm.analyzePerformance('xiaohongshu', 'last_30_days', posts);
  
  if (!analysis.metrics) throw new Error('缺少 metrics 字段');
  if (analysis.metrics.totalPosts !== 3) throw new Error('帖子数量不正确');
  if (analysis.metrics.totalLikes !== 1600) throw new Error('总点赞数不正确');
  if (!analysis.metrics.recommendations) throw new Error('缺少建议');
});

test('分析空数据', () => {
  const analysis = smm.analyzePerformance('xiaohongshu', 'last_30_days', []);
  if (!analysis.error) throw new Error('应该返回错误');
});

// 测试平台适配器
asyncTest('平台适配器 - 小红书发布', async () => {
  const result = await platform.post('xiaohongshu', { content: '测试内容' });
  if (!result.success) throw new Error('发布失败');
  if (!result.postId) throw new Error('缺少 postId');
});

asyncTest('平台适配器 - 微博发布', async () => {
  const result = await platform.post('weibo', { content: '测试内容' });
  if (!result.success) throw new Error('发布失败');
});

asyncTest('平台适配器 - Twitter 发布', async () => {
  const result = await platform.post('twitter', { content: 'Test content' });
  if (!result.success) throw new Error('发布失败');
});

asyncTest('平台适配器 - 获取评论', async () => {
  const comments = await platform.getComments('xiaohongshu', 'test_post');
  if (!Array.isArray(comments)) throw new Error('评论应该是数组');
  if (comments.length === 0) throw new Error('评论为空');
});

asyncTest('平台适配器 - 获取分析', async () => {
  const analytics = await platform.getAnalytics('xiaohongshu', 'last_30_days');
  if (!analytics.views) throw new Error('缺少 views 字段');
  if (!analytics.followers) throw new Error('缺少 followers 字段');
});

// 测试话题标签生成
test('生成话题标签', () => {
  const calendar = smm.generateContentCalendar('xiaohongshu', new Date(), '测试主题', 1);
  const hashtags = calendar.calendar[0].hashtags;
  
  if (!Array.isArray(hashtags)) throw new Error('话题标签应该是数组');
  if (hashtags.length === 0) throw new Error('话题标签为空');
  if (!hashtags.some(tag => tag.includes('测试主题'))) {
    throw new Error('缺少主题相关标签');
  }
});

// 测试互动率预估
test('预估互动量', () => {
  const calendar = smm.generateContentCalendar('xiaohongshu', new Date(), '测试', 1);
  const engagement = calendar.calendar[0].estimatedEngagement;
  
  if (typeof engagement !== 'number') throw new Error('互动量应该是数字');
  if (engagement <= 0) throw new Error('互动量应该大于 0');
});

// 输出结果
console.log('\n' + '='.repeat(50));
console.log(`测试结果：${passed} 通过，${failed} 失败`);
console.log('='.repeat(50));

if (failed > 0) {
  process.exit(1);
} else {
  console.log('\n🎉 所有测试通过！');
  process.exit(0);
}
