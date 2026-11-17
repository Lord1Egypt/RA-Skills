# 投标报价策略沙盘 · 报价评分公式知识库（formula-kb）

> 本文件是 `bid-pricing-strategy-sandbox` 的内嵌公式知识库。**不依赖任何外部文件**。
> Agent 解析招标/采购文件中的报价评分规则时，必须先把规则归入以下 **10 种方法（M1–M10）** 之一，再逐一确认参数变体。
> 这 10 种方法**已内置进 `calculator.html` 引擎**；本文档示例说明各方法的数学与参数，供 AI 生成**配置（methodId + params）**时参照。用户不再需要持有或编写 `rule.js`。

---

## 0. 引擎契约速查（内部实现，AI 生成配置时无需改写，仅供理解）

`calculator.html` 内置引擎按以下契约把**配置**换算为得分；AI 只需产出符合第二节的配置 JSON，无需改动引擎：

- **全局 `RULE` 对象**（外壳初始化用）：
  ```javascript
  var RULE = {
      priceDimensions: [{ key: "price", label: "投标总价", maxScore: 40 }], // maxScore = 该维度满分(=价格权值)
      defaultUnit: "万元",          // "万元" | "元"
      defaultUnitCount: 6,
      description: "评标办法原文摘要…"
  };
  ```
- **入参 `bids`**：`bids.names: string[]`，`bids.prices: number[][]`（`prices[维度索引][投标人索引]`）。
- **返回对象**（缺任一字段外壳渲染异常 / 显示 `NaN`）：
  ```javascript
  {
      results: [                  // 必须按 score 降序；每项 {name, prices:[各维度报价], score:总得分, rank}
          { name: "单位A", prices: [100], score: 38.5, rank: 1 }
      ],
      benchmarkInfos: [          // 每维度一个 {label, value, desc}
          { label: "评标基准价", value: 95.0, desc: "计算方法简述" }
      ],
      detailScores: [[38.5, 35.2]],   // [维度][投标人] 各维度得分，须与 results 顺序一致
      deviations: [[5.26, -3.12]],    // [维度][投标人] 偏差率(%)，须与 results 顺序一致
      recommendedPrice: [95.0],       // [维度] 推荐报价（策略建议的落点）
      recommendedTotal: 95.0,         // number 推荐总价
      recommendationReason: "策略说明…" // string；策略建议(generateAdvice)内容写这里
  }
  ```
- **重排铁律**：计算完得分后，按 `score` 降序排序 `results`，并同步用 `_orig` 索引重排 `detailScores`/`deviations`，再删除 `_orig`。

---

## 1. 方法枚举（解析时必须归入之一）

| ID | 方法名 | 公式核心 | 典型场景 | 体系 |
|:---|:---|:---|:---|:---|
| M1 | 低价优先法（政采法定） | 得分=(评标基准价/报价)×价格权值×100；基准价=最低报价 | 政府采购货物/服务招标（87号令第55条**强制**） | 政采 |
| M2 | 基准价法-均值 | 基准价=有效报价算术平均×(1-K)；偏离基准价按比例扣分 | 工程招标综合评估法 | 招投标 |
| M3 | 基准价法-去极值 | 去掉最高/最低各 n 家→均值×(1-K) | 工程（投标人≥5/≥7家） | 招投标 |
| M4 | 复合基准价 | 基准价=A×α+B×(1-α)；A=有效均值，B=控制价/最低/最高 | 大型工程 | 招投标 |
| M5 | 反比法 | 得分=最低报价/报价×权重×100 | 通信/IT | 招投标 |
| M6 | 直线内插法 | 分段线性：[0,a]→[满分,x分]，[a,b]→[x分,0分] | 通信 | 招投标 |
| M7 | λ值法 | 得分=满分×(1-λ×偏离率) | 通信/设备 | 招投标 |
| M8 | 分段扣分法 | 0–5%扣X，5–10%扣Y，>10%扣Z（可不对称） | 工程/服务 | 招投标 |
| M9 | 合理低价法 | 低于成本→否决；其余按 M1/M2 计分 | 经评审的最低投标价法 | 招投标/政采 |
| M10 | 多价格维度 | 总价×W1+分项1×W2+分项2×W3…（各维度独立计分后加权求和） | 设备/集成 | 通用 |

