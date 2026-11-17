# CHANGELOG

## [1.9.6] — 2026-09-25 · 上架元数据固化（每次 publish/release 自动列出 categories + topics，供直接复制操作）

### 新增：发布元数据自动列出（回应"每次都要帮我列 categories/topics 我才好操作"）
- **frontmatter 固化上架元数据**：每个技能 SKILL.md 新增 `clawhub_categories`（ClawHub 官方精确 slug，≤3）、
  `clawhub_topics`（≤5，自动过滤保留词/≤48 字符）、`github_topics`。缺失时由 keywords 自动推导。
- **`publish` / `release` 每次都打印**：ClawHub 分类(slug) + ClawHub Topics + GitHub topics，可直接复制粘贴到各站，
  不用再问我"填什么分类/标签"。
- **ClawHub 官方 slug 白名单**已内置（`development/automation/security/...`），自动映射内部可读标签 → 官方 slug，
  杜绝"分类填错被拒"。
- 本技能与 `find-skills++` 均已预填各自的上架元数据（`parse_frontmatter` 读同目录 SKILL.md，跨技能通用）。

## [1.9.5] — 2026-09-25 · 多站上架编排（publish：正确更新/新技能后，一键分发 GitHub + ClawHub）

### 新增：★多站上架编排 `publish`（显式逐站授权，安全闸门前置）
- **新增子命令 `publish`**：统一入口，把"正确更新或有新技能后，自动上传到多站"做成一条命令。
- **显式逐站授权**（回应 ClawHub 误判 + 用户的"校对/审核/审定"要求）：每个目标需对应开关
  —— `--github`（推送到 GitHub）、`--clawhub`（经本机已登录的 clawhub CLI 发布）、
  `--xiaping` / `--workbuddy`（本轮预留）。**未开任何开关 → 绝不触碰任何远程**（防静默外发）。
- **安全闸门前置**：先跑 `validate`（校对，含 ★安全红线凭据扫描）+ `secretscan`（审定）；
  命中硬编码凭据/授权码 → **直接拒绝上架任何站点**，绝不入库/外发（`--allow-secret-risk` 可强制，危险）。
- **GitHub 推送**：`git add/commit/push`；普通 fast-forward，历史曾被 `git filter-repo` 重写、远端本地分叉时
  加 `--force-history`（用 `--force-with-lease` 防覆盖他人提交）。
- **ClawHub 发布**：本机已装并登录 `clawhub` CLI 时真发布，否则回退人工导入情报（与 `release` 一致）。
- **虾评 / WorkBuddy 本轮为预留位**：`--xiaping`（xiaping.coze.site）、`--workbuddy`（open.workbuddy.cn SkillHub）
  两者均无公开 API，本轮只给人工上传链接；待接入开放接口/机器人后同样的授权模型即可真自动。
- 子命令数 17 → **19**；`pytest` 84 → **88 passed**（新增 4 项 publish 断言：无开关不触远程 / dry-run 预览 / 凭据闸门拦截 / 预留位打印）。

## [1.9.4] — 2026-09-25 · 安全红线强化（凭据泄露硬闸门，校对/审核/审定环节消灭"不该进 GitHub 的东西"）

### 新增：★安全红线 secretscan（主动消灭凭据泄露）
- **新增独立子命令 `secretscan`**：专项扫描全仓硬编码密码 / 授权码 / API Token，**独立于就绪分**，供发布前单独把关。
- **`validate` / `gate` / `release` 内置 secret 维度（权重 12）**：发布前强制扫描；命中即 FAIL，并**直接拒绝 `release` 的提交/推送/发布**（审定闸门），绝不让凭据有机会入库。
- **扫描覆盖（宁可误报也要拦真凭据）**：① `.env` 文件本身即风险（禁止入库）；② 已知厂商令牌格式（AWS/GitHub/Slack/Google/Stripe/OpenAI/OpenRouter/JWT/PEM 私钥/`user:pass@host` BasicAuth）；③ 硬编码凭据赋值（`PASSWORD="..."` 等，仅当赋值左侧标识符含凭据关键词才判，避免文档/字符串误伤及扫描器自身被自伤）。
- **安全设计**：环境变量引用（`os.environ.get(...)` / `os.getenv(...)` / `${VAR}` / `{{ secrets.X }}`）视为安全；报告**一律脱敏**（仅留前 4 + 后 2 字符），**绝不回显明文**；误报用仓库根 `.releaser-secret-allow` 写放行正则（谨慎）。
- **应急指引**：已泄露须立即轮换/吊销凭据 → `git filter-repo --path <file> --invert-paths` 清历史 → 强推覆盖远端。

