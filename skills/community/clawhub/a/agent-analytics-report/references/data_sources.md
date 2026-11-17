# 数据源参考

## 一、Traces 目录

**路径**：`~/.workbuddy/traces/`

每个子目录以 PID 命名，包含一个或多个 `trace_*.json` 文件。

### Trace JSON 结构

```json
{
  "trace": {
    "traceId": "trace_xxx",
    "name": "Agent workflow",
    "workerPid": 12345,
    "startedAt": "2026-07-20T10:00:00.000Z",
    "endedAt": "2026-07-20T10:05:00.000Z",
    "duration": 300000,
    "status": "ok",
    "spanCount": 10,
    "totalTokens": 100000,
    "sessionId": "uuid",
    "modelInfo": {
      "models": ["auto"],
      "totalInputTokens": 90000,
      "totalOutputTokens": 10000,
      "totalCachedTokens": 50000,
      "callCount": 5
    }
  }
}
```

### 关键字段

| 字段 | 说明 |
|------|------|
| `totalTokens` | 总 Token 消耗 |
| `totalInputTokens` | 输入 Token |
| `totalOutputTokens` | 输出 Token |
| `totalCachedTokens` | 缓存命中 Token |
| `callCount` | API 调用次数 |
| `models` | 使用的模型列表 |
| `startedAt`/`endedAt` | ISO 8601 时间戳 |

---

## 二、WorkBuddy SQLite 数据库

**路径**：`~/.workbuddy/workbuddy.db`

### 主要表结构

#### sessions 表

| 列名 | 类型 | 说明 |
|------|------|------|
| id | TEXT | 会话 UUID |
| cwd | TEXT | 工作目录 |
| title | TEXT | 会话标题 |
| custom_title | TEXT | 用户自定义标题 |
| status | TEXT | 状态（completed/active） |
| created_at | INTEGER | 创建时间戳（毫秒） |
| mode | TEXT | 模式（craft/plan/ask） |
| model | TEXT | 使用的模型 |
| is_background_automation | INTEGER | 是否自动化后台任务 |

#### automation_runs 表

| 列名 | 类型 | 说明 |
|------|------|------|
| thread_id | TEXT | 运行线程 ID |
| automation_id | TEXT | 自动化任务 ID |
| status | TEXT | 状态 |
| result_success | INTEGER | 是否成功 |
| created_at | INTEGER | 创建时间戳 |
| thread_title | TEXT | 运行标题/摘要 |

#### session_usage 表

| 列名 | 类型 | 说明 |
|------|------|------|
| session_id | TEXT | 会话 ID |
| used | INTEGER | 已使用量 |
| size | INTEGER | 总容量 |
| credit_json | TEXT | 信用消耗 JSON |

---

## 三、Usage Log

**路径**：`~/.workbuddy/usage-log.json`

### 结构

```json
{
  "version": 1,
  "skills": {
    "skill-name": {
      "id": "skill-name",
      "type": "skill",
      "lastUsedDate": "2026-07-20",
      "recentDates": ["2026-07-20", "2026-07-19"],
      "firstSeenDate": "2026-06-01"
    }
  },
  "activeDays": ["2026-07-20", "2026-07-19"]
}
```

---

## 四、会话目录

**路径**：`~/WorkBuddy/`

目录命名格式：`YYYY-MM-DD-HH-MM-SS`

### 目录结构

```
2026-07-20-10-00-00/
├── output_file.html
├── report.md
└── .workbuddy/
    └── memory/
        ├── 2026-07-20.md
        └── MEMORY.md
```

### 记忆日志格式

```markdown
# 2026-07-20 工作日志

## 任务标题
- 完成内容 1
- 完成内容 2
```

---

## 五、自动化 API

通过 `automation_update` 工具查询：

```python
automation_update(mode="list")  # 列出所有自动化
automation_update(mode="view", id="...")  # 查看详情
```

### 自动化配置字段

| 字段 | 说明 |
|------|------|
| name | 任务名称 |
| scheduleType | once/recurring |
| rrule | RFC 5545 规则 |
| status | ACTIVE/PAUSED |
| cwds | 工作目录列表 |

