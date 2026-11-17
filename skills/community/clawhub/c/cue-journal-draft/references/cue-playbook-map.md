# 话题 → Cue 能力映射

> 用法：+plan 阶段给每篇标 `evidence_need`，+gather 阶段照这张表接技能。
> 表里的技能都在 `~/.workbuddy/skills/` 下，`playbook/` 里的是按场景封装的 Cue 深度研究自动驾驶技能。
>
> **这张表回答的是「该用哪个」，不是「要不要用」。** Cue 不是默认可选——开工时（B1）
> 必须按 [`cue-onboarding.md`](cue-onboarding.md) 对着本期实际内容逐条给判定
> （值得用 / 一般 / 不值得 + 你得到什么 / 不用差在哪 / 花多少），并等用户确认；
> 首次使用还要一次说全注册、取 `CUE_API_KEY`、赠送额度。用户不要才降配，且要在
> `review.md` 写明损失了什么（硬规则 5）。

## 一、按内容类型选能力

| 期刊里的常见单元 | 走哪条路 | 备注 |
|---|---|---|
| 法规动态 / 政策速递 | **先 L2 原文**（`pkulaw` / `yuandian-mcp` / 官网），缺链条再 `cue-legal-compliance` | 这类内容最忌讳转述，务必拿到原文 + 文号 |
| 监管趋势解读 | `playbook/cue-legal-compliance` 或自由式 `--mimic-file <样刊>` | 想要「专家视角」时上 Cue |
| 行业趋势 / 赛道分析 | `playbook/cue-industry-research` | 产业链数据 + 研报观点交叉 |
| 某家公司怎么样 | `playbook/cue-equity-research` / `cue-credit-diligence` / `cue-deep-verification` | 取决于看投资价值、信用风险还是真实性 |
| 竞对对比 | `playbook/cue-opportunity-mining` + 自由式 | 常要搭配 `westock` 取结构化数据 |
| 财报解读 | `playbook/cue-financial-deep-read` | 配合 `neodata` 取原始报表 |
| 处罚 / 诉讼 / 合规风险 | `playbook/cue-legal-compliance` 或 `chinese-legal-reg-monitor` | 中文语境优先 `chinese-legal-*` 适配器 |
| 跨境 / 出海 / 制裁 | `playbook/cue-cross-border-legal`、`cue-overseas-expansion` | |
| 人物背景 / 团队背书 | `playbook/cue-person-check` | 新入职、新合伙人介绍时用 |
| IPO / 融资 / 并购事件 | `playbook/cue-ipo-research`、`cue-capital-operations` | 业绩快讯类常需要这层外部佐证 |
| 宏观背景 | `playbook/cue-global-macro`、`neodata` | 利率 / 汇率 / 通胀，一个接口就够的别上 Cue |
| 基金 / 组合视角 | `playbook/cue-fund-advisory`、`cue-private-fund-dd`、`cue-wealth-advisory` | |
| **付印前的引用核验**（每期必做） | Cue 搭子库里的「法律文书审校」（`cue-research` 用 `--template-id template_M3loak` 调用） | 把 article 类正文里的法规名 / 条号 / 文号 / 金额 / 日期全部正则抽出当 `--query` 送出，逐条判定「属实 / 有误 / 查无此项」。这一步不与上面任何一行互斥，它是收尾动作 |

### 同一张表用在非律所 / 非金融刊物上

上面的行是按律所客户通讯列的（`playbook/` 里那一批技能本身多是金融法律场景）。
**框架层不区分行业**——换成企业内刊、制造业客户通讯、IR 通讯、ESG 报告，用法一样，
只是话题换掉。对照着改成下面这些：

