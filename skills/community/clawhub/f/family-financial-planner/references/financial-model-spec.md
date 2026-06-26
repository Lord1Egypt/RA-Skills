# 家庭财务全景分析 — 计算模型规范

本文档定义了仪表盘中所有财务计算的公式、逻辑和边界条件。
实现时以 JavaScript 内联在 HTML `<script>` 中，所有数值由常量派生，修改一处全局联动。

---

## 1. 数据结构 — 用户输入常量

### 1.1 资产类

```javascript
// 汇率（如有港币/美元资产）
const FX_RATE = __FX_RATE__;  // 例: 0.881 (1 HKD = 0.881 CNY)

// 股票/证券
const stockAccounts = [
  { name: '__NAME__', valueInOrigCurrency: __VALUE__, currency: 'HKD' },
  // ... 可多个账户
];
const totalStockCNY = stockAccounts.reduce((s, a) => s + a.valueInOrigCurrency * (a.currency === 'CNY' ? 1 : FX_RATE), 0);

// 未归属股权激励（RSU/Option）— 如用户有
const futureEquity = [
  { date: '__DATE__', shares: __N__, pricePerShare: __PRICE__, currency: 'HKD', label: '__LABEL__' },
];

// 房产
const properties = [
  { name: '自住房', value: __WAN__, mortgageRemain: __WAN__, monthlyPayment: __YUAN__, rate: __PCT__, isSelfUse: true, monthlyRent: 0 },
  { name: '投资房', value: __WAN__, mortgageRemain: 0, monthlyPayment: 0, rate: 0, isSelfUse: false, monthlyRent: __YUAN__ },
];

// 车辆
const carValue = __WAN__;

// 现金
const cashSaving = __WAN__;

// 负债
const loans = [
  { name: '商业贷款', remain: __WAN__, monthlyPayment: __YUAN__, rate: __PCT__, totalMonths: 360, paidMonths: __N__ },
  { name: '公积金贷款', remain: __WAN__, monthlyPayment: __YUAN__, rate: __PCT__, totalMonths: 360, paidMonths: __N__, minPayment: __YUAN__ },
  { name: '无息贷款（触发条件还款）', remain: __WAN__, monthlyPayment: 0, rate: 0, mustRepayOnQuit: true, note: '亲友借款/购房垫资/消费分期等，满足条件时需一次性归还' },
];
```

### 1.2 收支类

```javascript
// 工资（在职时）
const salary = {
  gross: __YUAN__,      // 税前
  ssi: __YUAN__,        // 社保个人
  hpf: __YUAN__,        // 公积金个人
  tax: __YUAN__,        // 个税
  net: __YUAN__,        // 到手
  companyHPF: __YUAN__, // 公司缴公积金
};

// 被动收入
const monthlyRentIncome = properties.filter(p => !p.isSelfUse).reduce((s, p) => s + p.monthlyRent, 0);

// 家庭生活支出项
const livingExpenses = {
  nanny: __YUAN__,       // 保姆/育儿嫂（可为 0）
  food: __YUAN__,        // 伙食
  baby: __YUAN__,        // 宝宝用品（可为 0）
  education: __YUAN__,   // 教育
  utility: __YUAN__,     // 水电物业网络话费
  misc: __YUAN__,        // 其他杂项
  insurance: __YUAN__,   // 家庭保险月均
  carCost: __YUAN__,     // 车辆保险+油费
  spouseSocial: __YUAN__,// 配偶灵活社保（可为 0）
};

// 创业/项目运营成本（可选模块）
const bizCost = {
  socialInsurance: __YUAN__, // 公司缴社保
  bookkeeping: __YUAN__,    // 记账报税
  cloudAndTools: __YUAN__,  // 云服务/SaaS/API
  misc: __YUAN__,           // 域名等杂费
};

// 系统参数
const INFLATION_RATE = __RATE__;     // 默认 0.035
const EMERGENCY_MONTHS = __N__;      // 默认 8（有小孩）或 6
const INVEST_RETURN = __RATE__;      // 默认 0.025
```

---

## 2. 核心计算模块

### 2.1 资产负债净值

```
totalAsset = Σ properties[i].value + totalStockWan + cashSaving + carValue
totalDebt  = Σ loans[i].remain
netWorth   = totalAsset - totalDebt
debtRatio  = totalDebt / totalAsset × 100%
liquidAsset = totalStockWan + cashSaving  // 可快速变现的
```

**判定标准**：
- 资产负债率 ≤ 40%：健康
- 40% < 资产负债率 ≤ 60%：需关注
- > 60%：偏高

### 2.2 月度收支模型

**在职时**：
```
onJobIncome    = salary.net + monthlyRentIncome
onJobExpense   = 商贷月供 + 家庭生活总支出 + 保险 + 车费
                 （公积金贷款由公积金账户扣，不计入自付）
onJobSaving    = onJobIncome - onJobExpense
```

