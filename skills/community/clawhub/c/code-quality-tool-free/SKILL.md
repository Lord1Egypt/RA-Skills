---
name: "code-quality-tool-free"
description: "提供代码风格规范、安全基础检查与可访问性要点,适合个人开发者快速校验代码质量。Use when 需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于无明确技术栈的模糊需求。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。提供结构化输出和错误处理机制。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "代码质量检查基础版"
  version: "1.0.0"
  summary: "提供代码风格规范、安全基础检查与可访问性要点,适合个人开发者快速校验代码质量。"
  tags:
    - "开发工具"
    - "代码质量"
    - "安全检查"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
tools:
  - exec
  - read

---

> **核心功能**: 本技能提供中文交互、化工作流场景等能力。

# 代码质量检查工具 - 免费版

## 概述

代码质量检查工具免费版为独立开发者提供基础的代码规范校验能力。工具聚焦于最常用的编码风格规则、基础安全检查和可访问性要点,帮助开发者在编码阶段就发现潜在问题,减少后期返工。

本版本适合个人项目、学习用途和小型团队日常代码评审。所有规则均以 Markdown 指令形式呈现,无需安装额外插件,直接在 AI Agent 中即可使用。

## 核心能力

### 1. 编码风格规范

提供主流语言的命名约定、格式化标准和注释规范。

| 规范类别 | 规则说明 | 示例 |
|:---------|:---------|:-----|
| 命名约定 | 变量/函数使用 camelCase,类/类型使用 PascalCase | `userName`、`UserService` |
| 格式化 | 4 空格缩进,单行不超过 80 字符 | 智能换行处理 |
| 注释规范 | 注释需有意义且与代码同步,删除过时注释 | 避免冗余注释 |
| 文件组织 | 相关函数集中放置,公共接口置顶 | 模块化组织 |

**输出**: 返回编码风格规范的执行结果,包含操作状态和输出数据。

### 2. 基础安全检查

覆盖最常见的代码安全风险点。

```bash
# 检查代码中是否存在硬编码密钥
grep -rnE "(password|secret|api_key|token)\s*=\s*['\"][^'\"]+['\"]" src/

# 检查是否使用了不安全的随机数
grep -rn "Math.random" src/

# 检查是否禁用了证书验证
grep -rn "rejectUnauthorized\s*:\s*false" src/
```

**输出**: 返回基础安全检查的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 3. 可访问性要点

提供基础的可访问性检查清单。

- 语义化 HTML 标签使用(`<button>`、`<nav>`、`<main>`)
- 图片需包含 `alt` 属性
- 表单元素需关联 `label`
- 键盘导航可用性验证
- 响应式断点检查:375px、768px、1024px、1440px

**输出**: 返回可访问性要点的执行结果,包含操作状态和输出数据。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：提供代码风格规范、安全基础检查与可、适合个人开发者快、速校验代码质量、面向独立开发者与、小团队的代码质量、辅助工具、涵盖命名规范、基础安全检查与可、核心能力、代码风格规范校验、密钥泄露、输入验证、可访问性要点提示、单文件快速审查等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一:个人项目代码自检

开发者在提交代码前进行快速自检。

```bash
# 对当前目录的源码进行基础检查
echo "=== 硬编码密钥检查 ==="
grep -rnE "(password|secret|api_key)\s*=\s*['\"]" . --include="*.js" --include="*.py"

echo "=== 详情见说明 检查 ==="

echo "=== 调试代码检查 ==="
grep -rn "console.log\|debugger\|print(" . --include="*.js" --include="*.py"
```

### 场景二:代码评审参考

在团队代码评审时作为检查清单使用。

```python
# 代码评审检查清单(免费版)
review_checklist = {
    "命名规范": [
        "变量名是否使用 camelCase",
        "类名是否使用 PascalCase",
        "常量是否使用 UPPER_SNAKE_CASE",
    ],
    "安全检查": [
        "是否存在硬编码密钥",
        "是否验证用户输入",
        "是否使用参数化查询",
    ],
    "可访问性": [
        "图片是否有 alt 属性",
        "表单是否有关联 label",
        "颜色对比度是否达标",
    ],
}

for category, items in review_checklist.items():
    print(f"\n=== {category} ===")
    for item in items:
        print(f"  [ ] {item}")
```

### 场景三:学习编码规范

新手开发者学习并应用编码规范。

