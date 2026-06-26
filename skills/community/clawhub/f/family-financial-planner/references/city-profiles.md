# 城市参数配置文件

本文档提供各城市的社保缴费比例、公积金上限、灵活就业社保费用及生活成本参考基线。
构建仪表盘时根据用户所在城市自动选取对应参数。

> **数据时效**：基于 2025 年度各地人社/税务部门公开信息。每年 7 月调基，
> 如当前日期在 7 月后，建议搜索最新数据更新。

---

## 1. 城市社保参数

### 1.1 在职员工社保（个人部分）

社保个人缴纳比例 = 养老(8%) + 医疗(2%左右) + 失业(0.2~0.5%)，各城市略有差异。

```javascript
const CITY_SSI_PROFILES = {
  // ============ 一线城市 ============
  "北京": {
    ssiBaseLower: 6843,    // 社保基数下限
    ssiBaseUpper: 36927,   // 社保基数上限
    ssiPersonalRate: 0.105, // 个人社保总比例 (8%+2%+0.5%)
    ssiCompanyRate: 0.265,  // 单位社保总比例 (16%+9.8%+0.5%+0.4%)
    hpfRate: 0.12,          // 公积金个人比例
    hpfBaseUpper: 35283,    // 公积金基数上限 (2025年)
    hpfBaseLower: 2420,     // 公积金基数下限
    medicalExtra: 3,        // 大额医疗互助（元/月）
    label: "北京",
  },
  "上海": {
    ssiBaseLower: 7850,
    ssiBaseUpper: 39250,
    ssiPersonalRate: 0.105,  // 8%+2%+0.5%
    ssiCompanyRate: 0.272,   // 16%+10.5%+0.5%+0.16%
    hpfRate: 0.07,           // 上海公积金 7%（大部分企业）
    hpfBaseUpper: 39250,
    hpfBaseLower: 2690,
    medicalExtra: 0,
    label: "上海",
  },
  "广州": {
    ssiBaseLower: 5642,
    ssiBaseUpper: 28210,
    ssiPersonalRate: 0.102,  // 8%+2%+0.2% (失业比例低)
    ssiCompanyRate: 0.208,   // 14%+5.5%+0.32%+0.85%+0.2%
    hpfRate: 0.12,
    hpfBaseUpper: 38082,
    hpfBaseLower: 2300,
    medicalExtra: 0,
    label: "广州",
  },
  "深圳": {
    ssiBaseLower: 2493,
    ssiBaseUpper: 25920,
    ssiPersonalRate: 0.103,  // 8%+2%+0.3%
    ssiCompanyRate: 0.224,   // 15%+6.2%+0.7%+0.5%+0.14%
    hpfRate: 0.05,           // 深圳公积金 5%（部分企业更高）
    hpfBaseUpper: 41190,
    hpfBaseLower: 2360,
    medicalExtra: 0,
    label: "深圳",
    note: "深圳社保基数较低,医疗分一二三档,此处按一档(最高)计算",
  },

  // ============ 新一线城市 ============
  "杭州": {
    ssiBaseLower: 4700,
    ssiBaseUpper: 25200,
    ssiPersonalRate: 0.105,  // 8%+2%+0.5%
    ssiCompanyRate: 0.242,   // 14%+9.5%+0.5%+0.2%
    hpfRate: 0.12,
    hpfBaseUpper: 35550,
    hpfBaseLower: 2280,
    medicalExtra: 4,         // 大病保险约50元/年
    label: "杭州",
  },
  "成都": {
    ssiBaseLower: 4560,
    ssiBaseUpper: 22800,
    ssiPersonalRate: 0.104,  // 8%+2%+0.4%
    ssiCompanyRate: 0.245,   // 16%+7.7%+0.6%+0.2%
    hpfRate: 0.12,
    hpfBaseUpper: 29380,
    hpfBaseLower: 2100,
    medicalExtra: 0,
    label: "成都",
  },
  "南京": {
    ssiBaseLower: 4879,
    ssiBaseUpper: 27216,
    ssiPersonalRate: 0.105,
    ssiCompanyRate: 0.256,
    hpfRate: 0.12,
    hpfBaseUpper: 33600,
    hpfBaseLower: 2280,
    medicalExtra: 10,
    label: "南京",
  },
  "武汉": {
    ssiBaseLower: 4494,
    ssiBaseUpper: 22470,
    ssiPersonalRate: 0.105,
    ssiCompanyRate: 0.25,
    hpfRate: 0.12,
    hpfBaseUpper: 29799,
    hpfBaseLower: 2010,
    medicalExtra: 7,
    label: "武汉",
  },
  "西安": {
    ssiBaseLower: 4281,
    ssiBaseUpper: 21405,
    ssiPersonalRate: 0.105,
    ssiCompanyRate: 0.256,
    hpfRate: 0.12,
    hpfBaseUpper: 28434,
    hpfBaseLower: 2160,
    medicalExtra: 0,
    label: "西安",
  },
  "苏州": {
    ssiBaseLower: 4879,
    ssiBaseUpper: 27216,
    ssiPersonalRate: 0.105,
    ssiCompanyRate: 0.255,
    hpfRate: 0.12,
    hpfBaseUpper: 34900,
    hpfBaseLower: 2280,
    medicalExtra: 5,
    label: "苏州",
  },
  "长沙": {
    ssiBaseLower: 4396,
    ssiBaseUpper: 21978,
    ssiPersonalRate: 0.105,
    ssiCompanyRate: 0.25,
    hpfRate: 0.12,
    hpfBaseUpper: 28236,
    hpfBaseLower: 1930,
    medicalExtra: 0,
    label: "长沙",
  },
  "重庆": {
    ssiBaseLower: 4359,
    ssiBaseUpper: 21793,
    ssiPersonalRate: 0.105,
    ssiCompanyRate: 0.24,
    hpfRate: 0.12,
    hpfBaseUpper: 29320,
    hpfBaseLower: 2100,
    medicalExtra: 5,
    label: "重庆",
  },
};
```

