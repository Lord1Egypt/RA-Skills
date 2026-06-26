---
name: cline-programming
description: 调用Cline AI编程工具的技能。提供plan-check-act工作流程，先让Cline生成代码规划，检查后执行，支持--verbose参数观察进度。
---

# C-Line 编程技能

通过Cline AI编程工具实现自动化代码生成和执行的技能，支持plan->check->act工作流程。

## 技能概述

本技能提供了一种结构化的编程方法，通过Cline AI编程工具实现自动化代码生成和执行。采用plan->check->act工作流程，确保代码质量和执行稳定性。

## 核心功能

### 1. 代码规划 (Plan)

使用Cline的plan模式生成代码规划，了解任务的实现方案。默认使用--yolo选项启用自动批准模式，避免交互式模式下的超时问题。

#### 使用方法

```bash
# 生成代码规划（自动批准模式）
cline task "创建一个简单的Web服务器" --plan --yolo --verbose --json
```

### 2. 规划检查 (Check)

检查Cline生成的代码规划，识别潜在问题并进行修改。

#### 使用方法

```bash
# 检查代码规划
# 注意：目前需要通过查看生成的规划文档进行手动检查
ls -la plan-*.md
cat plan-*.md
```

### 3. 代码执行 (Act)

使用Cline的act模式执行代码，支持--verbose参数观察执行进度。默认使用--yolo选项启用自动批准模式，避免交互式模式下的超时问题。

#### 使用方法

```bash
# 执行代码（自动批准模式）
cline task "创建一个简单的Web服务器" --act --yolo --verbose --json
```

**自动批准模式说明：**
- 使用 `--yolo` 选项会自动批准所有操作，适用于已知安全的简单任务
- 可以显著提高执行速度，避免交互式模式下的超时问题


## 完整任务流程

### 1. 完整任务执行

```bash
# 生成代码规划（自动批准模式）
cline task "创建一个简单的计算器程序" --plan --yolo --verbose --json

# 查看并检查代码规划
ls -la plan-*.md
cat plan-*.md

# 执行代码（自动批准模式）
cline task "创建一个简单的计算器程序" --act --yolo --verbose --json
```

### 2. 单步执行

```bash
# 生成代码规划（自动批准模式）
cline task "爬取并分析股票数据" --plan --yolo --verbose --json

# 检查规划文档
cat plan-2026-04-05.md

# 修改或优化规划（如果需要）
# 使用文本编辑器修改规划文档

# 执行代码（自动批准模式）
cline task "爬取并分析股票数据" --act --yolo --verbose --json
```

## 配置选项

### Cline配置

在使用Cline之前，需要先进行配置。Cline会在首次使用时提示配置信息，或者通过以下方式手动配置：

```bash
# 配置Cline（首次使用时会自动提示）
cline config

# 查看当前配置
cat ~/.cline/config.json
```

### 典型配置文件

Cline配置文件位于`~/.cline/config.json`，典型内容如下：

```json
{
  "actModeApiProvider": "openai",
  "actModeOpenAiModelId": "doubao-seed-2.0-code",
  "autoApprovalSettings": {"version":30,"enabled":true,"favorites":[],"manualApprovals":[]},
  "autoApproveAllToggled": false,
  "autoApprovalTimeout": 300000
}
```

### API凭证配置

Cline需要配置API凭证才能与AI模型通信。配置过程会要求提供API密钥，该密钥会安全地存储在系统密钥链或配置文件中。

```bash
# 配置API凭证
cline auth
```

### 自动批准模式

对于简单、已知安全的任务，可以使用--yolo选项启用自动批准模式，避免交互式模式下的超时问题。

```bash
# 使用自动批准模式执行任务
cline task "创建一个简单的文本文件" --act --yolo --timeout 60 --verbose --json
```

### 使用注意事项

1. **网络连接**：需要稳定的网络连接才能与AI模型通信
2. **执行时间**：AI生成代码和规划可能需要较长时间，耐心等待；使用--yolo选项可显著提高速度
3. **权限控制**：Cline会执行生成的代码，确保代码的安全性
4. **版本更新**：定期更新Cline工具以获取最新功能
5. **超时问题**：--yolo选项已默认启用，可有效避免超时问题

## 技术原理

### Cline集成

使用Cline的命令行接口：

