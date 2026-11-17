# ct-samplesize 进阶参考（开发者 / 调试用）

> 以下面向需要调试、复现或二次开发的用户。普通使用者无需阅读；日常使用请见 README_zh-CN.md 第一至四节。

### 5.1 CLI 命令示例（完整 65 种）

技能在底层通过 `scripts/samplesize_power.py` 生成并执行 R 代码。如果你要自己复现、调试或批量跑，可直接调用 CLI（普通对话使用者无需此步）：

```bash
# === 连续变量 ===
python scripts/samplesize_power.py --test ttest_ind --effect 0.5 --power 0.8
python scripts/samplesize_power.py --test ttest_paired --effect 0.5 --power 0.8
python scripts/samplesize_power.py --test anova --effect 0.25 --k_groups 3 --power 0.8
python scripts/samplesize_power.py --test equivalence --margin 2.0 --effect 3.0 --power 0.8
python scripts/samplesize_power.py --test mixed_model --effect 0.5 --nsim 500

# === 二分类 ===
python scripts/samplesize_power.py --test proportion_two --p1 0.3 --p2 0.15 --power 0.8
python scripts/samplesize_power.py --test non_inferiority --margin 0.1 --p1 0.85 --p2 0.80 --power 0.8
python scripts/samplesize_power.py --test be_tost --theta0 0.95 --cv 0.25 --design "2x2"
python scripts/samplesize_power.py --test superiority_margin --sup_margin 0.05 --p_control_sup 0.3 --delta_sup 0.15

# === 计数 ===
python scripts/samplesize_power.py --test poisson --lambda1 0.05 --lambda2 0.03 --t1 2 --t2 2 --power 0.8
python scripts/samplesize_power.py --test vaccine_efficacy --ve_control 0.02 --ve_treatment 0.005 --power 0.8

# === 生存 ===
python scripts/samplesize_power.py --test survival --hazard_ratio 0.75 --power 0.85
python scripts/samplesize_power.py --test survival_exact --hr_exact 0.75 --accrual_exact 12 --followup_exact 0.85
python scripts/samplesize_power.py --test ni_survival --ni_margin_surv 1.25 --accrual_time 12 --followup_time 12

# === 生存 — PASS 扩展（v3.5）===
python scripts/samplesize_power.py --test survival_equivalence --eq_margin_surv 1.25 --hr_expected 1.0 --accrual_time 12 --followup_time 12 --event_rate 0.7 --power 0.8
python scripts/samplesize_power.py --test survival_superiority --sup_margin_surv 0.8 --sup_hr 0.67 --accrual_time 12 --followup_time 12 --event_rate 0.7 --power 0.8
python scripts/samplesize_power.py --test cox_covariate --cox_hr 2.0 --cox_r2 0.3 --cox_prev 0.5 --cox_event_prop 0.3 --power 0.8
python scripts/samplesize_power.py --test survival_one_sample --median0 12 --median1 18 --accrual_time 12 --followup_time 12 --power 0.8
python scripts/samplesize_power.py --test competing_risks --ci_control 0.2 --ci_treatment 0.1 --power 0.8
python scripts/samplesize_power.py --test recurrent_events --rate_control 1.0 --rate_ratio 0.6 --recur_followup 2 --power 0.8
python scripts/samplesize_power.py --test survival_historical --hist_median 12 --new_median 18 --hist_n 100 --accrual_time 12 --followup_time 12 --power 0.8

# === 诊断/方法比对 ===
python scripts/samplesize_power.py --test roc --auc0 0.5 --auc1 0.75 --power 0.8
python scripts/samplesize_power.py --test bland_altman --sd_diff 5 --w 2.5

# === 特殊设计 ===
python scripts/samplesize_power.py --test cluster --icc 0.05 --m 30 --n_indiv 64
python scripts/samplesize_power.py --test multiple_endpoints --effect 0.3 --correlation 0.5
python scripts/samplesize_power.py --test bayesian --prob_control 0.3 --prob_treatment 0.15 --prior_a0 0.5
python scripts/samplesize_power.py --test dose_escalation --n_doses 5 --target_dlt 0.33

# === 高级终点 (v3.3) ===
python scripts/samplesize_power.py --test win_ratio --win_ratio_theta 1.5 --n_sim 1000
python scripts/samplesize_power.py --test must_win --n_endpoints_must 3 --effect_must 0.3 --correlation_must 0.5
python scripts/samplesize_power.py --test historical_controls --historical_response 15 --historical_n 100 --a0_borrowing 0.5
python scripts/samplesize_power.py --test mams --n_arms_mams 3 --n_stages_mams 2 --delta_effect 0.3
python scripts/samplesize_power.py --test conditional_power --timing 0.5 --observed_effect 0.2 --planned_effect 0.3
python scripts/samplesize_power.py --test assurance --n_assurance 100 --n_sim_assurance 5000
python scripts/samplesize_power.py --test dunnett --n_groups_dunnett 3 --n_control_dunnett 50 --effect_dunnett 0.4
python scripts/samplesize_power.py --test mediation --a_path 0.3 --b_path 0.3
python scripts/samplesize_power.py --test group_sequential --n_interim 1 --effect_gs 0.4
python scripts/samplesize_power.py --test adaptive --n_stages_adapt 2 --effect_adaptive 0.4

# === 组序贯模拟 (v3.7) — 蒙特卡洛验证 ===
python scripts/samplesize_power.py --test gsd_survival_sim --n_interim 2 --gs_median_control 12 --hazard_ratio 0.7 --accrual_time 12 --followup_time 12 --power 0.8 --n_simulations 2000 --sim_seed 1
python scripts/samplesize_power.py --test gsd_hazard_sim --n_interim 2 --gs_median_control 12 --hazard_ratio 0.7 --accrual_time 12 --followup_time 12 --nobs 180

# === 组序贯（PASS，rpact 驱动）— v3.6 ===
python scripts/samplesize_power.py --test gsd_proportion --n_interim 1 --p1 0.7 --p2 0.5 --power 0.8     # 正向 -> 每组 n≈75
python scripts/samplesize_power.py --test gsd_survival  --n_interim 1 --gs_median_control 12 --hazard_ratio 0.7 --accrual_time 12 --followup_time 12 --power 0.8   # 正向 -> 每组 n≈178（198 事件）
python scripts/samplesize_power.py --test gsd_hazard    --n_interim 1 --gs_median_control 12 --hazard_ratio 0.7 --accrual_time 12 --followup_time 12 --power 0.8   # 正向 -> 每组 n≈178
python scripts/samplesize_power.py --test gsd_poisson   --n_interim 1 --gs_rate1 0.6 --gs_rate2 1.0 --gs_poisson_time 2 --power 0.8   # 正向 -> 每组 n≈33

# 消耗函数 + futility（5 类组序贯共用）
python scripts/samplesize_power.py --test group_sequential --n_interim 2 --effect_gs 0.4 --spending_func Pocock --futility --power 0.8
python scripts/samplesize_power.py --test group_sequential --n_interim 1 --effect_gs 0.4 --spending_func WT --wt_delta 0.25 --power 0.8   # Wang-Tsiatis Δ=0.25；不可与 --futility 同用

# 反向：给定 n -> 可达效能（与正向 n 自洽）
python scripts/samplesize_power.py --test gsd_proportion --n_interim 1 --p1 0.7 --p2 0.5 --nobs 75        # 反向 -> 效能≈0.80
python scripts/samplesize_power.py --test gsd_survival  --n_interim 1 --gs_median_control 12 --hazard_ratio 0.7 --accrual_time 12 --followup_time 12 --nobs 178   # 反向 -> 效能≈0.82
```

