# 1688 Data Claw - 数据采集浏览器插件

> 专为 OpenClaw 设计的 1688.com 商品数据采集器，支持列表页和详情页自动/手动采集，提供标准化 API 接口。

---

## 功能特性

- **自动采集**：在 1688 页面加载完成后自动提取数据
- **列表页采集**：搜索列表、店铺商品列表的批量采集
- **详情页采集**：单个商品完整信息（标题、价格、SKU、图片、店铺、物流等）
- **数据去重**：基于 `offerId` 自动合并，避免重复数据
- **数据导出**：支持 CSV 和 JSON 格式导出
- **OpenClaw API**：提供标准化接口，供外部脚本/扩展调用
- **实时汇总**：数据即时同步，统计信息实时更新
- **SPA 路由监听**：支持 1688 单页应用的无刷新页面切换

---

## 文件结构

```
1688-data-claw/
├── manifest.json          # 扩展配置文件 (Manifest V3)
├── content.js             # 内容脚本 - 页面数据采集逻辑
├── background.js          # 后台脚本 - 数据存储、汇总、API接口
├── popup.html             # 弹出界面 HTML
├── popup.js               # 弹出界面交互逻辑
├── openclaw-bridge.js     # OpenClaw 调用桥接脚本
├── icons/  _(可选，未提供时 Chrome 显示默认占位图标)_
│   ├── icon16.png         # 16x16 图标
│   ├── icon48.png         # 48x48 图标
│   ├── icon128.png        # 128x128 图标
│   └── icon128.svg        # SVG 源文件
└── docs/                  # 文档目录 (预留)
```

---

## 安装方法

### 1. 加载未打包扩展

1. 打开 Chrome 浏览器，访问 `chrome://extensions/`
2. 打开右上角 **开发者模式** 开关
3. 点击 **加载已解压的扩展程序**
4. 选择 `1688-data-claw` 文件夹
5. 扩展安装成功，工具栏出现橙色图标

### 2. 验证安装

- 点击工具栏的橙色图标，弹出控制面板
- 访问任意 1688 商品页面，图标状态应变为 **就绪**
- 打开控制台 (F12)，应能看到 `[1688-Claw]` 日志输出

---

## 使用指南

### 手动采集

1. 打开 1688 商品列表页或详情页
2. 点击工具栏的 **1688 Data Claw** 图标
3. 点击 **立即采集当前页** 按钮
4. 等待采集完成，查看统计数据

### 自动采集

内容脚本会在页面加载完成后 **自动执行采集**，无需手动操作。数据会自动发送到后台脚本进行汇总和存储。

### 数据导出

在弹出面板中点击：
- **导出 CSV** — 下载列表商品为 CSV 文件（可用 Excel 打开）
- **导出 JSON** — 下载完整数据为 JSON 文件
- **查看数据** — 在新标签页打开 JSON 数据预览

### 清空数据

点击 **清空数据** 按钮，将删除所有已采集的数据（不可恢复）。

---

## 采集数据字段

### 列表页数据

| 字段 | 说明 |
|------|------|
| `offerId` | 商品唯一ID |
| `title` | 商品标题 |
| `price` | 价格（数值） |
| `priceText` | 价格原始文本 |
| `image` | 主图链接 |
| `url` | 商品链接 |
| `shop` | 店铺名称 |
| `shopUrl` | 店铺链接 |
| `sold` | 销量/成交数 |
| `location` | 发货地 |
| `tags` | 商品标签数组 |
| `keyword` | 搜索关键词 |
| `_addedAt` | 采集时间 |

### 详情页数据

| 字段 | 说明 |
|------|------|
| `offerId` | 商品唯一ID |
| `title` | 商品标题 |
| `price` | 当前价格 |
| `originalPrice` | 原价 |
| `images` | 主图链接数组 |
| `skus` | SKU规格数组（含名称、属性值） |
| `attributes` | 商品参数数组（含名称、值） |
| `shop` | 店铺信息（名称、链接、认证标识） |
| `logistics` | 物流信息（发货地、运费） |
| `sales` | 交易数据（销量、评价数） |
| `category` | 商品类目路径 |
| `brand` | 品牌名称 |
| `moq` | 最小起订量 |
| `supportDaifa` | 是否支持代发 |
| `descriptionImages` | 详情描述图数组 |
| `_addedAt` | 采集时间 |

