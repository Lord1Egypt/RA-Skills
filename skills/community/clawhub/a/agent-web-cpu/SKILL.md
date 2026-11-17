---
name: transweb-ai
description: "Use when the user wants to list, run, or chain transweb.cn AI apps, or generate web PPT, visual charts, 3D figure modeling, 3D animation, or mini-games. 需要 transweb.cn API Key（ak_live_...）。安装使用 transweb-create 后可无限拓展新功能，打造个人专属智能工具集。"
whenToUse: "当用户要用自己 transweb.cn 账号里的 AI 技能/应用完成一个任务，尤其是需要先选技能、或把多个技能串起来执行并拿到结果链接时；用户说“用 transweb 做…”“调用我的某个技能”“把几个技能串起来”“做个 PPT/图表/3D/小游戏”等。创建 Agent/Skill 应用请使用 transweb-create。"
display_name: "TransWeb 应用助手"
display_name_en: "TransWeb AI Apps"
description_zh: "浏览、运行和串联 transweb.cn 账号下的 AI 应用，默认支持生成网页版PPT、可视化图表、3D 手办建模、3D 动画和小游戏。(安装使用transweb-create技能后，可以无限拓展新功能，打造个人专属智能工具集)"
description_en: "Browse, run, and chain AI apps in a transweb.cn account. It supports web PPT, visual charts, 3D figure modeling, 3D animation, and mini-games by default; install transweb-create to extend new capabilities and build a personal toolset."
version: 1.2.3
author: "TransWeb"
examples_zh:
  - "用 transweb 帮我做一份季度汇报 PPT"
  - "列出我账号里能用的 AI 应用"
  - "把几个技能串起来：先写大纲，再生成 PPT"
examples_en:
  - "Make a quarterly report deck with my transweb apps"
  - "List the AI apps available in my account"
  - "Chain two apps: draft an outline, then turn it into slides"
metadata:
  openclaw:
    requires:
      bins:
        - python3
    primaryEnv: TRANSWEB_API_KEY
    envVars:
      - name: TRANSWEB_API_KEY
        required: false
        description: transweb.cn API Key（ak_live_...）；也可用 config 文件保存。
      - name: TRANSWEB_CONFIG
        required: false
        description: 自定义配置文件路径。
      - name: TRANSWEB_PROFILE
        required: false
        description: 选择 API Key profile。
      - name: TRANSWEB_BASE_URL
        required: false
        description: 覆盖 transweb.cn 服务地址。
      - name: TRANSWEB_API_NAME
        required: false
        description: 覆盖模型供应方 apiName。
      - name: TRANSWEB_MODEL
        required: false
        description: 覆盖模型名。
    emoji: "🧩"
    homepage: https://github.com/liuwenjin/transweb
---

# TransWeb 通用 AI Skill

适用于任何支持 `SKILL.md` 的 Agent Skills 客户端；只依赖 `python3`，不绑定特定宿主。

用 transweb.cn 的 API Key 调用账号下的 AI Skill/应用，支持：

- **默认能力**：生成网页版 PPT、可视化图表、3D 手办建模、3D 动画和小游戏。
- **PPT 自动路由**：当用户明确要求制作演示文稿（PPT/幻灯片/演示文稿/slides/deck/汇报材料/路演材料）时，直接用 `ppt` 命令走演示文稿应用（固定 `76f7de9504bad022a8978e9fe084df0f`），不需要先 `list`。
- **列出可用应用，优先级**：
  1. 先调 `/user/getLoginedData`，取自己账号下的 `pptItem.documentId`；
  2. 自己的应用没有匹配时，再调 `/user/getPublishedList`，取公开市场应用的 `documentId`。
- **单例执行**：选择一个 ID，按需求生成结果。
- **串行执行**：选择多个 ID，默认把上一步结果作为下一步输入。
- **返回链接**：查询生成后自动归档的 `questionData` 版本，取 `_id` 作为 `dataId`，拼接 `?solo=true&dataView=true&dataId=...&id=<应用ID>`。
- **访问权限**：默认保持私有（不修改 `isShare`）；仅当用户显式传入 `--share` 时才把每步存档设为公开可访问。