---

## 2. 参数变体（解析时必须逐一确认，消歧）

| 参数 | 常见变体 | 歧义点（须向用户确认） |
|:---|:---|:---|
| 基准价基数 | 均值 / 去极值均值 / 最低 / 最高 / 控制价 / 复合 | "评标价"是否含暂列金额、暂估价？ |
| 去极值规则 | 不去 / 去各1家 / 去各2家（≥7家时） | "投标人≥7家"是含还是不含？ |
| K值/系数 | 固定值 / 随机抽取（候选集）/ 区间 | K 是乘 (1-K) 还是直接乘 K？ |
| 满分条件 | 报价=基准价 / 报价≤基准价 / 报价=最低价 | "等于"是否含四舍五入后等于？ |
| 高于基准价 | 每高1%扣X（线性）/ 阶梯 / 固定 | 步长是 1% 还是 0.5% 还是连续？ |
| 低于基准价 | 每低1%扣Y（线性）/ 阶梯 / 固定 | 是否与高于对称？ |
| 下限 | 扣完为止(≥0) / 可为负 / 该项最低X分 | "扣完"是 0 分还是该项最低分？ |
| 精度 | 四舍五入2位 / 保留4位 / 不处理 | 中间过程是否也取整？ |
| 偏离率分母 | 基准价 / 报价 / 控制价 | "偏离率=(报价-基准价)/?" 的分母 |
| 多价格权重 | 总价60%+分项40% / 自定义 | 分项是"主要分项"还是"所有分项"？ |

---

## 3. 法定公式（不可修改，且须做体系校验）

### 3.1 政采法定（财政部87号令第55条）
```
价格分 = (评标基准价 / 投标报价) × 价格权值 × 100
评标基准价 = 满足招标文件要求且投标价格最低的投标报价
```
- **政采货物/服务招标 → 必须用 M1（低价优先法），不得用基准价法。**
- **价格扣除（落实政府采购政策）**：政采文件中常对小微企业、监狱企业、残疾人福利单位或本国产品给予价格扣除（如 20%），以扣除后价格参与评审。此时评标基准价与投标报价均应采用**扣除后**价格：有效报价 = 投标报价 × (1 − 扣除比例)。配置生成时（`params.deduction`）或内置引擎须先按扣除比例折算报价，再套用 M1 公式；专门面向中小企业/本国产品且文件明确"不重复享受"或"无实际扣除"的项目，按原报价计算。
- 若政采文件写了"基准价法" → **提示用户"该条款可能违反87号令第55条，建议核实"**，仍按文件生成但加风险提示（见 SKILL.md §错误处理）。

### 3.2 招投标法定（12号令第29条）
- 综合评估法：价格分按"评标办法前附表"规定的公式计算。
- 经评审的最低投标价法：评标价最低者推荐为第一中标候选人（低于成本除外）。
- **招投标体系 → 公式由招标文件自定义，无统一法定公式；必须从文件中提取，不可套用政采公式。**

---

## 4. 各方法参考实现（与内置引擎一致，供 AI 配置 params 时对照）

> 约定：以下为各方法在数学上等价的参考实现，与 `calculator.html` 内置引擎一致；引擎由**配置**驱动（配置中的 `priceDimensions` 对应这里的 `RULE.priceDimensions`，`params` 对应各方法内的参数）。单维度时 `prices = bids.prices[0]`；`maxScore = priceDimensions[0].maxScore`。