### 生意参谋 (sycm) 数据

| 字段 | 说明 |
|------|------|
| `companyName` | 公司名称（如：福州远集创科跨境电子商务有限公司） |
| `companyUrl` | 店铺主页链接 |
| `category` | 主营类目（如：宠物及园艺） |
| `subCategory` | 子类目（如：猫狗用品） |
| `identity` | 会员身份（如：svip） |
| `competeVersion` | 竞争情报版本（如：ultimate） |
| `isSvip` | 是否为SVIP |
| `hasSigned` | 是否已签约 |
| `isSudo` | 是否为管理员 |
| `rawUser` | 原始用户信息（完整数据结构） |
| `rawDiamond` | 原始Diamond配置数据 |
| `pageData.title` | 页面标题 |
| `pageData.urlPath` | 页面路径 |
| `rankTrend.lastDate` | 排名数据日期（如：2026-06-16） |
| `rankTrend.rank` | 店铺排名（如：4981） |
| `rankTrend.payAmt` | 支付金额（如：992.47） |
| `rankTrend.cateLevel1` | 一级类目（如：宠物及园艺） |
| `rankTrend.cateLevel2` | 二级类目（如：猫狗用品） |
| `rankTrend.layer` | 类目层级（如：1） |
| `rankTrend.rawDates` | 原始30天日期时间戳数组 |
| `rankTrend.rawRanks` | 原始30天排名数组 |
| `rankTrend.rawPayAmt` | 原始30天支付金额数组 |
| `itemOverview.statDate` | 概况数据日期（如：2026-06-17） |
| `itemOverview.itemCnt` | **在线商品数**（如：102） |
| `itemOverview.pullSalesItemCnt` | **动销商品数**（如：0） |
| `itemOverview.uv` | 商品访客数（如：13） |
| `itemOverview.payItemQty` | 支付商品数（如：0） |
| `itemOverview.hasVisitorItemCnt` | 有访客商品数（如：14） |
| `itemOverview.itemPv` | 商品浏览量（如：31） |
| `itemOverview.raw` | 原始概况数据 |
| `flowStats.statDate` | 流量数据日期 |
| `flowStats.revealCnt` | **展现次数** |
| `flowStats.pv` | **浏览量** |
| `flowStats.uv` | **访客数** |
| `flowStats.clickRate` | **点击转化率**（pv/revealCnt） |
| `flowStats.avgPvs` | **人均浏览量**（pv/uv） |
| `flowStats.bounceRate` | **跳失率** |
| `flowStats.payByrCnt` | 支付买家数 |
| `flowStats.payAmt` | 支付金额 |
| `flowStats.mobileUv` | 无线端访客数 |
| `flowStats.mobilePv` | 无线端浏览量 |
| `flowStats.mobileShare` | **无线端占比**（无线端uv/全平台uv） |
| `flowStats.allRaw` | 全平台原始数据 |
| `flowStats.mobileRaw` | 无线端原始数据 |
| `inquiry.statDate` | 询盘数据日期 |
| `inquiry.effectiveInQUsers` | **询盘人数**（如：3） |
| `inquiry.wangInQUsers` | 旺旺询盘人数 |
| `inquiry.bEffectiveInQUsers` | 访客询盘人数 |
| `inquiry.bWangInQUsers` | 访客旺旺询盘人数 |
| `inquiry.effectInQCnt` | 有效询盘次数 |
| `inquiry.wangInQCnt` | 旺旺询盘次数 |
| `inquiry.factoryInQUsers` | 工厂询盘人数 |
| `inquiry.factoryWangInQUsers` | 工厂旺旺询盘人数 |
| `inquiry.factorySheetInQUsers` | 工厂表单询盘人数 |
| `inquiry.factoryPhoneInQUsers` | 工厂电话询盘人数 |
| `inquiry.factoryPerfectInQUsers` | 工厂优质询盘人数 |
| `inquiry.repeatRate` | 回头率 |
| `inquiry.cateScoreFh` | 响应评分 |
| `inquiry.cateScoreHm` | 货描评分 |
| `inquiry.cateScoreXy` | 信用评分 |
| `inquiry.scorefh` | 响应服务分 |
| `inquiry.scorehm` | 货描服务分 |
| `inquiry.scorexy` | 信用服务分 |
| `inquiry.raw` | 原始询盘数据 |
| `trade.statDate` | 交易数据日期 |
| `trade.payAmt` | **支付金额** |
| `trade.payByrCnt` | **支付买家数** |
| `trade.payItemQty` | **支付商品件数** |
| `trade.payRate` | **支付转化率**（支付买家数/访客数） |
| `trade.perByrAmt` | **客单价**（支付金额/支付买家数） |
| `trade.rfdSucAmt` | **退款金额** |
| `trade.refundRate` | **退款金额占比**（退款金额/支付金额） |
| `trade.payMordCnt` | **支付订单数** |
| `trade.payNewByrCnt` | **支付新买家数** |
| `trade.payOldByrCnt` | 支付老买家数 |
| `trade.payToOnRate` | 支付到款率 |
| `trade.newBuyerAmt` | 新买家支付金额（payAmt - oldPayByrAmt） |
| `trade.newBuyerShare` | 新客成交占比（新买家支付金额 / 支付金额） |
| `trade.oldBuyerShare` | 老客复购占比（老买家数 / 支付买家数） |
| `trade.oldBuyerPerAmt` | 老客客单价（老买家支付金额 / 老买家数） |
| `trade.raw` | 原始交易数据 |
| `work.wwResponse.score` | **3分钟响应率**（如：97.73） |
| `work.wwResponse.display` | 响应率显示文本（如：97.73） |
| `work.wwResponse.name` | 指标名称（如：3分钟响应率） |
| `work.wwSatisfaction.score` | **咨询满意度**（如：100.0） |
| `work.wwSatisfaction.display` | 满意度显示文本（如：100.0） |
| `work.wwSatisfaction.name` | 指标名称（如：咨询满意度） |
| `_addedAt` | 采集时间 |

