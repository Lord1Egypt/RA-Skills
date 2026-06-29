---
name: cnki-download
description: 从中国知网（CNKI）检索并批量下载学术文献 PDF。一句话触发："知网下载"、"cnki 下载"、"帮我下几篇知网文献"。负责：首次运行让用户提供知网入口 URL 并保存到配置文件 → 启动 Playwright+Edge pipeline → 第一次会手动登录，登录态保留在 `browser_data/`，cookie 几个小时内有效，复用不需要再登录。覆盖检索 + 筛选（来源类别/年度等）+ 排序（相关度/时间/被引/下载/综合）+ 详情页访问 + PDF 下载全流程。
---

# CNKI 知网下载

## 什么时候用

用户说「知网下载」「cnki 下载」「帮我下几篇知网文献」「从知网搜点论文」时直接用本 skill。


## 命令调用约定（agent 必读，全局适用）

第 2 步（demo）和第 5 步（pipeline）都按本节的约定启动命令。

### `<SKILL_DIR>` 定义

SKILL.md 所在目录的**绝对路径**（去掉 SKILL.md 文件名）。

agent 读 SKILL.md 时已经知道自己这个文件的绝对路径，所以可以直接确定 `<SKILL_DIR>`。

> 本 skill 默认安装位置：`~/.openclaw/workspace-agentA/skills/cnki-download/`
> 但 skill 也可能在其他位置（全局 npm 安装、其他 workspace），**不要假设**它一定在某个特定路径下。

所有命令都必须在 `<SKILL_DIR>` 下执行，否则相对路径 `node scripts/search_cnki.js` 找不到文件。

### `<SKILL_DIR>` 适用范围（重要）

`<SKILL_DIR>` 是本 skill 所有**文件路径引用**的基准，**不仅**是命令 cwd：

- **执行命令**：cwd 必须是 `<SKILL_DIR>`（详见下面"启动命令模板"）
- **读取文件**：`read <SKILL_DIR>/scripts/user_config.json`、`read <SKILL_DIR>/assets/default-config.json` 等
- **写入文件**：`write <SKILL_DIR>/scripts/_user-config-20260623-1234.json`、`write <SKILL_DIR>/scripts/user_config.json` 等

**重要**：SKILL.md 里所有不带 `<SKILL_DIR>` 前缀的相对路径（如 `assets/default-config.json`、`scripts/user_config.json`、`references/config-schema.md` 等），**含义都是相对于 `<SKILL_DIR>`**，**不是**相对于 `scripts/`、也不是相对于"pipeline 当前 cwd"、也不是相对于"agent 默认 cwd"。

**反例（agent 不要这么推断）**：
- ❌ "pipeline 在 scripts/ 下跑，所以 `assets/default-config.json` 应该从 scripts/ 解析" → `scripts/assets/default-config.json` **不存在**，文件就在 `<SKILL_DIR>/assets/`
- ❌ "config 在 scripts/ 下生成，所以相对路径不需要 `<SKILL_DIR>` 前缀" → 同上，cwd 不一定是 scripts/
- ❌ "markdown 链接里的 `references/config-schema.md` 怎么读都 OK" → 仍然要用 `<SKILL_DIR>/references/config-schema.md` 才能 read 成功

### `<config 路径>` 定义

第 4 步生成的 config JSON 文件的**绝对路径**，例如：

```
C:\Users\xxx\.openclaw\workspace-agentA\skills\cnki-download\scripts\_user-config-20260623-1234.json
```

- 第 2 步 demo 跑：省略 `<config 路径>`（用 `<SKILL_DIR>/assets/default-config.json` 默认配置）
- 第 5 步自定义跑：传第 4 步生成的 config JSON 绝对路径

### 启动命令模板

**主推：在调 shell 之前由 agent 工具把 cwd 设为 `<SKILL_DIR>`**（最稳，不依赖 shell 内部状态）

不同 agent 框架设置 cwd 的字段名不同，下面是常见几种示例（用你框架对应的字段名）：

```yaml
# OpenClaw 的 exec 工具
exec:
  command: Start-Process powershell -ArgumentList "-NoExit", "-Command", "node scripts/search_cnki.js <config 路径>"
  workdir: <SKILL_DIR>

# Codex / Claude Code / 其他框架：找工具链里设置工作目录的字段
#   （可能叫 cwd / working_directory / Cwd / workingDirectory 等）
# 切记！codex或其他框架存在严格沙箱控制的，一定要在运行命令前获得权限提升，在沙箱外运行命令，否则无法打开命令窗口也无法打开浏览器
command: Start-Process powershell -ArgumentList "-NoExit", "-Command", "node scripts/search_cnki.js <config 路径>"
cwd: <SKILL_DIR>

# 自定义脚本 / process spawn：先把 cwd 切到 <SKILL_DIR> 再 spawn
process.chdir(SKILL_DIR); spawn(...)
```

