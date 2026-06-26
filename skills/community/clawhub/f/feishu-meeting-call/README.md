# 📞 飞书紧急提醒技能

通过飞书发送加急消息，实现紧急提醒。支持**电话加急**（真正打电话到手机）和**应用内加急**（飞书 App 强推送）。

## 功能特性

- **电话加急** — 直接拨打手机电话，适合紧急场景
- **应用内加急** — 飞书 App 强推送，免费无限制
- **用户查找** — 通过邮箱或手机号查找用户 open_id
- **手机号自动补全** — 自动加 +86 前缀，无需手动输入
- **跨平台配置管理** — `save-config` 命令替代 sed，macOS/Linux 通用，容器重建后不丢失
- **纯标准库** — 无需安装第三方依赖，Python 3.6+ 即可

## 安装

**OpenClaw 用户**（推荐）：
```bash
# 必须 clone 到 skills/ 目录，否则 clawhub list 找不到
git clone https://github.com/CY-CHENYUE/feishu-meeting-call.git ~/.openclaw/workspace/skills/feishu-meeting-call
```

**本地使用**：
```bash
git clone https://github.com/CY-CHENYUE/feishu-meeting-call.git
cd feishu-meeting-call
```

## 配置指南

### 第一步：创建飞书应用

1. 打开 [飞书开放平台](https://open.feishu.cn/app)，点击 **「创建企业自建应用」**
2. 填写应用名称和描述，创建应用
3. 记录应用的 **App ID** 和 **App Secret**（凭证与基础信息页面）

### 第二步：开通权限

进入应用详情，左侧菜单点击 **「权限管理」**，搜索并开通以下权限：

| 权限 | 说明 | 必需 |
|------|------|------|
| `im:message` | 机器人发送消息 | ✅ |
| `im:message.urgent:phone` | 电话加急（消耗企业配额） | ✅ |
| `contact:user.id:readonly` | 通过邮箱/手机号查找用户 | ✅ |

### 第三步：添加机器人能力

1. 进入应用详情，左侧菜单点击 **「应用能力」**
2. 找到 **「机器人」** 能力，点击 **「添加」**
3. 保存

### 第四步：设置可用范围并发布

1. 左侧菜单点击 **「版本管理与发布」**
2. 在 **「可用范围」** 中添加需要被提醒的用户或部门
3. 点击 **「创建版本」** 并发布

### 第五步：保存凭证

```bash
# 保存 App ID 和 App Secret
python3 scripts/feishu_meeting.py save-config --app-id "你的AppID" --app-secret "你的AppSecret"
```

配置默认保存到技能根目录下的 `.feishu.env`，容器重建后不会丢失。也可以用 `--path` 指定其他路径。

### 第六步：获取用户 open_id

```bash
# 通过手机号查找（自动补 +86）
python3 scripts/feishu_meeting.py lookup --phone "13800138000"

# 通过邮箱查找
python3 scripts/feishu_meeting.py lookup --email "user@company.com"
```

将获取到的 `open_id` 保存到配置：

```bash
python3 scripts/feishu_meeting.py save-config --user-id "查到的open_id"
```

## 使用示例

### 发送加急消息（应用内加急）

```bash
python3 scripts/feishu_meeting.py notify --message "小龙虾提醒你：该干活了"
```

### 电话加急（真正打电话到手机！）

```bash
python3 scripts/feishu_meeting.py notify --message "小龙虾提醒你：紧急线上故障" --phone-call
```

### 提醒其他人

```bash
# 先查找对方的 open_id
python3 scripts/feishu_meeting.py lookup --phone "13912345678"

# 再用查到的 open_id 发起提醒
python3 scripts/feishu_meeting.py notify --message "小龙虾提醒你：xxx" --user-id "查到的open_id" --phone-call
```

## 完整参数列表

### notify 命令

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--message` / `-m` | 消息内容（必填） | - |
| `--user-id` / `-u` | 用户 open_id | 从环境变量读取 |
| `--phone-call` | 使用电话加急 | 默认不加（应用内加急） |

### lookup 命令

| 参数 | 说明 |
|------|------|
| `--email` / `-e` | 用户邮箱 |
| `--phone` / `-p` | 用户手机号（自动补 +86，如 13800138000） |

### save-config 命令

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--app-id` | 飞书应用 App ID | - |
| `--app-secret` | 飞书应用 App Secret | - |
| `--user-id` | 用户 open_id | - |
| `--path` | 配置文件保存路径 | 技能根目录/.feishu.env |

## 常见错误排查

### 消息发送相关

| 错误码 | 原因 | 解决方法 |
|--------|------|---------|
| 230006 | 应用未启用机器人能力 | 应用详情 → 应用能力 → 添加「机器人」能力 |
| 230013 | 用户不在应用可用范围 | 版本管理与发布 → 可用范围 → 添加用户 |
| 230002 | 机器人不在会话中 | 让用户在飞书中搜索并打开该机器人对话 |

### 加急相关

| 错误码 | 原因 | 解决方法 |
|--------|------|---------|
| 230027 | 缺少加急权限 | 权限管理 → 开通 `im:message.urgent:phone` |
| 230023 | 用户未读加急超 200 条 | 让用户先处理部分加急消息 |
| 230024 | 电话加急配额用完 | 联系企业管理员充值或等待恢复 |
| 230052 | 群聊限制了加急 | 检查群聊加急权限设置 |

### 认证相关

| 错误现象 | 原因 | 解决方法 |
|---------|------|---------|
| 认证失败 | App ID 或 Secret 错误 | 检查环境变量 `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET` |
| Token 获取失败 | 应用未发布 | 在飞书开放平台创建版本并发布 |

## 技术说明

- **Python 3.6+** — 仅使用标准库，无需安装第三方依赖
- **自动重试** — 网络错误时自动重试（最多 2 次）
- **降级策略** — 电话加急失败时自动降级为应用内加急

## 外部接口说明

本技能会向以下地址发送请求：

| 接口 | 地址 | 发送的数据 |
|------|------|-----------|
| 飞书认证 | `https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal` | App ID、App Secret |
| 飞书消息 | `https://open.feishu.cn/open-apis/im/v1/messages` | 消息内容、用户 ID |
| 飞书加急 | `https://open.feishu.cn/open-apis/im/v1/messages/{id}/urgent_app` 或 `urgent_phone` | 用户 ID |
| 飞书通讯录 | `https://open.feishu.cn/open-apis/contact/v3/users/batch_get_id` | 邮箱或手机号（仅 lookup） |

除上述接口外，不会向任何其他地址发送数据。

## 许可证

MIT License

---

<div align="center">
  <h3>联系作者</h3>
  <p>扫码加微信，交流反馈</p>
  <img src="assets/wechat-qr.jpg" alt="WeChat QR Code" width="200">
</div>
