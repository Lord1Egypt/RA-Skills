# 小红书 + 飞猪浏览器自动化流程

本文档描述小红书旅游攻略搜索和飞猪机票查询的浏览器自动化操作流程。

---

## ⚠️ 超时处理策略

### 浏览器操作超时设置

**所有浏览器操作必须设置超时时间，避免无限等待：**

| 操作类型 | 超时时间 | 超时后处理 |
|----------|----------|------------|
| 页面打开 | 10 秒 | 使用模型知识库兜底 |
| 页面加载 | 5 秒 | 使用模型知识库兜底 |
| 元素查找 | 3 秒 | 跳过该步骤或使用备选方案 |
| 数据提取 | 5 秒 | 使用已获取的部分数据 |

### 超时处理示例

```javascript
// 浏览器操作设置超时
browser.open(url, timeout=10000)  // 10秒超时
browser.snapshot(delayMs=3000, timeout=5000)  // 5秒超时

// 超时后走模型兜底
try {
  const result = await browser.operation(timeout=10000)
} catch (timeout) {
  // 使用模型知识库生成内容
  return generateFromModelKnowledge()
}
```

### 兜底策略

**当浏览器操作超时时，使用以下兜底方案：**

1. **小红书攻略超时** → 使用通用旅游知识生成攻略
2. **机票查询超时** → 使用历史价格数据或估算价格
3. **数据提取超时** → 使用已获取的部分数据 + 模型补充

---

## 📱 小红书搜索流程

### 1. 打开小红书

```javascript
// 打开小红书首页
browser.open('https://www.xiaohongshu.com')
```

### 2. 登录检查

- 检查是否已登录（右上角用户头像）
- 未登录则显示二维码（需人工扫码）
- 登录状态会保持会话

### 3. 搜索攻略

```javascript
// 搜索框输入
browser.type('search-input', '{destination} 攻略')

// 点击搜索
browser.click('search-button')

// 等待结果加载
browser.wait('search-results', timeout=5000)
```

### 4. 筛选高互动内容

```javascript
// 按热度排序
browser.click('sort-by-popular')

// 提取前 10 篇笔记
notes = browser.evaluate(`
  document.querySelectorAll('.note-item').slice(0, 10).map(note => ({
    title: note.querySelector('.title')?.innerText,
    author: note.querySelector('.author')?.innerText,
    likes: parseNumber(note.querySelector('.likes')?.innerText),
    collects: parseNumber(note.querySelector('.collects')?.innerText),
    url: note.querySelector('a')?.href
  }))
`)
```

### 5. 进入笔记详情页

```javascript
// 点击笔记
browser.click(note_ref)

// 等待内容加载
browser.wait('note-content', timeout=3000)

// 提取正文内容
content = browser.evaluate(`
  document.querySelector('.note-content')?.innerText
`)
```

### 6. 数据提取字段

```json
{
  "title": "笔记标题",
  "author": "作者昵称",
  "likes": "点赞数（数字）",
  "collects": "收藏数（数字）",
  "comments": "评论数（数字）",
  "content": "正文内容",
  "images": ["图片 URL 列表"],
  "tags": ["话题标签"],
  "publish_date": "发布日期",
  "url": "笔记链接"
}
```

---

## ✈️ 飞猪机票查询流程

### URL 模板

**直接跳转搜索结果页（推荐）：**

单程：
```
https://sjipiao.fliggy.com/flight_search_result.htm?tripType=0&depCity={出发城市三字码}&arrCity={到达城市三字码}&depDate={出发日期}&depCityName={出发城市名URL编码}&arrCityName={到达城市名URL编码}
```

往返：
```
https://sjipiao.fliggy.com/flight_search_result.htm?tripType=1&depCity={出发城市三字码}&arrCity={到达城市三字码}&depCityName={出发城市名URL编码}&arrCityName={到达城市名URL编码}&depDate={出发日期}&arrDate={返程日期}
```

**参数说明：**

| 参数 | 说明 | 示例 |
|------|------|------|
| tripType | 行程类型：0=单程，1=往返 | 0 |
| depCity | 出发城市三字码 | BJS（北京） |
| arrCity | 到达城市三字码 | HGH（杭州） |
| depDate | 出发日期 | 2026-03-17 |
| arrDate | 返程日期（往返时必填） | 2026-03-20 |
| depCityName | 出发城市名（URL编码） | %E5%8C%97%E4%BA%AC |
| arrCityName | 到达城市名（URL编码） | %E6%9D%AD%E5%B7%9E |

