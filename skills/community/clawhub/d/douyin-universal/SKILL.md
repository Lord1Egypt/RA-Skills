---
name: douyin-universal
description: 抖音内容抓取(搜索视频/用户/拿作品/看评论)。HTTP API 拿基础数据,agent-browser 抓评论虚拟滚动 harvest(需登录 cookie)。零依赖、跨设备、支持最低风控的人类模式。只读 skill,不修改 douyin 任何数据。
version: 1.2.0
emoji: "🎵"
homepage: https://github.com/excalibursssooo/douyin-search
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - agent-browser
    envVars:
      - name: DOUYIN_COOKIE_FILE
        required: false
        description: 抖音登录 cookies 路径(评论 harvest 必需)。默认 $SKILL/data/cookies.txt;老的 /tmp/douyin/cookies.txt 也兼容。
      - name: DOUYIN_DATA_DIR
        required: false
        description: skill 运行时数据目录(覆盖默认 $SKILL/data/)。给 docker / CI 用。
      - name: SKILL
        required: false
        description: skill 根目录绝对路径,命令示例里用得到(agent 自填)。
    primaryEnv: DOUYIN_COOKIE_FILE
---

# douyin-search

## ⚡ 30 秒上手

```bash
export SKILL=/path/to/douyin-search    # 你 clone 的位置

# 抓数据(search / harvest)
python3 $SKILL/douyin-fetch.py search "<关键词>" --type video --limit 30 --raw-out <path>   # 主题搜视频
python3 $SKILL/douyin-fetch.py user "<昵称>" --videos 20                                    # 拿用户作品
python3 $SKILL/douyin-fetch.py video <id> --comments N                                       # 单视频元信息 + 5~20 条热评
python3 $SKILL/comments-harvest.py <id> --max 200                                            # 单视频深度评论
python3 $SKILL/comments-harvest.py <id1> <id2> ... --max 150                                 # 批量串行 harvest

# 聚合去重
python3 $SKILL/aggregate.py <export_dir>   # 跨 search+harvest 输出 3 个总表(见下方"典型工作流")
```

**agent 须知**:看完本文档就会用,不要 read 脚本源码。开发参考(目录结构、反爬坑、脚本实现细节)看 `docs/pitfalls.md`。

## 🔄 典型工作流(从搜索到聚合)

search + harvest 都只产**原始数据**(raw JSON / per-video comments)。跨次会话的**去重、合并、汇总**是 `aggregate.py` 的职责,**不是 agent 写代码的工作** - 任何 session 跑完一遍都直接调 aggregate。

```bash
export SKILL=/path/to/douyin-search
export SESSION=$SKILL/data/exports/$(date +%Y%m%d)-my-topic
mkdir -p $SESSION

# 1. 多个关键词搜,每个 --raw-out 落盘到 $SESSION/search-<kw>.json
for kw in "AI短剧" "AI漫剧" "AI短片" "AI动漫"; do
  python3 $SKILL/douyin-fetch.py search "$kw" --type video --limit 30 \
    --raw-out $SESSION/search-${kw}.json
done

# 2. 从 search 结果挑高赞视频(读 $SESSION/search-*.json 选 top N),串行 harvest
python3 $SKILL/comments-harvest.py <id1> <id2> ... --max 150 --output $SESSION/comments

# 3. 聚合去重 - 一次性产出 3 个产物
python3 $SKILL/aggregate.py $SESSION
# → $SESSION/aggregate_videos.csv        唯一视频清单(按赞数排序,带 matched_keywords)
# → $SESSION/aggregate_comments_all.csv  全部去重评论(单表,下游分析直接用)
# → $SESSION/aggregate_summary.json      统计(去重率 / 采样数 / 总览)
```

**agent 唯一要决定的事**:跑哪些关键词、harvest 哪些视频(其他都是 skill 自己处理)。
**不要**在 export 目录里手写 `aggregate.py` / `merge.py` / `dedup.py` - 这是 skill 自己的能力,不是 agent 临场编写的范畴。

## 前置(一次性 setup,新设备必跑)

```bash
# 1. Chrome 登录 douyin.com → F12 → Application → Cookies → 复制到 <skill>/data/cookies-raw.txt
#    (老路径兼容: /tmp/douyin/cookies-raw.txt 也行)
# 2. 转 Netscape 格式
python3 $SKILL/keepalive.py inject
# 3. 验证 cookie
python3 $SKILL/keepalive.py check      # 退出码 0 = 有效
# 4. (仅评论需要) 持久化 ab session
python3 $SKILL/keepalive.py state save
```

