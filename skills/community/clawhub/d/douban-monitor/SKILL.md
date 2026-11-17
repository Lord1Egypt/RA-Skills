# OpenClaw 豆瓣高分监控

> ⚠️ **运行前须知（副作用）**
> - 本 skill 会向豆瓣（`m.douban.com`）和 TMDB 发起 HTTP 请求，并在本地写入 `data/`、`reports/`、`detail/` 等文件。
> - **模式 B（`auto_git_push = true`）下会自动 `git pull / commit / push`**，把生成的数据推送到远端仓库。仅在你接受"自动提交并公开这些监控数据"的仓库里启用。
> - 不想联网之外产生任何推送时，用**模式 A**：设 `auto_git_push = false` 或运行时加 `DOUBAN_MONITOR_NO_PUSH=1`（注意：本地模式只是不推送，仍会联网抓豆瓣/TMDB）。

## 目标
这个 skill 用来监控豆瓣里“近期新出现并达到门槛”的影视内容，默认关注以下条件：

- 豆瓣评分大于 `8.0`
- 豆瓣评分人数大于 `3000`
- 条目是首次达标，或者后续热度显著增长，值得进一步关注

## 运行模式

这个 skill 支持两种部署方式，靠 `config.toml` 的 `auto_git_push` 区分：

### 模式 A：纯本地
- 不托管到 GitHub，数据只写在本地。配置 `auto_git_push = false`（或运行时带 `DOUBAN_MONITOR_NO_PUSH=1`），第 8 步会跳过 git 同步。
- **skill 行为**：每次跑完，直接在对话里向用户汇报当天结果——重点是「新增命中」（首次达标的影视）和「值得二次关注」的条目；没有新增时也明确说一句「今天无新增达标」。数据文件和 `reports/` 仍会写在本地供查看，但不推送。

### 模式 B：本地 + GitHub 双跑兜底
- 托管到 GitHub，`auto_git_push = true`。本地和 GitHub Action 各跑一次、错开时段（例如本地北京时间 09:00、GitHub 21:00），两边都推送到同一仓库。
- **互相兜底**：某一次因网络 / 豆瓣限流抓取失败（当日候选为 0），该次跳过日报和 `result.json` 写入、保留上一份好数据；第 8 步先 `git pull --rebase --autostash` 再推送，两边错峰不会冲突。任意一边失败，另一边的成功结果仍在仓库里。
- 详见 README 的「自动运行」一节（Secret、写权限、cron 配置）。

## 数据源策略
采用"豆瓣侧 + TMDB 侧"的混合候选池，只依赖 HTTP 请求，不需要浏览器环境。

来源职责：

- 豆瓣榜单
  发现近期热门候选。统一通过 Rexxar API（`m.douban.com` 移动网页版接口，无需签名）抓取
- 豆瓣详情
  提供评分和评分人数真值，同样走 Rexxar API
- TMDB 热门接口
  提供额外候选和展示元数据

默认配置的豆瓣榜单（见 `config.toml` 的 `douban_collection_urls`）：

- 电影：热门、实时热门、一周口碑
- 剧集：热门、实时热门、华语一周口碑、全球一周口碑

综艺类目（国内 / 国外）已停用：TMDB 几乎没有对应封面，命中率太低，跑了也是浪费。

## 抓取策略

1. 调用 Rexxar API 获取豆瓣各榜单的候选列表，接口直接返回条目 ID、标题、评分和评分人数
2. 对于榜单已包含完整评分数据的条目，跳过详情页请求
3. 对于缺少评分数据的条目（如 TMDB 候选），用 Rexxar 详情接口补全

## 执行流程

对应 `monitor.py` 的 `[1/8]` ~ `[8/8]`：

