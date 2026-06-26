---
name: weaver-e10-api
description: 泛微 E10 系统 API 调用工具，支持流程创建、待办查询、审批提交、流程退回等操作。使用 OAuth2.0 认证，自动管理 token 刷新。
allowed-tools: Bash
---

# 泛微 E10 API 调用 Skill

## 功能列表

| 功能 | 命令 | 说明 |
|------|------|------|
| 获取 Token | `weaver-e10 auth` | 获取/刷新 access_token |
| 创建流程 | `weaver-e10 create` | 发起新的审批流程 |
| 查询待办 | `weaver-e10 todos` | 获取用户待办列表 |
| 提交审批 | `weaver-e10 approve` | 提交/同意流程 |
| 退回流程 | `weaver-e10 reject` | 退回审批流程 |
| 查询流程 | `weaver-e10 get` | 获取流程详情 |

## 环境变量配置

在 `/ollama/workspace/.env/weaver-e10.env` 中配置：

```bash
# 泛微 E10 API 配置
# ⚠️ 请替换为你自己的实际值，不要使用示例中的占位符
WEAVER_API_BASE=http://your-weaver-server:port
WEAVER_APP_KEY=your_app_key_here
WEAVER_APP_SECRET=your_app_secret_here
WEAVER_CORPID=your_corpid_here
```

### 🔒 安全警告

1. **凭证保管**：`.env/weaver-e10.env` 文件包含敏感凭证，请：
   - 不要提交到 Git 等版本控制系统
   - 设置文件权限：`chmod 600 .env/weaver-e10.env`
   - 不要通过聊天工具、邮件等方式明文传输

2. **Token 缓存**：Token 缓存在 `~/.weaver-e10/token.json`，请：
   - 确保家目录权限安全
   - 定期清理过期 token
   - 不要在共享主机上使用

3. **网络隔离**：建议在内部网络使用，避免暴露在公网

## 使用示例

### 1. 获取 Token（自动）
```bash
# 首次获取
weaver-e10 auth

# 输出
{
  "access_token": "xxx",
  "expires_in": 7200,
  "refresh_token": "xxx"
}
```

### 2. 创建流程
```bash
weaver-e10 create \
  --userid 731942425541656576 \
  --workflow-id 5955363498899145211 \
  --title "请假申请" \
  --form-data '{"dataDetails": [{"fieldId": "123", "content": "张三"}]}' \
  --next-flow
```

### 3. 查询待办
```bash
weaver-e10 todos --userid 731942425541656576 --page 1 --size 20
```

### 4. 提交审批
```bash
weaver-e10 approve \
  --userid 731942425541656576 \
  --request-id 848951654078865410 \
  --remark "同意"
```

### 5. 退回流程
```bash
weaver-e10 reject \
  --userid 731942425541656576 \
  --request-id 848951654078865410 \
  --reject-type 1 \
  --remark "资料不全，请补充"
```

## 认证流程

```
1. 调用 /oauth2/authorize 获取 code（10 分钟有效）
2. 调用 /oauth2/access_token 用 code 换 token（2 小时有效）
3. token 过期后自动用 refresh_token 刷新（24 小时有效）
4. refresh_token 过期后重新授权
```

## 错误码

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 40001 | token 无效或过期 |
| 40002 | 权限不足 |
| 40003 | 参数错误 |
| 50000 | 系统错误 |

## 注意事项

1. **Token 管理**：token 自动缓存到 `~/.weaver-e10/token.json`
2. **自动刷新**：token 过期前 5 分钟自动刷新
3. **表单数据**：formData 必须是合法 JSON
4. **人员 ID**：userid 必须是泛微系统中的用户 ID

## 文件结构

```
weaver-e10-api/
├── SKILL.md              # 本文档
├── _meta.json            # 元数据
├── scripts/
│   ├── weaver-e10.py     # 主程序
│   └── auth.py           # 认证模块
└── examples/
    ├── create_request.json
    └── approve_request.json
```
