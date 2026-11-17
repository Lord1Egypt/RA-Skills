# coze 端修复清单（Backlog）

> 收录「根因在 coze 侧 R 引擎 / coze 节点、需下次 coze 部署时采纳」的修复项。
> 每项含：现状根因、目标改法（可直接落地）、验证方式、与服务端已有兜底的关系。
> 部署 coze 属人工操作，AI 不触碰 adapters/coze/ 的部署链路；本清单是部署时的作业依据。

---

## D1A：run_task.R 三分支对齐——布尔图开关「提前 return 只回图」丢主结果

- **状态**：**R 引擎源码已实现（v5.13.24，2026-10-22）；待 coze 打包部署**（源码与
  云端共用同一份 `adapters/coze/src/r_engine/run_task.R`，本次改动已落在源码上，
  本机 R 后端直跑已验证；云端需经人工打包部署后才生效）
- **登记日**：2026-10-21 ｜ **实现日**：2026-10-22
- **缺陷编号**：D1（工作台测试报告 §2 已知缺陷清单）
- **优先级**：P1（主结果丢失——用户勾一个图开关就看不到样本量）

> **实现说明（2026-10-22 更新）**：本项已按下方「目标改法」落盘到
> `run_task.R`——新增 `.has_solve_anchor()`（dispatch 之前定义），三分支改为
> 「有锚 → 图/警告累积 + continue；无锚 → 保留纯图 return」，并把 has_curve_arg
> 分支的内联锚判定改为复用该函数。本机验证（`CTSS_D1_SPLIT=0` 关闭服务端编排
> 直达引擎）：A 仅 power_time_seq（ttest_ind）→ status=warn + 主结果 n=64 保留 +
> warning；B 三开关全开 → 主结果 + 分布图 + 双 warning；C 纯图无锚 → 原语义不变。
> **剩余工作仅剩 coze 打包部署 + 云端回归**。

### 现状（根因）

`adapters/coze/src/r_engine/run_task.R` 的 `dispatch()` 中，三个图开关分支仍是
「提前 return、只回图」的旧语义：

| 分支 | 行号（约） | 触发键 | 现状 |
|---|---|---|---|
| ① H0/H1 分布重叠图 | 1087-1100 | `p$plot_dist` | `.run_dist` 后**直接 return**，只回 1 张图 + 一行 text，主求解（样本量 n）整个丢失 |
| ③ 生存随访-效能曲线 | 1102-1115 | `p$curve_power_time_seq` | 同上（`.run_surv_time` 后直接 return） |
| ④ 效能热力图 | 1117-1130 | `p$curve_heatmap` | 同上（`.run_heatmap` 后直接 return） |

2026-10-07 重构只把**序列曲线**参数（`curve_n_seq` / `curve_power_seq` /
`curve_effect_seq`，即 `has_curve_arg` 分支，1136-1165 行）改成「主求解锚存在时
主求解 + 曲线累积到 figs，continue 主求解；无锚时保留纯曲线提前 return」，
漏改这三个布尔/序列图开关分支。云端 2026-10-21 同参裁定同缺陷。

### 目标改法（与 has_curve_arg 分支同构）

三个分支统一改为「有主求解锚 → 图累积 + continue；无锚 → 保留纯图提前 return」：

```r
# ① H0/H1 分布重叠图（改写后）
if (!is.null(p$plot_dist)) {
  suppressMessages(library(pwr))
  dd <- .run_dist(test, p)
  if (!dd$ok) {
    if (.has_solve_anchor(p)) {
      warns <- c(warns, paste0("分布重叠图生成失败：", dd$msg))   # 不阻断主结果
    } else {
      return(list(status = "unknown_task", stats = NULL, narrative = "",
                  figures = list(), warnings = c(), notes = dd$msg, repro = NULL))
    }
  } else if (!is.null(dd$figure)) {
    figs <- c(figs, list(dd$figure))
    warns <- c(warns, dd$warns %||% c())
  }
}
```

③④ 同构（`.run_surv_time` / `.run_heatmap` 各自分支）。锚判定抽取复用：