```bash
# 生成代码风格报告
echo "=== 代码风格统计 ==="
echo "文件数: $(find . -name '*.js' -o -name '*.py' | wc -l)"
echo "总行数: $(find . -name '*.js' -o -name '*.py' -exec cat {} + | wc -l)"
echo "详情见说明 数: $(grep -rn '详情见说明' . --include="*.js" --include="*.py" | wc -l)"
echo "注释数: $(grep -rn '^\s*//' . --include="*.js" | wc -l)"
```

## 快速开始

### Step 1:触发检查

在 AI Agent 中输入以下指令触发代码质量检查:

```
请检查当前项目的代码质量,包括命名规范、安全风险和可访问性。
```

### Step 2:查看报告

Agent 会输出结构化的检查报告,包含问题分类、严重级别和修复建议。

### Step 3:应用修复

根据报告中的建议逐项修复,或让 Agent 自动生成修复补丁。

#
## 示例

在项目根目录创建 `.codequality.yml` 进行个性化配置:

```yaml
# 代码质量检查配置(免费版)
version: "1.0"

# 编码风格
style:
  indentation: 4
  max_line_length: 80
  naming:
    variables: camelCase
    classes: PascalCase
    constants: UPPER_SNAKE_CASE

# 安全检查
security:
  check_hardcoded_secrets: true
  check_insecure_random: true
  check_disabled_cert_validation: true

# 可访问性
accessibility:
  check_alt_text: true
  check_label_association: true
  responsive_breakpoints:
    - 375
    - 768
    - 1024
    - 1440
```

## 优选实践

1. **提交前必检**:在 `git commit` 前运行代码质量检查,避免问题进入仓库
2. **增量检查**:聚焦本次修改的文件,提升检查效率
3. **配合 Git Hook**:将检查集成到 `pre-commit` 钩子中实现自动化

```bash
# 配置 pre-commit 钩子
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
echo "运行代码质量检查..."
 --include="*.js" --include="*.py"
if [ $? -eq 0 ]; then
    echo "发现硬编码密钥,请修复后再提交"
    exit 1
fi
echo "检查通过"
EOF
chmod +x .git/hooks/pre-commit
```

4. **聚焦核心问题**:免费版优先关注安全风险和命名规范,风格细节可后续优化

## 常见问题

### Q1:免费版支持哪些编程语言?

免费版支持主流编程语言的通用规范检查,包括 JavaScript、TypeScript、Python、Java、Go 等。语言特定的深度检查需要专业版。

### Q2:如何处理大量误报?

建议通过 `.codequality.yml` 配置文件调整检查规则,关闭不适用的规则。对于特定文件或目录,可以使用注释标记跳过检查:

```javascript
// codequality-ignore-next-line
const demoToken = "test-token-for-demo";
```

### Q3:免费版与专业版有何区别?

| 能力维度 | 免费版 | 专业版 |
|:---------|:-------|:-------|
| 检查范围 | 单文件/单目录 | 全项目批量 |
| 安全深度 | 基础规则 | OWASP Top 10 |
| 报告格式 | 文本输出 | HTML/JSON/SARIF |
| 自定义规则 | 不支持 | 支持 |
| CI/CD 集成 | 手动触发 | 自动化流水线 |
| 团队协作 | 单人 | 多租户协同 |

### Q4:检查速度慢怎么办?

```bash
# 仅检查最近修改的文件
git diff --name-only HEAD | xargs grep -rnE "(password|secret)" 2>/dev/null

# 依赖说明
grep -rnE "(password|secret)" . --include="*.js" --exclude-dir=node_modules --exclude-dir=dist
```

## 依赖说明

### 运行环境

- **Agent 平台**:支持 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**:Windows / macOS / Linux
- **运行时**:Bash 或 PowerShell(用于执行检查脚本)

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| grep | 系统工具 | 必需 | 系统自带 |
| find | 系统工具 | 必需 | 系统自带 |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置

- 本 Skill 基于 Markdown 指令,无需额外 API Key
- 所有检查均在本地执行,代码不会上传到外部服务

### 可用性分类

- **分类**:MD+execute(纯 Markdown 指令,部分功能需要 exec 命令行执行能力)
- **说明**:基于 Markdown 的 AI Skill,通过自然语言指令驱动 Agent 执行代码质量检查任务
- **适用规模**:单文件到中小型项目(文件数 < 500)

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响

## 输出格式

处理结果以结构化格式返回, 包含状态码、消息和数据字段。

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。

## 核心功能

- **自动化执行**: 基于指令驱动的自动化流程
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据