如果 cookie 不存在/过期/无效,立刻停止并提示用户重新导 cookies,或把整段 cookies 直接发给你,你落盘到 `$SKILL/data/cookies-raw.txt` 然后跑 inject → check → state save。

之后每次新 session 开头跑 `state load` 一次即可。`state check` 可验证登录态是否还有效。

## 关键提示(只讲 agent 决策点)

**主题搜索找爆款**:
- AI 类短剧要搜 `AI短剧` / `AI漫剧` / `AI短片` / `AI动漫` 多个,合并去重 - 只搜一个会漏一大半
- 时间过滤不支持,按输出里的 `YYYY-MM-DD` 自己挑近一周;`--limit 30` 一次拿全
- `--raw-out <path>` 落盘原始 JSON(aggregate 需要,debug 也需要)

**评论抓取**:
- **多个 video / harvest 命令必须串行**(`&&` 或 `;`),不能 `&` 并行 - ab 单 tab 单 session,并行会全部拿到第一条的评论
- `video --comments` 只给前 5 条(快但浅);深度评论用 `comments-harvest.py`
- 失败时脚本会显式提示原因(captcha / cookie 失效),不会静默返回空

**user 搜索**：仅精确匹配昵称/抖音号。模糊词（像"财经"）搜不到，需要先有具体昵称。

**视频下载**（1.2.0+）：
- `--download` 会从 detail API 拿 `play_addr` 链接（1080p 无水印），需带 `Referer: https://www.douyin.com/` 头，否则 403
- 抖音视频 URL 带 `dy_q=` 过期戳（默认 ~2 小时有效），fetch_url → download 必须连贯；单个命令内部已处理，**不要**先跑一遍拿 URL 再隔一段时间下载
- 默认下载到 `<--output>/downloads/` 或 `<--raw-out 父目录>/downloads/`，可在 `$SKILL/data/exports/<session>/` 下随时找到
- `--quality download` 选 720p 带水印（文件约一半大小，适合备份存档）
- 已存在的本地文件跳过重下（`download.cached=true`）— 重复跑同一条命令不会浪费带宽
- `aggregate.py` 会自动从 `<export_dir>/downloads/` 目录反向补视频路径，老 session（未带 `--download` 跑的）也能在 CSV 里拿到本地链接

## 🛠 故障排查

| 症状 | 修复 |
|---|---|
| `state check` 报 "state 实际不可用" / "未登录首页" | cookie 过期 → `keepalive.py check` 验证;非 0 退出码就重新 setup(导 cookie → `inject` → `check` → `state save`) |
| `state check` 报 "页面是验证码中间页" | **state 已坏,daemon 状态被 captcha 污染** → `agent-browser close && sleep 2 && state save` 重生成(不要干等) |
| `state check` 报 "state 文件不存在" | 还没跑过 `state save` → 跑一次 |
| `state load/save/check` 卡住无输出 | daemon 残留 → `agent-browser close && sleep 2` 再重跑 |
| `state check` 拿到 fallback 话题页(`#某话题` 而非视频标题) | `PROBE_VIDEO` 常量里的视频被删/转私密 → 改 `keepalive.py` 顶部的 `PROBE_VIDEO` |
| `search` 返回 0 条,或 `video --comments` 报登录态问题 | cookie 失效 → 重 setup |
| `harvest` 跑到一半报 "Failed to read: Resource temporarily unavailable" | ab daemon 累积状态坏 → `agent-browser close && sleep 3`,重 state save |
| `video --comments` 抓到的评论像第一条重复 | 多个 `video` 命令并行了 → 串行跑(`&&` 或 `;`) |

**经验法则**:
- 看到 captcha 字样先想"state 是不是坏了" → 默认动作 `close && sleep && state save`,不是 sleep 等
- 脚本卡死 → `agent-browser close && sleep 2` 再重跑
- 登录/评论类问题 → `keepalive.py check` 看退出码(0=有效)

## 边界(不做的事)
- 点赞/发评论/关注 — 只读
- 其他网站 — agent-browser skill
- 业务级大规模抓取(>100 视频/天) — 需用 Playwright + 真实 Chrome profile + 代理 IP 池,超出 skill 范围
- 反爬坑、脚本实现细节、目录结构 — 看 `docs/pitfalls.md`
- **视频下载仅限 `play_addr` / `download_addr` 两个公开 addr** — 不去解密 m3u8 / 找其他镜像 / 串流录制(那超出了"只读"边界)
