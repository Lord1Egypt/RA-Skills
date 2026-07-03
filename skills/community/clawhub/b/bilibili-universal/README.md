# bilibili-universal

> B 站抓取 skill（GitHub 仓库名是 `bilibili-search`，因为 ClawHub 上 `bilibili-search` slug 已被别人占用，所以在 ClawHub 上以 `@excalibursssooo/bilibili-universal` 形式发布）

bilibili 内容抓取 skill。统一走 agent-browser + 公开 API，让浏览器帮我们处理 buvid cookie 和 wbi 签名环境。

> **不强制登录** — 默认未登录态就能跑通 80% 用例（搜索 / UP 主空间 / 视频详情 / 评论）。

## 安装

### ClawHub (推荐)

```bash
# 仓库内路径 (已安装)
openclaw skills install @excalibursssooo/bilibili-universal
# 或通过 clawhub CLI
clawhub install bilibili-universal
```

### GitHub 直接 git clone

```bash
git clone https://github.com/excalibursssooo/bilibili-search.git
cd bilibili-search
python3 bili-fetch.py --help
```

## 5 个核心命令

```bash
# 1. 主题搜索
python3 bili-fetch.py search "逗比的雀巢" --order pubdate --pages 2

# 2. 用户名 → mid 解析
python3 bili-fetch.py user-search "逗比的雀巢"

# 3. UP 主主页 + 视频列表 (走 SPA)
python3 bili-fetch.py user 5294454 --videos 40

# 4. 单视频详情 + 评论
python3 bili-fetch.py video BV1K3Gz6pEoo --comments 20

# 5. 深翻评论
python3 bili-fetch.py comments BV1K3Gz6pEoo --ps 50 --pages 5

# + 收割编排 (一条命令 → 落盘 + REPORT.md)
python3 bili-harvest.py user 5294454 --videos 40 --comments 20
python3 bili-harvest.py hot "逗比的雀巢" --order pubdate --limit 10
python3 bili-harvest.py ids BV1K3Gz6pEoo BV16ooQBsERA
```

**`bili-harvest.py`** 编排工作流（增量+断点+限速+报告全包），**`bili-fetch.py`** 原子操作（细粒度控制）。

## 快速开始

```bash
# 不需要 cookie，直接跑
python3 bili-fetch.py search "AI" --order pubdate --pages 1
python3 bili-fetch.py video BV1K3Gz6pEoo --comments 10

# 想拿更高画质/关注状态? 注入 cookie (可选)
echo "buvid3=xxx; SESSDATA=xxx; bili_jct=xxx; ..." > data/cookies-raw.txt
chmod 600 data/cookies-raw.txt
# 用 agent-browser --state 或手动加载
```

## 核心优势

- **零反爬负担**：复用浏览器内置 wbi 签名环境，不用算 w_rid
- **不强制登录**：未登录态跑通所有核心命令
- **skill 自包含**：git clone 即用，数据全在 `data/` 下
- **env 覆盖**：`BI_DATA_DIR` / `BI_COOKIE_FILE` 给 docker / CI 用
- **双层架构**：`bili-fetch.py` 原子 + `bili-harvest.py` 编排

## cookie 生命周期

| 字段 | 有效期 | 用途 |
|---|---|---|
| `buvid3` | **数月** | 设备指纹，未登录也能用 |
| `SESSDATA` | 数天-数周 | 登录态（拿 1080P / 评论权限） |
| `bili_jct` | 同 SESSDATA | CSRF，写操作需要 |

**体感**：完全没必要主动注入 cookie，除非要登录态专属数据。

## 路径与风控

| 路径 | 用途 | 风控 |
|---|---|---|
| `/x/web-interface/view` | 视频详情 | 🟢 弱 |
| `/x/v2/reply/main` | 评论 | 🟢 弱 |
| `/x/web-interface/search/type` | 搜索 | 🟡 中 (search 桶偶发 captcha) |
| `space.bilibili.com/{mid}/upload/video` | UP 主空间 SPA | 🟢 弱 |
| `/x/space/wbi/arc/search` | UP 主空间 API | 🔴 强 (本 skill 不用) |

详细决策规则见 [SKILL.md](./SKILL.md)。

## 与其他 skill 的差异

| 维度 | douyin | zhihu | xhs | **bilibili** |
|---|---|---|---|---|
| 抓取路径 | HTTP API | HTTP API | agent-browser only | **agent-browser + 公开 API** |
| 必填 cookie | ttwid | z_c0 | a1+web_session | **❌ 不强制** |
| 风控强度 | 中 | 弱 | 强 | **中** |

## 详细文档

- [SKILL.md](./SKILL.md) — 给 LLM agent 用的完整文档
- [docs/pitfalls.md](./docs/pitfalls.md) — 反爬坑 / 调试笔记
- [CHANGELOG.md](./CHANGELOG.md) — 版本历史
- [CONTRIBUTING.md](./CONTRIBUTING.md) — 贡献指南

## License

MIT