### M1 低价优先法（政采法定）
```javascript
var RULE = {
    priceDimensions: [{ key: "price", label: "投标报价", maxScore: 30 }],
    defaultUnit: "万元", defaultUnitCount: 6,
    description: "政采低价优先法：价格分=(评标基准价/投标报价)×价格权值×100，基准价=最低报价（87号令第55条）"
};
function calculateScores(bids) {
    var prices = bids.prices[0], names = bids.names, n = prices.length;
    var maxScore = RULE.priceDimensions[0].maxScore;
    var minPrice = Math.min.apply(null, prices);
    var scores = [], deviations = [[]];
    for (var i = 0; i < n; i++) {
        scores.push((minPrice / prices[i]) * maxScore);
        deviations[0].push((prices[i] - minPrice) / minPrice * 100);
    }
    var results = [];
    for (var i = 0; i < n; i++) results.push({ _o: i, name: names[i], prices: [prices[i]], score: scores[i] });
    results.sort(function (a, b) { return b.score - a.score; });
    var ds = [], dev = [];
    results.forEach(function (r, i) { r.rank = i + 1; ds.push(scores[r._o]); dev.push(deviations[0][r._o]); delete r._o; });
    return {
        results: results,
        benchmarkInfos: [{ label: "评标基准价(最低报价)", value: minPrice, desc: "满足要求且价格最低的投标报价" }],
        detailScores: [ds], deviations: [dev],
        recommendedPrice: [minPrice], recommendedTotal: minPrice,
        recommendationReason: "低价优先法：报最低价得满分(" + maxScore + "分)。成本线以上尽量低；不得低于成本，否则可能被否决。"
    };
}
```

### M2 基准价法-均值
```javascript
var RULE = {
    priceDimensions: [{ key: "price", label: "投标报价", maxScore: 40 }],
    defaultUnit: "万元", defaultUnitCount: 6,
    description: "基准价法(均值)：基准价=有效报价算术平均×(1-K)；高于每1%扣0.5，低于每1%扣0.3"
};
function calculateScores(bids) {
    var prices = bids.prices[0], names = bids.names, n = prices.length;
    var maxScore = RULE.priceDimensions[0].maxScore;
    var K = 0.04, K_high = 0.5, K_low = 0.3;   // 按解析结果填参
    var sum = 0; for (var i = 0; i < n; i++) sum += prices[i];
    var benchmark = (sum / n) * (1 - K);
    var scores = [], deviations = [[]];
    for (var i = 0; i < n; i++) {
        var dev = (prices[i] - benchmark) / benchmark * 100;
        var ded = dev >= 0 ? dev * K_high : Math.abs(dev) * K_low;
        scores.push(Math.max(0, maxScore - ded));
        deviations[0].push(dev);
    }
    var results = [];
    for (var i = 0; i < n; i++) results.push({ _o: i, name: names[i], prices: [prices[i]], score: scores[i] });
    results.sort(function (a, b) { return b.score - a.score; });
    var ds = [], dev = [];
    results.forEach(function (r, i) { r.rank = i + 1; ds.push(scores[r._o]); dev.push(deviations[0][r._o]); delete r._o; });
    return {
        results: results,
        benchmarkInfos: [{ label: "评标基准价(均值×" + (1 - K) + ")", value: benchmark, desc: "有效报价算术平均×(" + (1 - K) + ")" }],
        detailScores: [ds], deviations: [dev],
        recommendedPrice: [benchmark], recommendedTotal: benchmark,
        recommendationReason: "报基准价得满分(" + maxScore + "分)。高扣" + K_high + "/低扣" + K_low + "：略低于基准价策略占优。"
    };
}
```

