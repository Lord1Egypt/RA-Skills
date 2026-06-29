# coding-framework 扩展指南

> 版本: 10.1.0 | 更新日期: 2026-06-29

本文档说明如何扩展 coding-framework 的功能。

---

## 一、新增代理

### 1.1 创建代理定义文件

在 `agents/` 目录下创建 YAML 文件：

```yaml
# agents/i18n-checker.yaml
name: i18n-checker
display_name: "国际化检查员"
description: "检查代码中的硬编码字符串、日期格式、货币等国际化问题"
model: sonnet
color: purple

# 工具权限（最小权限原则）
tools:
  - Read
  - Grep
  - Glob

# 触发示例
trigger_examples:
  - "检查国际化"
  - "i18n review"
  - "有没有硬编码字符串"

# 系统提示
system_prompt: |
  你是一个专业的国际化检查员。你的职责是检查代码中的国际化问题。
  
  ## 检查维度
  
  1. **硬编码字符串**: 用户可见的文本是否使用 i18n 函数
  2. **日期格式**: 是否使用本地化日期格式
  3. **货币格式**: 是否使用 Intl.NumberFormat 或类似工具
  4. **时区处理**: 是否正确处理时区
  
  ## 输出格式
  
  ```markdown
  ### 国际化检查报告
  
  #### 发现的问题
  1. [文件:行号] 硬编码字符串: "Submit"
     建议: 使用 i18n.t('submit')
  
  #### 评分
  - 国际化就绪度: X/10
  ```
```

### 1.2 注册代理

在 `.coding-framework.yml` 中注册（可选）：

```yaml
agents:
  custom_agents:
    - i18n-checker
```

### 1.3 更新职责矩阵

在 `SKILL.md` 的"代理职责矩阵"中添加新代理的职责。

---

## 二、新增安全模式

### 2.1 添加模式定义

在 `rules/security-patterns.md` 中添加：

```markdown
### 26. 不安全的文件上传

**严重度**: high

**模式**:
- 未验证文件类型
- 未限制文件大小
- 直接保存到公开目录

**检查规则**:
```regex
# Python Flask
request\.files\[.*\]\.save\(
# Node.js multer
upload\.single\(.*\)\(req, res
```

**修复建议**:
1. 验证文件 MIME 类型
2. 限制文件大小
3. 使用随机文件名
4. 保存到非公开目录
```

### 2.2 添加匹配规则

在 `rules/security-rules.md` 中添加：

```yaml
- name: insecure-file-upload
  enabled: true
  severity: high
  matcher:
    pattern: 'request\.files\[.*\]\.save\('
    type: regex
  action:
    type: block
    message: "检测到不安全的文件上传，请验证文件类型和大小"
```

### 2.3 自动加载

`pre-exec-check.sh` 会自动加载 `rules/` 目录下的所有规则文件，无需修改脚本。

---

## 三、新增迭代模式

### 3.1 修改 loop-controller.py

在 `scripts/loop-controller.py` 中添加新模式：

```python
class IterationMode(Enum):
    FIXED = "fixed"
    MAX = "max"
    ADAPTIVE = "adaptive"
    CUSTOM = "custom"  # 新增

def check_custom_mode(self, state: dict) -> bool:
    """自定义模式检查逻辑"""
    # 你的实现
    current_iteration = state.get("iteration", 0)
    custom_condition = self.evaluate_custom_condition(state)
    return current_iteration < state["max"] and not custom_condition
```

### 3.2 更新文档

在 `references/iteration-patterns.md` 中添加新模式说明。

---

## 四、新增 Hook 事件

### 4.1 创建 Hook 脚本

在 `hooks/` 目录下创建脚本：

```bash
#!/bin/bash
# hooks/pre-commit-check.sh

# 从 stdin 读取 JSON 事件数据
EVENT_DATA=$(cat)

# 提取字段
if command -v jq &>/dev/null; then
    COMMIT_MSG=$(echo "$EVENT_DATA" | jq -r '.commitMessage // ""')
else
    COMMIT_MSG=$(echo "$EVENT_DATA" | grep -o '"commitMessage"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*: *"//;s/"$//')
fi

# 检查逻辑
if [[ "$COMMIT_MSG" =~ ^(WIP|wip) ]]; then
    echo '{"decision": "warn", "message": "检测到 WIP 提交，请考虑 squash"}'
else
    echo '{"decision": "allow", "message": ""}'
fi
```

### 4.2 注册事件

在 `references/hook-system.md` 中记录新事件。

---

## 五、贡献规范

### 5.1 代码风格

- Python: 遵循 PEP 8，使用类型提示
- Shell: 使用 `set -euo pipefail`
- YAML: 2 空格缩进
- Markdown: 中文使用全角标点

### 5.2 测试要求

新增功能必须包含：
- 单元测试（Python 脚本）
- 使用示例（文档）
- 边界情况处理

### 5.3 提交格式

```
<type>(<scope>): <subject>

type: feat/fix/docs/style/refactor/test
scope: agent/hook/iteration/security/docs
subject: 简短描述
```

示例：
```
feat(agent): 添加 i18n-checker 代理
fix(loop-controller): 修复并发状态冲突
docs(security): 更新安全模式文档
```

---

## 六、常见问题

### Q: 如何在不修改核心代码的情况下添加自定义规则？

A: 创建 `rules/custom-security-patterns.md`，在 `.coding-framework.yml` 中配置：

```yaml
security:
  custom_rules: rules/custom-security-patterns.md
```

### Q: 如何让我的代理只在特定场景触发？

A: 在代理 YAML 的 `trigger_examples` 中精确定义触发关键词，并在 `system_prompt` 中明确职责边界。

### Q: 迭代循环意外中断，如何恢复？

A: 使用 `--force` 参数重置状态：

```bash
python scripts/loop-controller.py init --name "task" --mode max --max 10 --force
```

---

## 七、联系与支持

- 问题反馈: 在 OpenClaw 工作区提交 Issue
- 讨论: OpenClaw Discord #coding-framework 频道

---

*本文档随 coding-framework 版本更新，请定期查看最新内容。*
