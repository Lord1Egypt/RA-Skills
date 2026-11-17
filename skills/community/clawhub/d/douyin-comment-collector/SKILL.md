---
slug: douyin-comment-collector
name: douyin-comment-collector
displayName: 抖音评论采集·主页作品抓取
version: 1.4.0
description: "抖音数据采集技能（评论采集 + 账号主页作品抓取）。① 评论：手上有抖音视频完整 URL、短链 v.douyin.com 转发链接或数字 aweme_id，想把评论抓下来做舆情/选题/复盘/词频统计时使用；② 主页作品：给定账号主页 URL / 短链 / sec_uid，抓取该账号发布的作品标题（desc）与发布时间（create_time），支持 --since/--until 本地时间区间过滤，正是「拉取指定账号在指定时间发布内容的标题和时间」场景。评论提供两条路径：无头浏览器游客态（免登录）与纯 Python 签名(a_bogus)+mssdk 真 msToken 创作者接口（需本人 cookie）；主页作品用浏览器拦截 aweme/post 接口，支持 --since/--until 时间过滤与 --analyze 按天分布统计。统一入口 douyin.py 一键路由评论/作品两个子命令。支持可选 jieba 词频分析；全自包含、可独立安装。不适用于快手/小红书/视频号等其他平台（那是别的技能），也不绕过登录做越权抓取——仅采集你有权访问的公开数据。"
agent_created: true
---
# 抖音评论采集

> **结论先行（务必告诉使用技能的人）**：
> - **建议登录后抓取**。不登录（游客态）抖音会弹「评论墙」，**只能拿到前 ~14-20 条样本评论**；登录后注入 cookie 通常能越过评论墙、拿到更多甚至全部。
> - **取 cookie 不用开控制台**：普通人运行 `login_helper.py` 即可——看得见浏览器扫码/账号密码登录，自动存 cookie，零开发者工具操作。
>
> 两条采集路径，按"有无 cookie"二选一：
> - **无 cookie / 想免登录** → 加 `--browser`：真实 Chromium 游客态打开视频页，自动翻页抓评论（实测可用，但抖音对游客有评论墙，通常抓到前 ~14-20 条）。
> - **有本人 cookie** → 默认 HTTP 创作者接口：账号授权通道，不受环境指纹风控，可抓全部评论（最稳）。

## 何时用
- 给定抖音视频的**完整 URL**、**短链转发链接**（`v.douyin.com/xxx/`）或直接给 **aweme_id**，要把评论抓下来。
- **不想登录 / 没有 cookie** → 用 `--browser` 无头浏览器游客态方案（推荐）。
- 有本人 cookie、要抓**全部**评论 → 用默认纯 Python 签名 HTTP 创作者接口（最稳）。
- 抓完后还想做**中文词频分析**：jieba 分词 + 停用词过滤（可选功能）。

### 账号主页作品抓取（`fetch_posts.py`）
- 给定抖音**账号主页 URL**（`https://www.douyin.com/user/<sec_uid>`）、**短链转发链接**或纯 **sec_uid**（`MS4wLj...`），要抓该账号发布的**作品标题 + 发布时间**。
- 典型场景：拉取**指定账号在指定时间段**发布内容的标题和时间（配合 `--since` / `--until` 本地时间窗口过滤）。
- 输出字段：`aweme_id`、`desc`（标题）、`create_time`（时间戳）、`publish_time`（可读时间，+8 时区）、`type`、`video_url`；加 `--with-stats` 附带点赞/评论/分享/收藏/播放量；加 `--analyze` 输出按天作品数分布（`daily_distribution`）。

## 核心约束（先读，避免误判）
1. **账号域隔离**：创作者中心评论接口必须用**目标视频发布账号本人**的 cookie 调用，否则返回 `status_code:5`。cookie 通过 `--cookie` 或环境变量 `DOUYIN_COOKIE` 传入。任何人装上技能后填**自己的** cookie + **自己的**视频链接即可使用；抓别人视频需对方本人 cookie。
2. **公开接口已加固（纯 HTTP 免登录不可行）**：`www.douyin.com/aweme/v1/web/comment/list/`（aid=6383）自 ~2026-08-20 起对非真实浏览器**静默空体**——实测：零 cookie 打该接口返回 HTTP 200 但响应体为空（`body=''`）。结论：**纯 HTTP 免登录方案当前抓不到公开评论**（全链路零 cookie 都通，唯独服务端空体）。`--guest` 开关即为此验证场景预留，跑出来空体属预期。
3. **无头浏览器可免登录，但有评论墙**： `--browser` 用真实 Chromium 游客态打开视频页（绕过空体风控），实测能抓到真实评论；但抖音对游客有评论墙，滚到第 3 页左右（前 ~14-20 条）后不再加载更多（页面显示"请先登录后发表评论"）。**要抓全部评论仍需本人 cookie + 创作者接口**。一次一个作品、只需部分样本时，浏览器方案足够。
4. **a_bogus 是逆向算法**：抖音改签名即失效 → 表现为 `status_code!=0` / 空响应体。纯 HTTP 路线此时不可用，需等算法更新或换浏览器方案。脚本会明确报错，不会静默吐空。

