---
name: excel-table-structurer
description: 结构化整理层级型 Excel 表格（.xlsx），处理父子层级关系、向下填充、分组首行显示、筛选优化。当用户上传 Excel 文件并要求「结构化整理」「填充数据」「整理表格」「整理测试用例」「清理表格格式」时使用。
---

# Excel 表格结构化整理

## 核心概念

很多业务表格（如测试用例、项目清单、台账）是**层级结构**的：

```
A列(业务场景) → B列(测试分类) → C列(用例编号) + D/E列(信息)
                                      ↓
                                F列(操作步骤1) + G列(期望结果1)
                                F列(操作步骤2) + G列(期望结果2)
                                ...
```

处理这类表格的核心操作：

| 操作 | 说明 | 示例 |
|------|------|------|
| **fill-down** | 父层级值向下填充到所有子行 | 业务场景、测试分类每行都可见 |
| **group-header** | 组级信息仅首行显示 | 用例编号/名称仅在用例首行 |
| **fill-down-group** | 组级信息填充到所有行（便于筛选） | 测试结论向下填充，筛选 fail 可看完整步骤 |

## 使用方法

### 快速上手

```python
python3 scripts/restructure.py 输入文件.xlsx 输出文件.xlsx --spec '<JSON_SPEC>'
```

`JSON_SPEC` 定义列的层级角色。

### 分析表格结构

收到用户文件后，先读取数据确认层级关系：

1. 哪些列是父层级（A/B列），需要**fill-down**
2. 哪一列是分组键（C列，定义行组），需要**group-header**
3. 哪些列携带组级信息（H列测试结论），需要**fill-down-group**
4. 哪些列需要额外处理

### JSON_SPEC 参数说明

```jsonc
{
  "sheet": "Sheet1",                        // 工作表名称（可选，默认 Sheet1）
  "fill_down_columns": [0, 1],              // 父层级列（0-based index）→ 向下填充
  "group_key_column": 2,                    // 分组键列 → 定义行组
  "group_header_columns": [2, 3, 4],        // 组首行列 → 仅首行显示
  "fill_down_group_columns": [7],           // 组级填充列 → 所有行显示（便于筛选）
  "col_widths": {"0": 20, "1": 18},        // 列宽（可选，key=col_index, value=width）
  "freeze_panes": "A2",                    // 冻结窗格（可选，默认 A2）
  "skip_empty_rows": true                  // 跳过空行（可选，默认 true）
}
```

### 常见场景

**场景一：测试用例整理（本次案例）**

```
A=业务场景, B=测试分类 → fill-down
C=用例编号, D=用例名称, E=前提条件 → group-header（仅有首行）
H=测试结论 → fill-down-group（复制到所有行便于筛选）
```

```json
{
  "fill_down_columns": [0, 1],
  "group_key_column": 2,
  "group_header_columns": [2, 3, 4],
  "fill_down_group_columns": [7],
  "col_widths": {"0": 20, "1": 18, "2": 14, "3": 35, "4": 40, "5": 55, "6": 45, "7": 12, "8": 35}
}
```

**场景二：项目任务清单**

```
A=项目名称 → fill-down
B=负责人, C=截止日期 → group-header（仅有首行）
D=任务状态 → fill-down-group（所有行可见，便于筛选）
E=任务事项, F=备注 → 每行独有
```

```json
{
  "fill_down_columns": [0],
  "group_key_column": 1,
  "group_header_columns": [1, 2],
  "fill_down_group_columns": [3]
}
```

**场景三：台账明细表**

```
A=客户名称 → fill-down
B=合同编号, C=合同金额 → group-header
D=开票状态 → fill-down-group
E=发票号, F=开票日期 → 每行独有
```

```json
{
  "fill_down_columns": [0],
  "group_key_column": 1,
  "group_header_columns": [1, 2],
  "fill_down_group_columns": [3]
}
```

## 输出格式

- 首行冻结 + 自动筛选
- 组交替底色（白/浅灰）
- 结论列自动着色（pass=绿, fail=红, 无法测试=黄）
- fail 行左侧红色边框高亮

## 输出说明

运行后脚本返回统计信息：

```json
{"total_rows": 562, "group_count": 119}
```
- `total_rows` = 数据行数（不含表头）
- `group_count` = 分组数量（如测试用例数）

## 使用流程

1. 用户发送 Excel 文件并说明需求
2. 读取文件，分析列层级关系
3. 构造 JSON_SPEC
4. 运行 `restructure.py`
5. 验证输出，将结果文件发送给用户
