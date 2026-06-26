# 🤖 飞书机器人配置助手

> 在飞书对话中直接配置新机器人，自动完成所有配置

**版本**: v1.0.0  
**作者**: OpenClaw 来合火  
**创建时间**: 2026-03-17

---

## ✨ 核心功能

- ✅ 在飞书对话中直接配置新机器人
- ✅ 自动解析配置信息
- ✅ 智能匹配 Agent 类型（7 种规则）
- ✅ 自动创建工作空间
- ✅ 自动更新 openclaw.json
- ✅ 自动重启 Gateway
- ✅ 返回配置报告

---

## 🚀 快速开始

### 安装

**Mac / Linux**:
```bash
cd ~/.openclaw/workspace-main/skills/
git clone https://github.com/jiebao360/feishu-bot-config-helper.git
cd feishu-bot-config-helper
bash install.sh
```

**Windows**:
```powershell
cd ~/.openclaw/workspace-main/skills/
git clone https://github.com/jiebao360/feishu-bot-config-helper.git
cd feishu-bot-config-helper
.\install.bat
```

---

## 📋 配置格式

### 标准格式

```
配置飞书机器人：机器人名称
飞书应用凭证：
App ID: cli_xxx
App Secret: xxx
创建技能：技能名称（可选）
```

### 示例 1: 配置笔记虾

```
配置飞书机器人：来合火 1 号第二大脑笔记虾
飞书应用凭证：
App ID: cli_a93cff63cc789cee
App Secret: DN8oxaxAV2h0pKqykSGWIenRSvIXkzl1
```

**自动匹配**:
- Agent ID: `notes`
- Agent 名称：`第二大脑笔记虾`
- 技能：`make-notes, web-search, file-reading`

---

### 示例 2: 配置工作助手

```
配置飞书机器人：工作助手
飞书应用凭证：
App ID: cli_xxx_work
App Secret: work_secret
创建技能：Content Agent
```

**自动匹配**:
- Agent ID: `work`
- Agent 名称：`工作助手`
- 技能：`make-create, content-optimization`

---

## 🎭 智能匹配规则

| 机器人名称包含 | Agent ID | Agent 名称 | 默认技能 |
|---------------|---------|-----------|---------|
| 笔记/笔记虾/第二大脑/知识 | notes | 第二大脑笔记虾 | make-notes, web-search, file-reading |
| 内容/创作/文章/通用 | generic_content | 通用内容创作虾 | make-create, content-optimization |
| 朋友圈/社交/媒体 | moment | 朋友圈创作虾 | make-moments |
| 视频/导演/脚本 | video | 电商视频导演虾 | video-script, storyboard |
| Seedance/提示词 | seedance | 电商 Seedance 导演虾 | seedance-director, prompt-engineering |
| 图片/设计/封面/素材 | image | 图片素材生成虾 | make-image, image-search, doubao-prompt |
| 工作/助手 | work | 工作助手 | all |

---

## ⚙️ 配置规范

严格遵循官方参考模板：

### 1. 每个飞书机器人对应一个独立 Agent

```json
{
  "id": "work",
  "name": "工作助手",
  "workspace": "~/.openclaw/workspace-work",
  "model": { "primary": "ark/doubao" },
  "skills": ["all"]
}
```

### 2. 在 `agents.list` 中定义 Agent

- `id`: 唯一标识
- `name`: 显示名称
- `workspace`: 工作空间路径
- `model`: 使用的大模型
- `skills`: 启用的技能列表

### 3. 创建工作空间目录

```bash
~/.openclaw/workspace-work/
```

### 4. 在 `channels.feishu.accounts` 中配置

```json
"work": {
  "appId": "cli_xxx_work",
  "appSecret": "work_secret",
  "botName": "工作助手",
  "dmPolicy": "allowlist",
  "allowFrom": ["*"],
  "groupPolicy": "open"
}
```

### 5. 在 `bindings` 中添加路由绑定

```json
{
  "agentId": "work",
  "match": {
    "channel": "feishu",
    "accountId": "work"
  }
}
```

### 6. 会话隔离

```json
"session": {
  "dmScope": "per-account-channel-peer"
}
```

### 7. 群组策略

```json
"groupPolicy": "open"
```

---

## 🚀 自动完成

配置后系统自动完成：

1. ✅ 解析配置信息
2. ✅ 智能匹配 Agent
3. ✅ 创建工作空间目录
4. ✅ 添加 Agent 配置
5. ✅ 添加飞书账户配置
6. ✅ 添加路由绑定
7. ✅ 更新 openclaw.json
8. ✅ 重启 Gateway
9. ✅ 返回配置报告

---

## 📊 配置报告示例

```
✅ 飞书机器人配置完成！

📋 配置信息:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
机器人名称：工作助手
Agent ID: work
Agent 名称：工作助手
工作空间：~/.openclaw/workspace-work
App ID: cli_xxx_work
技能：all
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 已完成的配置:
✅ 创建工作空间目录
✅ 添加 Agent 配置
✅ 添加飞书账户配置
✅ 添加路由绑定
✅ 更新 openclaw.json
✅ 重启 Gateway

📱 下一步:
1. 在飞书开放平台完成应用配置
2. 配置事件订阅
3. 发布应用
4. 在飞书中搜索"工作助手"并测试
```

---

## 🐛 常见问题

### Q1: 配置后机器人无响应

**解决**:
```bash
# 1. 检查 Gateway 状态
openclaw status

# 2. 查看日志
tail -f ~/.openclaw/logs/*.log

# 3. 验证配置
cat ~/.openclaw/openclaw.json | jq '.agents.list[] | {id, name}'
```

### Q2: Agent 匹配不准确

**解决**:
- 在配置信息中明确指定技能
- 如：`创建技能：Content Agent`

### Q3: 工作空间已存在

**解决**:
- 自动配置会检测，如果存在会跳过创建
- 如需重置，手动删除工作空间目录

---

## 📚 相关资源

- **GitHub**: https://github.com/jiebao360/feishu-bot-config-helper
- **OpenClaw 文档**: https://docs.openclaw.ai
- **飞书开放平台**: https://open.feishu.cn/

---

<div align="center">

**🦞 在飞书对话中直接配置，让 AI 帮你完成所有配置！**

**版本**: v1.0.0 | **创建**: 2026-03-17

</div>
