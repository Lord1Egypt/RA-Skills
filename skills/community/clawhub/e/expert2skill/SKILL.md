---
name: expert2skill
description: |
  专家方法沉淀器（meta-skill）— 通过引导式访谈，把一个"具备专业技术/知识但不懂 AI"
  的专家（如营养师、验房师、投资顾问、设备工程师）的隐性方法，蒸馏成结构化规则库
  （rule_library JSON）+ 可运行 skill 包。

  仅在用户明确要求"把我的 XX 方法/经验做成 skill"、"帮我把我的专业判断沉淀成工具"、
  "我想让别人能按我的标准做评估"、"expert2skill"、"方法蒸馏"时激活。
  普通对话中提及"skill/方法"等词不自动触发。

  核心能力：
  1. 适配性判断（P0）— 5 问内判断方法是否适合规则引擎，不适合诚实告知转咨询型。
  2. 引导式访谈（P1-P5）— 领域定义 → 维度拆解 → 逐项蒸馏 → 条件/开放/自问题 → 权重汇总。
  3. 生成（P6-P7）— 产出 rule_library JSON（v2 schema）+ 纯本地 skill 包，含合规自检与免责声明。

  关键原则：专家只说业务语言，AI 负责翻译到 schema；AI 永不替专家做判断；
  开放题永不自动判分；不可规则化部分诚实标记。
  locale: zh-CN

agent_created: true
---

# 专家方法沉淀器（expert2skill）

> ⚠️ 执行前必读：使用本 skill 时，先从头到尾阅读本 SKILL.md 全文，并按顺序执行
> P0-P6 流程。每阶段有产出物，确认后再进入下一阶段，禁止跳步。

## 何时使用

- 用户有一项专业方法/经验/判断标准，想变成别人能用的评估工具。
- 用户说"把我的 XX 做成 skill""我的方法能变成工具吗"。
- 触发词：expert2skill、方法蒸馏、把我的经验做成 skill、我的专业方法。

## 整体流程

```
P0 适配性判断 ── 不适合 → 诚实告知，给咨询型 skill 建议
   │ 适合
P1 领域与对象定义 → rule_library 元数据
P2 维度拆解       → categories
P3 逐项蒸馏       → items + judge + 阈值  （最重，循环执行）
P4 条件/开放/自问 → conditional / text / self_check
P5 权重与汇总     → 生成 rule_library JSON
P6 打包与验证     → skill 包 + 试跑 evaluate
```

详细访谈脚本见 `references/interview-guide.md`；schema 定义见 `references/rule-library-schema-v2.md`。

## 执行指引

### P0 适配性判断（5 问内）

按 `references/interview-guide.md` P0 提问模板执行。**通过标准**：评估型 + 有明确标准 +
能接受打分/分级 + ≥2 个维度 + 愿意逐条讲述。

**不适合时的转交话术**（模板）：
> "您的方法更适合做**咨询型 skill**——由 AI 扮演您跟用户对话，而不是规则引擎打分。
> 规则引擎需要能拆成'判定对象 + 判定标准 + 结论'三件套，您的方法目前更偏经验对话型。
> 如果您愿意，我也可以帮您做一个 AI 咨询专家包。您想继续哪个方向？"

### P1-P5 访谈蒸馏

严格遵循 `references/interview-guide.md` 的提问模板与铁律，逐阶段产出：

| 阶段 | 产出 | 确认方式 |
|------|------|---------|
| P1 | 元数据（title 显示名 / id slug / 对象 / 结论 / authority） | 一句话复述确认 |
| P2 | categories 列表 | 逐条复述确认 |
| P3 | 每维度 items + judge + 阈值 + evidence | 每维度汇总 ≤5 项确认 |
| P4 | conditional/text/self_check 特殊题 | 汇总确认 |
| P5 | 完整 rule_library JSON | 逐维度展示确认 |

**P1 命名规则**：
- `title`：中文显示名，≤12 字，含"评估/检查"等动作词。
- `id`（slug）：kebab-case 小写英文（仅 `[a-z0-9-]`），AI 从显示名生成候选，专家确认/修改。
- **ch- 前缀语义**：`ch-` 前缀表示"帮网站用户代生产的 skill"（如 `ch-nutrition-assessment`）。
  expert2skill 等**平台工具自身不带前缀**（slug 即 `expert2skill`）。
  访谈阶段不涉及前缀，由打包器在 P6 决定（代生产默认 `ch-`，工具自身上架用空前缀）。

**P3 关键技巧**：
- 用"反例 → 边界 → 及格"三步挖阈值（什么不行 / 刚好及格 / 什么算好）。
- 专家迟疑阈值时，从素材库/公开口径给默认值让他微调（如 PE 20/30、ROE 15%）。
- 题型自动推断：数值→numeric，好/中/差→scale，有无→binary，多选→multi_select。
- **若判定基准依赖对象属性**（如"蛋白质 g/kg 体重"），进入 v2 能力：收集
  `subject_profile` + `judge.reference`，见 `references/rule-library-schema-v2.md`。

