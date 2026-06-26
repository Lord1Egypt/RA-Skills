---
name: "ai-coding"
version: "1.0.0"
description: "AI辅助编程技能，帮助Claude学习如何创建和使用OpenClaw技能"
author: "AI Skills Team"
tags: ["编程", "开发", "OpenClaw", "技能"]
requires: []
---

# AI编程技能

AI辅助编程技能，帮助Claude学习如何创建和使用OpenClaw技能。

## 技能描述

这是一个关于如何开发OpenClaw技能的完整指南。它解释了技能的结构、如何编写SKILL.md、如何创建工具脚本，以及如何在对话中"教"Claude使用这些技能。

## 使用场景

- 用户问："如何在OpenClaw中创建新技能？" → 提供完整指南
- 用户说："创建一个数据处理技能" → 按照指南创建技能结构
- 用户问："SKILL.md应该怎么写？" → 提供格式和示例
- 用户说："我写了一个技能，OpenClaw不会用" → 解释如何教学

## 技能结构

### 标准技能目录结构

```
skill-name/
├── SKILL.md              # 主文档（OpenClaw自动读取）
├── references/           # 参考文档（自动读取）
│   ├── topic1.md
│   └── topic2.md
└── tools/               # 工具脚本（需要教OpenClaw调用）
    └── script.py
```

### OpenClaw如何学习

**自动做的**：
- ✅ 读取 `SKILL.md`
- ✅ 读取 `references/*.md`
- ✅ 理解功能说明
- ✅ 响应相关请求

**需要你做的**：
- ⚠️ 安装 Python 依赖
- ⚠️ 在对话中教它如何使用工具
- ⚠️ 提供清晰的工具脚本

## 创建技能的步骤

### 步骤1：创建技能目录

```bash
mkdir -p ~/.openclaw/skills/my-skill/references
```

### 步骤2：编写SKILL.md

```markdown
---
name: my-skill
description: 我的自定义技能
version: 1.0.0
---

# 我的技能

## 功能
- 功能1: 描述
- 功能2: 描述

## 使用方法
当我说"XXX"时，请调用YYY工具
```

### 步骤3：添加参考文档（可选）

```bash
cat > ~/.openclaw/skills/my-skill/references/guide.md << 'EOF'
# 使用指南

详细的使用说明...
EOF
```

### 步骤4：在对话中"教"OpenClaw

```
用户: 我创建了一个新技能 my-skill，位置在 ~/.openclaw/skills/my-skill/

OpenClaw: 我看到这个技能了，它包含...

用户: 这个技能有一个工具在 tools/script.py，
当我说"执行XXX"时，请调用它。

OpenClaw: 明白了，我会记住这个规则。

用户: 执行XXX

OpenClaw: [自动调用工具]
```

## SKILL.md编写规范

### 推荐格式

```markdown
---
name: your-skill
description: 简短描述
version: 1.0.0
author: 你的名字
---

# 技能名称

## 功能概述
简要描述这个技能做什么

## 主要功能

### 功能1
- 说明
- 使用示例

### 功能2
- 说明
- 使用示例

## 使用方法

### 场景1: XXX
当用户说"XXX"时，我会：
1. 步骤1
2. 步骤2

## 工具脚本

### script1.py
位置: tools/script1.py
功能: 描述
调用方式: python tools/script1.py

## 限制
- 限制1
- 限制2
```

## 工具脚本最佳实践

### 基本结构

```python
#!/usr/bin/env python3
"""
工具脚本名称
"""

def main():
    """主函数"""
    # 你的代码
    pass

if __name__ == "__main__":
    main()
```

### 关键点

- ✅ 清晰的函数命名
- ✅ 完整的注释
- ✅ 错误处理
- ✅ 命令行参数支持

## 故障排除

### 问题1：OpenClaw识别不到Skill

**解决**：
```bash
# 确认位置
ls ~/.openclaw/skills/your-skill/SKILL.md

# 验证格式
head -5 ~/.openclaw/skills/your-skill/SKILL.md
# 应该看到 --- 开头的YAML
```

### 问题2：OpenClaw不会调用工具

**解决**：需要在对话中教它
- 告诉它工具位置
- 告诉它调用方式
- 告诉它触发条件

### 问题3：文档没有被索引

**解决**：确认文件在 references/ 目录
```bash
ls ~/.openclaw/skills/your-skill/references/
```

## 最佳实践

### ✅ DO（推荐）

1. **清晰的命名**
   - skill-name: 清楚表达功能
   - file names: 描述性命名

2. **完整的文档**
   - SKILL.md: 完整功能说明
   - references/: 详细参考文档

3. **示例丰富**
   - 代码示例
   - 对话示例
   - 使用场景

4. **错误处理**
   - 工具脚本处理异常
   - 提供错误信息

### ❌ DON'T（避免）

1. 不要过度依赖自动化
   - OpenClaw需要你教它如何使用工具

2. 不要省略文档
   - 没有文档 = OpenClaw学不会

3. 不要硬编码路径
   - 使用相对路径或环境变量

## 注意事项

1. **SKILL.md是关键**：OpenClaw自动读取
2. **需要你教学**：在对话中教它使用工具
3. **提供工具脚本**：清晰的调用接口
4. **持续优化**：根据使用反馈改进