**离职后**：
```
quitExpense = Σ loans[i].monthlyPayment  // 所有贷款（含公积金自付）
            + Σ livingExpenses
            + Σ bizCost                   // 如有创业
quitIncome  = monthlyRentIncome           // 仅被动收入
quitDeficit = quitExpense - quitIncome
```

### 2.3 通胀调整的 N 年支出时间线

```javascript
// 基准年数据
const yearPlanBase = [
  { year: 1, nanny: X, food: X, baby: X, education: X, ... },
  { year: 2, ... },
  // ... 最多 5 年
];

// 通胀修正
const yearPlan = yearPlanBase.map((base, idx) => {
  const inflator = Math.pow(1 + INFLATION_RATE, idx); // 第1年=1, 第2年=1.035...
  // 所有支出项乘以 inflator
  const adjusted = {};
  for (const key of expenseKeys) {
    adjusted[key] = Math.round(base[key] * inflator);
  }
  adjusted.monthlyFamily = Σ adjusted[expenseKeys];
  adjusted.monthlyDeficit = adjusted.monthlyFamily + adjusted.carCost + totalMonthlyLoans + bizMonthlyCost - monthlyRentIncome;
  return adjusted;
});
```

**关键点**：
- 通胀按复利逐年累计，不是每年加固定额
- 保姆→幼儿园的结构性变化先在基准数据中体现，通胀再叠加
- 教育支出随年龄非线性增长（幼儿园、兴趣班等）

### 2.4 两种场景对比

设用户有"立即行动"（Scenario A）和"延期行动"（Scenario B）两个时间点：

**Scenario A — 立即行动**：
```
liquidAfterLoan_A = liquidAsset - mustRepayLoans  // mustRepayLoans = 所有 mustRepayOnQuit=true 的贷款余额之和（含亲友借款、垫资等）
emergency_A       = quitExpense × EMERGENCY_MONTHS / 10000
deployable_A      = liquidAfterLoan_A - emergency_A
survivalMonths_A  = floor(deployable_A × 10000 / quitDeficit)
```

**Scenario B — 延期行动**（多等 M 个月）：
```
extraSavings      = onJobSaving × M / 10000
extraEquity       = futureEquityAfterTax / 10000  // 如有 RSU
liquidAsset_B     = liquidAsset + extraSavings + extraEquity
liquidAfterLoan_B = liquidAsset_B - mustRepayLoans
deployable_B      = liquidAfterLoan_B - emergency_A  // 备用金标准相同
survivalMonths_B  = floor(deployable_B × 10000 / quitDeficit)
```

### 2.5 等额本息贷款摊销

```javascript
function calcAmortization(principal, annualRate, totalMonths, paidMonths) {
  const r = annualRate / 100 / 12;
  const monthlyPayment = principal * r * Math.pow(1+r, totalMonths) / (Math.pow(1+r, totalMonths) - 1);
  
  let balance = principal;
  let totalInterestPaid = 0, totalPrincipalPaid = 0;
  
  for (let m = 1; m <= totalMonths; m++) {
    const interest = balance * r;
    const principalPart = monthlyPayment - interest;
    balance -= principalPart;
    if (m <= paidMonths) {
      totalInterestPaid += interest;
      totalPrincipalPaid += principalPart;
    }
  }
  
  return {
    monthlyPayment,
    totalPayment: monthlyPayment * totalMonths,
    totalInterest: monthlyPayment * totalMonths - principal,
    remainingPrincipal: principal - totalPrincipalPaid,
  };
}
```

### 2.6 动态生存模拟（含投资回报 + 通胀）

比静态计算更精确——每个月计算投资收益，支出按通胀逐年递增：

```javascript
function calcRealSurvival(monthlyExtraIncome = 0) {
  let asset = deployable * 10000;
  for (let m = 1; m <= 120; m++) {
    // 每月投资回报
    asset += asset * (INVEST_RETURN / 12);
    // 当年支出（按通胀后数据）
    const yearIdx = Math.min(Math.floor((m-1) / 12), yearPlan.length - 1);
    const deficit = yearPlan[yearIdx].monthlyDeficit - monthlyExtraIncome;
    asset -= deficit;
    if (asset <= 0) return m;
  }
  return Infinity; // 超过10年，财务可持续
}
```

### 2.7 反推税前工资（中国个税七级累进）

给定目标到手月薪，反推需要的税前工资。**需要根据城市参数调整社保/公积金比例**。

详见 `city-profiles.md` 中的 `reverseGrossSalary(netTarget, city)` 函数。

