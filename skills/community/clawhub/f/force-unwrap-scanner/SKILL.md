---
name: force-unwrap-scanner
description: 扫描并报告 Swift 项目中的强制解包（!）和 try! 使用情况，识别潜在崩溃风险
domain: ios-macos
risk: low
version: 1.0
homepage: https://github.com/soponcd/timeflow-skills/tree/main/teams/skills/force-unwrap-scanner
metadata:
  clawdbot:
    emoji: 🔎
---

# Force Unwrap Scanner

扫描并报告项目中的强制解包使用情况，帮助识别潜在的运行时崩溃风险。

## 功能

- 扫描项目中所有的 `try!` 和 `!` 强制解包使用
- 按风险等级分类（高/中/低）
- 生成详细报告
- 提供修复建议

## 使用方法

```bash
cd .agent/skills/force-unwrap-scanner
./RunSkill.sh [scan|report|fix]
```

### 参数说明

- `scan` - 扫描项目并输出结果
- `report` - 生成详细的 HTML 报告
- `fix` - 交互式修复（高风险项需要手动确认）

## 风险分级

| 风险等级 | 说明 | 示例 |
|-----------|------|------|
| 🔴 高 | EKEventStore、SwiftData、FileIO 等系统级操作 | `try! EKEventStore()` |
| 🟡 中 | 数据库查询、网络请求 | `try! fetchTasks()` |
| 🟢 低 | 本地数据、已知安全值 | `let x = dict["key"]!` |

## 输出示例

```
🔍 Force Unwrap Scanner Report
===================================

Total: 3 findings
  🔴 High: 1
  🟡 Medium: 1
  🟢 Low: 1

Files with issues:
  TimeFlow/Services/EventKitService.swift:35
  TimeFlow/ViewModels/AppState.swift:12
  TimeFlow/Helpers/ParseHelper.swift:45
```
