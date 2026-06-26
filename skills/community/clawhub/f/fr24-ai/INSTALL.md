# FR24-AI 安装说明

项目概览见 **[README.md](./README.md)**（中文）/ **[README.en.md](./README.en.md)**（English）。

## 产品信息

| 项 | 说明 |
|----|------|
| 项目名称 | FR24-AI |
| Skill 标识 | `fr24-ai` |
| 产品名称 | Flightroutes24 航路国际机票 |
| 作者 | FR24 |
| 能力范围 | 国际机票查询（演示/采购）、校验、生单（需配置采购密钥） |

本文说明如何在 Cursor、Claude Code 等 Agent 环境中安装并启用本 Skill。

---

## 一、环境要求

1. **服务端**：export 已发布 Skill 搜索接口 `POST /ai/shopping`，且账号体系已配置演示采购 **`SKILL_DEMO`**（演示查价）。
2. **本机**：Python **3.10 及以上**。
3. **预订功能**（可选）：执行 `pip install -r requirements.txt` 安装依赖（含 `pycryptodome`、`pypinyin`）。

---

## 二、获取安装包

从公司内部仓库或发布包取得 **FR24-AI（fr24-ai）** 完整目录，确保包含 `SKILL.md`、`config.py`、`scripts/`、`references/` 等文件。

**注意**：不要将 `.cache/`、`__pycache__/` 或他人机器上的 `skill_client.json`（含 `clientKey`）拷贝或提交到版本库。

---

## 三、安装到 Agent

### 3.1 推荐目录

| 方式 | 路径 | 说明 |
|------|------|------|
| 用户级（推荐） | `~/.cursor/skills/fr24-ai/` | 本机所有工作区可用 |
| 项目级 | `<项目根>/.cursor/skills/fr24-ai/` | 随项目共享给团队 |

其他 Agent 产品请将目录置于其 **skills 扫描路径**，且文件夹名与 `SKILL.md` 中 `name: fr24-ai` 一致。

| 产品 | 常见 skills 路径 |
|------|------------------|
| Cursor | `~/.cursor/skills/fr24-ai/` 或 `.cursor/skills/fr24-ai/` |
| Claude Code | `~/.claude/skills/fr24-ai/` |

### 3.2 安装命令示例

**Windows（用户级）：**

```powershell
xcopy /E /I "D:\path\to\FR24-AI" "%USERPROFILE%\.cursor\skills\fr24-ai"
```

**macOS / Linux：**

```bash
cp -r /path/to/FR24-AI ~/.cursor/skills/fr24-ai
```

### 3.3 目录结构（安装后）

```
fr24-ai/
├── README.md             # 项目说明（中文）
├── README.en.md          # Project overview (English)
├── SKILL.md              # Agent 指令与业务流程
├── INSTALL.md            # 本安装说明
├── config.py
├── requirements.txt
├── scripts/
│   ├── nl_to_search.py
│   ├── skill_search_client.py
│   └── skill_booking_client.py
└── references/
    ├── places.json
    ├── output-rules.md
    ├── user-appkey-config.md
    ├── booking.md
    └── search_params.md
```

安装完成后 **重启 Cursor**（或重新打开 Agent 会话），以便根据 `SKILL.md` 的 `description` 自动匹配（如：查航班、搜机票、预订等）。

---

## 四、配置

### 4.1 网关（`config.py`）

export 根地址与灰度头在 **`config.py`** 中固定：

- `EXPORT_BASE_URL`（默认 `https://flight-deve.flightroutes24.com`）
- `GRAY_HEADER`（deve 默认 `ww`）

切换测试/生产环境时由维护者直接修改该文件，**无需** `skill.local.env`。

### 4.2 演示查价

无需额外配置。首次搜索时本机会自动生成 `clientKey`（保存在 `.cache/skill_client.json`），请勿外传。

### 4.3 采购搜索与预订

在 [航路官网](https://www.flightroutes24.com/) 开通 API 采购后，按 **[references/user-appkey-config.md](./references/user-appkey-config.md)** 在本机 **用户环境变量** 中配置：

- `FR_NEWAPI_APPKEY`
- `FR_NEWAPI_SIGN_SECRET`
- `FR_NEWAPI_AES_SECRET`

配置后需 **完全退出并重新打开** Agent 客户端。

**配置是否生效**（在本机 Skill 目录执行）：

```powershell
python -c "import config; print('configured:', config.is_newapi_configured()); print('booking_ready:', config.is_booking_ready())"
```

| 输出 | 含义 |
|------|------|
| `configured: True` | 可进行采购账号搜索 |
| `booking_ready: True` | 可进行校验、生单 |

---

## 五、安装验证

在 **fr24-ai** 目录下执行：

```bash
python scripts/skill_search_client.py ensure-key
python scripts/nl_to_search.py parse --text "深圳到曼谷 6月1日 1成人"
```

若 `parse` 返回 `status: success` 且 `userView` 中含行程与日期，说明解析与本地环境正常。

用户确认行程后，由 Agent 执行搜索（将消耗演示日配额，若已配置采购密钥则不受演示日限额约束）：

```bash
python scripts/skill_search_client.py search --payload-file .cache/pending_search.json
```

搜索成功时响应中 `code` 为 `000000`，且 `userView` 含直飞/中转报价摘要。

---

## 六、配额与安全

| 模式 | 条件 | 搜索接口 | 配额 |
|------|------|----------|------|
| 演示 | 未配置 `FR_NEWAPI_APPKEY` | `POST /ai/shopping` + `X-Skill-Client-Key` | 每 clientKey 每日限额（默认 10，以 export 配置为准） |
| 采购 | 已配置 APPKEY 与签名密钥 | 同上，请求带 `authentication` 与头 `appkey` | 不扣演示日配额 |

- 演示日配额用尽（`307901`）：引导用户开通采购并配置密钥，见 `user-appkey-config.md`。
- 勿将 `clientKey`、采购密钥提交至 git 或在对话中发送给他人。

---

## 七、常见问题

| 现象 | 建议处理 |
|------|----------|
| HTTP 404 | 确认 `config.py` 中 `EXPORT_BASE_URL`、`GRAY_HEADER` 正确且 export 已发布 `/ai/shopping` |
| `307901` | 演示配额已用完；开通采购并配置 APPKEY 后继续搜索 |
| `307900` | `clientKey` 格式无效，删除 `.cache/skill_client.json` 后重新执行 `ensure-key` |
| Agent 未触发 Skill | 确认 `SKILL.md` 位于 skills 目录且已重启 Agent；`description` 需包含查价相关场景 |

---

## 八、相关文档

| 文档 | 用途 |
|------|------|
| [SKILL.md](./SKILL.md) | Agent 业务流程与命令 |
| [references/output-rules.md](./references/output-rules.md) | 对用户展示与下载规范 |
| [references/user-appkey-config.md](./references/user-appkey-config.md) | 用户配置采购密钥 |
| [references/booking.md](./references/booking.md) | 预订流程说明 |
| [references/search_params.md](./references/search_params.md) | 搜索请求参数说明 |
