---
name: cdisc-library-api
description: "CDISC Library API Skill - 查询临床数据标准（QRS 量表、ADaM、CDASH、SDTM、受控术语）"
---

# CDISC Library API Skill - 临床数据标准查询

查询 CDISC Library API，获取 QRS 量表、ADaM、CDASH、SDTM、受控术语等临床数据标准。

## 🔐 配置

在 `TOOLS.md` 中添加 API Key：

```markdown
## CDISC API

- **API Key**: `你的 API Key`
```

获取地址：https://api.developer.library.cdisc.org/profile

或在环境变量中设置 `CDISC_API_KEY`。

## 📋 命令

### 基础查询

| 命令 | 说明 | 示例 |
|------|------|------|
| `/cdisc-library-api products` | 列出所有产品类别 | `/cdisc-library-api products` |
| `/cdisc-library-api qrs <code> [version]` | 查询 QRS 量表 | `/cdisc-library-api qrs AIMS01` |
| `/cdisc-library-api items <code> <version>` | 查询量表项目列表 | `/cdisc-library-api items AIMS01 2-0` |
| `/cdisc-library-api adam <product> [ds]` | 查询 ADaM 产品/数据结构 | `/cdisc-library-api adam adam-2-1` |
| `/cdisc-library-api sdtm <version> [domain]` | 查询 SDTM 实施指南 | `/cdisc-library-api sdtm 3-4 DM` |
| `/cdisc-library-api cdash <version> [domain]` | 查询 CDASH 标准 | `/cdisc-library-api cdash 1-0 DM` |
| `/cdisc-library-api ct <codelist>` | 查询受控术语代码表 | `/cdisc-library-api ct C102111` |
| `/cdisc-library-api ct-packages` | 查询术语包列表 | `/cdisc-library-api ct-packages` |

### 高级查询

| 命令 | 说明 | 示例 |
|------|------|------|
| `/cdisc-library-api root <type>` | 查询版本无关根资源 | `/cdisc-library-api root qrs` |
| `/cdisc-library-api docs [category]` | 查询 CDISC 文档 | `/cdisc-library-api docs` |
| `/cdisc-library-api rules [product]` | 查询 CDISC 规则 | `/cdisc-library-api rules adam` |
| `/cdisc-library-api search <keyword>` | 搜索变量/域/量表 | `/cdisc-library-api search USUBJID` |
| `/cdisc-library-api compare <type> <id> <v1> <v2>` | 版本比较 | `/cdisc-library-api compare qrs AIMS01 1-0 2-0` |

### 工具命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `/cdisc-library-api export <type> <id> [v]` | 导出数据为 JSON/CSV | `/cdisc-library-api export items AIMS01 2-0 --format=csv` |
| `/cdisc-library-api batch <file>` | 批量查询 | `/cdisc-library-api batch queries.txt` |
| `/cdisc-library-api cache clear` | 清除缓存 | `/cdisc-library-api cache clear` |

## 📦 文件结构

```
skills/cdisc/
├── SKILL.md                  # 本文件
├── README.md                 # 快速开始指南
├── cdisc_client.py           # API 客户端封装
├── commands/
│   ├── products.py           # 产品列表
│   ├── qrs.py                # QRS 量表查询
│   ├── items.py              # 量表项目查询
│   ├── adam.py               # ADaM 查询
│   ├── sdtm.py               # SDTM 查询
│   ├── cdash.py              # CDASH 查询
│   ├── ct.py                 # 受控术语查询
│   ├── ct_packages.py        # 术语包列表
│   ├── root.py               # 根资源查询
│   ├── docs.py               # 文档查询
│   ├── rules.py              # 规则查询
│   ├── search.py             # 搜索
│   ├── compare.py            # 版本比较
│   ├── export.py             # 导出功能
│   └── batch.py              # 批量查询
└── assets/
    └── quickref.md           # 速查表
```

## 🔧 使用示例

### 查询量表详情

```
/cdisc-library-api qrs AIMS01
```

输出：
- 量表名称、类型、注册状态
- 最新版本号
- 项目数量
- 前 5 个项目预览

### 查询量表完整项目

```
/cdisc-library-api items AIMS01 2-0
```

输出所有项目列表（序号、代码、标签）。

### 查询 ADaM 数据结构

```
/cdisc-library-api adam adam-2-1 ADSL
```

输出 ADSL 数据结构的所有变量集。

### 查询 SDTM 域变量

```
/cdisc-library-api sdtm 3-4 DM
```

输出 DM 域的所有变量，按角色分组（标识符、时间戳、记录标识等）。

### 查询受控术语

```
/cdisc-library-api ct C102111
```

输出代码列表详情和前 20 个术语。

### 搜索

```
/cdisc-library-api search USUBJID
```

跨所有产品类别搜索匹配项。

### 版本比较

```
/cdisc-library-api compare qrs AIMS01 1-0 2-0
```

输出两个版本之间的新增、删除、修改项。

### 导出为 CSV

```
/cdisc-library-api export items AIMS01 2-0 --format=csv
```

导出量表项目到 CSV 文件。

### 批量查询

创建 `queries.txt`:
```
qrs AIMS01
qrs CGI01 1-0
items AIMS01 2-0
adam adam-2-1
ct C102111
```

执行：
```
/cdisc-library-api batch queries.txt
```

## ⚠️ 注意事项

1. **速率限制**：自动添加 100ms 请求间隔
2. **缓存**：查询结果缓存 1 小时，位于 `skills/cdisc/.cache/`
3. **错误处理**：
   - 401：检查 API Key 是否正确
   - 404：检查参数格式（版本号应为 `x-y` 格式）
   - 429：请求过于频繁，已自动限流
4. **版本号格式**：使用 `x-y` 格式（如 `2-0`），不是 `x.y`

## 🔗 相关资源

- [CDISC Library Browser](https://library.cdisc.org/browser)
- [API Portal](https://api.developer.library.cdisc.org)
- [速查表](assets/quickref.md)
- [完整 API 文档](../../E:/openclaw/CDISC_API_使用指南.md)

---

*Skill 版本：1.0 | 基于 CDISC Library API v1 | 覆盖 9 大类 350+ 端点*