### 文档
- SKILL.md：「🔒 安全与隐私」声明新增安全红线硬闸门说明；命令总览与 validate 权重表新增 secret 维度（权重 12，合计仍为 100）；新增 §2.7.1 `secretscan` 专节；§4 发布清单新增 `secretscan` 步骤。
- SKILL.en.md / README.md 同步。

### 验证
- pytest **84 passed**（新增 6 项凭据闸门断言：硬编码密码 FAIL、拦截 release、secretscan 命中且脱敏、环境变量引用放行、`.env` 命中、allowlist 放行；原有 78 + 新增 6）。
- 技能自身 `validate` 13/13 PASS、100/100（无凭据误报）；`secretscan` 干净通过；`selfdemo` 8/8。

## [1.9.3] — 2026-09-24 · 安全整改（回应 ClawHub SkillSpector 误判 malicious.llm_malicious）

### 根因
- ClawHub SkillSpector 将本技能判为 `malicious.llm_malicious` 并 Blocked/Hidden。经排查，真正触发项是**技能目录内混入的个人辅助脚本 `send_review_email.py`**——其中硬编码了一个真实 QQ 邮箱 SMTP 授权码，并会把技能文件外发到指定邮箱。任何含明文凭据 + 外发脚本的技能都会被安全扫描判恶意。
- 次要因素：文档含"链式传播/碾压/护城河/搜索即获客/设计即分发"等易被解读为"生态滥用/自主传播"的营销话术；`release` 默认会静默 `git push` + 自动 `clawhub publish`；存在无用的 `--api-token` 凭据形参。

### 修复
- **删除 `send_review_email.py`**（个人邮件辅助脚本，不应进入发布包）；`.gitignore` 新增 `send_*.py` / `*_email*.py` 防再混入。⚠️ 该文件此前已提交进 git 历史并推到 GitHub，密码已暴露，**须立即重置 QQ 邮箱 SMTP 授权码**并清理历史。
- **release 远程动作改为显式门禁**：`git push` 需 `--push`、`clawhub publish` 需 `--publish`，默认只本地提交 + 打印人工导入步骤，绝不静默触碰远端。
- **删除死代码 `--api-token` 凭据形参**。
- **文档去操纵化**：移除全部"链式传播/碾压/护城河/搜索即获客/设计即分发/分发节点/全网分发"等话术，改为"链回徽章/差异化价值/覆盖长尾搜索/引用致谢"等中性表述；新增显式「🔒 安全与隐私」声明（纯本地、除显式远程动作外无外联、不存凭据、只读扫描、账本本地化、无命令注入面）。
- **修正 §3.4.2 错误说法**：OG 图接口对**任何** slug（含假 slug）都回 200 占位图，**不能**作为"已上架"证据；权威核验改用 `clawhub inspect` / `clawhub search`。

### 验证
- pytest **78 passed**（`release` 新增 2 项安全断言：未传 `--push`/`--publish` 绝不发起 git push / clawhub publish；原有 77 + 新增 1）。
- `validate` 12/12 PASS、100/100；`selfdemo` 8/8。
- 全目录凭据扫描：除已删除文件外，无硬编码 token / 无 `urllib`/`requests`/`socket` 外联代码。

## [1.9.2] — 2026-09-24 · 三审文档修正（无代码改动）

### 校对发现并修复 2 处文档缺陷
- README「30 秒了解它」代码示例误写 `python releaser.py elevator`（`elevator` 非子命令；30 秒电梯演讲由 `promote` 产出）→ 改为 `python releaser.py promote --path .`。
- `SKILL.en.md` §2.3 遗留中文「data回流」→ 改为「data flows back」（英文手册不应残留中文）。

### 验证（三审）
- 子命令计数：SKILL.md / SKILL.en.md / README 三处均写 17，与代码 `build_parser` 实际注册 17 个一致。
- pytest **77 passed**（与 README 徽章「77 tests」一致）；`validate` 12/12 PASS、100/100；`selfdemo` 8/8；`promote` 正常产出电梯演讲。
- `releaser.py elevator` 经代码核验**确不存在**（17 子命令清单中无 elevator），证实 README 原写法为断链。

## [1.9.1] — 2026-09-24 · 文档沉淀（发布管道实战 gotcha 增补，无代码改动）

