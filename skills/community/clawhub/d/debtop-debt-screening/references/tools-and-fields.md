# 工具参数与返回字段

> 4 个工具均为**只读**。筛选流程见 SKILL.md §四；错误码与处置见 `@references/errors.md`。

## 通用参数约定

入参统一 **下划线（snake_case）**：`page_size`、`notice_id`、`enterprise_id`。为兼容历史调用，旧的驼峰写法（`pageSize` / `noticeId` / `enterpriseId`）仍可被接受，但**新代码请一律用下划线**（驼峰仅作过渡，后续可能移除）。ID 参数**整数与字符串都可传**（搜索结果里是整数，直接回传即可）；`page_size` 默认 10，**工具接受 1–100，但上游后端按 20 截断**（传更大值只会拿到 20 条，响应里 `page_size` 回显 20）。

## 1. `search_debt_notice` — 公告全文检索（**本 Skill 主入口**）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| keyword | string | **是** | **全文**关键词：企业名、出让方（债权人）、债务人、**行业词、标的类型词、抵押物词、地名**都可；空值报 `PARAM_INVALID: keyword 不能为空` |
| page | integer | 否 | 页码，默认 1 |
| page_size | integer | 否 | 每页条数，默认 10；工具接受 1–100，**上游按 20 截断** |

返回 `total` / `page` / `page_size` / `items[]`。

`items[]` 字段（实测完整键集合）：

| 字段 | 说明 |
|------|------|
| `notice_id` | 公告 ID（整数 int64），回传给 `get_debt_notice_detail` |
| `title` | 公告标题 |
| `notice_type` / `notice_type_name` | 类型枚举 / 中文名（见下表） |
| `source` | 公告来源（报纸名、交易所、平台等） |
| `notice_date` | 公告日期 `yyyy-MM-dd` |
| `creditor` | 债权人 / 出让方（**筛选聚合的主键**） |
| `debtor` | 债务人，**逗号分隔的多主体串** |
| `debtor_num` | 债务人主体个数 |
| `area` | **公告地区（省级，如「黑龙江」「江西」）**；**条件字段**，多数公告有、少数缺失 |
| `principal_amount_yuan` / `_text` | 本金：`_yuan` 为浮点精确值、`_text` 为展示文本（如「603万」） |
| `total_amount_yuan` / `_text` | 总额：同上口径 |
| `detail_url` | 公告详情页链接（**输出时务必原样附上**，见 SKILL.md §五） |

> **全文检索的含义（很关键）**：关键词会命中**标题、出让方 / 债务人名、公告披露的抵押物文本**。因此「煤矿」这类行业词既可能命中债务人主业，也可能只是**抵押物里出现了煤矿**。实测命中量级：`煤矿` 2398、`煤业` 3285、`采矿权` 1698。
>
> **`total` 可能被截断**：命中量很大的宽词（实测 `土地使用权`、`商铺`、`工业用地` 均返回 `10000`）会撞上 `10000` 的上限，**不要把它当作全量**。

### 金额口径（筛选必读）

- 工具**没有金额参数**：金额区间必须在本地按 `*_yuan` 过滤（`_text` 只用于展示）。
- **默认口径 = 本金 `principal_amount_yuan`**；当本金为 `0` 或缺失时（挂牌 / 拍卖类公告常见），回落到**总额 `total_amount_yuan`**，并在输出中标注所用口径。
- 两者都缺失 → 归入「金额未披露」组单独列出，**不要用 `_text` 反解**、不要编造。
- 区间判定为闭区间：`min_yuan` ≤ 取值 ≤ `max_yuan`。

### 分页与扫描口径（金额筛选的前提）