### 5.2 双向求解：给定样本量求检验效能

默认（`--power` 或省略）为**正向**：给定目标效能求解所需样本量 `n`。
传入 `--nobs N` 切换为**反向**：给定样本量求解可达检验效能（power）。
`--power` 与 `--nobs` **互斥**。

```bash
# 给定 n=50/组，求两独立样本 t 检验可达效能
python scripts/samplesize_power.py --test ttest_ind --effect 0.5 --nobs 50

# 给定 n=20/序列，求生物等效 TOST 可达效能
python scripts/samplesize_power.py --test be_tost --nobs 20

# 给定 n=100/组，求多臂多阶段(MAMS)设计可达效能
python scripts/samplesize_power.py --test mams --nobs 100
```

**覆盖全部 65 种检验类型。** 反向求解策略：优先使用原生包反解（`pwr.*`、`PowerTOST::power.TOST`、`rpact::getPowerMeans/getPowerSurvival`）；自写检验采用解析逆公式（非中心参数逆推 `z_b` 后 `power = pnorm(z_b)`）；精度型检验（`bland_altman`）回报可达 CI 半宽而非效能。

### 5.3 曲线模式：Power / 样本量曲线

在双向求解基础上，支持**批量绘制曲线**，直观展示样本量与检验效能的关系。

