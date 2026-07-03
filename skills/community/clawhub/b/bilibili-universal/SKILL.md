---
name: bilibili-universal
description: bilibili 内容抓取(搜索/UP 主空间/视频详情/评论)。统一走 agent-browser,自动复用 buvid cookie + wbi 签名环境。无需登录即可抓大部分公开数据。
version: 0.1.0
emoji: "📺"
homepage: https://github.com/excalibursssooo/bilibili-search
metadata:
  openclaw:
    requires:
      bins: [python3, agent-browser]
      pip:
        # 仅 danmaku 子命令需要;默认装在 $SKILL/.venv/ 里不污染全局
        - bilibili-api-python
        - curl_cffi
        - protobuf
    envVars:
      - {name: BI_DATA_DIR,    required: false, description: "覆盖整个 data/ 目录(给 docker/CI 用)"}
      - {name: BI_COOKIE_FILE, required: false, description: "覆盖 cookie 路径(可选, B 站抓取不强制登录)"}
    primaryEnv: BI_DATA_DIR
changelog:
  - v0.2.0: 加弹幕抓取 (danmaku 子命令 + harvest --danmaku 选项, 走 .venv 里的 bilibili-api)
  - v0.1.0: 初版 (atomic fetch + 编排 harvest 双层架构)
---

# bilibili-universal

> **B 站公开数据抓取** skill。**不强制登录**,登录后能拿到更高画质 / 关注状态 / 个人化推荐。
> 
> - **GitHub 仓库**: https://github.com/excalibursssooo/bilibili-search (本地路径: `$SKILL/bilibili-search/`)
> - **ClawHub slug**: `bilibili-universal` (因为 bilibili-search 已被别人占用)
> - 安装: `clawhub install bilibili-universal` 或 `openclaw skills install @excalibursssooo/bilibili-universal`

## ⚡ 30 秒上手

```bash
export SKILL=/path/to/bilibili-search

# 🔍 主题搜索
python3 $SKILL/bili-fetch.py search "逗比的雀巢" --order pubdate --pages 2

# 👤 用户名 → mid 解析
python3 $SKILL/bili-fetch.py user-search "逗比的雀巢"

# 👤 UP 主主页 + 视频列表 (⭐ 推荐路径, 走 SPA 拿全量)
python3 $SKILL/bili-fetch.py user 5294454 --videos 40

# 🎬 单视频详情 + 热门评论
python3 $SKILL/bili-fetch.py video BV1K3Gz6pEoo --comments 20

# 💬 深翻评论 (单独抓)
python3 $SKILL/bili-fetch.py comments BV1K3Gz6pEoo --ps 50 --pages 5

# 💢 弹幕 (走 bilibili_api 库, 需在 venv 里)
.venv/bin/python $SKILL/bili-fetch.py danmaku BV1K3Gz6pEoo --out dm.json
.venv/bin/python $SKILL/bili-fetch.py video BV1K3Gz6pEoo --danmaku-out dm.json

# 🎯 收割编排(自动落盘 + 生成 REPORT.md)
.venv/bin/python $SKILL/bili-harvest.py user 5294454 --videos 40 --comments 20 --danmaku
.venv/bin/python $SKILL/bili-harvest.py hot "逗比的雀巢" --order pubdate --limit 10
.venv/bin/python $SKILL/bili-harvest.py ids BV1K3Gz6pEoo BV16ooQBsERA --danmaku

# 🎯 同期收割 (推荐路径: 拿 1年以来)
.venv/bin/python $SKILL/bili-harvest.py user 5294454 --since 2025-01-01 --before 2025-12-31 --auto-pages --videos 200 --comments 20 --danmaku
```

`bili-harvest.py` 编排工作流,`bili-fetch.py` 原子操作。落盘: `$SKILL/data/harvests/<topic>-<ts>/REPORT.md`。

---

## 🎯 同期收割: --since / --before / --auto-pages (v0.3.0+)

```bash
# STN 工作室今年以来 (32 个视频)
.venv/bin/python $SKILL/bili-harvest.py user 7349 --since 2026-01-01 --auto-pages --comments 20 --danmaku

# 2025 整年 (--before 2025-12-31 表示 不含 2026)
.venv/bin/python $SKILL/bili-harvest.py user 7349 --since 2025-01-01 --before 2025-12-31 --auto-pages --comments 20 --danmaku
```

**为什么需要 `--auto-pages`**:
- 实际 UPC 主页首页只渲染 ~40 张卡 、有 37+ 页
- `--auto-pages` 会通过 fetch.py user 的 `--scroll` 拏多页 () 还是手动调 `翻页按钮` (动获取页码验证), 拿到全部 BV
- 推荐: 配合 `--since` 使用, 在跨越一年窗口时避免 跳出

