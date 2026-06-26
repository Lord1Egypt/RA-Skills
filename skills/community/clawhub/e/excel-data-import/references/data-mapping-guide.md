# Excel 数据导入 - 数据映射配置详解

## 概述

数据映射是 Excel 数据导入的核心功能，它定义了源数据字段到目标表字段的对应关系、转换规则和验证逻辑。本指南详细说明如何配置数据映射。

## 基本映射

### 简单字段映射

最基本的映射配置：

```yaml
field_mappings:
  - source: "源字段名"
    target: "目标字段名"
```

**示例**：
```yaml
field_mappings:
  - source: "姓名"
    target: "员工姓名"
  - source: "年龄"
    target: "年龄"
  - source: "部门"
    target: "所属部门"
```

## 必填字段

### 配置必填字段

使用 `required` 标记必填字段：

```yaml
field_mappings:
  - source: "身份证号"
    target: "身份证号码"
    required: true              # 必填
  - source: "姓名"
    target: "员工姓名"
    required: true
  - source: "年龄"
    target: "年龄"
    required: false             # 可选（默认为 false）
```

**效果**：
- 如果必填字段为空，导入会报错并跳过该记录
- 错误日志会记录缺失的必填字段

## 默认值

### 为空值设置默认值

```yaml
field_mappings:
  - source: "年龄"
    target: "年龄"
    default: "18"               # 空值时使用默认值
  - source: "部门"
    target: "所属部门"
    default: "待定"
  - source: "入职日期"
    target: "参加工作时间"
    default: "2024-01-01"
```

**优先级**：源数据值 > 默认值 > 空

## 数据转换

### 内置转换函数

#### 1. strip - 去除空格

```yaml
field_mappings:
  - source: "姓名"
    target: "员工姓名"
    transform: "strip"          # 去除前后空格
```

**适用场景**：
- 用户手动输入的数据
- 从其他系统导出的数据
- OCR 识别的数据

#### 2. upper/lower - 大小写转换

```yaml
field_mappings:
  - source: "email"
    target: "邮箱"
    transform: "lower"          # 转小写

  - source: "country_code"
    target: "国家代码"
    transform: "upper"          # 转大写
```

#### 3. title - 标题格式

```yaml
field_mappings:
  - source: "product_name"
    target: "产品名称"
    transform: "title"          # 首字母大写
```

**示例**：
- 输入: "apple iphone"
- 输出: "Apple Iphone"

#### 4. date - 日期格式转换

```yaml
field_mappings:
  - source: "入职日期"
    target: "参加工作时间"
    transform: "date"
    transform_params:
      input_format: "%Y-%m-%d"
      output_format: "%Y年%m月%d日"
```

**常见日期格式**：
```yaml
# 格式1: 2024-01-20
input_format: "%Y-%m-%d"

# 格式2: 2024/01/20
input_format: "%Y/%m/%d"

# 格式3: 20-01-2024
input_format: "%d-%m-%Y"

# 格式4: January 20, 2024
input_format: "%B %d, %Y"
```

#### 5. float/int - 数值类型转换

```yaml
field_mappings:
  - source: "价格"
    target: "单价"
    transform: "float"          # 转浮点数

  - source: "数量"
    target: "库存数量"
    transform: "int"            # 转整数
```

### 自定义转换函数

**在脚本中添加**：

```python
def custom_transform(value, params):
    """自定义转换函数"""
    # 示例: 手机号格式化
    if len(value) == 11:
        return f"{value[:3]}-{value[3:7]}-{value[7:]}"
    return value

# 在配置中使用
field_mappings:
  - source: "手机号"
    target: "联系电话"
    transform: "custom_phone_format"
```

## 数据验证

### 内置验证规则

#### 1. required - 必填验证

```yaml
field_mappings:
  - source: "身份证号"
    target: "身份证号码"
    validate: "required"
```

#### 2. not_empty - 非空验证

```yaml
field_mappings:
  - source: "姓名"
    target: "员工姓名"
    validate: "not_empty"
```

**区别**：
- `required`: 字段必须存在且有值
- `not_empty`: 值不能为空字符串或 None

#### 3. id_card - 身份证号验证

```yaml
field_mappings:
  - source: "身份证号"
    target: "身份证号码"
    validate: "id_card"
```

**验证规则**：
- 15位或18位
- 最后一位可以是 X（18位）
- 格式正确性检查

#### 4. phone - 手机号验证

```yaml
field_mappings:
  - source: "手机号"
    target: "联系电话"
    validate: "phone"
```

