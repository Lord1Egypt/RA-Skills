# Cron表达式助手 Skill

这是一个OpenClaw skill，用于创建、验证和展示cron表达式。

## 功能特性

- 🎯 **交互式创建** - 通过问答方式帮助用户构建cron表达式
- ✅ **语法验证** - 检查cron表达式的语法正确性
- ⏰ **时间展示** - 显示cron表达式最近10次执行时间
- 📝 **自然语言解释** - 用中文解释cron表达式的含义

## 安装

1. 将整个`cron-expression-helper`文件夹复制到OpenClaw的skills目录：
   ```
   C:\Users\<用户名>\.openclaw\workspace\skills\
   ```

2. 确保Python已安装（需要Python 3.6+）

## 使用方法

### 1. 创建cron表达式

```bash
# 交互式创建
python scripts/create_cron.py --interactive

# 直接创建
python scripts/create_cron.py --minute "*/5" --hour "9-17" --day "*" --month "*" --weekday "1-5"
```

### 2. 验证和展示cron表达式

```bash
# 验证并展示最近10次执行时间
python scripts/show_cron.py "*/5 9-17 * * 1-5"

# 指定显示数量
python scripts/show_cron.py "0 0 * * *" --count 20
```

### 3. 解释cron表达式

```bash
# 解释cron表达式的含义
python scripts/explain_cron.py "0 0 * * 0"

# 查看示例
python scripts/explain_cron.py --examples
```

## 在OpenClaw中使用

当用户需要创建或理解cron表达式时，Claude会自动加载这个skill。你可以：

1. 直接运行脚本：
   ```bash
   exec python scripts/create_cron.py --interactive
   ```

2. 或者让Claude使用skill的知识来帮助用户：
   - "帮我创建一个每天上午9点执行的cron表达式"
   - "解释这个cron表达式：*/5 9-17 * * 1-5"
   - "显示这个cron表达式最近10次执行时间：0 0 * * 0"

## 脚本说明

### create_cron.py
交互式创建cron表达式。通过问答方式收集每个字段的值，生成完整的cron表达式。

### show_cron.py
验证cron表达式并展示执行时间。如果表达式无效，会显示错误信息。

### explain_cron.py
用自然语言解释cron表达式的含义，帮助用户理解表达式的执行计划。

## Cron表达式格式

标准cron表达式包含5个字段：

```
分钟 小时 日 月 星期
```

示例：
- `0 0 * * *` - 每天午夜执行
- `0 9 * * 1-5` - 工作日上午9点执行
- `*/5 * * * *` - 每5分钟执行

## 依赖

脚本本身不需要额外依赖。如果需要更准确的cron时间计算，可以安装：

```bash
pip install croniter python-dateutil
```

## 许可证

MIT License