- `--n_seq "20,40,200"` → **Power 曲线**（x=样本量，y=效能）
- `--n_seq "20:20:200"` → 同上，但按「起:步:止」自动展开
- `--power_seq "0.6:0.05:0.95"` → **样本量曲线**（x=效能，y=样本量）
- `--plot_effects "0.3,0.5,0.8"` → 多效应量叠加多条曲线（敏感性分析）
- `--out path.png` → 指定 PNG 输出路径（默认写入系统临时目录）

```bash
# Power 曲线：n = 20,40,...,200，叠加 3 条效应量曲线
python scripts/samplesize_power.py --test ttest_ind --n_seq "20:20:200" --plot_effects "0.3,0.5,0.8" --out power_curve.png

# 样本量曲线：power = 0.6,0.65,...,0.95
python scripts/samplesize_power.py --test ttest_ind --power_seq "0.6:0.05:0.95" --out n_curve.png
```

**曲线模式支持 9 种核心检验类型**：ttest_ind、ttest_paired、ttest_one、anova、proportion_one、proportion_two、survival、equivalence、be_tost（与 R 引擎 `.curve_solvers` 一致）。曲线复用与单点求解**同一套已验证公式**，数值完全一致。其余所有检验类型（含 odds_ratio、risk_ratio、roc、poisson、non_inferiority、superiority_margin、ni_survival、vaccine_efficacy、group_sequential、survival_exact、mams、dunnett、mixed_model、bayesian、win_ratio 等）仅支持单点求解，曲线请求会返回清晰的「curve not supported」提示。

### 5.4 核心公式

| 场景 | 公式 |
|:---|:---|
| 独立样本 t（等样本） | $n_1 = 2(\frac{Z_{1-\alpha/2} + Z_{1-\beta}}{d})^2$ |
| 率比较（arcsin） | $n = 2(\frac{Z_{1-\alpha/2} + Z_{1-\beta}}{h})^2$ |
| 生存（Schoenfeld） | $d = \frac{(Z_{1-\alpha/2} + Z_{1-\beta})^2}{(\log HR)^2}$ |
| 生存等效（TOST/log-HR） | $D = \frac{[2(Z_{1-\alpha} + Z_{1-\beta})]^2}{(\log\delta_E)^2},\ n_{pg}=\frac{D/2}{e}$ |
| 含界值生存优效 | $\delta=\log\delta_S-\log HR;\ D = \frac{[2(Z_{1-\alpha} + Z_{1-\beta})]^2}{\delta^2}$ |
| Cox 含协变量（Vittinghoff） | $d = \frac{(Z_{1-\alpha/2} + Z_{1-\beta})^2}{(1-R^2)\,p(1-p)\,(\log HR)^2}$ |
| 单组指数生存 | $\lambda_j=\frac{\log2}{m_j},\ e_j=1-e^{-\lambda_j\bar t},\ n=\lceil\frac{\mu_1}{e_1}\rceil$ |
| 竞争风险（CIF） | $n_{pg}=\lceil\frac{(Z_{1-\alpha/2}+Z_{1-\beta})^2[\pi_C(1-\pi_C)+\pi_T(1-\pi_T)]}{(\pi_C-\pi_T)^2}\rceil$ |
| 复发事件（Poisson） | $n_{pg}=\lceil\frac{(Z_{1-\alpha/2}+Z_{1-\beta})^2(\lambda_1+\lambda_2)}{t(\lambda_1-\lambda_2)^2}\rceil$ |
| 历史对照 logrank | 单组 vs 历史中位 $m_H$；同单组指数结构 |
| ROC（Obuchowski） | $n = \frac{(Z_{1-\alpha/2} + Z_{1-\beta})^2}{4(\arcsin\sqrt{AUC_1} - \arcsin\sqrt{AUC_0})^2}$ |
| 类随机 DEFF | $DEFF = 1 + (m - 1) \times ICC$ |
| Bland-Altman | $n = 2(\frac{Z_{1-\alpha/2} \times SD_{diff}}{W})^2$ |
| Win-Ratio（近似） | $n = \frac{(Z_{1-\alpha/2} + Z_{1-\beta})^2}{(\ln WR)^2 / SE_{approx}^2}$ |
| Must-Win 膨胀因子 | $n = n_{single} \times [1 + (k-1)\rho \times 0.5]$ |
| MAMS（Bonferroni） | $n = \frac{(Z_{1-\alpha/(2k)} + Z_{1-\beta})^2}{\delta^2}$ |
| 确信度 | $P(\text{success}) = \frac{1}{N}\sum_{i=1}^N I(\text{trial}_i \text{ significant})$ |