### M3 基准价法-去极值
```javascript
var RULE = {
    priceDimensions: [{ key: "price", label: "投标报价", maxScore: 40 }],
    defaultUnit: "万元", defaultUnitCount: 6,
    description: "基准价法(去极值)：投标人≥7家去最高1+最低1；均值×(1-K)"
};
function calculateScores(bids) {
    var prices = bids.prices[0].slice().sort(function (a, b) { return a - b; }), names = bids.names, n = bids.prices[0].length;
    var maxScore = RULE.priceDimensions[0].maxScore;
    var K = 0.04, trimEach = (n >= 7) ? 1 : 0;   // 去极值阈值
    var trimmed = prices.slice(trimEach, trimEach > 0 ? prices.length - trimEach : prices.length);
    var sum = 0; for (var i = 0; i < trimmed.length; i++) sum += trimmed[i];
    var benchmark = (sum / trimmed.length) * (1 - K);
    var orig = bids.prices[0];
    var scores = [], deviations = [[]];
    for (var i = 0; i < n; i++) {
        var dev = (orig[i] - benchmark) / benchmark * 100;
        var ded = dev >= 0 ? Math.abs(dev) * 0.5 : Math.abs(dev) * 0.3;
        scores.push(Math.max(0, maxScore - ded));
        deviations[0].push(dev);
    }
    var results = [];
    for (var i = 0; i < n; i++) results.push({ _o: i, name: names[i], prices: [orig[i]], score: scores[i] });
    results.sort(function (a, b) { return b.score - a.score; });
    var ds = [], dev = [];
    results.forEach(function (r, i) { r.rank = i + 1; ds.push(scores[r._o]); dev.push(deviations[0][r._o]); delete r._o; });
    return {
        results: results,
        benchmarkInfos: [{ label: "评标基准价(去极值均值×" + (1 - K) + ")", value: benchmark, desc: "去最高/最低各" + trimEach + "家后均值×(" + (1 - K) + ")" }],
        detailScores: [ds], deviations: [dev],
        recommendedPrice: [benchmark], recommendedTotal: benchmark,
        recommendationReason: "去极值后极端报价不影响基准价→不必刻意压低。报基准价得满分。"
    };
}
```

### M4 复合基准价
```javascript
var RULE = {
    priceDimensions: [{ key: "price", label: "投标报价", maxScore: 40 }],
    defaultUnit: "万元", defaultUnitCount: 6,
    description: "复合基准价：基准价=有效均值×α + 控制价×(1-α)"
};
function calculateScores(bids) {
    var prices = bids.prices[0], names = bids.names, n = prices.length;
    var maxScore = RULE.priceDimensions[0].maxScore;
    var alpha = 0.7, bidCap = 1000;   // 控制价；α 按文件
    var sum = 0; for (var i = 0; i < n; i++) sum += prices[i];
    var avg = sum / n;
    var benchmark = avg * alpha + bidCap * (1 - alpha);
    var scores = [], deviations = [[]];
    for (var i = 0; i < n; i++) {
        var dev = (prices[i] - benchmark) / benchmark * 100;
        var ded = dev >= 0 ? Math.abs(dev) * 0.5 : Math.abs(dev) * 0.3;
        scores.push(Math.max(0, maxScore - ded));
        deviations[0].push(dev);
    }
    var results = [];
    for (var i = 0; i < n; i++) results.push({ _o: i, name: names[i], prices: [prices[i]], score: scores[i] });
    results.sort(function (a, b) { return b.score - a.score; });
    var ds = [], dev = [];
    results.forEach(function (r, i) { r.rank = i + 1; ds.push(scores[r._o]); dev.push(deviations[0][r._o]); delete r._o; });
    return {
        results: results,
        benchmarkInfos: [{ label: "复合评标基准价", value: benchmark, desc: "有效均值×" + alpha + "+控制价×" + (1 - alpha) }],
        detailScores: [ds], deviations: [dev],
        recommendedPrice: [benchmark], recommendedTotal: benchmark,
        recommendationReason: "复合基准价含控制价权重，报价贴近基准价最稳。"
    };
}
```

