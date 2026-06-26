---
name: bitable-formula-generator
description: 飞书多维表格字段公式生成器。通过导出Excel分析字段结构，利用Excel公式逻辑生成多维表格兼容公式，并写入多维表格字段。
---

# 飞书多维表格字段公式生成器

## 目的
根据用户描述的业务逻辑，自动生成可直接用于飞书多维表格公式字段的公式。
公式语法与 Excel 类似，但只使用多维表格支持的函数，且用**字段名**（而非列字母）引用数据。

---

## 完整工作流程

### 第 1 步：获取多维表格结构

优先通过以下方式获取字段信息：
1. **API 自动获取（推荐）**：使用 `scripts/feishu-bitable-api.js` 脚本自动列出表和字段。
2. **导出为 Excel**：用户导出多维表格为 `.xlsx`，读取表头行获取字段名和数据类型。
3. **用户直接提供**：用户列出字段名及数据类型。

#### 使用 API 脚本获取字段信息

脚本路径：`scripts/feishu-bitable-api.js`

**前置条件**：需设置环境变量 `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET`。

**列出所有表**：
```bash
node scripts/feishu-bitable-api.js list-tables <app_token>
```

**列出指定表的所有字段**（公式字段会显示当前公式预览，`⚠️ 0` 表示公式未设置）：
```bash
node scripts/feishu-bitable-api.js list-fields <app_token> <table_name>
```

**查看指定字段的完整 property**（公式字段显示完整公式，单选字段显示所有选项）：
```bash
node scripts/feishu-bitable-api.js get-field <app_token> <table_name> <field_name>
```

> `app_token` 可从多维表格 URL 中获取，格式如 `https://xxx.feishu.cn/base/<app_token>`。

从 Excel 读取字段信息时，提取第 1 行（表头）作为字段名列表。

---

### 第 1b 步：确认依赖字段的公式正确性（重要！）

**如果目标公式依赖其他公式字段（中间字段），必须先确认中间字段的公式是否正确，再继续。**

```bash
# 查看中间字段的当前公式
node scripts/feishu-bitable-api.js get-field <app_token> <table_name> <中间字段名>
```

⚠️ 常见陷阱：中间字段可能是硬编码的 `0` 或空公式，会导致最终结果全为 0。

---

### 第 2 步：生成公式（Excel 风格 → 多维表格风格）

#### 2a. 先构造 Excel 公式

借鉴 `excel-formula-generator` 技能的公式模式，基于字段映射（A列=字段1, B列=字段2 ...）构造 Excel 公式原型。

#### 2b. 替换列字母为字段名

将公式中的列引用（如 `B2`、`C2`、`B:B`）替换为对应字段名：

| Excel 引用 | 多维表格写法 |
|---|---|
| `B2` | `字段名` |
| `C2` | `另一个字段名` |
| `"固定文本"` | 保持不变 |
| `数字常量` | 保持不变 |

示例：
- Excel: `=(B2-C2)/B2`  
- 多维表格: `(销售额-成本)/销售额`

#### 2c. 函数替换规则（仅使用多维表格支持的函数）

不使用 Excel 专有函数，严格只用多维表格支持的函数（见下方函数列表）。

**常见替换：**
| Excel 函数 | 多维表格替代 |
|---|---|
| `VLOOKUP` | `LOOKUP` |
| `XLOOKUP` | `LOOKUP` |
| `CONCAT` / `&` | `CONCATENATE` |
| `SUMPRODUCT` | 无直接等价，用 `SUM`+`FILTER` 组合 |
| `COUNTIFS` | `COUNTIF`（单条件）|
| `AVERAGEIF/AVERAGEIFS` | 用 `SUM`/`COUNTA` 手工计算 |
| `STDEV` | 不支持，提示用户 |
| `PERCENTRANK` | 不支持，提示用户 |
| `XLOOKUP/INDEX/MATCH` | `LOOKUP` |

---

### 第 3 步：将公式写入多维表格

#### 方法 A：API 脚本写入（推荐）
使用 `scripts/feishu-bitable-api.js` 脚本直接写入公式字段，支持自动创建新字段或更新已有字段：

```bash
node scripts/feishu-bitable-api.js set-formula <app_token> <table_name> <field_name> <formula> [formatter]
```