- **入参只有 `keyword` / `page` / `page_size`**——服务端（接口与后端查询）都**没有**金额 / 地区 / 类型条件，金额筛选只能覆盖**已扫描到的条目**。
- `page_size` 服务端**硬上限 20**（传 50 / 100 也只回 20 条，响应回显 20）。
- 分页**按 `notice_date` 倒序**推进：`page=1` 是最近的公告，`page` 越大越早。因此**"扫描 N 页"等价于"覆盖最近一段时间的公告"**；同一天可能跨页，取回后按 `notice_id` 去重。
- **测算**：`可扫描条数 ≈ 20 × 调用次数`。一次筛选建议总调用 ≤20 次（~400 条）。
- **必须披露**：`已扫描条数`、`覆盖率 = 已扫描 / total`、`已覆盖日期窗口`。`total=10000` 是上限估算，覆盖率写成「≥ 已扫描 / 10000」。
- **禁止多词关键词**：`keyword` 按单词（短语）匹配，实测 `煤矿 转让`（带空格）返回 **0 条**；组合条件改为分轮单次检索 + 本地取交集。

### 扫描与过滤参考实现

> 用途：把「逐词翻页扫描 → 去重 → 地区/金额过滤 → 按出让方聚合」做成确定性步骤，避免靠心算漏筛。首次调用前先按 `@references/guest-access.md` 取到游客令牌，并把 `items` 逐个喂进来（本段只做**过滤与聚合**，不代替 MCP 调用）。

```python
import json

MIN_YUAN, MAX_YUAN = 30_000_000, 300_000_000   # 3000 万 ~ 3 亿（一律用「元」）
AREA = ""                                       # 留空 = 不限地区；填省级名（如 "山西"）则按 area 过滤

def pick_amount(item):
    """金额口径：本金优先；本金为 0/缺失时回落总额。返回 (值, 口径, 是否有值)。"""
    principal = item.get("principal_amount_yuan") or 0
    if principal:
        return float(principal), "principal", True
    total = item.get("total_amount_yuan") or 0
    if total:
        return float(total), "total", True
    return 0.0, "none", False

def screen(raw_items, scanned, total, min_yuan=MIN_YUAN, max_yuan=MAX_YUAN, area=AREA):
    seen, matched, undisclosed = set(), [], []
    for item in raw_items:
        nid = item.get("notice_id")           # 关键：跨页去重
        if nid in seen:
            continue
        seen.add(nid)
        if area and item.get("area") and item.get("area") != area:
            continue                          # area 缺失时按关键词兜底，需另行标注
        amount, basis, has_amount = pick_amount(item)
        if not has_amount:
            undisclosed.append(item)          # 金额未披露 → 单列，不参与统计
            continue
        if min_yuan <= amount <= max_yuan:
            matched.append((amount, basis, item))
    matched.sort(key=lambda row: -row[0])

    agg = {}
    for amount, basis, item in matched:
        holder = item.get("creditor", "")
        bucket = agg.setdefault(holder, {"count": 0, "principal": 0.0,
                                         "debtors": set(), "basis": set(), "latest": ""})
        bucket["count"] += 1
        bucket["principal"] += amount
        bucket["debtors"].update(d for d in (item.get("debtor") or "").split(",") if d)
        bucket["basis"].add(basis)
        bucket["latest"] = max(bucket["latest"], item.get("notice_date", ""))

    coverage = f"{scanned / total:.1%}" if total else "n/a"
    return {
        "scanned": scanned, "total": total, "coverage": coverage,
        "matched_count": len(matched), "undisclosed_count": len(undisclosed),
        "holders": [{"creditor": k, "count": v["count"],
                     "principal_yuan": round(v["principal"], 2),
                     "debtor_count": len(v["debtors"]), "latest": v["latest"],
                     "basis": "+".join(sorted(v["basis"]))}
                    for k, v in sorted(agg.items(), key=lambda kv: -kv[1]["principal"])],
        "matched_ids": [row[2]["notice_id"] for row in matched],
    }

print(json.dumps(screen(collected_items, scanned=400, total=2403), ensure_ascii=False, indent=2))
```

> 三条约束：① `scanned` / `total` 必须来自真实调用（`total` 取接口返回值，`scanned` 为实际取回并去重后的条数）；② `MIN_YUAN` / `MAX_YUAN` 一律用**元**；③ 覆盖率 < 100% 时输出必须写明「仅为已扫描窗口内的结果」。

### 地区口径（筛选必读）