### 沉淀（本轮两个技能双端上架实战中验证、此前文档未覆盖的硬知识）
- §3.4.1 ClawHub CLI 实操：Windows 须调 `.cmd` 包装器；`whoami`/`search`/`login --token` 用法；分类固定 8 选、强制满 3。
- §3.4.2 确证"已上架"核验法：ClawHub 搜索索引滞后（搜不到 ≠ 没上架）；**后经 1.9.3 更正**：`og/skill` 接口对**任意** slug（含假 slug）都回 200 占位图，**不能**作为已上架证据，权威核验应改用 `clawhub inspect` / `clawhub search`。
- §3.6 增补：GitHub API **密码鉴权已停用**（建库只能 SSH 推已存在仓库 / PAT / 网页自建）；clawhub `.cmd` 包装器；pytest **批量删除守卫** SystemExit 1 不影响结果。
- **双语推广件（本回合新增，无代码改动）**：README.md 重写为推广级双语（英文 TL;DR + 徽章行 + 竞品对比表 + 双语卖点/长尾）；新增 `SKILL.en.md` 全英文手册（17 子命令 + 陷阱速查 + 发现机制）；生成真实 `readiness-badge.svg`（100/100）提交进仓库，README 徽章链回 ClawHub 已上架页。frontmatter 双语元数据（`description_zh`/`description_en`/`keywords` 中英混合/`xiaping_*`）此前已具备。

## [1.9.0] — 2026-09-23 · 体系升级（发布侧治理系统：状态层 + 生命周期 + 自证底座 + 供给侧策展）

### 新增（对标 find-skills++ 治理模型，落实体系级支柱 A/B/E/F——纯代码可落地）
- `registry` 子命令 + 本地账本（默认 `~/.workbuddy/cli-skill-release/ledger.json`，可用 `RELEASER_LEDGER` 覆盖）：
  持有"已发布技能账本"（slug/name/repo/version/score/market/path/published_at）。`release` 成功自动登记，
  从"一次性校验器"升级为"发布侧治理者"（状态层 A）。
- `recheck` 子命令：读账本再校验已发布技能，对比登记分数，报告 漂移/弃用/缺失/健康——
  把"发完即终"升级为持续治理（生命周期 B）。
- `selfdemo` 子命令：当场对自己仓库运行每个能力并打印演示摘要（主张即演示），
  对标 find-skills++ 的 smoke.py，碾压级信任不靠叙述靠当场跑（自证底座 E）。
- `curate` 子命令：把 `gap` 的市场情报升级为可操作策展清单（组合机会 / 空白类目 / 单薄类目优先级），
  主动告诉生态该造什么（供给侧策展 F）。

### 设计依据
- 上一轮对标 find-skills++ 体系模型，指出 cli-skill-release 缺 6 根支柱；其中 A/B/E/F 为纯代码可落地，
  本期逐一落实。C/D（双向活通道：find-skills++ 读取 readiness 信号 + 本工具消费其市场数据）需接口打通 + 授权，
  已预留 `gap --scan-json` 与账本数据结构作为对接基座。
- 子命令增至 **17 个**（本期新增 registry / recheck / selfdemo / curate 四大体系支柱 A/B/E/F）；dogfooding 自身仍 12/12 PASS、100/100。

## [1.8.0] — 2026-09-23 · 长尾强化（diagnose 长尾诊断 + preflight 上架清单 + 双语发现元数据 + clawhub CLI 真一键）

### 新增（长尾功能：让"搜索即获客"成立）
- `diagnose` 子命令：内置 **长尾知识库（症状→根因→修复）**，直接回答用户实际会搜的长尾问题
  （"LICENSE 显示 Other" / "pytest exit code 2" / "CI 一直红" / "技能搜不到" / "我的技能能不能发" 等）。
  竞品（jeremyknows/publish-skills 等）只给静态清单，我们给**可执行 + 可诊断**——这是"搜索即获客"的发动机。
- `preflight` 子命令：`--market clawhub|skillhub|agentskills|generic` 输出**市场定制上架前检查清单**
  （markdown 勾选框 + 必填/建议标注），逐条对应真实规则（MIT-0、skill-card.md 保留名、Topics≤48、3 分类、
  仅文本文件、GitHub topics、`gh skill publish --dry-run` 等），回答长尾"skill publish checklist /
  pre-publish checklist for agent skills"。
- **双语 README.md**：用中英文长尾问题做 H2/H3 标题 + 双语正文，被搜索引擎 / ClawHub / GitHub 索引
  （人类与英文搜索面的核心载体，ClawHub 亦要求 README 必填）。