**时间过滤原理 (零额外成本)**:
- harvest 拿到候选后逐个调 `bili-fetch.py video` 拿详情, 本来就是必走
- 详情返回里现成有精确 `pubdate` (Unix ts)
- 按 B 站默认顺序 (时间倒序), 一旦遇到一条早于 `--since` 的, 后续全部 早终止
- 例如 STN 跨 200 条候选 但跳 168 条 historical, 只跑 32 条

**支持的格式**:
- `--since 2026-01-01` (天级)
- `--since 2026-01-15T10:30` (带时分秒, 较少用)

参数表:

| 参数 | 说明 |
|---|---|
| `--since YYYY-MM-DD` | 只拿该日期及之后 (含) 的视频 |
| `--before YYYY-MM-DD` | 只拿该日期及之前 (含) 的视频 |
| `--auto-pages` | 拿全量 UP 主视频 (配合 `--since` 使用, 拿一年区间建议开这个) |

---

## 🎯 核心:收割 UP 主(⭐ 推荐路径)

```bash
bili-harvest.py user <mid> --videos 40 --comments 20 --danmaku
```

**为什么是推荐路径**:
- ✅ **完全不走 search 桶** → 不触发 B 站 search 路径的风控
- ✅ UP 主空间 SPA 一次性渲染,DOM 里就有元数据 + 视频列表 + BV 号
- ✅ 一条命令,内部完成: 主页拿 N 条 → 逐条 video 抓详情 + 评论 + 弹幕 → 报告

### 内部流程

```
Step 1  bili-fetch.py user <mid> --videos N   →  user.json (含 videos[])
Step 2  对每个 bvid, 调 bili-fetch.py video <bvid> --comments N [--danmaku-out dm/<bvid>.json]
        ↓ 公开 API: /x/web-interface/view + /x/v2/reply/main + /x/v2/dm/web/seg.so
Step 3  落盘 + 写 REPORT.md
```

### 落盘结构

```
$SKILL/data/harvests/user-<mid前12>-<时间戳>/
├── REPORT.md          ← 人类可读报告 (视频表 + 弹幕统计 + 每条 top 3 评论)
├── user.json          ← UP 主元数据 + 视频列表
├── videos/
│   ├── v01-<BV前8>.json
│   └── ...
└── danmaku/           ← (--danmaku 时) 弹幕原始数据
    ├── BV....json
    └── ...
```

### 弹幕字段说明 (`danmaku/<bvid>.json` 是 list[dict])

| 字段 | 说明 |
|---|---|
| `time_s` | 视频内出现时间 (秒, 0 开始) |
| `time_ms` | 同上 (毫秒) |
| `mode` | 1 滚动 / 4 底部 / 5 顶部 |
| `font_size` | 字号 |
| `color` | 十六进制颜色 (例 `#e70012`) |
| `content` | 弹幕文本 |
| `uid_hash` | 发送者 mid 哈希 (B 站脱敏) |
| `pool` | 弹幕池 (0=普通 / 1=字幕 / 2=特殊) |
| `sender_id` | 弹幕 ID |
| `weight` | 权重 |
| `is_sub` | 是否字幕弹幕 |

> 弹幕 API 走 **bilibili_api 库** (内部用 `curl_cffi`),**不受 agent-browser 风控影响**。需要 .venv 环境安装: `python3 -m venv .venv && .venv/bin/pip install bilibili-api-python curl_cffi`

---

## 🌐 抓取路径与风控

B 站公开数据有 3 条主要抓取路径,风控阈值完全不同:

| 路径 | 用途 | 风控 |
|---|---|---|
| `/x/web-interface/view` | 视频详情 | 🟢 弱 |
| `/x/v2/reply/main` | 评论 | 🟢 弱 |
| `/x/web-interface/search/type` | 搜索 | 🟡 中 (search 桶偶尔 captcha) |
| `space.bilibili.com/{mid}/upload/video` | UP 主空间 SPA | 🟢 弱 (已登录 cookie 后更稳) |
| `/x/space/wbi/arc/search` | UP 主空间 API | 🔴 强 (需要 wbi 签名,本 skill 不用) |

### 黄金法则:**走 SPA + 公开 API,绕开 wbi 签名桶**

本 skill 所有命令**不直接调 wbi 接口**,而是通过:
1. agent-browser 内部 fetch (复用 buvid cookie + wbi 签名所需的密钥环境)
2. UP 主空间走 SPA (DOM 解析,不碰 API)

