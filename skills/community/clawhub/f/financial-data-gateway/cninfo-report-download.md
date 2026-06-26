---
name: cninfo-report-download
description: 从巨潮资讯网（cninfo.com.cn）按公司名称和年份精确搜索并下载中国A股上市公司年报PDF。这是数据采集流水线的第一步，为下游的financial-statement-extraction Skill提供原始PDF文件。Use when: (1) 需要下载A股上市公司年报，(2) 批量收集财务数据，(3) 构建财务数据库，(4) 进行财务分析前的数据准备。
version: 1.1.0
author: Shi Changlong时昌隆
copyright: © 2026 LibraQuant. All rights reserved.
license: MIT

# Dependencies
dependencies:
  - requests

# Environment Variables
env_vars: []

# Installation
install: |
  pip install requests

# Network Usage
network: true
network_targets:
  - www.cninfo.com.cn
  - static.cninfo.com.cn

# Filesystem Permissions
filesystem:
  read: []
  write:
    - "workspace/reports/"
    - "workspace/reports/*.pdf"

# Privacy Notice
privacy_notice: |
  本Skill会访问巨潮资讯网（cninfo.com.cn）搜索和下载公开披露的上市公司年报。
  仅下载监管要求公开披露的信息，不涉及非公开数据。
---

# Skill: 巨潮资讯年报下载 (cninfo-report-download)

> 从巨潮资讯网（cninfo.com.cn）按公司名称和年份精确搜索并下载中国A股上市公司年报PDF。
> 这是数据采集流水线的第一步，为下游的 `financial-statement-extraction` Skill 提供原始PDF文件。

---

## 版本

v1.1.0 — 2026-04-07

---

## 依赖

- **前置Skill**：无（数据源入口）
- **工具依赖**：`requests`

---

## 下游Skill

- `financial-statement-extraction` — 从下载的PDF中提取结构化财务数据

---

## 输入

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| company_name | str | ✅ | 公司简称（如"海天味业"、"甘源食品"） |
| year | int | ✅ | 年报年份（如2024，对应2024年年度报告） |
| output_dir | str | 可选 | 下载目录，默认 `workspace/reports/` |

---

## 输出

| 成功 | 返回类型 | 说明 |
|:---|:---:|:---|
| ✅ | str | 下载的PDF文件完整路径 |

| 失败 | 返回类型 | 说明 |
|:---|:---:|:---|
| ❌ | None | 下载失败（网络错误、未找到文件等） |

---

## 处理流程

### 步骤1：公司识别

**目标**：获取目标公司的股票代码和orgId。

**操作**：
1. **本地映射表查询**：先查本地 `COMPANY_CODES` 映射表获取股票代码（已收录13家常用公司）
2. **API查询**：用股票代码或公司名称调用巨潮 `topSearch/query` 接口获取 `orgId`
3. **交易所判断**：根据股票代码前缀判断交易所：
   - `6xx` → 上交所(sse)
   - `0xx/3xx` → 深交所(szse)

**异常处理**：
- 公司不在映射表 → 通过API动态查询
- API返回空 → 返回 `None`（公司不存在或名称有误）

---

### 步骤2：搜索年报

**目标**：在巨潮资讯网搜索目标年报。

**搜索策略（双层）**：

**第一层：精确搜索（主策略）**
1. 构造搜索请求：
   - 搜索期间：`{year+1}-01-01 ~ {year+1}-06-30`（年报通常在次年4月前披露）
   - 分类：`category_ndbg_szsh`（年度报告）
   - 精确搜索：用 `stock={code},{orgId}` 定位
2. API调用：巨潮 `hisAnnouncement/query` 接口

**第二层：关键词搜索（降级策略）**
- 当精确搜索失败时自动降级
- 使用 `searchkey={公司名}{year}年年度报告` 模糊搜索

**搜索参数说明**：
| 参数 | 值 | 说明 |
|:---|:---|:---|
| pageNum | 1 | 页码 |
| pageSize | 30 | 每页条数 |
| column | sse/szse | 交易所代码 |
| stock | 代码,orgId | 精确搜索参数 |
| category | category_ndbg_szsh | 年度报告分类 |
| seDate | YYYY-MM-DD~YYYY-MM-DD | 日期范围 |
| isHLtitle | true | 高亮标题（会返回<em>标签） |

---

### 步骤3：筛选目标公告

**目标**：从搜索结果中筛选正确的年报文件。

**匹配规则**：
| 类型 | 条件 | 处理方式 |
|:---|:---|:---|
| ✅ 包含 | 标题包含"年度报告"或"年报" | 进入候选列表 |
| ❌ 排除 | 标题包含"摘要" | 丢弃 |
| ❌ 排除 | 标题包含"更正" | 丢弃 |
| ❌ 排除 | 标题包含"补充" | 丢弃 |
| ❌ 排除 | 标题包含"英文"/"English" | 丢弃 |
| ❌ 排除 | 标题包含"修订" | 丢弃 |
| 🔄 兜底 | 无精确匹配 | 使用第一条结果 |

