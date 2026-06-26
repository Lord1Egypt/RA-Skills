---
name: cc-session-bridge
description: 安装和使用 CC Session Bridge 脚本，将 Claude Code (CC) 的调用会话转换为 OpenClaw 会话格式，使 AIMA 平台能采集并展示 CC 的会话记录。支持流式写入、自动绑定 AIMA 任务、追加已有会话。触发场景：(1) 用户要求安装 CC 会话桥接脚本，(2) 用户想让 CC 调用记录在 AIMA 上可见，(3) 用户要求迁移 cc-session-bridge 技能到其他小灵，(4) 用户问怎么让 AIMA 看到 CC 的会话。关键词：cc-session-bridge、CC会话、AIMA采集、会话桥接、cc bridge、CC桥接。
---

# CC Session Bridge — CC 会话转 OpenClaw 格式技能

将 Claude Code (CC) 的调用会话转换为 OpenClaw 会话格式，使 AIMA 平台能采集并展示 CC 的会话记录。支持流式写入、自动绑定 AIMA 任务、追加已有会话。

## 一键安装

```bash
# 1. 解压技能包到 skills 目录
mkdir -p ~/.openclaw/skills
unzip -o <技能包路径>/cc-session-bridge.skill -d ~/.openclaw/skills/

# 2. 拷贝脚本和配置到全局目录
mkdir -p ~/.openclaw/scripts
cp ~/.openclaw/skills/cc-session-bridge/scripts/cc-session-bridge.py ~/.openclaw/scripts/
cp ~/.openclaw/skills/cc-session-bridge/scripts/cc-bridge-config.yaml ~/.openclaw/scripts/
chmod +x ~/.openclaw/scripts/cc-session-bridge.py

# 3. 编辑配置文件，添加当前 agent 的信息
# 编辑 ~/.openclaw/scripts/cc-bridge-config.yaml
```

配置文件格式（`~/.openclaw/scripts/cc-bridge-config.yaml`）：

```yaml
# 按 agent 目录名配置
# ⚠️ 填小灵自己的工号和名称，不是主人的
xiaoling-qinfang:
  chat_id: "WB02521102"
  sender_id: "WB02521102"
  sender_name: "小灵-财富风控001"

# 其他小灵安装时，替换为自己的身份信息:
# xiaoling-xxx:
#   chat_id: "你的工号"
#   sender_id: "你的工号"
#   sender_name: "小灵-xxx"
```

## 验证安装

```bash
# 检查依赖
which claude && claude --version   # CC CLI
which aima && aima --version       # AIMA CLI
which python3 && python3 --version # Python3

# 测试运行
python3 ~/.openclaw/scripts/cc-session-bridge.py \
  --agent-name <你的agent目录名> \
  --task-id <一个AIMA任务ID> \
  --query "你好，这是测试"
```

预期输出：`🆕 新建会话: xxx` → `✅ 会话已绑定到任务 xxx` → CC 执行 → `🎉 完成`

## 使用方法

### 基本用法（从配置文件读取 chat_id 等）

```bash
python3 ~/.openclaw/scripts/cc-session-bridge.py \
  --agent-name xiaoling-qinfang \
  --task-id 8700205 \
  --query "分析项目结构"
```

### 命令行覆盖参数

```bash
python3 ~/.openclaw/scripts/cc-session-bridge.py \
  --agent-name xiaoling-qinfang \
  --task-id 8700205 \
  --chat-id WB02521102 \
  --sender-id WB02521102 \
  --sender-name "小灵🤖财富风控001" \
  --query "分析项目结构"
```

### 指定工作目录

```bash
python3 ~/.openclaw/scripts/cc-session-bridge.py \
  --agent-name xiaoling-qinfang \
  --task-id 8700205 \
  --cwd ~/projects/my-project \
  --query "分析项目结构"
```

CC 会在 `~/projects/my-project` 目录下工作，能读取该项目的文件。不传 `--cwd` 时默认使用当前目录。

### 指定模型

```bash
python3 ~/.openclaw/scripts/cc-session-bridge.py \
  --agent-name xiaoling-qinfang \
  --task-id 8700205 \
  --model opus \
  --query "复杂分析任务"
```

默认 `sonnet`，可选 `opus`、`haiku` 等。

### 追加会话

同一 task-id 第二次调用时自动追加（append 模式），无需手动操作。

## 参数说明

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `--agent-name` | ✅ | - | OpenClaw agent 目录名 |
| `--task-id` | ✅ | - | AIMA 任务 ID |
| `--query` | ✅ | - | 传给 CC 的请求内容 |
| `--model` | ❌ | sonnet | CC 模型 |
| `--chat-id` | ❌ | 配置文件 | 小灵 chat_id（填小灵自己的工号） |
| `--sender-id` | ❌ | 配置文件 | 小灵 sender_id（填小灵自己的工号） |
| `--sender-name` | ❌ | 配置文件 | 小灵 sender 名称 |
| `--cwd` | ❌ | 当前目录 | CC 的工作目录，决定 CC 能访问哪些文件 |