---

## OpenClaw 调用接口

### 方法一：外部消息 (推荐)

从其他 Chrome 扩展或页面脚本调用：

```javascript
// 替换为你的扩展 ID (从 chrome://extensions/ 查看)
const EXTENSION_ID = 'your-extension-id-here';

// 获取完整数据 (列表 + 详情)
chrome.runtime.sendMessage(EXTENSION_ID, {
  action: 'OPEN_CLAW_API',
  mode: 'full',
  limit: 50
}, (response) => {
  console.log('1688数据:', response.data);
});

// 获取列表商品
chrome.runtime.sendMessage(EXTENSION_ID, {
  action: 'OPEN_CLAW_API',
  mode: 'items',
  keyword: '手机壳',  // 可选：按关键词过滤
  limit: 30
}, (response) => {
  console.log('商品列表:', response.data.items);
});

// 获取特定商品详情
chrome.runtime.sendMessage(EXTENSION_ID, {
  action: 'OPEN_CLAW_API',
  mode: 'details',
  offerId: '610947572360'
}, (response) => {
  console.log('商品详情:', response.data.details);
});

// 获取数据汇总
chrome.runtime.sendMessage(EXTENSION_ID, {
  action: 'OPEN_CLAW_API',
  mode: 'summary'
}, (response) => {
  console.log('数据汇总:', response.data);
});

// 获取生意参谋数据
chrome.runtime.sendMessage(EXTENSION_ID, {
  action: 'OPEN_CLAW_API',
  mode: 'sycm',
  limit: 30
}, (response) => {
  console.log('生意参谋:', response.data.sycm);
});
```

### 方法二：使用桥接脚本

1. 引入 `openclaw-bridge.js` 文件
2. 设置扩展 ID
3. 调用便捷函数

```javascript
// 引入桥接脚本
// <script src="openclaw-bridge.js"></script>

// 设置扩展 ID (从插件弹出面板中查看)
setClawExtensionId('your-extension-id-here');

// 获取数据
const result = await clawAll(50);
console.log(result.data);

// 按关键词过滤
const items = await clawItems('数据线', 20);
console.log(items.data.items);

// 获取详情
const details = await clawDetails('610947572360');
console.log(details.data.details);

// 获取汇总
const summary = await clawSummary();
console.log(summary.data);

// 获取生意参谋数据
const sycm = await clawSycm(20);
console.log(sycm.data.sycm);

// 获取工作台数据
const work = await clawWork(20);
console.log(work.data.work);
```

