# 多维表格函数 vs Excel 函数对照表

## 完全支持（行为与 Excel 一致）
| 类别 | 函数 |
|---|---|
| 逻辑 | IF, IFS, AND, OR, NOT, TRUE, FALSE, IFERROR, ISBLANK, ISERROR, ISNUMBER, SWITCH |
| 文本 | LEFT, RIGHT, MID, LEN, LOWER, UPPER, TRIM, FIND, SUBSTITUTE, REPLACE, CHAR, TEXT, CONCATENATE |
| 数字 | ABS, SUM, AVERAGE, MAX, MIN, ROUND, ROUNDUP, ROUNDDOWN, FLOOR, CEILING, MOD, INT, POWER, SQRT（无，用POWER替代）, PI, SUMIF, COUNTIF, COUNTA, RANK, MEDIAN |
| 日期 | TODAY, NOW, YEAR, MONTH, DAY, HOUR, MINUTE, SECOND, DATE, DATEDIF, DAYS, EDATE, EOMONTH, WEEKDAY, WEEKNUM, NETWORKDAYS, WORKDAY |
| 数学 | SIN, COS, TAN, ASIN, ACOS, ATAN, ATAN2, SINH, COSH, TANH, ASINH, ACOSH, ATANH |

## 多维表格特有（Excel 无对应）
| 函数 | 说明 |
|---|---|
| CONTAIN | 判断字段是否包含某值（常用于多选字段）|
| CONTAINSALL | 字段包含所有指定值 |
| CONTAINSONLY | 字段仅包含指定值 |
| CONTAINTEXT | 文本字段是否包含某子串 |
| RECORD_ID | 获取当前行的唯一 ID |
| DURATION | 生成时长值 |
| ARRAYJOIN | 将多值字段拼接为字符串 |
| LISTCOMBINE | 合并多组字段 |
| LOOKUP | 跨表/关联字段查找 |
| FILTER | 筛选关联字段记录 |
| SORT / SORTBY | 对关联字段排序 |
| MAP | 字段值映射转换 |
| FORMAT | 模板字符串格式化 |
| REGEXEXTRACT / REGEXEXTRACTALL / REGEXMATCH / REGEXREPLACE | 正则函数 |
| DISTANCE | 两地理坐标间距离 |
| TODATE | 文本转日期 |
| IFBLANK | 等同 IF(ISBLANK(...)) |
| ISNULL | 等同 ISBLANK |
| SEQUENCE | 生成数字序列 |
| RANDOMITEM | 从列表随机选取 |
| RANDOMBETWEEN | 指定范围随机整数 |
| HYPERLINK | 创建超链接 |
| ENCODEURL | URL 编码 |
| SPLIT | 文本分割 |

## Excel 有但多维表格不支持的函数
| Excel 函数 | 说明 | 替代方案 |
|---|---|---|
| VLOOKUP | 垂直查找 | 使用 `LOOKUP` |
| XLOOKUP | 扩展查找 | 使用 `LOOKUP` |
| INDEX | 索引引用 | 使用 `LOOKUP`/`NTH` |
| MATCH | 匹配位置 | 使用 `LOOKUP` |
| HLOOKUP | 水平查找 | 使用 `LOOKUP` |
| SUMIFS | 多条件求和 | 用 `SUMIF` 嵌套或 `SUM(FILTER(...))` |
| COUNTIFS | 多条件计数 | 用 `COUNTIF` 嵌套 |
| AVERAGEIF/AVERAGEIFS | 条件均值 | `=SUMIF(...)/COUNTIF(...)` |
| CONCAT | 文本连接 | `CONCATENATE` |
| TEXTJOIN | 带分隔符连接 | `ARRAYJOIN` |
| STDEV/STDEVP | 标准差 | 不支持，提示用户 |
| VAR/VARP | 方差 | 不支持，提示用户 |
| PERCENTRANK | 百分位排名 | 不支持，提示用户 |
| INDIRECT | 间接引用 | 不支持 |
| OFFSET | 偏移引用 | 不支持 |
| CHOOSE | 按序号选择 | 用 `IFS` 或 `SWITCH` 替代 |
| ISNUMBER | 判断数字 | 多维表格支持 `ISNUMBER` ✅ |
| ISERR | 判断错误 | 用 `ISERROR` |
| EXACT | 精确匹配（区分大小写）| 不支持，用 `=` 比较（不区分大小写）|
| PROPER | 首字母大写 | 不支持 |

## 字段引用语法
```
普通字段：     字段名
关联字段：     关联字段.子字段名
多选字段判断：  CONTAIN(多选字段, "选项A")
多选转文本：   ARRAYJOIN(多选字段, ",")
```