**验证规则**：
- 11位数字
- 以1开头
- 符合手机号段规则

#### 5. email - 邮箱验证

```yaml
field_mappings:
  - source: "email"
    target: "邮箱地址"
    validate: "email"
```

**验证规则**：
- 标准邮箱格式
- 包含 @ 符号
- 域名部分有效

#### 6. numeric - 数值验证

```yaml
field_mappings:
  - source: "年龄"
    target: "年龄"
    validate: "numeric"
```

#### 7. range - 范围验证

```yaml
field_mappings:
  - source: "年龄"
    target: "年龄"
    validate: "range"
    validate_params:
      min: 18
      max: 65
      message: "年龄必须在18-65岁之间"
```

#### 8. regex - 正则表达式验证

```yaml
field_mappings:
  - source: "邮政编码"
    target: "邮编"
    validate: "regex"
    validate_params:
      pattern: "^\\d{6}$"
      message: "邮政编码必须是6位数字"
```

### 复合验证

**同时应用多个验证规则**：

```yaml
field_mappings:
  - source: "手机号"
    target: "联系电话"
    transform: "strip"
    validate:
      - "required"
      - "phone"
```

## 高级映射场景

### 场景1: 字段合并

**将多个源字段合并为一个目标字段**：

```yaml
field_mappings:
  - source: ["姓", "名"]
    target: "姓名"
    transform: "concat"
    transform_params:
      separator: ""
```

**效果**：
- 源数据: 姓="张", 名="三"
- 目标: 姓名="张三"

### 场景2: 字段拆分

**将一个源字段拆分为多个目标字段**：

```yaml
field_mappings:
  - source: "姓名"
    target: "姓"
    transform: "split"
    transform_params:
      index: 0              # 取第一部分

  - source: "姓名"
    target: "名"
    transform: "split"
    transform_params:
      index: 1              # 取第二部分
```

### 场景3: 条件映射

**根据条件选择不同的值**：

```yaml
field_mappings:
  - source: "年龄"
    target: "年龄段"
    transform: "conditional"
    transform_params:
      rules:
        - condition: "value < 18"
          value: "未成年"
        - condition: "value >= 18 and value < 60"
          value: "成年"
        - condition: "value >= 60"
          value: "老年"
        - default: "未知"
```

### 场景4: 查找表映射

**使用查找表进行值映射**：

```yaml
field_mappings:
  - source: "性别"
    target: "性别代码"
    transform: "lookup"
    transform_params:
      lookup_table:
        "男": "M"
        "女": "F"
        "未知": "U"
```

### 场景5: 多字段验证

**验证多个字段的组合**：

```yaml
field_mappings:
  - source: "密码"
    target: "密码"
    validate: "custom"
    validate_params:
      rule: "confirm_password"
      confirm_field: "确认密码"
```

**自定义验证逻辑**：
```python
def validate_confirm_password(value, params):
    """验证两次密码是否一致"""
    confirm_value = get_field_value(params['confirm_field'])
    return value == confirm_value
```

## 映射配置最佳实践

### 1. 分层配置

**将映射配置分离到独立文件**：

**主配置文件** (`import_config.yaml`):
```yaml
task_name: "人员信息导入"

source:
  file_path: "data/source.xlsx"
  ...

target:
  file_path: "templates/template.xlsx"
  ...

# 引用外部映射配置
field_mappings_file: "configs/field_mappings.yaml"
```

**映射配置文件** (`configs/field_mappings.yaml`):
```yaml
field_mappings:
  - source: "姓名"
    target: "员工姓名"
  - source: "身份证号"
    target: "身份证号码"
```

### 2. 配置复用

**使用模板避免重复**：

**基础模板** (`field_mappings_template.yaml`):
```yaml
basic_mappings: &basic_mappings
  - source: "姓名"
    target: "员工姓名"
    required: true
  - source: "身份证号"
    target: "身份证号码"
    required: true

contact_mappings: &contact_mappings
  - source: "手机号"
    target: "联系电话"
    validate: "phone"
  - source: "邮箱"
    target: "邮箱地址"
    validate: "email"
```

**使用模板** (`import_config.yaml`):
```yaml
field_mappings:
  <<: *basic_mappings
  <<: *contact_mappings
```

### 3. 环境特定配置

**开发/生产环境分离**：

**开发环境** (`import_config_dev.yaml`):
```yaml
field_mappings:
  - source: "姓名"
    target: "员工姓名"
    validate: false          # 开发环境不验证
```

