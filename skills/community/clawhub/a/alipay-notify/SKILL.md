---
name: alipay-notify-relay
description: >-
  支付宝异步通知中继：本地开发无公网 IP 也能收到支付宝异步通知。
  Skill 自包含 CLI 脚本，安装后 Agent 自动执行注册 → 获取 notify_url → 实时监听 → 查看原始报文 → 本地验签全流程。
  仅依赖 Python 3，无需部署服务端。仅限联调环境。
---

# 支付宝异步通知中继

> **仅限联调/沙箱/内部调试**，不可用于生产。

## 它解决什么问题

本地开发环境没有公网 IP，无法接收支付宝异步通知（`notify_url`）。  
本 Skill 内置 CLI 脚本 + 云端中继服务，安装后 Agent 直接运行即可在本地实时收到支付宝的异步通知。

```
支付宝 ──POST──► 云端中继 /notify/<token>
                       │
                       └──► 开发者本机 CLI 实时拉取
                             ├─ 查看原始报文
                             ├─ RSA2 验签
                             └─ 对接本地业务逻辑
```

## Skill 目录结构

```
alipay-notify-relay/
├── SKILL.md           # 本文件（Agent 指令）
└── scripts/
    └── cli.py         # CLI 工具（注册/监听/查询/验签/导出）
```

## Agent 执行规则

**本 Skill 的所有 CLI 操作由 Agent 直接在终端执行，开发者无需手动输入命令。**

Agent 必须先定位 CLI 脚本路径：SKILL.md 同级目录下的 `scripts/cli.py`。  
执行方式：
```bash
# SKILL_DIR 是 SKILL.md 所在目录的绝对路径
python3 "$SKILL_DIR/scripts/cli.py" <command> [args]
```

- 配置自动保存到开发者当前工作目录的 `.alipay-notify.json`
- 验签在开发者本地完成，云端不存私钥

---

## 前置条件

- Python 3.6+（macOS/Linux 自带）
- 验签（可选）需额外安装：`pip install cryptography`
- **无需部署服务端** — 中继服务已在云端运行，安装 Skill 后直接用 CLI 注册即可

---

## 完整流程

### Step 1：注册（获取异步通知地址）

Agent 执行：
```bash
python3 "$SKILL_DIR/scripts/cli.py" register --server http://8.136.213.223:9010 --name <开发者名称>
```

- 默认中继服务地址：`http://8.136.213.223:9010`
- 如果配置文件中已有 `server_url`，可省略 `--server`
- 不带任何参数则进入交互式引导

输出 `notify_url`，开发者将其传入支付下单接口即可。

> 同一 IP 只能注册一次。重复执行返回已有凭证。

### Step 2：支付接口传入 notify_url

**`notify_url` 是调用下单接口的参数，不是在开放平台控制台配置的。**

Java：
```java
request.setNotifyUrl("<notify_url>");
```

Python：
```python
result = client.page_execute(request, notify_url="<notify_url>")
```

### Step 3：支付成功后获取异步通知

Agent 执行：
```bash
# 实时监听（不自动确认，保留支付宝重试能力）
python3 "$SKILL_DIR/scripts/cli.py" listen

# 查询已收到的通知
python3 "$SKILL_DIR/scripts/cli.py" list

# 查看某条通知完整内容
python3 "$SKILL_DIR/scripts/cli.py" get <id>

# 导出并打印原始报文
python3 "$SKILL_DIR/scripts/cli.py" export <id> && cat notify_<id>.txt
```

> **ack 策略**：`listen` 默认不加 `--auto-ack`，避免自动确认导致支付宝停止重试。
> 仅当开发者明确要求「自动确认」时才使用 `listen --auto-ack`。
> 手动确认单条：`python3 "$SKILL_DIR/scripts/cli.py" ack <id>`

### Step 4：本地验签

开发者在自己项目中用支付宝公钥做 RSA2 验签。

CLI 快速验签（可选）：

1. 配置支付宝公钥（仅首次）：向开发者索取支付宝公钥（Base64 格式，以 `MIIBIjAN` 开头），写入 `.alipay-notify.json`：
```bash
# Agent 直接编辑 .alipay-notify.json，添加 alipay_public_key 字段
# 值为支付宝公钥 Base64 字符串（不含 PEM 头尾）
```

2. 执行验签：
```bash
python3 "$SKILL_DIR/scripts/cli.py" verify <id>
```

### Step 5：重新获取异步地址 / 查询通知

```bash
# 重新获取（返回已有凭证）
python3 "$SKILL_DIR/scripts/cli.py" register

# 查看本地配置
python3 "$SKILL_DIR/scripts/cli.py" config

# 查询通知列表
python3 "$SKILL_DIR/scripts/cli.py" list

# 检查服务状态
python3 "$SKILL_DIR/scripts/cli.py" status
```

---

## CLI 命令速查

所有命令格式：`python3 "$SKILL_DIR/scripts/cli.py" <command> [args]`

| 命令 | 说明 |
|------|------|
| `register` | 注册，获取 notify_url（支持 `--server`、`--name` 或交互式） |
| `listen` | 实时监听通知（支持 `--out-trade-no` 按订单过滤） |
| `listen --auto-ack` | 监听 + 自动确认（仅开发者明确要求时使用） |
| `list` | 查询最近通知（支持 `--limit`、`--out-trade-no`、`--trade-status`） |
| `get <id>` | 查看通知详情（含格式化原始报文） |
| `export <id>` | 导出原始报文到文件（支持 `-o` 自定义文件名，默认 `notify_<id>.txt`） |
| `ack <id>` | 确认通知（停止支付宝重试） |
| `verify <id>` | 验签通知（需先配置 `alipay_public_key`） |
| `status` | 检查服务状态 |
| `config` | 查看当前配置 |

---

## 安全与容量

| 机制 | 默认值 |
|------|--------|
| 通知保留 | 1 天自动清除 |
| 每租户通知上限 | 200 条 |
| 租户注册上限 | 1000 |
| 每租户 SSE 连接 | 3 个 |
| 同一 IP 限注册 | 1 次 |
| 通知入口限流 | 300/min |
| 注册限流 | 10/hour |

---

## Agent 约束

1. **不存私钥** — 云端无商户私钥
2. **验签在本地** — 开发者自行完成
3. **报文原样** — raw_body 是支付宝的原始报文
4. **租户隔离** — 数据严格隔离，无法访问他人
5. **不主动 ack** — 查看/查询通知时不自动确认，保留支付宝重试能力。仅当开发者明确要求时才 ack
6. **原始报文必须打印** — 当开发者要求查看原始内容时，用 `export` 导出后 `cat` 打印完整 URL 编码原始报文到终端（`get` 命令展示的是格式化版本，不是原始报文）