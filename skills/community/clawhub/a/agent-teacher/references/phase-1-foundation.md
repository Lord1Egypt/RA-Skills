# 基础课程详解

## 持续存在技能

### daily-log（每日工作日志）

**用途**：记录每日工作内容，是记忆系统的核心输入

**安装**：`clawhub install daily-log --dir skills`

**核心规范**：
- 输出位置：`memory/daily/YYYY-MM-DD.md`
- 触发时机：每次会话结束前、完成重要任务后
- 写日记不是记流水账，要记录：做了什么、遇到什么问题、怎么解决的

**验证**：学完后能写出符合规范的日记

### memory-review（知识沉淀）

**用途**：从日记中提取可复用知识，写入知识库

**安装**：`clawhub install memory-review --dir skills`

**核心概念**：
- 日记是输入，knowledge 是输出
- 两者配合：详细日记 → 更多可提取知识
- 没有日记，沉淀链条断裂

**验证**：学完后能运行知识沉淀流程

### daily-backup（Git 每日备份）

**用途**：每日自动备份工作区所有变更到 Git

**安装**：`clawhub install daily-backup --dir skills`

**核心概念**：
- 工作目录是 `/home/axelhu/.openclaw/workspace/`
- 备份会自动提交到 Git
- 配合 cron 实现每日定时备份
- 报告必须发送到飞书群（永远不要静默退出）

**验证**：能看到今天的备份报告在群里

---

## 沟通协作技能

### feishu-send（飞书消息发送）

**用途**：发送文件、图片、语音到飞书群

**安装**：`clawhub install feishu-send --dir skills`

**核心用法**：
- 文件发送：用 `message` 工具的 `filePath` 参数
- 图片发送：分三步（获取 token → 上传图片 → 发送）
- 语音发送：用 curl 调用飞书 opus API

**验证**：能在群里成功发送一条文字消息和一张图片

### 飞书@提及（Feishu @Mention）

**用途**：在消息中 @提醒某人

#### 接收 @提及

收到 @提及时，消息内容会包含 `<at user_id="...">name</at>` 标签。系统元数据也会提供 `sender_id`，可直接识别发送者身份。

#### 发送 @提及（message 工具方式，推荐）

**必须同时传 `accountId` 和 `target` 两个参数**：

```javascript
message({
  action: "send",
  channel: "feishu",
  accountId: "你的账号名",      // ← 必须！从 contacts 查 account_id
  target: "chat:oc_群ID",     // ← 必须！chat: 前缀
  message: "<at user_id=\"ou_xxx\">群名片</at> 内容"
})
```

⚠️ **常见错误**：不传 `accountId` 会盗用 main 身份；不传 `target` 消息发不出去。

#### 发送 @提及（curl 方式，备选）

如果 message 工具不可用，可以用 curl：

```bash
AGENT_NAME=你的账号名
read -r APP_ID APP_SECRET <<< "$(get_feishu_creds)"
TOKEN=$(curl -s -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json' \
  -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['tenant_access_token'])")

curl -X POST 'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"receive_id":"oc_群ID","msg_type":"text","content":"{\"text\":\"<at user_id=\\\"ou_xxx\\\">群名片</at> 内容\"}"}'
```

⚠️ curl 方式送达正常，但对方 session 可能收不到 relay 通知，优先用 message 工具。

#### 获取用户 open_id

| 方式 | 说明 |
|------|------|
| **contacts 技能** | 查 `memory/contacts/contacts.d/<name>.yaml` 的 `open_id` |
| **消息来源** | 收到的消息 metadata 中 `sender_id` 就是 open_id |
| **群成员列表** | 用 `feishu_chat(action=members, chat_id="oc_xxx")` 查询 |

**注意**：@提及只能在群聊中使用，私聊无法 @提醒对方。

### contacts（联系人管理）

**用途**：查找工作室成员联系方式，是所有沟通技能的基础

**安装**：`clawhub install contacts --dir skills`

**联系人卡片格式**（`memory/contacts/contacts.d/<contact_id>.yaml`）：

```yaml
contact_id: "mala"           # 内部唯一标识
name: "麻辣小龙虾"             # 内部通用名称

channels:
  feishu:
    open_id: "ou_51b..."    # 飞书 open_id，用于 @ 路由
    nickname: "麻辣小龙虾"     # 群里的显示名，@ 时填这个
    chat_id: "oc_87d..."    # 所在群 chat_id
    account_id: "mala"        # message 工具的 accountId 参数

internal:
  agent_id: "mala"           # OpenClaw agent ID
  role: "设计师"
  project: "AI游戏工作室"
```

