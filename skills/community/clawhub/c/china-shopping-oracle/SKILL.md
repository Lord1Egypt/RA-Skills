---
name: china-shopping-oracle
description: 国内全平台比价工具。Compare prices on Taobao/JD/Pinduoduo. Supports member pricing (88VIP/Plus). 电商比价、购物助手。
version: 1.1.1
license: MIT-0
metadata: {"openclaw": {"emoji": "🛒", "requires": {"bins": ["python3"], "env": []}}}
---

# China Shopping Oracle

国内全平台（淘宝/京东/拼多多）比价工具。

## Features

- 🛒 **多平台比价**: 淘宝、京东、拼多多同时搜索
- 💰 **会员价格**: 支持88VIP/Plus真实到手价
- ⚡ **并行调度**: 多页签同时工作
- 📊 **决策矩阵**: 生成清晰的价格对比表
- 🌍 **多语言**: 支持中英文输出

## Trigger Conditions

- "帮我比价XXX" / "Compare prices for XXX"
- "淘宝京东拼多多哪个便宜" / "Which platform is cheaper for XXX"
- "XXX在哪里买最划算" / "Best deal for XXX"
- "查一下XXX的价格" / "Check price for XXX"
- "比一比XXX" / "Compare XXX prices"

---

## Prerequisites

### OpenClaw 版本要求
- **OpenClaw v2026.3.22+**

### 支持的浏览器
- ✅ Google Chrome
- ✅ Brave Browser  
- ✅ Microsoft Edge
- ✅ 其他 Chromium 内核浏览器

### 配置步骤
1. 确保已安装 OpenClaw v2026.3.22+
2. 在浏览器中登录淘宝/京东/拼多多
3. 配置 OpenClaw browser 工具
4. 使用浏览器工具进行搜索

---

## Step 1: Environment Check

```
使用前请确保：
1. 已登录淘宝/京东/拼多多（至少一个）
2. 浏览器未关闭
3. 网络连接正常
```

---

## Step 2: Parse User Request

分析用户请求，提取：
1. **商品关键词** - 用户想比价的商品
2. **平台选择** - 默认三平台，可指定
3. **价格类型** - 是否包含会员价

---

## Step 3: Browser Search

使用浏览器工具进行搜索。自动继承用户浏览器会话，无需手动登录。

### 搜索流程

1. 打开淘宝搜索页面
2. 打开京东搜索页面
3. 打开拼多多搜索页面
4. 提取各平台商品数据（标题、价格、店铺、销量）

---

## Step 4: Data Processing

### 价格标准化
- 提取价格数字
- 移除货币符号
- 统一格式

### 会员价格计算

| 平台 | 会员类型 | 折扣 |
|------|----------|------|
| 淘宝 | 88VIP | 95折 |
| 京东 | Plus | 98折 |
| 拼多多 | 会员 | 98折 |

---

## Step 5: Comparison Report

### 中文报告示例

```
商品比价报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
关键词：iPhone 16 Pro 256GB

价格对比：
| 排名 | 平台 | 价格 | 会员价 | 店铺 | 销量 |
|------|------|------|--------|------|------|
| 1 | 拼多多 | ¥8,999 | ¥8,819 | 官方旗舰店 | 10万+ |
| 2 | 京东 | ¥9,199 | ¥9,015 | Apple官方 | 50万+ |
| 3 | 淘宝 | ¥9,299 | ¥8,834 | Apple官旗 | 100万+ |

购买建议：
- 最低价：拼多多 ¥8,999
- 最可靠：京东（自营正品保障）
- 88VIP最优：淘宝 ¥8,934
```

### 英文报告示例

```
Price Comparison Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Keyword: iPhone 16 Pro 256GB

| Rank | Platform | Price | Member Price | Shop | Sales |
|------|----------|-------|--------------|------|-------|
| 1 | Pinduoduo | ¥8,999 | ¥8,819 | Official | 100K+ |
| 2 | JD.com | ¥9,199 | ¥9,015 | Apple Official | 500K+ |
| 3 | Taobao | ¥9,299 | ¥8,834 | Apple Flagship | 1M+ |

Recommendation:
- Lowest: Pinduoduo ¥8,999
- Most Reliable: JD.com
- Best 88VIP: Taobao ¥8,934
```

---

## Error Handling

```
浏览器未配置       → 提示用户配置 OpenClaw browser 工具
页面加载失败       → 跳过该平台，报告其他平台结果
价格提取失败       → 标记为"价格获取失败"
DOM结构变化        → 使用备用选择器或提示用户反馈
```

---

## Multi-Language Support

输出语言自动匹配用户输入语言：
- 中文输入 → 中文报告
- English input → English report

---

## Limitations

- **价格时效**: 价格随时变化，仅供参考
- **DOM变化**: 平台页面结构变化可能导致提取失败
- **会员价格**: 需要用户已开通会员才能获取会员价
- **浏览器依赖**: 需要 OpenClaw 配置好 browser 工具

---

## Privacy & Security

### Browser Access

此 skill 需要浏览器工具来访问电商网站。

- 使用浏览器搜索商品
- 访问已登录的电商页面
- 获取价格信息

### Data Handling

- ✅ 不上传数据到外部服务器
- ✅ 所有处理在本地完成
- ⚠️ 执行期间使用浏览器工具

### Recommendations

1. **交互式使用**: 手动运行，不作为自动化后台任务
2. **安装前审查**: 了解将访问的数据

---

## Notes

- 使用浏览器工具访问电商网站
- 价格仅供参考，以实际下单为准
- 支持 50+ 语言输出
- 首次使用请确保浏览器已登录各平台