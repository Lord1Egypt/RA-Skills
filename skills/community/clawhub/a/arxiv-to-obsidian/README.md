# arxiv-to-obsidian

把 arXiv `cs.AI` 分类中最新发布的论文抓取下来，翻译标题和摘要为简体中文，并通过 Obsidian CLI 追加到 Obsidian 中的今日笔记。

这个 skill 的默认目标是：

```text
402论文资料/YYYY-MM-DD.md
```

追加到笔记末尾的内容格式为：

```markdown
## 今日AI论文

| 标题（中文） | 摘要（中文） | 原文链接 | 发布日期 |
| ------ | ------ | ---- | ---- |
| ... | ... | ... | ... |
```

## 功能

- 从 `https://export.arxiv.org/rss/cs.AI` 获取论文
- 按发布时间倒序排序
- 只保留最新 10 篇论文
- 翻译标题和摘要为简体中文
- 摘要不截断
- 通过 Obsidian CLI 写入或追加到指定笔记

## 适合谁用

适合已经在用 Obsidian 做 AI 论文整理、文献摘录、日报归档的人。

如果你希望每天把最新 arXiv AI 论文整理成中文表格，直接写入固定笔记目录，这个 skill 就是为这个场景准备的。

## 前提条件

使用前需要确认你的环境满足以下条件：

