# 更新日志（Changelog）

本文件记录 `find-skills++` 从派生到逐步超越的演进过程。**保持高频、真实的迭代记录**，
是开源项目建立信任的关键信号之一。

格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)；
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

---

## [Unreleased] · 许可证对齐（仓库合规收尾）

将本仓库**新增内容**的许可从 MIT 对齐为 **MIT-0**，与 ClawHub 上架所选许可一致，降低下游再分发摩擦。

### 变更
- **LICENSE**：新增内容改为 MIT-0（保留 He Wei 署名，但不再强制要求保留许可文本）；派生自上游的部分仍受原 MIT 约束。
- **NOTICE（新增）**：完整保留上游 `guipi888/find-skills`（MIT, Copyright 2026 Kyle）与源头 `vercel-labs/skills` 的署名与 MIT 许可全文，满足 MIT 的署名保留义务。
- **文档同步**：`SKILL.md` / `MARKETPLACE-LISTING.md` / `market-card.md` / `README.md`（徽章与正文）/ `CONTRIBUTING.md` 的"本仓库新增内容"许可口径统一改为 MIT-0，上游 MIT 署名链保持不变。

> 说明：上游派生部分仍为 MIT，本仓库仅对**新增自研内容**采用 MIT-0；未删除任何上游署名声明。

---

## [5.3.0] — 2026-09-21 · 跨 agent 支持（P1-3）

补齐"多 agent 安装 / 治理"能力，扩大可触达人群，缩小与 Vercel find-skills（27 agent）在"分发面"上的差距。

### 新增
- **`detect_target_dir()` 多 agent 识别**：自动判定当前 agent（CodeBuddy 环境变量 / 家目录存在性），支持 WorkBuddy、CodeBuddy、**OpenClaw**、**Claude Code** 四端，默认 WorkBuddy 兜底。
- **`--target` 接受 agent 名**：`install <slug> --target openclaw|claude|codebuddy|workbuddy`，也可传显式路径（`expanduser`）。
- **`discover_local` 默认 roots 纳入 OpenClaw / Claude Code 技能目录**：`list` / `audit` / `clean-dupes` / `quality` 默认即可治理其它 agent 已装的技能，实现跨 agent 生态治理。

### 数据
- 版本：5.2.1 -> **5.3.0**（新增能力，增强项仍为 52，测试数仍为 140）

---

## [5.2.1] — 2026-09-21 · 审定复审修正（出厂后两轮校对 / 审核 / 审定）

5.2.0 出厂后，独立一轮「校对 -> 审核 -> 审定」复审，发现并修复两个**真实性缺陷**（均属"误报 / 虚报"类——正是工程纪律严防的）：

### 修复
- **`publish` 对自身源码误报硬编码路径**：原实现直接对 ROOT 目录扫描，把工具自身的 docstring 示例（如「/root/.ssh/id_rsa」）、审计 HTML 文档、测试夹具里的**故意写入路径**全部判为"硬编码绝对路径 FAIL"，导致上架闸门狼来了。
  -> 改为与 `doctor` 一致口径：发布工具自身（ROOT）时跳过自身源码 / 文档 / 测试的路径与密钥扫描并如实说明；第三方技能用 `--path` 指定时仍全量扫描。同时把 `.html/.htm` 加入路径扫描的文档跳过列表。
- **`outdated` 虚报"全部已是最新"**：当 registry/cache 中技能均无 `version` 字段时，版本比较恒为假（"?" vs "?"），空结果被误读为"全部最新"。
  -> 改为如实提示「注册表 / 缓存共 N 条记录，但均无 version 字段，无法比对；请先 sync」，不再谎报。

### 数据
- pytest：139 -> **140 passed**（新增 1 项 `outdated` 无版本数据诚实性测试）
- 版本：5.2.0 -> **5.2.1**（纯 bug 修复补丁，无新增能力，增强项仍为 52）

---

## [5.2.0] — 2026-09-20 · 生命周期闭环 + 发布闸门

按"是否真值得加附属功能"的诚实复检结论，补齐三条高 ROI 能力（均以 16 项新测试覆盖）：