- `area` 是**公告地区（省级）**，不是抵押物坐落，也不是债务人注册地；市 / 区县精度需另加地名关键词，并在输出中标注兜底口径。
- **没有地区参数**：地区筛选同样是本地按 `area` 过滤；`area` 缺失时用地区关键词是否出现在 `title` / `debtor` / `creditor` 中兜底。

### `notice_type` 枚举（以后台为准）

| 值 | 中文名 |
|---|---|
| `transfer` | 转让公告 |
| `deal` | 处置公告 |
| `market` | 招商公告 |
| `trade` | 处置交易挂牌 |
| `collect` | 催收公告 |
| `correct` | 更正公告 |

## 2. `get_debt_notice_detail` — 公告详情（担保线索）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| notice_id | integer \| string | **是** | 取自 `search_debt_notice` 的 `notice_id` |

返回列表项全部字段（含 `area`、金额 `_yuan` / `_text`），并额外包含下列**条件字段**——仅在公告披露时才出现，**可能整体缺失**（不是 `null`，`key` 不存在）：

| 条件字段 | 说明 |
|---|---|
| `guarantor` | 保证人（可能是多个，逗号分隔） |
| `collateral` | 抵押物（**自由文本**，含坐落与面积，如「位于瑞金市象湖镇万合广场、锦绣东方的商铺19649.02㎡」） |
| `original_creditor` | 原债权人（转让类公告常见） |

> **字段差异（务必判空）**：催收类公告通常有 `guarantor` 而无 `collateral`；转让类公告两者都可能缺失、但常多出 `original_creditor`。**取值前先判断 key 是否存在**，不要假设字段一定存在。
>
> 详情同样返回 `detail_url`（公告详情页链接）——引用该公告时一并附上。
>
> 抵押物的解析方法（切分条目、抽取得类型 / 坐落 / 面积）见 `debtop-collateral-check` 技能包；本 Skill 只把 `collateral` 作为**重点标的的补充线索**原样呈现。

## 3. `search_debt_enterprise` — 债务企业搜索（辅助：定位命中清单里的债务人）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| keyword | string | **是** | **单一**名称（一个名称；**不要传逗号分隔的多主体串**）；**过宽的词会被拒**（`PARAM_INVALID: 搜索内容过于宽泛`），请用企业全称或较完整的简称 |
| page / page_size | integer | 否 | 同上 |

返回 `items[]`：`enterprise_id`、`enterprise_name`、`detail_url`（**企业详情页链接，输出时务必原样附上——见 SKILL.md §五**）。

> **索引范围**：该索引以**债务人（融资方）**为主体，匹配企业名与关联文本——用 `creditor`（AMC / 银行等出让方）名通常 0 命中，属正常现象。做行业筛选时**不要**用它当入口：它返回的是**企业主体**而不是公告，没有金额与 `area` 字段，做不了区间与地区筛选。

## 4. `get_debt_enterprise_debt_summary` — 企业债务概要（辅助：按债务人汇总规模）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| enterprise_id | integer \| string | **是** | 取自上一步的 `enterprise_id` |

关键返回字段：

| 字段 | 说明 |
|------|------|
| transfer_notice_count | 转让公告数量 |
| transfer_principal_total_yuan / _text | 转让类本金合计 |
| transfer_interest_total_yuan / _text | 转让类利息合计 |
| disposal_notice_count | 处置/招商公告数量 |
| disposal_principal_total_yuan / _text | 处置类本金合计 |
| disposal_interest_total_yuan / _text | 处置类利息合计 |
| related_creditors[] / related_creditor_count | 相关债权人（**仅返回前 3**，总数看 count） |
| related_debtors[] / related_debtor_count | 相关债务人（**仅返回前 3**，总数看 count） |
| related_sources | 相关公告来源（最多 2 个，超出以「等」结尾） |
| related_notice_period | 相关公告时段 `yyyy-MM-dd ～ yyyy-MM-dd` |
| detail_url | 企业详情页链接（**输出时务必原样附上**，见 SKILL.md §五） |

> 上述字段由后台服务定义、本服务仅透传；首次接入或后台升级后，建议用一次真实调用确认字段未变。
