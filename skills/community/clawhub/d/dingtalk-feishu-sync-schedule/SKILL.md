# dingtalk-feishu-sync-schedule

**功能**：将钉钉日历日程同步到飞书日历（钉钉 → 飞书，单向）
**同步范围**：本周（今天 + 未来6天）
**定时同步**：每天 09:00 / 12:00 / 15:00 自动执行

---

## 执行同步

```bash
python3 /root/.openclaw/workspace/skills/dingtalk-feishu-sync-schedule/sync_week_ahead.py
```

脚本自动处理：
- 获取钉钉本周所有日程（过滤已取消）
- 刷新飞书 access_token（自动检测，过期刷新）
- 清理飞书旧同步日程（根据描述含"从钉钉自动同步"判断）
- 重建所有日程到飞书

**保护机制**：手动创建的飞书日程不会被删除（只删带同步标记的）

---

## 配置文件

### 钉钉 `~/.dingtalk/config.json`

| 字段 | 说明 |
|------|------|
| `app_key` | 钉钉应用 Key，从 OpenClaw 配置自动读取 |
| `app_secret` | 钉钉应用 Secret，从 OpenClaw 配置自动读取 |
| `user_id` | 钉钉 unionid，Agent 根据用户手机号自动获取并填充 |

### 飞书 `~/.feishu/config.json`

| 字段 | 说明 |
|------|------|
| `app_id` | 飞书应用 ID，从 OpenClaw 配置自动读取 |
| `app_secret` | 飞书应用 Secret，从 OpenClaw 配置自动读取 |
| `user_open_id` | 飞书用户 open_id，从 OpenClaw 配置自动读取 |
| `calendar_id` | 飞书日历 ID，Agent 自动获取并填充 |
| `access_token` | 运行时 token，Agent 自动管理 |
| `refresh_token` | 刷新凭证，用户授权后 Agent 自动获取 |

---

## 首次配置流程

当配置文件缺失或不完整时，按以下步骤引导用户：

### Step 0: 开通应用权限

**在开始配置前，需在钉钉和飞书开放平台分别为两个应用开通日历相关权限：**