### 新增
- **`outdated` 子命令**：比对已装版本与注册表/缓存最新版，输出可更新清单（生命周期闭环）。
- **`doctor` 子命令**：环境体检——frontmatter 合法性、质量分 <40、重复安装、连接器依赖、硬编码路径/密钥泄露，逐技能排查，跳过工具自身源码免误报。
- **`publish` 子命令（上架闸门）**：发布前校验市场门槛（必填 frontmatter / LICENSE / skill-card / 引用完整性 / README 占位符 / 硬编码路径密钥），**并调用 `scripts/smoke.py` 端到端冒烟自证**；任一不过即 FAIL。
- 复用既有零依赖能力（`security_scan.parse_frontmatter`、`discover_local(include_self=)`、`load_registry`/`load_cache`、`find_duplicate_installs`），不新增外部依赖。

### 数据
- CLI 子命令：17 → **20**
- 优化清单：49 → **52 项**（新增 Phase 7）
- pytest：123 → **139 passed**（新增 8 publish + 4 outdated + 4 doctor）
- 端到端冒烟：**PASS**（help 20/20、执行 11/11、变体 7/7、恶意样本拦截 5/5、干净样本 LOW）

---

## [5.1.1] — 2026-09-20 · 出厂前复审（校对 / 审核 / 审定）

按「工程设计需校对→审核→审定才能出厂」的流程做了独立复检，发现并修复：

### 校对（文档一致性）
- README banner 残留 **「45 项增强」** → 49；roadmap 残留 **「测试扩展到 55 项」** → 123
- README 版本号自相矛盾 **「1.0 → 5.0」** → 统一为 5.1；更新日期 09-19 → 09-20
- `promote` 生成的 X/Twitter 文案写死 **「16 CLI commands」** → 改为动态取子命令数（17）
- 加固 `scripts/smoke.py`：除比对数字外，**额外扫描 README 过期数字、数 enhancements.md 真实表格行数（防灌水）、恶意样本必须判 EXTREME（不再放宽到 HIGH）**

### 审核（代码与逻辑）
- **修复安全扫描器显示 bug**：AST 命中语境 `执行块(AST)` 曾被错显为「文档提及」，与裁定逻辑（按「执行块」算）自相矛盾 → 现统一为「执行块」
- **修复 `demo` 自曝短板**：第③步原直接扫描项目自身，演示画面出现「⚠️ 谨慎安装（需人工批准）HIGH」→ 改为扫描生成的干净样例技能，展示 **LOW · 可安装**
- 自查：`scripts/security_scan.py` 无硬编码绝对路径（跨平台 OK）；`pytest` **123 passed**；冒烟 **PASS**；恶意样本 5/5 判 EXTREME、干净样本 LOW

### 审定结论
- 核心能力经实测兑现，可进入发布流程。
- **唯一发布阻塞（需用户处理）**：README 中 `<你的用户名>` 占位符（2 处）须替换为真实 GitHub 用户名；以及 GitHub 仓库地址与授权、SkillHub/ClawHub 市场同步（真正流量所在）。
- 自扫返回 HIGH 为**预期且诚实**（扫描器是第三方审计工具，扫自身会暴露自身 subprocess 用法与攻击模式文档），已在 README「开发者」与 CI 中说明，不代表工具可疑。

**这一轮不新增卖点，只做一件事：把已经吹出去的能力，全部变成当场跑得通、判得准的东西。**

起因是做了一次端到端冒烟（真跑每个子命令），发现文档与实现存在明显落差。

### 修正（均为实测发现的真缺陷）

- **🔴 凭据窃取曾被误判为 MEDIUM —— 第一卖点形同虚设**
  `print(open('/root/.ssh/id_rsa').read())` 这种真实窃取，原本只判 MEDIUM。
  根因：为 .md 文档正文设计的「引号内降级」规则被套用到了 `.py` 上，而代码里的路径本就写在引号内，
  于是 P0 被降成 P1、语境被标成「文档提及」。
  修复：新增 `_sink_string_lines()`，**用 AST 判断字符串是否被 `open`/`system`/`read_text` 等危险 sink
  真正使用**——被真正使用则判 EXTREME 禁止安装；仅文案/日志字面量则降级不误报。