- `cline plan` - 生成代码规划
- `cline act` - 执行代码
- `--verbose` - 详细输出模式

### 任务管理

技能实现了任务队列和状态管理，确保任务的可靠执行。

## 示例任务

### 示例1：创建简单Web服务器

```bash
# 生成代码规划（自动批准模式）
cline task "创建一个简单的Python Web服务器，使用Flask框架，监听8080端口" --plan --yolo --verbose --json

# 执行代码（自动批准模式）
cline task "创建一个简单的Python Web服务器，使用Flask框架，监听8080端口" --act --yolo --verbose --json
```

### 示例2：创建简单文本文件

```bash
# 使用自动批准模式创建文本文件（简单任务推荐）
cline task "创建一个名为 'test.txt' 的文本文件，内容为 'Hello Cline'" --act --yolo --timeout 60 --verbose --json
```

### 示例3：数据分析脚本

```bash
# 生成代码规划（自动批准模式）
cline task "创建一个Python脚本，读取CSV文件并分析数据，生成可视化图表" --plan --yolo --verbose --json

# 执行代码（自动批准模式）
cline task "创建一个Python脚本，读取CSV文件并分析数据，生成可视化图表" --act --yolo --verbose --json
```

## 错误处理

### 规划阶段错误

```bash
# 检查网络连接和API密钥
cat ~/.cline/config.json

# 重新生成代码规划（自动批准模式）
cline task "任务描述" --plan --yolo --verbose --json
```

### 执行阶段错误

```bash
# 查看错误信息
cline task "任务描述" --act --yolo --verbose --json 2>&1

# 检查生成的代码
ls -la generated-code/
cat generated-code/main.py
```

## 性能优化

### 任务拆分

将复杂任务拆分为多个简单任务，提高成功率。

```bash
# 任务拆分示例
cline task "创建用户登录功能" --plan --yolo --verbose --json
cline task "创建用户登录功能" --act --yolo --verbose --json

cline task "创建数据存储模块" --plan --yolo --verbose --json
cline task "创建数据存储模块" --act --yolo --verbose --json
```

### 规划复用

对常用任务进行规划复用，提高执行效率。

```bash
# 保存和复用代码规划
cline task "任务描述" --plan --yolo --verbose --json --save

# 加载之前的规划
cline task "任务描述" --act --yolo --verbose --json --load-plan plan-2026-04-05.md
```

### 使用自动批准模式

默认使用--yolo选项，对于已知安全的简单任务，可以显著提高执行速度，避免交互式模式下的超时问题。

**重要安全提示：**
使用--yolo选项会自动批准所有操作，包括代码执行。请确保您信任任务描述和执行过程，只对已知安全的任务使用此选项。

```bash
# 执行简单任务（自动批准模式）
cline task "创建一个简单的Python脚本" --act --yolo --verbose --json
```

## 安全注意事项

1. **代码审查**：在执行生成的代码前，仔细审查代码内容
2. **权限控制**：限制Cline的执行权限，避免执行危险代码
3. **安全配置**：配置Cline使用安全的API密钥和模型
4. **定期更新**：定期更新Cline和依赖库以修复安全漏洞

## 版本更新记录

### v1.0.5 (2026-04-05)

- 添加--json选项作为默认输出格式，便于自动化集成
- 更新所有示例，使用正确的命令格式：`cline task <prompt> --plan/--act --yolo --verbose --json`
- 重写测试脚本，验证--json选项功能

### v1.0.4 (2026-04-05)

- 修正了Cline命令使用方法，使用正确的`cline task --plan/--act`格式
- 避免了之前错误的`cline plan/act`格式
- 更新了所有示例和文档

### v1.0.3 (2026-04-05)

- 处理了ClawHub上报的安全警告
- 删除了未使用的requirements.txt文件
- 添加了API凭证配置和安全使用说明

### v1.0.2 (2026-04-05)

- 将plan模式也更新为使用--yolo自动批准模式
- 统一了整个工作流程的模式
- 添加了详细的配置说明

### v1.0.1 (2026-04-05)

- 添加了--yolo选项（自动批准模式）的说明
- 区分了交互式模式和自动批准模式的使用场景
- 提供了完整的使用方法示例

### v1.0.0 (2026-04-05)

- 初始版本
- 实现plan->check->act工作流程
- 支持--verbose参数
- 提供基本的错误处理
- 示例任务和使用说明