这样**完全不需要登录 cookie**,也**不需要算 w_rid**。

---

## 🚨 已知风控 / 坑

| # | 坑 | 怎么避 |
|---|---|---|
| 1 | `search` 接口偶尔 `code=-352` 风控失败 | 换 `--order` 重试,或等 10 分钟 |
| 2 | `user` 第一次进 SPA 没渲染视频卡片 | 脚本自动 `reload()` + sleep 6s |
| 3 | `comments` 返回 `data.replies` 为空 | 该视频评论区被关闭或全部折叠,正常 |
| 4 | `video` 接口需要 aid 而脚本用 bvid | 内部自动 `view` 转 aid,无需手动 |
| 5 | `search` 的 author 字段含后缀如 `"逗比的雀巢·昨天"` | 已用 `author` 字段 (原始) 不用正则解析 |
| 6 | 评论接口有 IP 频控 | 默认 sleep 0.5s,大批量抓换 IP |
| 7 | `user` 命令在 headless 模式下首次 SPA 不渲染 | 脚本强制 reload() 触发二次渲染 |

---

## ⚠️ ab 调用限速铁律

| 场景 | 间隔 |
|---|---|
| `ab_open` → `ab_open`(不同页面) | **必须 sleep ≥ 2s**(脚本默认已加) |
| `ab_eval` → `ab_eval`(同一页面) | 不需 sleep |
| 连续多次 `ab_open`(调试) | **必中风控** |

**黄金法则**:能交给脚本的事,绝不要用 `ab` 手动打。

---

## 决策规则(报错时查这个)

| 错误 | 含义 | 动作 |
|---|---|---|
| `code = -352` | wbi / 风控校验失败 | 脚本内已不调 wbi 接口;若仍出,等 10 min 或换 IP |
| `code = -403` | 访问权限不足 | 多见于评论接口 IP 频控,等 5-10 min |
| `code = -101` | 需要登录 | 该资源(1080P/会员视频)需登录,本 skill 不支持 |
| `code = -404` | 视频不存在/已删除 | 检查 bvid 是否正确 |
| `code = 25010` | 风控验证码 | **不重试**,等 10 min 或换 IP |
| `comments = []` | 评论为空 | 视频评论关闭或全被折叠,正常 |
| `user` 没拿到视频卡片 | SPA 未渲染 | 脚本自动 reload + sleep;仍失败就 `agent-browser close --all` 重跑 |

---

## 🆚 与其他 skill 的差异

| 维度 | douyin | zhihu | xhs | **bilibili** |
|---|---|---|---|---|
| 抓取路径 | HTTP API | HTTP API | agent-browser only | **agent-browser + 公开 API** |
| 必填 cookie | ttwid | z_c0 | a1+web_session | **❌ 不强制** |
| 强登录态 | 中 | 弱 | 极强 (web_session 6-12h) | **弱** (buvid 即可) |
| 风控强度 | 中 | 弱 | 强 | **中** (search 桶偶发 captcha) |
| 内容主体 | 视频/图文 | 问答/专栏 | 笔记 | **视频 + 评论** |

---

## 边界

- B 站抓数据 → 本 skill
- 写操作(点赞/评论/关注)/ 其他网站 → agent-browser skill
- 长视频弹幕导出 → agent-browser skill 自己写 (未集成)

---

## 首次 setup(可选)

```bash
# B 站抓取不强制 cookie,默认直接能跑
# 想拿更高画质 / 关注状态,需要登录 cookie:
# 浏览器登录 bilibili.com → F12 → Application → Cookies → 复制 .bilibili.com 全部
cat > $SKILL/data/cookies-raw.txt <<'EOF'
buvid3=xxx; SESSDATA=xxx; bili_jct=xxx; ...
EOF
chmod 600 $SKILL/data/cookies-raw.txt

# (目前暂无 inject/check 工具,可手动转 Netscape 后用 agent-browser --state 加载)
```

### 弹幕功能依赖(必装)

弹幕子命令 (`bili-fetch.py danmaku`) 和 `--danmaku` 选项走 `bilibili_api` 库,
**仅在 .venv 里安装**,**不污染全局**:

```bash
python3 -m venv .venv
.venv/bin/pip install bilibili-api-python curl_cffi protobuf
```

`bili-harvest.py` 会**自动**检测 `.venv/bin/python` 并优先使用;找不到时回退到 `sys.executable`。

**当前阶段**: 未登录态已能跑通 80% 用例;登录 cookie 通道为"可选项"。弹幕功能要求 .venv。