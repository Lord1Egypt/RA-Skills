# AI Weekly Report Skill

> 生成**可搜索、可筛选、支持暗色模式**的 AI 行业新闻单文件 HTML 网站的 Agent 技能。核心引擎为纯 Python（11 模块），零 Agent SDK 依赖，产物为单文件 HTML——可被任意框架复用。**单一跨平台 `SKILL.md`**（开放 Agent Skill 规范），Claude Code / OpenAI Codex / OpenCode / OpenClaw / Coze / WorkBuddy 通用，无需任何平台专属包装。

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/python-3.10%2B-green.svg)](https://www.python.org/)
[![AgentSkills](https://img.shields.io/badge/spec-AgentSkills-8A2BE2)](https://github.com/anthropics/skills)
[![Cross-Platform](https://img.shields.io/badge/platform-Claude%20Code%20%7C%20Codex%20%7C%20OpenClaw%20%7C%20Coze%20%7C%20WorkBuddy-10a37f)](./SKILL.md)

---

## 特性

- **自治优先**：新闻默认全部来自公开 RSS 抓取（14 个精选源：国内 7 + 国外 7，国内优先），**默认不调用任何付费/商业 API**（可选 NewsAPI 接入需自备 `NEWSAPI_KEY`，默认关闭）
- **单文件交付**：所有 CSS/JS 内联，Chart.js 也内联进 HTML，无外部文件依赖，可直接托管或分享
- **高可信度**：每条新闻附带原始报道 URL；市场 / 融资数据由 WebSearch 获取真实值后注入，未提供时明确标注「示例 / 估算」
- **排行榜自适应**：多源池（LMArena / Hugging Face / OpenCompass 司南 / SuperCLUE / ModelScope），实时失败自动回退快照 / 缓存，绝不空白
- **本周看点**：自动从新闻聚类生成洞察（关键词彩标 + 本周数字 + 三受众行动建议），服务端预渲染进静态 HTML，禁 JS 也可见
- **市场数据双源**：全球 + 中国市场规模 / 融资 4 图 2×2 布局，含趋势洞察 × 本周印证桥接
- **模型资料卡**：26+ 模型档案（成本 / 上下文 / 许可证 / 币种），以 `model_profiles.json` 为权威源
- **可定时**：支持每周自动生成最新版网站
- **安全加固**：RSS / CLI 不可信内容的注入面在**服务端 Python**与**客户端模板**两层分别防御——`<script>` 上下文 JSON 注入、URL 属性突破、属性内 JS 字符串、客户端 `${...}` 插值均按上下文转义 / 协议白名单处理
- **多后端部署**：`deploy.py` 统一入口支持 GitHub Pages / 腾讯云 COS / Vercel / Netlify / Cloudflare Pages / 本地 6 种托管，飞书卡片 `view_url` 与部署解耦，非 GitHub 后端完全不碰 GitHub
- **国内镜像自动回退**：LMArena / HuggingFace / Artificial Analysis 主源不可达时自动切换 hf-mirror 等国内镜像，再失败才回退快照（探活见 `scripts/leaderboard_diagnose.py`）
- **交互式飞书配置**：`scripts/init_feishu_config.py` 交互式生成连接器推送目标 `feishu_target.json`（格式校验），首次配置不再手写出错
- **错误提示人性化**：`ERR-*` 错误码体系 + `UserFacingError`，部署 / 推送失败给出含解决步骤的友好提示，不再丢裸 RuntimeError
- **硬约束集中声明**：单次抓取 ≤100 条新闻、每榜排行榜 ≤50 条模型、HTML ≤5 MB（`scripts/aiweekly/const.py` 统一常量 + `validate_checks/constraints.py` 事后审计）
- **独立 FAQ 文档**：`references/FAQ.md` 九节 + 排错速查表，覆盖安装 / 配置 / 网络 / 模型数据等常见坑
- **实时排行榜刷新更稳（R3/R4）**：慢源 LMArena/HF/AA 超时提额（60–75s）且整体墙钟上限放宽至 240s，减少因网络抖动导致的空榜；`scripts/install_scheduler.py` 把每日 09:00 刷新注册为 Windows 任务计划 / Linux cron，会话不在线也能刷新（WorkBuddy automation 仍作即时触发，系统调度仅兜底）

---

## 快速开始

```bash
# 1. 安装依赖（3 个运行依赖 feedparser / requests / beautifulsoup4 + pytest，版本均已钉）
python -m venv .venv && .venv/Scripts/pip install -r requirements.txt

# 2. 抓取本周 AI 新闻（RSS）
bash run_report.sh scripts/fetch_ai_news.py --output news.json

# 3. 生成单文件新闻网站
bash run_report.sh scripts/generate_site.py --api-json news.json -o AI_News.html

# 4. 校验产出
bash run_report.sh scripts/validate_report.py --html AI_News.html

# 5. 部署到 GitHub Pages（gh-pages 分支；飞书卡片的 view_url 即此地址）
bash run_report.sh deploy --html AI_News.html
#   默认仅本地提交、不推送；需推送请加 --push（--no-push 兼容旧调用）
#   部署后顺手把 Pages 源切到 gh-pages：加 --switch-pages（需 gh 凭据，见下文）
```

> **完整分发一步到位**：`publish.py` 在推送飞书卡片的同时可顺带部署周报——
> `bash run_report.sh scripts/publish.py --news-json news.json --insights-json insights.json --html AI_News.html --deploy`。

> **统一启动器 `run_report.sh`**：自动探测已安装依赖的 Python（优先复用 `aiweekly` 受管 venv，回退 `python3`/`python`），无需手动激活环境。支持 `--proxy` 出站代理（企业内网）、`--region` 区域探测、`--translate-en` 本地翻译、`--health-check` 健康检查等全部 CLI 参数透传。

---

## 架构

核心执行引擎（`scripts/`）为**纯 Python、零 Agent SDK 依赖**，产物为**单文件 HTML**。

```
ai-weekly/
├── SKILL.md                      # 单一跨平台入口（开放 Agent Skill 规范；Claude Code / Codex / OpenCode / OpenClaw / Coze / WorkBuddy 通用）
├── manifest.json                 # 通用框架接口描述（LangGraph / Dify / Coze 等）
├── run_report.sh                 # 统一启动器（自动探测 Python + venv，CLI 参数透传）
├── requirements.txt              # 运行依赖 3 个（feedparser / requests / beautifulsoup4）+ pytest（开发/CI）；均已钉版本
├── README.md
├── LICENSE
├── .gitignore
├── .github/workflows/mirror.yml  # 每日 CI：抓取榜源 + 生成周报站，发布到 GitHub Pages
├── scripts/
│   ├── fetch_ai_news.py          # RSS 抓取 → news.json（14 源 + 时间窗口过滤）
│   ├── generate_site.py          # 生成单文件 HTML 网站（含排行榜 / 市场 / 看点 / 翻译）
│   ├── validate_report.py        # 产出校验（结构 / ISO8601 / 体量 / 看点 / 市场 / XSS 守护）
│   ├── deploy_report.py          # 部署辅助（提取摘要 + 框架无关通知文本）
│   ├── build_pages_site.py       # CI 专用：组装 Pages 站点（榜镜像 + 周报 HTML + 往周数据源 JSON）
│   └── aiweekly/                 # 内部 Python 包（11 模块）
│       ├── __init__.py           # 包入口 + 公开 API
│       ├── news.py               # RSS 抓取 / 解析 / 分类 / 去重
│       ├── leaderboard.py        # 排行榜合并 / 资料卡权威覆盖（P0#13）
│       ├── leaderboard_sources.py# 多源池抓取（LMArena / HF / OpenCompass / SuperCLUE / ModelScope）
│       ├── insights.py           # 本周看点 / 关键词聚类 / 受众摘要
│       ├── market.py             # 市场 / 融资图表数据（全球 + 中国双源）
│       ├── render.py             # HTML 渲染 + XSS 安全序列化
│       ├── translate.py          # 英文报道中文总结（本地 Ollama）
│       ├── utils.py              # HTTP 重试退避 / 出站代理 / 区域探测 / ISO8601 日期
│       ├── model_meta.py         # 模型元数据查找（成本 / 上下文 / 许可证）
│       └── types.py              # TypedDict 类型定义
├── delivery/                    # 飞书推送（周报分发，P0）
│   ├── feishu_bot.py            # 卡片构造库（build_headline_card，纯卡片 schema）；连接器复用
│   ├── feishu_connector.py      # 飞书连接器直推 CLI（lark-cli，密钥不落盘，复用前者卡片构造）
│   └── feishu_target.json       # 连接器推送目标（gitignore，不入库）
├── assets/
│   └── news_site_template.html   # 单文件 HTML 模板（含内联 Chart.js + safeUrl 守卫）
├── tools/                        # 独立辅助工具（不进入主生成流程）
│   └── accumulate_data.py        # 历史数据累积器（WoY/YoY 环比，可选工具）
├── references/                   # 数据源与报告结构参考文档
├── docs/
│   └── agent-skill-format-landscape.md  # （本地开发参考，已 gitignore，不随仓库发布）
├── data/                         # 本地运行时数据（feed 健康/历史缓存）；gitignore，不入库
├── model_profiles.json           # 模型档案（排行榜描述字段唯一权威源）
└── models_cost.json              # 模型成本兜底数据
```

> 运行时产物（`news.json` / `insights.json` / `leaderboard_cache.json` / `AI_News_*.html` 等）已被 `.gitignore` 排除，不会入库；仓库只保留可复现的源码与参考配置。

---

## 本地数据与首次使用说明

ai-weekly 的**排行榜、市场分析**等展示「实时数据 / 趋势」的模块，依赖**本地累积的历史快照**（如 `snapshots/` 下的周度榜单快照、`data/` 下的趋势累积数据）。

这些历史数据**只在你运行生成时于本地产生**，且只能捕捉**最近**的数据窗口——它们**不会、也不应**随仓库分发（本就属于个人运行产物，已加入 `.gitignore`）。

**⚠️ 首次安装请注意**：头几周生成的报告里，上述模块的「趋势线 / 环比（WoW）变化」会显示为**空白**，这是正常现象、**并非 Bug**。随着你每周持续运行（本地累积 2 周以上快照后），趋势线会自动填充。

> 若希望首次即可看到历史趋势，可手动放入近期快照文件，或先连续运行几周累积本地数据。

---

## GitHub Pages 公开站点（在线 demo）

周报通过 `scripts/deploy_ghpages.py` 部署到 **`gh-pages` 分支根目录**，飞书卡片里的 `view_url`（`https://<owner>.github.io/<repo>/AI_News_<date>.html`）即指向这里。部署是**本地流水线的一步**（不是 CI），结构如下：

```
gh-pages 分支（Pages 源 = Deploy from a branch: gh-pages / /root）
├── AI_News_2026-08-17.html   # 当期周报（根路径直达）
├── AI_News_<更早日期>.html   # 历史周报（累加保留）
└── index.html                # 自动生成的存档页（列出所有期，最新高亮）
```

发布方式（`run_report.sh deploy` 即封装此脚本）：
```bash
bash run_report.sh deploy --html AI_News.html
#   --push           推送（默认不推送，仅本地生成+提交）；--no-push 兼容旧调用
#   --switch-pages   部署后通过 GitHub API 把 Pages 源切到 gh-pages / /root（需 gh 凭据）
#   --dry-run        只做 worktree+复制+index 预览，不提交不推送
```

### 首次启用（一次性）
1. 把 `gh-pages` 分支推送到远端：`git push origin gh-pages`（已推过可跳过）。
2. 把 GitHub Pages **源**切到 `gh-pages / /root`（二选一）：
   - **手动**：仓库 **Settings → Pages → Source** 选 **Deploy from a branch → `gh-pages` / `/root`** → Save。
   - **自动（可选，需凭据）**：跑 `bash scripts/setup_pages_source.sh`。该脚本走 GitHub REST API，需要一个**能修改该仓库 Pages 设置**的凭据——优先复用 `gh` CLI 已登录的凭据（凭据由 gh 自己保管，**不落项目文件**）：
     ```bash
     gh auth login          # 首次登录；已登录可跳过
     bash scripts/setup_pages_source.sh
     ```
     > 若确实需要用 PAT：请使用**仅限该仓库、仅含必需权限、尽量短的有效期**的令牌，通过环境变量传入，**不要落盘**。
     > **不要**再把长期 PAT 写进仓库目录下的 `.github_token`（旧版本曾这样建议，**已废弃**）：长期、宽权限的令牌落在工作目录里，一旦目录被同步、备份或打包，就等于把仓库写权限一起带走。
3. 等待约 1 分钟，访问 `https://<owner>.github.io/<repo>/AI_News_<date>.html` 验证不再 404。

> **为什么是 gh-pages 分支而非 CI artifact？** 飞书卡片的 `view_url` 直接指向分支根目录的 `AI_News_*.html`，与「Deploy from a branch」模型天然契合；GitHub Pages 只允许单一来源，故原先的 `.github/workflows/mirror.yml`（Actions artifact 部署）已停用（`if: false`），以免两种来源互斥导致部署失败。

### 已知限制
- **中文翻译**：若需公开站点也带中文总结，请在**本地**生成时加 `--translate-en`（依赖本机 Ollama），再 `run_report.sh deploy` 推上去。
- **数据新鲜度**：周报新闻窗口为「最近 7 天滚动」（RSS 仅保留约 1 周），要保留某周需在该周仍处保留期内至少部署一次。
- **硬约束**：单次抓取 ≤100 条新闻、每榜排行榜 ≤50 条模型、HTML ≤5 MB（超限自动压缩）、趋势线需 ≥2 周数据。详见 [SKILL.md 第二节.5](SKILL.md#二5硬约束必须遵守的边界)。

### 排错：gh-pages 部署 / 推送常见坑

- **飞书 `view_url` 打开 404**：先确认 Pages **源**已切到 `gh-pages / /root`（Settings → Pages → Source）。若已切源仍 404，多半是 `deploy_ghpages.py` 的 `git push` 没推上云——本地已 commit 但远端还是旧版本。用 `curl -I https://<owner>.github.io/<repo>/AI_News_<date>.html` 验证 HTTP 状态。
- **`git push` 报 `invalid credentials` / 卡死超时**：这是**认证方式**问题，**不等于 token 无效**（可用 `curl -H "Authorization: Bearer <token>" https://api.github.com/user` 验证 token 本身有效）。
  - ❌ 不要走 `http.extraheader=AUTHORIZATION: Bearer <token>`：`Bearer` 只对 GitHub **REST API** 有效；git 推送走 **git smart HTTP** 协议，只认 **Basic** 认证，会被拒。
  - ❌ 不要依赖 Windows `wincred` 凭据助手：无交互 tty 的环境（CI / 沙箱 / 定时自动化）会卡在用户名提示导致超时。
  - ✅ **首选（零凭据文件）**：用 `gh` 的 git 凭据助手——`gh auth login`（已登录可跳过）后执行 `gh auth setup-git`，让 git 走 gh 托管的凭据。**项目目录里不再需要任何 token 文件**。
  - ✅ 次选（自动化/CI 场景）：通过环境变量 `GITHUB_TOKEN` / `GH_TOKEN` 一次性传入**短期**令牌，`deploy_ghpages.py` 会注入 `Authorization` 头（仅内存，不落盘）。
  - ⚠️ **已废弃**：把 PAT 写入仓库目录下的 `.github_token`。长期凭据落在工作目录里，目录一旦被同步/备份/打包，即连同仓库写权限一起泄露。
- **`setup_pages_source.sh` 切源报 403 / 404**：多为令牌类型或权限范围不匹配。**最省事的规避方式是直接手动切源**（Settings → Pages → Source，一次性操作、零凭据）；若必须走 API，请确认所用凭据对该仓库具备修改 Pages 设置的权限，并以 GitHub 官方文档为准。

---

## 跨框架兼容性

核心执行引擎**不依赖任何 Agent SDK**，产物为**单文件 HTML**——可被任意 Agent 框架当作普通脚本 + 普通文件复用。

**单一跨平台 `SKILL.md` 即全部入口。** 本技能遵循 Anthropic 首创、已被 OpenClaw / Coze / OpenAI Codex 等广泛采纳的开放 `SKILL.md` 规范。把技能目录放入支持该规范的任意 Agent 即可加载，无需 `plugin.json` 或任何 per-agent 副本。

| 形态 / 平台 | 入口文件 | 状态 |
|---|---|---|
| **Claude Code / Claude.ai** | `SKILL.md`（根） | ✅ 原生读取 |
| **OpenAI Codex CLI** | `SKILL.md`（根） | ✅ 直接读取 |
| **OpenCode** | `SKILL.md`（根） | ✅ 原生 |
| **OpenClaw / ClawHub / 天禧AI** | `SKILL.md`（根） | ✅ 直接读取 |
| **Coze（字节跳动）** | `SKILL.md`（根） | ✅ 兼容（可手动导入） |
| **GitHub Copilot Skills** | `SKILL.md`（`.github/skills/` 或 `~/.copilot/skills/`） | ✅ 兼容（放入对应目录即可） |
| **WorkBuddy** | `SKILL.md`（根） | ✅ 原生 frontmatter |
| **通用框架（Dify / LangGraph 等）** | `manifest.json` | ✅ 引擎接口描述 |

- **引擎层零耦合（可复核）**：以下 grep 应无任何命中：
  ```bash
  grep -rn "import workbuddy\|from workbuddy\|skill_executor" scripts/ || echo "零耦合 ✅"
  ```
- **依赖白名单**：`requirements.txt` 仅 3 个纯标准第三方库——`feedparser` / `requests` / `beautifulsoup4`（另含 `pytest`，仅供开发与 CI 测试，不影响运行）；无闭源 SDK、无云端强依赖，任何框架可 `pip install` 后直接运行；**所有版本均已钉死**，避免上游静默升级引入回归
- **产物框架无关**：`generate_site.py` 输出**单文件 HTML**（CSS/JS/Chart.js 全部内联），不依赖任何 Agent 运行时，可被任意 Agent 返回给用户或托管到静态站点

### 能力分级：核心（全框架通用）vs 框架增强（依赖具体环境）

| 类别 | 能力 | 入口 | 依赖 |
|---|---|---|---|
| **核心** | RSS 新闻抓取 | `fetch_ai_news.py` | `feedparser` + 外网 |
| **核心** | 单文件 HTML 生成（含排行榜 / 市场 / 看点） | `generate_site.py` | `requests` / `bs4` |
| **核心** | 产出校验（6 项守护） | `validate_report.py` | 无 |
| **框架增强** | 英文报道中文总结 | `generate_site.py --translate-en` | 本机 Ollama（`AIWEEKLY_OLLAMA_URL` + 模型） |
| **框架增强** | 摘要提取 / 通知文本 | `deploy_report.py` | 无（纯文本拼装，推送由调用方实现） |
| **框架增强** | 飞书头条卡片推送 | `publish.py`（经 `delivery/feishu_connector.py` 走 lark-cli 发送） | 已连接的飞书连接器（lark-cli，密钥不落盘） |
| **框架增强** | 出站代理（企业内网）+ 区域探测 | `generate_site.py --proxy / --region` | PySocks（SOCKS 代理时可选） |
| **框架增强** | 健康检查 | `generate_site.py --health-check` | 无（聚合所有源可达性 + 退出码） |

> **要点**：核心链路 `fetch_ai_news.py → generate_site.py → validate_report.py` **不依赖任何 Agent SDK**，任何框架直接调用即可。`--translate-en` / `--proxy` / `--health-check` 等增强参数跳过也不影响核心产出。

---

## 校验

`validate_report.py` 对生成的 HTML 运行 6 项守护：

| 守护项 | 检查内容 |
|---|---|
| 结构完整性 | `<script>`, `</script>`, `</html>` 存在 |
| 新闻体量 | ≥ 20 条新闻（10–19 条降级为警告而非失败） |
| ISO 8601 日期 | 所有 `publishedAt` 格式正确 |
| 本周看点 | `.insight-card`, `.kw-tag`, `.audience-card` 均存在 |
| 市场图表 | 6 组 Chart.js canvas（含中国数据图） |
| 合作桥接 | `.trend-evidence` 趋势印证行存在 |

阈值通过命令行参数调整：`--min-news`（默认 20）、`--min-coverage`（默认 80）、`--min-ranking`（默认 5）；加 `--strict` 可让警告项也算不通过。

---

## 安全

本技能经过对抗式代码审查，并修复了 RSS / CLI 不可信内容导致的注入类缺陷（审查记录为发布者本地文档，不随包分发）：

- **H1 存储型 XSS（`<script>` 上下文 JSON 注入）**：`render.py` 用 `_json_script_safe()` 把序列化结果中的 `<` `>` `&` 转义为 `\u003c`/`\u003e`/`\u0026`，阻止 `</script>` 突破脚本块。**已覆盖的 JSON 占位符**：`NEWS_DATA` / `LEADERBOARD_DATA` / `INSIGHTS_DATA` / `AUDIENCE_SUMMARY` / `KEYWORD_SEARCH_SOURCES`
- **H2 URL 属性突破 + 危险协议**：仅放行 `http(s):` / `mailto:`，`javascript:` / `data:` 回退 `#`。服务端渲染的 `href` 统一经 `utils.safe_href()`（协议白名单 + `html.escape(quote=True)`）；浏览器侧另有模板 `safeUrl()`
- **H3 HTML 属性内的 JS 字符串**：`onclick="switchAudience('…')"` 这类上下文需**两层**转义（JS 层转义 `\` / `'` / 换行，再加 HTML 层 `quote=True`）——仅 `html.escape` 无效，因为浏览器会先做实体解码再把结果交给 JS 解析。统一走 `utils.js_str_in_attr()`
- **H4 客户端模板插值面（`assets/news_site_template.html`）**：`renderInsights()` 会在运行时用 `innerHTML` 覆盖服务端预渲染的同一容器，而客户端模板字面量对不可信字段原为**零转义**——这会让服务端修复在启用 JS 的浏览器上被绕过。现客户端全部 `${...}` 插值按上下文补齐：文本 / 属性走 `escapeHtml`、属性内 JS 字符串走 `jsStrInAttr`（等价于服务端 `utils.js_str_in_attr`）、`href` 与 `setHref()` 走模板 `safeUrl()`。该文件是纯客户端 JS、pytest 无法执行其中的逻辑，故其防护由**静态断言闸门**（对模板文本做正则校验）守护
- **M1–M2 CLI 可控文本转义**：`--market-source` 系列（`[MARKET_SOURCE]` / `[FUNDING_SOURCE]` / `[CN_*_SOURCE]` 及其汇总与页脚）、外部源、`LEAD`、关键词均经 `html.escape`；JS 字符串上下文走 `_js_str()`
- **M3 TLS 证书校验**：`utils._build_opener()` 校验证书链与主机名。企业 TLS 拦截场景的正确做法是把代理根证书装入系统信任库（或指向 `SSL_CERT_FILE`），而非关闭校验

> 上述修复通过恶意 payload（`</script><img onerror=...>`、`javascript:alert(1)`、`'` 闭合 JS 字符串、`"` 闭合属性）注入回归测试验证，并做了改动前后整页渲染等价性比对。**服务端 Python 侧为可执行的行为测试；客户端模板侧因 pytest 无法执行其 JS，为静态断言闸门（正则校验模板文本），二者覆盖范围不同、不可互相替代。**

---

## 可选外部增强（合规说明）

本技能**默认完全自治**，不调用任何付费/商业 API（可选 NewsAPI 接入需自备 `NEWSAPI_KEY`，且默认关闭）。

若希望用 AI HOT 等「AI 行业知识类」外部 API 增强可信度，请**自行**获取数据并导出 JSON，以 `--external-news-json` 注入；页脚会自动署名。是否启用完全由你决定，并须遵守对应服务条款、自行承担合规风险。使用任何第三方 API 时请保留其署名与授权。

> **AI HOT 停服提醒**：其 legacy `/api/public/*` 接口已按官方 openapi 明示于 **2026-10-31 停止服务**（原定 12-31，提前至 9-30 公告），域名已 301 到 `aihot.news`。
> v1（`/api/v1/*`）是完全不同的形态：端点从 9 个扩到 33 个，新增 `weeklies` / `monthlies` / `stories/{id}` / `agent/*` 等 12 个 Agent 专用端点；参数 `take` → `limit`、`since` → `window`、另有 `by`。
> 照着 legacy 形态写的脚本切到 v1 **不会抛异常**，而是拿到 `400 {"detail":"Unknown query parameter: take."}` —— 静默失败、取数为空。取数前请先对照目标 API 的 openapi 确认参数名。

---

## 飞书头条卡片推送（可选）

生成报告后，可把**本周头条速览**以飞书消息卡片推送到群 / 私聊，让情报在"工作者已在用的地方"被消费。卡片由 `delivery/feishu_bot.build_headline_card` 构造，经 **飞书连接器**（lark-cli，密钥由连接器托管、绝不落配置文件）发送——`publish.py` 组装 `report.json` 后自动经连接器推送。

> ⚠️ **一次流水线只推一次（防重复）**：`publish.py` 组装 `report.json` 后**默认就会**经连接器推送一张卡片（只要解析到目标，即 `--chat-id/--user-id` > 环境变量 > `delivery/feishu_target.json`；未解析到目标则仅警告、exit 0 不阻断）。`delivery/feishu_connector.py` 的独立 CLI 只是 **publish.py 的等价替代入口**——两者发的是**同一张**卡片，**只能二选一，切勿在同一任务里两个都跑**，否则同一张周报会发两次（重复卡片）。二者都只推一次、无重试：`publish.py` 仅在其内部那一次调用里发送，`feishu_connector.py` 的 `main()` 也仅调用一次 `send_card()`。

> 🔒 **部署 / 刷新 / 调度同样「显式才执行、默认不推送」**：`deploy_ghpages.py`、`deploy.py`（`publish.py --deploy` 分发入口）、`refresh_deploy.py` 默认都只本地提交、**不推送** gh-pages（`refresh_deploy.py` / `deploy.py` 需显式 `--push` 才推）；`install_scheduler.py` 注册的定时任务**默认仅本地刷新、永不自动推送**，仅 `--enable-push` 才允许定时自动推送。报告生成流程不会自动触发其中任何一项。

```bash
# 组装 report.json 并经飞书连接器推送到群（bot 身份）
bash run_report.sh scripts/publish.py \
  --news-json news.json --audience-json audience_summary.json \
  --output report.json --chat-id oc_xxxx

# 推给自己（user 身份 → 私聊，首次冒烟测试最省心）
bash run_report.sh scripts/publish.py \
  --news-json news.json --output report.json --user-id ou_xxxx --as user
```

推送目标解析优先级：`--chat-id/--user-id` > 环境变量 `FEISHU_CHAT_ID/FEISHU_USER_ID` > `delivery/feishu_target.json`（格式 `{"chat_id":"oc_xxx"}` 或 `{"user_id":"ou_xxx"}`）。发送仅依赖标准库 + 已连接的飞书连接器（lark-cli），无需 `requests`，webhook token 不落仓库。首推 `scripts/init_feishu_config.py` 生成目标配置，无需手写出错。

> 卡片内容：本周主线 + 🔥本周重点（Top5）+ 💡本周看点（Top3）+ 👥分角色摘要 + 🔖关键词 + 「查看完整周报」按钮（链接自动追加 `?src=feishu&uid=<uid>` 度量参数）。

---

## 相关文档

- [SKILL.md](SKILL.md) — 完整技能说明（含文件清单 §10.1 / §10.2）
- [references/FAQ.md](references/FAQ.md) — 常见问题集中解答（安装配置 / 飞书推送 / GitHub Pages / 网络）
- [references/data_sources.md](references/data_sources.md) — 备用与候选数据源清单
- [references/report_structure.md](references/report_structure.md) — 报告结构参考

> 发布者本地另有对抗式审查记录与优化方案文档，因**不随包分发**（见 `SKILL.md` §10.2），此处不再链接，避免发行包内出现死链。

---

## 内容标识与免责

- **AIGC 标识**：生成的 HTML 报告**页脚固定展示「本报告由 AI 辅助编制」标识**（依据《生成式人工智能服务管理暂行办法》第十二条对生成内容标识的要求）。**转载或二次分发时请保留该标识，不要移除**。
- **不构成投资建议**：报告中的市场规模、融资额度、公司估值、模型成本等均为公开来源的**静态快照或折算估算**，仅供参考，**不构成任何投资建议**；投资决策请以官方公告为准。
- **数据准确性**：每条新闻均附原始报道链接，请以原始来源为准；榜单为实时抓取或**标注日期的快照**，不冒充实时。

---

## 许可

[MIT](./LICENSE) © 2026 Elisabeth15501
