# 高级功能

## 多源文件/目录数据源导入

当有多个源文件需要合并导入时（例如：多个班级的成绩单、多个部门的数据表），技能提供了三种方式：

### 方式1：目录自动遍历

**最简单的方式**，指定一个目录，脚本自动处理所有 Excel 文件：

```yaml
source:
  directory_path: "input/"          # 指定目录
  file_pattern: "*.xlsx"            # 可选：文件过滤模式
  sheet_name: "Sheet1"
  header_row: 1
  key_field: "学籍号码"
```

**特性**：
- ✅ 自动遍历目录中的所有 `.xlsx` 文件
- ✅ 支持通配符过滤（如 `*成绩*.xlsx`、`班级*.xlsx`）
- ✅ 按文件名排序后依次处理（保证可预测性）
- ✅ 后处理的文件会覆盖前面的数据（相同关键字段）

### 方式2：多源文件显式配置

**最灵活的方式**，精确控制每个文件的配置：

```yaml
sources:  # 注意使用复数 sources
  - file_path: "input/701_702班.xlsx"
    sheet_name: "Sheet1"
    header_row: 1
    key_field: "学籍号码"
    # 每个源文件可以有独立的字段映射
    field_mappings:
      - source: "思品"
        target: "思品"

  - file_path: "input/703_705班.xlsx"
    sheet_name: "Sheet1"
    header_row: 1
    key_field: "学籍号码"
    field_mappings:
      - source: "道德与法治"
        target: "思品"  # 不同源文件可以有不同的字段名
```

**特性**：
- ✅ 完全控制导入顺序
- ✅ 每个源文件可以有独立的字段映射
- ✅ 适合处理格式不完全一致的多个文件

### 方式3：混合配置

结合目录和显式配置：

```yaml
sources:
  # 先导入指定的文件
  - file_path: "input/特殊文件.xlsx"
    sheet_name: "特殊Sheet"

  # 再导入整个目录
  - directory_path: "input/其他班级/"
    file_pattern: "*.xlsx"
```

**数据合并规则**：
1. 所有源文件的数据根据 `key_field`（关键字段）进行匹配
2. 如果多个源文件包含相同的关键字段值，**后处理的文件会覆盖前面的**
3. 如果某个源文件缺少某条记录，会从其他源文件中查找
4. 最终将所有有效数据合并到目标文件

### 实际案例

**场景**：七年级11个班级的成绩分布在2个文件中
- `2026,7年级登分册(2).xlsx` 包含：701、702、704、707班
- `2026.7年级登分册1.xlsx` 包含：703、705、706、708、709、710、711班

**配置方案**：

```yaml
task_name: "七年级道历成绩导入"

source:
  directory_path: "input/"
  file_pattern: "*.xlsx"
  sheet_name: "Sheet1"
  header_row: 1
  key_field: "学籍号码"

target:
  file_path: "七年级道历成绩汇总 .xlsx"
  sheet_name: "Sheet1"
  header_row: 1
  data_start_row: 2
  output_path: "output/七年级道历成绩汇总_已导入.xlsx"

field_mappings:
  - source: "思品"
    target: "思品"
  - source: "历史"
    target: "历史"
```

**结果**：自动从2个文件中读取数据，合并后导入到模板，508名学生中502人成功导入（98.8%覆盖率）。

---

## 处理合并单元格

技能会自动识别和处理模板中的合并单元格，确保导入数据时不破坏原有格式。

**配置**:
```yaml
options:
  preserve_formatting: true      # 保持格式（包括合并单元格）
  skip_merged_cells: false       # 不跳过合并单元格
```

---

## 多字段匹配

当单个字段无法唯一确定记录时，可以使用多字段匹配。

**配置**:
```yaml
source:
  key_fields:                    # 多字段匹配
    - "身份证号"
    - "姓名"
```

---

## 自定义验证规则

除了内置验证规则，还可以定义自定义验证规则。

**配置**:
```yaml
validations:
  - field: "年龄"
    rules:
      - type: "range"
        min: 18
        max: 65
        message: "年龄必须在18-65岁之间"
```

---

## 数据转换

支持多种数据转换函数，也可以自定义转换逻辑。

**配置**:
```yaml
field_mappings:
  - source: "入职日期"
    target: "参加工作时间"
    transform: "date"
    transform_params:
      input_format: "%Y-%m-%d"
      output_format: "%Y年%m月%d日"
```

---

## 内置转换函数

- `strip`: 去除首尾空格
- `upper`: 转大写
- `lower`: 转小写
- `title`: 标题格式（首字母大写）
- `date`: 日期格式转换

---

## 内置验证规则

- `required`: 必填字段
- `id_card`: 身份证号格式验证
- `phone`: 手机号格式验证
- `email`: 邮箱格式验证

---

## 中文支持

### 字体配置

技能使用 `chinese-font-solution` 确保中文字体正确显示。

**默认字体**: 微软雅黑
**后备字体**: 宋体、黑体、Arial Unicode MS

**自定义字体配置**:
```yaml
options:
  font_settings:
    default_font: "微软雅黑"
    fallback_fonts: ["宋体", "黑体"]
    font_size: 11
```

---

## 关键配置说明

### 字段映射 (field_mappings)

```yaml
field_mappings:
  - source: "源字段名"           # 源数据表的字段名
    target: "目标字段名"          # 模板表的字段名
    required: true               # 是否必填
    default: "默认值"            # 默认值（可选）
    transform: "strip"           # 数据转换函数（可选）
    validate: "id_card"          # 验证规则（可选）
```

### 错误处理配置

```yaml
error_handling:
  backup: true                   # 自动备份
  backup_path: "backup/"         # 备份路径
  stop_on_error: false           # 遇到错误是否停止
  log_errors: true               # 记录错误日志
  error_log_path: "logs/import_errors.log"
```
