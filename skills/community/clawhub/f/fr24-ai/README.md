# FR24-AI · 航路国际机票 Agent Skill

[English](README.en.md)

Flightroutes24（航路）国际机票 **Agent Skill**（`fr24-ai`）：通过 Python 脚本对接 export 网关，支持自然语言解析、演示/采购查价、校验与生单。供 Cursor、Claude Code 等 Agent 在对话中调用。

| 项 | 说明 |
|----|------|
| 项目名 | FR24-AI |
| Skill ID | `fr24-ai` |
| 作者 | FR24 |
| Python | 3.10+ |

---

## 功能概览

| 模式 | 条件 | 能力 |
|------|------|------|
| 演示查价 | 未配置采购密钥 | `POST /ai/shopping` + `X-Skill-Client-Key`，每 clientKey 每日限额（默认 10 次） |
| 采购查价 | 已配置 APPKEY + 签名密钥 | 同上，携带 `appkey` 与 `authentication`，不扣演示日配额 |
| 预订 | 另需 AES 密钥 | `POST /api/new/pricing`（校验）、`POST /api/new/booking`（生单） |

- 支持 **单程 / 往返**（最多 2 段），不支持缺口程
- 自然语言解析城市、日期、人数、舱位；支持航司、起飞时段 **refine** 后重新搜索
- 结果摘要：**直飞最低** + **中转最低**（含退改、行李摘要）
- 标准输出 JSON：`userView`（可展示给用户）与 `agentOnly`（仅 Agent 内部续跑）

---

## 快速开始

### 1. 环境

```bash
cd /path/to/skill
pip install -r requirements.txt   # 预订功能需要；仅查价可暂不安装
```

### 2. 安装到 Agent

将本目录复制到 Agent 的 skills 路径，文件夹名须为 **`fr24-ai`**（与 `SKILL.md` 中 `name` 一致）：

| 产品 | 路径示例 |
|------|----------|
| Cursor | `~/.cursor/skills/fr24-ai/` |
| Claude Code | `~/.claude/skills/fr24-ai/` |

详细步骤见 [INSTALL.md](./INSTALL.md)。

### 3. 网关配置

在 **`config.py`** 中修改（勿使用 `skill.local.env`）：

```python
EXPORT_BASE_URL = "https://flight.flightroutes24.com"
```

搜索实际请求：`{EXPORT_BASE_URL}/ai/shopping`。

### 4. 本地验证

```bash
python scripts/skill_search_client.py ensure-key
python scripts/nl_to_search.py parse --text "深圳到曼谷 6月1日 1成人"
python scripts/skill_search_client.py search --payload-file .cache/pending_search.json
```

---

## 配置说明

| 配置项 | 位置 | 说明 |
|--------|------|------|
| `EXPORT_BASE_URL` | `config.py` | export 网关根地址 |
| `GRAY_HEADER` | `config.py` | 灰度路由请求头（如 `ww`） |
| `FR_NEWAPI_APPKEY` | 环境变量 / `.env` / `keys.json` | 采购 APPKEY |
| `FR_NEWAPI_SIGN_SECRET` | 环境变量 / `.env` / `keys.json` | SHA512 签名密钥 |
| `FR_NEWAPI_AES_SECRET` | 环境变量 / `.env` / `keys.json` | 16 字节 AES（预订加密乘客） |

采购密钥支持三种配置方式（优先级从高到低）：

1. **环境变量**（需重启 Agent 生效）
2. **`.env` 文件**（Skill 根目录，无需重启）
3. **`config_keys.py set`**（写入 `.cache/keys.json`，无需重启）

检查采购配置是否生效：

```bash
python scripts/config_keys.py status
```

或：

```bash
python -c "import config; print('configured:', config.is_newapi_configured()); print('booking_ready:', config.is_booking_ready())"
```

用户侧密钥配置说明：[references/user-appkey-config.md](./references/user-appkey-config.md)  
维护者联调说明：[references/setup-maintainer.md](./references/setup-maintainer.md)

---

## 目录结构

```
fr24-ai/
├── README.md                 # 本文件（中文）
├── README.en.md              # English
├── SKILL.md                  # Agent 业务流程与触发词
├── INSTALL.md                # 安装说明
├── config.py                 # 网关常量与采购环境变量读取
├── requirements.txt
├── scripts/
│   ├── nl_to_search.py       # 自然语言 parse / refine
│   ├── skill_search_client.py
│   ├── skill_booking_client.py
│   ├── newapi_client.py      # HTTP 客户端
│   └── ...
├── references/               # 业务与展示规范
└── .cache/                   # 本地状态（勿提交 git）
    ├── skill_client.json
    ├── pending_search.json
    └── booking_context.json
```

---

## 常用命令

在 Skill 根目录执行：

| 命令 | 说明 | 扣演示配额 |
|------|------|------------|
| `python scripts/nl_to_search.py parse --text "..."` | 解析行程 | 否 |
| `python scripts/nl_to_search.py refine --text "..."` | 合并航司/时段等条件 | 否 |
| `python scripts/skill_search_client.py search --payload-file .cache/pending_search.json` | 搜索 | 是（演示模式） |
| `python scripts/skill_search_client.py search ... --selection direct\|transfer` | 搜索并选中直飞/中转 | 是 |
| `python scripts/skill_booking_client.py parse-passengers --text "..."` | 解析乘客 | — |
| `python scripts/skill_booking_client.py verify --passenger-confirmed` | 校验报价 | — |
| `python scripts/skill_booking_client.py order --user-confirmed` | 生单 | — |
| `python scripts/config_keys.py status` | 查看密钥配置状态 | — |
| `python scripts/config_keys.py set --appkey ... --sign-secret ... --aes-secret ...` | 配置采购密钥 | — |
| `python scripts/config_keys.py clear` | 清除本地密钥配置 | — |

Agent 须先向用户确认行程再执行 `search`；预订须两次用户确认（乘客、生单）。详见 [SKILL.md](./SKILL.md)。

---

## 文档索引

| 文档 | 用途 |
|------|------|
| [SKILL.md](./SKILL.md) | Agent 指令、查价/预订流程 |
| [INSTALL.md](./INSTALL.md) | 安装与环境 |
| [references/booking.md](./references/booking.md) | 预订步骤 |
| [references/search_params.md](./references/search_params.md) | 搜索请求参数 |
| [references/output-rules.md](./references/output-rules.md) | 对用户展示规范 |
| [references/user-appkey-config.md](./references/user-appkey-config.md) | 用户配置采购密钥 |
| [references/setup-maintainer.md](./references/setup-maintainer.md) | 维护者联调（勿展示给用户） |

---

## 安全与注意事项

- 勿将 `.cache/`、`skill_client.json` 或采购密钥提交到版本库或在对话中明文发送
- 仅将脚本输出中的 **`userView`** / **`message`** 展示给用户；`agentOnly`（含 `traceId`、`offerId`）仅供内部续跑
- 生单为真实订单，必须在用户明确确认后调用 `order`
- 演示配额用尽（`307901`）：引导用户开通采购并配置密钥

---

## 相关链接

- 航路官网：https://www.flightroutes24.com/
