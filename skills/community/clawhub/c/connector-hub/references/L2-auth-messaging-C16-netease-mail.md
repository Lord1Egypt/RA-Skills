# C16 - 网易邮箱

## 基本信息

| 字段 | 值 |
|------|-----|
| ID | C16 |
| 连接器名 | netease-mail |
| 显示名 | 网易邮箱 |
| 层级 | L2 鉴权便利型 |
| 可替代 | ✅ 可替代（Skill） |
| 分类 | 消息/通讯 |
| 替代难度 | 简单 |

## 连接器能力

| 能力 | 说明 |
|------|------|
| 发送邮件 | 文本/HTML 邮件 |
| 附件 | 发送附件 |
| 批量发送 | 批量邮件 |

## Skill 替代方案

### 脚本位置

使用 connector-hub 技能中的脚本：

```
scripts/
└── L2-auth-messaging-C16-netease-mail-send-email.py  # 发送邮件
```

### 环境变量配置

```bash
export NETEASE_MAIL_ADDRESS="your_email@163.com"
export NETEASE_MAIL_AUTH_CODE="your_auth_code"
```

### 鉴权方式

**API Key / SMTP**：
1. 在平台开放平台注册账号
2. 获取 API Key 或 SMTP 授权码
3. 请求时携带凭证

**环境变量配置**：
```bash
export API_KEY="your_api_key"
```

### 核心脚本示例

使用 connector-hub 技能中的脚本：

```bash
python scripts/$(basename "$f" .md).py [参数]
```

### 迁移成本

| 项目 | 说明 |
|------|------|
| API 变更 | 改 API 域名即可 |
| 凭证更新 | 重新申请 API Key |
| 工作流 | 无需修改 |

### 对比

| 维度 | 连接器 | Skill |
|------|--------|-------|
| 鉴权 | 平台托管 | 用户自管 |
| 功能 | 固定 | 可自定义 |
| 迁移 | 重配连接器 | 改 API 地址 |
