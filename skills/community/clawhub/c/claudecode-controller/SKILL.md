---
name: claudecode-controller
description: 控制和管理 Claude Code 编码助手，支持项目感知编码、代码审查、重构和功能实现。使用 ACP 运行时在隔离会话中执行 Claude Code 任务，或在主会话中管理配置和项目上下文。
license: MIT
---

# Claude Code Controller

本技能提供对 Anthropic Claude Code 的完整控制，让你能够在 OpenClaw 环境中高效使用 Claude 进行代码开发。

## 核心能力

1. **项目感知编码** - Claude Code 理解你的项目结构和上下文
2. **代码审查** - 自动审查 PR、提供改进建议
3. **重构辅助** - 安全地重构现有代码
4. **功能实现** - 从需求描述到完整实现
5. **调试帮助** - 定位和修复 bug
6. **文档生成** - 自动生成代码文档

## 使用方式

### 模式选择

| 模式 | 用途 | 命令 |
|------|------|------|
| **ACP 隔离会话** | 长时间编码任务、需要独立上下文 | `/claudecode <任务描述>` |
| **主会话管理** | 配置管理、快速查询、项目设置 | `/claudecode-config <操作>` |

### 基本命令

```bash
# 启动 Claude Code 进行编码任务
/claudecode 帮我实现一个用户登录功能，使用 JWT 认证

# 代码审查
/claudecode 审查这个 PR 的代码质量，检查潜在问题

# 重构代码
/claudecode 重构这个模块，提高可维护性和性能

# 调试帮助
/claudecode 帮我找出这个 bug 的原因并修复
```

## 配置管理

### 设置 Claude Code

1. **安装 Claude Code CLI** (如未安装):
```bash
npm install -g @anthropic-ai/claude-code
```

2. **配置 API 密钥**:
```bash
# 设置环境变量
export ANTHROPIC_API_KEY="your-api-key"

# 或在 ~/.claude/config.json 中配置
```

3. **验证安装**:
```bash
claude --version
```

### 项目配置

在项目根目录创建 `.claude/settings.json`:

```json
{
  "model": "claude-sonnet-4-5-20250929",
  "allowedTools": ["bash", "edit", "write", "read"],
  "maxTurns": 50,
  "permissionMode": "auto"
}
```

## 工作流程

### 1. 代码开发流程

```
需求分析 → 方案设计 → 代码实现 → 测试验证 → 代码审查
```

**示例对话**:
```
用户：帮我创建一个 REST API，包含用户 CRUD 操作
Claude: 我将使用 Express.js 创建 API，包含以下端点：
  - POST /users - 创建用户
  - GET /users/:id - 获取用户
  - PUT /users/:id - 更新用户
  - DELETE /users/:id - 删除用户
  开始实现...
```

### 2. 代码审查流程

```
代码加载 → 静态分析 → 问题识别 → 建议生成 → 修复实施
```

**审查要点**:
- 代码风格和一致性
- 潜在 bug 和边界情况
- 性能优化机会
- 安全漏洞检查
- 测试覆盖率

### 3. 重构流程

```
代码分析 → 识别改进点 → 制定重构计划 → 安全重构 → 验证测试
```

**常见重构**:
- 提取函数/类
- 简化条件逻辑
- 优化数据结构
- 改进命名和文档

## 最佳实践

### 提示词技巧

1. **具体明确**: 清晰描述需求和约束
2. **提供上下文**: 说明项目背景和技术栈
3. **分步执行**: 复杂任务分解为小步骤
4. **验证输出**: 审查生成的代码是否符合预期

### 安全注意事项

1. **权限控制**: 限制 Claude Code 的文件访问范围
2. **代码审查**: 始终审查生成的代码后再提交
3. **敏感信息**: 不要将 API 密钥等敏感信息放入代码
4. **版本控制**: 使用 git 跟踪所有更改

## 故障排除

### 常见问题

| 问题 | 解决方案 |
|------|----------|
| API 密钥错误 | 检查 `ANTHROPIC_API_KEY` 环境变量 |
| 命令未找到 | 确认已安装 `@anthropic-ai/claude-code` |
| 权限被拒绝 | 检查 `.claude/settings.json` 中的 allowedTools |
| 超时错误 | 增加 `maxTurns` 配置或使用更小的任务 |

### 日志和调试

```bash
# 查看 Claude Code 日志
cat ~/.claude/logs/latest.log

# 调试模式运行
claude --debug
```

## 高级功能

### 多模型支持

```json
{
  "models": {
    "default": "claude-sonnet-4-5-20250929",
    "complex": "claude-opus-4-5-20250929",
    "quick": "claude-haiku-4-5-20250929"
  }
}
```

### 自定义工具

创建自定义工具脚本放在 `~/.claude/tools/`:

```bash
#!/bin/bash
# ~/.claude/tools/run-tests.sh
npm test "$@"
```

### 项目模板

使用预定义模板快速启动项目:

```bash
claude --template express-api
claude --template react-app
claude --template python-package
```

## 与 OpenClaw 集成

### ACP 会话使用

当使用 ACP 运行时，Claude Code 将在隔离会话中执行:

```
用户请求 → OpenClaw → ACP 会话 → Claude Code → 结果返回
```

**优势**:
- 独立上下文，不污染主会话
- 可配置超时和模型
- 支持长时间运行任务

### 主会话管理

在主会话中管理配置和项目设置:

- 查看和修改配置
- 管理项目上下文
- 查看历史记录
- 快速查询和统计

## 参考资源

- [Claude Code 官方文档](https://docs.anthropic.com/claude-code)
- [OpenClaw ACP 文档](https://docs.openclaw.ai)
- [技能开发指南](/usr/lib/node_modules/openclaw/skills/skill-creator/SKILL.md)
