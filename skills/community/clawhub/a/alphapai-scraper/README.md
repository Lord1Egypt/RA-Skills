# AlphaPai 全市场点评抓取与检索 Skill

这个版本的升级，重点解决 9 件事：

1. 自动登录 Alpha派，支持 `USER_AUTH_TOKEN`、`cookies.json`、账号密码、storage state、Chrome Profile
2. 浏览器抓取有优先方案和备选方案，不再依赖单一路径
3. 原文、结构化记录、索引库、摘要保存到固定目录，便于归档和迁移
4. 支持“最近 N 小时”抓取，默认 1 小时
5. 每次抓取后会自动把每条点评拆成结构化记录并写入 SQLite + FTS5
6. 支持查询“最近 N 天关于某个主题/标的的所有点评”，默认 7 天
7. 生成手机友好的抓取摘要和查询摘要，强调增量信息和边际变化
8. 查询时支持 `exact / vector / hybrid` 三种模式，默认走混合召回
9. 可以生成一份不含本地密钥的可发布副本，方便后续上 ClawHub

## 当前能力边界

现在已经是混合检索：

- 抓取后归档到 `raw/ + normalized/ + index/`
- 精确索引使用 `SQLite + FTS5`
- 向量索引使用本地 `Chroma + bge-small-zh-v1.5`
- 查询时先按最近 N 天过滤，再合并精确匹配和向量召回
- 内置少量实体别名，例如 `英伟达 / NVIDIA / NVDA / Blackwell / GB200`
- 如果没有命中，固定返回：`alphapai最近N天没有相关点评`

当前还没有做更强的 rerank 和否定句去噪，所以像“与英伟达无直接关系”这种文本，仍可能因为命中关键词而被召回。

## 推荐认证顺序

- 首选：已缓存 `storage_state`
- 次选：`USER_AUTH_TOKEN`
- 再次：`cookies.json`
- 再兜底：账号密码
- 最后兜底：本机 Chrome Profile

原因很简单：

- 缓存的 `storage_state` 对本机日常使用最稳
- `USER_AUTH_TOKEN` 最可迁移，适合别人一键复制流程
- `cookies.json` 也比较稳，但会受过期和导出格式影响
- 账号密码最容易碰到验证码或表单改版
- Chrome Profile 最适合你本机调试，不适合直接分发

## 浏览器抓取顺序

浏览器启动：

1. Playwright 无状态浏览器
2. 本机 Chrome Profile 兜底

正文提取：

1. 点击点评条目抓弹窗正文
2. 打开详情链接抓正文
3. 回退抓卡片正文

## 固定输出目录

公开版默认输出目录：

`~/.openclaw/data/alphapai-scraper`

目录结构如下：

```text
<base_dir>/
  raw/
  normalized/
  index/
  reports/
  runtime/
```

其中：

- `raw/` 保存原文抓取文件
- `normalized/` 保存结构化 JSON 归档
- `index/alphapai.sqlite` 保存全文检索索引
- `index/vector/` 保存向量索引
- `reports/` 保存抓取摘要和查询摘要
- `runtime/` 保存调试和元数据文件

## 首次配置

复制这些示例文件并填入你自己的信息：

```bash
cp config/settings.example.json config/settings.local.json
cp config/token.example.json config/token.local.json
cp config/cookies.example.json config/cookies.local.json
cp config/credentials.example.json config/credentials.local.json
```

你不需要四种都填。
只要填你最终决定采用的一种认证方式即可。

也可以直接用初始化脚本生成本地配置：

```bash
python3 scripts/init_config.py \
  --output-dir ~/.openclaw/data/alphapai-scraper \
  --default-hours 1 \
  --custom-requirements "按行业分组，重点强调加单/涨价/公告/订单"
```

## 运行

默认抓最近 1 小时：

```bash
python3 scripts/run.py
```

抓最近 3 小时：

```bash
python3 scripts/run.py --hours 3
```

查询最近 7 天关于英伟达的归档点评：

```bash
python3 scripts/run.py --query 英伟达 --days 7
```

强制只走向量模糊召回：

```bash
python3 scripts/run.py --query 英伟达 --days 7 --query-mode vector
```

默认推荐的混合召回：

```bash
python3 scripts/run.py --query 英伟达 --days 7 --query-mode hybrid
```

如果想看真实浏览器过程：

```bash
python3 scripts/run.py --hours 3 --headed
```

如果只生成本地文件，不发飞书：

```bash
python3 scripts/run.py --skip-feishu
```

## 一次性人工登录缓存会话

如果 token 失效、cookies 过期、账号密码登录又碰到验证码，可以先本地执行一次：

```bash
python3 scripts/bootstrap_session.py
```

它会打开真实浏览器让你手动登录，登录成功后自动保存 storage state 和 cookies 备份。之后再跑 `run.py` 时，会优先复用这份缓存会话。

## 摘要格式

抓取摘要会尽量稳定输出下面这套结构，目标总字数约 1000 字：

```text
# Alpha派摘要
## 今日结论
## 边际变化 / 增量信息 TOP5
## 行业 / 标的脉络
## 情绪温度计
## 待验证
```

查询摘要会尽量稳定输出下面这套结构：

```text
# AlphaPai 检索摘要
## 检索结论
## 时间线 / 重点更新
## 行业 / 标的归类
## 边际变化
## 待验证
```

两类摘要都强调：

- 增量信息和边际变化
- 行业或标的清晰分类
- 适合手机阅读
- 重点公司和关键词加粗

## 飞书发送

如果你配置了：

- `feishu.enabled=true`
- `feishu.webhook_url`

脚本会自动把抓取摘要或查询摘要发到飞书 webhook。

## 打包成可发布版本

发布前先生成一个不含本地 secrets 的副本：

```bash
python3 scripts/package_skill.py
```

默认输出到：

```bash
../dist/alphapai-scraper
```

这个副本会排除：

- `token.json`
- `token.local.json`
- `cookies.local.json`
- `credentials.local.json`
- `settings.local.json`

后续如果要推到 ClawHub，建议只用这个副本去发布。

## 一键发布到 ClawHub

准备好 ClawHub CLI 并登录后，可以直接执行：

```bash
python3 scripts/publish_skill.py \
  --slug alphapai-scraper \
  --name "AlphaPai 评论抓取" \
  --version 0.2.0 \
  --changelog "Add hybrid retrieval with local vector index"
```

这个脚本会先生成去敏 dist 目录，再调用 `clawhub publish`。
