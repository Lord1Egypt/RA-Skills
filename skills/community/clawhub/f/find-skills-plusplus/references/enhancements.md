# ++ 优化清单（相对源头 `vercel-labs/skills` 的 find-skills v1.0.0）

共 **52 项**实质增强。分七期落地。

## Phase 1 — 骨架（可演示）

| # | 优化项 | 源头版 | 本版 |
|---|---|---|---|
| 1 | 原生市场优先 | 首选外部 SkillHub | WorkBuddy 原生市场首选，复用宿主鉴权 |
| 2 | 安装前安全闸门 | 无 | 加载 `skills-security-check` + 手动清单 |
| 3 | 中文结构化卡片+排序 | 偏英文纯文本 | 综合分排序中文卡片 |
| 4 | 跨平台客户端判定 | macOS 专属变量 | `CODEBUDDY_*` / `~/.codebuddy` 健壮判定 |
| 6 | 安装历史可追溯 | 无 | `skills-install-log.md` |
| 7 | 离线/失败兜底 | 无 | 列本地已装与本地市场 |
| 8 | 综合排序+过期标记 | 只信 API score | `0.5匹配+0.3热度+0.2时效`，>365天标未维护 |
| **9** | **跨源合并去重** | **串行 fallback，漏同名** | **三源合并成统一候选表，取最优版本** |
| **10** | **安全扫描真执行** | **只是建议清单** | **下载后静态扫描，P0 阻断** |
| **11** | **本地优先搜索** | **无（仅离线才列）** | **装前先扫本地已装，秒回防重复** |
| **12** | **安装校验强化** | **只 `ls`** | **额外校验 SKILL.md frontmatter 合法** |
| **13** | **真实安全扫描脚本** | **无（仅 prompt 建议）** | **`scripts/security_scan.py` 零依赖可执行，误报控制** |
| **14** | **来源信誉门槛** | **无** | **官方源加权、低信誉降权标记** |
| **15** | **已连连接器感知** | **无** | **结合已连连接器加权/提示前置依赖** |
| **16** | **搜索结果缓存** | **无** | **TTL 24h 缓存，省 API、离线可回看** |
| **17** | **零依赖 CLI 工具** | **纯 SKILL.md 指令（无产物）** | **`findskills.py`，可演示、可测试、跨平台** |
| **18** | **离线可信注册表** | **依赖实时 API（一挂就残废）** | **内置 `registry.json`，信誉分代替编造下载量** |
| **19** | **pytest 测试套件** | **无** | **全套单测 + CI 自动跑，工程可信度** |

## Phase 2 — 智能层

| # | 优化项 | 源头版 | 本版 |
|---|---|---|---|
| **20** | **语义匹配（轻量离线）** | **纯关键词+score** | **`INTENT_SYNONYMS` 意图词典，自然语言→技能意图，零依赖、不依赖 embedding API** |
| **21** | **技能质量评级** | **无** | **七维 0-100 分，search 结果直接标注** |
| **22** | **冗余检测** | **无** | **区分「重复安装」与「功能冗余」，中文去停用+bigram 降误报** |
| **23** | **瘦身建议（只读）** | **无** | **重复安装+功能冗余+质量偏弱 → 保留/清理建议，诚实标注非真实使用追踪** |

## Phase 3 — 硬核安全 + 全生命周期

| # | 优化项 | 源头版 | 本版 |
|---|---|---|---|
| 5 | 更新与卸载 | 无 | ✅ `update` / `uninstall`（回收站可还原）/ `clean-dupes` |
| **24** | **AST 级安全分析** | **纯正则浅扫描，可绕过** | **`ast`+`shlex` 语法树级：os.system/subprocess(shell=True)/eval/exec/pickle.loads/动态拼接 rm -rf/base64+exec 组合/curl\|sh** |
| **25** | **在线目录 sync + 离线缓存** | **API 一挂就残废** | **`sync` 拉全量目录到 `registry.cache.json`（TTL 24h），真·离线全能** |
| **26** | **环境感知引用校验** | **只看表象** | **质量评级新增「引用完整性」维度，专治假优** |
| **27** | **update 子命令** | **无（仅安装）** | **重下最新并覆盖，同样过安全网关** |
| **28** | **uninstall 子命令（回收站）** | **无** | **进回收站（非硬删除），可还原** |
| **29** | **clean-dupes 子命令** | **无** | **每组保留最新一份，其余进回收站** |
| **30** | **discover 榜单 + 跨源版本仲裁** | **无** | **`discover [--new\|--trending]`；三源版本不一致自动选最高版并标出落后源** |

