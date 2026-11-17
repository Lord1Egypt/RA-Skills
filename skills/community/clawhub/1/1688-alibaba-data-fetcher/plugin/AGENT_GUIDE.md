# 1688 Data Claw - Agent 使用指南

## 插件简介

**1688 Data Claw** 是一个 Chrome 扩展插件，用于在 1688 卖家工作台和生意参谋页面自动采集店铺经营数据。插件通过 Chrome Extension API 暴露数据接口，供外部 Agent（如 OpenClaw）调用。

## 安装方式

1. 将插件文件夹加载到 Chrome 浏览器：
   - 打开 Chrome，访问 `chrome://extensions/`
   - 开启右上角 **"开发者模式"**
   - 点击 **"加载已解压的扩展程序"**
   - 选择插件文件夹（`1688-data-claw/`）

2. 插件安装后，在 1688 相关页面自动运行内容脚本采集数据。

## 支持的页面类型

| 页面类型 | URL 匹配 | 采集内容 |
|---------|---------|---------|
| **生意参谋** | `sycm.1688.com` | 店铺排名、支付金额、商品概况、流量统计、询盘、交易、近7天流量来源、入店关键词 |
| **工作台** | `work.1688.com` | 旺旺响应率、咨询满意度、物流指标、品质退款率、新灯塔评分 |

## OpenClaw API

插件通过 Chrome 外部消息 API 提供数据访问接口。

### 获取扩展 ID

在插件 popup 中查看 **扩展 ID** 字段，或通过代码获取：

```javascript
// 固定扩展 ID
chrome.runtime.sendMessage('ekmgnempbbamlmaolijdfjakeopniion', { action: 'GET_VERSION' }, (resp) => {
  console.log(resp);
});
```

```json
// manifest.json 关键配置
{
  "externally_connectable": {
    "matches": ["https://*.1688.com/*", "https://1688.com/*"],
    "ids": ["*"]
  }
}
```

此配置允许：
- 所有 Chrome 扩展（`"ids": ["*"]`）向本插件发送外部消息
- 1688 域名下的网页通过 `chrome.runtime` 与插件通信

### 获取数据

```javascript
chrome.runtime.sendMessage('ekmgnempbbamlmaolijdfjakeopniion', {
  action: 'OPEN_CLAW_API',
  mode: 'full',      // 'full' | 'sycm' | 'work' | 'summary'
  limit: 50          // 可选，返回条数限制
}, (response) => {
  console.log(response.data);
});
```

### Mode 说明

| mode | 返回数据 |
|-----|---------|
| `full` | 所有数据（sycm + work + stats） |
| `sycm` | 仅生意参谋数据 |
| `work` | 仅工作台数据 |
| `summary` | 汇总统计 |

### 触发采集

`TRIGGER_CLAW_CONTENT` 是**内部消息 action**，仅能在 popup 或扩展内部页面中调用，**无法通过外部 API 调用**。如需通过外部 Agent 触发，需先访问目标页面等待自动采集，或借助其他扩展中转内部消息。

```javascript
// 仅限扩展内部调用（popup 或扩展页面）
chrome.runtime.sendMessage({
  action: 'TRIGGER_CLAW_CONTENT'
}, (response) => {
  console.log(response);
});
```

## 数据结构

### 生意参谋数据（sycm）

```javascript
{
  _pageType: 'sycm',
  companyName: '公司名称',
  companyUrl: '公司主页',
  category: '主营类目',
  subCategory: '子类目',
  identity: '店铺身份',
  isSvip: false,
  
  // 排名趋势
  rankTrend: {
    statDate: '2026-06-17',
    rank: 5,              // 层级排名
    layer: 3,             // 层级
    cateLevel2: '二级类目',
    payAmt: 12345.67      // 支付金额
  },
  
  // 商品概况
  itemOverview: {
    itemCnt: 100,         // 商品总数
    pullSalesItemCnt: 50  // 动销商品数
  },
  
  // 流量统计
  flowStats: {
    statDate: '2026-06-17',
    revealCnt: 1000,      // 展现次数
    pv: 500,              // 浏览量
    uv: 200,              // 访客数
    bounceRate: 0.3,      // 跳失率
    payByrCnt: 10,        // 支付买家数
    payAmt: 5000,         // 支付金额
    mobileShare: 0.6      // 无线端占比
  },
  
  // 询盘概况
  inquiry: {
    statDate: '2026-06-17',
    effectiveInQUsers: 5,    // 有效询盘人数
    wangInQUsers: 3,          // 旺旺询盘人数
    // ... 其他询盘字段
  },
  
  // 交易概况
  trade: {
    statDate: '2026-06-17',
    payAmt: 5000,         // 支付金额
    payByrCnt: 10,        // 支付买家数
    payNewByrCnt: 3,      // 新买家数
    payOldByrCnt: 7,      // 老买家数
    payItemQty: 20,       // 支付商品件数
    payMordCnt: 15,       // 支付订单数
    payRate: 0.05,        // 支付转化率
    perByrAmt: 500,       // 客单价
    rfdSucAmt: 200,       // 退款金额
    refundRate: 0.04      // 退款率
  },
  
  // 近7天流量来源
  flowSourceRecent7: {
    dateRange: '2026-06-11|2026-06-17',
    sources: [
      { name: '搜索', myUv: 50, goodUv: 249 },
      { name: '1688首页推荐', myUv: 8, goodUv: 156 }
    ],
    totalMyUv: 103,
    totalGoodUv: 758
  },
  
  // 近7天入店关键词
  keywordsRecent7: {
    dateRange: '2026-06-11|2026-06-17',
    keywords: [
      {
        keyword: '宠物冰垫',
        keywordRevealCnt: 82,    // 展现数
        uv: 3,                    // 访客数
        leadPayAmt: 0,           // 引导支付金额
        clickRate: 0.036,        // 点击率
        webSearchIndex: 6014,    // 搜索指数
        revealItem: 9            // 曝光商品数
      }
    ],
    totalKeywordReveal: 1000,
    totalLeadPayAmt: 0
  }
}
```