每次生成都会消耗账号积分，链式执行会按步数累计。

> 命令约定：下文命令以本 Skill 的 base directory 为工作目录。宿主加载 Skill 时会提供该目录的绝对路径。
>
> 创建 Agent/Skill 应用（资料转 Agent、需求转 Skill）已拆到 **`transweb-create`** 技能。

## 安全与隐私

- **默认私有**：每次生成的结果默认保持私有，不会自动公开或分享；只有显式加 `--share` 才会把存档设为公开可访问。
- **Key 不泄露**：技能包不包含任何默认 API Key，也不会读取其他技能的 Key；Key 只保存在本地 `0600` 权限的配置文件或环境变量中。
- **仅请求官方服务**：所有请求固定发往官方 `https://transweb.cn`，不会把数据改向其他服务器。

## 离线预览（无 API Key / 沙箱 / 审核环境）

**不需要 API Key、不发起任何网络请求、不读取账号、不消耗积分**，即可完整演示本技能的工作流。
在无凭据环境里请优先用下面这些命令，而不是直接跑 `list` / `run` / `ppt`（后者会明确报 `missing_key`）：

```bash
# 无参数离线演示完整工作流（list → run → ppt）
python3 scripts/transweb_ai.py demo --json

# 分别预览单个环节
python3 scripts/transweb_ai.py demo list --json
python3 scripts/transweb_ai.py demo run --json
python3 scripts/transweb_ai.py demo ppt --json

# 用自己的输入做预览（真实命令加 --dry-run 即可离线）
python3 scripts/transweb_ai.py ppt --input "做一份季度汇报 PPT" --dry-run --json
python3 scripts/transweb_ai.py run --ids 11111111111111111111111111111111 --input "先写大纲" --dry-run --json
python3 scripts/transweb_ai.py list --dry-run --json
```

预览返回结构化内容：可用应用清单、多步串联的执行顺序与输入输出传递、PPT 页大纲与生成步骤。
其中应用 ID 是**示例数据**（`1111...`/`2222...`），返回中 `sample:true`、`created:false`、
`network:false`、无真实链接，明确表示未访问账号、未创建任何文档。配置 Key 后去掉
`--dry-run` 即为真实执行。

平台审核可直接运行离线自检，全部通过返回 `ok:true`：

```bash
python3 scripts/transweb_ai.py selftest --json
```

## 配置

需要显式配置本技能自己的 Key。技能包**不包含默认 API Key**，也不会读取其他技能的 Key。检查：

```bash
python3 scripts/transweb_ai.py config show
```

- `configured: true`：可直接用。
- 否则让用户提供 transweb.cn API Key（`ak_live_...`），或在自己的终端运行：

```bash
python3 scripts/transweb_ai.py configure --verify
```

Key 需要的 scope：

| scope | 用途 |
| --- | --- |
| `doc:read` | `list` 调用 `/user/getLoginedData` 等标注接口时校验 |
| `ai:chat` | `run` 调用 `/gpt/aiGatewayRequest` 时校验 |
| `account:read` | 可选，`whoami` 调用 `/user/getUserData` 时校验 |

注意：当前只有显式声明 `requiredScope` 的接口会校验 scope。`getPublishedList`、`getDocumentData`、`getAgentData`、`publishPptItem`、`setDocumentStatus`、bucket 上传等不校验 scope；`doc:write` 目前没有接口使用，不能当作写权限边界。

配置文件位置（权限 `0600`，按优先级从高到低）：

- 自定义：`--config <path>` / `TRANSWEB_CONFIG`（最高优先级）
- 用户级：`~/.config/transweb-ai/config.json`（遵循 `XDG_CONFIG_HOME`）
- 旧版用户级兼容：`~/.dsh/transweb-ai.json`
- 项目通用：`<项目>/.transweb-ai.json` 或 `<项目>/.transweb/transweb-ai.json`（仅当无用户级配置时使用）
- 旧版项目兼容：`<项目>/.dsh/transweb-ai.json`

配置文件支持多个 Key profile。

### 换 API Key / 多账号切换

