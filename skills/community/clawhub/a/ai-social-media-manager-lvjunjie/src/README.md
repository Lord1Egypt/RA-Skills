# AI-Social-Media-Manager API 文档

## 概述

AI-Social-Media-Manager 是一个强大的社交媒体管理工具，提供内容日历生成、智能调度、自动互动和数据分析功能。

## 快速开始

```javascript
const { SocialMediaManager } = require('./src/index');
const { PlatformAdapter } = require('./src/platform-adapter');

const smm = new SocialMediaManager();
const platform = new PlatformAdapter();
```

## 核心 API

### 1. 内容日历生成

```javascript
/**
 * 生成内容日历
 * @param {string} platform - 平台名称
 * @param {Date} month - 目标月份
 * @param {string} topic - 内容主题
 * @param {number} postCount - 帖子数量（默认 15）
 * @returns {Object} 日历对象
 */
const calendar = smm.generateContentCalendar(
  'xiaohongshu',
  new Date(2026, 2, 1),
  '科技产品评测',
  15
);
```

**返回示例：**
```json
{
  "month": "2026-03",
  "platform": "xiaohongshu",
  "totalPosts": 15,
  "calendar": [
    {
      "date": "2026-03-02",
      "time": "08:30",
      "platform": "xiaohongshu",
      "topic": "科技产品评测",
      "contentType": "评测",
      "contentStructure": "痛点 + 解决方案 + 产品亮点 + 使用体验 + 购买建议",
      "status": "planned",
      "hashtags": ["#小红书", "#种草", "#好物分享", "#科技产品评测"],
      "estimatedEngagement": 120
    }
  ],
  "summary": {
    "postsPerWeek": 4,
    "topHashtags": ["#小红书", "#种草", "#好物分享"],
    "platforms": ["xiaohongshu"],
    "estimatedTotalEngagement": 1800
  }
}
```

### 2. 最佳发布时间推荐

```javascript
/**
 * 获取最佳发布时间
 * @param {string} platform - 平台名称
 * @param {Date} date - 日期
 * @param {Object} audience - 受众分析（可选）
 * @returns {string} 推荐时间（HH:mm 格式）
 */
const bestTime = smm.getBestPostingTime(
  'xiaohongshu',
  new Date(),
  { ageRange: '18-35' }
);
// 返回："08:30"
```

**支持的受众参数：**
- `ageRange`: '18-25' | '25-35' | '35-50' | '50+'
- `location`: 地理位置（未来版本）
- `interests`: 兴趣标签（未来版本）

### 3. 自动回复和互动

```javascript
/**
 * 自动生成回复
 * @param {string} comment - 评论内容
 * @param {string} tone - 回复语气
 * @param {Object} context - 上下文信息
 * @returns {Promise<Object>} 回复对象
 */
const reply = await smm.autoReply(
  '这个产品怎么样？价格多少？',
  '友好专业',
  { productId: '123' }
);
```

**支持的回复语气：**
- `友好专业` - 适合大多数场景
- `幽默风趣` - 适合轻松话题
- `简洁直接` - 适合快节奏平台

**返回示例：**
```json
{
  "originalComment": "这个产品怎么样？价格多少？",
  "reply": "感谢您的关注和支持！关于价格，您可以在我们的官方店铺查看最新优惠哦~ 期待您的再次光临~",
  "tone": "友好专业",
  "sentiment": "neutral",
  "timestamp": "2026-03-15T14:30:00.000Z"
}
```

### 4. 表现分析和优化

```javascript
/**
 * 分析表现数据
 * @param {string} platform - 平台名称
 * @param {string} period - 时间段
 * @param {Array} posts - 帖子数据数组
 * @returns {Object} 分析报告
 */
const analysis = smm.analyzePerformance(
  'xiaohongshu',
  'last_30_days',
  [
    { likes: 500, comments: 80, shares: 120, views: 8000, contentType: '评测' },
    { likes: 300, comments: 50, shares: 80, views: 5000, contentType: '教程' }
  ]
);
```