```r
.has_solve_anchor <- function(p) {
  pw <- suppressWarnings(as.numeric(p$power %||% NA_real_))
  nb <- suppressWarnings(as.numeric(p$nobs %||% NA_real_))
  !is.na(pw) || !is.na(nb)
}
```

（即把 1139-1141 行内联的锚判定提为函数，三分支 + has_curve_arg 共用。）

### 落地要点

1. 三个分支**只删提前 return、改累积**，不动 `.run_dist` / `.run_surv_time` /
   `.run_heatmap` 本体（含各自的 test 适用范围校验，如 surv_time 仅 survival）。
2. dispatch 尾部（2632-2637 行）统一返回已消费累积后的 `figs`，无需再改；
   `explicit_fig` 守卫（2622-2625 行）已含这三个键，显式开开关时跳过默认图集
   的语义天然保持。
3. 无锚（纯图请求，如只给 plot_dist 不给 power/nobs）保留提前 return 语义，
   与 has_curve_arg 的「纯曲线模式」一致，零回归。
4. 改完跑 `tests/` 下既有 coze 用例（若有用例覆盖布尔开关），补 3 个用例：
   `ttest_ind + plot_dist + power`、`survival + curve_power_time_seq + power`、
   `ttest_ind + curve_heatmap + curve_n_seq + curve_effect_seq + power`，
   断言「主结果 n 在 + 图在」。

### 与服务端兜底的关系

工作台 server.py 已有**服务端拆分编排**兜底（v5.13.23，`_d1_split_specs` /
`_compute_fig_split`：主求解去开关 + 每开关单开图 spec，compute_batch 一次
调用合并）。本项部署后：

- 服务端编排**可继续保留作双保险**（R 端原生累积后，拆分合并结果等价，代价是
  多 1-3 次 R 调用）；也可在云端回归验证通过后移除，减调用开销。
- 建议顺序：先部署 D1A → 云端回归（C1/C2/C5 同参）→ 再评估服务端编排去留。
  **不要在 D1A 未验证前移除服务端编排。**
- v5.13.24 起服务端编排新增总开关 `CTSS_D1_SPLIT=0`：关闭编排、直达引擎，用于
  验证 R 端原生修复（否则编排会掩盖 R 端行为）。回归时应两模式各跑一遍：
  `CTSS_D1_SPLIT=0`（验 R 端）与默认（验编排兼容 + 云端等价路径）。
- 编排侧同步加了 `_d1_merge_fig_text` 行级去重：R 端修复后图 spec 会连带带回
  主求解文本，去重复可避免主结果在页面上出现两次。

---

## 部署批次 v5.13.24–v5.13.26（2026-10-22：**已部署 + 云端端到端回归全部通过，闭环**）

> R 侧改动已全部落盘并通过本机 R 后端回归（25 用例 + 65 方法）。**一次部署覆盖全部**。
>
> ### 部署状态（2026-10-22 终态）
> - ✅ 已上传云端并部署；云端实测发现并热修 `.event_prob` 的 NULL 防护（已回写镜像）
> - ✅ **云端端到端回归 12 项全部通过**（`cloud_retest_51326.py`，经 CozeBackend 全链路
>   打 https://ct-samplesize.coze.site/run）：响应含 5.13.26 版本串；基线 n=64 无漂移；
>   D1 主结果+7 图；D4 93.4/312；D5 0.3137 vs 0.0488；D6 0.7533 vs 0.77；
>   B 方案 survival 529(0.2337)/626(0.1974)、ni 730(0.3402)/1072(0.2318)——数值与本机逐项一致
> - **包（加固版，与云端一致）**：`adapters/coze/_archive_20260830/coze_project_5.13.26.zip`
>   396.9 KB · 74 文件 · MD5 `e8ff520dabc024c3e9bad77cfd0f9294`
> - 独立核验：无 .bak/tests/__pycache__ 泄漏；`manifest.json` version=5.13.26；
>   `_version.py` COZE_VERSION=5.13.26
> - 服务端编排（server.py D1B）继续保留作双保险；`CTSS_D1_SPLIT=0` 可隔离排查
> - 构建前已把 6 个 .bak_* 备份移入 `_archive_20260830/bak_20261022/`（避免进包）