如果 agent 工具**完全没有**设置 cwd 的能力，跳到下面的"备选"。

**备选：在 shell 命令里 `Set-Location`**（依赖 shell 内部状态，不推荐）

```powershell
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '<SKILL_DIR>'; node scripts/search_cnki.js <config 路径>"
```

### 反例（agent 不要这么写）

- ❌ `cd scripts; node scripts/search_cnki.js <config>` —— 路径变成 scripts/scripts/...，找不到
- ❌ `cd scripts; node search_cnki.js <config>` —— 看着对但脚本找不到 config
- ❌ 不设 cwd 直接 `node scripts/search_cnki.js <config>` —— agent 默认 cwd 可能是别的根目录，路径找不到
- ❌ 拆成两条命令 `Set-Location ...` + `Start-Process ...` —— 第二条的 cwd 不继承第一条的，跨 shell 失效


## 第 0 步：启动前 agent 自检（用户不用动手脚）

**不要**让用户自己去 `npm install`、装 Node、装 Edge —— 全部由 agent 跑前自检、自行装好。

启动脚本前依次跑下面 4 项检查，全部 ✅ 才进入工作流第 1 步：

1. **Node 可用**：`node --version` 能输出 v18+。如果不通过，提示用户装 Node 后由 agent 重试。
2. **Edge 可用**：检测 `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe` 或 `C:\Program Files\Microsoft\Edge\Application\msedge.exe` 是否存在。缺失则提示用户装 Microsoft Edge（https://www.microsoft.com/edge）。
3. **Playwright 可用且版本够**：在 `scripts/` 目录下跑 `node -e "import('playwright').then(m=>process.exit(0)).catch(e=>process.exit(1))"`，exit 0 即通过。Node 会沿父目录向上找 `node_modules/`，所以 workspace 根目录已装的 playwright 也能复用。
4. **Playwright 不够/缺失**时：在 `scripts/` 目录下自己跑 `npm install`。**重要**：执行时设环境变量 `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1`（这个 skill 用的是系统 Edge，不需要再下载 playwright 自带的 chromium，能省几百 MB）。具体命令由 agent 根据当前工作目录自己拼（不要在 SKILL.md 里写死绝对路径）。

自检全通过后告诉用户「环境 OK，开始干」，再进入第 1 步反问参数。

> 如果用户第一次说"知网下载"时已经在聊天里走了一段时间了，先做这 4 步自检再问参数 —— 自检可能也要十几秒，提前跑能省一次往返。

---

## 工作流（agent 视角）

### 1. 确认并保存知网入口 URL（必做，且只问一次）

首先读取 `<SKILL_DIR>/scripts/user_config.json`：
- 文件不存在 / 内容为空 `{}` / 没有 `url` 字段 → **首次运行**，用下面话术问用户，并在用户回复后**立刻**把 URL 写入 `<SKILL_DIR>/scripts/user_config.json`（覆盖原内容，格式 `{"url": "<用户提供的URL>"}`）。然后才进入步骤 2。
- 文件已有 `url` 字段 → 直接读取 `url`，记下来供后续 pipeline 使用，进入步骤 2。

**首次运行话术（必须原文使用，一字不改）**：

> 首次运行，由于每个平台链接过来的地址都不一样，比如中南大学链接过来的地址就是：'https://www-cnki-net-s-11.libdb.csu.edu.cn/'，所以请提供你的的地址让我保存。提供你的知网搜索页面浏览器地址栏显示的地址

写入文件后，给用户一个简短确认：「已保存：&lt;url&gt;」，然后进入步骤 2。

**注意**：
- 步骤 1 和步骤 2 必须**严格分开执行**，不要在确认 URL 之前就问检索参数
- 写文件用 `write` 工具直接覆盖 `<SKILL_DIR>/scripts/user_config.json`，不要用 `edit`（原文件是空 `{}` 没有匹配锚点）
- **编码必须是纯 UTF-8 无 BOM**（BOM 字符 `\uFEFF` 会让 Node.js `JSON.parse()` 抛 `Unexpected token` 错误，详见"关键约束"）
- 写完后**必须**用以下命令验证一遍（无输出无报错才算成功）：
  ```powershell
  node -e "JSON.parse(require('fs').readFileSync('<SKILL_DIR>/scripts/user_config.json','utf-8'))"
  ```
- 不要自动把任何默认 URL 写进去 —— 一定要等用户明确提供

### 2. 先建议 demo 试跑

**不要**一上来就问一堆参数。用一段话先建议 demo 试跑，小白用户可以先看到完整流程怎么走的（demo 关键词是「区块链」，下载 5 篇，筛选北大核心/CSSCI + 2024-2025 年）。

示范话术：

