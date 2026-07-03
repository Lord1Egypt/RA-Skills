---
name: bilibili-content-summary
description: "提取 B站视频/图文内容并生成摘要 — 下载音频 + ASR 转写 / 图片 OCR、LLM 摘要、飞书推送。关键词：B站视频摘要 / B站图文摘要 / bilibili / ASR / 转写 / OCR / 视频总结"
url: https://github.com/zify9000/bilibili-content-summary
license: MIT
---

# B站视频/图文摘要

## 使用指南（以 hermes agent 为例）

1. 加载 skill。下达指令，"安装skill，https://github.com/zify9000/bilibili-content-summary"；
2. 配置凭证。下达指令，"配置B站内容摘要skill"，交互式完成初始化配置（ASR/LLM/飞书凭据，B站 Cookie）；
3. 触发式调用，下达指令，"总结这个视频 https://b23.tv/XXXXX"，或 "帮我看看这个B站视频 BV1QKGC63E6X"，或 "总结这篇图文 https://www.bilibili.com/opus/1211772336215162889"。

## 目录结构

```
bilibili-content-summary/
├── SKILL.md                      # Skill 说明文档
├── .gitignore                    # 排除敏感凭据和运行时数据
├── references/
│   └── asr-remote.md             # ASR 服务调用参考文档
└── scripts/
    ├── common.py                 # 公共工具：配置加载、日志、环境变量、飞书、重试
    ├── summarize.py              # 主流程：URL 分发 → 视频(ASR) / 图文(OCR) → LLM摘要
    ├── push.py                   # 推送摘要：读取摘要结果 → 构建飞书卡片 → 发送
    ├── init/
    │   ├── credentials.py        # 凭据初始化：写入 ASR/LLM/飞书凭据
    │   ├── bili_get_qr.py        # B站登录步骤1：获取二维码，浏览器保持运行
    │   └── bili_wait_login.py    # B站登录步骤2：等待扫码，保存 Cookie
    ├── config/
    │   └── base.yaml             # 全局配置（B站请求参数、ASR分段参数、LLM参数、飞书重试策略）
    ├── env/
    │   ├── .bili.env             # B站 Cookie（扫码获取，含 SESSDATA/bili_jct 等）
    │   ├── .bili.env.example
    │   ├── .llm.env              # LLM/ASR/OCR 模型配置（model / base_url / api_key）
    │   ├── .llm.env.example
    │   ├── .feishu.env           # 飞书应用凭据
    │   └── .feishu.env.example
    ├── tmp/                      # 步骤间临时文件（摘要结果缓存）
    └── log/                      # 运行日志（按日滚动，保留7天）
```

## 业务流

> # 🚫 agent 强制规则（最高优先级，无条件执行）
>
> **摘要 + 推送是一条不可拆分的流水线。无论任何场景（DM、群聊、自动化），都必须走完。**
>
> | 规则 | 内容 |
> |------|------|
> | **禁止 `--no-push`** | agent 调用 `summarize.py` 时 **严禁** 添加 `--no-push` 参数。该参数仅供人类直接使用 |
> | **禁止读缓存** | **绝对禁止** 读取 `scripts/tmp/summary_result.json`。该文件仅供 `push.py` 内部使用 |
> | **禁止自行输出** | **绝对禁止** 用 markdown / `send_message` 等方式向用户展示摘要。摘要只能通过飞书卡片呈现 |
> | **唯一流程** | `summarize.py --quiet <URL>` → 确认 `"status": "done"` → 立即 `push.py` → 回复用户「已推送」 |
>
> **常见错误心理（全部无效）**：
> - ❌ "这是 DM 对话，直接回复更方便" → 仍然推送
> - ❌ "我不确定 feishu_chat_id 对不对" → 仍然推送，配置由用户负责
> - ❌ "用户只说了总结，没说推送" → 推送是默认行为，不需要用户额外指令
> - ❌ "我先看看缓存文件里有什么" → 禁止读缓存

### 0. 初始化

#### 凭据配置

凭据文件统一在 `scripts/env/`：

| 文件 | 内容 | 用途 |
|------|------|------|
| `.bili.env` | `bili_cookies_json` | B站 Cookie（避免 412 错误，扫码获取） |
| `.llm.env` | `llm_model` / `llm_base_url` / `llm_api_key` / `asr_model` / `asr_base_url` / `asr_api_key` / `ocr_model` / `ocr_base_url` / `ocr_api_key` | 摘要 LLM + ASR 转写 + OCR 识图 |
| `.feishu.env` | `feishu_app_id` / `feishu_app_secret` / `feishu_chat_id` | 飞书推送 |

agent 首次使用时应检查这 3 个文件是否存在，对缺失的逐一询问配置。

> **⚠️ agent 注意**：
> 1. `.bili.env`、`.llm.env`、`.feishu.env` 是以 `.` 开头的隐藏文件。部分工具的 glob 匹配对隐藏文件支持有缺陷。**用 `ls -la scripts/env/` 或直接 `Read` 目标路径确认**，不要单独依赖 glob 搜索结果。
> 2. Hermes 等agent框架会拦截终端中出现的 key 明文。**不要直接在终端 echo/cat/粘贴 key**，应通过 `credentials.py` 脚本写入。
> 3. 优先考虑从 agent 自身配置中自动读取asr/llm/feishu 等凭据项。
> 4. **B站 Cookie 扫码必须分两步执行**：先执行 `bili_get_qr.py` 获取二维码并展示给用户，再执行 `bili_wait_login.py` 等待扫码完成。不要合并为一步，否则会忘记展示二维码。