**完整公式推导：** `references/formulas.md` | **扩展函数：** `references/extended_functions.md`

### 5.5 系统要求

| 组件 | 要求 |
|:---|:---|
| Python | ≥ 3.8，**纯标准库**——无任何第三方运行时依赖 |
| R | ≥ 4.1.0——**仅在 coze 服务端运行**；发布技能不需要本地 R（dev 后端 `adapters/local-r/` 除外） |
| 操作系统 | Windows / macOS / Linux |

R 包**不需要全部预装**——发布技能中全部 R 计算在 **coze 服务端**完成，本地无需安装任何 R 包。注意：一键安装旗标 `--install-all-packages` 已于 **v5.0.2 移除**。可选的本地 R 开发后端（`adapters/local-r/`，不随发布包分发）请按提示使用 `install.packages()` 代码片段安装。
**无需 R 包的检测类型：** `poisson`, `cluster`, `bland_altman`, `vaccine_efficacy`, `bayesian`, `dose_escalation`, `survival`（仅 Schoenfeld）, `must_win`, `multiple_endpoints`, `assurance`, `dunnett`, `mediation`, `win_ratio`

### 5.6 常见错误

| 错误 | 解决方案 |
|:---|:---------|
| "Rscript not found" | 安装 R 或指定路径（仅 dev 后端需要） |
| "package not found" | install.packages("xxx")（仅 dev 后端需要） |
| coze 不可达 | 检查网络/代理后重试（serverless 冷启动可能 >15s） |
| simr timeout | 减少 --nsim 或简化模型 |
| BuyseTest convergence | 增加 n_sim，检查先验分布 |
| rpact error | 更新 rpact 至最新版本 |

### 5.7 文件结构

```
ct-samplesize/
├── SKILL.md                  ← 技能定义（默认跟随 OS 语言设定输出中文或英文，提示词可强制切换）
├── README.md                 ← 英文版说明
├── README_zh-CN.md           ← 中文版说明
├── ADVANCED.md               ← 英文进阶参考（本文的英文镜像）
├── ADVANCED_zh-CN.md         ← 中文进阶参考（本文）
├── AGENTS.md                 ← 自改进约定（英/中双语）
├── CHANGELOG.md              ← 版本 / 整改记录
├── requirements.txt
├── .gitignore
├── assets/
│   ├── icon.svg              ← A 级绿色图标（104×104，三要素模板）
│   ├── icon_4x.png / icon_8x.png
│   └── ct-samplesize_4x.png / ct-samplesize_8x.png
├── scripts/
│   ├── samplesize_power.py   ← CLI：65 种检验计算（coze 后端；v5，纯标准库）
│   ├── compute_backend.py    ← 后端抽象：CozeBackend（唯一后端，无本地兜底）
│   ├── i18n.py               ← 中英切换 helper（复制自 ct-base）
│   └── office_to_md.py       ← 用户上传 docx/pptx → md（ct-base §6.7）
├── adapters/
│   ├── coze_client.py        ← coze 出站计算客户端（仅试验设计参数）
│   ├── coze_token_embedded.py← 公共凭据库（XOR+base64，§5）
│   ├── bug_report.py         ← 技能错误报告客户端（11 键信封，§20.3）
│   └── rendering.py          ← 图形渲染管线（SVG 内联 / PNG 兜底）
└── references/
    ├── language_policy.md    ← 双语策略（复制自 ct-base）
    ├── report_template.md    ← 报告骨架（复制自 ct-base）
    ├── units.md              ← 原子任务单元索引（BASE.md §6）
    ├── menu.md               ← 权威分层检验菜单（终点主树 + 设计族索引）
    ├── cli_examples.md       ← 完整 65 种检验 CLI 示例 + 双向求解
    ├── operation_sop.md      ← 端到端操作 SOP + 故障排查
    ├── data_format_guide.md  ← 65 种检验数据框架 + 示例
    ├── formulas.md        ← 公式推导
    ├── extended_functions.md ← 扩展函数清单
    ├── r_packages.md      ← R 包参考（20+ 包）
    ├── python_usage.md       ← Python 速查
    ├── r_usage.md            ← R 速查
    ├── effect_size.md        ← 效应量标准（d/f/h + Z 值表）
    ├── examples.md           ← 3 个完整走查（率比较 / GS / 非劣效）
    └── adaptive_simulator.md ← 自适应蒙特卡洛仿真器指南
```