**返回示例：**
```json
{
  "platform": "xiaohongshu",
  "period": "last_30_days",
  "metrics": {
    "totalPosts": 2,
    "totalLikes": 800,
    "totalComments": 130,
    "totalShares": 200,
    "totalViews": 13000,
    "avgEngagementRate": "8.69%",
    "bestPerformingPost": { ... },
    "worstPerformingPost": { ... },
    "growthRate": 15.5,
    "recommendations": [
      "互动率表现良好，继续保持",
      "参考最佳表现帖子的内容风格：评测",
      "小红书用户偏好真实体验和精美图片，建议增加生活化场景"
    ]
  },
  "generatedAt": "2026-03-15T14:30:00.000Z"
}
```

## 平台适配器 API

### 发布内容

```javascript
const platform = new PlatformAdapter();

const result = await platform.post('xiaohongshu', {
  title: '超好用的科技产品！',
  content: '最近发现了一个宝藏产品...',
  images: ['image1.jpg', 'image2.jpg'],
  tags: ['#科技', '#种草', '#好物分享']
});
```

### 获取评论

```javascript
const comments = await platform.getComments('xiaohongshu', 'post_123');
```

### 获取分析数据

```javascript
const analytics = await platform.getAnalytics('xiaohongshu', 'last_30_days');
```

## 支持的平台

| 平台 | 发布 | 评论 | 分析 | 最佳时段 |
|------|------|------|------|----------|
| 小红书 | ✅ | ✅ | ✅ | 8:00, 12:00, 19:00, 21:00 |
| 微博 | ✅ | ✅ | ✅ | 7:00, 12:00, 18:00, 22:00 |
| Twitter | ✅ | ✅ | ✅ | 9:00, 13:00, 17:00, 20:00 |
| LinkedIn | ✅ | ✅ | ✅ | 8:00, 12:00, 17:00 |
| Instagram | ✅ | ✅ | ✅ | 11:00, 14:00, 19:00, 21:00 |
| 微信公众号 | ✅ | ✅ | ✅ | 8:00, 12:00, 20:00, 22:00 |

## 内容模板

### 小红书模板
1. **评测** - 痛点 + 解决方案 + 产品亮点 + 使用体验 + 购买建议
2. **教程** - 目标 + 步骤分解 + 注意事项 + 常见问题
3. **种草** - 场景引入 + 产品发现 + 核心优势 + 个人体验 + 推荐理由
4. **对比** - 对比维度 + 产品 A + 产品 B + 总结建议

### 微博模板
1. **热点** - 事件 + 观点 + 互动问题
2. **分享** - 内容 + 感悟 + 话题标签
3. **互动** - 问题 + 选项 + 奖励

### Twitter 模板
1. **Thread** - 钩子 + 要点 1-5 + 总结 + CTA
2. **Update** - 进展 + 数据 + 下一步
3. **Engagement** - 问题 + 背景 + 邀请讨论

## 错误处理

```javascript
try {
  const calendar = smm.generateContentCalendar('invalid_platform', ...);
} catch (error) {
  console.error(error.message); // "不支持的平台：invalid_platform"
}
```

## 配置选项

在 `TOOLS.md` 中配置平台凭证：

```markdown
### Social Media

- xiaohongshu: 
  username: "your_username"
  cookie: "your_cookie"
  
- weibo:
  username: "your_username"
  password: "your_password"
  
- twitter:
  api_key: "your_api_key"
  api_secret: "your_api_secret"
  access_token: "your_access_token"
```

## 最佳实践

1. **内容规划** - 提前生成月度日历，保持一致性
2. **发布时间** - 根据平台特性选择最佳时段
3. **互动响应** - 及时回复评论，提升粉丝粘性
4. **数据驱动** - 定期分析表现，优化内容策略
5. **多平台协同** - 统一品牌形象，差异化内容

## 版本历史

- **v1.0.0** (2026-03-15) - 初始版本
  - 内容日历生成
  - 最佳发布时间推荐
  - 自动回复
  - 表现分析
  - 6 个平台支持

## 许可证

MIT License
