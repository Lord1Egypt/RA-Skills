# Fallbacks — festival-flight

> Failure recovery procedures for each error scenario.

---

## Case 0: flyai-cli Not Installed

**Detection:** `command not found` when running `flyai --version`

**Response:**
```
⚠️ flyai-cli 未安装。正在安装...
```

**Action:** Run `npm i -g @fly-ai/flyai-cli`, then retry.

---

## Case 1: No Flights Found

**Detection:** CLI returns empty result list

**Response:**
```
未找到符合条件的航班。

建议：
1. 扩大日期范围（节日高峰航班紧张）
2. 接受中转航班
3. 尝试附近机场
```

**Action:** Retry with `--journey-type 2` or wider date range.

---

## Case 2: Over Budget

**Detection:** User specifies `--max-price` and all results exceed it

**Response:**
```
所有航班均超出预算 ¥{max_price}。

建议：
1. 调整预算至 ¥{lowest_price}
2. 错峰出行（节前/节后出发）
3. 选择中转航班
```

---

## Case 3: Ambiguous City Name

**Detection:** City name matches multiple airports

**Response:**
```
"{city}" 匹配多个机场，请确认：
1. {airport_1}
2. {airport_2}
```

---

## Case 4: Invalid Date Format

**Detection:** Date not in YYYY-MM-DD format

**Response:**
```
日期格式需为 YYYY-MM-DD，例如 2026-01-25
```

---

## Case 5: Parameter Conflict

**Detection:** Both `--dep-date` and `--dep-date-start/--dep-date-end` provided

**Response:**
```
请选择：指定具体日期（--dep-date）或日期范围（--dep-date-start + --dep-date-end）
```

**Action:** Use `--dep-date-start/--dep-date-end` and ignore `--dep-date`.

---

## Case 6: API Timeout

**Detection:** CLI does not respond within 30 seconds

**Response:**
```
⚠️ 查询超时，请稍后重试。
```

**Action:** Retry once. If still fails, suggest user try again later.