### M5 反比法（通信/IT，公式同 M1 但非政采法定）
```javascript
var RULE = {
    priceDimensions: [{ key: "price", label: "投标报价", maxScore: 30 }],
    defaultUnit: "万元", defaultUnitCount: 6,
    description: "反比法：得分=最低报价/报价×价格权重×100（通信/IT，非政采法定）"
};
function calculateScores(bids) {
    var prices = bids.prices[0], names = bids.names, n = prices.length;
    var maxScore = RULE.priceDimensions[0].maxScore;
    var minPrice = Math.min.apply(null, prices);
    var scores = [], deviations = [[]];
    for (var i = 0; i < n; i++) { scores.push((minPrice / prices[i]) * maxScore); deviations[0].push((prices[i] - minPrice) / minPrice * 100); }
    var results = [];
    for (var i = 0; i < n; i++) results.push({ _o: i, name: names[i], prices: [prices[i]], score: scores[i] });
    results.sort(function (a, b) { return b.score - a.score; });
    var ds = [], dev = [];
    results.forEach(function (r, i) { r.rank = i + 1; ds.push(scores[r._o]); dev.push(deviations[0][r._o]); delete r._o; });
    return {
        results: results,
        benchmarkInfos: [{ label: "最低报价基准", value: minPrice, desc: "最低报价作为反比基准" }],
        detailScores: [ds], deviations: [dev],
        recommendedPrice: [minPrice], recommendedTotal: minPrice,
        recommendationReason: "反比法：报最低价得满分。注意不得低于成本。"
    };
}
```

### M6 直线内插法
```javascript
var RULE = {
    priceDimensions: [{ key: "price", label: "投标报价", maxScore: 40 }],
    defaultUnit: "万元", defaultUnitCount: 6,
    description: "直线内插：报价≤a得满分；a~b线性降至0；>b得0"
};
function calculateScores(bids) {
    var prices = bids.prices[0], names = bids.names, n = prices.length;
    var maxScore = RULE.priceDimensions[0].maxScore;
    var a = 90, b = 100;   // 内插区间（按文件，单位同报价）
    var scores = [], deviations = [[]];
    for (var i = 0; i < n; i++) {
        var p = prices[i], s;
        if (p <= a) s = maxScore;
        else if (p >= b) s = 0;
        else s = maxScore * (b - p) / (b - a);
        scores.push(s);
        deviations[0].push((p - a) / a * 100);
    }
    var results = [];
    for (var i = 0; i < n; i++) results.push({ _o: i, name: names[i], prices: [prices[i]], score: scores[i] });
    results.sort(function (x, y) { return y.score - x.score; });
    var ds = [], dev = [];
    results.forEach(function (r, i) { r.rank = i + 1; ds.push(scores[r._o]); dev.push(deviations[0][r._o]); delete r._o; });
    return {
        results: results,
        benchmarkInfos: [{ label: "内插区间", value: (a + b) / 2, desc: "[" + a + "," + b + "] 线性内插" }],
        detailScores: [ds], deviations: [dev],
        recommendedPrice: [a], recommendedTotal: a,
        recommendationReason: "直线内插：报价≤" + a + "得满分，建议贴近下沿但高于成本。"
    };
}
```

### M7 λ值法
```javascript
var RULE = {
    priceDimensions: [{ key: "price", label: "投标报价", maxScore: 40 }],
    defaultUnit: "万元", defaultUnitCount: 6,
    description: "λ值法：得分=满分×(1-λ×偏离率)，偏离率=(报价-基准价)/基准价"
};
function calculateScores(bids) {
    var prices = bids.prices[0], names = bids.names, n = prices.length;
    var maxScore = RULE.priceDimensions[0].maxScore;
    var lambda = 0.3;
    var sum = 0; for (var i = 0; i < n; i++) sum += prices[i];
    var benchmark = sum / n;
    var scores = [], deviations = [[]];
    for (var i = 0; i < n; i++) {
        var dev = (prices[i] - benchmark) / benchmark;   // 比例(非%)
        var s = maxScore * (1 - lambda * dev);
        scores.push(Math.max(0, s));
        deviations[0].push(dev * 100);
    }
    var results = [];
    for (var i = 0; i < n; i++) results.push({ _o: i, name: names[i], prices: [prices[i]], score: scores[i] });
    results.sort(function (x, y) { return y.score - x.score; });
    var ds = [], dev = [];
    results.forEach(function (r, i) { r.rank = i + 1; ds.push(scores[r._o]); dev.push(deviations[0][r._o]); delete r._o; });
    return {
        results: results,
        benchmarkInfos: [{ label: "评标基准价(均值)", value: benchmark, desc: "有效报价算术平均" }],
        detailScores: [ds], deviations: [dev],
        recommendedPrice: [benchmark], recommendedTotal: benchmark,
        recommendationReason: "λ值法：报基准价得满分；λ=" + lambda + "不对称时按方向判断优劣。"
    };
}
```