- 已安装 [Obsidian](https://obsidian.md/)
- Obsidian 已开启 CLI，终端中可以运行 `obsidian`
- 终端中可以运行 `claude`
- 已安装 `python3`
- 已安装 `curl`

可以先在终端自测：

```bash
obsidian help
claude -p "只输出 ok"
python3 --version
curl --version
```

## 安装

把这个仓库放到你的 Claude skills 目录中：

```bash
git clone <你的仓库地址> ~/.claude/skills/arxiv-to-obsidian
```

如果你已经下载到别的目录，也可以自己移动过去：

```bash
mv /你的下载目录/arxiv-to-obsidian ~/.claude/skills/arxiv-to-obsidian
```

## 第一次使用前必须做的事

这一段最重要。

**如果其他人下载这个 skill，第一件事不是直接运行，而是先修改配置文件。**

配置文件在：

[`scripts/config.sh`](./scripts/config.sh)

请先打开它：

```bash
nano ~/.claude/skills/arxiv-to-obsidian/scripts/config.sh
```

或者：

```bash
vim ~/.claude/skills/arxiv-to-obsidian/scripts/config.sh
```

## 必须修改的配置

其他人下载后，至少要确认下面这 3 项：

```bash
VAULT_NAME="你的Vault名称"
VAULT_FOLDER="你的文件夹路径"
NOTE_NAME="你的笔记文件名"
```

其中最容易出错的是前两项。

### 1. `VAULT_NAME`

这个值必须改成你自己 Obsidian 里的 **Vault 名称**。

默认值是：

```bash
VAULT_NAME="${VAULT_NAME:-AI}"
```

如果你的 vault 不叫 `AI`，那就必须改掉，否则 skill 会写入失败，或者写到错误的 vault。

例如你的 vault 叫 `KnowledgeBase`，就应该改成：

```bash
VAULT_NAME="${VAULT_NAME:-KnowledgeBase}"
```

### 2. `VAULT_FOLDER`

这个值必须改成你想写入的 **目标文件夹路径**。

默认值是：

```bash
VAULT_FOLDER="${VAULT_FOLDER:-402论文资料}"
```

如果你的 Obsidian 里没有 `402论文资料` 这个目录，或者你实际想写到别的目录，就必须改成你自己的路径。

例如你想写到：

```text
文献/AI/arXiv日报
```

那就改成：

```bash
VAULT_FOLDER="${VAULT_FOLDER:-文献/AI/arXiv日报}"
```

### 3. `NOTE_NAME`

默认值是：

```bash
NOTE_NAME="${NOTE_NAME:-$(date +%Y-%m-%d).md}"
```

这表示默认写入：

```text
402论文资料/2026-03-20.md
```

如果你不想按日期命名，而是想固定写入某个笔记，比如：

```text
今日AI论文.md
```

就改成：

```bash
NOTE_NAME="${NOTE_NAME:-今日AI论文.md}"
```

## 推荐配置示例

如果你是第一次使用，建议按你自己的环境改成类似这样：

```bash
VAULT_NAME="${VAULT_NAME:-MyResearchVault}"
VAULT_FOLDER="${VAULT_FOLDER:-文献/AI/arXiv日报}"
NOTE_NAME="${NOTE_NAME:-$(date +%Y-%m-%d).md}"
PAPER_COUNT="${PAPER_COUNT:-10}"
ARXIV_RSS_URL="${ARXIV_RSS_URL:-https://export.arxiv.org/rss/cs.AI}"
DRY_RUN="${DRY_RUN:-0}"
```

## 配置文件完整说明

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `VAULT_NAME` | `AI` | Obsidian 的 vault 名称。通常必须改。 |
| `VAULT_FOLDER` | `402论文资料` | 目标文件夹路径。通常必须改。 |
| `NOTE_NAME` | `YYYY-MM-DD.md` | 写入的笔记名称。 |
| `PAPER_COUNT` | `10` | 获取论文数量。 |
| `ARXIV_RSS_URL` | `https://export.arxiv.org/rss/cs.AI` | RSS 来源。 |
| `DRY_RUN` | `0` | 设为 `1` 时只预览，不写入 Obsidian。 |

## 强烈建议先做 Dry Run

在正式写入之前，先跑一次预览：

```bash
cd ~/.claude/skills/arxiv-to-obsidian/scripts
DRY_RUN=1 ./fetch-arxiv.sh
```

这样你可以先确认三件事：

- 抓取的 RSS 是否正常
- 翻译是否正常
- 目标路径是否是你预期的路径

如果输出里显示的 `Vault`、`Folder`、`Note` 不对，就先回去改 `config.sh`，不要直接正式运行。

## 如何在 Claude 中使用

安装并配置好之后，可以直接在 Claude Code 里说：

```text
获取今日 arXiv 论文
```

或者：

```text
帮我把今天的 arXiv AI 论文写入 Obsidian
```

或者：

```text
抓取 arXiv 最新 AI 论文并追加到今日日记
```

## 如何手动运行

如果你想直接在终端里执行：

```bash
cd ~/.claude/skills/arxiv-to-obsidian/scripts
./fetch-arxiv.sh
```

## 环境变量覆盖示例

你也可以临时覆盖配置，而不改 `config.sh`：

```bash
cd ~/.claude/skills/arxiv-to-obsidian/scripts
VAULT_NAME="MyResearchVault" VAULT_FOLDER="文献/AI/arXiv日报" DRY_RUN=1 ./fetch-arxiv.sh
```

这适合测试不同目录，或者临时写入另一个 vault。

## 输出示例

生成并追加的内容示例如下：

```markdown
## 今日AI论文

| 标题（中文） | 摘要（中文） | 原文链接 | 发布日期 |
| ------ | ------ | ---- | ---- |
| 深度不确定性下社会环境规划中的生成式人工智能辅助参与式建模 | 深度不确定性下的社会环境规划要求研究人员在探索政策和部署计划之前首先识别并概念化问题。...完整摘要... | https://arxiv.org/abs/2603.17021 | 2026-03-19 |
| Transformers 是贝叶斯网络 | Transformers 是人工智能领域的主导架构，但其为何有效仍缺乏充分理解。...完整摘要... | https://arxiv.org/abs/2603.17063 | 2026-03-19 |
```

## 常见问题

### 1. 提示 `Vault not found`

说明 `VAULT_NAME` 配错了。

先去 Obsidian 里确认你的 vault 真名，再修改：

```bash
VAULT_NAME="${VAULT_NAME:-你的真实Vault名称}"
```

### 2. 写入到了错误的文件夹

说明 `VAULT_FOLDER` 配错了。

请把它改成你 Obsidian 里真实存在、并且你希望写入的目录路径。

### 3. 文件名不符合你的习惯

修改 `NOTE_NAME`。

例如固定写入某个文件：

```bash
NOTE_NAME="${NOTE_NAME:-今日AI论文.md}"
```

### 4. 我只想测试，不想真的写入

用：

```bash
DRY_RUN=1 ./fetch-arxiv.sh
```

### 5. 运行时报 `claude` 或 `obsidian` 找不到

先确认这两个命令在终端里可直接执行。
如果命令本身都不存在，skill 无法工作。

## 文件结构

```text
arxiv-to-obsidian/
├── README.md
├── SKILL.md
└── scripts/
    ├── config.sh
    ├── fetch-arxiv.sh
    ├── parser.py
    └── translator.py
```

## 对其他下载者的最短说明

如果你准备把这个 skill 分享给别人，请至少提醒对方：

1. clone 到 `~/.claude/skills/arxiv-to-obsidian`
2. 先改 `scripts/config.sh`
3. 一定要检查 `VAULT_NAME`
4. 一定要检查 `VAULT_FOLDER`
5. 先运行 `DRY_RUN=1 ./fetch-arxiv.sh`
6. 确认没问题后再正式运行