```bash
# 替换当前 profile 的 Key（最常用）
python3 scripts/transweb_ai.py configure --api-key ak_live_NEW --verify

# 新建一个 profile 并切过去
python3 scripts/transweb_ai.py configure --profile work --api-key ak_live_WORK --verify

# 查看所有 profile（Key 已脱敏）
python3 scripts/transweb_ai.py config list

# 切换当前 profile
python3 scripts/transweb_ai.py config use work
python3 scripts/transweb_ai.py config use default

# 删除非当前 profile
python3 scripts/transweb_ai.py config remove work

# 只对单次命令使用某个 profile，不改全局 active
python3 scripts/transweb_ai.py ppt --profile work --input "..."
python3 scripts/transweb_ai.py list --profile work --query "PPT"
```

- 默认 profile 名为 `default`；旧版扁平配置（`{apiKey, baseUrl}`）会自动识别为 `default`。
- `configure` 不带 `--profile` 时更新**当前 active** profile；带 `--profile` 时创建/更新该 profile 并设为 active。
- 单次命令的 `--api-key` / `TRANSWEB_API_KEY` 优先级最高，临时换 Key 不必写配置。
- `TRANSWEB_PROFILE=work` 可在环境变量层指定 profile。
- `config path` 显示当前实际读取的配置文件；`configure`/`config use` 会写入当前解析到的配置路径。

### 离线自检（审核/沙箱）

不需要 API Key，不发起网络请求：

```bash
python3 scripts/transweb_ai.py selftest --json
python3 scripts/transweb_ai.py --version
```

检查 Python 版本、包内文件、frontmatter 必需字段、依赖与密钥泄漏；沙箱/平台审核可先运行这一条。

## PPT 需求：自动映射

当用户**明确要求制作演示文稿**（例如说“做个 PPT”“把这份报告做成幻灯片”“做一份路演材料”“生成演示文稿”等）时，直接用 `ppt` 命令，不要先 `list` 选应用：

```bash
python3 scripts/transweb_ai.py ppt --input "主题、章节、每页要点或完整需求描述" --json
```

- 固定使用官方「演示文稿」应用 `76f7de9504bad022a8978e9fe084df0f`。
- 输入可以是完整大纲（推荐）或一句需求；输出 Reveal.js 演示文稿并返回链接。
- 支持 `--file` / `--stdin`、`--wait`、`--timeout`、`--share`。
- 成功返回：

```json
{
  "ok": true,
  "link": "https://transweb.cn/?solo=true&dataView=true&dataId=...&id=76f7...",
  "dataId": "...",
  "documentId": "76f7de9504bad022a8978e9fe084df0f",
  "title": "演示文稿标题",
  "slides": 12,
  "pointsCost": 250,
  "archived": true,
  "accessible": true,
  "elapsedMs": 113000
}
```

`ppt` 命令内部仍然是：生成 → 查询存档 → 设置访问权限 → 拼接链接；只是固定了应用 ID，并额外解析 `title` / `slides`。

> 原 `transweb-ppt` 技能已并入本技能并从技能目录移除；需要做 PPT 时统一用 `transweb-ai` 的 `ppt` 命令。本技能不包含默认 API Key，需要单独 `configure`。

## 其他需求：第一步：列出可用应用

```bash
python3 scripts/transweb_ai.py list --json --limit 50
```

默认 `--source auto`：**先查自建应用（getLoginedData），没有匹配才回退公开市场（getPublishedList）**。`--query` 是判断“有没有匹配”的依据，所以建议带上需求关键词。

来源选项：

| `--source` | 行为 |
| --- | --- |
| `auto`（默认） | 先自建；自建无匹配时回退公开市场 |
| `mine` | 只查自建（`getLoginedData`） |
| `published` | 只查公开市场（`getPublishedList`） |
| `both` | 同时返回自建 + 公开市场，自建优先去重 |

自建应用默认只列 `publishStatus: "true"` 的已发布应用（当前账号约 45 个）；`--all` 会包含未发布的自己应用。公开市场当前约 65 个。返回：