**参数说明：**
- `app_token`：多维表格的 app_token
- `table_name`：表名（支持中文，如「客户档案表」）
- `field_name`：目标字段名（如「热爱得分」）
- `formula`：公式内容（建议用引号包裹）
- `formatter`（可选）：数字格式，默认 `0.0`（一位小数）。可选 `""`（整数）、`0.00`（两位小数）、`#,##0.0`（千分位）

**示例：**
```bash
# 写入公式到「热爱得分」字段
node scripts/feishu-bitable-api.js set-formula MIASw72fgiRMCxkyqhtcuSwVnPf 客户档案表 "热爱得分" "REGEXEXTRACT(时间投入, \"（([0-9]+)分）\")"

# 写入公式，保留两位小数
node scripts/feishu-bitable-api.js set-formula MIASw72fgiRMCxkyqhtcuSwVnPf 客户档案表 "毛利率" "(销售额-成本)/销售额" "0.00"
```

> ⚠️ **公式含 `<`、`>`、`|`、`&` 等特殊字符时，不能通过命令行传入**，PowerShell 会截断参数导致 `FormulaFieldPropertyError`。请改用方法 C（脚本文件 PUT 写入）。

> 脚本会自动：通过环境变量获取 access_token → 通过表名查找 table_id → 检查字段是否存在 → 创建或更新字段。

#### 方法 B：手动粘贴
直接输出公式，让用户复制到多维表格公式字段。

#### 方法 C：直接调用 API
使用飞书开放平台 API 写入公式字段（`PUT` 方法）：

```
PUT https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields/{field_id}
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "field_name": "目标字段名",
  "type": 20,
  "property": {
    "formatter": "0.0",
    "formula_expression": "={公式内容}",
    "type": {
      "data_type": 2,
      "ui_property": { "formatter": "0.0" },
      "ui_type": "Number"
    }
  }
}
```
> - 字段类型 `20` 对应公式字段（Formula）
> - 更新已有字段用 `PUT`，创建新字段用 `POST`
> - `data_type: 2` 表示数字类型

---

## 多维表格支持的函数列表

### 日期函数
`DATE` `DATEDIF` `DAY` `DAYS` `EDATE` `EOMONTH` `HOUR` `MINUTE` `SECOND` `MONTH` `NETWORKDAYS` `NOW` `TODAY` `WEEKDAY` `WEEKNUM` `WORKDAY` `YEAR` `DURATION` `TODATE`

### 逻辑函数
`AND` `CONTAIN` `FALSE` `IF` `IFBLANK` `IFERROR` `IFS` `ISBLANK` `ISERROR` `ISNUMBER` `ISNULL` `MAP` `NOT` `OR` `RANK` `RECORD_ID` `SWITCH` `TRUE` `CONTAINSALL` `CONTAINSONLY` `RANDOMBETWEEN` `RANDOMITEM`

### 文本函数
`CHAR` `CONCATENATE` `CONTAINTEXT` `FIND` `HYPERLINK` `LEFT` `RIGHT` `MID` `LEN` `LOWER` `UPPER` `REPLACE` `SUBSTITUTE` `TEXT` `SPLIT` `TRIM` `ENCODEURL` `FORMAT` `REGEXEXTRACT` `REGEXEXTRACTALL` `REGEXMATCH` `REGEXREPLACE`

### 数字函数
`ABS` `ACOS` `ASIN` `ATAN` `ACOSH` `ASINH` `ATANH` `ATAN2` `AVERAGE` `CEILING` `COS` `SIN` `TAN` `COSH` `SINH` `TANH` `COUNTA` `COUNTIF` `FLOOR` `INT` `ISODD` `MAX` `MIN` `MEDIAN` `MOD` `PI` `POWER` `QUOTIENT` `ROUND` `ROUNDDOWN` `ROUNDUP` `SUM` `SUMIF` `VALUE` `SEQUENCE`

### 位置函数
`DISTANCE`

### 列表/查找函数
`ARRAYJOIN` `FILTER` `FIRST` `LAST` `LIST` `LISTCOMBINE` `LOOKUP` `NTH` `SORT` `SORTBY` `UNIQUE`