## 目录结构（全部自包含，不依赖本机其它代码）
```
抖音评论采集/
├── SKILL.md
├── scripts/
│   ├── douyin.py           # 统一入口：douyin comments / douyin posts 一键路由评论/作品
│   ├── fetch_comments.py   # 评论采集 CLI：解析 URL/转发链接 → 拉评论 → JSON/CSV（--browser 切浏览器模式）
│   ├── fetch_posts.py      # 账号主页作品抓取 CLI：主页URL/sec_uid → 作品标题+发布时间（--since/--until 过滤、--analyze 按天分布，浏览器拦截 aweme/post）
│   ├── browser_fetch.py    # 无头浏览器游客态采集评论（免登录，依赖 playwright）
│   ├── analyze.py          # 可选：jieba 分词 + 停用词 + 词频（依赖 jieba）
│   ├── mstoken.py          # mssdk 真 msToken 换发（零浏览器）
│   ├── self_check.py       # 一键环境自检：必装层 FAIL 即 exit!=0，可选层缺失只告警
│   ├── install.py          # 一键依赖安装器：装到「运行脚本的解释器」，装完跑自检
│   ├── login_helper.py     # Cookie 获取助手：看得见浏览器扫码/账号密码登录，自动存 cookie（免开发者工具）
│   ├── douyin_cookie.json  # login_helper 生成的登录态 cookie（被 --cookie-file 自动读取；不入库）
│   ├── requirements.txt    # httpx(必) / jieba(可选) / playwright(浏览器模式可选)
│   └── sign/               # a_bogus 纯 Python 签名（零 node）
│       ├── __init__.py
│       ├── ab_pure.py      # ABogusPureSigner
│       ├── fingerprint.py  # 静态浏览器指纹
│       └── sm3.py          # 国密 SM3
├── references/
│   └── api.md              # 接口/签名顺序/踩坑点/ cookie 获取/浏览器方案
└── assets/
    └── stopwords.txt       # 默认中文停用词表（可用 --stopwords 覆盖）
```

## 使用流程
1. **一键装依赖（推荐，装完即可跑）**：运行自带安装器，自动装到「运行脚本的解释器」，装完跑自检确认。
   ```bash
   cd <skill>/scripts
   python install.py            # 必装 httpx + 自检（核心抓取就绪）
   python install.py --all     # 必装 + jieba(词频) + playwright+chromium(浏览器免登录)
   ```
   - 安装器始终用 `sys.executable -m pip`，**不会装错解释器**（这是「装完跑不起来」的头号原因）。
   - 遇到系统 python 的 externally-managed 限制（PEP 668），安装器会提示在该目录建 `.venv` 后重试。
2. **首次运行也会自愈**：即使没先跑安装器，`fetch_comments.py` 启动时若发现缺 httpx，会**自动装好再继续**（装到当前解释器），不会直接报 ModuleNotFoundError 退出。
3. **一键自检（可选，装后确认）**：确认环境就绪并定位「跑不起来」的根因，不联网。
   ```bash
   python <skill>/scripts/self_check.py
   ```
   - 必装层（Python/httpx/签名子包/SM3/a_bogus/解析）有 `❌` → 核心 HTTP 抓取不可用，`exit!=0`，按提示修。
   - 可选层（jieba/playwright）`⚠️` 只告警，不影响核心；按需 `pip install`。