### 5.8 参考文献（R 包）

- rpact: https://www.rpact.org/
- gsDesign: https://keaven.github.io/gsDesign/
- TrialSize: https://cran.r-project.org/web/packages/TrialSize/
- PowerTOST: https://cran.r-project.org/web/packages/PowerTOST/
- simr: https://github.com/pitakakariki/simr/
- powerSurvEpi: https://cran.r-project.org/web/packages/powerSurvEpi/
- BayesCTDesign: https://cran.r-project.org/web/packages/BayesCTDesign/
- BuyseTest: https://cran.r-project.org/web/packages/BuyseTest/
- RBesT: https://cran.r-project.org/web/packages/RBesT/
- MCPAN: https://cran.r-project.org/web/packages/MCPAN/
- powerMediation: https://cran.r-project.org/web/packages/powerMediation/
- CRAN ClinicalTrials View: https://cran.r-project.org/web/views/ClinicalTrials.html


## 效应量参考库：命令行入口（自 README 4.14 移入，2026-10-22 v5.13.27 规范对齐）

展示模式（绝不静默代入）：

```bash
python scripts/samplesize_power.py --test ttest_ind \
    --effect-ref references/effect_size_benchmarks/肝细胞癌__OS.json \
    --ta "肝细胞癌" --endpoint "OS" --show-assumptions
```

显式采纳（来源可审计）：

```bash
python scripts/samplesize_power.py --test ttest_ind \
    --effect-ref references/effect_size_benchmarks/肝细胞癌__OS.json \
    --adopt-ref conservative --sd 10 --side two --power 0.8
```

- 采纳后：来源与 `basis` 打印到 stdout、写入假设清单 `references` 段，可复现 R 代码注释标注来源。
- 敏感场景可 `--adopt-ref low|high` 做三点敏感性（CI 下界 / 中位 / 上界各算一次），或 `--adopt-ref <序号>` 指定单一来源。
- 可采纳的参考类型（`param`/`scale`）：`effect`（d/MD/SMD，服务 ttest / anova / meta_planning）、`hazard_ratio`（HR，服务生存检验）、`odds_ratio`（OR，服务 ci_or / regression_logistic）、`risk_ratio`（RR，服务 ci_rr / regression_poisson / rates_ext；OR/RR 参考经 `--effect` 落地，引擎比值通道读 `effect`）。
- 候选条目核实后 `--confirm` 入库 `references/effect_size_benchmarks/`；检索由 `adapters/ma_extractor.py` 完成。


## 工作台（Workbench）启动与功能概览（2026-10-22 自 README 第七节收敛）

- **在线门户（免安装）**：https://ct.medstatstar.com —— 与本地工作台同一套功能与 65 种检验目录。
- **本地启动**：`cd workbench && python server.py 8790`（默认连真实 coze R 引擎；
  `CTSS_COZE_MOCK=1` 离线演示模式；`CTSS_BACKEND=local_r` 走本机 R 开发后端，仅 dev/回归用）。
- **核心功能**：自然语言一键识别（零 LLM 确定性路由 + 大模型兜底）、65 检验动态表单、
  效应量助手、曲线 / 分配比图、当前分析设定卡、关键数值卡片、内联 SVG 图形（可切 PNG）、
  可复现 R 代码、coze 请求信封预览（不发）、会话线程 diff（继承 / 覆盖 / 缺失）、
  多组对比表、一键导出单文件 HTML 报告、脱敏两阶段反馈上报。
- 咨询类表述（如"这个检验是什么意思"）不会触发云端计算——结果区给出提示，避免误耗算力。
