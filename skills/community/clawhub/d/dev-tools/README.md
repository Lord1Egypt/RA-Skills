# /dev-tools - 开发工具箱

**版本**: 1.0.0  
**合并来源**: spec-management (v1.2.0) + pre-commit-check (v1.2.0) + diagnose-error (v1.2.0) + tech-debt-tracker (v1.2.0)

---

## 概述

`/dev-tools` 是开发工具箱技能，提供开发过程中的辅助工具：

- **spec** - 规范管理：版本管理、项目定制、冲突检测
- **pre-commit** - 预提交检查：提交前质量检查
- **diagnose** - 错误诊断：分析错误原因并提供解决方案
- **debt** - 技术债务跟踪：管理和跟踪技术债务

---

## 使用方式

### 查看所有工具

```bash
/dev-tools
```

输出：
```
**开发工具箱**

可用工具：
1. spec - 规范管理
2. pre-commit - 预提交检查
3. diagnose - 错误诊断
4. debt - 技术债务跟踪

请选择一个工具（输入编号或名称）：
```

---

## 1. spec - 规范管理

管理项目规范，包括版本管理、定制和冲突检测。

### 查看当前规范

```bash
/dev-tools spec view
```

### 定制项目规范

```bash
/dev-tools spec customize
```

可定制项：
- 命名规范
- 代码格式
- 注释规范
- 技术栈规范

### 更新规范版本

```bash
/dev-tools spec update
```

### 检测规范冲突

```bash
/dev-tools spec conflict
```

---

## 2. pre-commit - 预提交检查

代码提交前进行检查，确保符合规范和质量标准。

### 检查当前修改

```bash
/dev-tools pre-commit
```

### 检查指定目录

```bash
/dev-tools pre-commit src/points/
```

### 检查项目

**P0 检查（必须通过）**：
- ✅ 编译通过
- ✅ 无严重安全问题
- ✅ 无严重空指针风险
- ✅ 测试通过率 100%
- ✅ 无敏感信息泄露

**P1 检查（推荐通过）**：
- ✅ 代码规范遵循
- ✅ 测试覆盖率>80%
- ✅ 无重复代码
- ✅ 注释完整
- ✅ 提交信息规范

---

## 3. diagnose - 错误诊断

诊断执行过程中的错误，分析原因并给出解决方案。

### 诊断最近一次错误

```bash
/dev-tools diagnose
```

### 诊断指定技能错误

```bash
/dev-tools diagnose --skill=gen-code --task=Task-001
```

### 诊断流程

1. 收集错误信息
2. 分析可能原因（给出概率评估）
3. 执行诊断步骤
4. 给出诊断结论
5. 提供解决方案

---

## 4. debt - 技术债务跟踪

跟踪和管理技术债务。

### 查看债务清单

```bash
/dev-tools debt list
```

输出示例：
```
| 编号 | 描述 | 优先级 | 状态 |
|------|------|--------|------|
| TD-001 | 积分扣减未加事务 | P0 | 待修复 |
| TD-002 | 并发扣减可能超扣 | P0 | 待修复 |
| TD-003 | 积分规则硬编码 | P2 | 待修复 |

**统计**：
- 总债务数：4
- P0 债务：2
- P1 债务：1
- P2 债务：1
```

### 添加技术债务

```bash
/dev-tools debt add
```

### 生成债务报告

```bash
/dev-tools debt report
```

### 标记债务为已修复

```bash
/dev-tools debt fix TD-001
```

---

## 典型工作流

### 工作流 1：开发前定制规范

```bash
# 1. 查看当前规范
/dev-tools spec view

# 2. 定制项目规范
/dev-tools spec customize

# 3. 检测规范冲突
/dev-tools spec conflict
```

### 工作流 2：提交前检查

```bash
# 1. 开发完成，准备提交
/dev-tools pre-commit

# 2. 如果检查不通过，修复问题
# ...

# 3. 重新检查
/dev-tools pre-commit
```

### 工作流 3：错误处理

```bash
# 1. 技能执行失败
/gen-code Task-001
# 错误：代码生成失败

# 2. 诊断错误
/dev-tools diagnose

# 3. 根据诊断结果修复
# ...

# 4. 重新执行
/gen-code Task-001
```

### 工作流 4：技术债务管理

```bash
# 1. 代码审查后发现技术债务
/dev-tools debt add

# 2. 定期查看债务清单
/dev-tools debt list

# 3. 修复债务后标记
/dev-tools debt fix TD-001

# 4. 项目复盘时生成报告
/dev-tools debt report
```

---

## 与其他技能的区别

### dev-tools pre-commit vs review-code

| 维度 | dev-tools pre-commit | review-code |
|------|---------------------|-------------|
| 目的 | 提交前快速检查 | 详细代码审查 |
| 输出 | 通过/不通过判断 | 详细问题清单 |
| 使用时机 | 代码提交前 | 代码完成后 |
| 检查深度 | P0/P1 关键项 | 完整规范对照 |

**建议**：先使用 `review-code` 进行详细审查，修复问题后再使用 `pre-commit` 进行提交前检查。

---

## 向后兼容

为了向后兼容，以下旧命令仍然可用：

| 旧命令 | 新命令 |
|--------|--------|
| `/spec-management` | `/dev-tools spec` |
| `/spec-management view` | `/dev-tools spec view` |
| `/spec-management customize` | `/dev-tools spec customize` |
| `/pre-commit-check` | `/dev-tools pre-commit` |
| `/diagnose-error` | `/dev-tools diagnose` |
| `/tech-debt-tracker` | `/dev-tools debt` |
| `/tech-debt-tracker list` | `/dev-tools debt list` |
| `/tech-debt-tracker add` | `/dev-tools debt add` |
| `/tech-debt-tracker report` | `/dev-tools debt report` |

---

## 相关文件

- [技能定义](./SKILL.md)

---

*AI Speckits - 让 AI 编程更高效、更稳定*
