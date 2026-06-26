---
name: dealpilot
slug: dealpilot
version: 0.1.0
description: |
  Cross-Platform Shopping Decision Agent / 全网购物决策官.
  Compares prices, quality, and risk across 淘宝/拼多多/京东/一号店/唯品会
  and recommends the best platform for a given product and context.
---

# DealPilot / 全网购物决策官

你是**全网购物决策官**。

你的任务不是罗列商品参数，而是在用户给出购物需求后，**帮他在多个平台中找到最优解**，
并给出可执行的购买建议。

## 产品定位

DealPilot 是一个跨平台购物比价决策引擎，覆盖：淘宝、拼多多、京东、一号店、唯品会。

核心价值：
- **跨平台比价**：同商品多平台实时价格对比
- **风险评估**：卖家信誉、售后保障、假货风险
- **时机判断**：当前是否是最佳购买时机
- **推荐收敛**：给出明确平台建议和理由

## 使用场景

用户可能会说：
- "帮我看看这个产品在哪个平台买最划算"
- "对比一下京东和拼多多买这个"
- "我想买 X，百元以内，哪个平台靠谱"
- "这个价格是不是好价，要不要等"
- "淘宝和唯品会哪个更靠谱"

## 输入 schema（统一需求格式）

```typescript
interface ShoppingRequest {
  // 商品信息
  product?: string;          // 商品名称/关键词
  productUrl?: string;       // 商品链接（可多平台）
  category?: string;         // 品类

  // 用户偏好
  budget?: PriceRange;       // 预算范围
  priorities?: string[];     // 优先级：["价格", "品质", "速度", "售后"]
  quantity?: number;         // 购买数量

  // 场景
  scenario?: "personal" | "gift" | "resale";  // 自用/送礼/转卖
  urgency?: "low" | "medium" | "high";        // 紧急程度

  // 平台范围（默认全部）
  platforms?: Platform[];

  // 约束
  mustHave?: string[];      // 必须有的特性/服务
  mustAvoid?: string[];     // 必须避免的
}

type Platform = "taobao" | "pdd" | "jd" | "yhd" | "vip";
type PriceRange = { min?: number; max?: number; };
```

## 输出 schema（统一决策报告）

```typescript
interface DecisionReport {
  // 推荐决策
  recommendedPlatform: Platform;
  recommendedUrl?: string;
  recommendedPrice?: number;

  // 决策理由
  reasons: string[];           // 为什么要选这个平台

  // 风险提示
  risks: RiskItem[];          // 当前方案的风险点

  // 替代方案
  alternatives: AltPlatform[]; // 其他可选平台，排序

  // 时机建议
  timingAdvice: TimingAdvice;

  // 对比摘要（表格）
  comparison: PlatformSummary[];

  // 最终结论（可执行）
  conclusion: string;
}

interface RiskItem {
  level: "low" | "medium" | "high";
  description: string;
  mitigation?: string;  // 如何降低风险
}

interface AltPlatform {
  platform: Platform;
  score: number;        // 0-100
  price?: number;
  keyReason: string;
}

interface TimingAdvice {
  verdict: "buy_now" | "wait" | "compare_first";
  reason: string;
  waitDays?: number;    // 建议等多少天
  betterPeriod?: string; // "618", "双十一" 等
}

interface PlatformSummary {
  platform: Platform;
  price?: number;
  quality: "low" | "medium" | "high";
  shipping: "slow" | "medium" | "fast";
  afterSales: "weak" | "medium" | "strong";
  authenticity: "risky" | "medium" | "safe";
  score: number;
}
```

## 决策引擎流程

```
用户需求输入
    ↓
[需求解析] → 识别商品、预算、偏好、场景
    ↓
[平台搜索] → 各平台并行搜索（stub 阶段返回 mock 数据）
    ↓
[价格抓取] → 提取各平台到手价（含优惠/拼团等）
    ↓
[质量评估] → 店铺信誉、评论、售后标识
    ↓
[风险评分] → 假货/售后/物流风险量化
    ↓
[决策推荐] → 综合评分 + 时机判断
    ↓
[报告生成] → DecisionReport 输出
```

## 平台适配层

每个平台适配器需实现以下接口：

```typescript
interface PlatformAdapter {
  platform: Platform;
  
  // 搜索商品
  search(query: string, options?: SearchOptions): Promise<SearchResult[]>;

  // 获取商品详情
  getProductDetail(url: string): Promise<ProductInfo>;

  // 计算最终到手价（含优惠/拼团/百亿补贴等）
  calcFinalPrice(product: ProductInfo): Promise<FinalPrice>;

  // 评估店铺/卖家风险
  assessSeller(url: string): Promise<SellerRisk>;

  // 平台特性判断
  getPlatformTraits(): PlatformTraits;
}

interface SearchOptions {
  category?: string;
  minPrice?: number;
  maxPrice?: number;
  sortBy?: "price" | "sales" | "rating";
}

interface FinalPrice {
  rawPrice: number;
  finalPrice: number;
  discountDesc: string[];   // ["百亿补贴-100", "拼团-30"]
  isSubsidized: boolean;    // 是否官方补贴
}

interface PlatformTraits {
  strength: string[];      // ["价格最低", "自营可信"]
  weakness: string[];       // ["物流较慢", "退换麻烦"]
  bestFor: string[];       // ["标准品", "电子产品"]
  worstFor: string[];       // ["生鲜", "奢侈品"]
}
```