### M8 分段扣分法（阶梯，可不对称）
```javascript
var RULE = {
    priceDimensions: [{ key: "price", label: "投标报价", maxScore: 40 }],
    defaultUnit: "万元", defaultUnitCount: 6,
    description: "分段扣分：偏离≤3%不扣；3~5%每1%扣0.5；5~8%每1%扣1；>8%每1%扣2"
};
function calcDeduction(absDev) {
    if (absDev <= 3) return 0;
    if (absDev <= 5) return (absDev - 3) * 0.5;
    if (absDev <= 8) return (5 - 3) * 0.5 + (absDev - 5) * 1;
    return (5 - 3) * 0.5 + (8 - 5) * 1 + (absDev - 8) * 2;
}
function calculateScores(bids) {
    var prices = bids.prices[0], names = bids.names, n = prices.length;
    var maxScore = RULE.priceDimensions[0].maxScore;
    var sum = 0; for (var i = 0; i < n; i++) sum += prices[i];
    var benchmark = sum / n;
    var scores = [], deviations = [[]];
    for (var i = 0; i < n; i++) {
        var dev = (prices[i] - benchmark) / benchmark * 100;
        var ded = calcDeduction(Math.abs(dev));
        scores.push(Math.max(0, maxScore - ded));
        deviations[0].push(dev);
    }
    var results = [];
    for (var i = 0; i < n; i++) results.push({ _o: i, name: names[i], prices: [prices[i]], score: scores[i] });
    results.sort(function (x, y) { return y.score - x.score; });
    var ds = [], dev = [];
    results.forEach(function (r, i) { r.rank = i + 1; ds.push(scores[r._o]); dev.push(deviations[0][r._o]); delete r._o; });
    return {
        results: results,
        benchmarkInfos: [{ label: "评标基准价(均值)", value: benchmark, desc: "有效报价算术平均" }],
        detailScores: [ds], deviations: [dev],
        recommendedPrice: [benchmark], recommendedTotal: benchmark,
        recommendationReason: "分段阶梯扣分：避免落在高扣分段的边界（如恰好 5%、8%）。"
    };
}
```

### M9 合理低价法（含低于成本否决）
```javascript
var RULE = {
    priceDimensions: [{ key: "price", label: "投标报价", maxScore: 40 }],
    defaultUnit: "万元", defaultUnitCount: 6,
    description: "合理低价法：低于成本线→否决(0分)；其余按低价优先法计分"
};
function calculateScores(bids) {
    var prices = bids.prices[0], names = bids.names, n = prices.length;
    var maxScore = RULE.priceDimensions[0].maxScore;
    var costFloor = 80;   // 成本预警线（由用户/文件给出；不可臆造）
    var minPrice = Math.min.apply(null, prices);
    var scores = [], deviations = [[]], invalid = [];
    for (var i = 0; i < n; i++) {
        if (prices[i] < costFloor) { scores.push(0); invalid.push(names[i]); }
        else scores.push((minPrice / prices[i]) * maxScore);
        deviations[0].push((prices[i] - minPrice) / minPrice * 100);
    }
    var results = [];
    for (var i = 0; i < n; i++) results.push({ _o: i, name: names[i], prices: [prices[i]], score: scores[i] });
    results.sort(function (x, y) { return y.score - x.score; });
    var ds = [], dev = [];
    results.forEach(function (r, i) { r.rank = i + 1; ds.push(scores[r._o]); dev.push(deviations[0][r._o]); delete r._o; });
    var warn = invalid.length ? ("⚠️ " + invalid.join("、") + " 报价低于成本预警线(" + costFloor + ")，可能被否决。") : "";
    return {
        results: results,
        benchmarkInfos: [{ label: "评标基准价(最低有效报价)", value: minPrice, desc: "满足成本要求的最低报价" }],
        detailScores: [ds], deviations: [dev],
        recommendedPrice: [Math.max(minPrice, costFloor)], recommendedTotal: Math.max(minPrice, costFloor),
        recommendationReason: warn + "合理低价法：不得低于成本；其余报最低有效价得满分。"
    };
}
```

