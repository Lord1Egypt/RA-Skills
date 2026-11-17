# 输出模板 / Demo（投标报价策略沙盘）

> 以下为技能面向用户的标准输出样例：先给出结构化解析供确认，确认后给配置 JSON，最后给使用说明与免责声明。

---

## ① 解析结果（待确认）

```json
{
  "method_id": "M3",
  "method_name": "基准价法-去极值-随机K",
  "system": "招投标",
  "benchmark": { "base": "算术平均值", "trim_rule": "投标人≥7家时去最高1+最低1", "trim_threshold": 7, "adjustment": "×(1-K)", "K_type": "随机抽取", "K_values": [0.03,0.04,0.05], "K_default_for_calc": 0.04 },
  "scoring": { "weight": 30, "full_score_condition": "报价=基准价", "above_rule": "每高1%扣0.5分(线性)", "above_step": 0.01, "above_deduct": 0.5, "below_rule": "每低1%扣0.3分(线性)", "below_step": 0.01, "below_deduct": 0.3, "floor": 0, "precision": "四舍五入保留2位" },
  "deviation_formula": "(报价-基准价)/基准价×100%",
  "special_rules": ["扣完为止"],
  "ambiguities_found": ["'每高1%'按线性连续处理"],
  "risk_flags": ["不对称扣分：高扣0.5/低扣0.3，策略上略低于基准价有利"]
}
```

📋 请确认：✅ 正确 → 回复"确认"，我生成配置 ｜ ✏️ 有误 → 指出哪里错 ｜ ❓ 不确定 → 我按最可能理解生成

---

## ② 配置 JSON（确认后生成）

```
规则：基准价法-去极值-随机K / 来源：XX 项目施工招标 / 方法ID：M3 / ⚠️本测算仅供参考，以招标文件原文为准
```

```json
{
  "methodId": "M3",
  "methodName": "基准价法-去极值-随机K",
  "system": "招投标",
  "priceDimensions": [{ "label": "投标总价", "maxScore": 30 }],
  "defaultUnit": "万元",
  "defaultUnitCount": 3,
  "description": "报价得分满分30分，以去最高最低后的算术平均价为基准价，基准价×(1-K)为满分（K随机抽取0.04）；每高于基准价1%扣0.5分，每低于基准价1%扣0.3分，扣完为止。",
  "params": { "K": 0.04, "K_high": 0.5, "K_low": 0.3, "trimMinCount": 7, "trimEach": 1 },
  "bids": { "names": ["A","B","C"], "prices": [[100,110,120]] },
  "recommendation": "不对称扣分（高0.5/低0.3）：略低于基准价（约109万）得分更优；随机K请分别测0.03/0.04/0.05取最稳健报价。"
}
```

---

## ③ 使用方式

📦 **使用方式**
1️⃣ 打开 `calculator.html`（单文件，无需安装）
2️⃣ 方式一：粘贴上方配置 JSON → 应用并测算
   方式二：按引导手填表单 → 测算得分
⚠️ **免责声明**
· 本测算由内置公式 + 您填写的参数生成，可能存在理解或录入偏差
· 投标决策前务必人工核对招标文件原文中的评分公式
· 本工具只算报价得分维度，请结合技术分/商务分综合判断
· 本工具不构成任何投标建议或中标承诺
