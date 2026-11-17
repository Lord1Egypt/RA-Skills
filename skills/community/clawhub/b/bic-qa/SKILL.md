---
name: bic-qa
description: BIC-QA 数据库与操作系统知识库问答（支持多轮上下文）。当用户提出数据库（Oracle/MySQL/PostgreSQL/达梦/金仓/GaussDB/Redis/MongoDB 等）或操作系统相关的原理、运维、故障排查、性能优化问题，或需要基于 BIC-QA 知识库检索权威资料时使用。同一话题的连续追问必须复用会话。
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
        - py
      config:
        - ~/.bic/config/api_key
        - ~/.bic/openapi/api_key
    primaryEnv: BIC_API_KEY
    envVars:
      - name: BIC_API_KEY
        required: false
        description: BIC-QA API Key。不设置时，脚本从 ~/.bic/config/api_key 读取（推荐，避免 Key 进入环境）。
      - name: BICQA_API_KEY
        required: false
        description: BIC_API_KEY 的兼容别名。
      - name: BIC_QA_API_KEY
        required: false
        description: BIC_API_KEY 的兼容别名。
      - name: BICQA_KEY_FILE
        required: false
        description: 自定义 API Key 文件路径。
      - name: BICQA_BASE_URL
        required: false
        description: 测试或受控代理使用的自定义 API 地址；必须同时显式启用 BICQA_ALLOW_CUSTOM_BASE_URL。
      - name: BICQA_ALLOW_CUSTOM_BASE_URL
        required: false
        description: 设为 1 才允许把 API Key 发往非官方地址；远程地址必须使用 HTTPS。
      - name: BICQA_STATE_FILE
        required: false
        description: 自定义会话状态文件路径。
      - name: BICQA_STATE_DIR
        required: false
        description: 覆盖会话状态目录，默认 ~/.bic/openapi/。
      - name: BICQA_TTL_ACTIVE
        required: false
        description: 会话空闲超时秒数，默认 7200。
      - name: BICQA_TTL_HARD
        required: false
        description: 会话硬过期秒数，默认 86400。
      - name: BICQA_MAX_TURNS
        required: false
        description: 单个会话最大轮数，默认 20。
    emoji: "🐘"
    homepage: https://www.bic-qa.com
---

# BIC-QA 知识问答（Open API）

基于 BIC-QA 官方 Open API 的**有状态**多轮问答。服务端保存上下文：先创建会话拿到 `conversationId`，之后同一话题的每一轮都复用这个 id。

需要 Python 3.8+（仅标准库）和有效的 BIC-QA API Key。默认只向 `https://api.bic-qa.com` 发送请求。

## 会话协议（强制，不可绕过）

所有提问必须走 `scripts/bicqa.py`。脚本负责建会话、判定复用/重建、状态落盘。

**禁止**自己构造或猜测 `conversationId`、**禁止**直接 curl、**禁止**把会话 id 暴露给用户（只在结尾用短号标注）。

Unix、macOS 与 WSL 优先使用 `python3`；Windows 使用 `py -3`。若命令不可用，从 frontmatter 的 `requires.anyBins` 中选择本机存在的解释器。

```bash
# <SKILL_DIR> = 本 SKILL.md 所在目录
python3 <SKILL_DIR>/scripts/bicqa.py ask -q "用户的问题原文"
python3 <SKILL_DIR>/scripts/bicqa.py ask -n -q "..." -t "索引失效排查"
python3 <SKILL_DIR>/scripts/bicqa.py list                 # 列出本地会话
python3 <SKILL_DIR>/scripts/bicqa.py resume 3f1a          # 切回某个旧会话
python3 <SKILL_DIR>/scripts/bicqa.py check                # 排障自检，不消耗 token
```

`ask` 参数：`-q/--question` 问题（必填）、`-n/--new` 强制新会话、`-t/--title` 新建会话时的标题、`--timeout` 流式问答总时限秒数（默认 600）。
`new` 参数：`-t/--title`。简写与全写等价。
找不到脚本时用 `--help` 自检，或按常见安装位置查找：`~/.agents/skills/bic-qa/`、`~/.workbuddy/skills/bic-qa/`、`~/.claude/skills/bic-qa/`、`~/.codex/skills/bic-qa/`。

运行 `ask` 的外层命令执行器也应允许至少 `--timeout` 加 30 秒；若工具支持 yield/poll，应等待原进程完成，不要因暂时没有 stdout 就重复发起同一问题。

### 必须加 `--new`（简写 `-n`）的四种情况