**常用城市三字码：**

| 城市 | 三字码 | 城市 | 三字码 |
|------|--------|------|--------|
| 北京 | BJS | 上海 | SHA |
| 广州 | CAN | 深圳 | SZX |
| 杭州 | HGH | 成都 | CTU |
| 西安 | SIA | 重庆 | CKG |
| 南京 | NKG | 武汉 | WUH |
| 三亚 | SYX | 昆明 | KMG |
| 大理 | DLU | 丽江 | LJG |

### 1. 打开飞猪机票搜索页

```javascript
// 构建搜索 URL
const depCity = 'BJS'  // 出发城市三字码
const arrCity = 'HGH'  // 到达城市三字码
const depDate = '2026-03-17'
const arrDate = '2026-03-20'  // 往返时需要
const depCityName = encodeURIComponent('北京')
const arrCityName = encodeURIComponent('杭州')

// 单程
const oneWayUrl = `https://sjipiao.fliggy.com/flight_search_result.htm?tripType=0&depCity=${depCity}&arrCity=${arrCity}&depDate=${depDate}&depCityName=${depCityName}&arrCityName=${arrCityName}`

// 往返
const roundTripUrl = `https://sjipiao.fliggy.com/flight_search_result.htm?tripType=1&depCity=${depCity}&arrCity=${arrCity}&depCityName=${depCityName}&arrCityName=${arrCityName}&depDate=${depDate}&arrDate=${arrDate}`

// 直接打开搜索结果页
browser.open(roundTripUrl)
```

### 2. 登录

- 首次使用需要手动扫码登录
- 登录状态会保持会话，后续无需重复登录

### 3. 提取航班信息

```javascript
// 等待结果加载
browser.wait('flight-results', timeout=10000)

// 按价格排序
browser.click('sort-by-price')

// 提取最低价航班
flights = browser.evaluate(`
  document.querySelectorAll('.flight-item').slice(0, 5).map(flight => ({
    price: parsePrice(flight.querySelector('.price')?.innerText),
    departure_time: flight.querySelector('.departure-time')?.innerText,
    arrival_time: flight.querySelector('.arrival-time')?.innerText,
    flight_number: flight.querySelector('.flight-number')?.innerText,
    airline: flight.querySelector('.airline')?.innerText,
    duration: flight.querySelector('.duration')?.innerText,
    stops: flight.querySelector('.stops')?.innerText,
    booking_url: flight.querySelector('a')?.href
  }))
`)
```

### 4. 数据提取字段

```json
{
  "price": "价格（数字，单位：元）",
  "departure_flight": "去程航班号",
  "departure_time": "去程起飞时间",
  "return_flight": "返程航班号",
  "return_time": "返程到达时间",
  "airline": "航空公司",
  "duration": "飞行时长",
  "stops": "中转信息",
  "booking_url": "预订链接"
}
```

---

## 🔄 失败处理策略

### 小红书

| 错误 | 处理策略 |
|------|----------|
| 未登录 | 显示二维码，等待人工扫码 |
| 搜索无结果 | 尝试简化关键词（去掉"攻略"） |
| 内容加载失败 | 刷新页面，重试 1 次 |
| 验证码 | 通知人工介入 |

### 飞猪

| 错误 | 处理策略 |
|------|----------|
| 未登录 | 提示用户手动扫码登录 |
| 登录失败 | 提示用户重新扫码 |
| 查询无结果 | 检查日期是否过期 |
| 价格加载失败 | 等待 3 秒后重试 |
| 验证码 | 通知人工介入 |

---

## 🎯 优化技巧

### 小红书

1. **搜索词优化**
   - 基础：`{目的地} 攻略`
   - 进阶：`{目的地} X 天 X 夜`、`{目的地} 必去`、`{目的地} 避雷`
   
2. **筛选高质内容**
   - 优先选择点赞>1000 的笔记
   - 优先选择最近 3 个月的内容
   - 优先选择带详细行程的笔记

3. **防反爬策略**
   - 请求间隔 2-3 秒

### 飞猪

1. **直接跳转搜索结果页**
   - 使用 URL 模板直接跳转，跳过首页操作
   - 减少页面加载和交互步骤

2. **价格排序**
   - 默认按价格升序排列
   - 提取前 5 个航班供用户选择