**优先级**：精确匹配 > 部分匹配 > 第一条结果

---

### 步骤4：下载PDF

**目标**：下载年报PDF文件到本地。

**操作**：
1. 从 `static.cninfo.com.cn` 下载PDF文件
2. 文件命名：`{公司名}_{报告标题}.pdf`
3. 文件名清理：
   - 清理HTML标签（巨潮接口返回的 `<em>` 高亮标签）
   - 清理非法文件名字符（`/`、`\`、`|`、`>`、`<`、`:`、`"`、`*`、`?`）
4. 保存到指定目录

**下载地址格式**：
```
https://static.cninfo.com.cn/{adjunctUrl}
```

---

## 巨潮API接口说明

### 搜索接口

```
POST http://www.cninfo.com.cn/new/hisAnnouncement/query
Content-Type: application/x-www-form-urlencoded

参数：
- pageNum: 页码
- pageSize: 每页条数
- column: 交易所（sse/szse）
- stock: 股票代码,orgId
- searchkey: 关键词搜索（与stock二选一）
- category: 公告分类（category_ndbg_szsh = 年度报告）
- seDate: 搜索日期范围（格式：YYYY-MM-DD~YYYY-MM-DD）
- isHLtitle: 是否高亮标题（true会返回<em>标签）
```

### 公司搜索接口

```
POST http://www.cninfo.com.cn/new/information/topSearch/query

参数：
- keyWord: 股票代码或公司名称
- maxNum: 返回条数

返回：[{code, zwjc, orgId, ...}]
```

### 下载地址

```
https://static.cninfo.com.cn/{adjunctUrl}
```

---

## 已踩过的坑

| 问题 | 现象 | 解决方案 |
|:---|:---|:---|
| HTML标签污染文件名 | 巨潮搜索接口设置 `isHLtitle=true` 后，返回的 `secName` 和 `shortTitle` 会包含 `<em>` 标签，直接用于文件名会导致 `[Errno 22] Invalid argument` | 用 `re.sub(r"<[^>]+>", "", text)` 清理 |
| 交易所判断错误 | 上交所股票代码以6开头，深交所以0或3开头。搜索时 `column` 参数必须匹配，否则搜不到 | 根据代码前缀自动判断交易所 |
| 搜索时间窗口不对 | 2024年年报在2025年1-4月披露，固定日期可能搜不到 | 搜索范围设为 `{year+1}-01-01 ~ {year+1}-06-30`，留足余量 |
| 公司未收录 | 映射表有限，新公司可能找不到 | 通过 `topSearch/query` 接口动态获取 `orgId` 和股票代码 |
| 重复下载 | 当前版本不检查文件是否已存在，每次都会重新下载 | 下游的 `data_collector.py` 有缓存逻辑来避免重复调用 |

---

## 已验证的公司

| 公司 | 代码 | 交易所 | 年份 | 文件大小 | 状态 |
|------|------|--------|------|----------|------|
| 海天味业 | 603288 | SSE | 2024 | ~3 MB | ✅ |
| 千禾味业 | 603027 | SSE | 2024 | ~1.2 MB | ✅ |
| 中炬高新 | 600872 | SSE | 2024 | ~1.8 MB | ✅ |
| 甘源食品 | 002991 | SZSE | 2024 | ~4.7 MB | ✅ |

---

## 已知限制

| 限制 | 说明 | 解决方案 |
|:---|:---|:---|
| 仅支持A股年报 | 不支持港股、美股、债券公告等 | v2.0规划多市场支持 |
| 仅支持年度报告 | 半年报、季报需要修改 `category` 参数 | v1.2规划支持 |
| 无本地缓存 | 不检查本地是否已有同名文件，每次都重新下载 | v1.3规划本地缓存+断点续传 |
| 无代理机制 | 巨潮网站偶尔限流，无重试和代理机制 | v1.3规划 |
| 公司映射表有限 | 仅预置13家，其他公司依赖动态查询 | 可手动扩展映射表 |
| 单线程下载 | 大批量下载效率低 | v2.0规划多线程 |

---

## 迭代路线

```
v1.1（当前）
    ↓
v1.2（支持半年报/季报）
    ↓
v1.3（本地缓存+断点续传+代理）
    ↓
v2.0（批量下载+多线程+港股支持）
```

---

## 工具文件

- `src/tools/download_cninfo.py` — 主下载逻辑
- `src/data/company_codes.py` — 公司代码映射表
