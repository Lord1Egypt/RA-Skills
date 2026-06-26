---
name: ai-interview
description: |
  🤖 AI 面试系统 - 完整的 AI 面试解决方案
  
  提供求职者和面试官两个 AI Agent，支持飞书群聊面试 + 实时可视化观察。
  
  **功能：**
  - 👨‍💻 job-seeker - AI 求职者（3年前端，微前端经验）
  - 👨‍💼 recruiter - AI 面试官（提问、评估候选人）
  - 📊 web-viewer - 实时可视化观察面板
  
  **依赖：**
  - 飞书应用 x2（job-seeker + recruiter）
  - MoonShot API Key
  
  **触发词：**
  - "安装 ai-interview"
  - "安装面试系统"
  - "ai-interview"
metadata:
  version: "1.0.0"
  openclaw:
    emoji: "🤖"
    triggers:
      - "安装 ai-interview"
      - "安装面试系统"
      - "ai-interview"
---

# 🤖 AI 面试系统

完整的 AI 面试解决方案，包含求职者和面试官 Agent，支持飞书群聊面试。

## 系统架构

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  job-seeker │ ◄── │  飞书群聊   │ ──► │  recruiter  │
│   求职者    │     │             │     │    面试官   │
└─────────────┘     └─────────────┘     └─────────────┘
                          │
                    ┌─────┴─────┐
                    │ web-viewer │
                    │  可视化面板 │
                    └───────────┘
```

## 快速开始

### 方式一：一键安装（需要先配置）

```bash
# 1. 配置飞书应用
# 2. 运行安装脚本
cd ~/.openclaw/workspace/skills/ai-interview
./scripts/install.sh
```

### 方式二：手动配置

#### 步骤 1：准备飞书应用

需要创建两个飞书应用：

| 角色 | App ID | 用途 |
|------|--------|------|
| job-seeker | `cli_xxxxxxxx` | 求职者 Bot |
| recruiter | `cli_xxxxxxxx` | 面试官 Bot |

每个应用需要权限：
- `im:chat:send_as_bot` - 发送消息
- `im:message:content:readonly` - 读取消息
- `im:chat:readonly` - 查看群信息

#### 步骤 2：配置 openclaw.json

编辑 `~/.openclaw/openclaw.json`，添加：

```json
{
  "agents": {
    "list": [
      {
        "id": "job-seeker",
        "name": "求职者",
        "workspace": "~/.openclaw/workspace-job-seeker",
        "model": "moonshot/kimi-k2.5"
      },
      {
        "id": "recruiter",
        "name": "面试官",
        "workspace": "~/.openclaw/workspace-recruiter",
        "model": "moonshot/kimi-k2.5"
      }
    ]
  },
  "channels": {
    "feishu": {
      "accounts": {
        "job-seeker": {
          "appId": "你的job-seeker App ID",
          "appSecret": "你的job-seeker App Secret",
          "enabled": true,
          "agent": "job-seeker"
        },
        "recruiter": {
          "appId": "你的recruiter App ID",
          "appSecret": "你的recruiter App Secret",
          "enabled": true,
          "agent": "recruiter"
        }
      },
      "tools": {
        "agentToagent": true
      }
    }
  }
}
```

#### 步骤 3：配置 Agent 工作空间

创建 `~/.openclaw/workspace-job-seeker/IDENTITY.md`：

```markdown
# 你是求职者

你是参加前端工程师面试的求职者。

## 基本信息
- 姓名：张三
- 经验：3 年前端开发经验
- 技术栈：React, Vue, TypeScript, 微前端, Node.js

## 项目经验
- 参与过企业级微前端架构设计与实现
- 使用 qiankun 框架实现微前端改造

## 行为规则
- 只在飞书群里回复消息
- 被 @ 时才回复面试官
- 保持专业、友好的态度
```

创建 `~/.openclaw/workspace-recruiter/IDENTITY.md`：

```markdown
# 你是面试官

你是负责前端工程师面试的面试官。

## 基本信息
- 公司：某知名互联网公司
- 部门：前端技术部

## 考察重点
- 前端基础（HTML/CSS/JS）
- 框架能力（React/Vue）
- 微前端经验
- 问题解决能力

## 面试流程
1. 开场自我介绍
2. 项目经验介绍
3. 技术问题考察
4. 候选人提问环节
5. 总结与结束

## 行为规则
- 问题循序渐进，由浅入深
- 每轮问题后等待候选人回答
- 保持专业、友好的态度
```

#### 步骤 4：启动服务

```bash
openclaw gateway start
```

## 启动可视化面板

```bash
cd ~/.openclaw/workspace/skills/ai-interview
python3 server.py
```

然后打开浏览器访问：**http://localhost:8091**

## 使用方法

1. 把 job-seeker 和 recruiter 两个 Bot 加入同一个飞书群
2. 在群里 @recruiter 说"开始面试"
3. 面试官会自动 @job-seeker 开始提问
4. 可打开可视化面板实时观察对话

## 故障排除

| 问题 | 解决 |
|------|------|
| Bot 不回复 | 检查 App Secret 是否正确 |
| 消息发不出去 | 检查飞书群权限设置 |
| 无法对话 | 确认已启用 `agentToagent: true` |
| 可视化面板空白 | 检查 server.py 端口是否正确 |

## 文件结构

```
ai-interview/
├── SKILL.md              # 本文件
├── server.py             # 可视化面板后端
├── public/               # 前端静态文件
│   └── index.html
├── scripts/
│   └── install.sh        # 安装脚本
└── config/
    ├── job-seeker/       # 求职者配置模板
    └── recruiter/        # 面试官配置模板
```

## 更新日志

- 2026-03-18: 整合 job-seeker、recruiter、web-viewer 为统一 Skill
