---
name: baijiahao-publish
version: 1.0.0
description: 使用 auth 登录态打开百家号发布页，可填入标题与正文（支持 .md 转富文本）、选封面、存草稿或发布。当用户需要发布百家号、用 cookie 打开编辑页、或配合 OpenClaw 自动发布/存草稿时使用。
author: Maynor
license: MIT
tags: ["baijiahao", "publish", "automation", "playwright"]
entry: scripts/open_baijiahao_edit.py
language: python
requirements:
  - playwright>=1.40.0
  - markdown>=3.5.0
user-invocable: true
metadata: '{"openclaw":{"skillKey":"baijiahao-publish","requires":{"bins":["python3"]}}}'
---

# 百家号自动发布 Skill

## 用途

本 Skill 提供：用已有登录态打开百家号发布页，自动关闭常见弹窗，可选填入标题与正文（支持 Markdown 文件转富文本 HTML），可选选封面后点击「存草稿」或「发布」。

发布页地址：`https://baijiahao.baidu.com/builder/rc/edit?type=news&is_from_cms=1`

---

## 环境准备

### 1. Python

需要 Python 3.8+，建议 3.10+。

### 2. 安装依赖

在项目根或任意可运行脚本的目录执行：

```bash
# 安装 Python 包（Playwright + Markdown）
pip install -r skills/baijiahao-publish/requirements.txt

# 安装浏览器（必须执行一次）
playwright install chromium
```

或手动安装：

```bash
pip install playwright>=1.40.0
pip install markdown>=3.5.0
playwright install chromium
```

说明：

- **playwright**：打开浏览器并操作百家号页面，`playwright install chromium` 会下载 Chromium，只需执行一次。
- **markdown**：使用 `--content-file xxx.md` 时，将 Markdown 转为富文本 HTML 填入正文，必装。

### 3. 准备 auth（二选一）

- **auth.json**：在浏览器中登录百度/百家号后，用 Playwright 的 `context.storage_state(path="auth.json")` 保存状态。
- **Cookie 文本 .txt**：一行 Cookie，格式可为 `name1=value1; name2=value2; ...` 或 `账号----账号----cookie字符串`，脚本会自动解析并注入。

`--auth` 支持**相对路径和绝对路径**；路径若从别处粘贴，会自动去掉常见不可见字符。

---

## 如何调用

### 脚本路径

入口脚本：`skills/baijiahao-publish/scripts/open_baijiahao_edit.py`

在**项目根**或能访问到该路径的目录下执行下面的命令（或将 `skills/baijiahao-publish/scripts/open_baijiahao_edit.py` 换成绝对路径）。

### 参数说明

| 参数 | 说明 |
|------|------|
| `--auth` | 登录态文件路径，默认 `auth.json`。支持相对路径与绝对路径。 |
| `--headless` | 无头模式（不显示浏览器窗口）。 |
| `--title` | 文章标题，填入页面标题框。 |
| `--content` | 正文纯文本，直接填入编辑区。 |
| `--content-file` | 正文来源文件。若为 `.md` 会转为富文本 HTML 填入（依赖 markdown 库）；否则按纯文本读取。与 `--content` 二选一，优先本参数。支持绝对路径。 |
| `--strip-title-from-content` | 当同时提供 `--title` 和 `--content-file` 时，在文件中用标题做第一次匹配并截断，只把该行之后的内容当正文，避免标题重复。 |
| `--publish` | 填完正文后：等 2 秒 → 选择封面 → 确定 → 等 2 秒 → 按文字完全匹配点击「发布」。 |
| `--draft` | 与 `--publish` 流程相同，但最后按文字完全匹配点击「存草稿」。 |
| `--keep-open` | 执行完成后不立即关闭浏览器，等待用户按回车确认后再关闭；未指定则执行完直接关闭并返回结果。 |

**执行结果**：脚本结束前会输出一行 `[RESULT] success` 或 `[RESULT] failed`，进程退出码分别为 0 / 1，便于 OpenClaw 或其它调用方解析。默认执行完即关闭浏览器并返回，无需人工确认。

