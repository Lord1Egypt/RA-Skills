---
name: agent-config-validator
description: OpenClaw Agent配置验证器 - 自动检查openclaw.json与agent核心文档的一致性，检测过时引用，生成诊断报告并支持自动修复。当新增/调整agent或修改核心文档后使用此技能确保配置完整性。
---

# Agent Config Validator Skill

OpenClaw Agent 配置验证器 - 确保多智能体系统配置的一致性和完整性。

## 功能概述

此技能用于验证 OpenClaw 多智能体系统的配置完整性，包括：

1. **配置一致性检查** - 验证 `openclaw.json` 与实际 agent 目录结构是否匹配
2. **过时引用检测** - 检测核心文档中引用的已删除 agent、旧模型配置等
3. **文档完整性验证** - 检查必需的核心文档是否存在
4. **自动修复** - 支持自动修复常见问题（仅限安全配置项）
5. **诊断报告** - 生成详细的验证报告

## 安全设计原则

### ❌ 严禁自动修改的内容

以下核心数据**严禁**自动修改，仅做检测和报告：

| 类型 | 文件路径 | 原因 |
|------|---------|------|
| Agent 角色定义 | `agents/{agent}/agent/{agent}.md` | 包含角色人格定义 |
| 身份文档 | `agents/main/agent/IDENTITY.md` | 定义 Star 助手身份 |
| 灵魂/价值观 | `agents/main/agent/SOUL.md` | 核心价值观和行为准则 |
| 记忆文档 | `agents/main/agent/MEMORY.md` | 用户偏好和历史记忆 |
| 用户偏好 | `agents/main/agent/USER.md` | 用户个性化设置 |

### ⚠️ 需要人工确认的配置

以下配置变更**需要人工确认**：

| 配置项 | 说明 |
|--------|------|
| `agents.list` | 新增/删除 agent |
| `model.primary` | 主模型变更 |
| `model.fallbacks` | 备用模型变更 |
| `channels` | 渠道配置 |
| `auth` | 认证配置 |

### ✅ 可以安全自动修复的内容

| 类型 | 示例 | 安全级别 |
|------|------|---------|
| 清理无效引用 | 从 allowAgents 移除已删除 agent | ✅ 安全 |
| 移除无效绑定 | 清理指向不存在 agent 的 binding | ✅ 安全 |
| 格式修复 | JSON 语法错误、多余逗号 | ✅ 安全 |
| 备份创建 | 修改前自动备份 | ✅ 安全 |

## 使用场景

- 新增 agent 后验证配置
- 删除/合并 agent 后清理引用
- 修改 agent 核心文档后检查一致性
- 定期维护检查

## 工作流程

### 1. 执行完整验证（默认只读模式）

```javascript
// 默认：只检查，不修复（推荐）
validate_agent_config()

// 或显式指定
validate_agent_config({ 
    fix: false,        // 是否自动修复
    dryRun: true,      // 试运行模式（显示会做什么但不执行）
    verbose: true      // 显示详细信息
})
```

### 2. 安全修复模式

```javascript
// 仅修复安全项（清理无效引用）
validate_agent_config({ 
    fix: true,                    // 启用修复
    safeMode: true,               // 仅修复白名单内的配置
    confirmSensitive: false       // 不询问敏感变更
})
```

### 3. 完整修复模式（需要交互确认）

```javascript
// 修复所有可修复项（会询问敏感变更）
validate_agent_config({ 
    fix: true,
    safeMode: false,              // 允许修复非白名单项
    confirmSensitive: true        // 敏感变更需要确认
})
```

### 4. 检查特定 Agent

```javascript
validate_specific_agent({
    agentId: "luffy",
    checkDocs: ["AGENTS.md", "IDENTITY.md"]
})
```

### 5. 生成修复建议

```javascript
generate_fix_suggestions({
    outputPath: "D:\\OpenClaw\\工作汇报\\agent-config-report.md"
})
```

## 检查项目

### A. openclaw.json 配置检查

- [x] agents.list 中的每个 agent 都有对应的目录
- [x] agent 目录中的每个 agent 都在配置中注册
- [x] subagents.allowAgents 只包含存在的 agent
- [x] agentToAgent.allow 只包含存在的 agent
- [x] bindings 中的 agentId 都有效

### B. 核心文档过时检查

检查以下文档中的过时引用：

- **AGENTS.md**
  - [x] 可用子Agent列表与实际一致
  - [x] 模型配置表与实际一致
  - [x] 团队架构图与实际一致
  - [x] 文档保存目录与实际一致

- **IDENTITY.md**
  - [x] 团队架构描述与实际一致
  - [x] 调度规则表与实际一致
  - [x] 核心职责描述与实际一致

- **SOUL.md**
  - [x] 团队引用与实际一致

- **Agent 自身文档** (如 luffy.md, nami.md)
  - [x] 协作对象引用是否有效
  - [x] 能力描述是否准确

### C. 目录结构检查

- [x] 每个 agent 都有 agent/ 目录
- [x] 每个 agent 都有 workspace/ 目录
- [x] 必需的核心文档存在

## 安全修复白名单

以下配置项可以安全自动修复：

```javascript
SAFE_TO_AUTO_FIX = [
    'subagents.allowAgents',      // 清理无效 agent 引用
    'agentToAgent.allow',         // 清理无效通信权限
    'bindings'                    // 清理无效绑定
]
```