优先级：命令行参数 > 配置文件

## 工作流程

```
1. 查找 AIMA 任务是否已有绑定会话
   ├── 有 → APPEND：追加到现有 jsonl
   └── 无 → NEW：新建会话 + 绑定到 AIMA 任务

2. 新建模式：
   a. 生成 session_id (UUID)
   b. 写入 session header
   c. bind-session 到 AIMA 任务
   d. 写入 user message + custom_message

3. 流式调用 CC (claude -p --output-format stream-json --verbose)
   ├── system 事件 → cc-raw 完整原始事件 + cc-init 摘要
   ├── assistant 事件 → cc-raw 完整原始事件 + 结构化 message (含 thinking/tool_use/text)
   ├── user 事件 → cc-raw 完整原始事件 + toolResult message
   ├── result 事件 → cc-raw 完整原始事件 + cc-result (完整文本，不截断)
   └── 未知事件 → cc-raw 完整原始事件
```

### 数据完整性保障

脚本采用**双写策略**，确保 CC 所有返回结果完整写入龙虾会话：

1. **cc-raw 原始事件**：每个 CC 事件完整写入 `custom(cc-raw)` 记录，不丢失任何数据
2. **结构化 message**：同时写入 OpenClaw 标准格式的 message，便于 AIMA 采集展示
3. **result 完整文本**：CC 最终结果文本完整保留，不截断（旧版只保留前500字符）
4. **thinking 完整保留**：CC 思考过程完整写入 assistant message 的 thinking 字段
5. **tool_use 完整 input**：工具调用的参数完整保留，不再只写摘要文本
6. **未知事件兜底**：CC 未来新增的事件类型通过 cc-raw 自动保留

## CC stream-json 事件类型

CC 用 `--output-format stream-json` 输出时，每行一个 JSON，按 `type` 字段分 4 类：

| 事件类型 | 说明 | 关键字段 |
|---------|------|----------|
| `system` | 初始化事件，CC 启动时发一次 | model, cwd, tools, permissionMode, mcp_servers, skills, session_id |
| `assistant` | CC 的回复，每轮调用模型后返回 | message.content (text/thinking/tool_use blocks) |
| `user` | 工具执行结果回传 | message.content (tool_result blocks) |
| `result` | 最终结果，任务完成后发一次 | result, total_cost_usd, num_turns, duration_ms, stop_reason, is_error |

**一次完整 CC 调用的流程**：

```
system → assistant(text+tool_use) → user(tool_result) → assistant(text+tool_use) → user(tool_result) → ... → result
```

即：初始化 → CC思考+调工具 → 工具返回结果 → CC再思考+再调工具 → ... → 最终结果

## 脚本处理逻辑

| CC 事件 | 脚本处理 | AIMA 展示 |
|---------|---------|----------|
| `system` | 只写一次，Markdown 格式 | 🔧 CC 初始化（模型、工具数、MCP服务等） |
| `assistant` | 拆出 text/thinking/tool_use，写两条：原始折叠 + 结构化 message | 🤖 CC Assistant Event + 正常 assistant message |
| `user` | 拆出每个 tool_result，折叠展示 | 🔧 Tool Result: `工具名`（点击展开） |
| `result` | 只写统计表格，不重复 result_text | 📊 CC Summary（费用、轮次、耗时） |

**Markdown 格式优化**：
- 长内容用 `<details>` 折叠，默认只显示概要
- toolResult 默认折叠，点击展开完整输出
- cc-result 只显示统计表格，避免与 assistant message 重复
- cc-init 只在首次写入，APPEND 模式跳过

## 故障排查

**AIMA 看不到会话**：
1. 检查 jsonl 是否生成：`ls ~/.openclaw/agents/<agent>/sessions/`
2. 检查 custom_message 是否含钉钉元数据（chat_id、sender_id、sender）
3. AIMA 采集是定时轮询，等几分钟
4. 确认绑定：`aima workspace task detail --taskId <id>`

**CC 调用失败**：检查 `which claude`，模型名是否正确

**绑定失败**：检查 `which aima`，手动绑定：`aima workspace task bind-session --taskId <id> --sessionId <sid>`

## 迁移到其他机器

只需 3 步：
1. 拷贝 `~/.openclaw/scripts/cc-session-bridge.py`
2. 拷贝 `~/.openclaw/scripts/cc-bridge-config.yaml`（添加新 agent 配置）
3. 确保依赖：`claude` CLI + `aima` CLI + `python3`

零 Python 依赖（内置简单 YAML 解析，不需要 pyyaml）。