### 1.2 灵活就业社保（辞职后本人/配偶参保）

灵活就业人员只缴养老+医疗，无失业/工伤/生育。
缴费基数可选（通常在 60%~300% 社平工资之间），以下按最低基数估算月缴金额。

```javascript
const CITY_FLEX_SOCIAL = {
  // 格式: { pension: 养老月缴, medical: 医疗月缴, total: 合计 }
  // 均按最低基数（60%档）估算
  "北京": { pension: 1096, medical: 580, total: 1676, note: "养老20%×6843=1369,实际可选更低档" },
  "上海": { pension: 1256, medical: 792, total: 2048, note: "灵活就业养老20%×7850,医疗11.5%+3元" },
  "广州": { pension: 904,  medical: 418, total: 1322, note: "养老20%×5642,医疗含大病" },
  "深圳": { pension: 499,  medical: 452, total:  951, note: "深户养老最低基数低,非深户参照户籍地" },
  "杭州": { pension: 752,  medical: 434, total: 1186, note: "养老20%×4700,医疗含大病" },
  "成都": { pension: 730,  medical: 396, total: 1126, note: "养老20%×4560,医疗8.5%" },
  "南京": { pension: 781,  medical: 397, total: 1178, note: "养老20%×4879" },
  "武汉": { pension: 719,  medical: 360, total: 1079, note: "养老20%×4494" },
  "西安": { pension: 685,  medical: 343, total: 1028, note: "养老20%×4281" },
  "苏州": { pension: 781,  medical: 390, total: 1171, note: "养老20%×4879" },
  "长沙": { pension: 703,  medical: 352, total: 1055, note: "养老20%×4396" },
  "重庆": { pension: 697,  medical: 340, total: 1037, note: "养老20%×4359" },
};
```

---

## 2. 生活成本参考基线

