# 错误处理

## 自动备份

默认情况下，导入前会自动备份目标文件。

**备份位置**: `backup/` 目录
**备份文件名**: `原文件名_备份_时间戳.xlsx`

**配置**:
```yaml
error_handling:
  backup: true                   # 启用自动备份
  backup_path: "backup/"         # 备份路径
```

---

## 错误日志

所有导入错误都会记录到错误日志中。

**日志内容**:
- 错误发生时间
- 错误类型
- 涉及的行号和字段
- 错误详情

**配置**:
```yaml
error_handling:
  log_errors: true               # 记录错误日志
  error_log_path: "logs/import_errors.log"
```

---

## 验证报告

导入完成后会生成 JSON 格式的验证报告。

**报告内容**:
```json
{
  "task_name": "人员信息导入",
  "timestamp": "2024-01-20T10:30:00",
  "summary": {
    "total_records": 100,
    "successful": 95,
    "failed": 5,
    "skipped": 0
  },
  "errors": [
    {
      "row": 10,
      "field": "身份证号",
      "value": "123456",
      "error": "格式错误"
    }
  ]
}
```

---

## 错误处理策略

### 停止或继续

**配置**:
```yaml
error_handling:
  stop_on_error: false           # 遇到错误是否停止
  # false: 记录错误但继续处理
  # true: 遇到错误立即停止
```

### 错误恢复

**回滚机制**:
- 如果导入失败，可以自动回滚到备份状态
- 确保数据不会部分损坏

**配置**:
```yaml
error_handling:
  rollback_on_failure: true      # 失败时回滚
```

---

## 常见错误类型

### 1. 文件未找到

```
错误: 源文件不存在: data.xlsx
解决: 检查文件路径是否正确
```

### 2. 字段不匹配

```
错误: 找不到源字段: "姓名"
解决: 检查 field_mappings 配置
```

### 3. 数据验证失败

```
错误: 身份证号格式错误 (行 10)
解决: 检查数据格式，调整验证规则
```

### 4. 合并单元格冲突

```
错误: 无法写入合并单元格 (行 5, 列 C)
解决: 设置 skip_merged_cells: true 或调整模板
```

---

## 完整错误处理配置示例

```yaml
error_handling:
  # 备份设置
  backup: true
  backup_path: "backup/"

  # 错误日志
  log_errors: true
  error_log_path: "logs/import_errors.log"
  log_level: "DEBUG"

  # 处理策略
  stop_on_error: false
  rollback_on_failure: true

  # 验证报告
  generate_report: true
  report_path: "reports/validation_report.json"
```

---

## 调试技巧

### 1. 启用详细日志

```yaml
error_handling:
  log_level: "DEBUG"
  verbose: true
```

### 2. 测试模式

```yaml
options:
  dry_run: true                  # 不实际写入数据
  # 用于测试配置和验证数据
```

### 3. 部分导入

```yaml
options:
  max_rows: 100                  # 只处理前 100 行
  # 用于快速测试
```

更多故障排除请参考：[故障排除完整指南](troubleshooting.md)