#### 钉钉应用（需管理员权限）
登录 [钉钉开放平台](https://open.dingtalk.com/) → 找到对应应用 → **权限管理** → 开通以下权限：
- `Calendar` → `calendar:calendar:read` （读取日历）
- `Calendar` → `calendar:calendar:write` （写入日历）

#### 飞书应用（需管理员权限）
登录 [飞书开放平台](https://open.feishu.cn/) → 找到对应应用 → **权限管理** → 开通以下权限：
- `calendar:calendar:read` （读取日历）
- `calendar:calendar:write` （写入日历）

> 如果应用为企业内部自用，需确认管理员已审批通过上述权限申请。权限开通后约5分钟生效。

### Step 1: 初始化配置
```bash
python3 /root/.openclaw/workspace/skills/dingtalk-feishu-sync-schedule/scripts/init_config.py
```
钉钉配置读取优先级：
1. `~/.dingtalk/config.json` — 优先读取
2. `~/.openclaw/openclaw.json` — 缺失时自动补充并回写 dingtalk/config.json
3. 仍缺失 → 提示用户输入

飞书配置：从 `~/.openclaw/openclaw.json` 读取，写入 `~/.feishu/config.json`

### Step 2: 获取钉钉 unionid

Agent 询问用户提供以下任一信息：

**方式1: 直接提供 unionid**
用户直接输入 unionid，Agent 直接写入 `~/.dingtalk/config.json`，跳过 API 调用。

**方式2: 提供手机号**
Agent 调用钉钉 API 获取 unionid 后写入配置：

**API 1**: 通过手机号获取 userid
```
POST https://oapi.dingtalk.com/topapi/v2/user/getbymobile?access_token={access_token}
Body: {"mobile": "用户手机号"}
```
access_token 通过 `GET https://api.dingtalk.com/v1.0/oauth2/accessToken` 获取（Body: `{"appKey":"app_key","appSecret":"app_secret"}`）

**API 2**: 通过 userid 获取 unionid
```
POST https://oapi.dingtalk.com/topapi/v2/user/get?access_token={access_token}
Body: {"language": "zh_CN", "userid": "Step1返回的userid"}
```

获取后自动写入 `~/.dingtalk/config.json` 的 `user_id` 字段。

### Step 3: 飞书授权（获取 refresh_token）

**生成授权链接**（app_id 从配置文件读取）：
```
https://open.feishu.cn/open-apis/authen/v1/index?app_id={app_id}&scope=calendar:calendar:read%20calendar:calendar:write&redirect_uri=https://example.com
```

引导用户访问链接，授权后将 url 中 `?code=xxx` 的 code 部分给 Agent。

**用 code 换取 refresh_token**：
```
POST https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal
Body: {"app_id": "xxx", "app_secret": "xxx"}
```
再用返回的 `app_access_token` 调用：
```
POST https://open.feishu.cn/open-apis/authen/v1/oidc/access_token
Body: {"app_access_token": "xxx", "grant_type": "authorization_code", "code": "用户给的code"}
```
返回的 `refresh_token` 自动写入配置文件。

### Step 4: 获取 calendar_id
Agent 通过飞书 API 获取用户主日历 ID，自动写入配置文件。

### Step 5: 验证
运行同步脚本验证配置正确性。

---

## Token 管理

| Token 类型 | 有效期 | 刷新方式 |
|-----------|--------|---------|
| 钉钉 access_token | 2小时 | 每次同步自动获取（新token） |
| 飞书 access_token | 2小时 | 脚本自动检测，过期调用 refresh API |
| 飞书 refresh_token | 30天 | 过期后需重新授权（见上文 Step 3） |

### 手动刷新飞书 token
```bash
python3 /root/.openclaw/workspace/skills/dingtalk-feishu-sync-schedule/utils/refresh_token.py
```

---

## 定时任务

### 查看
```bash
crontab -l | grep dingtalk
```

### 编辑
```bash
crontab -e
```

当前配置：
```
0 9,12,15 * * * /usr/bin/python3 /root/.openclaw/workspace/skills/dingtalk-feishu-sync-schedule/sync_week_ahead.py >> /var/log/dingtalk_sync.log 2>&1
```

### 日志
```bash
tail -f /var/log/dingtalk_sync.log
```

---

## 故障排查

| 症状 | 可能原因 | 处理方式 |
|------|---------|---------|
| 同步失败/钉钉日程获取为空 | unionid 错误或已失效 | 重新执行 Step 2 获取 unionid |
| 飞书日程创建失败 | access_token 过期 | 手动刷新 token |
| refresh_token 过期 | 超过30天未授权 | 重新授权（Step 3） |
| 日程时间差8小时 | 时区问题 | 检查脚本时区逻辑，API 返回时间已做 +08:00 转换 |
| 飞书日历空白 | calendar_id 指向错误日历 | 重新获取 calendar_id |

### 调试
直接运行脚本，查看实时输出：
```bash
python3 /root/.openclaw/workspace/skills/dingtalk-feishu-sync-schedule/sync_week_ahead.py
```

---

## 安全须知

- **配置文件中的 app_secret / refresh_token 不可外泄**
- 脚本不打印任何 token 实际值（只打印前10位用于确认）
- 同步日志不包含敏感信息
- 所有敏感凭证仅存储在本地配置文件，不硬编码在脚本中

---

## 关键 API

### 钉钉
- `POST https://api.dingtalk.com/v1.0/oauth2/accessToken` — 获取 access_token
- `GET https://api.dingtalk.com/v1.0/calendar/users/{unionId}/calendars/primary/events` — 获取日历事件列表

### 飞书
- `POST https://open.feishu.cn/open-apis/authen/v1/refresh_access_token` — 刷新 access_token
- `GET https://open.feishu.cn/open-apis/calendar/v4/calendars/{calendarId}/events` — 获取日历事件
- `POST https://open.feishu.cn/open-apis/calendar/v4/calendars/{calendarId}/events` — 创建日历事件
- `DELETE https://open.feishu.cn/open-apis/calendar/v4/calendars/{calendarId}/events/{eventId}` — 删除日历事件

---

## 文件结构

```
dingtalk-feishu-sync-schedule/
├── sync_week_ahead.py         # 主同步脚本
├── scripts/
│   ├── config_loader.py      # 配置加载器
│   └── init_config.py        # 初始化脚本（从 openclaw.json 读取凭证）
├── utils/
│   └── refresh_token.py      # 飞书 token 刷新工具
└── SKILL.md                  # 本文件
```