### 工作台数据（work）

```javascript
{
  _pageType: 'work',
  url: 'https://work.1688.com/...',
  
  // 旺旺服务
  wwResponse: {
    score: 95.0,
    display: '95.0',
    time: '06.17',
    averageScore: '90%',
    excellentScore: '100%',
    name: '3分钟响应率',
    define: '定义说明'
  },
  wwSatisfaction: {
    score: 98.0,
    display: '98.0',
    name: '咨询满意度'
  },
  
  // 物流体验
  lgt48hGotRate: { score: 98.5, display: '98.5', name: '48H揽收率' },
  lgtFulfillRate: { score: 98.5, display: '98.5', name: '履约率' },
  lgtPlanAccRate: { score: 76.5, display: '76.5', name: '物流时效达成率' },
  lgt72hReceiveRate: { score: 65.7, display: '65.7', name: '72H支签率' },
  lgtFulfillDzRate: { score: 100, display: '100', name: '定制品履约率' },
  lgtRfdFhRate: { score: 0, display: '0', name: '物流发货退款率' },
  
  // 品质体验
  qualityRfdRate: { score: 0, display: '0', name: '品质退款率' },
  qualityBadRate: { score: 0, display: '0', name: '商品品质差评率' },
  
  // 新灯塔综合评分
  nlhScore: { score: '3.3', name: '新灯塔分', title: '差', copyWriting: '落后78%同行' },
  qualityScore: { score: '5.0', name: '商品体验', title: '优', proportionSuffix: '15%' },
  refundScore: { score: '1.7', name: '售后体验', title: '差', proportionSuffix: '30%' },
  lgtScore: { score: '2.4', name: '物流体验', title: '差', proportionSuffix: '35%' },
  wwScore: { score: '5.0', name: '咨询体验', title: '优', proportionSuffix: '20%' },
  starScore: { score: '4.0', name: '星级' },
  cateLvl1Name: '宠物及园艺',
  benefitsUnlocked: ['满足金冠品设置门槛'],
  benefitsUnlockedPending: ['获得金冠商品积分']
}
```

## 使用流程

1. **安装插件**：将插件加载到 Chrome 浏览器
2. **访问目标页面**：
   - 打开 `sycm.1688.com` 进入生意参谋
   - 或打开 `work.1688.com` 进入工作台
3. **触发采集**：通过 popup 点击"立即采集当前页"，或通过 API 发送 `TRIGGER_CLAW_CONTENT`
4. **等待数据**：生意参谋页面需等待约 3 秒（多个 API 并行请求）
5. **获取数据**：通过 `OPEN_CLAW_API` 获取已采集的数据

## 注意事项

- 插件依赖页面 Cookie 进行身份验证，需要确保用户已登录 1688
- 工作台采集需要 `_m_h5_tk` Cookie，如未找到则跳过
- 生意参谋的数据采集需要用户已登录生意参谋并有权限访问相关数据
- 数据以 URL 或公司名作为 key 进行去重，同一页面多次采集会更新已有数据

## 文件说明

| 文件 | 说明 |
|-----|------|
| `manifest.json` | 扩展清单，定义权限和内容脚本 |
| `content.js` | 内容脚本，在 1688 页面执行数据采集 |
| `md5.js` | MD5 哈希工具，用于工作台 MTOP 签名 |
| `background.js` | Service Worker，数据存储和 API 接口 |
| `popup.html/js` | 弹出界面，用于手动触发和状态查看 |