### 方法三：从插件内部调用

在同一个扩展的其他脚本中直接调用：

```javascript
chrome.runtime.sendMessage({
  action: 'GET_ALL_DATA'
}, (response) => {
  console.log('全部数据:', response.data);
});

chrome.runtime.sendMessage({
  action: 'GET_ITEMS',
  filter: { minPrice: 10, maxPrice: 100 },
  limit: 20
}, (response) => {
  console.log('过滤结果:', response.items);
});

chrome.runtime.sendMessage({
  action: 'GET_DETAILS',
  offerId: '610947572360'
}, (response) => {
  console.log('详情:', response.details);
});
```

---

## API 响应格式

### 成功响应

```json
{
  "success": true,
  "clawVersion": "1.0.0",
  "source": "1688-data-claw",
  "data": {
    "items": [...],
    "details": [...],
    "stats": {
      "totalItems": 42,
      "totalDetails": 15,
      "lastUpdate": "2024-06-18T10:30:00.000Z"
    }
  }
}
```

### 错误响应

```json
{
  "success": false,
  "error": "未设置扩展ID"
}
```

---

## 获取扩展 ID

1. 打开 Chrome 扩展管理页面：`chrome://extensions/`
2. 找到 **1688 Data Claw**
3. 复制 **ID** 字段（如：`abcdefgh1234567890abcdef`）
4. 在 OpenClaw 脚本中填入此 ID

> 提示：也可以在点击插件图标后，在 **OpenClaw API** 区域直接看到扩展 ID。

---

## 数据存储

- 所有数据存储在 Chrome 的 `localStorage` 中
- 数据在浏览器会话间持久保存
- 存储上限约为 5MB（Chrome 扩展限制）
- 建议定期导出并清空旧数据

---

## 支持页面类型

| 页面类型 | 自动识别 | 采集内容 |
|---------|---------|---------|
| 商品详情页 (`/offer/xxxx.html`) | 是 | 完整详情 |
| 搜索列表页 (`s.1688.com`) | 是 | 商品列表 |
| 店铺列表页 | 是 | 商品列表 |
| 生意参谋 (`sycm.1688.com`) | 是 | 公司信息、类目、店铺链接 |
| 工作台 (`work.1688.com`) | 是 | 旺旺响应率、咨询满意度 |
| 其他 1688 页面 | 否 | 跳过 |

---

## 常见问题

**Q: 采集的数据不完整？**
A: 1688 页面结构经常更新，可能需要调整 `content.js` 中的 CSS 选择器。打开控制台查看 `[1688-Claw]` 日志定位问题。

**Q: 扩展无法安装？**
A: 确保使用 Chrome 浏览器，已开启开发者模式，选择的是包含 `manifest.json` 的文件夹。

**Q: OpenClaw 调用返回错误？**
A: 检查扩展 ID 是否正确；检查目标扩展是否已安装并启用；检查 `chrome.runtime.sendMessage` 的第一个参数是否为字符串格式的 ID。

**Q: 数据存储满了？**
A: 点击弹出面板中的 **清空数据** 或导出后手动删除。

---

## 技术栈

- **Manifest V3** - Chrome 扩展最新标准
- **Service Worker** - 后台脚本运行环境
- **Content Script** - 页面注入与数据采集
- **Chrome Storage API** - 本地数据持久化
- **Chrome Runtime Messaging** - 跨组件通信
- **Chrome External Messaging** - 外部扩展调用

---

## 版本信息

- **当前版本**: 1.0.0
- **兼容浏览器**: Chrome 88+ (Manifest V3)
- **开发日期**: 2024-06

---

## 开发计划

- [ ] 支持更多 1688 子页面类型
- [ ] 批量详情页自动采集（列表页点击后自动进入详情）
- [ ] 数据定时自动备份到云端
- [ ] 支持更多导出格式（Excel、SQL）
- [ ] 价格变动监控和历史趋势
- [ ] 图片批量下载功能

---

## 许可证

MIT License — 自由使用、修改和分发。

---

> **提示**: 本插件仅供学习和技术研究使用，请遵守 1688 平台的服务条款和 robots.txt 协议，不要用于大规模商业爬虫或侵犯他人权益。
