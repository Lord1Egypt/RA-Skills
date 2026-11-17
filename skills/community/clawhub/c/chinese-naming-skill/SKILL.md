---
name: "chinese-naming"
description: "Guide users through systematic Chinese baby naming: bazi analysis, classics search, wuxing verification, and multi-dimensional comparison."
---

# Chinese Naming · 中文取名

引导用户完成一次系统化的中文取名。六步流程：基础信息 → 八字五行 → 期许方向 → 典籍挖掘 → 逐个验证 → 横向对比。

## 核心原则

**告知而非替决，引导而非规定。** 遇到流派分歧、方法论选择、价值判断时，向用户呈现选项和依据，把选择权交给用户。

## 流程

### ① 收集基础信息
用 `assets/requirements-template.md` 收集：父母姓名、姓氏、性别、出生时间地点、长辈名讳、地域脉络、风格偏好。

### ② 八字五行分析（可选）
先询问用户是否采用八字维度。如采用：
- 排盘后，**向用户说明**真太阳时 vs 时区时间的区别，**让用户选择**
- 分析格局和用神时，如遇流派分歧（如《渊海子平》vs《滴天髓》），**说明分歧点和各派依据，让用户选择**
- 询问是否提供父母八字作辅助参考，说明作用与局限
- 详细参考 `references/bazi-reference.md`

### ③ 确定期许方向
提供预设方向供参考（平安健康/自成其才/通透豁达/温润有度/坚韧持久），**鼓励用户用自己的话自定义**。用户自定义优先于预设。

### ④ 典籍挖掘候选名
- **向用户说明**常用典籍及取名逻辑
- **让用户选择**典籍范围，允许添加本地文档、在线链接、网络检索
- 按意境检索（非按字检索），每个候选须出自具体典籍句段
- 详细参考 `references/classics-and-wuxing.md`

### ⑤ 逐个验证候选名
用 `assets/candidates-template.md` 记录，六步验证：意境 → 取字 → 五行（康熙+字义法，不限偏旁）→ 音律 → 避讳 → 可用度

### ⑥ 六维度横向对比
用 `assets/comparison-template.md` 生成对比表（意境/期许/五行/音律/避讳/可用度），提供不同侧重的建议，**最终选择权交给用户**。

## 参考文档

- `references/flow-guide.md` — 完整流程操作指南
- `references/bazi-reference.md` — 八字五行基础知识与流派
- `references/classics-and-wuxing.md` — 典籍来源与五行验证标准

## 模板

- `assets/requirements-template.md` — 需求文档
- `assets/candidates-template.md` — 候选名记录
- `assets/comparison-template.md` — 六维度对比表