```json
{
  "ok": true,
  "source": "auto",
  "selectedSource": "mine",
  "fallback": false,
  "ownTotal": 45,
  "publishedTotal": null,
  "total": 1,
  "returned": 1,
  "publishedOnly": true,
  "query": "PPT",
  "apps": [
    {
      "id": "76f7de9504bad022a8978e9fe084df0f",
      "title": "演示文稿",
      "description": "将 PPT 大纲转化为 Reveal.js 结构化数据…",
      "type": "创意写作类",
      "tags": ["数据分析、幻灯片"],
      "category": "未定义",
      "appLabel": "创智通",
      "publishStatus": "true",
      "source": "mine",
      "owner": "创博",
      "folderName": "1714628260"
    }
  ]
}
```

推荐带关键词，让 `auto` 能判断自建是否匹配并自动回退：

```bash
python3 scripts/transweb_ai.py list --query "商业方案" --limit 10
python3 scripts/transweb_ai.py list --query "PPT" --limit 10
python3 scripts/transweb_ai.py list --query "研究报告" --all --limit 10
python3 scripts/transweb_ai.py list --source published --query "数据分析" --limit 10
python3 scripts/transweb_ai.py list --source both --query "PPT" --limit 10
```

判断返回：

- `selectedSource: "mine"`：用的是自建应用。
- `selectedSource: "published"` 且 `fallback: true`：自建没有匹配，已回退公开市场。
- `selectedSource: "both"`：两类都返回，`apps[].source` 标明来源，自建优先。
- `apps[].owner` / `folderName`：可判断是否为自己账号的应用。
- `--all`：只影响自建列表（包含未发布）；公开市场本身就是已发布。
- `--with-document-type`：逐个查询 `documentType`，返回 `agent` / `skill`；会增加请求次数。

选择时优先 `title`/`tags`/`type` 与需求匹配；`fallback: true` 时直接使用 `source: "published"` 的 ID 执行。

## 第二步：执行

`run` 会先调用 `/user/getDocumentData` 读取 `documentType`：

| `documentType` | 输出 |
| --- | --- |
| `agent` | **字符串结果**（`usage.result`），不查存档、不生成链接 |
| `skill` | **链接**（归档 `dataId` + `?solo=true&dataView=true&dataId=...`） |
| 缺失/未知 | 按 `skill` 兼容处理 |

`run` 不区分 ID 来源：`selectedSource: "mine"` 或 `"published"` 的 ID 都可以直接传。单例 Skill：

```bash
python3 scripts/transweb_ai.py run \
  --ids ec2bdd5d40cfaab61884c5edb170aeb9 \
  --input "把 AI 数字劳动力的三个层级画成流程图" \
  --json
```

链式（按 `--ids` 顺序串行）：

```bash
python3 scripts/transweb_ai.py run \
  --ids dcd76a6c644295cdc29b33bdbe825017,76f7de9504bad022a8978e9fe084df0f \
  --input "为一家 SaaS 公司做年度商业方案，并生成汇报 PPT" \
  --json
```

链式输入模式：

| `--chain-mode` | 下一步输入 |
| --- | --- |
| `result`（默认） | 上一步的输出内容 |
| `requirement` | 原始需求（各步独立执行） |
| `both` | 原始需求 + 上一步输出 |

注意：

- 链式应用之间没有强制 schema；如果下游应用需要特定 JSON/格式，先看它的 `description`，或先用单例跑一次确认输出。
- 每步都会消耗积分；失败时已完成的步骤会保留在 `completed` 中：agent 步骤含 `result` 字符串，skill 步骤含 `link`。
- `--wait 30` 可延长等待存档时间（默认 15 秒）。
- `--share` 显式把每步存档设为公开可访问；默认保持私有、不修改访问权限。

Agent 单例成功时返回字符串：

```json
{
  "ok": true,
  "finalAppId": "e8ce18f7b4f04e7c8961f28301cff280",
  "documentType": "agent",
  "result": "**结论：Pod 一直 Pending，先确认对象与影响范围...**",
  "steps": [
    {
      "index": 1,
      "appId": "e8ce18f7b4f04e7c8961f28301cff280",
      "documentType": "agent",
      "result": "...",
      "chars": 758,
      "pointsCost": 13
    }
  ],
  "pointsCost": 13
}
```

