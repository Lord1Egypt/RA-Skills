# External References / 外部参考清单

本文件列出 `person-profile` skill 吸收的 GitHub 开源项目与学术方法论。**每条附 URL + 核心主张 + 我们吸收了什么**。

> **背景结论**：本方向（AI-agent person profile skill）GitHub 上开源项目稀缺，无同类直接对标。所有可吸收内容分散在四类相邻生态：Agent skill 生态 / Obsidian 人物笔记 / 深研证据纪律 / 权威事实核查。

## 目录

1. Agent Skill 生态（目录结构 / eval / validator）
2. Obsidian 人物笔记生态
3. 深研与证据纪律
4. 权威事实核查与学术规范
5. 方法论（Zettelkasten / Persona / Karpathy）
6. 明确吸收 vs 仅参考

---

## 1. Agent Skill 生态

### Anthropic skills + skill-creator v2
- **URL**：https://github.com/anthropics/skills ; https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf
- **核心**：SKILL.md + scripts/ + references/ + assets/ 目录标准；progressive loading；skill-creator 4 模式（Create / Eval / Improve / Benchmark）
- **吸收**：
  - SKILL.md 正文控制 ≤ 5k tokens，重内容下沉 references/
  - trigger phrases 与非 trigger 都要写
  - skill 迭代走 Create → Eval → Improve → Benchmark 闭环
- **落点**：本 skill 目录结构与 Anthropic 标准同构

### olgasafonova/SkillCheck-Free
- **URL**：https://awesomeclaude.ai/awesome-claude-skills
- **核心**：30+ 项 SKILL.md 结构/命名/语义 validator
- **吸收**：作为本 skill 的 CI 校验器候选
- **落点**：`scripts/validate_skill.py` 待实现

### shaishavmaisuria/research-paper-lifecycle-skills
- **URL**：https://github.com/shaishavmaisuria/research-paper-lifecycle-skills
- **核心**：42 个 skill 覆盖文献评审/学术写作/引用核验全生命周期
- **吸收**：把 citation verification 拆成独立子 skill
- **落点**：v1.2 考虑拆出 `citation-verification` 子 skill

### alirezarezvani/claude-skills
- **URL**：https://github.com/alirezarezvani/claude-skills
- **核心**：跨域 380+ skill + persona/agents，跨 13 工具可迁移
- **吸收**：agents/personas 结构可映射本 skill 的核心价值观+思维模式+方法论章节；多工具 install script 模式
- **落点**：v1.1 考虑加 multi-tool install script

## 2. Obsidian 人物笔记生态

### kepano/obsidian-skills（官方）
- **URL**：https://github.com/kepano/obsidian-skills
- **核心**：Obsidian CEO 亲维护 agent skill，官方 marketplace 可 /plugin install
- **吸收**：marketplace 发布路径 `/plugin marketplace add + /plugin install`
- **落点**：v1.1 考虑 Obsidian marketplace 发布

### AgriciDaniel/claude-obsidian (15.2k★)
- **URL**：https://github.com/AgriciDaniel/claude-obsidian
- **核心**：Claude Code + Obsidian 自组织知识系统；"Trust is part of the architecture"
- **吸收**：
  - **明示信任声明**（不上传/可离线/可 git）—— 对涉人物隐私的档案项目重要
  - `/claude-obsidian:wiki-lint` 命名式子命令，把校验做成可调用命令
- **落点**：本 skill README 加信任声明段；scripts/ 命令可命名为 `person-profile:validate`

### Dann Berg Obsidian People Note Template
- **URL**：https://dannb.org/blog/2022/obsidian-people-note-template ; https://gist.github.com/dannberg/2fc4d0b8a3e88cc24598473f4eb626ed
- **核心**：People Note = YAML 元数据（company/location/title/email/website/aliases/date_last_spoken/follow_up）+ Notes + Dataview 自动拉会议列表
- **吸收**：
  - YAML frontmatter 显式 `aliases`（多语言/昵称多链）
  - Central MOC + Dataview 自动聚合
  - `WHERE contains(outgoing, this.file.link)` 关系网络自动化
  - Meta Bind 一键创建档案
