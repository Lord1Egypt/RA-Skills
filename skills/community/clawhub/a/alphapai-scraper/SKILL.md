---
name: alphapai-scraper
description: 登录 Alpha派并抓取最近 N 小时点评，保存原文、结构化归档并建立本地索引；也可以用精确检索、向量检索或混合检索查询最近 N 天的历史点评库并生成手机友好摘要，可选发送到飞书。
---

# AlphaPai Scraper

这个 skill 现在包含两类能力：

1. 抓取 Alpha派最近 N 小时点评，保存原文、结构化记录、摘要
2. 查询已经归档的 Alpha派点评库，按主题和时间窗口生成检索摘要

## 何时使用

- 用户要抓取 Alpha派最近 1 小时或最近 N 小时点评
- 用户要自动登录 Alpha派并复用 token / cookies / 账号密码
- 用户要把原文归档成可检索的本地索引
- 用户要问“最近一周关于英伟达的所有点评”这类历史查询
- 用户要把摘要发回飞书
- 用户要把这个 skill 打包成可迁移、可发布的版本

## 默认规则

- 如果用户没有指定时间窗口，默认抓取最近 `1` 小时
- 如果用户明确说“抓最近 3 小时”，运行时传 `--hours 3`
- 如果用户要查询历史点评库，默认查最近 `7` 天
- 原文、结构化记录、索引库、摘要默认都保存到 `~/.openclaw/data/alphapai-scraper`
- 飞书发送默认关闭，只有配置了 webhook 才发送

## 认证优先级

优先按下面顺序尝试，成功一个就继续：

1. 已缓存 storage state
2. `USER_AUTH_TOKEN`
3. `cookies.json`
4. `账号密码`
5. 本机 Chrome Profile

如果目的是“最稳且最可迁移”，优先向用户要 `USER_AUTH_TOKEN`。
如果 token 没有，再要 `cookies.json`。
账号密码方案留作最后，因为可能遇到验证码或页面变更。
如果用户愿意做一次人工登录引导，也可以运行 `scripts/bootstrap_session.py` 先缓存会话，后续任务直接复用。

## 首次配置

优先只读以下文件，不要把示例文件整段贴回对话：

- `config/settings.example.json`
- `config/token.example.json`
- `config/cookies.example.json`
- `config/credentials.example.json`

首次使用时，让用户把示例文件复制为本地文件并填写：

- `config/settings.local.json`
- `config/token.local.json`
- `config/cookies.local.json`
- `config/credentials.local.json`

已有旧版 `config/token.json` 时，脚本也会兼容读取。
如果想快速初始化，也可以直接运行 `scripts/init_config.py` 生成 `settings.local.json`。

## 运行方式

标准抓取：

```bash
python3 /Users/bot/.openclaw/workspace/skills/alphapai-scraper/scripts/run.py --hours 1
```

查询最近 7 天关于英伟达的点评：

```bash
python3 /Users/bot/.openclaw/workspace/skills/alphapai-scraper/scripts/run.py --query 英伟达 --days 7
```

如果用户明确想只走向量模糊召回：

```bash
python3 /Users/bot/.openclaw/workspace/skills/alphapai-scraper/scripts/run.py --query 英伟达 --days 7 --query-mode vector
```

如果想看浏览器过程，追加：

```bash
--headed
```

如果只要文件，不发飞书，追加：

```bash
--skip-feishu
```

## 抓取策略

浏览器启动优先顺序：

1. Playwright 无状态浏览器
2. 本机 Chrome Profile 兜底

内容提取优先顺序：

1. 点击条目抓弹窗正文
2. 打开详情链接抓正文
3. 回退到卡片正文

## 输出

- 原文：`<output.base_dir>/raw/YYYYMMDD_HHMMSS.md|txt`
- 结构化：`<output.base_dir>/normalized/YYYYMMDD_HHMMSS.json`
- 索引库：`<output.base_dir>/index/alphapai.sqlite`
- 向量索引：`<output.base_dir>/index/vector/`
- 摘要：`<output.base_dir>/reports/YYYYMMDD_HHMMSS_summary.md|txt`
- 查询摘要：`<output.base_dir>/reports/YYYYMMDD_HHMMSS_query_summary.md`
- 运行元数据：`<output.base_dir>/runtime/*.json`

## 查询规则

- 默认使用 `hybrid` 模式，合并 `SQLite + FTS5` 精确检索和本地 `Chroma` 向量召回
- 如果用户明确要“只精确搜”或“只模糊搜”，可以分别传 `--query-mode exact` 或 `--query-mode vector`
- 会先按最近 N 天过滤，再对标题和正文做全文检索，并补充向量召回
- 内置少量实体别名，例如 `英伟达 / NVIDIA / NVDA / Blackwell / GB200`
- 如果没有命中，固定返回：`alphapai最近N天没有相关点评`

## 飞书

如果 `feishu.enabled=true` 且配置了 `webhook_url`，脚本会自动发送抓取摘要或查询摘要。
如果没有 webhook，只保留本地文件。

## 打包与发布

发布前不要直接上传带有真实 token/cookies 的技能目录。

先执行：

```bash
python3 /Users/bot/.openclaw/workspace/skills/alphapai-scraper/scripts/package_skill.py
```

这会生成一个去敏后的可发布副本，默认输出到：

```bash
/Users/bot/.openclaw/workspace/skills/dist/alphapai-scraper
```

后续如果用户确认已经登录 ClawHub，再用这个去敏副本发布。
如果本机已经安装并登录 ClawHub，也可以直接运行 `scripts/publish_skill.py` 一键发布。
