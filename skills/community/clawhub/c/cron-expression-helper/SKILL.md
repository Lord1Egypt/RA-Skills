---
name: cron-expression-helper
description: 创建、验证和展示cron表达式的工具。当用户需要创建cron表达式、验证cron语法、查看cron表达式的下一次执行时间、或生成最近10个符合cron表达式的时间点时使用。支持标准cron格式（5字段：分钟 小时 日 月 星期）和扩展格式。
---

# Cron表达式助手

这个skill帮助用户创建、验证和展示cron表达式。它提供交互式cron表达式创建、语法验证、以及展示最近10个符合cron表达式的时间点。

## 核心功能

1. **创建cron表达式** - 通过交互式问答帮助用户构建cron表达式
2. **验证cron语法** - 检查cron表达式的语法正确性
3. **展示执行时间** - 显示cron表达式最近10次执行时间
4. **解释cron表达式** - 用自然语言解释cron表达式的含义

## 使用方法

### 1. 创建cron表达式

使用交互式问答模式创建cron表达式：

```bash
python scripts/create_cron.py --interactive
```

或者直接指定参数：

```bash
python scripts/create_cron.py --minute "*/5" --hour "9-17" --day "*" --month "*" --weekday "1-5"
```

### 2. 验证和展示cron表达式

验证cron表达式并展示最近10次执行时间：

```bash
python scripts/show_cron.py "*/5 9-17 * * 1-5"
```

指定显示数量：

```bash
python scripts/show_cron.py "0 0 * * *" --count 20
```

### 3. 解释cron表达式

用自然语言解释cron表达式的含义：

```bash
python scripts/explain_cron.py "0 0 * * 0"
```

查看所有示例：

```bash
python scripts/explain_cron.py --examples
```

### 4. 在OpenClaw中直接使用

你也可以在OpenClaw会话中直接运行这些命令：

```bash
exec python scripts/create_cron.py --interactive
exec python scripts/show_cron.py "0 9 * * 1-5"
exec python scripts/explain_cron.py "*/5 * * * *"
```

## Cron表达式格式

标准cron表达式包含5个字段，用空格分隔：

```
分钟 小时 日 月 星期
```

字段取值范围：
- **分钟**：0-59
- **小时**：0-23
- **日**：1-31
- **月**：1-12 或 JAN-DEC
- **星期**：0-6 或 SUN-SAT（0和7都表示周日）

特殊字符：
- `*` - 任何值
- `,` - 值列表分隔符（例如：`1,3,5`）
- `-` - 范围（例如：`1-5`）
- `/` - 步长（例如：`*/5` 每5个单位）
- `?` - 仅在日和星期字段使用，表示"无特定值"

## 示例

1. **每天午夜执行**：`0 0 * * *`
2. **工作日每5分钟执行**：`*/5 9-17 * * 1-5`
3. **每月1号上午9点执行**：`0 9 1 * *`
4. **每周日午夜执行**：`0 0 * * 0`

## 脚本说明

### create_cron.py
交互式创建cron表达式。通过问答方式收集每个字段的值，生成完整的cron表达式。

### show_cron.py
验证cron表达式并展示最近10次执行时间。如果表达式无效，会显示错误信息。

### explain_cron.py
用自然语言解释cron表达式的含义，帮助用户理解表达式的执行计划。

## 注意事项

1. 日和星期字段有冲突时，cron解析器通常只使用其中一个
2. 月份名称（JAN-DEC）和星期名称（SUN-SAT）不区分大小写
3. 使用`?`字符可以避免日和星期字段的冲突
4. 时区基于系统时区，展示的时间会转换为用户本地时间

## 常见用例

- 设置定时任务
- 验证cron表达式语法
- 理解现有cron表达式的执行计划
- 调试定时任务调度问题