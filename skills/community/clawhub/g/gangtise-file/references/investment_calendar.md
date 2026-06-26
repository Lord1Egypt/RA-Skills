# 投研日程调用指导

## 简介

本脚本 `scripts/investment_calendar.py` 整合四类资讯日程列表接口（均为 `POST`，分页 `from`/`size`，单页最大 50 条）：

| `-t` / `--type` | 说明 | 接口路径（相对 open-insight） |
|----------|------|------------------------------|
| `roadshow` | 路演 | `/schedule/roadshow/getList` |
| `site_visit` | 调研 | `/schedule/site-visit/getList` |
| `strategy_meeting` | 线下策略会 | `/schedule/strategy-meeting/getList` |
| `forum` | 论坛 | `/schedule/forum/getList` |

牵头机构名称通过 `INSTITUTIONS_MAP` 智能匹配为机构 ID；研究方向支持 `utils.py` 中 `RESEARCH_AREA_MAP` 的中文名（宏观、策略、固收、金工、海外）或**直接传研究方向 ID**。证券代码请使用标准格式（如 `000001.SZ`）。

## 公共参数

| 参数 | 说明 |
|------|------|
| `-t` / `--type` | **必填**，`roadshow` / `site_visit` / `strategy_meeting` / `forum` |
| `-k` / `--keyword` | 搜索关键词，可为空 |
| `-sd` / `--start_date` | 开始日期 `YYYY-MM-DD`（转为 13 位时间戳 `startTime`） |
| `-ed` / `--end_date` | 结束日期 `YYYY-MM-DD`（结束日含全天，转为 `endTime`） |
| `-l` / `--limit` | 返回条数上限，默认见 `FILE_DEFAULT_LIMIT["calendar"]` |

## 按类型的可选参数

### 路演 `roadshow`

| 参数 | 对应请求字段 | 取值说明 |
|------|----------------|----------|
| `--research_areas` | `researchAreaList` | 研究方向 ID 或中文名（见 `RESEARCH_AREA_MAP`） |
| `--institutions` | `institutionList` | 牵头机构，逗号分隔，智能匹配 brokerId |
| `--securities` | `securityList` | 证券代码，逗号分隔 |
| `--category_list` | `categoryList` | `earningsCall` 业绩会、`strategyMeeting` 策略会、`companyAnalysis` 公司分析、`industryAnalysis` 行业分析、`fundRoadshow` 基金路演 |
| `--market_list` | `marketList` | `aShares`、`hkStocks`、`usChinaConcept`、`usStocks` |
| `--participant_role_list` | `participantRoleList` | `management` 高管、`expert` 专家 |
| `--broker_type_list` | `brokerTypeList` | `cnBroker` 中资卖方、`otherBroker` 外资卖方 |
| `--permission` | `permission` | `1` 公开、`2` 私密；可逗号多选，如 `1` 或 `1,2` |

### 调研 `site_visit`

| 参数 | 对应请求字段 | 取值说明 |
|------|----------------|----------|
| `--research_areas` | `researchAreaList` | 同路演 |
| `--institutions` | `institutionList` | 牵头机构 |
| `--securities` | `securityList` | 证券代码 |
| `--object_list` | `objectList` | `company` 公司调研、`industry` 行业调研 |
| `--category_list` | `categoryList` | `single` 单场、`series` 系列 |
| `--market_list` | `marketList` | 同路演 |
| `--permission` | `permission` | `1` / `2`，可多选 |

### 线下策略会 `strategy_meeting`

仅支持公共参数与：

| 参数 | 对应请求字段 |
|------|----------------|
| `--institutions` | `institutionList` |

（接口无 `researchAreaList` / `securityList` 等。）

### 论坛 `forum`

| 参数 | 对应请求字段 |
|------|----------------|
| `--securities` | `securityList` |
| `--research_areas` | `researchAreaList` |

## 枚举与辅助脚本

- **机构**：`python3 scripts/get_institutions.py`
- **研究方向中文名**：见 `scripts/utils.py` 中 `RESEARCH_AREA_MAP`（若平台「研究方向分类」与内置 ID 不一致，请直接传接口要求的 ID）

## 返回说明

每条记录包含 `类型`（路演 / 调研 / 线下策略会 / 论坛）、`类型中ID`（如 `roadshowId`、`siteVisitId` 等）及标题、时间区间、地点等字段。日程类结果**不通过** `get_file.py` 下载文件；如需报名链接等，见返回中的 `报名链接`（线下策略会）等字段。

## 调用示例

```bash
# 路演：关键词 + 时间 + 路演类型
python3 scripts/investment_calendar.py -t roadshow -k 策略会 -sd 2026-02-01 -ed 2026-03-30 --category_list strategyMeeting -l 20

# 调研：公司调研 + 公开权限
python3 scripts/investment_calendar.py -t site_visit --object_list company --permission 1 -sd 2026-03-01 -ed 2026-03-30

# 线下策略会：机构
python3 scripts/investment_calendar.py -t strategy_meeting --institutions 开源证券 -l 10

# 论坛：研究方向（宏观 → ID 由 RESEARCH_AREA_MAP 解析）
python3 scripts/investment_calendar.py -t forum --research_areas 宏观 -k 论坛 -l 15
```
