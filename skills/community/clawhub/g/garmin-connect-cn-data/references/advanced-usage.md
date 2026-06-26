# 端到端批量测试模板

> 本文档被 `SKILL.md` 的"端到端批量测试"节引用。
> **使用前请先完成 SKILL.md 中"环境准备"节的检测，确定 SKILL_DIR 和 RUNNER。**
> 以下所有 `<RUNNER>` 均替换为你确定的运行方式，`<SKILL_DIR>` 替换为技能目录绝对路径。

---

## 统一原则

1. 日期使用绝对日期（`YYYY-MM-DD`），避免"今天/最近几天"的歧义。
2. 每一步都检查 JSON 的 `status` 字段，只有 `success` 才进入下一步。
3. 长周期查询和批量导出必须先落盘，再做统计与抽样。
4. FIT 解析统一使用 `scripts/fit_file_parser.py` + `fitparse`，不要引入其他 FIT 解析库。

---

## 端到端测试流程示例（长周期 + 多跑步 + 赛事导出）

### 1) 准备测试目录

```bash
TEST_ROOT="/tmp/garmin-cn-test-$(date +%Y%m%d)"
mkdir -p "$TEST_ROOT"/{raw,exports,analysis,logs}
```

### 2) 登录与会话检查

```bash
<RUNNER> login <邮箱> <密码> > "$TEST_ROOT/raw/01_login.json"
<RUNNER> status > "$TEST_ROOT/raw/02_status.json"
```

### 3) 长周期健康数据

将 `<START_DATE>` / `<END_DATE>` 替换为实际日期范围（如 `2025-01-01` / `2026-03-31`）：

```bash
<RUNNER> health --start <START_DATE> --end <END_DATE> --metrics hrv,rhr,stress,bb,spo2,respiration > "$TEST_ROOT/raw/03_health_long.json"
<RUNNER> sleep --start <START_DATE> --end <END_DATE> > "$TEST_ROOT/raw/04_sleep_long.json"
```

### 4) 跑步记录（季度 + 宽区间）

```bash
<RUNNER> activities --start <Q_START> --end <Q_END> --type running > "$TEST_ROOT/raw/05_running_quarter.json"
<RUNNER> activities --start <START_DATE> --end <END_DATE> --type running > "$TEST_ROOT/raw/06_running_wide.json"
```

### 5) 赛事样本导出（全马/半马）

先在宽区间结果中筛选：
- 全马：`distance_km >= 40`
- 半马：`20 <= distance_km <= 22`

对每个活动 ID 执行：

```bash
AID=<activity_id>
OUT="$TEST_ROOT/exports/$AID"
mkdir -p "$OUT"

<RUNNER> export "$AID" --format fit --output "$OUT"
<RUNNER> export "$AID" --format gpx --output "$OUT"
<RUNNER> export "$AID" --format tcx --output "$OUT"
<RUNNER> export "$AID" --format csv --output "$OUT"
```

### 6) 公里级抽查（km_1 / km_5 / km_10 / km_last）

优先使用活动详情中的圈段数据：

```bash
<RUNNER> detail <activity_id> > "$TEST_ROOT/raw/detail_<activity_id>.json"
```

再用 FIT 解析进行交叉校验：

```bash
<FIT_RUNNER> <SKILL_DIR>/scripts/fit_file_parser.py <fit_file_path> --targets 1,5,10,last --pretty --output "$TEST_ROOT/analysis/fit_parse_<activity_id>.json"
```

---

## 结果判读口径

1. `garmin_cli.py` 成功：`status == "success"`
2. 导出成功：`status == "success"` 且 `data.file_path` 存在、`data.size_bytes > 0`
3. `fit_file_parser.py` 重点字段：
   - `parse.metrics.hr`
   - `parse.metrics.cadence`
   - `parse.metrics.stride`
   - `km_samples`

字段语义：
- `direct`：原生字段直接可得
- `estimated`：由距离 + 时长 + 步频估算
- `unavailable`：不可得

---

## 统一清理模板（仅保留最终摘要）

```bash
# 假设最终摘要为 $TEST_ROOT/analysis/final_summary.json
rm -rf "$TEST_ROOT/raw" "$TEST_ROOT/exports" "$TEST_ROOT/logs"
find "$TEST_ROOT/analysis" -type f ! -name "final_summary.json" -delete
```

---

## 统一失败分类

| 错误码 | 含义 |
|--------|------|
| `auth_failed` | 登录失败或凭据不可用 |
| `api_failed` | Garmin 接口调用失败 |
| `file_corrupted` | 导出文件损坏或不可读 |
| `parse_failed` | 文件可读但字段提取失败 |
| `env_incompatible` | 运行环境不兼容（重新检测 RUNNER） |