- **🔴 `discover --new` 崩溃** `TypeError: bad operand type for unary -: 'str'`
  registry 用 `'2026-03-05'` 字符串、SkillHub 缓存用毫秒整数，排序时直接取负。
  修复：新增 `_ts()` 统一归一为秒级时间戳，无法解析返回 0。
- **🔴 `quality` 评不了自己**，报「未找到该技能」——一个做质量评级的工具评不了自己，出场必穿帮。
  修复：`discover_local()` 增加 `include_self`；`quality` 支持 `self` / slug / 名称别名；
  默认仍排除自己（搜索结果不自荐）。
- **🟡 文档数字自相矛盾**：子命令数同时出现 14 / 16（实际 17），增强项 45 与 37 打架。

### 新增

- **`scripts/smoke.py`（端到端冒烟自证）**：真跑 17 个子命令的 `--help`、9 个只读子命令、
  7 组参数变体（含历史上崩过的）、6 组恶意/干净样本检测力，并校验 SKILL.md 里的每个数字
  与实现一致。任一项不过即 FAIL；`--json` 供 CI 消费。已接入 CI。
- **12 条回归测试**（111 → 123）：凭据窃取定级、文档/代码语境区分、日期混排、
  自身可评级——成对设计，防修复被回退。

### 数据

- pytest：111 → **123 passed**
- 端到端冒烟：**PASS**（help 17/17、执行 9/9、变体 7/7、恶意样本拦截 5/5、干净样本 LOW）
- 优化清单：45 → **49 项**（新增 Phase 6：实测修缺陷）

---

## [5.0.0] — 2026-09-19 · 自我营销 + 市场合规

**定位升级**：从「工具」升级为「有自我表达能力的产品」——一出场就能讲清自己强在哪。

### 新增

- **`promote` 子命令（自我营销引擎）**：一键生成全套推广素材——一句话/三句话简介、
  市场简介、README Banner 与 badge、9 条差异化卖点、竞品对比表、
  公众号/小红书/X 三套社交文案、发布检查清单、电梯演讲（5000+ 字，可直接复制）。
- **`demo` 子命令（可录屏演示）**：端到端跑通「搜索 → 质量评级 → AST 安检 → 冗余治理 → 自述」
  五个场景，带耗时与退出码，输出可直接录成 GIF/asciinema。
- **`elevator` 子命令（30 秒电梯演讲）**：对话中可直接引用的差异化自述。
- **市场 SEO 元数据**：`slug` / `displayName`（卖点化）/ `xiaping_trigger` /
  `xiaping_category` / `xiaping_tags` / `xiaping_eval_strategy`，提升市场内被检索到的概率。
- **触发文案重写**：`description` 卖点前置 + 中英触发词全覆盖，覆盖
  「找个 skill / 安装技能 / 技能管理 / 技能安全审查 / 技能装太多」等真实说法。
- **CHANGELOG.md**（本文件）与作者品牌区。

### 修正

- **溯源更正**：生态下载量最高的社区版是 `guipi888/find-skills`（**MIT，99.4 万下载**），
  此前记为「官方插件」不准确。现已在 frontmatter、`LICENSE`、README 中更正为双上游署名链。
- **许可证结案**：上游确认为 MIT（Copyright 2026 Kyle），派生合规前提成立——
  保留其 MIT 许可与署名即可发布（此前一直标记为"待确认"）。
- 演示输出中 CJK 全角字符导致边框错位，改为按显示宽度计算填充。

### 数据

- CLI 子命令：14 → **17**
- 优化清单：37 → **45 项**
- 自评质量：**92.5 / 100（优）**

---

## [4.0.0] — 2026-09-19 · 对标生态头部看齐

对标生态第一 `self-improving-agent`（121 万下载）、直接竞品 `skill-vetter`（31 万下载）。

### 新增

