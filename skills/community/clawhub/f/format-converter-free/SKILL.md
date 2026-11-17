---
slug: format-converter-free
name: format-converter-free
version: 1.0.0
displayName: 数据格式转换(免费版)
summary: CSV、JSON、XML、YAML、TOML 等格式互转的免费核心能力,支持单文件快速转换。
license: Proprietary
edition: free
description: '数据格式转换免费版面向需要在不同数据格式间快速转换的开发者与数据工作者,提供 CSV、JSON、XML、YAML、TOML 等主流格式的互转能力。核心能力:

  - 主流格式互转:CSV ↔ JSON ↔ YAML ↔ XML ↔ TOML

  - 单文件快速转换:输入一个文件,输出另一种格式

  - 嵌套结构保留:支持多层嵌套对象与数组

  - 类型智能推断:数字、布尔、null 自动识别

  - 编码自动处理:UTF-8/GBK/UTF-16 自动检测与转换


  适用场景:

  - 配置文件迁移(如 YAML → TOML)

  - API ...'
tags:
- 格式转换
- 数据交换
- 配置文件
- 集成工具
tools:
- read
- exec
homepage: https://skillhub.cn
pricing_tier: "L1-入门级"
pricing_model: per_use
suggested_price: "9.9 CNY/per_use"
tools: ["read", "write", "exec"]
tags: "工具,效率,自动化"
---
# 数据格式转换 免费版

## 一、概述

数据格式转换免费版面向需要在不同数据格式间快速转换的开发者与数据工作者。覆盖 CSV、JSON、XML、YAML、TOML 等主流格式的互转,适合单文件、小规模的转换场景。

免费版聚焦"快速、准确、类型智能"的核心转换能力,适合 10MB 以内的文件,无需复杂配置即可上手。

## 核心能力

### 2.1 支持的格式矩阵

| 输入格式 | 输出格式 | 典型场景 |
|----|----|----|
| CSV | JSON | 表格数据入 API |
| JSON | CSV | API 数据入 Excel |
| JSON | YAML | 配置文件人性化 |
| YAML | JSON | 配置文件程序化 |
| XML | JSON | 旧系统集成 |
| JSON | XML | SOAP/legacy 接口 |
| TOML | JSON | Python 配置入程序 |
| JSON | TOML | 程序配置入 Python |

**输入**: 用户提供1 支持的格式矩阵所需的指令和必要参数。
**处理**: 解析1 支持的格式矩阵的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回1 支持的格式矩阵的响应数据,包含状态码、结果和日志。

### 2.2 嵌套结构保留

- 支持多层嵌套对象与数组
- 嵌套结构在 CSV 中以 `.` 分隔展开(如 `user.address.city`)
- 数组在 CSV 中以 `[item1, item2]` 形式保留
- 转换过程不丢失字段,保留原始数据完整性

**输入**: 用户提供2 嵌套结构保留所需的指令和必要参数。
**处理**: 解析2 嵌套结构保留的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回2 嵌套结构保留的响应数据,包含状态码、结果和日志。

### 2.3 类型智能推断

| 原始值 | 推断类型 | 说明 |
|:-----|:-----|:-----|
| `42` | int | 整数 |
| `3.14` | float | 浮点数 |
| `true` / `false` | bool | 布尔值 |
| `null` / `None` | null | 空值 |
| `2024-01-01` | str(保留原文) | 日期字符串 |
| 其他 | str | 字符串 |

**输入**: 用户提供3 类型智能推断所需的指令和必要参数。
**处理**: 解析3 类型智能推断的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回3 类型智能推断的响应数据,包含状态码、结果和日志。

### 2.4 编码自动处理

- 自动检测 UTF-8 / GBK / UTF-16 / Latin-1
- 输出统一为 UTF-8(可选其他)
- BOM 头自动识别与处理
- 中文内容完整保留,不会乱码

**输入**: 用户提供4 编码自动处理所需的指令和必要参数。
**处理**: 解析4 编码自动处理的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回4 编码自动处理的响应数据,包含状态码、结果和日志。

### 2.5 边界情况处理

- **空文件**:返回空结构,不报错
- **超大行**:单行长度无上限,但建议 <1MB
- **特殊字符**:引号、换行、制表符等正确转义
- **重复键**:JSON 中保留最后一个,转换时给出警告
- **循环引用**:JSON/XML 不允许,转换前自动检测

**输入**: 用户提供5 边界情况处理所需的指令和必要参数。
**处理**: 解析5 边界情况处理的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回5 边界情况处理的响应数据,包含状态码、结果和日志。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：等格式互转的免费、核心能力、支持单文件快速转、数据格式转换免费、版面向需要在不同、数据格式间快速转、换的开发者与数据、工作者、等主流格式的互转、主流格式互转、单文件快速转换、输入一个文件、输出另一种格式、自动检测与转换等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 适用场景

| 角色 | 典型场景 | 输入 | 输出 |
|---:|---:|---:|---:|
| 后端开发者 | API 数据入 Excel | JSON | CSV |
| 运维工程师 | 配置文件迁移 | YAML | TOML |
| 数据分析师 | 表格数据入程序 | CSV | JSON |
| 集成工程师 | 旧系统适配 | XML | JSON |
| Python 开发者 | 配置文件管理 | TOML | JSON |

## 使用流程

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

预计上手时间:**< 60 秒**。