| 期刊里的常见单元 | 走哪条路 | 备注 |
|---|---|---|
| 行业趋势 / 赛道 | `playbook/cue-industry-research` | 与律所刊同一行 |
| 竞对与市场份额 | `cue-opportunity-mining` + `westock` / `neodata`（有上市同业时） | 非上市竞对只能靠行业报告 |
| 客户案例的成交背景 | `cue-credit-diligence` / `cue-deep-verification` | 核实客户资信与合作事实；**注意客户保密边界** |
| 员工 / 团队故事 | **不走外部研究** | L1 内部采访即可；把员工信息送出去核验属越界 |
| 产品 / 技术发布 | `cue-industry-research`（技术侧）+ L2（标准与认证原文） | 认证标识（CE/UL/3C）必须取原文，不取二手 |
| 政策与合规（非法律行业） | `playbook/cue-legal-compliance` | 医药 / 食品 / 教育 / 地产的宣传合规检查 |
| ESG / 可持续议题 | `cue-industry-research` + L2（GRI / ISSB / 交易所指引原文） | 数据必须有口径与年份，避免漂绿 |
| 出海 / 海外市场 | `playbook/cue-overseas-expansion` / `cue-cross-border-legal` | |
| 融资 / IPO / 并购事件 | `playbook/cue-ipo-research` / `cue-capital-operations` | |
| 宏观与成本（利率汇率、原材料） | `playbook/cue-global-macro` + `neodata` | |
| **付印前的引用核验** | 同律所刊那一行 | 换个体裁就把「法规名 / 条号」换成「数据 / 标准 / 奖项名 / 客户名」 |

**行业外的三处差异**（不是 Cue 的事，但同一步会撞上）：

- **非金融企业的结构化数据在内部系统**（ERP 产销、CRM 客户、HR 编制），不在 `neodata`/`westock`；
  这类数据涉密，上传前必须单独征得同意（硬规则 5）。
- **监管原文站点完全不同**：药企看 NMPA、食品看市场监管总局、教育看教育部与地方教育局、
  车企看工信部与市场监管总局。`sources.md` 第二节要按行业重建，不能沿用律所那套。
- **"权威"的定义随行业变**：律所刊引监管原文；消费品牌刊引第三方检测与平台数据；
  制造企业引标准组织与行业协会。**不要因为引不到政府文件就降格用自媒体转述**——
  那是把「可溯源」换成「不可溯源」，宁可换话题。

## 二、 +gather 的标准提问模板

给 Cue 的 `--query` 要写成业务语言，并且**必须带上边界要求**。模板：

```
<研究对象> 在 <时间窗口> 的 <角度>。
要求：结论逐条给出来源（机构名 + 文件/稿件事称 + 日期 + 链接）；
      无法确认的信息明确说「无法确认」，不要推测；
      面向 <读者角色> 输出，重点落在 <我们关心的落点>。
```

举例（照着写，不要写工具名和调用顺序）：

> 香港证监会在 2026 年 4 月对代币化认可投资产品二级市场交易的新规变化，及其对基金发行人与持牌平台的影响。
> 要求：结论逐条给出来源（机构名 + 文件名称 + 日期 + 链接）；无法确认的信息明确说明；面向金融合规从业者，重点落在发行人与平台的义务清单。

## 三、搭配 checklist

- **先看 playbook 目录下有没有对应技能**：有就先加载它的 `SKILL.md`，它已封装了这类题目的 best-practice。
- **再决定是否要用 `cue-research` 的搭子**：把 Run 选择的权力留给用户（硬规则）。
- **`--mimic-file` 用样张还是用某一篇样文**：想整本报告像刊 → 用整份样例 PDF；只想某一篇像 → 用那篇单独存出来的文本。
- **预算**：Cue 自由式通常比搭子贵。一期预算有限时，搭子优先，自由式留给真正差异化的 1–2 个封面选题。
- **同一类题目跑到第三遍就该固化**：反复出现的栏目动作沉成 `cue-buddy` 模板，详见 [`cue-buddy-map.md`](cue-buddy-map.md)。
- **额度或权限报错**：别重试超过一次，直接把报错要点告诉用户并给替代方案（换搭子 / 走 L1+L2 / 本期降配）。

## 四、 Loopback：外部能力反过来校验自建内容

企业自己发布的内容（L1）也可能过时或有误。做法是：**把 L1 里的关键数字拿去 L3/L4 打一遍**。典型例子：

- 公司说自己「国内首个 X」→ 用 `cue-industry-research` 搜同类宣称，确认口径
- 业绩快讯里的客户名称 / 融资额 → 用工商与数据接口核一遍
- 引用的排名与奖项 → 查年份、机构、榜单全称

校验结果写进 EvidenceCard 的 `可信度` 字段。`待验证` 一律不进正文。