以下配置项需要人工确认：

```javascript
REQUIRE_MANUAL_CONFIRM = [
    'agents.list',                // 增删 agent
    'models.primary',             // 主模型变更
    'models.fallbacks',           // 备用模型变更
    'channels',                   // 渠道配置
    'auth'                        // 认证配置
]
```

## 自动修复功能

### 1. 安全自动修复（无需确认）

- 从 subagents.allowAgents 中移除无效 agent
- 从 agentToAgent.allow 中移除无效 agent
- 从 bindings 中移除无效绑定

### 2. 敏感变更（需要确认）

- 修改 agents.list
- 变更模型配置
- 修改渠道配置
- 修改认证信息

### 3. 文档更新（永不自动修复）

- 核心文档内容更新
- Agent 角色定义修改
- 团队架构描述更新

## 诊断报告格式

```markdown
# Agent Config Validation Report
生成时间: 2026-03-19 12:00:00

## 摘要
- 总 Agent 数: 3
- 配置有效: ✅
- 发现问题: 5
- 可安全修复: 2
- 需人工确认: 2
- 需人工处理: 1

## 安全状态
✅ 白名单修复: 启用
⚠️ 敏感变更确认: 需要
❌ 文档自动修复: 禁用

## 详细结果

### 1. openclaw.json 配置检查
✅ 所有配置的 agent 目录都存在
✅ subagents.allowAgents 有效
⚠️ agentToAgent.allow 包含无效引用: ["zoro", "sanji"]
   [可安全自动修复] 运行 --fix 清理

### 2. AGENTS.md 检查
⚠️ 发现过时引用:
  - 第42行: 引用已删除 agent "zoro"
  - 第58行: 模型配置表过时
   [需人工处理] 文档内容不会自动修改

### 3. IDENTITY.md 检查
✅ 团队架构描述正确
⚠️ 第31行: 仍引用已删除的 "索隆、山治"
   [需人工处理] 文档内容不会自动修改

## 修复建议
### 可安全自动修复
1. 从 agentToAgent.allow 移除 ["zoro", "sanji"]
   命令: validate_agent_config({fix: true, safeMode: true})

### 需人工处理
2. 更新 AGENTS.md 第42-45行
3. 更新 IDENTITY.md 第31行

## 执行修复
安全修复: validate_agent_config({fix: true, safeMode: true})
完整修复: validate_agent_config({fix: true, safeMode: false, confirmSensitive: true})
```

## 最佳实践

### 何时运行验证

1. **新增 Agent 后**
   - 验证新 agent 配置正确
   - 确保其他文档更新引用

2. **删除/合并 Agent 后**
   - 检查并清理所有引用
   - 验证无残留配置

3. **修改核心文档后**
   - 确保文档间一致性
   - 验证与配置匹配

4. **定期维护**
   - 建议每周运行一次
   - 及时发现配置漂移

### 修复策略

1. **先查看报告**
   ```javascript
   // 第一步：只检查，不修复
   validate_agent_config({ fix: false, verbose: true })
   ```

2. **安全修复**
   ```javascript
   // 第二步：修复安全项
   validate_agent_config({ fix: true, safeMode: true })
   ```

3. **人工处理文档**
   - 根据报告手动更新文档
   - 审核敏感配置变更

4. **验证修复结果**
   ```javascript
   // 第四步：再次验证
   validate_agent_config({ fix: false })
   ```

## 注意事项

### 1. 备份机制
- 自动修复前始终创建备份
- 备份文件: `openclaw.json.backup.{timestamp}`
- 可随时手动恢复

### 2. 权限要求
- 需要读写 openclaw.json
- 需要访问所有 agent 目录
- 建议以相同用户运行

### 3. 安全警告
⚠️ **永远不要**：
- 自动修改 Agent 核心文档
- 未经确认修改敏感配置
- 在生产环境直接修复

✅ **始终**：
- 先运行检查模式查看问题
- 确认备份已创建
- 验证修复后的配置

## 命令行使用

```bash
# 默认：只检查
agent-config-validator

# 详细输出
agent-config-validator --verbose

# 试运行（显示会做什么）
agent-config-validator --dry-run

# 安全修复（仅白名单项）
agent-config-validator --fix --safe-mode

# 完整修复（会询问敏感变更）
agent-config-validator --fix

# 生成报告文件
agent-config-validator --output report.md
```

## API 使用

```javascript
const AgentConfigValidator = require('agent-config-validator');

const validator = new AgentConfigValidator();

// 基本验证
const result = validator.validate({
    fix: false,
    verbose: true
});

// 获取详细结果
const report = validator.generateReport('report.md');

// 查看发现的问题
console.log(validator.issues);

// 查看已应用的修复
console.log(validator.fixes);
```

## 错误处理

### 配置文件不存在
```
❌ 错误: 配置文件不存在: D:\OpenClaw\.openclaw\openclaw.json
解决: 确保在正确的目录运行，或设置 OPENCLAW_ROOT 环境变量
```

### JSON 语法错误
```
❌ 错误: 无法加载 openclaw.json: Unexpected token...
解决: 手动修复 JSON 语法错误，或使用 JSON 验证器检查
```

### 权限不足
```
❌ 错误: 保存配置失败: EACCES: permission denied
解决: 确保有写入权限，或以管理员身份运行
```