---

## 六、官方用量导出（对账源，v1.6.0 / F17）

**路径**：官网手动下载的 `request-usage-*.xlsx`（通常在 `~/Downloads/`）
**接入**：`collect_usage_data.py --import-official <xlsx>`（仅 `--source workbuddy`）
**实现**：`adapters/official_usage.py` —— 纯标准库 `zipfile` + `xml.etree` 解析，**不引入 openpyxl**

### 为什么需要它

本地 trace 的成本是**估算**，存在两类静态价表在数学上无法弥补的偏差：

| 偏差 | 实测（30 日窗口） |
|---|---|
| **盲区**：图像模型、minimax-m3 不进 trace | 漏记 **¥251.74**（8.7%） |
| **标签不分免费/收费**：`hy4-preview` 白天夜间同名 | 12 次调用里 11 次实际 0 积分，静态价表全计成收费 |
| 粒度差：1「请求」≈ 11.9「generation」 | 802 请求 vs 9222 generation |

官方导出的「积分消耗」是**服务端实际计费结果**，是唯一真值。

### 导出格式（实测两版）

| 版本 | 列顺序 |
|---|---|
| 旧版（~2026-09-12） | RequestID / 积分消耗 / 模型 / 客户端 / 时间 |
| 新版（2026-09-13 起） | RequestID / 积分消耗 / **User Prompt** / 模型 / 客户端 / 时间 |

所有单元格均为**明文字符串**（含积分与时间），无共享字符串、无日期序列值；
图像模型「客户端」列为空；时间为**北京时间**（trace 是 UTC，已归一，无 ±8h 错位）。

> ⚠️ **禁止按固定列位解析**：官方 09-13 加列后，按列位解析会把 `User Prompt` 当成模型名
> （调试脚本已踩过一次）。适配器一律**按表头名映射**，缺必需列直接报错。

`credits <= 0` 判为**免费请求**；导入后报告新增 **§3.5 双源对账**与 **L1 真值横幅**。

---

## 七、数据来源与已知偏差

> 回答一个问题：**报告里的数字，哪些能信、哪些只能看结构。**

### 7.1 trace 盲区（官方有 / trace 无 → 成本被低估）

| 模型 | 性质 | 漏记 |
|---|---|---|
| `hunyuan-image-alpha` | 图像生成 | ¥119.91 |
| `minimax-m3` | **WorkBuddy 客户端却不被 trace 记录** | ¥120.39 |
| `hunyuan-image-v3.0-art` | 图像生成 | ¥11.44 |
| **合计** | | **¥251.74（8.7%）** |

> 早期版本曾把 `deepseek-v4-pro` 也列为盲区，实为 VSCode / Codebuddy 客户端调用，已剔除。

### 7.2 trace 独有（官方无 → 不是漏记，别去对账）

本地模型（`custom-local:*`）、限免入口（`hy3` 至 2026-10-31）、
路由别名（`balanced-model` / `fast-model`）、免费时段（`hy4-preview` 夜间 23:00–08:00）。

### 7.3 模型名不体现「是否免费」

| 时间 | 模型 | 时段 | 积分 |
|---|---|---|---|
| 2026-09-13 23:53 | `hy4-preview` | 夜间 | 0（免费） |
| 2026-09-12 11:32 | `hy4-preview` | 白天 | 43.40（收费） |
| 2026-08-29 02:42 | `hy4-preview-x` | 夜间 | 13.52（**`-x` 不参与夜间免费**） |

→ **绝不能靠模型名或调用时段推断是否免费**，只能看官方积分。
→ `hy4-preview-x` 是「免费额度用尽后的收费变体」，单价维持 x0.29，**不得置 0**。

### 7.4 怎么办

1. **要准确金额** → 加 `--import-official <xlsx>`，切 L1 真值 + 出 §3.5 双源对账。
2. **只做趋势分析** → 默认 L2 即可，但别把金额当账单。
3. 受时段减免影响的模型已写入 `pricing.json` 的 `low_confidence` 段，L2 下标 ⚠ 并剔除出「最贵模型」结论。

---
