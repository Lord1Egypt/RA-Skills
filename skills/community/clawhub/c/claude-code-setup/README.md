# claude-code-setup

为项目创建生产级 `.claude/` AI 协作层配置。

## 快速开始

```bash
# 在项目根目录运行
openclaw skill claude-code-setup
```

## 生成的目录结构

```
.claude/
├── CLAUDE.md              # ⭐ 项目级全局指令（最重要）
├── rules/                 # 团队规则库
│   ├── frontend.md        # React/Vue 组件规范
│   ├── typescript.md      # TypeScript 类型规则
│   └── commit.md          # Git 提交规范
├── context/               # 项目上下文知识
│   ├── project.md         # 项目概述和模块
│   └── stack.md           # 技术栈详情
├── skills/                # 项目私有技能
│   └── generate-crud.md   # CRUD 生成工作流
└── prompts/               # 可复用 Prompt 模板
    └── review.md          # 代码审查清单
```

## 核心文件说明

### CLAUDE.md

权重最高的项目指令，Claude Code 每次工作都会优先读取。

**关键内容：**
- AI 角色定义
- 技术栈声明
- 编码规则（MUST/ALWAYS/NEVER）
- 代码生成要求

### rules/

团队硬规则，AI 必须遵守的约束。

**规则示例：**
- `NEVER use any type`
- `ALWAYS include error handling`
- `MUST use functional components`

### context/

项目知识库，让 Claude 真正理解你的项目。

**包含：**
- 项目概述
- 核心模块
- 技术栈详情

### skills/

可复用的工作流模板。

**示例：**
- CRUD 生成流程
- API 设计规范
- 测试编写流程

## 最佳实践

### ✅ 必做

1. **CLAUDE.md 控总规则** - 定义 AI 行为和约束
2. **rules/ 放硬约束** - 使用 MUST/ALWAYS/NEVER
3. **context/ 放项目知识** - 让 AI 理解项目背景
4. **skills/ 放稳定工作流** - 复用最佳实践

### ❌ 避免

1. 写成需求文档或 README
2. 规则太模糊（"尽量"、"建议"）
3. 只有 CLAUDE.md 没有模块化
4. 缺少项目上下文
5. 写太长废话

## 自定义

编辑生成的文件以适配你的项目：

```bash
# 修改 CLAUDE.md 添加项目特定规则
vim .claude/CLAUDE.md

# 添加新的规则
vim .claude/rules/backend.md

# 添加项目特定的技能
vim .claude/skills/generate-api.md
```

## 与其他工具对比

| 目录 | 作用 |
|------|------|
| `.vscode/` | 编辑器配置 |
| `.github/` | CI/CD 和 PR 模板 |
| `.cursor/` | Cursor IDE 配置 |
| **`.claude/`** | **Claude Code AI 行为中枢** |

## 许可证

MIT
