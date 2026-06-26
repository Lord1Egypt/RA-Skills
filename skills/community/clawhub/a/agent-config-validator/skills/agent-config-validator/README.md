# Agent Config Validator

OpenClaw Agent 配置验证器 - 带安全机制的自动化配置检查工具

## 简介

自动验证 OpenClaw 多智能体系统的配置完整性，检测过时引用，支持安全自动修复。

**核心安全特性：**
- ✅ 默认只读模式，不修改任何内容
- ✅ 安全修复白名单机制
- ✅ 敏感变更需要交互确认
- ✅ 核心文档永不自动修改
- ✅ 修改前自动创建备份

## 安装

```bash
# 全局安装（推荐）
cd agent-config-validator
npm link

# 或本地使用
node src/validator.js [options]
```

## 快速开始

### 1. 检查模式（默认，安全）

```bash
# 仅检查，不修复（推荐首次使用）
agent-config-validator

# 详细输出
agent-config-validator --verbose
```

### 2. 安全修复模式

```bash
# 仅修复白名单内的安全项
agent-config-validator --fix --safe-mode
```

### 3. 完整修复模式（需确认）

```bash
# 修复所有可修复项（敏感变更会询问）
agent-config-validator --fix --confirm-sensitive
```

### 4. 试运行模式

```bash
# 显示会做什么，但不实际执行
agent-config-validator --fix --dry-run
```

## 命令行选项

| 选项 | 简写 | 说明 |
|------|------|------|
| `--fix` | `-f` | 启用自动修复 |
| `--safe-mode` | | 仅修复白名单项（默认启用） |
| `--safe-mode=false` | | 允许修复非白名单项 |
| `--confirm-sensitive` | `-c` | 敏感变更需要确认 |
| `--dry-run` | `-d` | 试运行模式 |
| `--verbose` | `-v` | 详细输出 |
| `--output <path>` | `-o` | 保存报告到文件 |

## 安全设计

### 安全修复白名单

以下配置项可以**安全自动修复**：

- `subagents.allowAgents` - 清理无效 agent 引用
- `agentToAgent.allow` - 清理无效通信权限
- `bindings` - 清理无效绑定

### 需要人工确认的配置

以下配置变更**需要确认**：

- `agents.list` - 增删 agent
- `models.primary` - 主模型变更
- `models.fallbacks` - 备用模型变更
- `channels` - 渠道配置
- `auth` - 认证配置

### 严禁自动修改的内容

以下核心数据**永不自动修改**：

| 类型 | 文件 | 原因 |
|------|------|------|
| Agent 角色定义 | `agents/{agent}/agent/{agent}.md` | 包含角色人格 |
| 身份文档 | `agents/main/agent/IDENTITY.md` | 定义助手身份 |
| 灵魂/价值观 | `agents/main/agent/SOUL.md` | 核心价值观 |
| 记忆文档 | `agents/main/agent/MEMORY.md` | 用户偏好 |
| 用户偏好 | `agents/main/agent/USER.md` | 个性化设置 |

## 使用场景

### 场景 1: 新增 Agent 后

```bash
# 1. 手动创建 agent 目录和核心文档
# 2. 手动更新 openclaw.json
# 3. 运行验证检查
agent-config-validator --verbose

# 4. 安全修复配置引用
agent-config-validator --fix --safe-mode

# 5. 人工更新其他文档中的引用
```

### 场景 2: 删除/合并 Agent 后

```bash
# 1. 从 openclaw.json 移除配置
# 2. 运行安全修复清理引用
agent-config-validator --fix --safe-mode

# 3. 根据报告人工更新文档
```

### 场景 3: 定期维护

```bash
# 建议每周运行一次
agent-config-validator --verbose --output report.md
```

## 编程接口

```javascript
const AgentConfigValidator = require('agent-config-validator');

const validator = new AgentConfigValidator();

// 基本验证（只读）
await validator.validate({
    fix: false,
    verbose: true
});

// 安全修复
await validator.validate({
    fix: true,
    safeMode: true
});

// 完整修复（带确认）
await validator.validate({
    fix: true,
    safeMode: false,
    confirmSensitive: true
});

// 生成报告
const report = validator.generateReport('report.md');

// 查看问题
console.log(validator.issues);

// 查看修复记录
console.log(validator.fixes);
```

## 诊断报告

验证完成后会生成详细报告：

```markdown
# Agent Config Validation Report
生成时间: 2026/3/19 12:00:00

## 摘要
- 总 Agent 数: 3
- 错误数: 0
- 警告数: 3
- 可安全修复: 2
- 需人工处理: 1

## 安全状态
✅ 白名单修复: 启用
⚠️ 敏感变更确认: 需要
❌ 文档自动修复: 禁用

## 详细结果
### 1. openclaw.json 配置检查
⚠️ agentToAgent.allow 包含无效 agent [✅ 可安全自动修复]

### 2. 文档过时检查
⚠️ AGENTS.md 第42行: 引用已删除的 agent [🔒 受保护文档]

## 修复建议
### 可安全自动修复
1. 从 agentToAgent.allow 移除无效 agent
   命令: agent-config-validator --fix --safe-mode

### 需人工处理
2. 更新 AGENTS.md 第42行
```

## 备份机制

每次自动修复前都会创建备份：

```
openclaw.json.backup.1710835200000
```

如需恢复：

```bash
cp openclaw.json.backup.1710835200000 openclaw.json
```

## 最佳实践

1. **先检查再修复**
   ```bash
   agent-config-validator          # 先查看问题
   agent-config-validator --fix    # 再执行修复
   ```

2. **使用试运行模式**
   ```bash
   agent-config-validator --fix --dry-run
   ```

3. **定期维护**
   ```bash
   # 添加到定时任务
   0 9 * * 1 agent-config-validator --output weekly-report.md
   ```

4. **版本控制**
   ```bash
   # 修复前提交当前配置
   git add .openclaw/openclaw.json
   git commit -m "备份配置"
   
   # 运行修复
   agent-config-validator --fix
   ```

## 故障排除

### 配置文件不存在
```
❌ 错误: 配置文件不存在
解决: 确保在 OpenClaw 根目录运行，或设置 OPENCLAW_ROOT 环境变量
```

### JSON 语法错误
```
❌ 错误: 无法加载 openclaw.json: Unexpected token...
解决: 手动修复 JSON 语法错误
```

### 权限不足
```
❌ 错误: 保存配置失败: EACCES
解决: 确保有写入权限
```

## 许可证

MIT
