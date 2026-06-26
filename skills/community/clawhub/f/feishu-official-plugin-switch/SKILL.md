---
id: feishu-official-plugin-switch
owner_id: rfdiosuao
name: 飞书官方插件一键转换
description: 3 分钟从社区版升级到官方版，开启流式输出、用户身份、50+ 官方工具
version: 3.0.0
icon: "\U0001F99E"
author: rfdiosuao
metadata:
  clawdbot:
    emoji: "\U0001F99E"
    requires:
      bins: ["openclaw"]
---

# 飞书官方插件一键转换 🦞

> 3 分钟搞定！从 OpenClaw 社区版升级到飞书官方版，开启流式输出、用户身份、50+ 官方工具

## ✨ 功能特性

### 1. 一键自动转换
- 自动检查 OpenClaw 版本（≥2026.2.26 Linux/MacOS，≥2026.3.2 Windows）
- 自动安装官方插件（@larksuite/openclaw-lark-tools）
- 自动配置流式输出（打字机效果）
- 自动切换插件（禁用社区版，启用官方版）
- 自动重启 OpenClaw Gateway
- 自动验证配置生效

### 2. 智能诊断
- 版本检测
- 插件状态检查
- 配置验证
- 问题自动修复建议

### 3. 详细状态报告
- 每个步骤的执行结果
- 成功/失败状态清晰展示
- 问题诊断建议

### 4. 安全提示
- 转换前风险提示
- 权限配置指引
- 数据隐私保护建议

### 5. 新功能介绍
- 电子表格读写
- 表情识别
- 多账号支持
- 话题群独立上下文

## 🚀 使用方式

### 启动转换

在飞书中对机器人说以下任意一句话：
- 「切换到官方飞书插件」
- 「安装官方插件」
- 「开启流式输出」
- 「switch to official plugin」

### 自动执行流程

```typescript
await main(ctx, { action: 'start_switch' });
```

### 检查版本

```typescript
await main(ctx, { action: 'check_version' });
```

### 安装官方插件

```typescript
await main(ctx, { action: 'install_plugin' });
```

### 配置流式输出

```typescript
await main(ctx, { 
  action: 'configure_streaming',
  options: {
    streaming: true,
    footer_status: true,
    footer_elapsed: true
  }
});
```

### 切换插件

```typescript
await main(ctx, {
  action: 'switch_plugin',
  disable: 'feishu',
  enable: 'feishu-openclaw-plugin'
});
```

### 重启 OpenClaw

```typescript
await main(ctx, { action: 'restart_openclaw' });
```

### 验证配置

```typescript
await main(ctx, { action: 'verify_config' });
```

## 📋 转换流程

1. **版本检查** - 检查 OpenClaw 版本是否满足要求
2. **插件安装** - 安装官方插件 (@larksuite/openclaw-lark-tools)
3. **流式配置** - 开启流式输出、状态显示、耗时显示
4. **插件切换** - 禁用社区版，启用官方版
5. **重启服务** - 重启 OpenClaw Gateway
6. **验证配置** - 检查插件状态和流式配置
7. **完成报告** - 展示转换结果和新功能介绍

## ⚠️ 版本要求

- **OpenClaw:** ≥ 2026.2.26 (Linux/MacOS) / ≥ 2026.3.2 (Windows)
- **官方插件:** ≥ 2026.3.15
- **Node.js:** ≥ 18.0.0

## 🔐 权限配置

确保飞书机器人已申请以下核心权限：

**应用身份权限：**
```json
{
  "scopes": {
    "tenant": [
      "contact:contact.base:readonly",
      "docx:document:readonly",
      "im:chat:read",
      "im:chat:update",
      "im:message.group_at_msg:readonly",
      "im:message.p2p_msg:readonly",
      "im:message:send_as_bot",
      "cardkit:card:write",
      "cardkit:card:read"
    ]
  }
}
```

**用户身份权限（批量授权时用）：**
```json
{
  "scopes": {
    "user": [
      "base:record:*",
      "docs:document:*",
      "calendar:calendar.event:*",
      "task:task:*",
      "im:message",
      "drive:file:*"
    ]
  }
}
```

## 🎉 转换后的新能力

| 能力 | 社区版 | 官方版 |
|------|--------|--------|
| 身份 | 机器人 | 用户身份 ✅ |
| 文档权限 | 只读 | 读写 ✅ |
| 消息历史 | ❌ | 完整读取 ✅ |
| 流式输出 | ❌ | 打字机效果 ✅ |
| 表情识别 | ❌ | 支持 ✅ |
| 电子表格 | ❌ | 读写支持 ✅ |
| 工具数量 | 基础 | 50+ ✅ |
| 多账号 | ❌ | 支持 ✅ |
| 话题群 | ❌ | 独立上下文 ✅ |

## 📊 诊断命令

转换完成后，在飞书中发送以下命令验证：

- `/feishu start` - 确认安装成功
- `/feishu doctor` - 检查配置
- `/feishu auth` - 批量授权

**命令行诊断：**
```bash
npx @larksuite/openclaw-lark-tools doctor
npx @larksuite/openclaw-lark-tools doctor --fix
npx @larksuite/openclaw-lark-tools info
```

## 🐛 常见问题

### Q1: 插件安装失败？
```bash
# 使用 sudo
sudo npx -y @larksuite/openclaw-lark-tools install

# 使用国内镜像
export NPM_CONFIG_REGISTRY=https://registry.npmmirror.com
```

### Q2: 流式没效果？
```bash
# 检查插件状态
openclaw plugins list | grep feishu

# 期望：feishu-openclaw-plugin loaded, feishu disabled
```

### Q3: Coze 上安装失败？
```bash
export NPM_CONFIG_REGISTRY=https://registry.npmmirror.com
npx -y @larksuite/openclaw-lark-tools install
```

### Q4: 需要 OAuth 授权吗？
**可以跳过！** 安装后不授权也能用基础功能（流式输出、对话），只是无法读取消息历史和以你的身份操作。

## 📚 完整文档

查看 [GitHub README](https://github.com/rfdiosuao/openclaw-skills/blob/main/feishu-official-plugin-switch/README.md)

## 🔗 相关链接

- [官方插件使用指南](https://bytedance.larkoffice.com/docx/MFK7dDFLFoVlOGxWCv5cTXKmnMh)
- [GitHub 仓库](https://github.com/rfdiosuao/openclaw-skills)
- [OpenClaw 官方文档](https://docs.openclaw.ai)

---

**版本：** 3.0.0  
**最后更新：** 2026-03-18  
**作者：** rfdiosuao  
**许可证：** MIT