以下数据为各城市三口之家（2 大人 + 1 幼儿）每月典型支出参考。
**这是参考起点**，实际建模时应根据用户的具体生活方式调整。

```javascript
const CITY_LIVING_COST = {
  // 格式: { rent, food, baby, utility, misc, nanny, car, insurance, total }
  // 单位: 元/月   
  // rent = 自住不填(0)，租房按中等地段两居室
  // car = 车险月均 + 油费/充电（无车则 0）
  // nanny = 住家保姆/育儿嫂 (可选)

  "北京": {
    rent: 0,         // 自住房默认 0（有房贷在贷款里算）
    food: 4000,      // 三口之家 + 偶尔外食
    baby: 3000,      // 奶粉/纸尿裤/儿童用品/医疗
    utility: 2000,   // 水电燃气物业网络话费
    misc: 2000,      // 服装/社交/日杂
    nanny: 6500,     // 育儿嫂（住家）
    car: 2300,       // 保险800 + 油费1500
    insurance: 1700, // 年缴2万/12
    total: 21500,
    inflationRate: 0.035, // 北京通胀较高
    label: "北京（一线）",
  },
  "上海": {
    rent: 0,
    food: 4200,
    baby: 3200,
    utility: 2100,
    misc: 2200,
    nanny: 7000,
    car: 2100,
    insurance: 1700,
    total: 22500,
    inflationRate: 0.035,
    label: "上海（一线）",
  },
  "广州": {
    rent: 0,
    food: 3500,
    baby: 2500,
    utility: 1800,
    misc: 1800,
    nanny: 5500,
    car: 2000,
    insurance: 1500,
    total: 18600,
    inflationRate: 0.03,
    label: "广州（一线）",
  },
  "深圳": {
    rent: 0,
    food: 3800,
    baby: 2800,
    utility: 1900,
    misc: 2000,
    nanny: 6000,
    car: 2000,
    insurance: 1600,
    total: 20100,
    inflationRate: 0.035,
    label: "深圳（一线）",
  },
  "杭州": {
    rent: 0,
    food: 3500,
    baby: 2500,
    utility: 1700,
    misc: 1800,
    nanny: 5500,
    car: 1800,
    insurance: 1500,
    total: 18300,
    inflationRate: 0.03,
    label: "杭州（新一线）",
  },
  "成都": {
    rent: 0,
    food: 3000,
    baby: 2200,
    utility: 1500,
    misc: 1500,
    nanny: 4500,
    car: 1600,
    insurance: 1200,
    total: 15500,
    inflationRate: 0.025,
    label: "成都（新一线）",
  },
  "南京": {
    rent: 0,
    food: 3500,
    baby: 2500,
    utility: 1700,
    misc: 1800,
    nanny: 5500,
    car: 1800,
    insurance: 1500,
    total: 18300,
    inflationRate: 0.03,
    label: "南京（新一线）",
  },
  "武汉": {
    rent: 0,
    food: 3000,
    baby: 2200,
    utility: 1500,
    misc: 1500,
    nanny: 4500,
    car: 1600,
    insurance: 1200,
    total: 15500,
    inflationRate: 0.025,
    label: "武汉（新一线）",
  },
  "西安": {
    rent: 0,
    food: 2800,
    baby: 2000,
    utility: 1400,
    misc: 1500,
    nanny: 4000,
    car: 1500,
    insurance: 1000,
    total: 14200,
    inflationRate: 0.025,
    label: "西安（新一线）",
  },
  "长沙": {
    rent: 0,
    food: 2800,
    baby: 2000,
    utility: 1300,
    misc: 1400,
    nanny: 4200,
    car: 1500,
    insurance: 1000,
    total: 14200,
    inflationRate: 0.025,
    label: "长沙（新一线）",
  },
  "重庆": {
    rent: 0,
    food: 2800,
    baby: 2000,
    utility: 1300,
    misc: 1400,
    nanny: 4000,
    car: 1500,
    insurance: 1000,
    total: 14000,
    inflationRate: 0.025,
    label: "重庆（新一线）",
  },
};
```