Skill 单例/链式成功时 `--json` 返回：

```json
{
  "ok": true,
  "documentType": "skill",
  "link": "https://transweb.cn/?solo=true&dataView=true&dataId=...&id=76f7...",
  "finalAppId": "76f7de9504bad022a8978e9fe084df0f",
  "steps": [
    {
      "index": 1,
      "appId": "...",
      "link": "...",
      "dataId": "...",
      "accessible": true,
      "chars": 5037,
      "pointsCost": 250,
      "elapsedMs": 113000
    }
  ],
  "pointsCost": 250,
  "elapsedMs": 113000
}
```

失败时：

```json
{
  "ok": false,
  "error": "积分余额不足，请充值。",
  "hint": "...",
  "code": "points",
  "completed": [{"index": 1, "link": "..."}],
  "failedAppId": "...",
  "failedIndex": 2
}
```

## 向用户交付

Agent 需求：

1. 直接把 `result` 字符串作为最终答案交付，不要编造链接。
2. 说明使用了哪个 Agent（`finalAppId`）和消耗积分。

Skill 需求：

1. 最终链接：`[打开结果](https://transweb.cn/...)`
2. 说明应用标题/ID、步骤数与消耗积分

PPT 需求：

1. 最终链接：`[打开 PPT](https://transweb.cn/...)`
2. 演示文稿标题与页数（来自 `ppt` 命令的 `title` / `slides`）
3. 访问权限与消耗积分
4. 如果用户要可下载的 `.pptx` 文件，改用 `office-pptx`

其他需求：

1. 最终链接：`[打开结果](https://transweb.cn/...)`
2. 用了哪些应用（标题/ID）和步骤数
3. 总消耗积分（`pointsCost`）
4. 如果 `accessible: false`，说明权限设置失败及 `accessError`；链接可能仅账号本人可看
5. 链式失败时，给出已完成步骤的链接和失败原因

不要重复粘贴完整结果 JSON。若用户要修改，追加需求后重新执行，或只重跑最后一步。

## 排障

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| `code:1 / ret:1 未登录` | Key 无效/过期 | 重新创建 Key 并 configure |
| `ret:3 缺少 scope` | 仅 `requiredScope` 接口会报，通常是 `doc:read`/`ai:chat`/`account:read` | 按 5.2 的接口表补对应 scope；写接口不靠 scope 拦截 |
| `ret:2 积分余额不足` | 账号积分不足 | 充值；链式可减少步数 |
| `list` 返回 0 条 | 自建和公开市场都没有匹配，或 filter 太窄 | 换关键词；用 `--source both`/`--all` 查看；确认公开市场有对应应用 |
| `auto` 一直只返回自建 | 没带 `--query`，无法判断“适合” | 加 `--query`，或显式用 `--source published` |
| `在文档存档中没有找到对应版本` | 存档异步/计费记录失败 | 加 `--wait 30`；确认积分正常 |
| 链式下游结果不对 | 下游不接受上一步格式 | 改用 `--chain-mode requirement`，或先单例确认输出 |
| `accessible: false` | 权限更新失败/非存档所有者 | 查看 `accessError`；链接仍可能本人可用 |
| `ppt` 输出缺少 slides | 上游模型异常 | 重试；仍失败就让大纲更具体（主题/章节/每页要点） |
| 用户要的是 .pptx 文件 | `ppt` 只返回网页链接 | 改用 `office-pptx` 技能生成本地文件 |

## 资源

- `scripts/transweb_ai.py demo`：无参数离线演示完整工作流；`list` / `run` / `ppt` 均支持 `--dry-run` 离线预览。

- `scripts/transweb_ai.py`：list / ppt / run / 存档查询 / 权限设置；HTTP 优先用系统 `curl`，无 curl 时回退 `urllib`
- `references/api.md`：`getLoginedData`、`getPublishedList`、`aiGatewayRequest`、`queryQuestionData`、`setDocumentStatus` 字段说明