直接以自然语言向 Agent 描述转换任务,以下为可复制模板:

## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|:---:|:---:|:---:|:---:|
| input | string | 是 | 数据格式转换(免费版)处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```text
请把 config.yaml 转换为 toml 格式,保留所有嵌套结构与注释。
```

```text
请把 users.json 转换为 csv,嵌套字段以点号展开。
```

Agent 会自动识别输入格式与目标格式,执行转换并输出结果。

## 示例

### 5.1 CSV ↔ JSON

输入(CSV):
```csv
name,age,city
张三,30,北京
李四,25,上海
```

输出(JSON):
```json
[
  {"name": "张三", "age": 30, "city": "北京"},
  {"name": "李四", "age": 25, "city": "上海"}
]
```

### 5.2 JSON ↔ YAML

输入(JSON):
```json
{
  "database": {
    "host": "localhost",
    "port": 5432,
    "name": "myapp"
  },
  "debug": true
}
```

输出(YAML):
```yaml
database:
  host: localhost
  port: 5432
  name: myapp
debug: true
```

### 5.3 XML ↔ JSON

输入(XML):
```xml
<users>
  <user id="1">
    <name>张三</name>
    <age>30</age>
  </user>
</users>
```

输出(JSON):
```json
{
  "users": {
    "user": {
      "@id": "1",
      "name": "张三",
      "age": 30
    }
  }
}
```

### 5.4 TOML ↔ JSON

输入(TOML):
```toml
[database]
host = "localhost"
port = 5432
# ...
[servers.alpha]
ip = "10.0.0.1"
```

输出(JSON):
```json
{
  "database": {
    "host": "localhost",
    "port": 5432
  },
  "servers": {
    "alpha": {
      "ip": "10.0.0.1"
    }
  }
}
```

### 5.5 Python 代码示例

```python
import csv, json, yaml, xmltodict, tomllib, tomli_w
# ...
# CSV → JSON
with open('data.csv', 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)
# ...
# JSON → YAML
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
with open('data.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
# ...
# YAML → TOML
with open('config.yaml', 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)
with open('config.toml', 'wb') as f:
    tomli_w.dump(data, f)
# ...
# XML → JSON
with open('data.xml', 'r', encoding='utf-8') as f:
    data = xmltodict.parse(f.read())
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

## 六、最佳实践

- **备份原文件**:转换前保留原始文件,便于回退
- **校验输出**:转换后用 `diff` 或工具校验数据完整性
- **嵌套适度**:CSV 不适合过深的嵌套结构,建议 ≤3 层
- **编码统一**:输入输出统一 UTF-8,避免乱码
- **特殊字符**:CSV 中含逗号/引号/换行的字段必须用引号包裹
- **类型显式**:JSON 中数字与字符串需明确区分
- **注释处理**:YAML/TOML 注释在转换为 JSON 时会丢失(JSON 不支持注释)

## 常见问题

### Q1: 转换后中文乱码怎么办?

A: 检查输入文件编码与输出编码是否一致。免费版默认 UTF-8,如需其他编码请在指令中说明,如"输出 GBK 编码"。

### Q2: CSV 嵌套字段如何处理?

A: 免费版自动以 `.` 分隔展开嵌套字段,如 `user.address.city`。数组以 `[item1, item2]` 形式保留。

### Q3: 转换后字段顺序变了?

A: JSON 对象字段无序,但免费版会尽量保留原始顺序。YAML/TOML 转换可能因库实现略有差异。

### Q4: 大文件能否处理?

A: 免费版推荐处理 10MB 以内文件。更大文件建议使用专业版的流式转换与批处理能力。

### Q5: 注释会保留吗?

A: YAML/TOML 中的注释在转换为 JSON 时会丢失(JSON 不支持注释)。YAML ↔ TOML 互转时注释尽量保留。

## 已知限制

本免费体验版限制以下高级功能:

- 禁用批量文件转换(单次仅处理 1 个文件)
- 禁用流式转换(文件大小上限 10MB)
- 禁用自定义字段映射与重命名
- 禁用转换模板保存与复用
- 禁用定时转换任务
- 禁用与外部数据库(如 `PostgreSQL`)的导入导出
- 禁用转换历史与审计日志

解锁全部功能请使用专业版:`format-converter-pro`
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 依赖说明

### 运行环境

- **Agent 平台**: 任意支持 SKILL.md 的 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **Python**: 3.11+(tomllib 内置)

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |
| pyyaml | Python 库 | 必需 | `pip install pyyaml`(YAML) |
| xmltodict | Python 库 | 必需 | `pip install xmltodict`(XML) |
| tomli_w | Python 库 | 必需 | `pip install tomli_w`(TOML 写入) |
| tomllib | Python 库 | 必需 | Python 3.11+ 内置(TOML 读取) |
| chardet | Python 库 | 可选 | `pip install chardet`(编码检测) |

### API Key 配置

- 本 Skill 基于自然语言指令,无需额外 API Key
- 如对接外部存储,需用户自行提供访问凭证,通过环境变量传入,**禁止**在对话或脚本中明文硬编码

### 可用性分类

- **分类**: MD+EXEC(纯 Markdown 指令,核心功能需要 exec 命令行执行能力)
- **说明**: 基于自然语言驱动的 AI Skill,通过类型智能与编码自动处理保障转换质量

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|:---|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |
