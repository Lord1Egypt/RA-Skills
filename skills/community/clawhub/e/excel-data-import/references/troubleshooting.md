# Excel 数据导入 - 故障排除

## 快速诊断流程

遇到问题时，按以下步骤快速定位：

```
问题发生
  ↓
1. 检查配置文件 (YAML 语法、路径)
  ↓
2. 检查源数据 (文件格式、数据质量)
  ↓
3. 检查目标模板 (表头、格式)
  ↓
4. 查看错误日志 (详细错误信息)
  ↓
5. 查看备份文件 (验证备份是否生成)
```

## 常见问题及解决方案

### 问题 1: 配置文件错误

#### 错误: `YAML 语法错误`

**错误信息**:
```
yaml.scanner.ScannerError: while scanning a simple key
```

**原因**: YAML 缩进或语法错误

**解决方案**:
```yaml
# ❌ 错误: 使用 Tab 缩进
field_mappings:
  	- source: "姓名"

# ✅ 正确: 使用空格缩进 (2个空格)
field_mappings:
  - source: "姓名"
```

**检查工具**:
```bash
# 使用在线工具验证 YAML 语法
# https://www.yamllint.com/

# 或使用 Python 验证
python -c "import yaml; yaml.safe_load(open('import_config.yaml'))"
```

#### 错误: `文件路径不存在`

**错误信息**:
```
FileNotFoundError: [Errno 2] No such file or directory: 'data.xlsx'
```

**原因**: 文件路径不正确

**解决方案**:
```yaml
# ❌ 错误: 相对路径不明确
source:
  file_path: "data.xlsx"

# ✅ 正确: 使用绝对路径或相对于配置文件的路径
source:
  file_path: "/home/user/project/data/data.xlsx"
  # 或
  file_path: "./data/data.xlsx"
```

**调试命令**:
```bash
# 检查文件是否存在
ls -l /home/user/project/data/data.xlsx

# 检查当前工作目录
pwd
```

### 问题 2: 数据导入问题

#### 错误: `找不到匹配的行`

**错误信息**:
```
警告: 找不到 10 条记录的匹配行
```

**原因**: 关键字段值不匹配

**诊断步骤**:
```python
# 1. 检查源数据的关键字段值
import pandas as pd
df = pd.read_excel('source.xlsx')
print(df['身份证号'].head())

# 2. 检查目标表的关键字段值
df_target = pd.read_excel('template.xlsx')
print(df_target['身份证号码'].head())

# 3. 比较是否有空格或格式差异
print(f"源数据: ['{df['身份证号'][0]}']")
print(f"目标表: ['{df_target['身份证号码'][0]}']")
```

**解决方案**:
```yaml
field_mappings:
  # 添加 strip 转换，去除前后空格
  - source: "身份证号"
    target: "身份证号码"
    transform: "strip"

# 或使用多字段匹配
source:
  key_fields:
    - "身份证号"
    - "姓名"
```

#### 错误: `字段映射失败`

**错误信息**:
```
KeyError: '字段名不存在'
```

**原因**: 源数据或目标表中缺少指定的字段

**解决方案**:
```python
# 列出源数据所有字段
import pandas as pd
df = pd.read_excel('source.xlsx')
print("源数据字段:", df.columns.tolist())

# 列出目标表所有字段
df_target = pd.read_excel('template.xlsx')
print("目标表字段:", df_target.columns.tolist())
```

**配置修正**:
```yaml
# 确保字段名完全匹配（区分大小写）
field_mappings:
  - source: "姓名"          # 必须与源数据列名完全一致
    target: "员工姓名"      # 必须与目标表列名完全一致
```

### 问题 3: 数据验证错误

#### 错误: `必填字段为空`

**错误信息**:
```
ValidationError: 第 10 行: 身份证号不能为空
```

**原因**: 必填字段包含空值

**解决方案**:
```yaml
# 方案 1: 添加默认值
field_mappings:
  - source: "年龄"
    target: "年龄"
    required: true
    default: "18"           # 添加默认值

# 方案 2: 移除 required 标记
field_mappings:
  - source: "年龄"
    target: "年龄"
    required: false         # 改为非必填

# 方案 3: 前置数据清洗
# 使用 pandas 清洗数据
import pandas as pd
df = pd.read_excel('source.xlsx')
df = df.dropna(subset=['身份证号'])  # 删除空值行
df.to_excel('source_cleaned.xlsx', index=False)
```

#### 错误: `数据格式验证失败`

**错误信息**:
```
ValidationError: 第 5 行: 身份证号格式错误
```

**原因**: 数据不符合验证规则

**解决方案**:
```yaml
# 方案 1: 调整验证规则
field_mappings:
  - source: "身份证号"
    target: "身份证号码"
    validate: false        # 临时禁用验证

# 方案 2: 添加数据转换
field_mappings:
  - source: "身份证号"
    target: "身份证号码"
    transform: "strip"     # 去除空格
    validate: "id_card"

# 方案 3: 自定义验证
validations:
  - field: "身份证号"
    rules:
      - type: "regex"
        pattern: "^\d{15}|\d{18}$"
        message: "身份证号必须是15位或18位数字"
```

