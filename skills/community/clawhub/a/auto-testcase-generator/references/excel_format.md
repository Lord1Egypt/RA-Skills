# Excel 输出格式规范

## 工作表结构

所有测试用例输出到单个工作表中，工作表名称为"测试用例（按模块分组）"。

## 标准列定义

| 列序 | 列名 | 必填 | 说明 |
|------|------|------|------|
| A | 用例编号 | ✅ | 全局连续编号，格式 `TC-001`、`TC-002`...，模块分隔行不占编号 |
| B | 优先级 | ✅ | P0（冒烟/核心路径）、P1（重要功能）、P2（一般场景）、P3（低频/锦上添花） |
| C | 测试类型 | ✅ | 功能 / 异常 / 边界 / 集成 / 性能 / 安全 / 端到端（与七维度对应） |
| D | 模块 | ✅ | 功能模块名称 |
| E | 场景 | ✅ | 测试场景描述（含视觉来源说明） |
| F | 测试点 | ✅ | 具体的测试验证点 |
| G | 操作步骤 | ✅ | 详细的操作步骤（多步骤使用 chr(10) 换行） |
| H | 预期结果 | ✅ | 预期的正确行为和输出 |
| I | 测试结果 | ❌ | 留空，供测试人员填写 |
| J | 用例生成依据 | ✅ | 关联的需求来源（章节引用或规则编号） |
| K | 图像来源 | ✅ | 关联的图片/流程图来源（无则填"无"） |
| L | 截图 | ❌ | 留空，供测试人员贴图 |

### 优先级定义

| 优先级 | 含义 | 典型场景 | 建议占比 |
|--------|------|---------|---------|
| **P0** | 冒烟级 — 不通过则阻塞发布 | 核心业务主路径、登录/支付等关键功能 | 10~15% |
| **P1** | 核心级 — 重要功能必测 | 主要分支路径、关键异常处理、重要边界值 | 30~40% |
| **P2** | 一般级 — 正常回归覆盖 | 次要场景、非关键异常、普通边界 | 30~40% |
| **P3** | 低优先级 — 时间允许时执行 | 极端边界、低频操作、锦上添花场景 | 10~20% |

### 优先级分配规则

1. **P0**：核心业务主流程的正向验证用例，阻塞级异常处理
2. **P1**：重要分支路径、关键边界值、核心模块的异常处理
3. **P2**：一般功能验证、非关键异常处理、集成测试
4. **P3**：极端边界、性能压测、低频场景、安全探索性测试

## 模块分组规则

### 分组方式

按功能模块分组，模块内用例按以下测试类型排序（对应"测试类型"列）：

1. 功能测试（功能）
2. 异常处理（异常）
3. 边界值测试（边界）
4. 集成测试（集成）
5. 性能测试（性能）
6. 安全测试（安全）

同一测试类型内，按优先级 P0 → P1 → P2 → P3 排序。

### 模块分隔行

在每个模块的第一条用例前插入分隔行：

- 分隔行格式：第一列填写 `【模块名称】`，其余列为空
- **注意**：不使用 `=` 开头（避免 Excel 公式解析）
- 不使用 `=== 模块名 ===` 格式

### 分隔行样式

- 背景色：绿色（RGB: 70, 130, 80 或类似深绿色）
- 字体：白色、粗体
- 其余列空白

## 表头样式

- 背景色：蓝色（RGB: 68, 114, 196 或类似深蓝色）
- 字体：白色、粗体
- 冻结首行

## 数据格式处理

### 换行符

Excel 单元格内换行必须使用真实换行符 `chr(10)`，并设置单元格 `wrap_text=True`。

```python
# 正确写法
cell.value = "步骤1：打开页面" + chr(10) + "步骤2：点击按钮"
cell.alignment = Alignment(wrap_text=True)

# 错误写法（会显示为文字 \n）
cell.value = "步骤1：打开页面\n步骤2：点击按钮"
```

### 用例编号

全局连续编号，格式 `TC-001`、`TC-002`...，模块分隔行不占编号：

```python
# 确保用例编号为字符串类型，3 位数字补零
df['用例编号'] = [f'TC-{i:03d}' for i in range(1, len(df) + 1)]
df['用例编号'] = df['用例编号'].astype(str)
```

### 行高

