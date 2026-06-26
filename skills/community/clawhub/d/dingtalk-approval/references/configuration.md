# 钉钉审批插件配置指南

## 📋 配置步骤

### 步骤 1：创建钉钉应用

1. 登录 [钉钉开放平台](https://open.dingtalk.com/)
2. 进入"应用开发" → "企业内部开发"
3. 点击"创建应用"
4. 填写应用名称和图标
5. 选择应用类型（建议选择"H5 微应用"）

### 步骤 2：获取凭证

1. 在应用管理页面，点击"凭证与基础信息"
2. 记录以下信息：
   - **AppKey**：应用的唯一标识
   - **AppSecret**：应用的密钥（请妥善保管）

### 步骤 3：配置权限

1. 在应用管理页面，点击"权限管理"
2. 添加以下权限：
   - **OA 审批**：`process` 相关权限
   - **通讯录**：`contact` 相关权限（用于获取用户信息）
3. 提交审核（部分权限需要审核）

### 步骤 4：获取用户 ID

**方法 1：通过钉钉管理后台**
1. 进入钉钉管理后台（oa.dingtalk.com）
2. 通讯录 → 找到对应用户
3. 点击用户详情，查看"用户 ID"

**方法 2：通过 API 获取**
```bash
curl "https://oapi.dingtalk.com/user/get?access_token=ACCESS_TOKEN&userid=USER_ID"
```

**方法 3：使用默认值**
- 如果是管理员，可以使用 `admin` 或管理员的用户 ID

### 步骤 5：配置 OpenClaw

在 `openclaw.json` 中添加配置：

```json
{
  "plugins": {
    "entries": {
      "dingtalk-approval": {
        "config": {
          "dingtalkUserId": "your-user-id",
          "appKey": "your-app-key",
          "appSecret": "your-app-secret"
        }
      }
    }
  }
}
```

### 步骤 6：验证配置

1. 重启 OpenClaw
2. 询问："我有什么待办审批吗？"
3. 如果返回待办列表，说明配置成功

---

## 🔧 配置文件位置

### macOS / Linux
```
~/.openclaw/config/openclaw.json
```

### Windows
```
%USERPROFILE%\.openclaw\config\openclaw.json
```

---

## ⚠️ 注意事项

### 安全建议

1. **不要将 appSecret 提交到代码仓库**
   - 使用环境变量或加密存储
   - 定期更换 appSecret

2. **权限最小化原则**
   - 只申请必要的权限
   - 定期审查应用权限

3. **访问令牌管理**
   - token 有效期 2 小时
   - 实现自动刷新机制
   - 不要在客户端暴露 token

### 常见问题

#### Q1: 配置后仍然提示"配置不完整"

**原因**：配置文件路径错误或格式不正确

**解决**：
1. 检查 openclaw.json 文件路径
2. 验证 JSON 格式是否正确（使用 JSON 验证工具）
3. 确保配置在 `plugins.entries.dingtalk-approval.config` 路径下
4. 重启 OpenClaw

#### Q2: 提示"权限不足"

**原因**：应用未开通对应 API 权限

**解决**：
1. 登录钉钉开放平台
2. 进入应用管理 → 权限管理
3. 添加"OA 审批"相关权限
4. 提交审核（如需要）
5. 等待审核通过后重试

#### Q3: 获取用户 ID 失败

**原因**：用户 ID 格式错误或用户不存在

**解决**：
1. 确认用户 ID 是钉钉系统中的真实 ID
2. 联系企业管理员获取正确的用户 ID
3. 检查用户是否在应用可见范围内

#### Q4: token 获取失败

**原因**：appKey 或 appSecret 错误

**解决**：
1. 重新从钉钉开放平台复制凭证
2. 注意不要复制多余的空格
3. 确认应用状态正常（未停用）

---

## 📝 配置示例

### 完整配置示例

```json
{
  "gateway": {
    "port": 8080
  },
  "plugins": {
    "entries": {
      "dingtalk-approval": {
        "config": {
          "dingtalkUserId": "manager123",
          "appKey": "ding456abc",
          "appSecret": "secret789xyz"
        }
      },
      "feishu-openclaw-plugin": {
        "config": {
          "appId": "cli_a1b2c3d4",
          "appSecret": "secret123"
        }
      }
    }
  },
  "models": {
    "default": "bailian/qwen3.5-plus"
  }
}
```

### 使用环境变量（推荐）

```json
{
  "plugins": {
    "entries": {
      "dingtalk-approval": {
        "config": {
          "dingtalkUserId": "${DINGTALK_USER_ID}",
          "appKey": "${DINGTALK_APP_KEY}",
          "appSecret": "${DINGTALK_APP_SECRET}"
        }
      }
    }
  }
}
```

然后在启动 OpenClaw 前设置环境变量：

```bash
export DINGTALK_USER_ID="manager123"
export DINGTALK_APP_KEY="ding456abc"
export DINGTALK_APP_SECRET="secret789xyz"
openclaw start
```

---

## 🔗 相关资源

- [钉钉开放平台文档](https://open.dingtalk.com/document/)
- [OpenClaw 插件配置指南](https://docs.openclaw.ai/plugins)
- [企业内部应用开发指南](https://open.dingtalk.com/document/orgapp-server/enterprise-application-development)
