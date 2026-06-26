---
name: feishu-meeting-call
description: 通过飞书发送加急消息提醒用户。支持应用内加急和电话加急（真正打电话到手机）。
version: 1.3.0
tools: Bash, Read
metadata: {"clawdbot":{"emoji":"📞","primaryEnv":"FEISHU_APP_ID","requires":{"bins":["python3"],"env":["FEISHU_APP_ID","FEISHU_APP_SECRET","FEISHU_USER_OPEN_ID"]}}}
---

# 飞书紧急提醒

通过飞书发送加急消息，实现紧急提醒。支持**电话加急**（真正打电话到手机）和**应用内加急**（飞书 App 强推送）两种方式。

## 首次使用配置（最高优先级）

**每次执行技能前，必须先检查环境变量。** 缺哪项补哪项，不要全量重配。

### 检查步骤

```bash
echo "APP_ID=${FEISHU_APP_ID:-(未设置)}" && echo "APP_SECRET=${FEISHU_APP_SECRET:-(未设置)}" && echo "USER_OPEN_ID=${FEISHU_USER_OPEN_ID:-(未设置)}"
```

- 三项都存在 → 跳过本节，直接执行用户请求
- 任何一项显示「未设置」→ 只针对缺失项执行下方对应步骤

### 补全缺失的 FEISHU_APP_ID / FEISHU_APP_SECRET

仅当 APP_ID 或 APP_SECRET 缺失时执行。