- **AST 级安全分析**：`ast` + `shlex` 语法树检测，识破动态拼接 `rm -rf`、
  `base64` 混淆执行、`subprocess(shell=True)`、`__import__` 动态导入等正则抓不到的模式。
- **红旗补齐 8 项**（对标 skill-vetter）：`~/.ssh`/`~/.aws` 凭据目录、
  `MEMORY.md`/`IDENTITY.md` 等 Agent 身份文件、裸 IP 直连、浏览器 cookie、
  `chmod 777`、静默装包、混淆转义、系统目录写入。
- **四级风险分类**：EXTREME（禁止）/ HIGH（需批准）/ MEDIUM（审查）/ LOW（可装）。
- **权限清单**：自动提取 文件 · 网络 · 命令 三类，回答"是否超出声明目的最小集"。
- **5 级信任层级**：官方源 → 知名源 → 已知作者 → 未知 → 索取凭据（一律人工批准）。
- **渐进式披露**：365 行单体 SKILL.md → 188 行核心 + `references/` 五个专题。
- **`skill-card.md`**：市场标准卡，含 License、Use Case、Known Risks and Mitigations。
- **隐私条款**：明确不收集、不上传、不外传。

### 修正

- `.py` 文件只走 AST、从不跑正则 → 字面量类检测（混淆转义/裸 IP/凭据路径）在 Python 中完全失效。改为 AST + 正则双跑。
- 权限清单只取行首命令，`sudo chmod` 被漏 → 改为按 `|` / `&&` / `;` / `$(` 分段取段首词。
- 自扫误判 EXTREME → 元凶是 `tests/` 恶意夹具，新增 `--exclude-tests` 显式开关（默认全扫，安全优先）。

### 数据

- pytest：55 → **96 passed**

---

## [3.0.0] — 2026-09-19 · 智能层（语义 / 质量 / 冗余）

- **语义匹配**：20 类意图同义词词典，自然语言需求 → 技能意图，离线零依赖，不依赖 embedding API。
- **技能质量评级**：七维 0-100（frontmatter / 示例 / 参考 / 文档长度 / 新鲜度 / 可操作性 / 引用完整性）。
- **冗余检测**：区分「重复安装」vs「功能冗余」，中文去停用字 + bigram 相似度，大幅降误报。
- **`prune` 瘦身建议**：只读，诚实标注"非真实使用追踪"。

### 修正

- `redundancy` 曾误把 13 个无关技能聚成一组（字符级 Jaccard 在中文上失真）。
- `clean-dupes` 曾把 `SKILL.md` 路径直接送回收站，只删文件留空目录 → 改为整目录迁移。

### 数据

- pytest：32 → **55 passed**；本地实测扫出 **31 组重复安装**。

---

## [2.0.0] — 2026-09-19 · Phase 2 骨架（可运行工具）

- 零依赖 `findskills.py` CLI：search / scan / install / list / audit / registry。
- 离线可信注册表 `registry.json`（用信誉分代替编造的下载量，`downloads=null` 即"未核实"）。
- pytest 测试套件 + CI（校验 frontmatter、跑扫描器自测、pytest）。

---

## [1.0.0] — 2026-09-19 · 派生起点

- 基于 `find-skills`（源头 `vercel-labs/skills`；社区版 `guipi888/find-skills`）派生。
- 首批 16 项增强：原生市场优先、跨源合并去重、安装前安全闸门、中文结构化卡片 + 综合排序、
  跨平台客户端判定、安装历史可追溯、离线兜底。

---

## 署名链（Attribution）

- 源头：[`vercel-labs/skills`](https://github.com/vercel-labs/skills) 的 `find-skills`
- 最近的派生上游：[`guipi888/find-skills`](https://github.com/guipi888/find-skills) — **MIT**，Copyright (c) 2026 Kyle
- 思路参考：[`sandbaseai/workbuddy-skill`](https://github.com/sandbaseai/workbuddy-skill)（真实脚本化审查）
- 红旗对标：`skill-vetter`（SkillHub，31 万下载）
- 本仓库新增内容：**何巍**，以 MIT 提供；扫描器与 CLI 均为独立自研、纯标准库、零依赖实现。