### 问题 4: 格式和编码问题

#### 错误: `中文显示乱码`

**原因**: 字体或编码问题

**解决方案**:
```yaml
# 配置中文字体
options:
  font_settings:
    default_font: "微软雅黑"
    fallback_fonts: ["宋体", "黑体", "Arial Unicode MS"]
```

**检查步骤**:
```python
# 检查文件编码
import chardet

with open('data.xlsx', 'rb') as f:
    result = chardet.detect(f.read())
    print(f"编码: {result['encoding']}")
```

#### 错误: `合并单元格格式丢失`

**错误信息**:
```
警告: 导入后合并单元格格式可能丢失
```

**解决方案**:
```yaml
options:
  preserve_formatting: true      # 保持格式
  skip_merged_cells: false       # 不跳过合并单元格
```

**验证方法**:
```python
from openpyxl import load_workbook

wb = load_workbook('output/result.xlsx')
ws = wb.active

# 检查合并单元格
print("合并单元格:", ws.merged_cells.ranges)
```

### 问题 5: 性能问题

#### 问题: 处理速度慢

**原因**: 大文件或复杂配置

**解决方案**:
```yaml
# 1. 禁用不需要的功能
options:
  preserve_formatting: false     # 不保持格式，提升速度
  skip_validation: true          # 跳过验证（谨慎使用）

# 2. 分批处理
# 手动分割大文件
```

**性能优化脚本**:
```python
import pandas as pd

# 分割大文件
df = pd.read_excel('large_file.xlsx')
batch_size = 5000

for i in range(0, len(df), batch_size):
    batch = df.iloc[i:i+batch_size]
    batch.to_excel(f'batch_{i//batch_size}.xlsx', index=False)
    print(f"已生成批次 {i//batch_size + 1}")
```

#### 问题: 内存占用过高

**解决方案**:
```python
# 使用 openpyxl 的 read_only 模式
from openpyxl import load_workbook

wb = load_workbook('large.xlsx', read_only=True)
ws = wb.active

for row in ws.iter_rows(values_only=True):
    # 逐行处理
    process_row(row)
```

### 问题 6: 权限和文件系统问题

#### 错误: `权限被拒绝`

**错误信息**:
```
PermissionError: [Errno 13] Permission denied: 'output.xlsx'
```

**原因**: 文件被占用或权限不足

**解决方案**:
```bash
# 检查文件权限
ls -l output.xlsx

# 修改权限
chmod 644 output.xlsx

# 检查文件是否被其他程序占用
# Windows: 使用 Process Explorer 查看锁定进程
# Linux: 使用 lsof
lsof | grep output.xlsx
```

#### 错误: `磁盘空间不足`

**错误信息**:
```
OSError: [Errno 28] No space left on device
```

**解决方案**:
```bash
# 检查磁盘空间
df -h

# 清理临时文件
rm -rf /tmp/excel_import_temp_*

# 清理旧备份
find backup/ -name "*.xlsx" -mtime +30 -delete
```

## 错误日志分析

### 日志位置

```
logs/import_errors.log       # 错误日志
logs/import_info.log         # 信息日志
logs/import_debug.log        # 调试日志
```

### 日志格式

```json
{
  "timestamp": "2024-01-20T10:30:00",
  "level": "ERROR",
  "row": 10,
  "field": "身份证号",
  "value": "123456",
  "error": "格式错误",
  "error_type": "ValidationError",
  "traceback": "..."
}
```

### 分析脚本

```python
import json
from collections import Counter

# 读取错误日志
with open('logs/import_errors.log', 'r') as f:
    errors = [json.loads(line) for line in f]

# 统计错误类型
error_types = Counter(e['error_type'] for e in errors)
print("错误类型分布:")
for error_type, count in error_types.most_common():
    print(f"  {error_type}: {count}")

# 统计错误字段
error_fields = Counter(e['field'] for e in errors)
print("\n错误字段分布:")
for field, count in error_fields.most_common():
    print(f"  {field}: {count}")

# 统计错误行
error_rows = [e['row'] for e in errors]
print(f"\n错误行数: {len(error_rows)}")
print(f"错误行范围: {min(error_rows)} - {max(error_rows)}")
```

## 调试技巧

### 1. 启用详细日志

```yaml
error_handling:
  verbose: true               # 详细输出
  log_level: "DEBUG"          # 日志级别
  debug_mode: true            # 调试模式
```

### 2. 测试数据集

**创建小规模测试数据**:
```python
import pandas as pd

# 从大文件中提取前 20 行作为测试数据
df = pd.read_excel('large_file.xlsx')
df.head(20).to_excel('test_data.xlsx', index=False)
```