### P6 打包与验证

1. 调用 `scripts/distill.py` 生成规范化的 rule_library JSON。
2. 调用 `scripts/package_skill.py <rules.json> -o <目录> --publish-prefix ch-` 生成上架包
   （SKILL.md + scripts/{slug}.py + package.json + _meta.json）。
   - 生成的评估器**纯本地运行**：零依赖、零网络，支持全部题型 + v2 能力
     （subject_profile / judge.reference / weight_conditions / conditional 触发）。
   - 生成时自动按领域（投资/医疗/法律/工程/通用）写入**针对性免责声明**。
   - 本地试用可加 `--publish-prefix ""` 生成无前缀包；上架包统一 `ch-` 前缀。
3. 用 2-3 个真实案例试跑 `scripts/{slug}.py`，专家核对结果。

> **分阶段边界**：当前第一批**只生成纯本地 skill，不涉及云端规则库**。
> compliancehub 云端 evaluate / 私有规则库托管（`/api/v1/libraries`）属后续阶段，
> 本阶段不实现、不依赖。

### P7 合规与发布上架

发布前必须执行，两步：

**① 上架前自检**（自动，必做）：
```bash
python3 scripts/package_skill.py --check-upload <skill包目录> [--require-ch-prefix]
```
- 代生产 skill（帮网站用户生成）自检时加 `--require-ch-prefix`，强制 slug 带 `ch-` 前缀。
- 平台工具自身（如 expert2skill）不加该参数，slug 无前缀。
自检覆盖：slug 合法性、package.json 关键字段、
`locale: zh-CN`、激活约束（"仅在用户明确要求…时激活"）、
permissions 为空、SKILL.md frontmatter + 免责声明、
凭据安全扫描（复用 skill-secret-audit）、硬编码凭据、残留文件。
**有任何 ❌ 必须先修，全部 ✅ 才可上传。**

**② 发布引导（触发网站注册动作）**：

自检通过后，AI 必须**主动询问**专家是否要发布，而非默默结束。若专家选择发布：

1. **引导注册**：告诉专家需要 compliancehub 网站账号才能上传，给出注册入口：
   > "要把您的 skill 发布出去，需要先在 compliancehub 网站注册一个免费账号（约 1 分钟）。
   > 打开 https://compliancehub.cn/account.html?skill=expert2skill 注册即可。
   > 若您已经注册过，直接登录即可，无需重复注册。"
   - 若专家已有账号：跳过注册引导，直接进入下一步。
   - 若专家表示不注册：尊重选择，告知"skill 已生成在本地，可自行使用或日后发布"，流程结束。
2. **上传生成包**：专家注册后，引导其将 `<slug>/` 目录（或打包 zip）**上传到网站**：
   > "请把您生成的 `<slug>/` 文件夹上传到网站「我的 Skill」页，提交后由我们的团队人工审核并代上架到 ClawHub / SkillHub。"
3. **团队手动代上架**：网站团队收到上传后，按 SKILL_UPLOAD_CHECKLIST 经验完成上架
   （整包上传、触发 security scan、领域敏感 skill 强调免责）。

**③ 上架要点**（团队侧，参考 SKILL_UPLOAD_CHECKLIST 经验）：
  - ClawHub / SkillHub 实际读取 `package.json.description`（非 SKILL.md frontmatter），
    生成器已内置激活约束 + locale + 数据披露。
  - 整包上传（含 scripts/），不要只传单文件。
  - 上传后在平台重新触发 security scan 确认零 finding。
  - **领域敏感 skill 发布提示**：投资/医疗/法律类 skill 涉及持牌业务边界，
    免责声明已内置，但发布文案仍应强调"非持牌、仅供参考、不构成专业建议"，
    且不建议声称可替代持牌顾问。

- **自动化上架（网站代提交 API）属后续阶段**：等人工链路跑通、需求明确后，
  再实现 `POST /api/v1/skill-submissions` 自动代提交，当前不做。

## 铁律（违反即失败）

1. **AI 永不替专家做判断**——专家确认是唯一权威，AI 只翻译。
2. **开放题永不自动判分**——expert_review 模式，AI 只辅助展示描述。
3. **不可规则化部分诚实标记**——不硬塞，给咨询型 skill 建议。
4. **一次确认 ≤5 项**——防认知过载，大维度拆多轮。
5. **外部素材须标注来源**——authority/ref 记录出处。
6. **每阶段有产出物**——任何阶段可回退重来，不丢已确认内容。

## 输出物

- `<slug>.rules.json`：规则库（v2 schema）
- `<slug>/` skill 包：SKILL.md + scripts/*.py + package.json + _meta.json
- 产物默认放在用户指定目录（无指定则 `~/.workbuddy/skills/<slug>/`）
