# 移动端兼容规范（强制规则）

本 Skill 支持通过企业微信等移动端远程使用，全流程不得触发任何需要在电脑 IDE 中手动确认的操作。以下规则与凭证安全同为最高优先级强制规则，不可违反。

## 禁令 1：禁止创建任何临时文件或脚本

不得使用 `write_to_file`、`execute_command` 或任何其他方式创建辅助文件，包括但不限于：

- `/tmp/` 目录下的任何文件（如 `/tmp/parse_spans.py`、`/tmp/data.json`）
- 工作区目录下的临时 `.py`、`.json`、`.sh`、`.txt` 等文件
- 任何用于"数据解析""格式转换""中间处理"目的的脚本或数据文件

## 禁令 2：禁止执行文件删除命令

不得通过 `execute_command` 执行 `rm`、`rm -f`、`rm -rf`、`del`、`rmdir` 等文件删除命令，不得调用 `delete_file` 工具。这些操作会被 WorkBuddy 安全机制识别为危险命令（`security.dangerousCommand`），弹出"请在 IDE 中确认"拦截，导致移动端用户流程卡死。

## 禁令 3：返回数据必须在对话中直接处理

工具返回的所有数据（无论数据量大小、结构复杂度如何）必须在对话消息中直接完成解析和展示，不得借助外部脚本处理。具体要求：

- 使用 Markdown 表格展示结构化数据
- 使用代码块展示 JSON 原始数据或关键片段
- 使用缩进列表或树形文本展示层级结构（如 Span 调用树、火焰图）
- 数据量过大时，提取关键摘要信息展示，而非创建脚本做全量处理
- 如需统计分析（如耗时排序、错误率计算），直接在回复中计算并呈现结果

## 违规示例（严禁）

```
write_to_file("/tmp/parse_spans.py", ...)        # 禁止创建临时脚本
execute_command("python /tmp/parse_spans.py")     # 禁止执行临时脚本
execute_command("rm -f /tmp/parse_spans.py ...")  # 禁止删除文件
delete_file("/tmp/data.json")                     # 禁止调用删除工具
```

## 正确做法

```
1. 调用 call-tool 获取原始数据
2. 解析 JSON 结果，提取关键字段
3. 在回复消息中用 Markdown 表格/树形结构/代码块直接展示
4. 给出性能分析建议和结论
```
