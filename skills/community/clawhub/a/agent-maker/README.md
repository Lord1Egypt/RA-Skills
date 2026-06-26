# Agent Maker - Agent 创建助手

帮助你快速创建新的 OpenClaw Agent，包含完整的配置文件结构和工作空间设置。

---

## 🎯 功能特性

### 核心能力
1. **创建新 Agent** - 生成完整的配置文件结构
2. **模板生成** - 提供标准化的 Agent 模板
3. **配置验证** - 检查配置文件完整性
4. **Agent 列表** - 查看当前所有已配置的 Agent
5. **复制配置** - 基于现有 Agent 快速创建新 Agent

---

## 🚀 使用方法

### 创建新 Agent
```bash
# 基础创建
agent-maker create --name=my-new-agent --role="Description of role"

# 带模板创建
agent-maker create --name=frontend-dev --template=developer
agent-maker create --name=security-ops --template=sysadmin
agent-maker create --name=content-writer --template=creative
```

### 查看现有 Agent
```bash
agent-maker list
```

### 验证 Agent 配置
```bash
agent-maker validate --name=agent-name
```

### 复制现有 Agent
```bash
agent-maker copy --from=existing-agent --to=new-agent
```

---

## 📁 生成的文件结构

每个新 Agent 会创建以下结构：

```
～/.openclaw/agents/[agent-name]/
├── IDENTITY.md          # Agent 身份定义
├── SYSTEM.md            # 核心规则和限制
├── SOUL.md              # 个性和价值观
├── AGENTS.md            # 工作流程指南
├── USER.md              # 用户偏好
├── HEARTBEAT.md         # 定期检查清单
└── QUICKSTART.md        # 快速启动指南

～/[agent-workspace]/
├── README.md            # 工作空间总览
└── [项目文件夹]/         # 实际工作内容
```

---

## 💡 使用示例

### 示例 1: 创建前端开发 Agent
```
用户：帮我创建一个前端开发专家 Agent

Agent Maker 会：
1. 创建配置文件到 ~/.openclaw/agents/frontend-dev/
2. 设置工作空间 ~/aicode/
3. 生成 IDENTITY.md 定义前端专家身份
4. 生成 SYSTEM.md 设置编码规范
5. 生成 SOUL.md 定义工作哲学
```

### 示例 2: 创建运维安全 Agent
```
用户：我需要一个负责系统运维和安全的 Agent

Agent Maker 会：
1. 创建 security-ops Agent 配置
2. 设置 ~/securityops/ 工作空间
3. 包含安全操作清单和应急响应流程
4. 设置权限级别和确认机制
```

---



### 使用技能
```bash
# 在对话中调用
@agent-maker 帮我创建一个新的 Agent
```

---

## 📋 配置文件说明

### IDENTITY.md
定义 Agent 的基本身份：
- 姓名和角色
- 表情符号
- 专业领域
- 工作空间位置

### SYSTEM.md
设置核心规则：
- 工作目录限制
- 权限级别
- 操作边界
- 安全限制

### SOUL.md
定义个性和价值观：
- 工作哲学
- 行为准则
- 决策原则
- 沟通风格

### AGENTS.md
工作流程指南：
- 标准操作流程
- 质量检查清单
- 最佳实践
- 常见问题处理

### USER.md
用户偏好记录：
- 用户信息
- 工作环境
- 特殊要求
- 历史记录

### HEARTBEAT.md
定期检查任务：
- 系统健康检查
- 项目进度跟踪
- 待办事项提醒

### QUICKSTART.md
快速启动指南：
- 基本用法
- 常见任务示例
- 快速参考

---

## ⚠️ 注意事项

1. **权限控制** - 创建 Agent 需要管理员权限
2. **命名规范** - Agent 名称使用 kebab-case（如 frontend-dev）
3. **工作空间隔离** - 每个 Agent 应有独立的工作目录
4. **配置文件审核** - 创建后应检查关键配置是否正确

---

## 🆘 故障排除

### 问题：Agent 无法启动
```bash
# 检查配置文件是否存在
ls -la ～/.openclaw/agents/[agent-name]/

# 验证配置文件格式
agent-maker validate --name=[agent-name]
```

### 问题：工作空间权限错误
```bash
# 检查工作空间目录权限
ls -la ～/[workspace-name]/

# 修复权限
chown -R openclaw:openclaw ～/[workspace-name]/
```

---

_last_updated: 2026-03-17_
_Agent Maker Skill Documentation_
 _by [OpenClaw](https://openclaw.ai)_
