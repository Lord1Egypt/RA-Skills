# knowledge-base.md — 知识库目录生成与维护规范

> 适用于将业务系统的表结构、指标 SQL、枚举值整理为结构化知识库
> 更新时间：2026-04-01

---

## 一、知识库目录结构规范

按业务领域划分，每个领域一个文件夹，统一使用英文命名：

```
data-analysis/
├── README.md                    ← 总索引（领域总览 + 快速导航）
├── {domain}/                    ← 每个业务领域一个文件夹
│   ├── schema.md                ← 表结构说明
│   ├── metrics.md               ← 指标 SQL
│   ├── relations.md             ← 表关联关系（从 SQL 自动提取）
│   └── enums.md                 ← 枚举值速查
└── common/                      ← 公共规范
    ├── join-rules.md            ← 关联规则
    └── sql-pitfalls.md          ← 踩坑记录
```

### 领域文件夹命名规范

| 中文领域 | 英文文件夹 |
|---------|-----------|
| 需求管理 | requirement-management |
| 测试管理 | test-management |
| 缺陷管理 | defect-test-management |
| 项目管理 | project-management |
| 代码仓库 | code-repository |
| 安全管理 | security-management |
| 持续集成 | ci |
| 持续部署 | cd |
| 持续流水线 | pipeline |
| 制品管理 | artifact-management |
| 研发空间 | workspace-platform |
| 质量管理 | quality-management |
| 插件中心 | plugin-center |
| 任务管理 | task-management |
| 工时 | workhour |
| 成员 | member |

---

## 二、schema.md 生成规范

从表交接清单（xlsx 或文本）解析，每张表包含：

```markdown
## {序号}. {表名}（统一数据侧表名）

> 交接人：xxx | 调度时间：x | 主键：xxx | 增量字段：xxx | 预估数据量：xxx

### 字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| id | bigint | 主键ID |
| ...  | ...  | ...  |

### 核查信息

| 项目 | 结果 |
|------|------|
| 有无创建时间 | 有（create_time） |
| 有无修改时间 | 有（update_time） |
| 有无删除标识 | 有（deleted = 0 未删除） |
| 是否可增量同步 | 是（update_time） |

### 统一数据建表语句

```sql
CREATE TABLE ...
```

### 原始建表脚本

```sql
CREATE TABLE ...
```
```

---

## 三、metrics.md 生成规范

从指标 SQL 文件（xlsx）解析，结构如下：

```markdown
# {领域} — 指标 SQL

## 指标清单

| 指标ID | 指标名称 | 类型 | 频率 | 单位 | 维度数 |
|--------|---------|------|------|------|--------|
| kpi_xxx | 指标名 | 比率 | 日 | % | 2 |

---

## 1. {指标名称}

### 基本信息

| 项目 | 内容 |
|------|------|
| 指标ID | `kpi_xxx` |
| 度量类型 | 比率 |
| 更新频率 | 日 |
| 度量单位 | % |
| 时间限定 | 当月 |
| 维度 | 租户、项目 |

### 指标描述

{描述文本}

### SQL — {维度名称}（维度编码：{dim_code}）

```sql
SELECT ...
```
```

---

## 四、relations.md 生成规范

从 metrics.md 的 SQL 自动提取，包含：

1. **涉及表清单** — 每张表被多少个指标引用 + 指标示例
2. **关联关系图** — 主表 → JOIN 关联表 + ON 条件（树形结构）
3. **关联详情** — 每张主表的所有关联表 + JOIN 类型 + 关联字段

**提取逻辑：**
- 正则匹配 `FROM schema.table` 和 `JOIN schema.table`
- 建立别名映射（alias → full_table_name）
- 从 ON 条件提取关联字段
- 过滤已知 CTE 名（避免误识别）

---

## 五、enums.md 生成规范

从维度标准文件（xlsx）解析，结构如下：

```markdown
# {领域} — 枚举值速查

## {字典类型名称}

### {维度编码}

| 名称 | 值 |
|------|-----|
| 枚举名 | `枚举值` |
```

**字段映射：**
- 模块名 → 领域文件夹
- 字典类型名称 → 二级标题
- 原子指标维度编码 → 三级标题（SQL 中 WHERE 条件用的字段名）
- 字典数据名称 → 名称列
- 字典数据值 → 值列（SQL 中实际存储的值）

---

## 六、README.md 维护规范

README 包含三部分：

1. **目录结构** — 树形展示所有领域和文件
2. **领域总览表** — 每个领域的表数、指标数、已有文件
3. **快速导航表** — 四列（schema / metrics / relations / enums），每格为链接或 `—`

**更新时机：**
- 新增领域文件夹时
- 新增/删除任何 md 文件时
- 指标数量或表数量变化时

---

## 七、Python 脚本模板

### 从 xlsx 生成 schema.md

```python
import openpyxl, os

def parse_schema_xlsx(xlsx_path):
    wb = openpyxl.load_workbook(xlsx_path)
    ws = wb.active
    rows = []
    for row in ws.iter_rows(values_only=True):
        rows.append([str(c) if c is not None else '' for c in row])
    return rows

# 按模块分组，生成各领域 schema.md
```

### 从 metrics.md 提取表关联关系

```python
import re
from collections import defaultdict

def extract_joins(sql):
    pattern = re.compile(
        r'(?P<jtype>FROM|(?:LEFT\s+)?(?:INNER\s+)?JOIN)\s+'
        r'(?P<schema>[a-zA-Z_]\w*)\.(?P<table>[a-zA-Z_]\w*)'
        r'(?:\s+(?:AS\s+)?(?P<alias>[a-zA-Z_]\w*))?',
        re.IGNORECASE
    )
    return [m.groupdict() for m in pattern.finditer(sql)]

def extract_on_conditions(sql):
    pattern = re.compile(
        r'ON\s+(\w+)\."?(\w+)"?\s*=\s*(\w+)\."?(\w+)"?',
        re.IGNORECASE
    )
    return [
        {'left_alias': m.group(1), 'left_field': m.group(2),
         'right_alias': m.group(3), 'right_field': m.group(4)}
        for m in pattern.finditer(sql)
    ]
```

### 从 xlsx 生成 enums.md

```python
def parse_enums_xlsx(xlsx_path):
    wb = openpyxl.load_workbook(xlsx_path)
    ws = wb.active
    # 列：模块名, 字典类型名称, 字典类型编码, 原子指标维度编码, 字典数据名称, 字典数据值
    cur_module = ''
    result = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for row in ws.iter_rows(min_row=2, values_only=True):
        module = str(row[0]).strip() if row[0] else cur_module
        if row[0]: cur_module = module
        dict_type = str(row[1]).strip() if row[1] else ''
        dim_code  = str(row[3]).strip() if row[3] else ''
        name      = str(row[4]).strip() if row[4] else ''
        value     = str(row[5]).strip() if row[5] else ''
        if dict_type and name:
            result[module][dict_type][dim_code].append((name, value))
    return result
```