**向用户索取凭证：**
> 需要配置飞书应用凭证才能使用。请提供：
> - **App ID** 和 **App Secret** — 在 [飞书开放平台](https://open.feishu.cn/app) → 应用详情 → 凭证与基础信息 中获取
>
> 如果还没有飞书应用，请参考下方「飞书应用创建指南」创建。

**用户提供后，用 `save-config` 保存凭证（跨平台、幂等）：**

```bash
python3 {baseDir}/scripts/feishu_meeting.py save-config --app-id "用户提供的AppID" --app-secret "用户提供的AppSecret"
```

> **安全提醒**：写入完成后，**不要在聊天中回显 App Secret 明文**。只需告诉用户「凭证已保存」。

### 补全缺失的 FEISHU_USER_OPEN_ID

仅当 FEISHU_USER_OPEN_ID 缺失时执行。需要 APP_ID/SECRET 已就绪。

**向用户索取手机号或邮箱，然后 lookup：**

```bash
python3 {baseDir}/scripts/feishu_meeting.py lookup --phone "用户的手机号"
```

**查到 open_id 后，保存到配置文件：**

```bash
python3 {baseDir}/scripts/feishu_meeting.py save-config --user-id "查到的open_id"
```

### 配置完成

补全所有缺失项后告诉用户：
> 飞书配置已保存，后续使用无需再次配置。

然后**继续执行用户原本的请求**（发提醒、打电话等），Python 脚本会自动加载配置文件：

```bash
python3 {baseDir}/scripts/feishu_meeting.py notify --message "xxx"
```

### 飞书应用创建指南

如果用户还没有飞书应用，引导他们：

1. 打开 [飞书开放平台](https://open.feishu.cn/app)，点击「创建企业自建应用」
2. 填写应用名称和描述，创建应用
3. 记录 **App ID** 和 **App Secret**
4. 左侧「应用能力」→ 添加「机器人」能力
5. 左侧「权限管理」→ 搜索并开通以下权限：
   - `im:message`（发送消息）
   - `im:message.urgent:phone`（电话加急）
   - `contact:user.id:readonly`（查找用户）
6. 左侧「版本管理与发布」→ 可用范围中添加自己 → 创建版本并发布

## 目标用户判断（重要）

执行提醒前，你需要判断提醒发给谁：

### 情况 1：提醒自己（默认）

用户说「提醒我」「给我打个电话」「叫我一下」等**没有提到其他人**的情况，直接使用默认的 `FEISHU_USER_OPEN_ID`（即用户自己）。

```bash
# 不需要 --user-id，自动使用环境变量中配置的用户
python3 {baseDir}/scripts/feishu_meeting.py notify --message "小龙虾提醒你：该干活了"
```

如果 `FEISHU_USER_OPEN_ID` 环境变量未配置，回到上方「首次使用配置」流程引导用户完成配置。

### 情况 2：提醒其他人（用户提供了手机号或邮箱）

用户说「提醒 13912345678 的张三」「给 zhangsan@company.com 打个电话」等**包含手机号或邮箱**的情况：

> **注意：** 对方必须满足以下条件才能被提醒：
> 1. 对方已注册飞书账号（手机号/邮箱已关联飞书）
> 2. 对方与你在同一个飞书组织（租户）内
> 3. 对方已被添加到应用的可用范围中
>
> 如果 lookup 查不到用户，请提醒用户确认以上条件。

**第一步：用 lookup 查找对方的 open_id**

```bash
# 手机号不需要用户手动加 +86，脚本会自动补全
python3 {baseDir}/scripts/feishu_meeting.py lookup --phone "13912345678"
```

**第二步：用查到的 open_id 发起提醒**

```bash
python3 {baseDir}/scripts/feishu_meeting.py notify --message "小龙虾提醒你：xxx" --user-id "查到的open_id" --phone-call
```

### 手机号自动补全

用户提供的手机号**不需要加 +86 前缀**，脚本会自动处理：
- `13800138000` → 自动补全为 `+8613800138000`
- `8613800138000` → 自动补全为 `+8613800138000`
- `+8613800138000` → 保持不变

### 判断流程总结

1. 用户没有提到其他人 → 使用默认 `FEISHU_USER_OPEN_ID`
2. 用户提到了手机号或邮箱 → 先 `lookup` 查 open_id，再用 `--user-id` 指定
3. `FEISHU_USER_OPEN_ID` 未配置且未提供手机号 → 提示用户先配置

## 快速开始

```bash
# 发送加急消息（应用内加急）
python3 {baseDir}/scripts/feishu_meeting.py notify --message "小龙虾提醒你：该干活了"

# 电话加急（真正打电话到手机！）
python3 {baseDir}/scripts/feishu_meeting.py notify --message "紧急！线上故障" --phone-call

# 提醒其他人（先查 open_id，再提醒）
python3 {baseDir}/scripts/feishu_meeting.py lookup --phone "13912345678"
python3 {baseDir}/scripts/feishu_meeting.py notify --message "小龙虾提醒你：xxx" --user-id "查到的open_id" --phone-call
```

## 命令说明

### 1. `notify` — 发送加急消息（推荐）

发送一条加急文本消息，支持应用内加急和电话加急。

```bash
# 应用内加急（默认）
python3 {baseDir}/scripts/feishu_meeting.py notify --message "你的任务快到截止日期了"

# 电话加急（真正打电话到手机！）
python3 {baseDir}/scripts/feishu_meeting.py notify --message "紧急！" --phone-call
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--message` / `-m` | 消息内容（必填） | - |
| `--user-id` / `-u` | 用户 open_id | 从 `FEISHU_USER_OPEN_ID` 读取 |
| `--phone-call` | 使用电话加急（拨打手机），不加则默认应用内加急 | 默认不加 |

### 2. `lookup` — 查找用户 open_id

```bash
python3 {baseDir}/scripts/feishu_meeting.py lookup --email "user@company.com"
python3 {baseDir}/scripts/feishu_meeting.py lookup --phone "+8613800138000"
```

## 使用场景

| 场景 | 推荐命令 | 说明 |
|------|---------|------|
| 重要任务到期 | `notify` | 发送加急消息提醒 |
| 紧急消息通知 | `notify` | 应用内加急推送 |
| 需要电话提醒 | `notify --phone-call` | 直接打电话到手机 |
| 查找其他用户 | `lookup` | 通过手机号/邮箱查找 open_id |

## 使用示例

### 紧急任务提醒
```bash
python3 {baseDir}/scripts/feishu_meeting.py notify --message "小龙虾提醒你：15分钟后有客户会议"
```

### 电话加急提醒
```bash
python3 {baseDir}/scripts/feishu_meeting.py notify --message "小龙虾提醒你：紧急线上故障" --phone-call
```

### 简单消息提醒
```bash
python3 {baseDir}/scripts/feishu_meeting.py notify --message "数据分析报告已完成，请查收"
```

## 使用注意

1. **不要频繁加急** — 应用内加急是强提醒，每位用户最多 200 条未读加急
2. **消息要明确** — 让用户一眼看到提醒原因，建议格式: `小龙虾提醒你：具体事项`
3. **优先普通消息** — 非紧急事项用普通飞书消息，不要动不动就加急
4. **电话加急谨慎用** — 电话加急会消耗企业配额，确实紧急时再使用

## 提醒结果反馈

执行成功后，脚本会输出详细信息。**你必须将以下关键信息反馈给用户：**

1. **提醒状态**：消息是否发送成功、加急是否生效
2. **加急方式**：应用内加急还是电话加急

示例反馈格式：

```
已向你发送飞书紧急提醒：
- 消息内容：小龙虾提醒你：该干活了
- 消息发送：✅ 已发送
- 加急状态：✅ 已加急推送
```

如果失败，也要如实反馈，例如：

```
提醒发送失败：
- 消息发送：❌ 失败（缺少 im:message 权限）
- 建议：请在飞书开放平台开通 im:message 权限
```

如果脚本输出了权限错误提示（如 `-> 应用未启用机器人能力`），也要将提示信息转告用户。

## 所需飞书权限

### 权限列表

| 权限 | 说明 | 用途 | 必需 |
|------|------|------|------|
| `im:message` | 机器人发送消息 | notify 命令 | 是 |
| `im:message.urgent:phone` | 电话加急 | `--phone-call` 时使用（消耗企业配额） | 是 |
| `contact:user.id:readonly` | 通过邮箱/手机号查找用户 | lookup 命令 | 是 |

### 权限开通步骤

1. 打开 [飞书开放平台](https://open.feishu.cn/app)，进入你的应用
2. 左侧菜单点击 **「权限管理」**
3. 搜索上述权限名称（如 `im:message`），点击 **「开通」**
4. 全部权限开通后，进入 **「版本管理与发布」** 创建新版本并发布

### 机器人能力（必需）

发送消息功能要求应用具有**机器人能力**：

1. 进入应用详情，左侧菜单点击 **「应用能力」**
2. 找到 **「机器人」** 能力，点击 **「添加」**
3. 保存后重新发布应用

### 用户可用范围（必需）

被提醒的用户必须在应用的**可用范围**内：

1. 进入应用详情，左侧菜单点击 **「版本管理与发布」**
2. 找到 **「可用范围」**，将需要提醒的用户或部门添加进去
3. 发布新版本生效

## 常见错误排查

| 错误现象 | 原因 | 解决方法 |
|---------|------|---------|
| 消息发送失败 (230006) | 应用未启用机器人能力 | 应用详情 → 应用能力 → 添加「机器人」 |
| 消息发送失败 (230013) | 用户不在可用范围 | 版本管理 → 可用范围 → 添加用户 |
| 消息发送失败 (230002) | 机器人不在会话中 | 让用户在飞书中搜索并打开该机器人 |
| 加急失败 (230027) | 缺少加急权限 | 权限管理 → 开通 `im:message.urgent:phone` |
| 加急失败 (230023) | 用户未读加急超 200 条 | 让用户先处理部分加急消息 |
| 加急失败 (230024) | 电话加急配额用完 | 联系企业管理员充值或等待恢复 |
| 加急失败 (230052) | 群聊限制了加急 | 检查群聊加急权限设置 |
| 认证失败 | App ID 或 Secret 错误 | 检查环境变量 `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET` |

## 外部接口说明

本技能会向以下地址发送请求：

| 接口 | 地址 | 发送的数据 |
|------|------|-----------|
| 飞书认证 | `https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal` | App ID、App Secret |
| 飞书消息 | `https://open.feishu.cn/open-apis/im/v1/messages` | 消息内容、用户 ID |
| 飞书加急 | `https://open.feishu.cn/open-apis/im/v1/messages/{id}/urgent_app` 或 `urgent_phone` | 用户 ID |
| 飞书通讯录 | `https://open.feishu.cn/open-apis/contact/v3/users/batch_get_id` | 邮箱或手机号（仅 lookup） |

除上述接口外，不会向任何其他地址发送数据。