---

## 3. 个税计算的城市差异

个税七级累进税率全国统一，但以下参数各城市不同：

| 参数 | 说明 | 影响 |
|------|------|------|
| 社保个人比例 | 各城市 10.2%~10.5% | 影响应税收入 |
| 公积金比例 | 5%~12% | 影响应税收入 |
| 公积金基数上限 | 2.2万~3.9万 | 高薪人群影响大 |
| 专项附加扣除 | 全国统一 | 子女教育1000/房贷1000/赡养2000等 |

### reverseGrossSalary 城市适配

```javascript
function reverseGrossSalary(netTarget, city) {
  const profile = CITY_SSI_PROFILES[city] || CITY_SSI_PROFILES["北京"];
  let gross = netTarget * 1.4;
  for (let iter = 0; iter < 50; iter++) {
    // 社保 = 基数(取上下限) × 个人比例
    const ssiBase = Math.max(profile.ssiBaseLower, Math.min(gross, profile.ssiBaseUpper));
    const ssi = ssiBase * profile.ssiPersonalRate;
    // 公积金 = 基数(取上限) × 比例
    const hpfBase = Math.max(profile.hpfBaseLower, Math.min(gross, profile.hpfBaseUpper));
    const hpf = hpfBase * profile.hpfRate;
    // 个税（年度累进制）
    const taxable = gross - ssi - hpf - 5000 - (profile.medicalExtra || 0);
    let tax = 0;
    if (taxable > 0) {
      const annual = taxable * 12;
      if (annual <= 36000)        tax = annual * 0.03;
      else if (annual <= 144000)  tax = annual * 0.10 - 2520;
      else if (annual <= 300000)  tax = annual * 0.20 - 16920;
      else if (annual <= 420000)  tax = annual * 0.25 - 31920;
      else if (annual <= 660000)  tax = annual * 0.30 - 52920;
      else if (annual <= 960000)  tax = annual * 0.35 - 85920;
      else                        tax = annual * 0.45 - 181920;
      tax = tax / 12;
    }
    const net = gross - ssi - hpf - Math.max(0, tax) - (profile.medicalExtra || 0);
    const diff = net - netTarget;
    if (Math.abs(diff) < 10) break;
    gross -= diff * 0.7;
  }
  return Math.round(gross);
}
```

---

## 4. 使用指南

### 4.1 在 Phase 1 信息采集时

问用户：**"你在哪个城市生活/工作？"** 

根据回答匹配城市参数。如果用户所在城市不在预设列表中，使用最接近的城市参数或让 AI 搜索该城市最新社保数据。

### 4.2 在 Phase 2 建模时

```javascript
// 示例：根据城市初始化参数
const CITY = "杭州";
const citySSI = CITY_SSI_PROFILES[CITY];
const cityFlex = CITY_FLEX_SOCIAL[CITY];
const cityLiving = CITY_LIVING_COST[CITY];

// 灵活就业社保作为辞职后的支出项
const SPOUSE_SOCIAL = cityFlex.total;  // 或只算 pension 不交医保

// 通胀率使用城市特定值
const INFLATION_RATE = cityLiving.inflationRate;

// 反推税前工资时使用城市参数
const targetGross = reverseGrossSalary(targetNet, CITY);
```

### 4.3 城市对比功能（可选）

如果用户考虑换城市（如"从北京搬到成都"），可以生成城市对比分析 Tab：

- 生活成本对比（柱状图）
- 社保缴费对比
- 同样的资产在两个城市分别能撑多久
- 回去上班需要的薪资差异

---

## 5. 数据更新提示

每年 7 月各城市调整社保基数。当你使用此 skill 时：
1. 检查当前日期
2. 如果在每年 7 月后，建议搜索 "XX城市 {年份}年 社保缴费基数" 获取最新数据
3. 公积金基数通常每年 7 月 1 日更新
4. 灵活就业社保费用随基数同步调整