## Phase 4 — 对标头部技能看齐

对标对象：`self-improving-agent`（121 万下载，生态第一）、`agent-browser`（82 万）、
`skill-vetter`（31 万，同类头部）、`sandbaseai/workbuddy-skill`（成熟竞品）。

| # | 优化项 | 头部做法 | 本版落地 |
|---|---|---|---|
| **31** | **红旗补齐 8 项** | `skill-vetter` 17 项红旗 | 补 `~/.ssh`/`~/.aws` 凭据目录、`MEMORY.md`/`IDENTITY.md` 等 Agent 身份文件、裸 IP 直连、浏览器 cookie/session、`chmod 777`、静默装包、混淆转义、系统目录写入 |
| **32** | **四级风险分类** | LOW/MEDIUM/HIGH/EXTREME + 动作映射 | `classify_risk()` 按「执行块 vs 文档提及」归并，输出等级 + 动作 + 结论 |
| **33** | **权限清单** | 三问（文件/网络/命令） | `extract_permissions()` 自动提取，报告直接输出 |
| **34** | **信任层级 5 级** | Trust Hierarchy | 官方源 → 知名源 → 已知作者 → 未知 → 索取凭据（一律人工批准） |
| **35** | **frontmatter 标准化** | `version` + `metadata{slug,displayName}` | 补齐版本号与嵌套 metadata，对齐 #1 技能规范 |
| **36** | **渐进式披露** | `references/` 拆分，SKILL.md 精炼 | 365 行单体 → 核心 SKILL.md + `references/{security,cli,enhancements,ranking,roadmap}.md` |
| **37** | **市场标准卡 + 隐私条款** | `market-card.md`（含 License / Known Risks & Mitigations） | 新增 `market-card.md`；SKILL.md 与 README 增加隐私条款 |

## Phase 5 — 自我营销 + 合规（38–45）

> 「酒香也怕巷子深」——能力再强，讲不清差异化就无法脱颖而出。
> 本轮把「给自己打广告」做成技能的一等能力。

| # | 能力 | 对标 / 现状 | 本版做法 |
|---|---|---|---|
| **38** | **`promote` 自我营销引擎** | 生态内**无任何技能**具备 | 一键生成 5000+ 字推广素材：一句话/三句话简介、市场简介、README Banner+badge、9 条差异化卖点、竞品对比表、公众号/小红书/X 三套社交文案、发布检查清单、电梯演讲 |
| **39** | **`demo` 可录屏演示** | 无 | 端到端跑通「搜索→质量评级→AST 安检→冗余治理→自述」5 场景，带耗时与退出码，输出可直接录 GIF/asciinema（star 诱饵） |
| **40** | **`elevator` 30 秒电梯演讲** | 无 | 对话中可直接复述的差异化自述；SKILL.md 新增「被问到你是谁时」章节，主动亮剑而非只列功能 |
| **41** | **市场 SEO 元数据** | 头部技能用 `xiaping_*` 提升检索命中 | 补齐 `slug` / `displayName`（卖点化）/ `xiaping_trigger` / `xiaping_category` / `xiaping_tags` / `xiaping_eval_strategy` |
| **42** | **触发文案重写** | 原 description 只写能力、不写触发场景 | 卖点前置 + 中英触发词全覆盖（"找个 skill / 安装技能 / 技能管理 / 技能安全审查 / 技能装太多"） |
| **43** | **CHANGELOG 演进记录** | 头部技能迭代到 3.0.24，有版本演进史 | 新增 `CHANGELOG.md`，1.0 → 5.0 完整演进，含每轮修正的真实 bug 与数据变化 |
| **44** | **作者品牌区** | 99 万下载那位的 README 有强作者品牌引流 | README 补作者区 + 演进记录入口；`market-card.md` 标明 Publisher |
| **45** | **许可证结案 + 溯源更正** | 长期标记"上游许可证待确认" | 核实 `guipi888/find-skills` = **MIT（Copyright 2026 Kyle）**；更正此前的"官方插件"误判为**双上游署名链**；LICENSE 保留上游 MIT 全文 |

### 溯源更正说明（重要）

此前把生态里下载量最高的 `find-skills` 记为"官方插件"，**不准确**。经核实：

- 源头：`vercel-labs/skills` 的 `find-skills`（Vercel 官方）
- 生态下载量最高（99.4 万）的社区版：`guipi888/find-skills`，**MIT**，Copyright (c) 2026 Kyle
- 本版以此为**最近的派生上游**，完整保留其 MIT 许可与署名

