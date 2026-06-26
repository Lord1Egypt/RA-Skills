---
id: feishu-multi-agent-manager
owner_id: rfdiosuao
name: 飞书多 Agent 配置助手
description: 交互式引导配置多 Agent 系统，支持批量创建、凭证验证、角色模板、自动备份
version: 2.0.4
icon: "\U0001F916"
author: rfdiosuao
metadata:
  clawdbot:
    emoji: "\U0001F916"
    requires:
      bins: []
---

# 飞书多 Agent 配置助手 🤖

> 交互式引导配置多 Agent 系统，支持批量创建、凭证验证、角色模板

## ✨ 功能特性

### 1. 交互式配置向导
- 像聊天一样完成配置
- 询问创建几个 Agent（1-10）
- 提供预设角色推荐

### 2. 批量创建支持
- 一次性创建多个 Agent
- 自动验证每个凭证
- 详细的成功/失败报告

### 3. 飞书 Bot 创建教程
- 7 步详细教程
- 包含检查清单
- 常见问题解答

### 4. 预设角色模板
- 6 个经典角色（main/dev/content/ops/law/finance）
- 每个角色包含完整人设文件
- 支持完全自定义

### 5. 凭证验证
- 自动验证 AppID 格式
- 自动验证 AppSecret 长度
- 友好的错误提示

### 6. 工作区隔离
- 每个 Agent 独立 workspace
- 记忆文件独立
- 会话存储独立

## 🚀 使用方式

### 启动配置向导

```typescript
await main(ctx, { action: 'start_wizard' });
```

### 选择 Agent 数量

```typescript
await main(ctx, { action: 'select_count', count: '6' });
```

### 查看飞书教程

```typescript
await main(ctx, { 
  action: 'show_tutorial',
  step: '1',
  agentName: '大总管'
});
```

### 批量创建 Agent

```typescript
await main(ctx, {
  action: 'batch_create',
  agents: [
    { agentId: 'main', agentName: '大总管', appId: 'cli_xxx', appSecret: 'xxx', isDefault: true },
    { agentId: 'dev', agentName: '开发助理', appId: 'cli_xxx', appSecret: 'xxx' },
    { agentId: 'content', agentName: '内容助理', appId: 'cli_xxx', appSecret: 'xxx' }
  ]
});
```

### 查看配置状态

```typescript
await main(ctx, { action: 'show_status' });
```

## 📋 配置流程

1. **启动向导** - 回复「开始配置」
2. **选择数量** - 告诉 Bot 创建几个 Agent
3. **选择模式** - 预设/自定义/全新
4. **创建飞书应用** - 按照教程创建每个 Bot
5. **验证凭证** - 自动验证 AppID/AppSecret
6. **批量创建** - 一次性创建所有 Agent
7. **重启生效** - 重启 OpenClaw

## 🎯 预设角色

| 角色 | 职责 | 表情 |
|------|------|------|
| main | 大总管 - 统筹全局 | 🎯 |
| dev | 开发助理 - 技术架构 | 🧑‍💻 |
| content | 内容助理 - 文案创作 | ✍️ |
| ops | 运营助理 - 用户增长 | 📈 |
| law | 法务助理 - 合同审核 | 📜 |
| finance | 财务助理 - 账目管理 | 💰 |

## 📚 完整文档

查看 [GitHub README](https://github.com/rfdiosuao/openclaw-skills/blob/main/feishu-multi-agent-manager/README.md)

## 🔗 相关链接

- [GitHub 仓库](https://github.com/rfdiosuao/openclaw-skills)
- [飞书云文档教程](https://www.feishu.cn/docx/PYlXdsZoEoPPDbxyBRWc9HpRnIe)
- [OpenClaw 官方文档](https://docs.openclaw.ai)

---

**版本：** 2.0.4  
**作者：** rfdiosuao  
**许可证：** MIT

## 📝 更新日志

### v2.0.4 (2026-04-05)
- ✅ 兼容飞书官方插件 2026.4.1
- ✅ 适配 OpenClaw 2026.3.31+
- ✅ **新增配置前自动备份** - 修改 openclaw.json 前自动创建备份文件
- ✅ **修复路径硬编码** - 动态获取用户主目录，支持不同系统用户
- ✅ 支持话题模式独立上下文配置
- ✅ 支持流式输出配置

### v2.0.3 (2026-03-26)
- ✅ 兼容飞书官方插件 2026.3.25
- ✅ 适配 OpenClaw 2026.3.22+

### v2.0.2 (2026-03-19)
- ✅ 动态路径获取
- ✅ 配置前自动备份
- ✅ 自动复制认证配置

### v2.0.1 (2026-03-17)
- 🐛 修复 accounts 配置格式问题