- **落点**：templates/person-archive.md frontmatter 加 `aliases:` 字段

### CLSherrod/markdown-crm
- **URL**：https://github.com/CLSherrod/markdown-crm
- **核心**：纯 Markdown CRM 模板，文件名 `@Contact-Name-Company`，含 aliases / Created / Contact Info / Log
- **吸收**：
  - 文件名 `@` 前缀做搜索过滤（用于人物档案可考虑）
  - Log 章节 Date-Summary 固定格式，便于结构化校验
- **落点**：v1.1 讨论是否引入 `@` 前缀

## 3. 深研与证据纪律

### synaptiai/evidence-ledger（Grade A）
- **URL**：https://www.skillsdirectory.com/skills/synaptiai-evidence-ledger
- **核心**：每个实质性 claim 一行 ledger 记录，带 source-authority level + **6 态 claim state**（verified/corroborated/reported/inferred/unknown/not applicable）；**observed / interpreted / unknown / recommended** 四区块强制分区
- **吸收（重要升级）**：
  - claim state 6 态比本 skill 原 5 级更细
  - 四区块映射到 时间线 / 思维模式 / 待核实清单 / 可操作建议 四章
  - 内联 `[EV-####]` tag 让正文每条事实可点回证据行
  - dossier-ledger-lint.sh 机械 lint 加进校验脚本
- **落点**：
  - SKILL.md 增加 **Evidence Ledger 记账** 章节
  - 新脚本 `scripts/check_evidence_ledger.py`
  - templates 增加 `[EV-####]` 内联标记

### Deepdive skill
- **URL**：https://github.com/topics/citation-verification
- **核心**：12 阶段研究流水线；dissent protection；four-layer citation verification；relevance × authority 双维筛选
- **吸收**：
  - **dissent protection**：反方声音不被吞并（本 skill 已有反例审查，加强为独立机制）
  - **four-layer citation verification**：分四层验引
  - **relevance × authority** 双维筛选证据
- **落点**：references/citation-discipline.md 加 dissent protection 段

### B143KC47/deep-research-skill
- **URL**：https://skillsllm.com/skill/deep-research-skill
- **核心**：Codex 兼容自适应研究 skill，附 research_ledger.py CLI 记账工具
- **吸收**：
  - `research_ledger.py` CLI schema：`add-evidence --source-id --quality-score --stance --claim --quote-or-locator`
  - 6 步 workflow 映射本 skill 搜索阶段
- **落点**：本 skill 的 evidence ledger 用相同 schema

### Addy Osmani proof-of-done
- **URL**：https://github.com/addyosmani/agent-skills/issues/528
- **核心**：agent 交付用 claims ledger 而非散文总结，每条 claim 标 VERIFIED / UNVERIFIED / INFERRED + 指针到 session trace
- **吸收**：
  - **交付时不写"我完成了档案"，输出 claims ledger 摘要**
  - 每条事实标 verified / unverified / inferred
- **落点**：SKILL.md 第 [7] 交付步骤升级为"输出 claims ledger 摘要"

### Moonweave-Research/ref-verify
- **URL**：https://github.com/topics/citation-verification
- **核心**：Zero-hallucination 引用核验；CrossRef/S2/PubMed 检查；verbatim abstract traceability；**retraction check**
- **吸收**：
  - **retraction check**：引用被撤回/更新的来源应显式标记
  - **verbatim 原文可追溯**
- **落点**：v1.2 加入 retraction/staleness 检查到维护流程

### Firecrawl fact-checking skill
- **URL**：https://www.firecrawl.dev/glossary/web-search-apis/fact-checking-agent-skill
- **核心**：三步 fact-check：claim → 搜索 → LLM 判 supported/contradicted/unverified
- **吸收**：
  - **多源交叉**：每个 claim 跑 2-3 独立来源检索
  - **结构化 verdict**：supported / contradicted / unverified
- **落点**：references/citation-discipline.md 加多源交叉章节

