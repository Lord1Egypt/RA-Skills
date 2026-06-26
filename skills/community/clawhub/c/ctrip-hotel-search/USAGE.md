# 使用指南

## 基本使用

### 1. 安装和配置

```bash
# 进入技能目录
cd ~/.openclaw/workspace/skills/ctrip-hotel-search

# 安装依赖
npm install
npx playwright install

# 配置账号
# 编辑 config.json，填入您的携程账号密码
```

### 2. 搜索酒店

```javascript
const { search } = require('./src/index');

// 搜索建水古城酒店
const result = await search({
  city: '建水古城',
  checkInDate: '2026-04-09',
  checkOutDate: '2026-04-10',
  priceRange: { min: 200, max: 400 }
});

console.log(result.report);
```

### 3. 查看结果

搜索结果包含：
- 酒店列表（名称、价格、评分、位置）
- 对比分析（性价比、评分排序）
- 推荐列表（最经济、评分最高、性价比最高）

## 针对您的行程

### 建水古城（4月9日）

```javascript
const jianshui = await search({
  city: '建水古城',
  checkInDate: '2026-04-09',
  checkOutDate: '2026-04-10',
  priceRange: { min: 200, max: 400 },
  hotelType: 'homestay'  // 优先搜索民宿
});
```

### 南沙镇（4月12日）

```javascript
const nansha = await search({
  city: '南沙镇',
  checkInDate: '2026-04-12',
  checkOutDate: '2026-04-13',
  priceRange: { min: 150, max: 300 },
  hotelType: 'homestay'
});
```

## 高级功能

### 获取酒店详情

```javascript
const result = await search({
  city: '建水古城',
  checkInDate: '2026-04-09',
  checkOutDate: '2026-04-10',
  getDetails: true  // 获取详细信息
});
```

### 对比多家酒店

```javascript
// 搜索结果自动包含对比分析
const result = await search({/* params */});
console.log(result.comparison.recommendations);
```

## 常见问题

### Q: 遇到验证码怎么办？
A: 技能会自动检测验证码，需要手动完成登录。建议提前手动登录一次携程。

### Q: 搜索不到结果？
A: 检查城市名称是否正确，尝试使用更通用的名称（如"元阳"代替"南沙镇"）。

### Q: 如何搜索民宿？
A: 设置 `hotelType: 'homestay'`，或在搜索后筛选包含"民宿"、"客栈"关键词的酒店。