设置合理的行高以显示多行内容：

```python
# 根据内容行数自适应行高
line_count = str(cell.value).count(chr(10)) + 1
ws.row_dimensions[row].height = max(15, line_count * 15)
```

## 实现代码参考

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# 标准列定义（12 列）
columns = [
    '用例编号', '优先级', '测试类型', '模块', '场景', '测试点',
    '操作步骤', '预期结果', '测试结果', '用例生成依据', '图像来源', '截图'
]

# 优先级条件着色
priority_fills = {
    'P0': PatternFill(start_color='FF4444', end_color='FF4444', fill_type='solid'),  # 红色
    'P1': PatternFill(start_color='FF9800', end_color='FF9800', fill_type='solid'),  # 橙色
    'P2': PatternFill(start_color='4CAF50', end_color='4CAF50', fill_type='solid'),  # 绿色
    'P3': PatternFill(start_color='9E9E9E', end_color='9E9E9E', fill_type='solid'),  # 灰色
}
priority_font = Font(name='微软雅黑', size=11, bold=True, color='FFFFFF')

# 按模块分组测试用例
module_groups = {}
for tc in all_testcases:
    module = tc.get('模块', '未分类模块')
    if module not in module_groups:
        module_groups[module] = []
    module_groups[module].append(tc)

# 全局连续编号
tc_counter = 1

# 按模块顺序组织并添加分隔行
ordered_rows = []
for module_name in module_order:
    if module_name in module_groups:
        # 添加模块分隔行（不占编号）
        separator = {col: '' for col in columns}
        separator['模块'] = f'【{module_name}】'
        separator['_is_separator'] = True
        ordered_rows.append(separator)
        # 添加该模块的所有用例（分配编号）
        for tc in module_groups[module_name]:
            tc['用例编号'] = f'TC-{tc_counter:03d}'
            tc_counter += 1
            ordered_rows.append(tc)

# 写入 Excel
wb = openpyxl.Workbook()
ws = wb.active
ws.title = '测试用例（按模块分组）'

# 表头样式
header_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
header_font = Font(name='微软雅黑', size=11, bold=True, color='FFFFFF')

# 分隔行样式
separator_fill = PatternFill(start_color='468250', end_color='468250', fill_type='solid')
separator_font = Font(name='微软雅黑', size=11, bold=True, color='FFFFFF')

# 写入表头（12 列）
for col_idx, col_name in enumerate(columns, 1):
    cell = ws.cell(row=1, column=col_idx, value=col_name)
    cell.fill = header_fill
    cell.font = header_font
    cell.alignment = Alignment(horizontal='center', vertical='center')

# 冻结首行
ws.freeze_panes = 'A2'

# 写入数据行
for row_idx, row_data in enumerate(ordered_rows, 2):
    is_separator = row_data.pop('_is_separator', False)
    for col_idx, col_name in enumerate(columns, 1):
        cell = ws.cell(row=row_idx, column=col_idx, value=row_data.get(col_name, ''))
        cell.alignment = Alignment(wrap_text=True, vertical='top')
        if is_separator:
            cell.fill = separator_fill
            cell.font = separator_font
        # 优先级列条件着色
        elif col_name == '优先级' and cell.value in priority_fills:
            cell.fill = priority_fills[cell.value]
            cell.font = priority_font
            cell.alignment = Alignment(horizontal='center', vertical='center')
        # 用例编号列居中
        elif col_name == '用例编号':
            cell.alignment = Alignment(horizontal='center', vertical='center')
        # 测试类型列居中
        elif col_name == '测试类型':
            cell.alignment = Alignment(horizontal='center', vertical='center')

wb.save(output_path)
```

## 与传统多工作表格式的对比

| 特性 | 单工作表按模块分组 | 传统多工作表按类型分组 |
|------|-------------------|---------------------|
| **工作表数量** | 1个 | 5-6个 |
| **组织方式** | 按功能模块分组 | 按测试类型分组 |
| **查看便利性** | ✅ 一次查看所有用例 | ❌ 需要切换工作表 |
| **模块关联性** | ✅ 同模块用例聚集 | ❌ 同模块用例分散 |
| **打印友好** | ✅ 单页打印 | ❌ 多页分别打印 |
| **维护成本** | ✅ 低 | ❌ 高（多表同步） |