## 4. 权威事实核查与学术规范

### Wikipedia BLP（Biographies of Living Persons）
- **URL**：https://en.wikipedia.org/wiki/Wikipedia:Biographies_of_living_persons
- **核心**：在世人物内容必须引可靠来源；无来源/有争议材料立即删除无需讨论
- **吸收**：
  - 档案末尾显式写"人物是否在世"，在世则进入严审模式
  - 涉在世人物争议性内容时，"未取得"直接不写而非留空
- **落点**：SKILL.md 第 [1] 立项澄清加"人物是否在世"询问

### Wikipedia Notability（people）
- **URL**：https://en.wikipedia.org/wiki/Wikipedia:Notability_(people)
- **核心**："多个可靠且相互独立、且独立于本人的二次来源的实质性覆盖"才够资格；平台认证徽章不算
- **吸收**：
  - 立项澄清加第 4 问："是否符合 notability 标准？"
  - 自述档案标注"主要基于本人公开材料，二次来源覆盖有限"
- **落点**：SKILL.md 立项澄清升级为 4 问

### Wikipedia:Citing sources + BLP dos and don'ts
- **URL**：https://en.wikipedia.org/wiki/Wikipedia:Citing_sources
- **核心**：self-published sources 只能作为立场证据不能作为事实证据；不按宗教/性取向分类
- **吸收**：
  - 主体自出版源（官网/LinkedIn/官方博客）仅列为"主体立场"证据
  - 价值观章节避免宗教/性取向等敏感分类
- **落点**：SKILL.md 加强第 [14] 条硬规矩

### FActScore（arXiv 2305.14251）
- **URL**：https://arxiv.org/abs/2305.14251
- **核心**：把生成文本拆成 atomic facts（每条只含一个可验证事实），计算被可靠来源支持的比例
- **吸收**：
  - **atomic fact 分解作为写作硬约束**：一条时间线只写一件事
  - 写完后脚本化算档案的 FActScore
- **落点**：`scripts/check_fact_score.py` v1.2 实现

### HELM（Stanford CRFM）
- **URL**：https://crfm.stanford.edu/helm/
- **核心**：Holistic Evaluation of Language Models — 多维度评估而非单一分数
- **吸收**：档案验收至少四维度：事实精度（FActScore）+ 引用质量 + 反证覆盖 + 边界承认完整度
- **落点**：benchmarks/benchmark-rubric.md 升级为多维评估

### Cited but Not Verified（arXiv 2605.06635）
- **URL**：https://arxiv.org/abs/2605.06635
- **核心**：引用质量三维评估：Link Works / Relevant Content / Fact Check；引用数量与质量成反比
- **吸收**：
  - **F6 failure**：引用存在但不支持该 claim，比"引用不存在"更危险
  - 检查"引用是否真正支持该 claim"而不只是"链接是否可打开"
- **落点**：references/citation-discipline.md 加三维引用评估

### LitRAG / RefCheckr
- **URL**：https://github.com/topics/citation-verification
- **核心**：两阶段验引：先跑确定性 quote 匹配（quote 是否在原文里），再 LLM judge 判 passage 是否支持 claim
- **吸收**：
  - 阶段 1：字符串匹配验证所有直引语真的来自被引源
  - 阶段 2：对每条事实 claim 判 cited source 是否真正支持
- **落点**：`scripts/verify_quotes.py` v1.2 实现

### Evidence-Ledger Adjudication（arXiv 2607.26512）
- **URL**：https://arxiv.org/abs/2607.26512
- **核心**：claim-evidence traceability workflow；agent 条件 0.676 relation accuracy（vs baseline 0.383）
- **吸收**：
  - **adjudication 路由**：不支持/矛盾/缺证据的 claim 强制回炉不进最终档案
  - 接受"仍 30% 需人审"的现实
- **落点**：SKILL.md 加"人审兜底"章节

## 5. 方法论

