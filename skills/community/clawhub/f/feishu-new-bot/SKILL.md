---
name: feishu-new-bot
description: 飞书新机器人创建工作流。当大哥要求创建新的飞书bot、建立新的飞书机器人、或者新增bot时使用此skill。触发场景包括：大哥说"创建一个新的飞书bot"、"新建一个机器人"、"新增bot"、"帮我创建一个飞书机器人"。
---

# feishu-new-bot

飞书新机器人创建完整工作流。

## 前提条件

- 大哥已有飞书开放平台账号
- 大哥愿意亲自创建应用（这一步必须大哥操作，AI无法代劳）

## 完整流程

### 第一步：大哥创建应用

告诉大哥访问以下链接创建企业自建应用（机器人）：

```
https://open.feishu.cn/page/openclaw?form=multiAgent
```

**命名规则**（必须遵守）：
- 不能有空格
- 不能有特殊符号
- 只能使用字母、数字、下划线

### 第二步：大哥提供凭证

大哥把以下信息发给我：
- APP ID
- APP SECRET

### 第三步：创建工作目录

在 `/Users/jiaclaw/.openclaw/` 下建立新bot的workspace根目录，**目录名 = bot名字**（与APP名字一致）。

### 第四步：修改openclaw.json配置

在gateway配置中添加新bot信息，需要包含：
- APP ID
- APP SECRET
- workspace路径（刚创建的目录）

**重要：修改openclaw.json前必须先征得大哥同意，不能自行修改。**

### 第五步：重启Gateway

配置修改后需要重启Gateway使配置生效。

### 第六步：同步工作文件

从大哥的Thanos workspace同步以下文件到新bot的workspace：

| 文件 | 处理方式 |
|------|----------|
| AGENTS.md | 直接同步 |
| TOOLS.md | 直接同步 |
| USER.md | 直接同步 |
| MEMORY.md | 改造后同步（清理Thanos相关内容） |
| HEARTBEAT.md | 不同步（新bot自己创建） |

### 第七步：建立身份文件

为新bot创建 `SOUL.md` 和 `IDENTITY.md`：
- 根据新bot的角色和职责确定性格定位
- 设置合适的Emoji和Avatar描述
- 写入大哥制定的行为准则（最高执行准则）

### 第八步：验证连接

1. 获取新bot的sessionKey
2. 通过 `sessions_send` 发送测试消息确认能正常调用
3. 确认回复正常即完成

## 快速检查清单

- [ ] 大哥已创建应用并提供APP ID、APP SECRET
- [ ] 工作目录已创建
- [ ] openclaw.json已修改并重启Gateway
- [ ] 工作文件已同步
- [ ] SOUL.md和IDENTITY.md已创建
- [ ] 连接验证通过

## 注意事项

1. **openclaw.json修改必须先征得大哥同意**
2. HEARTBEAT.md由新bot自己创建，不要从Thanos复制
3. 新bot的SOUL.md和IDENTITY.md要根据其职责定制，不是简单复制
4. 如果大哥忘记创建应用，引导他去开放平台创建
