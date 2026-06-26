# Excel 数据导入 - 5分钟快速上手

## 快速概览

本指南将帮助您在 5 分钟内完成首次 Excel 数据导入操作。

## 前置条件

- Python 3.8+
- 已安装依赖: `uv add openpyxl pyyaml`

## 步骤 1: 准备测试数据 (1分钟)

创建测试目录和文件:

```bash
mkdir -p ~/excel_test/data ~/excel_test/templates ~/excel_test/output
```

### 创建源数据文件 (data.xlsx)

在 Excel 中创建以下内容:

| 姓名 | 身份证号 | 年龄 | 部门 |
|------|----------|------|------|
| 张三 | 110101199001011234 | 34 | 技术部 |
| 李四 | 110101199002021234 | 28 | 市场部 |

保存到: `~/excel_test/data/data.xlsx`

### 创建目标模板 (template.xlsx)

在 Excel 中创建以下格式:

| 身份证号码 | 员工姓名 | 年龄 | 部门 |
|------------|----------|------|------|
| (留空)     | (留空)   | (留空) | (留空) |

保存到: `~/excel_test/templates/template.xlsx`

## 步骤 2: 创建配置文件 (2分钟)

创建配置文件 `~/excel_test/import_config.yaml`:

```yaml
task_name: "人员信息导入测试"

source:
  file_path: "data/data.xlsx"
  sheet_name: "Sheet1"
  header_row: 1
  key_field: "身份证号"

target:
  file_path: "templates/template.xlsx"
  sheet_name: "Sheet1"
  header_row: 1
  data_start_row: 2
  output_path: "output/result.xlsx"

field_mappings:
  - source: "姓名"
    target: "身份证号码"
    required: true
  - source: "身份证号"
    target: "员工姓名"
    required: true
  - source: "年龄"
    target: "年龄"
  - source: "部门"
    target: "部门"

error_handling:
  backup: true
  backup_path: "backup/"
```

## 步骤 3: 执行导入 (1分钟)

```bash
cd ~/excel_test
python ~/.claude/skills/excel-data-import/scripts/excel_import.py import_config.yaml
```

**预期输出**:

```
正在读取配置文件: import_config.yaml
正在读取源数据: data/data.xlsx
正在读取目标模板: templates/template.xlsx
正在导入数据...
✓ 成功导入 2 条记录
✓ 输出文件: output/result.xlsx
✓ 备份文件: backup/template_备份_20240120_103045.xlsx
```

## 步骤 4: 验证结果 (1分钟)

打开 `output/result.xlsx`，您应该看到:

| 身份证号码     | 员工姓名 | 年龄 | 部门   |
|----------------|----------|------|--------|
| 110101199001011234 | 张三   | 34   | 技术部 |
| 110101199002021234 | 李四   | 28   | 市场部 |

## 常见用例

### 用例 1: 批量导入多个文件

修改配置文件:

```yaml
source:
  directory_path: "data/"  # 指定目录而非单个文件
  file_pattern: "*.xlsx"
  sheet_name: "Sheet1"
  header_row: 1
  key_field: "身份证号"
```

### 用例 2: 添加数据验证

```yaml
field_mappings:
  - source: "年龄"
    target: "年龄"
    validate: "range"
    validate_params:
      min: 18
      max: 65
```

### 用例 3: 数据转换

```yaml
field_mappings:
  - source: "入职日期"
    target: "参加工作时间"
    transform: "date"
    transform_params:
      input_format: "%Y-%m-%d"
      output_format: "%Y年%m月%d日"
```

## 故障排除

### 问题: 找不到模块

**解决方案**:
```bash
pip install openpyxl pyyaml
```

### 问题: 中文显示乱码

**解决方案**: 确保 Excel 文件保存为 UTF-8 编码

### 问题: 找不到匹配的行

**解决方案**:
1. 检查 `key_field` 的值是否正确
2. 确保源数据和目标表中的关键字段值一致
3. 检查是否有前后空格，可添加 `transform: "strip"`

## 下一步

恭喜！您已成功完成首次导入。接下来您可以:

- 📖 阅读 [配置详解](configuration-examples.md) 了解更多配置选项
- 📖 阅读 [数据映射指南](data-mapping-guide.md) 学习高级映射技巧
- 📖 阅读 [最佳实践](best-practices.md) 优化您的导入流程
- 📖 查看 [故障排除](troubleshooting.md) 解决复杂问题

## 配置速查表

| 配置项 | 说明 | 示例 |
|--------|------|------|
| `source.file_path` | 源文件路径 | `"data.xlsx"` |
| `source.directory_path` | 源目录（批量） | `"data/"` |
| `key_field` | 关键匹配字段 | `"身份证号"` |
| `field_mappings` | 字段映射规则 | 见上方示例 |
| `data_start_row` | 目标数据起始行 | `2` |
| `preserve_formatting` | 保持格式 | `true` |

## 性能提示

- **小文件** (<1000 行): 使用默认配置即可
- **大文件** (>10000 行): 考虑分批导入
- **批量文件**: 使用 `directory_path` 自动处理多个文件

---

**文档版本**: 1.0.0
**最后更新**: 2024-01-20
