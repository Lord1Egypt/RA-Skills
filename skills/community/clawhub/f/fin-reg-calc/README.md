# 金融AI合规计算 / Finance AI Compliance Calculator

A deep compliance tool for the "financial / licensed-institution AI (advisory · risk control · AML)" domain under the LGD Three Laws: investor suitability matching + large-amount reporting threshold checks (zero-dependency).

## English

### Pain point
Financial-AI compliance elements (suitability / large-amount filing) lack executable automated checks and rely on error-prone manual work.

### Quick start
```bash
python fin_reg_calc.py --help
```

### How the three laws land
- Registered → system/data identity registration (this domain's terminology)
- Evidenced → evidence artifacts verifiable (this domain's evidence types)
- Gated → high-risk actions pass through the gate (this domain's thresholds)

### Positioning
This skill is a **deep landing component** of the "凡自治之物" standard in the financial / licensed-institution AI domain — others can copy the features, but not the definition power of the standard.

![LGD-Powered](lgd-powered.png)

## 中文

LGD 三律在「金融 / 持牌机构 AI（投顾·风控·反洗钱）」域的纵深合规工具：投资者适当性匹配 + 大额上报阈值校验（零依赖）。

### 痛点
金融AI合规要素（适当性/大额报备）缺乏可执行的自动化校验，依赖人工易错漏。

### 快速开始
```bash
python fin_reg_calc.py --help
```

### 三律落地
- 有籍 → 系统/数据身份登记（本域术语）
- 有证 → 证据工件可核验（本域证据类型）
- 有门禁 → 高风险动作过门禁（本域阈值）

### 定位
本技能是"凡自治之物"标准在金融 / 持牌机构 AI（投顾·风控·反洗钱）域的**纵深落地件**——别人可抄功能，抄不走标准定义权。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

- **代码**（本包 `.py` 文件）：**MIT**
- **本 `README.md` / `SKILL.md` 及其中的理论文本、方法论与一切理论表述**：**不在 MIT 覆盖范围内**，保留所有权利（All rights reserved）

```
© 2026 SynomosAI · China. All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" — 未申请实体注册、未申请商标注册
                        (not a registered legal entity; no trademark registered)
生产参考部署 (production reference, self-reported) : 无（未声明外部生产参考部署）
                    ← 非认证、非背书、非监管认可（not a certification or endorsement）
代码许可 (code license) : 本包未附 LICENSE 文件（许可待定）
                    本文本与理论表述不在任何代码许可覆盖范围内
引用格式 (cite as)      : 本资产无 DOI
```
（上列为《LGD 对外表述规范》§3.2 统一块，**整体复制、未删改**；发布/重提前须照最新版本复核。）