**查询方法**：
```bash
# 查单个联系人
cat memory/contacts/contacts.d/mala.yaml

# 搜索联系人
grep -rl "name:" memory/contacts/contacts.d/ | xargs grep -l "小龙虾"
```

**关键字段说明**：

| 字段 | 用途 |
|------|------|
| `channels.feishu.open_id` | @ 某人时必须，消息路由依赖此字段 |
| `channels.feishu.nickname` | @ 时在标签里填的名字，显示在群里 |
| `channels.feishu.account_id` | message 工具发送时传 `accountId` 参数 |
| `channels.feishu.chat_id` | 发消息到哪个群 |

**更新维护**：
- 认识新联系人后，在 `contacts.d/` 下创建对应的 YAML 文件
- 发现联系人的飞书 ID、昵称变化时，及时更新
- 踩过的坑记录到 `notes` 字段

**验证**：能查到任意一个成员的 `open_id`、`nickname`、`account_id`

### sessions_send（跨 Agent 通信）

**用途**：向其他 agent 发消息、分配任务

**安装**：OpenClaw 内置，无需安装

**核心用法**：
```javascript
sessions_send({
  message: "任务描述",
  sessionKey: "agent:producer:feishu:...",
  timeoutSeconds: 60  // 同步等回复
})
```

**两种模式**：
- 同步（timeoutSeconds > 0）：发消息等回复
- 异步（timeoutSeconds = 0）：发完就走，不等结果

**⚠️ 重要注意：路径必须用绝对路径**
通过 `sessions_send` 向其他 agent 发送文件路径时，**必须使用绝对路径**，不能用相对路径。

原因：其他 agent 的工作目录和当前 agent 可能不同，相对路径在对方环境中无法定位文件。

正确示例：
```
/home/axelhu/.openclaw/workspace/skills/agent-teacher/references/rules-of-conduct.md
```

错误示例：
```
skills/agent-teacher/references/rules-of-conduct.md
```

**验证**：能给 producer 发消息并收到回复

---

## 知识检索技能

### memory_search（语义搜索）

**用途**：搜索记忆库中的内容

**安装**：OpenClaw 内置，无需安装

**核心用法**：
```javascript
memory_search({ query: "关于X的决策" })
```

**触发时机**：回答关于过去工作、决策、人名、偏好等问题前必须先搜索

### memory_get（读取记忆片段）

**用途**：读取记忆文件的特定行

**安装**：OpenClaw 内置，无需安装

**核心用法**：
```javascript
memory_get({ path: "memory/glossary.md", from: 1, lines: 50 })
```

**配合使用**：先 `memory_search` 找到文件，再 `memory_get` 拉取详情

---

## 飞书文档技能

### feishu_doc / feishu_wiki / feishu_bitable

**用途**：读写飞书文档、wiki、多维表格

**安装**：OpenClaw 内置，无需安装

**核心概念**：
- `feishu_doc`：读写飞书云文档
- `feishu_wiki`：读写飞书知识库
- `feishu_bitable`：读写飞书多维表格

**验证**：能读取一个飞书文档的内容

---

## 系统维护技能

### health-check（系统健康检查）

**用途**：检查 OpenClaw Gateway、磁盘、内存等系统健康状态

**安装**：`clawhub install health-check --dir skills`

**触发时机**：cron 定时任务或手动调用

### dependency-tracker（依赖检查）

**用途**：检查 Node.js、npm 版本和全局包是否有可用更新

**安装**：`clawhub install dependency-tracker --dir skills`

**触发时机**：每周或按需

---

## ⚠️ 学习原则：不重复记录

**已经学过并记住的内容不要重复记录，直接巩固现有知识点即可。**

### 示例

| 场景 | 不需要做的事 |
|------|-------------|
| 学 daily-log 时发现日记格式已在行为准则中提过 | 不要重新抄写格式说明，直接用 |
| 学 memory-review 时发现沉淀规则之前没学过 | 这是新知识，需要学习并执行 |
| 学 feishu-send 时发现"永远不要静默退出"是行为准则已有内容 | 直接记住，不需要再标注 |

### 判断标准

**新知识**：之前完全没学过、没见过 → 需要学习并记忆
**已知知识**：之前在行为准则或其他课程中学过 → 直接巩固，不需要重复记录

### 目的

避免 agent 学习时把已掌握的内容反复记录，浪费时间。

---

## 基础课程毕业标准

1. 能在群里发送今日工作日报
2. 知道日记写在哪里、格式是什么
3. 知道知识沉淀是什么、有什么用
4. 能在群里发送文件给用户
5. 今天的工作备份能在 Git 里看到
6. 能查到任意一个工作室成员的联系方式
7. 能给其他 agent 发消息并收到有意义回复
