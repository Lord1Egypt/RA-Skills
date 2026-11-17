# Changelog

本项目所有重要变更记录于此。格式参考 [Keep a Changelog](https://keepachangelog.com/)，版本号遵循 [语义化版本](https://semver.org/)。

> 版本策略：技能尚不完善，当前版本 `0.1.1`；未发布变更记于 [Unreleased]，是否切版由维护者决定（见 `docs/RELEASING.md`）。

## [Unreleased]

### Changed

- **发布流程改为仓库内自持**：`publish.yml` 原先 `uses: cgartlab/cgartlab-skills/.github/workflows/publish-skill.yml@main` 复用发布逻辑，仓库转为 public 后，public 仓库无法调用 private 仓库的 reusable workflow，`gh workflow run publish.yml` 直接报 `workflow was not found`，registry 发布整条链路静默失效。现把 ClawHub / SkillHub 的发布逻辑内联为 `.github/actions/publish/action.yml`，由 `release.yml` 创建 Release 后用 `needs:` 直接串起发布（`GITHUB_TOKEN` 创建的 Release 不会触发其它 workflow，事件接力本就不可靠），`publish.yml` 降级为纯手动重发入口。
- **`scripts/gate.sh` 增加 [5/5] 步骤**：解析 `.github/workflows/*.yml` 与 `.github/actions/*/action.yml`（composite 的每个 step 必须显式写 `shell`），把 YAML 缩进/键名错误挡在 push 之前；PyYAML 缺失时降级为 warn。

（空的 `[Unreleased]` 是 `docs/RELEASING.md` 发布流程的约定：每次发版后在其上方新开一个空章节，因此这里保留标题而不是删掉。）

## [0.1.1] - 2026-10-23

### Added

- **`zhihu` 后端从占位变为可用**（`scripts/search.mjs`）：接入知乎官方 OpenAPI **Global Search**（`GET https://developer.zhihu.com/api/v1/content/global_search`，Bearer + `X-Request-Timestamp`）。检索范围为**全网公开内容**而非仅 zhihu.com，对中文主题表现好。参数为 PascalCase（`Query` / `Count` / `Filter` / `SearchDB`），`Count` 服务端限制 1-20，适配器本地同样截断以保证 `--limit` 诚实；`--news` 映射为 `SearchDB=realtime`。`published` 取自 `EditTime`（**编辑时间**，不是发布时间），`score` 取自 `RankingScore`。
- **`tencent` 后端从占位变为可用**（`scripts/search.mjs`）：接入腾讯新闻官方 **`tencent-news-cli`**（Go 二进制，非 HTTP API）。`search <关键词>` 走关键词搜索，`hot` 走热点榜（**仅当没有关键词时**使用；`--news` 不改变检索方式），`--limit` 本地截断到 1-50。因 CLI **没有 `--json` / `--format`**（实测 v1.0.17），适配器解析其文本输出；标题行带 `N. ` 序号前缀而其余字段为缩进，这是解析的关键差异点。
- `references/backends.md` 为两个后端补齐完整规格：认证方式、参数表、返回字段、输出文本格式、失败分支，以及 Tencent 安装的**已知安装器 bug**（`setup.ps1` 经 `pwsh` 调用时 `checksums.txt` 被当作单个字符串，导致 `No matching checksum` 误报，需手动校验 SHA-256 安装）。

### Changed

- `SKILL.md`：`description` 去掉 “pending Tencent News/Zhihu”，路由表补 `tencent`（热点榜 / 中文新闻搜索）与 `zhihu`（中文全网）入口，Backend status 段改为 2026-10-20 实测结果。
- **`tencent` 的密钥归属特殊**：key 由 `tencent-news-cli apikey-set` 持久化到 CLI 自身配置（Windows 为 `HKCU\Environment`），**不读 `secrets.json`**；`TENCENT_NEWS_KEY` / `tencent_news_key` 两个槽位保留但未使用，文档已注明。

### Fixed

- **`tencent` 二进制解析**：适配器原来只按裸命令名 `tencent-news-cli` 查找，而官方安装器把二进制放进 `~/.tencent-news-cli/bin/` 且**不修改 `PATH`**，已装好的机器上仍报 “not found”。现按 `TENCENT_NEWS_CLI_PATH` → `PATH` → 安装器默认目录 顺序解析，并在报错里列出已尝试的路径。
- **`tencent "关键词" --news` 丢弃关键词**：原逻辑把 `--news` 映射到 `hot`（热点榜），带关键词查询会返回与查询无关的头条。现仅当关键词为空时走 `hot`；`--news` 不再改变检索方式（该后端结果本就全是 `type=news`）。`references/backends.md` 的映射表同步更正。
- **`scripts/search.sh` 的 `tencent` / `zhihu` 仍是 “not configured” 占位**，与 `search.mjs` 不一致：按同一规格补齐实现（zhihu 走 `/content/global_search`，`Count` 本地截断 1-20；tencent 调官方 CLI，`--limit` 截断 1-50，含无关键词热点榜）。
- **`search.sh` 在本机全后端静默返回空**：脚本一律调 `python3`，而 Windows 上该命令可能是 Microsoft Store 别名存根（exit 0、无输出）。现探测 `$PYTHON` → `python3` → `python` 并**验证真实输出**（`print(1)` 必须等于 `1`），无可用解释器时输出明确错误。
- **`search.sh` 读不到 `secrets.json`**：路径以 MSYS 形式（`/d/...`）传给 Windows 原生 Python，触发 `FileNotFoundError`。改为经 **stdin** 传入 JSON；同时去掉 `shlex.quote`——它会把字面单引号塞进 `Authorization` 等请求头。
- **`zhihu` / `so` 的时间戳弃用告警**：`datetime.utcfromtimestamp` 在 Python 3.14 已弃用并往 stderr 打 `DeprecationWarning`；改为 timezone-aware，输出与 `search.mjs` 一致的 `...Z` 形式。

## [0.1.0] - 2026-10-02

> **一句话概括**：这是首次公开发布，一次性并入自内部初版以来的全部工作——9 个搜索后端、路由策略、双实现调度脚本、密钥管理与 8 条评测用例。**你不需要做任何事**；需要 `brave` / `exa` 的话另行填入 `secrets.json`（见 `secrets.example.json`）。

首次发布（此前未对外发布过任何版本，本次涵盖自内部初版以来的全部工作）。

### Added

- **9 个搜索后端**（`references/backends.md`）：`bing`（cn.bing.com RSS 通用网页搜索）、`context7`（库/框架/API 文档两步检索）、`qqnews`（腾讯新闻热榜 JSON）、`hupu`（虎扑足球新闻列表）、`so`（Stack Overflow 问答）、`github`（仓库搜索）、`hn`（Hacker News）、`brave`（通用网页/新闻，需 key）、`exa`（深度语义检索，需 key）。前 7 个免密钥，可经 `web_fetch` 在受限出口环境使用。
- **路由策略**（`references/routing.md`）：按意图分流的双列路由表（curl harness / DSH web_fetch），含查询改写规则（长时效句改关键词、紧复合形式重试）、数字与行情两步法、故障范围判定、诚实降级规则。
- **双实现调度脚本**：`scripts/search.mjs`（零依赖 Node ESM，11 个后端适配器，输出归一化 JSON）与 `scripts/search.sh`（curl + python3 等价实现）。
- **密钥管理**：`secrets.example.json` 模板 + `.gitignore` 屏蔽真实 `secrets.json`（实测 `git check-ignore` 命中）；环境变量优先、文件回退。
- **实测记录**：`web_fetch` 主机可达性地图（区分可达 / JS 截断 / 不可达三类）、知乎 API 403 反爬、Bing `site:` 兜底在中文长句下坍缩为词条定义等实证案例。
- **评测用例**：`evals/evals.json` 8 条（文档检索、热点新闻、足球新闻、知乎降级诚实性、数据两步法、跨域广研等）。
- **仓库治理**：`.gitattributes`（LF 归一）、`LICENSE`（CC BY-NC-SA 4.0）、`docs/RELEASING.md`（发布流程与三道闸）、`CHANGELOG.md` 本文件。

### Changed

- `SKILL.md` frontmatter 增加 `license` 与 `metadata`（`version` / `date` / `reference`）——Agent Skill 的版本源就在此处。
- `README.md` 增加「发布与版本」章节，指向版本源与变更记录。

### Fixed
- **SKILL.md frontmatter 的 `description` 是非法 YAML**（值里 `Backends: Brave/Exa` 的 ASCII
  冒号+空格让纯标量被解析成嵌套映射）：DSH 自带的 `yaml` 解析器与 `js-yaml` 双双报错，
  而 DSH 的 skill-filesystem 对解析失败的 skill 直接忽略（`parseSkillFile` 的 warn 分支）——
  skill 可能因此不被加载。对照组 `attention`/`quill` 的 frontmatter 两解析器均通过。
  现改为单引号标量（值内撇号双写），解析后内容与修复前逐字一致（815 字符）。

- **`secrets.json` 解析路径错误**（`scripts/search.mjs` 与 `scripts/search.sh`）：文件实际位于技能根目录（`SKILL.md` 旁，与 `references/backends.md` 的说明一致），但两个脚本都在 `scripts/` 子目录下查找，导致 `brave` / `exa` / `context7` / `tencent` / `zhihu` 等需密钥的后端永远返回 `missing key`（异常被静默吞掉，退化为仅环境变量模式）。现改为按 `scripts/secrets.json` → `../secrets.json` 顺序探测，两个位置均可，环境变量优先级不变。免密钥后端不受影响。

**已知限制**（详见 `references/backends.md` 的可达性地图；不单列非标准章节）

- `brave` / `exa` 需密钥，且在当前受限出口环境不可达，仅在带 shell 网络的 harness 可用。
- `tencent`（官方腾讯新闻 API）与 `zhihu` 端点尚未配置，返回 `not configured` 并走降级路径。