### M10 多价格维度（各维度独立计分后加权求和）
```javascript
var RULE = {
    priceDimensions: [
        { key: "total", label: "投标总价", maxScore: 30 },
        { key: "spare", label: "备品备件", maxScore: 10 }
    ],
    defaultUnit: "万元", defaultUnitCount: 6,
    description: "多维度：总价30分(基准价法) + 备品10分(基准价法)，独立计分后求和"
};
function dimScore(prices, maxScore, K_high, K_low) {
    var n = prices.length, sum = 0;
    for (var i = 0; i < n; i++) sum += prices[i];
    var benchmark = sum / n;
    var scores = [], deviations = [];
    for (var i = 0; i < n; i++) {
        var dev = (prices[i] - benchmark) / benchmark * 100;
        var ded = dev >= 0 ? Math.abs(dev) * K_high : Math.abs(dev) * K_low;
        scores.push(Math.max(0, maxScore - ded));
        deviations.push(dev);
    }
    return { benchmark: benchmark, scores: scores, deviations: deviations };
}
function calculateScores(bids) {
    var names = bids.names, n = names.length;
    var d0 = dimScore(bids.prices[0], RULE.priceDimensions[0].maxScore, 1.0, 0.5);
    var d1 = dimScore(bids.prices[1], RULE.priceDimensions[1].maxScore, 0.5, 0.3);
    var results = [];
    for (var i = 0; i < n; i++) {
        results.push({ _o: i, name: names[i], prices: [bids.prices[0][i], bids.prices[1][i]], score: d0.scores[i] + d1.scores[i] });
    }
    results.sort(function (x, y) { return y.score - x.score; });
    var ds0 = [], ds1 = [], dev0 = [], dev1 = [];
    results.forEach(function (r, i) {
        r.rank = i + 1;
        ds0.push(d0.scores[r._o]); ds1.push(d1.scores[r._o]);
        dev0.push(d0.deviations[r._o]); dev1.push(d1.deviations[r._o]);
        delete r._o;
    });
    return {
        results: results,
        benchmarkInfos: [
            { label: "总价基准价", value: d0.benchmark, desc: "总价有效均值" },
            { label: "备品基准价", value: d1.benchmark, desc: "备品有效均值" }
        ],
        detailScores: [ds0, ds1], deviations: [dev0, dev1],
        recommendedPrice: [d0.benchmark, d1.benchmark],
        recommendedTotal: d0.benchmark + d1.benchmark,
        recommendationReason: "各维度独立优化：报各自基准价得各维度满分，合计满分(" + (RULE.priceDimensions[0].maxScore + RULE.priceDimensions[1].maxScore) + "分)。"
    };
}
```

---

## 5. 策略建议逻辑（generateAdvice → 写入 `recommendationReason`）

| 公式特征 | 策略提示 |
|:---|:---|
| 不对称扣分（高>低） | 略低于基准价占优 |
| 不对称扣分（低>高，罕见） | 略高于基准价占优（可能是陷阱） |
| 对称扣分 | 贴近基准价 |
| 低价优先法（M1/M5） | 成本线以上尽量低 |
| 随机 K | 分别测算所有 K 值，取最稳健报价 |
| 去极值（M3） | 极端报价不影响基准价→不必刻意压低 |
| 分段阶梯（M8） | 避免落在高扣分段的边界（5%、8%） |
| 多价格维度（M10） | 各维度独立优化，注意权重分配 |
| 合理低价法（M9） | 绝不能低于成本→准备成本证明材料 |

> 注意：外壳不读取 `advice` 字段，**所有策略提示必须写入 `recommendationReason` 字符串**。