3. **登录获取 cookie（免开发者工具，推荐）**：普通人不用去按 F12 翻控制台。直接跑登录助手，它会打开**看得见**的浏览器，你用手机抖音「扫一扫」或账号密码像平时一样登录，登录成功后**自动**把 cookie 存成文件，后续抓取脚本直接读取。
   ```bash
   # 默认登 creator.douyin.com（登录态落在 .douyin.com 通配域，
   # 对浏览器抓取 www.douyin.com 与纯 HTTP 创作者接口都生效）
   python <skill>/scripts/login_helper.py
   # 生成 douyin_cookie.json(浏览器注入) + douyin_cookie.txt(字符串形态)
   # 浏览器抓取会自动读取 .json；strings 可直接喂 HTTP 模式 --cookie
   ```
   > `--cookie-file` 同时兼容 JSON 列表与「name=value;…」字符串两种格式。
   > ⚠️ **为什么建议登录**：不登录（游客态）抖音会弹「评论墙」，**通常只能拿到前 ~14-20 条样本评论**；登录后注入 cookie 通常能越过评论墙，拿到更多甚至全部评论。洗稿/舆情/选题样本用游客态够用，要全量务必先登录。
   > 登录态 cookie 含账号凭证，**请勿分享给他人**，也不要提交进 git。
3. **抓评论**：
   ```bash
   # A) 免登录·无头浏览器（推荐无 cookie 场景，自动翻页）
   python <skill>/scripts/fetch_comments.py "https://v.douyin.com/iRxxxxxx/" --browser --output comments.json
   #    给完整 URL / 短链 / 数字 aweme_id 均可；可加 --no-headless 肉眼观察

   # B) 有 cookie·纯 HTTP 创作者接口（抓全部评论，最稳）
   python <skill>/scripts/fetch_comments.py "https://www.douyin.com/video/7301234567890123456" --cookie "$DOUYIN_COOKIE" --format csv --output comments.csv
   ```
**抓账号主页作品（标题 + 发布时间，`fetch_posts.py`）**：
   ```bash
   # 前置：与评论 --browser 同环境，需 playwright：pip install playwright && playwright install chromium
   # 1) 抓最近 N 条作品（最新在前）
   python <skill>/scripts/fetch_posts.py "https://www.douyin.com/user/MS4wLjABAAAA..." --limit 100 --output posts.json
   # 2) 指定时间窗口：只保留 2026-09-01 ~ 2026-09-18 发布的作品
   python <skill>/scripts/fetch_posts.py "<主页链接或sec_uid>" --since 2026-09-01 --until 2026-09-18 --format csv --output posts.csv
   # 3) 登录态抓更早/更全（自动读取 login_helper 生成的 douyin_cookie.json）
   python <skill>/scripts/fetch_posts.py "<主页链接>" --since 2026-08-01 --limit 500 --with-stats
   # 4) 按天时间分布统计（作品数按 YYYY-MM-DD 聚合）
   python <skill>/scripts/fetch_posts.py "<主页链接>" --since 2026-09-01 --until 2026-09-18 --analyze --output posts.csv
   #    生成 posts.csv（作品列表）+ posts.analyze.json（post_count / first/last_publish_time / daily_distribution）
   #   提示：主页接口本身不支持时间参数，「指定时间」靠本地按 create_time 过滤；窗口越早 --limit 给越大。
   ```

**统一入口（`douyin.py`，评论/作品二合一）**：
   ```bash
   python <skill>/scripts/douyin.py comments "<视频链接>" --browser --output c.json   # = fetch_comments.py
   python <skill>/scripts/douyin.py posts    "<主页链接>" --since 2026-09-01 --until 2026-09-18 --analyze   # = fetch_posts.py
   # 子命令别名：comments/comment/c、posts/post/p；子命令后加 -h 看各自完整参数
   ```
4. **可选词频分析**（需 jieba，浏览器模式同样支持）：
   ```bash
   python <skill>/scripts/fetch_comments.py "<url>" --browser --analyze --top-n 50 --output comments.json
   # 分析结果写到 comments.analyze.json（词频 top N）
   ```

