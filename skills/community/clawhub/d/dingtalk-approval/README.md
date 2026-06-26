# DingTalk Approval Plugin

钉钉 OA 审批处理插件 - OpenClaw Skill

## 📖 功能特性

- ✅ 查询待办审批任务列表
- ✅ 查看审批单详情
- ✅ 执行审批操作（同意/拒绝）
- ✅ 查询假期余额
- ✅ 支持审批意见备注
- ✅ 自动管理访问令牌
- ✅ 完善的错误处理

## 🚀 快速开始

### 1. 安装插件

```bash
cd ~/.openclaw/extensions/dingtalk-approval
npm install
```

### 2. 配置凭证

在 `openclaw.json` 中添加：

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

### 3. 使用示例

```
用户：我有什么待办审批吗？
助手：您有 3 个待办：
      1. 请假申请 - 张三 (task_12345)
      2. 报销审批 - 李四 (task_67890)
      3. 合同审批 - 王五 (task_abcde)

用户：同意第一个
助手：✅ 已同意张三的请假申请
```

## 📚 文档

- [SKILL.md](SKILL.md) - 技能使用说明
- [references/api-docs.md](references/api-docs.md) - API 接口文档
- [references/configuration.md](references/configuration.md) - 详细配置指南

## ⚙️ 配置项

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| dingtalkUserId | string | ✅ | 钉钉用户 ID |
| appKey | string | ✅ | 钉钉应用 AppKey |
| appSecret | string | ✅ | 钉钉应用 AppSecret |

## 🧰 工具列表

| 工具名 | 说明 |
|------|------|
| get_pending_tasks | 查询当前用户的待办审批任务 |
| get_task_details | 查询审批单详情 |
| execute_approval_task | 执行同意或拒绝操作 |
| get_vacation_balance | 查询假期余额 |

## 🛠️ 开发

### 目录结构

```
dingtalk-approval/
├── index.js              # 插件主程序
├── SKILL.md             # 技能说明（ClawHub 规范）
├── openclaw.plugin.json # 插件配置
├── package.json         # NPM 配置
├── README.md            # 本文件
├── _meta.json           # ClawHub 元数据
├── .clawhub/            # ClawHub 配置目录
└── references/          # 参考文档
    ├── api-docs.md      # API 接口文档
    └── configuration.md # 配置指南
```

### 本地测试

```bash
# 启动 OpenClaw
openclaw start

# 在对话中测试
"我有什么待办审批吗？"
```

## 📦 发布到 ClawHub

```bash
# 1. 更新版本号（package.json、openclaw.plugin.json、manifest、_meta.json、origin.json）
# 2. 登录 ClawHub
clawhub whoami

# 3. 发布到 ClawHub
clawhub publish ~/.openclaw/extensions/dingtalk-approval --version 2.3.2 --changelog "..."
```

> 注：如果本机 `clawhub publish` 遇到 `acceptLicenseTerms: invalid value`，说明本地 CLI 版本与服务端接口不匹配，需要先升级 ClawHub CLI，或改走网页发布。

## ⚠️ 注意事项

1. **权限要求**：需要在钉钉开放平台开通 OA 审批权限；假期余额查询还需要 `qyapi_holiday_readonly`
2. **Token 管理**：访问令牌有效期 2 小时，插件会自动刷新
3. **用户 ID**：确保配置的用户 ID 有审批权限
4. **错误处理**：查看 [references/api-docs.md](references/api-docs.md) 了解错误码

## 🔗 相关链接

- [ClawHub](https://clawhub.ai)
- [插件页面](https://clawhub.ai/whauff/dingtalk-approval)
- [OpenClaw 文档](https://docs.openclaw.ai)
- [钉钉开放平台](https://open.dingtalk.com/)
- [OA 审批 API 文档](https://open.dingtalk.com/document/orgapp-server/query-the-tasks-to-be-processed-by-the-user)

## 📄 许可证

MIT License

## 👤 作者

Yang