### 发现元数据强化（基于 2026 实测检索机理）
- `description` 改写为**含英文触发短语的双语**（ClawHub 官方确认 `description` 是 vector search 的匹配面），
  并保留 `description_en`；新增 `tags` 字段（publish / skill-publishing / pre-publish-checklist / clawhub /
  agent-skills / quality-gate …，决定市场相邻位）。
- SKILL.md §5.1 写明**中文 / 英文"被找到"三杠杆**（AI keyword 文本匹配 / description vector search / tags 相邻位 /
  GitHub topics 喂外部索引器）+ 长尾词清单（中/英）。

### release 增强（修正"无公开 API"的旧判断）
- 2026 实测：ClawHub **无公开 REST/网页 publish 端点，但有官方 npm CLI `clawhub publish`**。
  `release` 现可**探测并直调 clawhub CLI**（已装且登录即真一键发布，英文生态），缺 CLI 则回退人工导入情报。
  新增 `--no-cli` 强制回退。诚实标注：网页/REST 端点仍不存在，CLI 是合法真一键路径。

### 设计依据
- 先分析"找 skill 的人/AI"的发起与搜索模式（中文 keyword 文本匹配 + 英文 description/tags/topics 三杠杆 +
  自然语长尾触发），据此把"被找到/一直被需求/真解决问题/链式传播"落成**长尾功能**，而非空想营销。

## [1.7.0] — 2026-09-23 · 被发现 + 链式传播（badge 引擎 + promote 工具箱 + 发现元数据）

### 新增（传播系统，回应"如何被找到/一直被需求/链式传播"）
- `badge` 子命令：基于 `validate` 就绪分生成 shields 风格 SVG 徽章（绿≥90/黄70-89/红<70），
  并输出**链回本技能页**的 markdown 片段；徽章图片自托管于用户仓库 raw 地址，渲染必现。
  这是链式传播的发动机——每个使用者挂徽章，访问者点入即转化。
- `promote` 子命令：一次性产出"宣传工具箱"（README 徽章区 + 电梯演讲
  "别人 lint 文档，我们 execute 引擎" + 社媒可转发文案 + 安装一行 + 链式玩法说明），
  把一次下载变成一次分发。
- SKILL.md frontmatter 强化：keywords/description 命中高频查询
  （发布技能 / 上架 skill / publish skill / validate skill / 技能质量门禁 / skill CI gate / 技能徽章）。
- 新增 §5「如何让本技能被找到 + 链式传播」：设计即分发，文档直接教用户帮我们扩散。

### 设计依据
- 先分析"找 skill 的人/AI"的发起逻辑（本地→原生市场 keyword→社区 score 文本匹配→合并排序）
  与操作逻辑，据此把"被找到/一直被需求/真解决问题/链式传播"落成工具能力，而非空想营销。

## [1.6.0] — 2026-09-23 · 碾压级强化（功能验证 + CI 门禁 + 透明评分 + 组合缺口）

- **★功能级/可执行验证（护城河）**：`validate` 新增 compile + import + `--help` 烟测三维，把技能 CLI **真正执行起来证明它能 boot**。竞品（skill-lint / agent-skill-linter / @effectorhq/skill-lint / Skill Validator 等，已联网核查 6 款）全部只查 paperwork，**无人做功能验证**。权重表重排为 12 维（功能验证独占 32/100：compile 8 / import 10 / --help 14），使"就绪分"从"格式分"升级为"格式+功能分"。
- **`gate` 子命令（CI 门禁）**：`gate --path . --min 90` 就绪分低于阈值即非零退出，把"发布就绪分"变成可编排的流水线质量闸门（readiness-as-a-service），零依赖、1 行接入任何 CI。
- **透明评分 `--rubric`**：输出每维度权重+理由（含 `--json` 的 `rubric` 字段），使分数可被审计、可被信任，回应竞品"20 条规则但不可解释"的短板。
- **`gap` 升级为组合缺口**：本机覆盖始终计算；加 `--scan-json` 叠加 find-skills++ 真实市场数据后，交叉出"市场有供给 / 你为 0"的组合机会（独有飞轮情报）。
- 测试 48 → **54**（新增功能验证 compile/import/--help 三态、gate 通过/拦截、--rubric 输出与 JSON 字段、gap 组合机会）。
- Dogfooding 闭环保持：工具对自身 `validate --path .` 仍 **9/9 PASS、就绪分 100/100（含功能维度）**。

## [1.5.0] — 2026-09-23 · 强化路线落地（TAM 泛化 + 对标头部 + 发布接口预留）