### 调用示例

```bash
# 仅打开发布页（使用默认或指定 auth）
python skills/baijiahao-publish/scripts/open_baijiahao_edit.py
python skills/baijiahao-publish/scripts/open_baijiahao_edit.py --auth test/baijiahao.txt
python skills/baijiahao-publish/scripts/open_baijiahao_edit.py --auth "C:/path/to/baijiahao.txt"

# 填入标题 + 正文（MD 转富文本）
python skills/baijiahao-publish/scripts/open_baijiahao_edit.py --auth test/baijiahao.txt --title "文章标题" --content-file article.md

# MD 里自带标题，用 --title 截断后只把后面当正文
python skills/baijiahao-publish/scripts/open_baijiahao_edit.py --auth test/baijiahao.txt --title "文章标题" --content-file article.md --strip-title-from-content

# 填完后选封面并发布
python skills/baijiahao-publish/scripts/open_baijiahao_edit.py --auth test/baijiahao.txt --title "标题" --content-file article.md --strip-title-from-content --publish

# 填完后选封面并存草稿
python skills/baijiahao-publish/scripts/open_baijiahao_edit.py --auth test/baijiahao.txt --title "标题" --content-file article.md --draft

# 无头模式（不弹浏览器）
python skills/baijiahao-publish/scripts/open_baijiahao_edit.py --auth test/baijiahao.txt --headless

# 执行完后不关浏览器，等用户按回车再关闭（便于人工确认）
python skills/baijiahao-publish/scripts/open_baijiahao_edit.py --auth test/baijiahao.txt --title "标题" --content-file article.md --keep-open
```

### 在 OpenClaw 中调用

1. **放置 Skill**  
   将本 Skill 目录放在 OpenClaw 会加载的位置，例如：
   - 工作区：`<workspace>/skills/baijiahao-publish/`
   - 或全局：`~/.openclaw/skills/baijiahao-publish/`

2. **调用方式**  
   - **自然语言**：对助手说「用 test/baijiahao.txt 打开百家号并发布」「用 article.md 填标题和正文然后存草稿」等，由模型解析后执行上述脚本并传入对应参数（如 `--auth`、`--title`、`--content-file`、`--strip-title-from-content`、`--publish` 或 `--draft`）。  
   - **斜杠命令**：若该 Skill 配置为可被用户调用，可在对话中使用对应斜杠命令。  
   - **CLI**：在终端直接执行上面的 `python skills/baijiahao-publish/scripts/open_baijiahao_edit.py ...`，不依赖 OpenClaw。

3. **传参约定**  
   - 说明 auth 路径时，助手应传 `--auth <路径>`（支持绝对路径）。  
   - 说明「存草稿」时传 `--draft`；说明「发布」时传 `--publish`。  
   - 说明「正文用某 md 文件」时传 `--content-file <路径>`；若 md 里含标题且希望截断，同时传 `--title <标题>` 与 `--strip-title-from-content`。  
   - 需要「执行完不关浏览器、等用户确认再关」时传 `--keep-open`；未传则执行完直接关闭并输出 `[RESULT] success` / `[RESULT] failed` 与退出码，便于 OpenClaw 正确处理返回。

---

## 脚本与依赖位置

- 入口脚本：`skills/baijiahao-publish/scripts/open_baijiahao_edit.py`
- 依赖列表：`skills/baijiahao-publish/requirements.txt`（playwright、markdown）

## OpenClaw 安装与上传

- **手动安装**：将本目录 `baijiahao-publish` 整体复制到 `~/.openclaw/skills/` 或工作区 `./skills/`，重启 OpenClaw 后即可使用。
- **ClawHub 安装**（若已上架）：`npx clawhub@latest install baijiahao-publish`。
- **上传 / 发布**：在技能目录下执行 `clawhub publish . --slug baijiahao-publish --name "百家号发布器" --version 1.0.0`（需先配置 ClawHub 账号）。发布前请确保目录内包含 `SKILL.md`、`package.json`、`_meta.json`、`scripts/open_baijiahao_edit.py`、`requirements.txt`。