1. 用户明确说「新会话 / 换个话题 / 重新开始 / new session」。
2. **换了数据库种类、版本或实例**——即使问题类型相同（例如从 PG 15 切到 Oracle 19c）。这条最容易漏，也最容易串味。
3. 你判断新问题与当前会话主题无关（例如从「索引失效」跳到「备份恢复」）。
4. 脚本输出 `[bic-qa] 服务端会话失效` 后仍未恢复。

空闲超时（默认 2 小时）与轮数上限（默认 20）由脚本自动判定，你不需要操心。

### 不要新建的情况（高频误判，务必遵守）

追问、「详细说说」、换个说法复述、纠正上一轮答案、对同一张表/同一个现象换指标继续问——这些**全部复用**当前会话。上下文断了，答案质量会明显下降。

## 凭证

优先级：环境变量 `BIC_API_KEY` / `BICQA_API_KEY` / `BIC_QA_API_KEY` → `$BICQA_KEY_FILE` → `~/.bic/config/api_key` → `~/.bic/openapi/api_key`。

未配置时脚本报错退出。**此时不要用模型自身知识顶替**——按提示让用户去 https://www.bic-qa.com 获取 Key。

**不要把 Key 写进 SKILL.md、脚本、命令历史或回复里。** 配置方式（bash / WSL / macOS）：

```bash
mkdir -p ~/.bic/config && chmod 700 ~/.bic/config
printf '%s' '<你的Key>' > ~/.bic/config/api_key && chmod 600 ~/.bic/config/api_key
```

Windows PowerShell：

```powershell
New-Item -ItemType Directory -Force -Path "$HOME\.bic\config" | Out-Null
Set-Content -NoNewline -Path "$HOME\.bic\config\api_key" -Value "<你的Key>"
```

## 状态存放位置（跨平台，不绑定任何 Agent 厂商）

默认 `~/.bic/openapi/sessions.json`（权限 600）。可用环境变量覆盖：

- `BICQA_STATE_FILE=/path/to/sessions.json`——直接指定文件
- `BICQA_STATE_DIR=.bicqa`——按项目隔离会话（建议在仓库里把这个目录加进 .gitignore）

## 排障

调用失败时**第一步**跑 `check`（纯本地，不联网不消耗 token），它会告诉你凭证、状态文件、当前会话三件事分别是否正常，按输出处理即可：

```bash
python3 <SKILL_DIR>/scripts/bicqa.py check            # 本地环节
python3 <SKILL_DIR>/scripts/bicqa.py check --online   # 额外建一个测试会话验证 Key（会产生一个空会话）
```

`selftest` 是开发期用的完整离线自测（SSE 解析、过期判定、脱敏），**排障时不需要跑**，只在改动脚本或怀疑版本不匹配时用。

## 错误与限流

- **401 `OPEN_API_KEY_MISSING` / `OPEN_API_KEY_INVALID`**：提示用户更换或重新配置 Key，不要高频重试。
- **400 `OPEN_API_SESSION_NOT_FOUND`**：脚本会自动重建会话并重试一次；再次失败才上报。
- **429 `OPEN_API_RATE_LIMITED`**：创建会话 60 秒 60 次、流式聊天 60 秒 20 次（用户维度）。按提示的秒数退避，**不要连发**。
- **`OPEN_API_TIMEOUT` / `OPEN_API_STREAM_TIMEOUT`**：连接、响应头或流式问答超过时限。会话会保留；如需重试，先向用户说明可能已经产生部分处理或计费，不要自动重发。
- **`OPEN_API_STREAM_INTERRUPTED` / `OPEN_API_STREAM_INCOMPLETE`**：流传输中断或未收到最终 `done`。脚本会丢弃残缺正文并保留会话，不要把残缺内容当作答案。
- **503 / 500**：如实告知调用失败，可建议稍后重试。
- 任何时候都**不要**用训练数据冒充知识库答案。

## 输出要求

1. 严格基于脚本返回的正文组织回答，不自行补充技术细节。
2. 结尾用一行小字标注会话短号，例如：`（会话 3f1a2b）`。
3. 返回为空或报错时如实说明，并提示可稍后重试或换 `--new` 开新会话。
4. 回答较长时用小标题分块；涉及命令、参数、版本号的，原样保留。
5. 正文里的 `【本次回答基于知识库内容生成】` / `【本次回答未匹配到知识库】` 是服务端标记，不要照抄给用户。出现「未匹配到知识库」时，说明该问题知识库未覆盖，如实告知并用模型自身知识补充时须明确标注来源不是知识库。

## 流式事件速查

需要深入理解返回结构时读 `references/api.md`（SSE 五种事件：`meta` / `delta` / `file` / `error` / `done`）。
