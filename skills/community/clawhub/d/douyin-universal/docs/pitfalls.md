# 开发者参考 - Pitfalls & 内部细节

> **本文件是开发参考,不是 agent 决策文档。** agent 读 SKILL.md 就够。
> 这里收集:踩过的反爬坑、脚本实现细节、docker/CI 部署、目录结构说明。

## 数据路径

```
$SKILL/                              ← skill 根（可 git clone 到任何位置）
├── douyin-fetch.py          HTTP API 抓取（search / user / video）
├── comments-harvest.py      ab 虚拟滚动 harvest（单/多视频）
├── aggregate.py             跨次会话聚合去重
├── downloader.py            视频下载 helper（detail API → play_addr URL → 流式下载）
├── keepalive.py             cookie / ab state 维护
├── paths.py                 路径统一管理
├── SKILL.md                 agent 入口（必读）
├── docs/pitfalls.md         ← 本文件
├── CHANGELOG.md
├── CONTRIBUTING.md
├── README.md
└── data/                    运行时数据（cookie / state / exports / downloads）
```

**路径解析优先级**(从高到低):
1. 环境变量 `DOUYIN_DATA_DIR` (给 docker / CI 用)
2. 老的 `/tmp/douyin/` (向后兼容,如果存在)
3. 默认 `$SKILL/data/`

查看当前路径配置:
```bash
python3 -c "from paths import report; print(report())"
```

## 死胡同(踩过的反爬坑)

| 尝试 | 结果 |
|---|---|
| `ab open https://www.douyin.com/` (主页) | 触发滑块验证(首页反爬最严) |
| 匿名 `ab open` 任何抖音 URL | 弹登录 panel |
| 直接 curl 搜索 API | 200 但 0 字节(verify_check) |
| `/aweme/v1/web/search/item/` API | verify_check 拦截 |
| `aweme/v1/web/search/sug/` API | sug_list 是 null |
| 评论 API `aweme/v1/web/comment/list/` | verify_check 拦截,只能抓 DOM |
| 虚拟滚动容器用 `document.body` / 任何最大可滚动 div | 不会触发 lazy load |
| 解析评论 text 时把 `...` 当评论内容 | 取出的是占位符,不是 text(总输出会异常) |
| ab eval 单次跑 30s+ 的长任务 | ab daemon busy 5 次重试都失败 |
| Bing/百度 site:douyin.com | 全部反爬 |
| 多个 video / harvest 命令并行 | 全部拿到第一条评论(单 tab) |
| 触发 captcha 后立刻 reload | 还是 captcha,需等 30 秒 |
| `--comments > 20` 用 `video` 命令 | 只给前 5 条,要用 `comments-harvest.py` |

## 脚本实现细节(agent 不需要知道)

### harvest 走虚拟滚动
- douyin PC web 评论容器是 `.parent-route-container.route-scroll-container`
- 反复 `scrollBy(0, 200-500px)` 触发 lazy load
- 用 `localStorage` 中转评论数据(ab eval 输出无明显字节限制,但 localStorage 写入 native 不受任何限制)

### 跳过 `...` 占位符
douyin DOM 每条评论固定格式:
```
user
...     ← UI 占位符,不是被截断
text
time
likes
操作按钮
```
第二行的 `...` 必须跳过。

### 抓取策略
- **人类模式**(默认,最低风控):scrollBy 200-500px + sleep 1.5-5s + 10% 概率长停留 2-6s + 15 round 上限 + stalled 早停
- **激进模式**(`--aggressive`):scrollTop = scrollHeight + sleep 0.9s + 25 round 上限
- 视频间自动 sleep (base 25s × random 0.7-1.3 → 17-32s 区间),符合"每账号 ≤ 50-100 评论页/小时"
- `--max` 决定单视频抓取上限(人类模式默认 200,激进模式默认 500)
- harvest 拆成 incremental(每 round 一次 eval),避免 ab daemon busy

### 脚本已自动处理
- `state load/save/check` 自动清理 daemon 防 `--state` 抢占
- `video` 命令自动检测 captcha，遇风控明确报错而非返回空
- 视频元信息抓不到时显式标 `search-fallback`，不静默吞错
- `--raw-out` 落盘完整 raw JSON（含 detail API 响应）
- aggregate.py 自动跨 search 去重 + 跨 harvest 合并 + 评论内去重（video_id+user+text 三元组）
- `--download` 下载的视频路径同时嵌入到 `--raw-out` JSON 顶层 `download` 字段 / `comments-harvest.py` 输出的 `video.download` 字段 / 每个 comments CSV 的 `video_download` 列；`aggregate.py` 会从 `<export_dir>/downloads/` 目录反向补老 session 的路径

### 视频下载（1.2.0+）
- `play_addr`（默认）和 `download_addr` 都是 detail API 直接给的公开 URL，不涉及 m3u8 / 镜像
- **必须 `Referer: https://www.douyin.com/`**，否则 403 — `downloader.py` 已带
- URL 里 `dy_q=` 是过期时间戳，默认 ~2 小时有效；fetch → download 必须在同一脚本调用里连贯完成
- 1080p 无水印（play_addr）默认 100~200MB / 视频；720p 带水印（download_addr）约一半
- 已存在的本地文件跳过重下（`download.cached=true`）— 重复跑 harvest + download 不会浪费带宽
- **所有产物均在 `$SKILL/data/exports/<session>/downloads/`，不会散落到 `/tmp/`**