### 涉及的 coze 共享源码（均在 adapters/coze/src/r_engine/）

| 文件 | 版本 | 改动 |
|---|---|---|
| `run_task.R` | v5.13.24 | D1 根因：新增 `.has_solve_anchor()`；`plot_dist` / `curve_power_time_seq` / `curve_heatmap` 三分支改「有锚 → 图累积 + continue」，不再提前 return 丢主结果 |
| `run_task.R` | v5.13.25 | D4：cox_covariate 求 n 分支拆开 `list(d, n)`（此前 narrative 渲染成 `93.350941798387 312`）；D5：assurance 的 margin 两键兼收（`margin_assurance %||% margin`）；D6：adaptive_simulate 的 `n_simulations %||% sim_n` |
| `run_task.R` | v5.13.26 | B 方案：survival 求 n 分支接入 `.event_prob`，narrative/stats 增加「期望事件比例」 |
| `samplesize_functions.R` | v5.13.25 | D6：gsd_survival_sim / gsd_hazard_sim 的 `n_simulations %||% n_sim` |
| `samplesize_functions.R` | v5.13.26 | B 方案：新增 `.event_prob()`；重写 `ss_survival_logrank`（删恒返 NaN 的 TrialSize 分支）；`ss_ni_survival`（Cox.NIS d 参数改传 P）、`ss_surv_equiv` / `ss_surv_sup`（`/event_rate` → `/P`） |
| `common.R` | v5.13.26 | 新增 `label.event_prob`（zh/en 两处）；修 `10%%` → `10%`（label 未经 sprintf，不应双写） |

### 无需部署（纯本地）的同期改动

`workbench/server.py`（D1B 编排 + CTSS_D1_SPLIT 开关 + D2 PNG）、`adapters/coze_client.py`（D3 warnings 通道）、`form_schema.py`（survival 的 followup_time 必填）、`tests/coze_cases/_contract_index.json`（survival.required 补登 followup_time）、workbench 三份 HTML（figHTML 渲染）。

### 部署后必须做的云端回归（通过前不得移除服务端编排）

| 项 | 用例 | 期望 |
|---|---|---|
| D1 根因 | C1（ttest_ind 三开关全开）/ C2 / C5 | 主结果 n 在 + 全部图在；单次调用即出 |
| D4 | cox_covariate 求 n（HR=2.0） | 文本「所需事件数 (d): 93.4」+「n (合计): 312」，stats.n 为整数 |
| D5 | assurance margin=0.1 vs 0.3 | 保证度随 margin 变化，文本界值正确 |
| D6 | gsd_survival_sim n_sim=150 vs 400 | 经验功效随模拟次数变化 |
| B 方案 | survival / ni_survival / survival_equivalence / survival_superiority，改 accrual_time 与 followup_time | n 随之变化，方向：A↑→n↑、F↑→n↓；narrative 出现「期望事件比例」 |
| 回归保护 | ttest_ind 基线（每组 n=64）等非生存方法 | 数值与部署前一致 |

### 注意事项

1. **口径变更**：B 方案后四个生存方法的样本量变大（更保守）。若云端有旧报告缓存/对数，解读时注意版本分界（v5.13.26）。
2. `TrialSize` 包仍需要（ni_survival 的 Cox.NIS 在用）；`rpact` 仍需要（survival_exact / gsd）。本轮没有新增包依赖。
3. 回退：三个 R 文件均有 `.bak_d1a` / `.bak_d4d6` 快照；契约 JSON 有 `.bak_b`。
4. 部署后若发现异常，服务端编排（server.py）可用 `CTSS_D1_SPLIT=0` 隔离 D1 问题排查。

---

## （模板）新增条目格式

```
## DX：一句话标题
- **状态**：待采纳 / 已采纳（版本+日期） / 已驳回（原因）
- **缺陷编号**：与测试报告 §2 对应
- **优先级**：P0 卡死 / P1 功能缺损 / P2 体验
### 现状（根因）…… ### 目标改法…… ### 落地要点……
### 与服务端兜底的关系……（若有）
```