核心逻辑：
```javascript
function reverseGrossSalary(netTarget, city) {
  const profile = CITY_SSI_PROFILES[city]; // 从 city-profiles.md 加载
  let gross = netTarget * 1.4; // 初始猜测
  for (let iter = 0; iter < 50; iter++) {
    // 社保 = 基数(取上下限) × 个人比例（各城市不同）
    const ssiBase = Math.max(profile.ssiBaseLower, Math.min(gross, profile.ssiBaseUpper));
    const ssi = ssiBase * profile.ssiPersonalRate;
    // 公积金 = 基数(取上限) × 比例（各城市不同，5%~12%）
    const hpfBase = Math.max(profile.hpfBaseLower, Math.min(gross, profile.hpfBaseUpper));
    const hpf = hpfBase * profile.hpfRate;
    const taxable = gross - ssi - hpf - 5000;
    let tax = 0;
    if (taxable > 0) {
      const annual = taxable * 12;
      if (annual <= 36000) tax = annual * 0.03;
      else if (annual <= 144000) tax = annual * 0.10 - 2520;
      else if (annual <= 300000) tax = annual * 0.20 - 16920;
      else if (annual <= 420000) tax = annual * 0.25 - 31920;
      else if (annual <= 660000) tax = annual * 0.30 - 52920;
      else if (annual <= 960000) tax = annual * 0.35 - 85920;
      else tax = annual * 0.45 - 181920;
      tax = tax / 12;
    }
    const net = gross - ssi - hpf - Math.max(0, tax);
    const diff = net - netTarget;
    if (Math.abs(diff) < 10) break;
    gross -= diff * 0.7; // 阻尼收敛
  }
  return Math.round(gross);
}
```

**注意**：
- 社保基数有上限和下限，各城市不同 → 详见 `city-profiles.md`
- 公积金缴存基数上限各城市不同 → 详见 `city-profiles.md`
- 简化处理不含专项附加扣除（子女教育、住房贷款等，用户可自行调整）

### 2.8 止损线计算

```
jobSearchMonths = 4  // 平均找工作时间
stopLossAsset = quitDeficit × (EMERGENCY_MONTHS + jobSearchMonths) / 10000
```

**含义**：当资产降到此值时，必须立刻开始找工作，预留求职期间的生活费 + 紧急备用金。

### 2.9 职场空窗折损模型

| 空窗时间 | 薪资折损 | 求职难度 | 说明 |
|----------|----------|----------|------|
| ≤ 1 年 | 0-5% | 低 | 可解释为"创业尝试/深造"，技术栈未过时 |
| 1-2 年 | 5-15% | 中 | 需证明期间保持学习，可能需刷题 |
| 2-3 年 | 10-25% | 中高 | 技术迭代快的行业部分技能已过时 |
| 3-5 年 | 20-40% | 高 | 年龄+空窗双重压力，可能需降级或转方向 |

折损比例因行业而异——互联网/AI 更高，传统行业/公务员更低。

---

## 3. Tab 模块清单

根据用户具体情况，从以下 Tab 中选取适用的：

| Tab | 名称 | 内容 | 何时包含 |
|-----|------|------|----------|
| 0 | 资产总览 | 净值、资产负债率、资产/负债构成表 | **必须** |
| 1 | 股票 & RSU | 持仓明细、未归属 RSU、税务分析 | 有股票/RSU 时 |
| 2 | 房产 & 贷款 | 房产净值、贷款明细、离职后公积金影响 | 有房产贷款时 |
| 3 | 房贷成本 | 30 年总利息、逐年本息比、提前还贷分析 | 有房贷时 |
| 4 | 月度收支 | 在职 vs 离职收支对比、公积金优化 | **必须** |
| 5 | 辞职对比 | 两种场景全景对比、资产分层、OPC 收入情景 | 有两个场景时 |
| 6 | 行动清单 | 时间排序的待办事项 | **必须** |
| 7 | 家庭支出 | 5 年支出时间线、堆叠柱状图、饼图 | 有小孩/支出变化时 |
| 8 | 创业分析 | 运营成本拆解、盈亏平衡、资产消耗曲线 | 有创业计划时 |
| 9 | 提前还贷 | 提前还贷 vs 投资对比、净现值分析 | 有房贷时 |
| 10 | 盲区修正 | 通胀侵蚀、修正前后对比、动态生存模拟 | **建议** |
| 11 | 回归职场 | 最低/舒适/宽裕薪资、反推税前、止损线 | 有创业/离职场景时 |

---

## 4. 格式化辅助函数

```javascript
function fmt(n)   { return n.toLocaleString('zh-CN', {maximumFractionDigits:1}); }
function fmtY(n)  { return '¥' + n.toLocaleString('zh-CN', {maximumFractionDigits:0}); }
function fmtHK(n) { return 'HK$' + n.toLocaleString('zh-CN', {maximumFractionDigits:0}); }
function fmtPct(n){ return n.toFixed(1) + '%'; }
function fmtWan(n){ return fmt(n) + '万'; }
```

---

## 5. 给家人看的通俗总结模板

在所有计算完成后，生成一段 500 字以内的通俗总结。语气温暖、体贴、有底气，避免冷冰冰的数字罗列。
核心信息点：
1. 为什么做这个决定（家庭优先，不是逃避工作）
2. 钱够花多久（月数→年数）
3. 每月花多少、主要花在哪
4. 如果不成功，回去上班需要多少工资
5. 安全底线在哪（止损资产额）
6. 最关键的一个建议（如"一定要等到 X 月再辞"）