## 平台优先级参考

| 维度 | 淘宝 | 拼多多 | 京东 | 一号店 | 唯品会 |
|------|------|--------|------|--------|--------|
| 价格 | 中 | 最低 | 高 | 中低 | 中 |
| 品质 | 中 | 偏低 | 高 | 中 | 中 |
| 物流 | 中 | 慢 | 最快 | 快 | 中 |
| 售后 | 中 | 弱 | 强 | 中 | 中 |
| 正品 | 中 | 风险高 | 最安全 | 中 | 中 |

## 当前状态

- **搜索/比价**：stub（返回 mock 数据）
- **价格抓取**：stub
- **店铺评估**：stub
- **决策推荐**：stub（固定返回 mock 推荐）
- **时机判断**：stub

下一步由平台组接入真实适配器。

## 相关 Skill

- `taobao` - 淘宝平台适配
- `pdd-shopping` - 拼多多平台适配
- `jingdong` - 京东平台适配
- `shopping-advisor` - 单商品决策逻辑

## 当前状态 (v0.1.0)
## 当前状态 (v0.1.0)

**MVP 骨架版本** - 平台适配器为 stub 实现，返回 mock 数据。

### 已实现
- ✅ 输入/输出 schema 定义
- ✅ 决策引擎流程定义
- ✅ 平台适配器接口定义
- ✅ Mock 决策输出
- ✅ 自测脚本 (`scripts/test-stub.js`)

### 待实现
- 🔄 各平台真实搜索/价格抓取
- 🔄 真实店铺风险评估
- 🔄 实时价格/优惠信息
- 🔄 接入现有平台 skill (taobao, pdd-shopping, jingdong)

## 使用说明

### 本地测试
```bash
cd /Users/jianghaidong/.openclaw/skills/dealpilot
node scripts/test-stub.js
```

### 在 OpenClaw 中调用
```javascript
// 示例：调用 dealpilot 进行决策
const { normalizeRequest } = require('./scripts/normalize.js');
const { decide } = require('./scripts/decide.js');
const { formatReport } = require('./scripts/analyze.js');

async function runDealPilot(product, budget) {
  const request = normalizeRequest({ product, budget });
  const report = await decide(request);
  return formatReport(report);
}

// 示例调用
runDealPilot("蓝牙耳机", { max: 200 }).then(console.log);
```

### 平台适配器状态
| 平台 | 适配器 | 状态 | 备注 |
|------|--------|------|------|
| 淘宝 | `TaobaoAdapter` | stub | 待接入 `taobao` skill |
| 拼多多 | `PddAdapter` | stub | 待接入 `pdd-shopping` skill |
| 京东 | `JdAdapter` | stub | 待接入 `jingdong` skill |
| 一号店 | `YhdAdapter` | stub | 待接入 `yhd` skill |
| 唯品会 | `VipAdapter` | stub | 待接入 `vip` skill |

## 开发指南

### 目录结构
```
dealpilot/
├── SKILL.md                 # 技能定义
├── clawhub.json            # 技能元数据
├── package.json            # 依赖配置
├── README.md               # 项目说明
├── engine/                 # 决策引擎
│   ├── router.ts          # 路由层（决策入口）
│   └── types.ts           # 类型定义
├── platforms/              # 平台适配器
│   ├── base.ts            # 适配器基类
│   ├── taobao.ts          # 淘宝适配器
│   ├── pdd.ts             # 拼多多适配器
│   ├── jd.ts              # 京东适配器
│   ├── yhd.ts             # 一号店适配器
│   └── vip.ts             # 唯品会适配器
└── scripts/               # 工具脚本
    ├── normalize.js       # 需求解析
    ├── decide.js          # 决策调用
    ├── analyze.js         # 报告格式化
    └── test-stub.js       # 自测脚本
```

### 下一步开发
1. **接入真实平台数据** - 将各平台适配器的 stub 方法替换为真实 API 调用
2. **价格抓取** - 实现各平台实时价格获取
3. **风险评估** - 接入店铺信誉、评论分析
4. **时机判断** - 结合促销日历、历史价格
5. **集成测试** - 端到端测试真实商品决策

## 相关 Skill
- `taobao` - 淘宝平台搜索与详情
- `pdd-shopping` - 拼多多百亿补贴/拼团策略
- `jingdong` - 京东自营/物流分析
- `shopping-advisor` - 单商品深度分析