### Salesforce Agentforce Personas
- **URL**：https://www.salesforce.com/in/agentforce/personas
- **核心**：企业级 agent persona 设计框架，强调校准+部署+品牌一致 voice
- **吸收**：
  - **persona 校准测试**：写完 profile 后让 LLM 以该 persona 回答校准问题，看是否偏离人物真实立场
  - in-character QA
- **落点**：v2.0 考虑加"persona-from-archive"桥接子 skill

### Karpathy LLM Knowledge Base — Compiler Analogy
- **URL**：https://www.mindstudio.ai/blog/karpathy-llm-knowledge-base-compiler-analogy
- **核心**：LLM 是编译器；逐源抽取 → 跨源综合的两阶段 pipeline
- **吸收**：
  - **阶段 1** 每源用固定 prompt 抽 10 条 atomic facts
  - **阶段 2** 把抽取结果（非原文）喂给综合 prompt 合成到 11 节
- **落点**：SKILL.md 第 [2] 前置研究阶段加入两阶段 pipeline

### Karpathy 视角模拟 prompt 建议
- **吸收**：**不要问"你如何看 X"，问"某人会怎么看 X"** —— 从角色扮演改为视角模拟
- **落点**：references/writing-style.md 加"视角模拟 vs 角色扮演"章节

### Persona prompting 研究（Hu & Collier 2024）
- **URL**：https://arxiv.org/abs/2410.06359
- **核心**：162 persona × 4 家族测试显示加 persona line 对准确率提升多数与噪声不可区分
- **吸收**：
  - 档案生成 in-character 回答时，persona 只作 voice filter 不作事实来源
  - 避免让 LLM 扮演人物"补充档案没有的事实"
- **落点**：v2.0 加桥接子 skill 时的边界

### Zettelkasten（Luhmann 原法 + Ahrens 系统化）
- **URL**：https://www.luhmann.it ; https://ahrens.com
- **核心**：Luhmann 只有 Bibliographic + Permanent 两种卡；Ahrens 加 Fleeting/Literature/Permanent/Project 四档
- **吸收**：
  - **人物档案 = Permanent Note**（可独立理解完整想法）
  - **人物-README.md = Overview Note**（索引反向链回）
  - 11 节+15 硬规矩 = Luhmann 意义上的"一次定好规则"决策最小化
- **落点**：DESIGN.md 加"与 Zettelkasten 术语对齐"章节

---

## 6. 明确吸收 vs 仅参考

### 明确吸收（已进入 SKILL.md / templates / scripts）
- ✅ Anthropic skill 目录结构
- ✅ synaptiai evidence ledger（6 态 claim state + 四区块 + `[EV-####]` tag）
- ✅ Addy Osmani claims ledger 交付格式
- ✅ Wikipedia BLP 在世人物处理规则
- ✅ Wikipedia Notability 立项第 4 问
- ✅ Dann Berg YAML `aliases:` 字段
- ✅ Karpathy 两阶段 pipeline（抽取 → 综合）
- ✅ Deepdive dissent protection
- ✅ Firecrawl 多源交叉验证
- ✅ AgriciDaniel 信任声明
- ✅ Zettelkasten 术语对齐（Permanent Note / Overview Note）

### 仅参考（v1.1+ 视情况引入）
- 🟡 skill-creator 4 模式 eval 闭环
- 🟡 SkillCheck-Free CI 校验器
- 🟡 Moonweave retraction check
- 🟡 FActScore 脚本化验收
- 🟡 LitRAG 两阶段验引
- 🟡 markdown-crm `@` 前缀
- 🟡 Obsidian marketplace 发布
- 🟡 Salesforce persona 校准测试
- 🟡 Karpathy 视角模拟（避免角色扮演）
- 🟡 Cited but Not Verified 三维引用评估

---

## 7. 生态位结论

**本方向 GitHub 开源项目稀缺**，person-profile 项目占据独特生态位。最接近对标是 Dann Berg Obsidian People Note Template（CRM 向、非研究向）。本 skill 的定位是**研究向人物档案**（不是 CRM，不是 bio 生成），融合 Zettelkasten 结构 + evidence ledger 纪律 + 学术引用规范，是**当前生态空白区**。