1. 抓取豆瓣多榜单候选
2. 抓取 TMDB 候选
3. 去重并补全详情页，提取评分和评分人数
4. 更新状态与监控库，判定新增命中、继续观察和二次提醒
5. 写入状态文件、监控库和 Markdown 报告
6. 生成前端结果数据 `douban-monitor-result.json`，为每条达标条目附带入库时间（`qualified_at` / `first_discovered_at`）
7. 生成网页附加数据：`fetch_favorites.py` 手动收藏、`fetch_posters.py` 封面、`fetch_metadata.py` 元数据、`fetch_reviews.py` 短评、`generate_detail_pages.py` 静态详情页
8. 拉取远端最新代码，提交数据变更并推送到 GitHub（务必 `git add data/ detail/ reports/ posters/`，不要遗漏 detail 目录下的 HTML 页面）

**抓取失败保护**：若第 1、2 步豆瓣和 TMDB 全部失败、当日候选数为 0，第 5 步跳过 Markdown 报告写入、第 6 步跳过 `result.json` 写入，保留上一份好数据，避免网页刷新成空。

**推送保护**：第 8 步 `git pull --rebase --autostash` 失败或检测到待提交文件中出现合并冲突标记时立即中止，不提交坏数据。

## 可视化网页

项目根目录的 `index.html` 是一个静态网页，读取 `data/` 下的 JSON 文件展示达标内容。

- 暗色主题瀑布流卡片布局
- 支持电影 / 剧集 / 综艺分类切换和多维排序，默认"最近入库"按真实入库时间（`qualified_at` / `first_discovered_at`）倒序
- 卡片包含封面、评分、类型标签、简介、上映日期，点击跳转豆瓣详情页
- 数据来源：`douban-monitor-result.json`、`douban-monitor-favorites-result.json`、`douban-monitor-posters.json`、`douban-monitor-metadata.json`、`douban-monitor-reviews.json`

## 核心规则

### 首次达标
满足以下条件时视为“新增命中”：

- 评分大于 `min_rating`
- 评分人数大于 `min_rating_count`
- 历史状态中此前未达标

### 继续观察
未达到最终门槛但仍有潜力的条目继续进入监控库，例如：

- 评分已经接近目标
- 评分人数已具备增长空间
- 仍然出现在榜单来源中

## 入库规则
不要把所有候选都永久加入监控库。只有具备一定潜力的条目才会继续跟踪。

入库参考条件：

- 出现在豆瓣榜单页
- 出现在选定的 TMDB 热门源
- 豆瓣评分大于等于 `7.5`
- 豆瓣评分人数大于等于 `1000`

## 当前状态

当前版本已经验证通过：

- 纯 HTTP 抓取：Rexxar API 单通道，无需浏览器，无需签名
- 状态文件、监控库、Markdown 报告输出
- 阈值筛选与新增命中判定
- 网页可视化展示（瀑布流卡片布局、封面、简介、评分、短评）
- 手动收藏：`data/douban-monitor-favorites.json` 填豆瓣 ID 即可在网页展示
- 最近入库排序：达标条目携带入库时间戳，网页按真实入库时间排序
- TMDB 封面和元数据自动获取
- 静态详情页生成（`detail/<douban_id>.html`）
- GitHub Actions 手动触发运行（cron 暂停用观察；境外 runner 实测有时能抓豆瓣，但机房 IP 限流不稳定，稳定定时抓取由国内 Docker 负责）
- 抓取失败和推送冲突有兜底保护，不会覆盖或污染历史数据

当前已打通的榜单类型：

- 电影（热门 / 实时热门 / 一周口碑）
- 剧集（热门 / 实时热门 / 华语 / 全球）

## 已知限制

- 豆瓣侧抓取全部依赖 Rexxar API（`m.douban.com`）。若 Rexxar 整体宕机，本次运行会跳过日报和前端结果写入，保留上一份好数据
- 未配置 `TMDB_API_KEY` 时，TMDB 候选源和网页封面/元数据不会生效

## 后续扩展

- 支持豆瓣 Cookie，提升榜单和搜索相关页面稳定性
- 接入 MoviePilot，实现命中内容自动推送或下载
- 生成适合公众号发布的内容稿件