- `validate` 新增 `--mode package`：从「CLI 技能」泛化到**任意零依赖 Python 包**发布（再加打包清单 `pyproject.toml/setup.py/setup.cfg` 检测，信息项不计分）。与 `--mode cli` 共同把受众从"技能作者"拓到"所有 Python 包作者"（TAM ×N）。
- `validate` 新增 `--bench`：把绝对就绪分升级为**对标头部技能画像的相对分**——以满分 100 为头部基线（基准=本工具自身 9/9 PASS），报告"距头部还差 X 分 + 哪些加权维度未达标"，更具驱动力；`--json` 时附带 `bench` 字段。
- `release` 预留 `--api-token` 接口：令牌接收后当前仍走人工导入（情报已预填），待 ClawHub 公开 publish 端点即升级为「真一键」。诚实标注阻塞点，不伪造调用。
- 测试 42 → **48**（新增 `--mode package` 含/不含清单、 `--bench` 输出与 `--json --bench` 结构、 `--api-token` 优雅降级）。

## [1.4.0] — 2026-09-23 · 系统化闭环（可组合输出 + 真实市场情报）

- `validate` 新增 `--json`：输出机器可读报告（`{path,mode,score,summary,items}`），可被 CI / 其他工具 / **市场闭环直接消费**，让工具从「给人看」升级为「可编排」。
- `gap` 新增 `--scan-json <file>`：消费 find-skills++ 导出的真实市场扫描数据，把"本机启发式"升级为「真实在售缺口」情报，激活 **find-skills++ 扫缺口 → scaffold → validate → release → 被检索推荐** 的飞轮护城河。
- **Dogfooding 闭环达成**：修复引用完整性误报（正文描述 `scripts/references/assets` 不再被当成真实引用路径）+ 补齐 `.github/workflows/ci.yml`，使 `python releaser.py validate --path .` 对自身达 **9/9 PASS、就绪分 100/100**，工具首次能「验证自己」满分。
- 测试 36 → **42**（新增 `--json` 结构校验、`--scan-json` 市场模式、`score=100` 自校验、递归守卫）。

## [1.3.0] — 2026-09-22 · 碾压级能力（gap 情报 + 就绪分 + 近一键发布）

- `validate` 新增 **0-100 发布就绪分**（加权 PASS/WARN/FAIL），并支持 `--mode skill|cli` 泛化到任意零依赖 CLI 项目。
- 新增 `gap` 子命令（★市场情报）：扫描本机技能按 8 大类目归类，报告空白类目（缺口）与单薄类目（可补强），并给出 `scaffold` 建议；预留接入 find-skills++ 市场数据形成闭环。
- `release` 升级为**近一键发布**：git 推送后自动构造 ClawHub 导入情报（解析仓库地址、预填 Display/Slug、按关键词归类推荐分类、Topics 自动截断 ≤48）；`--dry-run` 不推送只出情报。（诚实说明：最终 Publish 点击需用户登录会话。）
- 测试深度 5 → **36**（覆盖 validate 全分支 / score / gap / bump 三型 / selfcheck / inventory / release dry-run / cli 模式 / 纯函数）。
- 战略评测见 `STRATEGY-EVAL` 思路：竞品给文档，本工具替你执行 + 懂市场。

## [1.2.0] — 2026-09-22 · 工具中心化（参考 find-skills++ 模式）

- 新增零依赖主工具 `releaser.py`（7 子命令）：`validate`（主动扫描全部发布陷阱）、
  `inventory`（治理本机技能就绪度）、`selfcheck`（零依赖校验）、`scaffold`（委托现有 scaffold.py）、
  `bump`（升版本+CHANGELOG）、`release`（git 推送+ClawHub 指引）、`doctor`（自检/校验）。
- SKILL.md 重写为工具中心：散文降级为背景，releaser.py 子命令成为主体。
- 修复：bump 正则分组引用错误（\10）；selfcheck 跳过生成器模板（scaffold.py）避免误报。
- 新增 `LICENSE`（MIT-0）+ ASCII 版权名，补齐自身发布合规。
- 新增 `tests/test_releaser.py`（5 项，managed venv 全过）。

## [1.1.0] — 2026-09-21 · 脚手架 + 竞争力对齐

- 新增 `scaffold.py` 一键生成带 CI 的完整可发布骨架。
- 明确与 skill-creator 边界（写 vs 发）；补 2026 ClawHub 上架规则（MIT-0 / skill-card.md 冲突 / Topics≤48 / 账号龄）。
- 补 CI 失败诊断决策树。

## [1.0.0] — 2026-09-20 · 初版

- 固化 find-skills++（v5.3.0）真实发布工程经验：目录结构、sys.path、doctor 门、CI、LICENSE、排障 SOP。