**使用测试数据验证配置**:
```bash
# 使用测试配置
python scripts/excel_import.py test_config.yaml
```

### 3. 逐步验证

```python
# 步骤 1: 验证配置文件
import yaml
with open('import_config.yaml') as f:
    config = yaml.safe_load(f)
print("配置加载成功:", config['task_name'])

# 步骤 2: 验证源数据
import pandas as pd
df = pd.read_excel(config['source']['file_path'])
print(f"源数据行数: {len(df)}")
print(f"源数据列: {df.columns.tolist()}")

# 步骤 3: 验证字段映射
for mapping in config['field_mappings']:
    if mapping['source'] not in df.columns:
        print(f"警告: 源字段 '{mapping['source']}' 不存在")

# 步骤 4: 验证目标模板
df_target = pd.read_excel(config['target']['file_path'])
print(f"目标表行数: {len(df_target)}")
print(f"目标表列: {df_target.columns.tolist()}")
```

### 4. 使用 Python 调试器

```python
# 在脚本中插入断点
import pdb

def import_data(config):
    # ... 导入逻辑
    pdb.set_trace()  # 设置断点
    # ... 继续执行
```

## 预防措施

### 1. 数据质量检查

**导入前检查清单**:
```python
def check_data_quality(file_path):
    """检查数据质量"""
    df = pd.read_excel(file_path)

    issues = []

    # 检查空值
    null_counts = df.isnull().sum()
    for col, count in null_counts.items():
        if count > 0:
            issues.append(f"列 '{col}' 有 {count} 个空值")

    # 检查重复行
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        issues.append(f"发现 {duplicates} 条重复行")

    # 检查数据类型
    for col in df.columns:
        if df[col].dtype == 'object':
            # 检查是否应该为数字
            try:
                pd.to_numeric(df[col])
                issues.append(f"列 '{col}' 可能为数字类型但存储为文本")
            except:
                pass

    return issues

# 使用
issues = check_data_quality('source.xlsx')
for issue in issues:
    print(f"警告: {issue}")
```

### 2. 配置验证

**配置验证脚本**:
```python
import yaml
import os

def validate_config(config_path):
    """验证配置文件"""
    with open(config_path) as f:
        config = yaml.safe_load(f)

    errors = []

    # 检查必需字段
    required_fields = ['task_name', 'source', 'target', 'field_mappings']
    for field in required_fields:
        if field not in config:
            errors.append(f"缺少必需字段: {field}")

    # 检查文件路径
    if 'file_path' in config['source']:
        if not os.path.exists(config['source']['file_path']):
            errors.append(f"源文件不存在: {config['source']['file_path']}")

    if 'file_path' in config['target']:
        if not os.path.exists(config['target']['file_path']):
            errors.append(f"目标文件不存在: {config['target']['file_path']}")

    return errors

# 使用
errors = validate_config('import_config.yaml')
if errors:
    for error in errors:
        print(f"错误: {error}")
else:
    print("配置验证通过")
```

### 3. 备份验证

**验证备份文件**:
```python
import os
from datetime import datetime

def verify_backups(backup_path):
    """验证备份文件"""
    if not os.path.exists(backup_path):
        print(f"警告: 备份目录不存在: {backup_path}")
        return

    backups = [f for f in os.listdir(backup_path) if f.endswith('.xlsx')]
    print(f"找到 {len(backups)} 个备份文件")

    if backups:
        # 检查最新备份
        latest = max(backups, key=lambda f: os.path.getmtime(os.path.join(backup_path, f)))
        mtime = datetime.fromtimestamp(os.path.getmtime(os.path.join(backup_path, latest)))
        print(f"最新备份: {latest} ({mtime})")
    else:
        print("警告: 没有找到备份文件")

# 使用
verify_backups('backup/')
```

## 获取帮助

### 信息收集模板

遇到问题时，请提供以下信息:

```markdown
## 问题描述
简要描述遇到的问题

## 配置文件
```yaml
# 粘贴您的配置文件（敏感信息请删除）
```

## 错误信息
```
粘贴完整的错误堆栈
```

## 环境信息
- Python 版本:
- 操作系统:
- 依赖包版本:

## 数据规模
- 源数据行数:
- 目标表行数:
- 字段映射数量:

## 已尝试的解决方案
列出已经尝试的解决方案
```

### 常用诊断命令

```bash
# 检查 Python 环境
python --version
pip list | grep -E "openpyxl|pyyaml"

# 检查文件
ls -lh source.xlsx template.xlsx

# 检查磁盘空间
df -h

# 检查内存
free -h

# 查看错误日志
tail -n 50 logs/import_errors.log
```

## 参考资源

- [快速开始](quickstart.md) - 基础使用指南
- [最佳实践](best-practices.md) - 优化建议
- [配置示例](configuration-examples.md) - 完整配置示例

---

**文档版本**: 1.0.0
**最后更新**: 2024-01-20