> 「好的，知网下载。在开始之前，要不要先用 **demo 跑一下测试**？
>
> demo 用的是内置默认配置：关键词『区块链』、北大核心 + CSSCI、2024-2025 年、下载 5 篇。
>
> 请选择 ：
> 1、跑demo      
> 2、自定义检索下载  
> 
> - 重要提示： 
- ```
  - 第一次会手动登录，后续几个小时内不需要再登录
  - 我会开启一个新的终端窗口，后续的指令和提示会在新窗口进行输出（主要涉及用户登录）；
  - 登录以后如果页面不在知网搜索页面，请 **自行链接** 到知网搜索页面，搜索将自动进行
  - 用最醒目的字体颜色提醒用户：  `<download文件保存的绝对路径>`
- ```
> 」

- 用户选 1 → 直接启动 demo（用 `<SKILL_DIR>/assets/default-config.json` 默认配置）

  按 **命令调用约定** 节的模板，把 `<config 路径>` **省略**（不传）。

- 用户选 2 → 跳到第 3 步（补全参数）。


### 3. 补全缺失参数

按下面 4 项问清楚：

> 「好，自定义检索。请告诉我：
> 1. **检索关键词**？（必填）
> 2. **下载几篇**？（必填，默认 5）
> 3. 要不要**筛选**？
> 4. 要不要**排序**？
> 明确提示可以指定的筛选与排序字段见 `<SKILL_DIR>/references/config-schema.md`
>
> 不筛不排的话只回关键词和篇数也行，剩下的我用默认。」

。

### 4. 写一份 config JSON

把用户的回答翻译成 config，写到一个临时文件，比如 `<SKILL_DIR>/scripts/_user-config-{YYYYMMDD-HHmm}.json`（写完必须验证无 BOM，详见"关键约束"）：

```json
{
  "keyword": "<用户说的关键词>",
  "download_count": <用户说的篇数>,
  "sort":   { "field": "<相关度|发表时间|被引|下载|综合>", "order": "<DESC|ASC>" },   // 可选
  "filters": [ { "col": "...", "values": ["..."] } ]                                   // 可选
}
```

只有 `keyword` 和 `download_count` 是必填。

### 5. 启动 pipeline

按 **命令调用约定** 节的模板，把 `<config 路径>` 替换为第 4 步生成的 config JSON 绝对路径。

## 启动进程后的处理约定

调 shell 启动 `node scripts/search_cnki.js` 后（典型场景用 `Start-Process powershell`），可能打开新进程和新窗口。把控制权完全交给它：

- 不要一直轮询进程状态（浪费 token）
- 让进程自己跑完，结果通过 console 输出到那个新窗口
- agent 这边直接结束当前 turn，等待用户反馈

## 关键约束

- **不要**自己用 `browser` 工具去探 CNKI（已经有 Playwright 跑着了），避免多开冲突
- **不要**修改 `<SKILL_DIR>/scripts/` 下的脚本；如发现 bug 写进 `<SKILL_DIR>/references/troubleshooting.md` 等用户决定
- **不要**让用户自己装 Node / Edge / 跑 `npm install`（agent 全包，见第 0 步）
- **不要**把 `<SKILL_DIR>/scripts/browser_data/` / `<SKILL_DIR>/scripts/download/` / `_login_state.png` 提交进 git（参考 `<SKILL_DIR>/references/troubleshooting.md` 的 `.gitignore` 写法）
- **所有 JSON 配置文件必须是无 BOM 的纯 UTF-8**（`user_config.json`、`_user-config-*.json` 等）。BOM 字符（`\uFEFF`）会让 Node.js `JSON.parse()` 抛 `Unexpected token` 错误（`... is not valid JSON`），上游会误判为"未找到 cnki_url"。
  - `write` 工具默认是**无 BOM** 的，但用 PowerShell 命令写文件时**必须**指定编码：
    - ✅ `Set-Content -Encoding utf8NoBOM <path>` 或 `Out-File -Encoding utf8NoBOM <path>`
    - ❌ **不要用** `Out-File` 默认编码（UTF-16 LE with BOM，会让 JSON.parse 失败）
    - ❌ **不要用** `[System.IO.File]::WriteAllText()` 默认重载（UTF-8 with BOM）
  - **写完任何 JSON 文件后必须验证**（兜底，防止 LLM 写文件时漏 BOM 看不到）：
    ```powershell
    node -e "JSON.parse(require('fs').readFileSync('<path>','utf-8'))"
    ```
    无输出无报错才算成功。失败时重新写，并检查 PowerShell 编码参数。

## 相关文件

- `<SKILL_DIR>/references/config-schema.md` —— config 字段详情、枚举值、3 种调用方式
- `<SKILL_DIR>/assets/default-config.json` —— 默认 demo（`node scripts/search_cnki.js` 不带参数就用这个的 hard-coded 等价物）