**生产环境** (`import_config_prod.yaml`):
```yaml
field_mappings:
  - source: "姓名"
    target: "员工姓名"
    validate: "not_empty"    # 生产环境验证
```

## 映射配置验证

### 验证脚本

**检查映射配置的正确性**：

```python
def validate_field_mappings(mappings, source_columns, target_columns):
    """验证字段映射配置"""
    errors = []

    for mapping in mappings:
        source = mapping['source']
        target = mapping['target']

        # 检查源字段是否存在
        if source not in source_columns:
            errors.append(f"源字段 '{source}' 不存在")

        # 检查目标字段是否存在
        if target not in target_columns:
            errors.append(f"目标字段 '{target}' 不存在")

        # 检查转换函数
        if 'transform' in mapping:
            if not is_valid_transform(mapping['transform']):
                errors.append(f"转换函数 '{mapping['transform']}' 无效")

        # 检查验证规则
        if 'validate' in mapping:
            if not is_valid_validation(mapping['validate']):
                errors.append(f"验证规则 '{mapping['validate']}' 无效")

    return errors

# 使用
source_columns = pd.read_excel('source.xlsx').columns.tolist()
target_columns = pd.read_excel('template.xlsx').columns.tolist()
mappings = load_yaml('import_config.yaml')['field_mappings']

errors = validate_field_mappings(mappings, source_columns, target_columns)
for error in errors:
    print(f"错误: {error}")
```

## 调试映射配置

### 1. 映射预览

**预览映射结果**：

```python
def preview_mapping(source_file, target_file, mappings):
    """预览映射结果（前5行）"""
    df_source = pd.read_excel(source_file)
    df_target = pd.read_excel(target_file)

    print("=== 映射预览 ===")
    for i, row in df_source.head(5).iterrows():
        print(f"\n行 {i + 1}:")
        for mapping in mappings:
            source_value = row[mapping['source']]
            print(f"  {mapping['source']} → {mapping['target']}: {source_value}")

# 使用
preview_mapping('source.xlsx', 'template.xlsx', mappings)
```

### 2. 映射测试

**测试映射配置**：

```python
def test_mapping(mappings, test_data):
    """测试映射配置"""
    print("=== 映射测试 ===")

    for mapping in mappings:
        source_field = mapping['source']
        target_field = mapping['target']

        # 测试转换
        if 'transform' in mapping:
            test_value = test_data.get(source_field)
            transformed = apply_transform(test_value, mapping['transform'])
            print(f"{source_field} → {target_field}: {test_value} → {transformed}")

        # 测试验证
        if 'validate' in mapping:
            test_value = test_data.get(source_field)
            is_valid = apply_validation(test_value, mapping['validate'])
            status = "✓" if is_valid else "✗"
            print(f"{status} {source_field} 验证: {test_value}")

# 使用
test_data = {
    "姓名": "张三",
    "身份证号": "110101199001011234",
    "年龄": 25
}
test_mapping(mappings, test_data)
```

## 性能优化

### 1. 减少不必要的转换

```yaml
# ❌ 避免不必要的转换
field_mappings:
  - source: "年龄"
    target: "年龄"
    transform: "strip"        # 数值类型不需要 strip
    transform: "int"

# ✅ 只使用必要的转换
field_mappings:
  - source: "年龄"
    target: "年龄"
    transform: "int"
```

### 2. 延迟验证

```yaml
# 先转换，后验证（推荐）
field_mappings:
  - source: "手机号"
    target: "联系电话"
    transform: "strip"        # 先去除空格
    validate: "phone"         # 再验证格式
```

### 3. 批量处理

**对大量字段使用批量映射**：

```python
# 自动生成映射配置
def auto_generate_mappings(source_file, target_file):
    """自动生成字段映射"""
    source_columns = pd.read_excel(source_file, nrows=0).columns
    target_columns = pd.read_excel(target_file, nrows=0).columns

    mappings = []
    for source_col in source_columns:
        # 自动匹配相似字段名
        for target_col in target_columns:
            if similarity(source_col, target_col) > 0.8:
                mappings.append({
                    'source': source_col,
                    'target': target_col
                })
                break

    return mappings
```

## 参考资源

- [快速开始](quickstart.md) - 基础使用指南
- [配置示例](configuration-examples.md) - 完整配置示例
- [最佳实践](best-practices.md) - 优化建议
- [故障排除](troubleshooting.md) - 问题解决方案

---

**文档版本**: 1.0.0
**最后更新**: 2024-01-20
