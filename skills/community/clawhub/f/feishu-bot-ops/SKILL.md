---
name: feishu-bot-ops
description: 飞书（Feishu/Lark）机器人运维大全 — 从部署到调试的全生命周期。覆盖 @mention 机制、bot 间通信、消息丢失排查、会话串线修复、WebSocket 连接稳定性、认证鉴权陷阱、交互卡片回调等 20+ 故障场景。
version: 1.1.0
author: Laura & Vincent (RONVUE)
category: feishu
tags: [feishu, lark, bot, ops, debugging, gateway, websocket, at-mention]
---

# 飞书 Bot 运维大全

让 Hermes Agent 的飞书 bot 稳定运行，覆盖从部署到深度调试的完整知识。

## 目录

- [快速诊断](#快速诊断) — 一键诊断 + 一键修复
- [环境变量速查](#环境变量速查)
- [消息与 @mention 机制](#消息与-mention-机制)
- [Bot 间通信](#bot-间通信)
- [会话上下文串线](#会话上下文串线)
- [故障场景速查表](#故障场景速查表) — 10+ 场景的现象→根因→修复
- [安全运维](#安全运维)
- [飞书 API 调试手段](#飞书-api-调试手段)
- [交互卡片回调](#交互卡片回调)
- [排查纪律](#排查纪律)

---

## 快速诊断

用户说「飞书不能用了 / 没反应」时，**跳过信息搜集，直接跑诊断**：

### 一键诊断命令

```bash
# 0. lark-oapi 是否安装（最常见的新装遗漏）
<hermes_venv>/bin/python -c "import lark_oapi" 2>&1 || echo "✗ lark-oapi 未安装"

# 1. Gateway 进程状态
ps aux | grep '[h]ermes.*gateway' | grep -v grep

# 2. 锁文件
ls -la $HERMES_LOCAL_STATE/gateway-locks/ 2>/dev/null

# 3. 最近日志错误
grep -iE 'error|unauthorized|feishu.*(connected|disconnected|dropping|lock)|panic' \
  $HERMES_HOME/logs/gateway.log | tail -20

# 4. Agent 卡死检测（消息收到但不回复）
grep -E 'Flushing text batch|response ready|Sending response' \
  $HERMES_HOME/logs/gateway.log | tail -10
# 如有 Flushing 但无 response ready → agent 卡死，查 errors.log：
tail -30 $HERMES_HOME/logs/errors.log
```

**快速定位**：lark-oapi 缺失→安装；锁文件残留→清理后重启；Unauthorized→`GATEWAY_ALLOW_ALL_USERS=true`；进程不在→启动 gateway；connected 正常但没回复→检查 `_admit` 拒绝原因；Flushing 有但 response ready 无→agent 卡死（查 errors.log 找 API 超时）→重启 gateway。

### 一键修复命令

```bash
# 场景A：多实例/锁文件冲突
pkill -9 -f 'hermes gateway run' 2>/dev/null; sleep 2
rm -f $HERMES_LOCAL_STATE/gateway-locks/feishu-app-id-*.lock
hermes gateway run 2>&1 &
sleep 5 && grep '✓ feishu connected' $HERMES_HOME/logs/gateway.log | tail -1

# 场景B：鉴权拦截
grep 'Unauthorized' $HERMES_HOME/logs/gateway.log | tail -3
# 如有输出 → .env 加 GATEWAY_ALLOW_ALL_USERS=true，重启

# 场景C：lark-oapi 未安装
<hermes_venv>/bin/python -m ensurepip 2>/dev/null
<hermes_venv>/bin/python -m pip install lark-oapi
# 国内用户可用镜像：-i https://mirrors.aliyun.com/pypi/simple/
# 装完重启 gateway
```

### 关键原则

- **先诊断，后解释**—不要先说「让我加载技能看看」，用户会觉得你卡死了
- 诊断结果出来后，一句话报告现状+下一步，不要长篇解释

---

## 环境变量速查

所有变量在 `$HERMES_HOME/.env` 中设置，修改后需重启 gateway 生效。

| 变量 | 默认值 | 作用 |
|------|--------|------|
| `FEISHU_GROUP_POLICY` | `allowlist` | 群消息准入策略：open/allowlist/blacklist/disabled |
| `FEISHU_REQUIRE_MENTION` | `true` | 是否要求群消息必须 @ bot 才处理。设 `false` 可接收所有群消息 |
| `FEISHU_ALLOW_BOTS` | `none` | 是否接收其他 bot 的消息：none/mentions/all |
| `FEISHU_AT_MAP` | (空) | @mention 映射表：`显示名=open_id,...`，让出站 @mention 转为真正的 `<at>` 标签 |
| `GATEWAY_ALLOW_ALL_USERS` | — | 设为 `true` 跳过 gateway 层面用户白名单，解决「消息到达但被拦截」问题 |

---

## 消息与 @mention 机制

### @mention 不是纯文本

飞书的 `@用户名` 需要带上 `open_id` 才能触发通知。Markdown 里 `@某人` 只是纯文本。

**真正生效的 @mention 格式**（飞书富文本消息）：

```
<at user_id="ou_xxx">名字</at>
```

**影响**：
- Bot 通过 Markdown 回复的 `@某人` 只是装饰性文本，不产生通知
- 用户端用飞书客户端原生 @ 可以正常生效
- Bot 之间的 @ 互叫需要构造 post 消息含 `<at>` 标签

### 群消息准入逻辑

群消息是否被处理，取决于两层检查（`feishu.py` `_admit()`）：

1. **Group policy**：`FEISHU_GROUP_POLICY` 控制（open/allowlist/blacklist/disabled）
2. **require_mention**（默认 `True`）：即使 `group_policy=open`，消息也必须 @ 了 bot 才放行

> ⚠️ `FEISHU_GROUP_POLICY=open` **不等于**「所有群消息都能收到」— 必须 @ 了 bot 才行。

- 未 @ bot 的消息静默丢弃（日志可见 `dropping inbound event: group_policy_rejected`）
- 设置 `FEISHU_REQUIRE_MENTION=false` 可让 bot 接收所有群消息（无需 @）
- `FEISHU_ALLOW_BOTS` 默认 `none`，所有来自其他 bot 的消息都会被静默拒绝

---

## Bot 间通信

两台 bot 互相 @ 需要双方都配好，缺一不可。

### 发送端配置（@ 别人）

```bash
# .env 中配置 AT_MAP
FEISHU_AT_MAP=对方显示名=对方open_id,别名=对方open_id
```

重启 gateway 后，bot 发出的 `@对方显示名` 会自动转为 post 消息含 `<at user_id="对方open_id">` 标签。

### 接收端配置（被别人 @）

```bash
# .env 中必须配
FEISHU_ALLOW_BOTS=mentions    # 或 all。默认 none 会静默拒绝所有 bot 消息
```

### 验证 @ 是否生效（API 反查）

发送后立即用飞书 API 拉取消息确认：

```bash
# 获取 token
TOKEN=$(curl -s -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json' \
  -d "{\"app_id\":\"$FEISHU_APP_ID\",\"app_secret\":\"$FEISHU_APP_SECRET\"}" | \
  grep -oP '"tenant_access_token":"\K[^"]+')

# 拉取消息
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://open.feishu.cn/open-apis/im/v1/messages/<message_id>"
```

| msg_type | mentions | 结论 |
|----------|----------|------|
| post | 有 mentions | ✅ 正常 |
| text | NONE | ❌ AT_MAP 未触发 |
| post | NONE | ❌ AT_MAP 检测失败（常见：`\b` 边界不匹配中文） |

**验证成功的标志**：
- `msg_type` 为 `"post"`（非 `"text"`）
- `mentions[]` 数组包含目标用户的 `open_id` 和 `name`
- `body.content` 中包含 `{"tag":"at","user_id":"@_user_1","user_name":"..."}`

### ⚠️ FEISHU_AT_MAP 代码回归陷阱

**现象**：`.env` 里 `FEISHU_AT_MAP` 配好了，也重启了 gateway，但 `@某人` 永远是纯文本。

**根因**：`FEISHU_AT_MAP` 的 `<at>` 转换逻辑是手动补丁加到 `feishu.py` 里的，不在 hermes-agent 主线代码中。gateway 更新或 feishu.py 被替换时，补丁代码会被覆盖丢失。

**快速检测**：
```bash
# 如果返回空 → 补丁已丢失，AT_MAP 永远不会生效
grep "at_mention_map\|_parse_at_mention" <hermes_home>/gateway/platforms/feishu.py
```

**修复**：重新应用 AT_MAP 补丁（5 处代码改动，详见 `references/at-mention-code-fix.md`），改前先备份：
```bash
cp <hermes_home>/gateway/platforms/feishu.py{,.bak.$(date +%Y%m%d_%H%M%S)}
```

### 已知 bug：`\b` 边界对中文名无效

`_build_at_mention_post_payload` 中用 `\b` 做边界匹配，但中文字符不是 `\w`，导致 `@中文名` 检测失败。修复：去掉 regex 中的 `\\b`。

### 排查 bot 间通信不生效

1. 先确认出站方的消息格式是否是 post + `<at>`（用飞书 API 拉消息验证）
2. 确认接收方 `FEISHU_ALLOW_BOTS` 不是 `none`
3. 确认接收方 gateway 未重启（WebSocket 断连会丢消息）
4. 检查对方 bot 消息是否到达：`grep "sender=bot:" $HERMES_HOME/logs/gateway.log | tail -20`
5. 如无 dropping 也无入站记录 → 消息未到达（大概率出站方 AT_MAP 未配或配错）

---

## 会话上下文串线

**现象**：群里有多个用户各自跟 bot 对话，bot 在收到用户 A 的新消息时，加载了用户 B 的历史 session 上下文，导致执行错误任务。

**根因（三个参数组合）**：
1. `gateway_auto_continue_freshness: 3600` — 1 小时内活跃过的 session 自动"续杯"而非新建
2. `compression` 开启 — 老 session 被压缩，关键上下文丢失但残影仍存在
3. `session_reset.idle_minutes: 1440` — 24 小时空闲才重置，太长

**🟢 永久修复（config.yaml）**：
```yaml
gateway_auto_continue_freshness: 300   # 5 分钟
session_reset:
  idle_minutes: 60                      # 1 小时重置
```

改前先备份 `config.yaml`，改后重启 gateway。

---

## 故障场景速查表

### 飞书不回复

| 可能原因 | 诊断命令 | 修复 |
|----------|----------|------|
| lark-oapi 未安装 | `<venv>/bin/python -c "import lark_oapi"` | `pip install lark-oapi` |
| Gateway 未运行 | `ps aux \| grep '[h]ermes.*gateway'` | `hermes gateway run &` |
| 用户被鉴权拦截 | `grep "Unauthorized user" $HERMES_HOME/logs/gateway.log` | `.env` 加 `GATEWAY_ALLOW_ALL_USERS=true` |
| 锁文件冲突 | `ls $HERMES_LOCAL_STATE/gateway-locks/` | 删除锁文件后重启 |
| 多余 CLI 进程 | `ps aux \| grep '[h]ermes' \| wc -l` (>3 有问题) | `pkill -9 -f hermes` 全杀后重启 |
| 没 @ bot | `grep "group_policy_rejected" gateway.log` |  @ bot 或设 `FEISHU_REQUIRE_MENTION=false` |
| 凭据无效 | `grep "app_id or app_secret" gateway.log` | 用 curl 验证、重置 Secret |
| Agent 卡死（API超时） | 日志有 `Flushing text batch` 但无后续 `Sending response`；`errors.log` 有 `ReadTimeout`/`APITimeoutError` | 重启 gateway（杀进程→清锁→启动） |

### @ 不生效

| 可能原因 | 诊断命令 | 修复 |
|----------|----------|------|
| AT_MAP 未配 | `grep FEISHU_AT_MAP $HERMES_HOME/.env` | 配置 `FEISHU_AT_MAP=显示名=open_id` |
| 补丁代码丢失 | `grep "at_mention_map" feishu.py` | 重新打补丁 |
| `\b` 边界不匹配中文 | 发送后 API 查消息 → msg_type=post 但 mentions 为空 | 去掉 regex 中的 `\\b` |
| gateway 未重启 | `stat feishu.py` vs gateway 启动时间 | 重启 gateway |
| 接收端 `FEISHU_ALLOW_BOTS=none` | `grep FEISHU_ALLOW_BOTS $HERMES_HOME/.env` | 设为 `mentions` 或 `all` |

### 消息丢失

| 可能原因 | 诊断 | 修复 |
|----------|------|------|
| WebSocket 断连 | `grep -E "Starting\|Gateway stopped\|Disconnected" gateway.log` | 重新连接（自动） |
| Gateway 重启期间 | 对比飞书客户端和 bot 收到消息的时间戳 | 重启后验证连接 |
| `bots_disabled` 拒绝 | `grep "bots_disabled" gateway.log` | `FEISHU_ALLOW_BOTS=mentions` |

### 卡片回调报错

| 错误码 | 含义 | 修复 |
|--------|------|------|
| 200671 | 事件订阅未配置 `card.action.trigger` | 飞书控制台 → 应用 → 事件订阅 → 添加 |
| 200340 | 按钮权限/作用域不对 | 检查卡片权限配置 |

诊断顺序：先修 200671（基础设施），再修 200340（权限）。都不需要重启 gateway。

---

## 安全运维

### 安全重启 Gateway

`hermes gateway restart` 在 30s 超时后会杀掉进程但不确保新进程成功拉起，导致 bot 离线。

**安全重启**：
```bash
pkill -9 -f 'hermes gateway'
sleep 2
rm -f $HERMES_LOCAL_STATE/gateway-locks/feishu-app-id-*.lock
hermes gateway run 2>&1 &
sleep 5 && grep '✓ feishu connected' $HERMES_HOME/logs/gateway.log | tail -1
```

### 锁文件僵尸

旧 gateway 变 `<defunct>` 但锁文件未释放，重启时报 `Another local Hermes gateway is already using this Feishu app_id`。

**修复**：
```bash
rm -f $HERMES_LOCAL_STATE/gateway-locks/feishu-app-id-*.lock
```

### 多实例冲突

多个 gateway 进程同时运行，先启动的持有飞书连接，后续的都被锁拒绝。

**诊断**：
```bash
ps aux | grep -E 'hermes.*gateway' | grep -v grep
```

**修复三步走**：
```bash
pkill -9 -f 'hermes gateway run'; sleep 2
rm -f $HERMES_LOCAL_STATE/gateway-locks/feishu-app-id-*.lock
hermes gateway run 2>&1 &
sleep 5 && grep '✓ feishu connected' $HERMES_HOME/logs/gateway.log | tail -1
```

### 多余 CLI 进程冲突（飞书不回复的隐藏原因）

**现象**：Gateway 日志显示 `✓ feishu connected`，也收到消息 `Inbound group message received`，但 `Flushing text batch` 后无 `Sending response`，飞书端不回复。

**根因**：系统里同时跑了多个 `hermes` CLI 进程（8+ 个），大量 `<defunct>` 僵尸进程，内存/资源竞争导致 agent 处理卡住。

**修复**：全杀只留 gateway。

**预防**：不要同时开多个 hermes CLI 会话。用完 `/exit` 退出，别直接关终端。

### .env 写入保护

Hermes 的 `write_file` 和 `patch` 工具拒绝写入 `.env`（受保护的凭据文件）。变通方案：用 `terminal` 直接 shell 写入：

```bash
printf 'FEISHU_ALLOW_BOTS=mentions\n' >> $HERMES_HOME/.env
```

修改后必须重启 gateway 生效。

### lark-oapi 依赖缺失

**现象**：gateway 日志报 `lark-oapi not installed or FEISHU_APP_ID/SECRET not set`。即使 `.env` 中凭证正确也会报此错——**错误信息具有误导性**，真正根因是 Python 包 `lark-oapi` 未安装。

**修复**：
```bash
# venv 默认不带 pip，需先 ensurepip
<hermes_venv>/bin/python -m ensurepip 2>/dev/null
<hermes_venv>/bin/python -m pip install lark-oapi
# 国内用户：-i https://mirrors.aliyun.com/pypi/simple/
```

### 飞书端「still working...」通知禁用

群聊中长任务时 gateway 会定期发「still working...」，设 0 完全禁用：

```bash
hermes config set agent.gateway_notify_interval 0
```

重启 gateway 生效。无按平台单屏蔽的配置，只能全局关。

### 飞书显示配置（隐藏思考过程 & 工具调用）

```yaml
# config.yaml
display:
  platforms:
    feishu:
      show_reasoning: false    # 隐藏 AI 思考过程
      tool_progress: "off"     # 隐藏工具调用详情（可选: "new", "all", "off"）
```

修改后需重启 gateway。

---

## 飞书 API 调试手段

当网关日志不完整时，直接用飞书 Open API 交叉验证。

### 获取 token

```bash
TOKEN=$(curl -s -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json' \
  -d "{\"app_id\":\"$FEISHU_APP_ID\",\"app_secret\":\"$FEISHU_APP_SECRET\"}" | \
  grep -oP '"tenant_access_token":"\K[^"]+')
```

Lark 国际版：`https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal`

### 查群成员列表

```bash
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://open.feishu.cn/open-apis/im/v1/chats/<chat_id>/members?page_size=20"
```

返回 `items[].member_id`（open_id）和 `items[].name`（显示名）。

### 反查已发送消息内容

```bash
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://open.feishu.cn/open-apis/im/v1/messages/<message_id>"
```

返回 `msg_type`（text/post）、`mentions[]`、`body.content`（JSON 字符串，含 `<at>` 标签结构）。

### 认证错误码速查

| 错误码 | 含义 | 处理 |
|--------|------|------|
| `0` | 成功 | — |
| `10014` | App Secret 无效 | 开放平台「凭证与基础信息」重置 Secret |
| `10013` | App ID 无效 | 检查 App ID 是否正确复制 |
| `1000040345` | SDK 层 app_id/app_secret 无效 | 用 curl 确认具体是哪个 |

---

## 交互卡片回调

### 发送测试卡片

```bash
curl -s -X POST 'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "receive_id": "<chat_id>",
    "msg_type": "interactive",
    "content": "{\"header\":{\"title\":{\"tag\":\"plain_text\",\"content\":\"测试\"}},\"elements\":[{\"tag\":\"action\",\"actions\":[{\"tag\":\"button\",\"text\":{\"tag\":\"plain_text\",\"content\":\"点我\"},\"type\":\"primary\",\"value\":\"{\\\"action\\\":\\\"test\\\"}\"}]}]}"
  }'
```

### 200671 错误

飞书卡片回调报 200671 时，通常是开放平台「事件与回调」中未配置卡片回调 URL。在飞书控制台 → 应用 → 事件订阅 → 添加 `card.action.trigger` 事件即可。不需改代码。

---

## 排查纪律

所有问题排查前先确认：

```bash
# 1. token 有效
curl -s -X POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal \
  -H 'Content-Type: application/json' \
  -d "{\"app_id\":\"$FEISHU_APP_ID\",\"app_secret\":\"$FEISHU_APP_SECRET\"}" | grep '"code":0'

# 2. 群成员
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://open.feishu.cn/open-apis/im/v1/chats/<chat_id>/members"

# 3. 消息内容
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://open.feishu.cn/open-apis/im/v1/messages/<message_id>"
```

### 改动后验证清单

每次改代码/配置/重启后，必须逐项确认：

| 验证项 | 命令 | 预期结果 |
|--------|------|----------|
| gateway 进程 | `ps aux \| grep gateway` | PID 存在 |
| 飞书连接 | `grep '✓ feishu connected' gateway.log \| tail -1` | 连接成功 |
| AT_MAP 代码 | `grep at_mention_map feishu.py` | 有匹配 |
| 出站 @ 消息 | 发测试 → API 查 message | msg_type=post, mentions 非空 |
| 入站消息 | `tail gateway.log \| grep "Inbound"` | 有新消息 |

### 经典排错方法论

**症状 → 证据 → 假说 → 验证 → 结论**，不跳步：

1. 拿一个假说 → 一条路走到头，确认或排除后再切假说
2. 每一步都验证（API 查消息 / grep 日志 / 对比时间戳）
3. 不要嘴说"应该好了"——必须用命令验证

**反面教材**：在两个假说间反复跳——先说"代码被覆盖了"，又说"`\b` 边界问题"，没一次查到底。正确做法是：API 拉消息 → msg_type=text → 查 AT_MAP 代码 → 找到匹配逻辑 → 定位根因 → 修复。

---

## WebSocket 连接稳定性

- 飞书 WebSocket 长连接模式，Gateway PID 随重启变化
- 连接中断期间群消息会丢失，bot 无法感知
- 排查思路：对比飞书客户端群聊记录和 bot 收到的消息，交叉验证是否漏消息

## 认证

- 获取 tenant_access_token: `POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal`
- feishu_doc / feishu_drive 仅在 gateway 会话中可用

### Gateway 全局用户鉴权陷阱

**现象**：Feishu adapter 配置正确（group_policy=open），消息到达 gateway（日志可见 `Inbound group message received`），但 bot 不回复。

**根因**：Gateway 层面有独立的用户白名单机制，默认拒绝所有用户，报错 `WARNING gateway.run: Unauthorized user: xxx on feishu`。这个报错出现在 gateway.log 但不出现在 errors.log，容易被忽略。

**修复**：在 `.env` 中设置 `GATEWAY_ALLOW_ALL_USERS=true`。

---

## 相关资源

- 一键恢复脚本模板：见本 skill 的 `scripts/feishu-gateway-recover.sh`
- 社区飞书 skill 清单：Hermes Skill Registry 搜索 tag:feishu