## CLI 参数
| 参数 | 说明 |
|------|------|
| `url`（位置参数） | 完整URL / 短链转发链接 / 纯数字 aweme_id |
| `--browser` | **无头浏览器模式（推荐）**：真实 Chromium 自动翻页采集；默认游客态仅前~14-20条，登录后越评论墙拿全部 |
| `--no-headless` | 浏览器模式关闭无头（可肉眼观察是否被风控弹窗拦截） |
| `--cookie-file` | 登录态 cookie 文件（login_helper 生成）；缺省自动探测 `scripts/douyin_cookie.json`。提供后浏览器以登录态抓取 |
| `--cookie` | 本人账号 cookie 串；或设环境变量 `DOUYIN_COOKIE`（HTTP 模式用） |
| `--endpoint` | `creator`（默认，需本人cookie）/ `public`（实验性，已加固） |
| `--guest` | 游客态：零 cookie 打公开接口，仅验证可用性（预期空体） |
| `--count` | 每页条数（默认 20，HTTP 模式） |
| `--max-pages` | HTTP 模式最大翻页数（默认 20，0=不限额） |
| `--max-scrolls` | 浏览器模式最大滚动加载次数（默认 20） |
| `--format` | `json`（默认）/ `csv` |
| `--output` | 输出文件路径（缺省打印 stdout） |
| `--analyze` | 附带 jieba 分词 + 停用词词频分析 |
| `--top-n` | 词频返回前 N 词（默认 50） |
| `--stopwords` | 自定义停用词文件（覆盖默认表） |
| `--min-word-len` | 词频最小词长（默认 2） |

### fetch_posts.py 参数（账号主页作品抓取）
| 参数 | 说明 |
|------|------|
| `url`（位置参数） | 账号主页完整 URL / 短链转发链接 / 纯 sec_uid（`MS4wLj...`） |
| `--since` | 仅保留该时间（含）之后发布的作品；`YYYY-MM-DD` 或 `YYYY-MM-DD HH:MM[:SS]` |
| `--until` | 仅保留该时间（含）之前发布的作品（只给日期=当天 23:59:59） |
| `--limit` | 最多抓取作品条数（默认 0=不设上限，滚动到底为止；时间窗口越早给越大） |
| `--max-scrolls` | 最大滚动加载次数（默认 30） |
| `--scroll-pause` | 每次滚动后等待毫秒（默认 1500） |
| `--timeout` | 页面加载超时毫秒（默认 60000） |
| `--no-headless` | 关闭无头，肉眼观察是否被风控弹窗拦截 |
| `--cookie-file` | 登录态 cookie 文件；缺省自动探测 `scripts/douyin_cookie.json`（越游客风控拿更早/更全） |
| `--with-stats` | 额外输出互动数据（点赞/评论/分享/收藏/播放） |
| `--analyze` | 附带按天时间分布统计（作品数按 `YYYY-MM-DD` 聚合）；配 `--output` 时写到 `<output>.analyze.json` |
| `--format` | `json`（默认）/ `csv` |
| `--output` | 输出文件路径（缺省打印 stdout） |
| `-v/--verbose` | 打印调试日志 |

## 实现要点（调用前必看 references/api.md）
- **参数顺序即签名的一部分**：`device_platform→aid→app_id→channel_id→aweme_id→cursor→count→sort_options→screen_*→browser_*→engine_*→os_*→cpu_core_num→device_memory→platform→downlink→effective_type→round_trip_time→webid/verifyFp/fp→msToken`，再算 a_bogus 追加。顺序在 `fetch_comments.py::fetch_raw` 固定，勿随意调整。
- **指纹同源**：params 的指纹字段必须取自与签名器同一个 `get_profile()`。
- **避免二次编码**：自拼 query 串后整 URL 直传 httpx，不让 httpx 重编码。
- **空 comments + has_more=0 属合法结果**，不当失败。

## 验证
- 一键安装：`python <skill>/scripts/install.py` 输出「必装层通过，环境就绪」且 `exit 0`。
- 一键自检：`python <skill>/scripts/self_check.py` 必装层全 `✅` 且 `exit 0` 即环境就绪。
- 离线：`python <skill>/scripts/sign/sm3.py` 应输出 SM3 自测 PASS。
- 离线：`ABogusPureSigner(fixed=True, aid=2906).sign_query("aid=2906")` 应返回定长 a_bogus 字符串（确定性，可用于单测）。
- 浏览器免登录（实测可用）：`python <skill>/scripts/fetch_comments.py "https://v.douyin.com/xxx/" --browser` 应能返回真实评论（游客态，前 ~14-20 条）。
- Cookie 助手（免控制台）：`python <skill>/scripts/login_helper.py` 打开可见浏览器，登录后生成 `douyin_cookie.json`；再次 `--browser` 会自动读取并以登录态抓取（越评论墙）。
- 真机（HTTP 创作者接口）：在 cookie 自然所在的账号环境跑 `fetch_comments.py --cookie ...`，确认返回 comments/total/has_more。异地登录可能触发风控，务必在目标账号本机/服务器验证。