## Phase 6 — 兑现承诺：实测修真缺陷（46–49）

> 前五轮重能力扩张，本轮转向**自我审计**：用端到端冒烟真跑一遍，
> 把「文档里吹了、实际跑不通/判不准」的地方全部修掉。
> 出场靠的不是清单更长，而是每一条都经得起当场验证。

| # | 缺陷（实测发现） | 根因 | 修复 |
|---|---|---|---|
| **46** | **偷读 `~/.ssh/id_rsa`、`MEMORY.md` 只判 MEDIUM** —— 第一卖点形同虚设 | `scan_segment` 的「引号内降级」本是给 .md 文档正文设计的，套到 .py 上：真实代码里的路径本就在引号内，P0 被降成 P1、语境被标「文档提及」 | 新增 `_sink_string_lines()`：用 **AST 判断字符串是否被 `open`/`system`/`read_text` 等危险 sink 真正使用**。被真正使用 → 不降级（EXTREME）；仅文案/日志字面量 → 降级。行级判定，兼顾漏判与误报 |
| **47** | `discover --new` **崩溃** `TypeError: bad operand type for unary -: 'str'` | registry 用 `'2026-03-05'` 字符串、缓存用毫秒整数，直接取负 | 新增 `_ts()` 统一归一为秒级时间戳，无法解析返回 0 |
| **48** | `quality` **评不了自己**，报「未找到该技能」（出场必演示项） | `discover_local` 无条件排除自身目录名 | 增加 `include_self` 参数；`quality` 支持 `self` / slug / 别名；默认仍排除自己（搜索结果不自荐） |
| **49** | 无端到端自证手段，只能靠单测（测得出函数对，测不出「敲下去能跑」） | — | 新增 `scripts/smoke.py`：**真跑 20 子命令 + 7 组参数变体 + 6 组恶意/干净样本检测力 + 文档数字一致性自检**；`--json` 供 CI 消费，任一项不过即 FAIL |

### 46 号修复的验证对照（成对测试，防回退）

| 样本 | 修复前 | 修复后 |
|---|---|---|
| `print(open('/root/.ssh/id_rsa').read())` | MEDIUM（P1/文档提及） | **EXTREME**（P0/执行块） |
| `promo = "能识破偷读 ~/.ssh 的行为"`（文案字面量） | MEDIUM | 降级，不误报 |
| `.md` 正文「注意不要泄露 ~/.ssh/id_rsa」 | MEDIUM | 保持宽容，不误报 |

> 判据不是"命中就拉满"，而是**字符串是否真的被用于危险调用**——这正是 AST 相对纯正则的分水岭。

## Phase 7 — 生命周期闭环 + 发布闸门（50–52）

> 前五轮扩能力，第六轮修真缺陷，本轮补齐「出场前的最后一公里」：
> 让已装技能能查更新、让环境问题一眼可诊、让上架前自带门槛校验——
> 把"被市场推荐"变成可自证的事（publish 直接服务此目标，且当前生态无同类）。
> 三者均复用既有零依赖能力（`security_scan.parse_frontmatter`、`discover_local(include_self=)`、
> `load_registry`/`load_cache`、`find_duplicate_installs`），不新增外部依赖。

| # | 能力 | 现状 / 缺口 | 本版做法 |
|---|---|---|---|
| **50** | **`outdated` 版本巡检** | 装了技能却不知道上游有没有新版本 | 比对 `discover_local()` 已装版本与 `load_registry()`/`load_cache()` 最新版，输出可更新清单；注册表空时回落缓存，TTL 24h 内不强制联网 |
| **51** | **`doctor` 环境体检** | 非运维用户遇 frontmatter 错 / 质量分低 / 重复安装 / 缺 Node 却跑 Node 脚本时无从下手 | 逐技能检查 frontmatter 合法性、质量分 <40、连接器依赖（tdx/westock/agent-mail）、硬编码绝对路径 / 密钥泄露；报告 `find_duplicate_installs`，并**跳过工具自身源码**免误报 |
| **52** | **`publish` 发布就绪校验（上架闸门）** | 文档吹得满，一上架就被市场门槛或占位符打回 | 校验 SKILL.md 必填 frontmatter + `metadata.slug/displayName`、LICENSE、`market-card.md`、引用完整性、README `<你的用户名>` 占位符、硬编码路径 / 密钥，**并调用 `scripts/smoke.py` 端到端冒烟自证**（--no-smoke / --strict 可配）；任一不过即 FAIL，出品前先过闸 |