---

## 公式语法要点

1. **字段引用**：直接用字段名，如 `销售额`、`时间投入`，字段名有空格也直接使用。
2. **函数调用**：与 Excel 一致，如 `IF(状态="完成", 1, 0)`。
3. **字符串**：用英文双引号 `""`。
4. **四则运算**：`+` `-` `*` `/` `^`。
5. **比较运算**：`=` `<>` `>` `<` `>=` `<=`。
6. **不支持数组公式**（Ctrl+Shift+Enter 那种）。

---

## 示例交互

### 示例 1：计算毛利率
**用户：** 字段有"销售额"和"成本"，要计算毛利率

**输出：**
```
IFERROR((销售额-成本)/销售额, 0)
```
> 说明：毛利除以销售额，除零时返回0。将目标字段类型设为"公式"，格式设为百分比。

---

### 示例 2：根据分数评级
**用户：** 字段"分数"，90以上优秀，70以上良好，60以上合格，否则不合格

**输出：**
```
IFS(分数>=90,"优秀",分数>=70,"良好",分数>=60,"合格",TRUE,"不合格")
```

---

### 示例 3：计算工龄（年）
**用户：** 字段"入职日期"，计算到今天的工龄

**输出：**
```
DATEDIF(入职日期, TODAY(), "Y")
```

---

### 示例 4：条件拼接文本
**用户：** 字段"姓名"和"部门"，生成"姓名(部门)"格式

**输出：**
```
CONCATENATE(姓名,"(",部门,")")
```
或简写：
```
姓名&"("&部门&")"
```

---

### 示例 5：蔬菜农场-计算总产值
**用户：** 字段"亩产"、"种植面积"、"销售单价"，计算总产值

**输出：**
```
亩产*种植面积*销售单价
```

---

### 示例 6：蔬菜农场-计算亩均收入
**用户：** 字段"总收入"、"总面积"，计算亩均收入

**输出：**
```
IFERROR(总收入/总面积, 0)
```
> 说明：防除零保护，总面积为空或0时返回0。

---

### 示例 7：检查中间字段公式是否正确
**场景：** 目标公式依赖 `学习投入分数` 字段，先确认它的公式

```bash
node scripts/feishu-bitable-api.js get-field MIASw72fgiRMCxkyqhtcuSwVnPf 客户档案表 学习投入分数
```

**输出示例（有问题）：**
```
字段 ID   : fldZTgCSLa
类型      : 20（Formula）
公式      : ⚠️  "0"（未设置有效公式！）
```
> 发现公式为 `0`，需先修复该字段，再使用它参与计算。

---

## 注意事项

- ⚠️ **中文括号不需要转义**：`（` 和 `）` 可以直接写在正则中，无需转义。
- ⚠️ **提取括号内分数的写法**：`VALUE(REGEXEXTRACT(字段名, "（\d+)分）"))`
- ⚠️ **不支持的 Excel 函数**：若用户需求涉及 Excel 专有函数（如 `XLOOKUP`、`SUMPRODUCT`、`STDEV`），需告知用户并给出多维表格的替代方案。
- ⚠️ **字段名区分大小写**：请与实际字段名完全一致。
- ⚠️ **关联字段**：引用"关联字段"中的子字段，用 `关联字段名.子字段名` 格式。
- ⚠️ **多选字段**：多选字段返回的是数组，搭配 `ARRAYJOIN`、`CONTAIN` 等函数使用。
- ⚠️ **API 写入时 PowerShell 中文问题**：在 Windows PowerShell 中执行包含中文的 API 调用可能出错，建议使用脚本文件（`.js`）而非直接命令行执行。
- ⚠️ **公式含特殊字符时禁止命令行传参**：公式中含 `<`、`>`、`|`、`&` 等字符时，PowerShell 会将其解析为重定向/管道符导致参数被截断，**必须**将公式写入 `.js` 脚本文件后执行，不能直接通过 `set-formula` 命令行传入。
- ⚠️ **单选字段 IF 匹配前必须检查实际选项**：用 `get-field` 查看字段的真实选项列表，不要假设选项文本唯一——历史录入可能存在前置空格、引号写法差异等脏数据，需用 `OR` 兼容所有变体写法。
