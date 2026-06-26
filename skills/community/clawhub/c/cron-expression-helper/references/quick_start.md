# Cron表达式助手 - 快速开始

## 简介

Cron表达式助手是一个OpenClaw skill，帮助用户创建、验证和理解cron表达式。cron表达式用于定义定时任务的执行计划。

## 快速示例

### 1. 解释cron表达式
```bash
python scripts/explain_cron.py "0 9 * * 1-5"
```
输出：工作日上午9点执行

### 2. 查看所有示例
```bash
python scripts/explain_cron.py --examples
```

### 3. 展示执行时间
```bash
python scripts/show_cron.py "*/5 9-17 * * 1-5"
```
显示最近10次执行时间

### 4. 创建cron表达式
```bash
# 交互式创建
python scripts/create_cron.py --interactive

# 直接创建
python scripts/create_cron.py --minute "0" --hour "9" --day "*" --month "*" --weekday "1-5"
```

## 常用cron表达式

| 需求 | Cron表达式 | 说明 |
|------|------------|------|
| 每分钟执行 | `* * * * *` | 最简单的cron表达式 |
| 每小时整点 | `0 * * * *` | 每小时的第0分钟执行 |
| 每天午夜 | `0 0 * * *` | 每天00:00执行 |
| 工作日上午9点 | `0 9 * * 1-5` | 周一到周五上午9点 |
| 每5分钟 | `*/5 * * * *` | 每5分钟执行一次 |
| 每周日午夜 | `0 0 * * 0` | 周日00:00执行 |
| 每月1号 | `0 0 1 * *` | 每月1号00:00执行 |

## 在OpenClaw中使用

在OpenClaw会话中，你可以：

1. 直接运行脚本：
```bash
exec python scripts/explain_cron.py "0 9 * * 1-5"
```

2. 或者让Claude使用skill知识帮助你：
- "帮我创建一个每天备份的cron表达式"
- "这个表达式是什么意思：0 */2 * * *"
- "显示这个表达式接下来5次执行时间：0 0 * * 0"

## 故障排除

### 1. 脚本不工作
- 确保Python已安装（Python 3.6+）
- 检查脚本文件权限
- 在脚本目录中运行：`cd skills/cron-expression-helper`

### 2. 时间计算不准确
脚本使用简化算法计算执行时间。如需精确计算，安装croniter库：
```bash
pip install croniter
```

### 3. 编码问题（中文显示乱码）
在Windows上，如果看到乱码，可以：
1. 修改系统区域设置支持UTF-8
2. 或使用PowerShell运行脚本

## 下一步

1. 查看详细示例：`references/examples.md`
2. 学习cron表达式语法：`SKILL.md`中的"Cron表达式格式"部分
3. 尝试创建自己的cron表达式