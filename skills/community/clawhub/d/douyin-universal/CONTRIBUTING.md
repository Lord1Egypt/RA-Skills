# Contributing to douyin-search

这份文档面向 **skill 维护者 / 贡献者**。用户视角的文档见 [README.md](README.md)。

---

## 架构总览

```
douyin-search/
├── SKILL.md                       # skill frontmatter + agent 决策入口(128 行)
├── README.md                      # GitHub 产品页
├── CONTRIBUTING.md                # ← 你在这里
├── CHANGELOG.md
├── LICENSE
├── douyin-fetch.py                # 主入口: search / user / video
├── comments-harvest.py            # 深度评论抓取
├── aggregate.py                   # 跨次会话聚合去重（search + harvest 后处理）
├── downloader.py                  # 视频下载 helper（detail API → play_addr URL → 流式下载）
├── keepalive.py                   # cookies / state 管理
├── paths.py                       # ⭐ 路径统一管理(所有脚本都引)
├── docs/
│   └── pitfalls.md                # 开发者参考(目录结构、反爬坑、脚本实现细节)
├── .gitignore
├── .github/workflows/test.yml     # CI: lint + smoke test + publish
└── data/                          # 运行时数据(.gitignore 排除,只留 .gitkeep)
    ├── .gitkeep
    ├── cookies-raw.txt            # 原始 cookies
    ├── cookies.txt                # Netscape 格式
    ├── state/douyin.state         # agent-browser session
    └── exports/                   # 抓取结果
```

### 关键设计决定

**1. 路径统一管理 (`paths.py`)**
所有路径在 `paths.py` 解析,优先级:`DOUYIN_DATA_DIR` env > 老的 `/tmp/douyin/` > 默认 `$SKILL/data/`。
改路径只改 `paths.py` 一个文件,三个脚本都用 `from paths import ...`。

**2. 抓取策略双模式**
- **人类模式**(默认): `scrollBy(0, 200-500px)` + 1.5-5s sleep + 10% 概率长停留 2-6s + 15 round 上限
- **激进模式** (`--aggressive`): `scrollTop = scrollHeight` + 0.9s sleep + 25 round 上限

理由: 抖音风控监控行为节奏,1 秒内 25 次 jump 是明显脚本特征。人类模式用 `scrollBy` 模拟手指拨动,行为更接近真人。

**3. Incremental harvest**
单次 ab eval 不能 > 30s,否则 ab daemon 5 次重试都失败。所以把 harvest 拆成:
- harvest 阶段: 每 round 一次 eval,状态存 `window.__hc` 全局变量
- dump 阶段: `localStorage` 中转评论数据,每 20 条一个 chunk
- Python 循环读 chunk

**4. Douyin DOM 特殊性**
评论 item innerText 固定格式: `user\n...\ntext\ntime\nlikes\n操作按钮`
- 第二行 `...` 是 douyin UI 占位符(被忽略的@/缩进),**不是被截断**
- 必须显式 skip `"..."` / `"回复"` / `"展开N条回复"` 等 UI 词,否则会拿到占位符当 text
- 评论容器 selector: `.parent-route-container.route-scroll-container`(不是 `document.body`)

**5. ab 串行硬性要求**
agent-browser 单 tab 单 session,多个 harvest 命令必须 `&&` 或 `;` 串行,并行会全部拿到第一条的评论。

---

## 工程经验(踩过的坑)

| 问题 | 解决 |
|---|---|
| `keepalive.py check` 报 captcha | state 过期 / 当前 IP 被风控,等 30s 重 `state save` |
| 老的 `comments-harvest.py` 单 eval > 30s 触发 ab busy | 拆成 incremental,每 round 一次 eval |
| ab eval 输出 JSON 字段被截断成 `"..."` | localStorage 中转 + 分批 read |
| `state save` 之后 `--state` 被忽略 | daemon 抢占,手动 `agent-browser close && sleep 2` |
| 多个 video 命令并发 | 全部拿到第一条的评论,必须串行 `&&` |
| 解析评论 text 拿到 `"..."` | 漏了 skip 那个 UI 占位符,加上 `l === '...'` 检查 |
| 中文乱码 | ab eval 输出双重转义,用 `json.loads(json.loads(s))` |
| cookies 失效后 `search` 返回 0 | 大概率 cookie 过期,重新走 setup |