**LLM / ASR / OCR / 飞书配置**：

```
python3 scripts/init/credentials.py \
  --llm-model <LLM模型> --llm-base-url <LLM地址> --llm-api-key <LLM密钥> \
  --asr-base-url <ASR地址> --asr-api-key <ASR密钥> --asr-model <ASR模型> \
  --ocr-model <OCR模型> \
  --feishu-app-id <app_id> --feishu-app-secret <secret> --feishu-chat-id <chat_id>
```

LLM / ASR / OCR 统一写入 `.llm.env`，飞书写入 `.feishu.env`。可只传需要的参数，或任意组合。仅当 agent 配置中缺少某项凭据时，才向用户询问。

**B站 Cookie 配置**：

```
# 步骤1：获取二维码
python3 scripts/init/bili_get_qr.py

# agent 读取 /tmp/bili_login_qr.png 展示给用户扫码

# 步骤2：等待扫码并保存 Cookie
python3 scripts/init/bili_wait_login.py
```

Docker/snap 环境需要加 `--no-sandbox`：
```
python3 scripts/init/bili_get_qr.py --no-sandbox
```

**直接执行上述命令，不要自己重写登录逻辑。** 步骤1以 headless 模式启动 Chromium，QR 图片保存至 `/tmp/bili_login_qr.png`，浏览器进程保持运行。步骤2连接已有浏览器等待扫码完成，登录后保存 Cookie 至 `.bili.env` 并关闭浏览器。

依赖：`nodriver>=0.50`、Chromium 浏览器

Cookie 过期后 API 调用会返回 HTML 登录页面（HTTP 412 或 JSON 解析异常），日志输出明确「Cookie 已过期」及恢复指令。

### 1a. 视频摘要

```
python3 scripts/summarize.py --quiet <B站视频URL或BV ID>
```

完整工作流：
1. 解析短链接 → 提取 BV ID
2. 获取视频元数据（标题、UP主、时长、cid）
3. 通过 B站 API 下载音频
4. ffmpeg 分段（15分钟 / 64kbps）
5. ASR 探针（单 chunk 测试可用性）
6. 并行转写（max_workers=3）
7. LLM 生成摘要（核心摘要 + 关键要点 + 章节时间线）

结果**仅缓存**到 `scripts/tmp/summary_result.json`，stdout 只输出精简状态（不含摘要正文）。

**参数**：
- `--quiet`：静默模式，不输出 LLM 流式内容到 stderr（agent 调用时必须使用）
- `--no-push`：不推送飞书，仅输出摘要（**人类专用**，agent 禁止使用）
- `--no-cleanup`：不清理临时音频文件

### 1b. 图文摘要

```
python3 scripts/summarize.py --quiet <B站图文URL或opus ID>
```

完整工作流：
1. 解析 opus URL → 提取 opus ID
2. 通过 B站 API 获取图文详情（标题、作者、段落）
3. 提取文本内容 + 下载图片
4. 并行 OCR 识别图片文字（mimo-v2.5-pro, max_workers=3）
5. LLM 生成摘要（核心摘要 + 关键要点 + 内容结构）

结果**仅缓存**到 `scripts/tmp/summary_result.json`。

> ⚠️ agent 行为见 [业务流顶部强制规则](#业务流)。`summarize.py` 返回 `"status": "done"` 后立即执行 `push.py`。

### 2. 飞书推送

```
python3 scripts/push.py
```

读取 `scripts/tmp/summary_result.json`，构建飞书卡片消息推送。

**🚫 推送只能通过 `push.py` 完成。** 飞书卡片消息（蓝色标题栏、视频信息、摘要内容）≠ 纯文本消息，`send_message` 等工具无法替代。

也可以一步完成摘要+推送：
```
python3 scripts/summarize.py --quiet <URL> && python3 scripts/push.py
```


## Output Formats

- **Summary**: 核心摘要（200字以内）
- **Key Points**: 3-5条关键要点
- **Chapters**: 章节时间线（如有明显分段）

### 3. 故障排查

#### Cookie 过期

**症状**：调用 `summarize.py` 时抛出 `RuntimeError`，包含「B站 Cookie 已过期」及恢复指令。日志中出现 `HTTP 412` 或 `API 返回登录页面`。

**根因**：`.bili.env` 中的 `SESSDATA` 已失效，B站 API 返回 HTTP 412 或 HTML 登录页面。

**恢复流程（agent 必须按此执行）**：
```
# 步骤1：获取二维码
python3 scripts/init/bili_get_qr.py
# agent 读取 /tmp/bili_login_qr.png 展示给用户扫码

# 步骤2：等待扫码并保存 Cookie
python3 scripts/init/bili_wait_login.py
```

> ⚠️ **禁止让用户手动从浏览器复制 Cookie。** 必须使用上述 QR 码登录流程。
