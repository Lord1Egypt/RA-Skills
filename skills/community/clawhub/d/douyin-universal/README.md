# douyin-search

**抖音内容抓取 skill — 搜索视频 / 找用户 / 拿作品 / 深度评论**

零依赖(只要 Python + agent-browser)、跨设备部署、默认最低风控的人类行为模式。

---

## 安装

**方式一:作为 pi/openclaw skill 安装到 `~/.pi/agent/skills/`**
```bash
git clone https://github.com/your-username/douyin-search.git \
  ~/.pi/agent/skills/douyin-search
```

**方式二:从 ClawHub 安装**
```bash
openclaw skills install douyin-search
```

**前置依赖**:
- Python 3.8+
- [agent-browser](https://github.com/vercel-labs/agent-browser) skill 已安装(用于评论抓取)
- 抖音账号的 cookies(见下方"快速开始")

---

## 快速开始

### 1. 注入 cookies(一次性)

1. 用 Chrome 登录 https://www.douyin.com/
2. F12 → Application → Cookies → 复制 www.douyin.com 全部 cookies
3. 粘到 `<skill>/data/cookies-raw.txt`(`k=v; k=v;` 格式)

### 2. 初始化(3 步)

```bash
export SKILL=~/.pi/agent/skills/douyin-search

python3 $SKILL/keepalive.py inject       # 转 Netscape 格式
python3 $SKILL/keepalive.py check        # 验证(退出码 0 = 有效)
python3 $SKILL/keepalive.py state save   # 持久化登录态
```

### 3. 使用

```bash
# 搜视频
python3 $SKILL/douyin-fetch.py search "SpaceX 上市" --type video --limit 10

# 找用户
python3 $SKILL/douyin-fetch.py user "小Lin说" --videos 20

# 单视频详情 + 5 条热评
python3 $SKILL/douyin-fetch.py video 7650453175333342470 --comments 5

# 深度评论 harvest(默认 200 条,人类模式)
python3 $SKILL/comments-harvest.py 7650453175333342470 --max 200

# 批量串行
python3 $SKILL/comments-harvest.py <id1> <id2> <id3> --max 150

# 视频下载(1.2.0+)
python3 $SKILL/douyin-fetch.py video 7650453175333342470 --download --raw-out x.json
python3 $SKILL/comments-harvest.py 7650453175333342470 --download --output $SESSION/comments
# → 下载文件在 <--output>/downloads/ 或 <--raw-out 父目录>/downloads/(默认 1080p 无水印)
```

---

## 命令速查

| 命令 | 数据源 | 输出 |
|---|---|---|
| `douyin-fetch.py search <kw> --type video` | HTTP API | 视频列表 |
| `douyin-fetch.py search <kw> --type user` | HTTP API | 用户列表 |
| `douyin-fetch.py user <nickname>` | HTTP API | 用户作品列表 |
| `douyin-fetch.py video <id> --comments N` | HTTP API + ab | 视频详情 + N 条热评 |
| **`comments-harvest.py <id> --max N`** | ab 虚拟滚动 | **深度评论(100~500 条),JSON + CSV** |
| **`comments-harvest.py <id1> <id2> ...`** | ab 串行 | **批量深度评论** |
| `comments-harvest.py <id> --download` | ab + HTTP | **深度评论 + 视频下载(1.2.0+)** |
| `douyin-fetch.py video <id> --download` | HTTP | **单视频元信息 + 评论 + 下载(1.2.0+)** |
| **`aggregate.py <export_dir>`** | 本地 | **跨次聚合去重**(videos.csv / comments_all.csv / summary.json) |

`comments-harvest.py` 参数:

| 参数 | 默认 | 说明 |
|---|---|---|
| `--max N` | 200 | 单视频最大抓取数 |
| `--output DIR` | `<skill>/data/exports/` | 输出目录 |
| `--aggressive` | 关 | 激进模式(快,但有风控风险) |
| `--warmup` | 关 | 抓前先刷 5-15s 推荐流(更安全) |
| `--interval N` | 25 | 视频间 base sleep 秒数(±30% jitter) |
| `--no-jitter` | 关 | 禁用 jitter(测试用) |
| `--download` | 关 | 同时下载视频到 `<--output>/downloads/` |
| `--download-dir DIR` | `<--output>/downloads/` | 自定义下载目录 |
| `--quality {play,download}` | play | 画质: play=1080p 无水印 / download=720p 带水印 |

`douyin-fetch.py video` 参数(1.2.0+ 新增下载相关):

| 参数 | 默认 | 说明 |
|---|---|---|
| `--download` | 关 | 下载视频到本地 |
| `--download-dir DIR` | `<--raw-out 父目录>/downloads/` | 自定义下载目录 |
| `--quality {play,download}` | play | 画质选择 |

---

## 输出格式

`comments-harvest.py` 落到 `--output` 目录,每个视频两个文件;加 `--download` 后同目录下多一个 `downloads/` 文件夹:

```
exports/
├── comments_7650771029597359394.json
├── comments_7650771029597359394.csv
└── downloads/                            ← --download 才有
    └── 7650771029597359394_<slug>_play.mp4
```

**JSON 结构**:
```json
{
  "video": {
    "title": "...",
    "author": "@xxx",
    "likes": 229000,
    "comments_total": 7084,
    "url": "https://www.douyin.com/video/...",
    "download": {                              ← --download 才有
      "path": "/.../downloads/7650771029597359394_xxx_play.mp4",
      "quality": "play",
      "size": 157946391
    }
  },
  "download": {                                ← --download 才有
    "aweme_id": "7650771029597359394",
    "ok": true,
    "path": "/.../downloads/7650771029597359394_xxx_play.mp4",
    "downloaded_bytes": 157946391,
    "http_code": 200,
    "cached": false
  },
  "comment_count": 148,
  "comments": [
    {
      "user": "张三",
      "text": "评论内容",
      "digg_count": 692,
      "relative_time": "2天前",
      "location": "北京",
      "video_download": "/.../downloads/7650771029597359394_xxx_play.mp4"
    }
  ]
}
```

**CSV 字段**: `video_id`, `video_title`, `video_author`, `video_likes`, `user`, `text`, `digg_count`, `relative_time`, `location`, `video_download`, `scraped_at`

---

## 适用 / 不适用

**适合**:
- 个人 / 小团队内容研究
- 找热点话题、热门视频
- 学术研究(短时间样本)
- AI agent 内嵌工具(需要"看看抖音最近什么火"时调用)

**不适用**:
- 商业爬虫服务(需要更复杂的反爬对抗 + 代理 IP 池)
- 24/7 自动监控(cookie 12-24h 过期,需要自动续期)
- 100+ 视频/天的批量抓取(需要养号 + IP 轮换)

**明确不会做**:
- 点赞 / 发评论 / 关注(只读)
- m3u8 解密 / 镜像站抓取 / 串流录制(只通过抖音公开的 `play_addr` / `download_addr` 下载)

---

## 故障排查

| 症状 | 修复 |
|---|---|
| `keepalive.py check` 退出码非 0 | cookies 过期,重新走"快速开始"第 1 步 |
| `state check` 报"页面是验证码中间页" | 触发 captcha,等 30 秒后重试 |
| `comments-harvest` 跑到一半 "Resource temporarily unavailable" | `agent-browser close && sleep 3`,重跑 `state save` |
| `search` 返回 0 条 | 大概率 cookies 失效,重新导 |
| 视频评论像第一条重复 | 多个 `video` 命令并行了,必须串行 `&&` 或 `;` |

更多见 [`SKILL.md`](SKILL.md)。

---

## 数据存储

所有运行时数据(cookies / 登录态 / 抓取结果)在 skill 自己的 `data/` 子目录,**自包含** — 跨设备直接 clone 即可使用。

**路径解析优先级**:
1. 环境变量 `DOUYIN_DATA_DIR`(给 docker / CI 用)
2. 老的 `/tmp/douyin/`(向后兼容)
3. 默认 `<skill>/data/`

查看当前配置:
```bash
python3 -c "import sys; sys.path.insert(0, '.'); from paths import report; print(report())"
```

**安全注意**: `data/cookies-raw.txt` 和 `data/cookies.txt` 包含你的抖音登录凭证,不要分享、提交到 git、或上传到云端。`.gitignore` 已经排除,但本地仍需注意权限(默认 `chmod 600`)。

---

## License

MIT — 详见 [LICENSE](LICENSE)。**使用本 skill 须遵守抖音用户协议(https://www.douyin.com/agreements),不得用于商业转售抖音内容、构建竞品或任何非法用途。**