---

## 本地测试

```bash
# 语法 + lint
python3 -c "import ast; [ast.parse(open(f).read()) for f in ['douyin-fetch.py', 'comments-harvest.py', 'keepalive.py', 'paths.py']]"
pyflakes *.py

# 脚本可执行
python3 comments-harvest.py --help
python3 douyin-fetch.py --help
python3 keepalive.py --help

# 路径解析
python3 -c "import sys; sys.path.insert(0, '.'); from paths import report; print(report())"

# 用真实 cookies 测一遍
python3 keepalive.py check              # 退出码 0 = OK
python3 douyin-fetch.py search "测试" --type video --limit 3
python3 comments-harvest.py <某 video id> --max 50
```

---

## 发布到 ClawHub

### 前置
- GitHub 账号
- clawhub CLI: `npm install -g @openclaw/clawhub-cli`
- 登录: `clawhub login`(浏览器 OAuth)

### 首次发布
```bash
# 1. 创建 GitHub repo
gh repo create douyin-search --public --source=. --push

# 2. 配置 CLAWHUB_TOKEN secret
#    → GitHub repo → Settings → Secrets → CLAWHUB_TOKEN

# 3. 本地发布
clawhub inspect .              # 先验证 SKILL.md 解析
clawhub skill publish .        # 发布(首次)
```

### 版本迭代
```bash
# 1. 改代码 + 更新 CHANGELOG.md
# 2. commit + tag
git add -A
git commit -m "Release v1.0.1: <改动>"
git tag v1.0.1
git push --tags

# 3. CI (.github/workflows/test.yml) 自动:
#    - 跑 lint + smoke test
#    - 如果 tag 格式 v*,发布到 ClawHub
```

### 发布前手动 checklist
- [ ] CHANGELOG.md 更新
- [ ] README.md 里的 GitHub 链接指向自己的 repo
- [ ] SKILL.md frontmatter `name` 跟 clawhub slug 一致
- [ ] 本地 dry-run: `clawhub inspect .` 通过
- [ ] GitHub repo 配了 `CLAWHUB_TOKEN` secret
- [ ] `.github/workflows/test.yml` 的 publish job CLI 命令按 clawhub 最新文档调整(目前是占位)

### 必要的 frontmatter 字段
clawhub 要求 SKILL.md 有 YAML frontmatter,最少包含:
```yaml
---
name: skill-slug
description: 一句话描述
metadata:
  openclaw:
    requires:
      env: []           # 必需的环境变量
      bins: []           # 必需的 CLI 工具
      primaryEnv: ""     # 主要 env(用于文档)
      primaryBin: ""     # 主要 bin
---
```

完整参考: https://clawhub.ai/docs/skill-format

---

## 安全 / 法律边界

- 本 skill **只读**,不修改 douyin 任何数据
- 不抓取私密内容(关注列表、收藏、好友)
- 用户需自行遵守:
  - 抖音用户协议
  - 《数据安全法》《个人信息保护法》/ GDPR
  - 不得商业转售 douyin 内容 / 构建竞品 / 任何非法用途
- 贡献 PR 时请保持"只读"原则

---

## 贡献方向

欢迎 PR:
- 新增搜索维度(按时间/地区过滤)
- 优化虚拟滚动 harvest 策略
- 修复 captcha 处理流程
- 翻译文档(i18n)
- 适配小红书 / 微博(同一套虚拟滚动 harvest 思路)
