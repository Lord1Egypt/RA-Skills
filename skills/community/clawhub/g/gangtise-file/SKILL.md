---
name: gangtise-file
description: 在 Gangtise 文件中心按不同文档类型（报告、公告、纪要等）检索，返回文件 ID 以及关键元数据/摘要，并提供按类型与 ID 下载完整文件的辅助。当你需要在“找哪些文件（先定位）”的阶段进行定位/筛选，并可能进一步下载核验时，务必使用本技能。检索结果基于系统匹配与字段归纳，强调专业性、准确性与覆盖全面；如需深入阅读与引用具体论点/段落内容，再优先选择 `gangtise-kb`。
version: 1.4.10
metadata:
  openclaw:
    requires:
      env:
        - GTS_ACCESS_KEY
        - GTS_SECRET_KEY
      config:
        - path: scripts/.authorization
          required: false
          description: 用于配置ak/sk, 内容为{"accessKey":"<ak>", "secretAccessKey":"<sk>"}。与GTS_ACCESS_KEY和GTS_SECRET_KEY使用其一即可。如果同时存在，则以GTS_ACCESS_KEY和GTS_SECRET_KEY为准，建议环境变量配置不成功时使用文件配置。
    envVars:
      - name: GTS_ACCESS_KEY
        required: true
        description: 用于和GTS_SECRET_KEY一起获取临时 authorization，推荐使用环境变量配置
      - name: GTS_SECRET_KEY
        required: true
        description: 用于和GTS_ACCESS_KEY一起获取临时 authorization，推荐使用环境变量配置
---

# 搜索

## 概览

该技能会查询 Gangtise 文件中心，检索多种文档类型，例如研究报告、公司公告、会议纪要、首席观点与投研日程（路演、调研、线下策略会、论坛）等。它会返回文件 ID，并附带关键元数据与简短摘要；这些命中结果基于检索匹配与字段归纳，强调专业性、准确性与覆盖全面，同时提供按“类型 + ID”下载完整文件的方法。注意：由于 API 限制，大多数结果最多限制为 100 条；多数情况下建议将结果数量限制在 10 条以内。

使用场景：
- 你需要按**类型、日期、证券或其他元数据**来定位、筛选或整理文档。
- 你想先构建一个**候选文档列表**（例如某只股票的近期报告、某段时间内的全部公告）。
- 你计划**下载完整文件**并在本技能之外处理（例如后续解析或单独阅读）。

与其他技能的区别：
- 当你主要关心的是*文本内容本身*（用于总结、问答、抽取论点等），并且不需要浏览长文件列表时，优先使用 **`gangtise-kb`**。

（中文说明：`gangtise-file` 更像"文件目录/索引"，解决"有哪些文件、ID 是什么、按条件筛一批出来"的问题；真正看内容、抽段落建议用 `gangtise-kb`。）


各文档类型的**主脚本**用于执行检索并返回文件列表；部分参数提供**枚举值脚本**（如行业、机构等），调用前可先执行对应脚本获取可选值。**无枚举值接口的参数**（如关键词、证券、日期等）会由后端**智能匹配**，直接传入用户意图相关文本即可。证券代码需传入标准格式（如 `000001.SZ`）。

所有脚本都具有 `-d` / `--download` 布尔型参数，用于判断在检索后自动下载对应文件至本地。一般来说用户不需要这个参数，除非用户明确要求下载文件。

所有脚本都具有`-sd`和`-ed`参数，使用时注意今天的年份和日期！

调用对应脚本前，请先查看对应脚本的调用指导文档，了解更多参数的含义和使用方法。

### 1. 从研究报告检索

按关键词、证券、日期、券商、行业、研报类别、语义标签、评级/评级变动、页数范围、来源类型等条件检索研究报告。

重要说明：**试用账号只能查询一个月内的研报**（以接口权限校验为准）。

示例（关键词"比亚迪"，限定时间范围与数量）：

```bash
python3 scripts/report.py -k 比亚迪 -sd 2026-01-01 -ed 2026-12-31 -l 20
```

行业、机构枚举值可通过 `scripts/get_industries.py`、`scripts/get_institutions.py` 获取。详见 [研究报告调用指导](./references/report.md)。

### 2. 外资研报检索

按关键词、证券、日期、券商、行业、区域、研报类别、语义标签、评级/评级变动、页数范围等条件检索外资研报列表。境外证券代码格式如 `UBER.N`。重要说明：**试用账号只能查询一个月内的外资研报**（以接口权限校验为准）。

示例（关键词 + 时间范围）：

```bash
python3 scripts/foreign_report.py -k 自动驾驶 -sd 2026-02-01 -ed 2026-03-30 -l 20
```

行业、券商、区域枚举值可通过 `scripts/get_industries.py`、`scripts/get_institutions.py`、`scripts/get_regions.py` 获取。详见 [外资研报调用指导](./references/foreign_report.md)。

### 3. 从公司公告检索

按证券、关键词、日期等条件检索公司公告。

示例（证券 + 关键词 + 时间）：

```bash
python3 scripts/announcement.py --securities 000858.SZ -k 业绩 -sd 2026-01-01 -ed 2026-12-31
```

详见 [公司公告调用指导](./references/announcement.md)。

### 4. 从会议纪要检索

按关键词、证券、机构、行业、来源类型、会议类别/市场/参会人角色等条件检索会议纪要。

示例（关键词 + 会议类别）：

```bash
python3 scripts/summary.py -k 锂电 --category_list earningsCall -l 20
```

行业、机构枚举值可通过 `scripts/get_industries.py`、`scripts/get_institutions.py` 获取。详见 [会议纪要调用指导](./references/summary.md)。

### 5. 首席观点列表检索

按关键词、证券、券商、研究方向、首席分析师、概念、投研标签、来源类型等条件检索首席观点列表。

示例（关键词 + 标签 + 来源）：

```bash
python3 scripts/opinion.py -k 半导体 --llm_tags strongRcmd --source_types realTime -l 20
```

券商枚举值可通过 `scripts/get_institutions.py` 获取。研究方向名称（宏观、策略、固收、金工、海外等）见 `scripts/utils.py` 中 `RESEARCH_AREA_MAP`。详见 [首席观点调用指导](./references/opinion.md)。

### 6. 投研日程（路演 / 调研 / 线下策略会 / 论坛）

示例（路演 + 关键词 + 时间）：

```bash
python3 scripts/investment_calendar.py -t roadshow -k 策略会 -sd 2026-02-01 -ed 2026-03-30 -l 20
```

机构枚举见 `scripts/get_institutions.py`；研究方向中文名见 `scripts/utils.py` 中 `RESEARCH_AREA_MAP`。详见 [投研日程调用指导](./references/investment_calendar.md)。

### 7. 获取枚举值

获取行业、机构的枚举值列表，用于为上述检索脚本提供参数可选值。

```bash
python3 scripts/get_industries.py
python3 scripts/get_institutions.py
python3 scripts/get_regions.py
```

### 8. 下载文件

根据文件 ID 与文件类型下载完整文件至本地。

示例（下载文件）：

```bash
python3 scripts/get_file.py --file-id 1234567890 --file-type "研究报告"
```