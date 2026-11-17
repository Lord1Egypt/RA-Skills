# 实现说明

当前 skill 已包含一个完整可运行的主脚本，位置在 `scripts/monitor.py`。

## 当前模块职责

### 豆瓣抓取（Rexxar 单通道）

统一走 `m.douban.com` 移动网页版 Rexxar API，无需签名和 apiKey，是当前豆瓣抓取的唯一通道（早期的 Frodo 签名通道已移除）。

- `rexxar_get(...)`
  调用 Rexxar API 的底层封装。
- `fetch_douban_collection_via_rexxar(...)` / `fetch_douban_subject_detail_via_rexxar(...)`
  Rexxar 版的榜单分页和条目详情抓取。
- `fetch_douban_weekly_candidates_lite(...)`
  榜单候选抓取入口：遍历 `config.toml` 的 `douban_collection_urls`，逐个榜单抓取，单个失败自动跳过。
- `fetch_douban_subject_detail_lite(...)`
  详情补全入口：仅对缺少评分/评分人数的条目请求 Rexxar 详情。

### 通用模块

- `fetch_tmdb_hot_candidates_with_config(...)`
  调用 TMDB 热门接口获取补充候选。
- `update_library(...)`
  应用入库规则、分配观察层级、刷新监控库条目。
- `update_state(...)`
  判定首次提醒和二次提醒。
- `render_report(...)`
  输出每日 Markdown 报告。
- `build_result_json(...)`
  生成前端结果数据，每条达标条目附带 `qualified_at` / `first_discovered_at`。

### 网页数据生成

- `fetch_favorites.py`
  读取 `data/douban-monitor-favorites.json` 的手动收藏豆瓣 ID，通过 Rexxar API 获取详情，同时附带 TMDB 封面和元数据。
- `fetch_posters.py`
  从 TMDB 获取封面图 URL。查找策略：Rexxar 取 IMDB ID → TMDB `/find/{imdb_id}`（最准确）→ TMDB 标题模糊搜索（逐步简化标题，去除季数后缀，拆分中外文混合词）。
  输出：`data/douban-monitor-posters.json`
- `fetch_metadata.py`
  从 TMDB 获取 original_title、overview、genres、runtime、release_date、cast 等。使用与 fetch_posters.py 相同的 IMDB→TMDB 查找策略。
  输出：`data/douban-monitor-metadata.json`
- `fetch_reviews.py`
  抓取豆瓣短评。
  输出：`data/douban-monitor-reviews.json`
- `generate_detail_pages.py`
  为每个达标条目生成静态详情页 `detail/<douban_id>.html`。

## Python 依赖

仅使用 Python 标准库，无需 `pip install` 额外依赖。

## 环境变量

- `TMDB_API_KEY`
- `TMDB_BEARER_TOKEN`

通常只需要 `TMDB_API_KEY`。`TMDB_BEARER_TOKEN` 是另一种认证方式，不是必需项。

## 当前数据策略

- 候选发现
  豆瓣多榜单页 + TMDB 热门接口
- 评分与评分人数真值
  豆瓣详情页（Rexxar API）；榜单已带评分的条目直接复用，不再重复请求详情
- TMDB 作用
  补充展示元数据，不覆盖豆瓣评分和评分人数
- 网页数据生成
  `fetch_posters.py` / `fetch_metadata.py` / `fetch_reviews.py` / `generate_detail_pages.py` 从 TMDB 和豆瓣获取展示用数据并生成详情页
- 数据版本管理
  `data/`、`detail/`、`reports/` 纳入 Git 跟踪。模式 B（`auto_git_push = true`）下每次运行后自动提交推送；模式 A（`auto_git_push = false` 或 `DOUBAN_MONITOR_NO_PUSH=1`）跳过第 8 步 git 同步，只写本地
- 抓取失败兜底
  候选为 0 时跳过 Markdown 报告和 `result.json` 的写入，保留上一份好数据；`git pull --rebase` 失败或检测到冲突标记时中止提交

当前已验证的榜单（综艺已停用，见 `config.toml`）：

- 电影：热门、实时热门、一周口碑
- 剧集：热门、实时热门、华语一周口碑、全球一周口碑
