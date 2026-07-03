# Changelog — bilibili-search

## v0.3.0 (同期收割 + 分页拿全量 + SPA reload 修)

- **`harvest user`** 加 `--since YYYY-MM-DD` / `--before YYYY-MM-DD` 时间过滤 (零额外 API 调用, 复用 video 的 pubdate)
- **`harvest user`** 加 `--auto-pages` 配合 `fetch.py user --scroll` 拿全量 (默认仅首页 40 张)
- **`harvest user`** 早终止优化: 按 B 站默认倒序, 跳过 `--since` 后数 168+ 条 historical, 余下几十个 只走正常路径
- **`fetch user`** 加 `--reload auto|yes|no` (默认 auto), 智能检测已渲染 session, 避免 reload 破坏 SPA 状态
- **`fetch user`** 加 `--scroll` 实际是点翻页分页, 从 0~40 个 → 拿全所有页

## v0.2.0

- 加弹幕抓取 (`danmaku` 子命令 + harvest `--danmaku` 选项, 走 .venv 里的 bilibili-api)

## v0.1.0 (initial)

初版。功能:

- **`bili-fetch.py`** 原子命令
  - `paths` — 路径配置
  - `search <keyword>` — 主题视频搜索（按 order 排序、翻页）
  - `user-search <keyword>` — 用户名 → mid 解析
  - `user <mid>` — UP 主主页 + 视频列表（走 SPA，自动 reload + sleep）
  - `video <bvid>` — 单视频详情 + 热门评论（自动 bvid→aid）
  - `comments <bvid|aid>` — 深翻评论（按 next_offset 翻页）
- **`bili-harvest.py`** 收割编排
  - `hot <keyword>` — 搜主题 → 候选 → 逐条 video → 落盘 + REPORT
  - `user <mid>` — UP 主主页 → 视频 → 逐条 video → 落盘 + REPORT
  - `ids <bvid>...` — 已知 BV 号批量抓
- **`paths.py`** 统一路径管理（`BI_DATA_DIR` / `BI_COOKIE_FILE` env 覆盖，老 `/tmp/bilibili/` 兼容）
- 完整 SKILL.md / README.md / docs/pitfalls.md

## 已知限制 (TODO for v0.2)

- 无 cookie 通道未实现 inject/check 工具（agent-browser `--state` 已可手动加载）
- 没集成"按 BVID 反查视频元数据"批量接口（已知 BV 列表时直接走 `video` 子命令即可）
- 没集成弹幕抓取（接口是 `/x/v2/dm/web/seg.so`，需 protobuf 解析）