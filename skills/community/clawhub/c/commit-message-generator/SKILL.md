---
name: commit-message-generator
description: Git 提交信息生成器。根据代码变更内容自动生成符合 Conventional Commits 规范的提交信息，包含类型、范围、简短描述、详细说明和关联的 Issue/需求号。触发词：生成提交信息、提交信息、commit message、git commit、生成 commit 信息
---

# Git 提交信息生成器

根据代码变更内容，自动生成符合 Conventional Commits 规范的 Git 提交信息。

## 何时使用

- 完成代码修改后，需要生成规范的提交信息
- 团队要求遵循 Conventional Commits 规范
- 需要关联 Issue 或需求号
- 不确定提交信息应该如何撰写

## 处理流程

### Step 1: 接收变更描述

用户可以通过以下方式提供变更内容：
- 文字描述变更内容
- 粘贴 `git diff` 输出
- 列出修改的文件和功能点

### Step 2: 分析变更类型

使用 `scripts/generate_commit_message.py` 自动分析：

```bash
scripts/generate_commit_message.py "用户输入的变更描述"
```

自动识别变更类型：
| 类型 | 说明 | 关键词 |
|------|------|--------|
| **feat** | 新功能 | 新增、添加、feature |
| **fix** | 修复 Bug | 修复、bug、问题 |
| **docs** | 文档 | 文档、readme、注释 |
| **style** | 格式 | 格式、空格、lint |
| **refactor** | 重构 | 重构、整理、清理 |
| **perf** | 性能优化 | 性能、优化、加速 |
| **test** | 测试 | 测试、unit、用例 |
| **chore** | 杂项 | 配置、构建、工具 |

### Step 3: 提取影响范围

自动识别模块/范围：
- 从文件路径提取（如 `src/algorithm/` → `algorithm`）
- 从代码内容识别（类名、函数名）
- 匹配常见模块名

### Step 4: 生成提交信息

生成符合规范的提交信息：
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Step 5: 输出和复制

输出格式化的提交信息，用户可直接：
- 复制到剪贴板
- 用于 `git commit` 命令
- 粘贴到 Git 工具中

## 提交信息结构

### 标准格式

```
feat(algorithm): 增加缓冲液单人份独立配置

- 新增配置项"单人份缓冲液量"，用于精确计算消耗
- 修改稀释逻辑，支持按实际人份计算而非固定倍数
- 更新相关接口文档

Closes #234
```

### 各部分说明

**主题行（Subject）**
- 格式：`<type>(<scope>): <description>`
- 长度：≤50 字符
- 时态：一般现在时
- 大小写：首字母小写

**正文（Body）**
- 说明为什么修改，而非修改了什么
- 每行≤72 字符
- 可包含多个变更点

**页脚（Footer）**
- Issue 关闭：`Closes #123`
- 破坏性变更：`BREAKING CHANGE: ...`
- 联合作者：`Co-authored-by: ...`

## 使用示例

### 示例 1：新功能

**用户输入：**
```
生成提交信息：新增缓冲液单人份配置功能，支持精确计算消耗量，需求号 234
```

**输出：**
```
feat(algorithm): 增加缓冲液单人份独立配置

- 新增配置项"单人份缓冲液量"
- 修改稀释逻辑，支持按实际人份计算

Closes #234
```

### 示例 2：Bug 修复

**用户输入：**
```
修复试剂仓传感器数据读取偶发失败的问题，添加重试机制
```

**输出：**
```
fix(sensor): 修复试剂仓传感器数据读取偶发失败

- 添加重试机制（最多 3 次）
- 增加超时处理
- 完善错误日志

影响：修复问题，建议尽快合并
```

### 示例 3：重构

**用户输入：**
```
重构稀释模块代码，提高可读性，无功能变化
```

**输出：**
```
refactor(dilution): 重构稀释模块代码提高可读性

- 拆分大函数为多个小函数
- 提取公共逻辑到工具类
- 添加单元测试覆盖

影响：代码重构，功能不变
```

### 示例 4：带 git diff

**用户输入：**
```
生成提交信息
diff --git a/src/core/algorithm.py b/src/core/algorithm.py
+ def calculate_reagent_volume():
+     """计算试剂用量"""
+     pass
```

**输出：**
```
feat(core): 新增试剂用量计算函数

- 新增 calculate_reagent_volume 函数
- 实现试剂用量计算逻辑

影响：新功能，不影响现有功能
```

## 参考文档

详见 `references/conventional-commits.md` - Conventional Commits 完整规范
详见 `references/commit-examples.md` - 提交信息示例集合

## 注意事项

1. **主题行简洁** - 50 字符以内，一眼看懂变更
2. **说明为什么** - 正文重点说明修改原因，而非内容
3. **关联 Issue** - 有需求号一定要关联，便于追溯
4. **破坏性变更** - 如有 API 不兼容修改，必须标注 BREAKING CHANGE
5. **原子提交** - 一次提交只做一件事，便于回滚和审查

## 团队规范建议

```markdown
## 提交规范

1. 使用 Conventional Commits
2. 主题行 50 字符以内
3. 正文说明为什么修改
4. 关联 Issue 号
5. 破坏性变更必须标注
```
