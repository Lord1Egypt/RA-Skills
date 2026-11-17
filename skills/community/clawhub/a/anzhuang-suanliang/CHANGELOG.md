# Changelog

## 0.4.38 · 2026-11-10 · S9 发布准备：版本收口

- 版本 patch bump；同步套件最低版本。s9 发布准备，未改算量逻辑。

## 0.4.37 · 2026-11-10 · mep_scan 只吃契约 + 入口闸门

- **`mep_scan.py` 删除生产直读**：移除 `scan()`、`expand_block_geometry()` 与 `dev_scan/ezdwg` 生产 import，删除 `--dev-allow-direct`；只允许 `--contract` 消费 `cad-contract/v1`，DWG/DXF/DWT 退出 `23`。
- **入口闸门 vendored**：新增 `scripts/entry_gate.py`，`mep_plan.py`/`mep_scan.py` 统一 `20/21/22/23/24`；`--check-deps` 缺 reader=`20`、缺 bus=`21`。
- **`dev_scan.py` 改为停用桩**：不再 import `ezdxf/ezdwg`。
- **文档修正**：`README.md` 删除 `mep_scan 平面图.dwg` 用法、`index.md` 删除「DWG → 扫描 JSON」，改为契约入口；SKILL.md 新增退出码表与固定提示。

## 0.4.36 · 2026-11-09 · 接入 contract_guard 主门闸

- **主入口闸门**：`mep_plan.py` 先 `guard_contract`；手工契约缺 `--allow-manual` exit 3，`mode=manual` 强制 `final_quantity=false`。`CAD_ALLOW_DIRECT` 环境变量闸替换为隐藏参数 `--dev-allow-direct`，输出强制 `DEV_DIRECT_PARSE`、`formal_ledger_eligible=false`。
- **兼容 reader 契约**：`_doc_provenance()` 同时识别顶层与 `contract` 对象内的 `contract_version=cad-contract/v1`、`provenance`。
- **新增**：`--check-deps`、`site_handoff.json`（`specialty=mep`）、`provenance`/`run_manifest` 输出。
- **manifest 统一**：`requires.skills={cad-file-reader>=0.41.0, lis-skill-bus>=0.1.11}`，`entry_policy=contract-only`。

## 0.4.35 · 2026-11-09 · 常驻注入瘦身

- **description 精简**：技能目录注入的 description 压到 ≤45 字，保留原有触发词与「不做什么」边界；SKILL.md 正文与算法口径未变。

## 0.4.34 · 2026-11-08 · 技能层瘦身与发布完整性

- **SKILL.md 瘦身**：18,003 B → 9,812 B（-45.5%）。触发词、硬规则、能力边界保留在前置段；低频细则外移到 `references/`、`docs/`、`packs/`，按需加载，算法与业务口径不变。
- **发布完整性**：被引用文件随包存在、Python/bash/JSON 语法通过、技能自检 PASS；未实现的检查如实记 SKIP。
- **脱敏**：本机路径、真实项目名与公司资料引用替换为通用示例；平台专用入口只改发布副本。


## 0.4.30

- **新增（市政管长汇总）** `scripts/municipal_pipe_length.py`（+ `.sh`）：
  吃 cad-file-reader `cad_municipal_geometry` 的 `*.municipal.json`
  （管道标注：系统/管径/原文；市政图层几何段），按三档证据出管长：
  - ① 显式长度：标注文本 `L=25000` / `长度4500`（置信高）
  - ② 桩号差：`K0+240.5~K0+412.3`（市政管道纵断面主口径，跨千米进位 K1+980~K2+030）
  - ③ 图面线段：管道图层的 geometry 段长合计，按「该图层管道标注的系统多数派」归属，
    管径记「未标注」；**系统已有显式长度时其图面线段整体跳过（防重复计数）**
  - 汇总按 系统 × 管径（DN/De/d/Φ 归一为 DN数字），输出 md/csv/json，
    标 final_quantity=false（图面长度，不含井段扣减/弯曲增长，非施工下料长度）。
- 新增 8 项单测（管径归一、L=、桩号差、跨千米、图层多数派、显式优先、空输入报错）；
  全套 31→**39** 项全绿。
- 注：本机暂无市政管网真图，真图门禁待有图时补跑
  `cad_scan --with-geom --detail-json` → `cad_municipal_geometry` → `municipal_pipe_length`。

## 0.4.29

样例二区 J-5# 楼电气图（`WDZ-BYJ-*` 裸规格、天正分层、R2007）真图回归驱动的一轮口径修复；新增 31 项单测（`scripts/tests/`）。

- **修复（图层误判·量翻倍）** `WIRE-消防` 等带 `WIRE` 前缀的图层此前同时命中电气和水专业两条判据：同一批 841.7m 既进「电线电缆」又进「水专业」，全楼管线量凭空多出一份。现在电气判据优先，`WIRE-*` 不再进水专业。
- **修复（标注层当管线）** 新增「非管线路由」判据：`DIM-*`（标注）、`EQUIP-*`（设备符号）、图框/标题/墙体/轴网/文字层不计入任何量。实测 J-5 电气图 `DIM-照明` 11329.9m、`DIM_SYMB` 1638.3m 此前被当成路由甚至水管（`PIPE_ROUTE_RE` 里的 `DIM_` 误伤）；`EQUIP-消防` 602.5m 设备符号线被按线长算成水管。
- **修复（总量守恒恒等于通过）** 电气行原写成 `matched + (total-matched)`，与源总长恒等，那张表永远全「通过」等于没核对。现在分档合计只算真正出量的部分，状态区分 通过 / 未出量 / 异常，未出量行给出原因与去向。
- **修复（长线匹配不上）** 回路标注匹配原按「线段中点→标注点」距离：一条 60m 直线只有中点，规格标在端头就超出 30m 半径。扫描端（`mep_scan.py`）现在给每段线带两端坐标，匹配按「点到线段」垂直距离；旧扫描 JSON（无端点）自动退回中点口径。
- **新增（相邻传播）** 标注够不到的线段，按同层 2.5m 内相邻线段接力定规格（最多 3 轮）；传播来的量在「置信度分级」记低，与直接命中分开。跨层绝不传播（强电/弱电不串）。
- **新增（图层分档表）** 原「匹配情况」表改为「图层分档」：每层标归属（电气回路/桥架/水专业/非管线路由/未归类）+ 已出量/未出量 + 说明；某层未出量超 30% 时直接给出主规格候选与占比（如 WIRE-照明未出量段候选 `WDZ-BYJ-3*2.5-PVC16`），不擅自回填数量，人工确认后再分档。
- **修复（规格解析，承接 0.4.28）** `parse_spec` 不再取 `split("-")[2]`：`BV-2*2.5-SC15` 曾解析成 15 芯；现在全串搜 `N*截面`（支持 `3*10`/`3x10`/`3×2.5`/`4*25+1*16`），家族名取「首段-纯字母次段」。`CONDUIT_RE` 补 `PVC|CPVC`。
- **新增（无线号兜底，承接 0.4.28）** 平面图只标裸规格、不标回路号时（样例这批全是），按规格就近匹配出量，回路列记 `-`；`looks_like_spec` 拒收说明文字（`消防信号线：3*NH-RVS-2X1.5-CT` 一类）。
- **对账口径** 「未匹配坐标簇」改为使用匹配函数实际未定规格的线段，不再重算一遍，避免与传播/端点距离口径不一致。

## 0.4.27

- **修复（发布兼容）** SkillHub 分发包（zip）不保留文件权限，装完脚本全是 644，直接执行会 permission denied。现在 `scripts/setup.sh` 与各入口脚本（`runtime_env.sh` / `ensure_runtime.sh`）首次运行时幂等补回 `scripts/*.sh`、`scripts/*.py` 的可执行位，用户无需手动 chmod。
- **修复** `scripts/setup.sh` 里 `bash bash "$SKILL_DIR/scripts/ensure_base.sh"` 的重复 bash 会让安装第一步直接报 `bash: bash: No such file or directory`，已改为 `bash "...ensure_base.sh"`。
- **修复（自测误报）** `scripts/self_test.py` 对未随轻量包提交的开发期单测（`scripts/tests/test_*.py`）改为「存在则校验、缺失则 SKIP」，不再让 `SELF_TEST` 因缺件判失败；Windows 专属 `.cmd` 在非 Windows 平台跳过。

## 0.4.26

- **更新发布** 补 CHANGELOG 详细条目与 README.en 版本号；三端（Codex/WorkBuddy/发布仓库）同版本同内容再次校验通过。tujian-suanliang 的 manifest tests 仅保留真实存在的 `scripts/self_test.py`（完整 tests 见本机 shangwu-suanliang 商务版）。
- 算法、契约、权限、SKILL.md 正文与上一版无变化。

## 0.4.25

- **授权与保留** 新增「授权与保留」段落：作者 lis 声明本技能可商用/可再分发/可对外授权，商用前按双许可说明确认是否需联系作者申报。
- **脱敏（发布合规）** rules 中的公司内部来源字段由「公司知识库/…/规范图集」改为「公开规范与行业通用做法整理」，不再引用公司内部资料路径。
- **版本对齐** 本机 `$CODEX_SKILLS_DIR/skills`、`~/.workbuddy/skills` 与发布仓库同步同版本；算法、契约、兼容性与上一版一致，未改业务逻辑。

## 0.4.23

- **修复** `mep_plan.py` 的 `from openpyxl import ...` 由模块顶层改为出表函数内延迟导入，缺库时给出安装指引而非裸 traceback；未装 openpyxl 也能正常执行 `--help`。
- **新增** `scripts/runtime_env.sh`：统一解析 Python 解释器、识图底座目录，并把「本技能 scripts + 底座 scripts + 底座 vendor」注入 PYTHONPATH，无需全局 pip 安装。
- **修复** 底座探测仅覆盖 `$HOME/.codex`、`~/.claude`，现增加同级目录与 `~/.workbuddy/skills/*/cad-file-reader`；自动安装落点由硬编码 `$HOME/.codex` 改为与技能同级目录。
- **新增** `requirements.txt` 与 Windows 启动器 `mep_scan.cmd` / `mep_plan.cmd` / `anzhuang_statesync.cmd`（静态校验，未实机验证）。
- **文档** CLI 示例改为 `bash scripts/*.sh`；清理 `## 依赖` 空标题。
- **修复（发布兼容）** `mep_plan.py` 调用 `cad_validate.sh` 改为 `bash` 启动；`ensure_base.sh` / `setup.sh` 内部调用同样改为 `bash`，不依赖执行位。
- **修复（跨 Agent）** `mep_plan.py` 底座探测增加同级目录与 `~/.workbuddy/skills/*`，保留 `~/.claude`、`$HOME/.codex` 回退。

## 0.4.22 (2026-10-23)
- 修复 SkillHub 版 Windows 无 `.cmd` 时的接线说明：改为 `python scripts/*_statesync.py` 等价调用（bus 安装用 `python install_py.py --apply`）；GitHub 完整包保留 `.cmd`。平台发布调整，算法/契约/口径不变。


## 0.4.21 (2026-10-22)
- lis-skill-bus 可选联动（试点）：scripts/anzhuang_statesync.py push/pull 对接 cad-contract/v1（route_segments/circuits/systems/equipment 等），新 Windows anzhuang_statesync.cmd（未实机跑通，仅静态校验）；bus 未装自动降级。算法/口径不变。

## 0.4.20 (2026-10-21)
- 三平台对齐（cross-platform + i18n overseas）：README.en.md、`--lang en|zh` 主入口、i18n.py、CFI 三平台 workflow 全绿。
- 不改变业务算法/中文模板；平台专用调整只改发布副本。

# 更新记录
## v0.4.19 — 2026-10-19（三平台发布对齐）

- 发布对齐：以本机为规范源同步三平台；含 qto-project/v1 联动契约与 zero-config 底座默认仓库。
## P1 联动（2026-10-19，文档说明）

- 新增与 `cad-file-reader` 的目录级联动说明：识别放 `<项目目录>/识别/<slug>/`，量算输出写 `<项目目录>/算量/<slug>/`，可用底座 `scripts/qto_p1_link.py` 登记；不改算法与口径。

## 0.4.13 — 2026-10-18（安装/电气替代版回归入池）

- 补充同项目替换版电气系统图回归清单 `anzhuang-suanliang-ts-elec-sys.json`（kind=electrical），与本轮 cad-file-reader 替代版共用同源 CAD 扫描，正式电气候选复核 1/1 通过：systems=1165/equipment=2430/circuits=1943，contract_valid=true。
- 依赖底座升至 cad-file-reader 0.28.14（含 `--dwg-dxf-fallback` 自动回退支持）。

## 0.4.12 — 2026-10-18（第二期真图回归：45 例 45/45 全通过）

- 45 例按 5 张一批串行跑完，45/45 `contract_valid=true`，覆盖给排水/暖通/电气三类。
- 自检 `run_preflight.sh` self_test OK + 发布合规扫描 problems=0。

## 0.4.11 — 2026-10-16（单位自动推断 + 图层别名扩展 + 输入质量核对）
- `scripts/mep_scan.py` 新增 `infer_unit_from_doc()`：INSUNITS=0 时按前 5000 条 LINE/LWPOLYLINE 长度中位数保守推断（0.1~100→m 标 `auto_inferred`；≥500→mm；灰区→`unknown/review`），不再静默按毫米误算；`drawing_unit_info()` 增加 `unit_inference` 字段与复核说明。
- 图层别名扩展：`ELECTRIC_ROUTE_RE`/`PIPE_ROUTE_RE` 及 `water_system`/`water_zone` 增加市政/室外常见图层别名（`PIPE-*`/`WIRE-*`/`管道-*` 等）。
- Excel 输出新增 `输入质量核对` sheet，汇总单位推断、块内几何复核提示与待核对项。
- 单测 `self_test.py` 增加单位推断断言（median=22.0→auto_inferred/m）。
- 真图验证：范村室外管网总图（6800 段、文本 4641、单位 median 5.11→auto_inferred/m、`PIPE-污水` 累计 10.4km 级）、范村室外强电总图（620 段、文本 1812），已出 xlsx。
- 自测：`run_preflight.sh` self_test OK，发布合规扫描 problems=0。

## 0.4.10 — 2026-10-12（真图回归纳入发布预检）
- 新增 `scripts/run_preflight.sh`：全量自测 → 发布合规扫描 → 真图回归（复用 cad 底座，--manifest 强制），发布前统一入口。
- `ensure_base.sh` 保留 SHA-256 完整性校验；默认底座版本 cad-file-reader 0.28.5。

## 0.4.6 — 2026-10-12（底座自动安装加固）

- `ensure_base.sh` 增加 cad-file-reader 完整包 SHA-256 校验（从同 Release 下载 SHA256SUMS），校验失败拒绝安装与执行。
- 自动安装底座前校验包内 manifest 版本；默认底座版本升至 0.28.1。
- 平台安全扫描合规：自动下载底座改为带完整性校验、版本固定。


## 0.4.0 — 2026-10-05

对接 cad-file-reader 0.25.0 底座增强：旋转标注聚合、图例匹配、契约置信度/跨专业引用字段；版本门槛升至 `cad-file-reader >= 0.25.0`。

## 0.3.0 — 2026-10-05

对接 cad-file-reader 0.19/0.20 底座的 MEP 拓扑关联候选与交接校验。

- `mep_plan.py` 新增 `--mep-geometry`：可导入 cad-mep-geometry/v2 的 `mep_relations`（设备—管段、立管—管段、端点连接、系统冲突），进「MEP关联候选核对」工作表；候选固定 `final_quantity=false`，不参与本技能算量。
- `--cad-measurement` 导入前用 cad-file-reader `cad_validate.sh` 校验交接 JSON；校验失败只提示，不阻断。
- 自检扩展：覆盖 `mep_relations` 解析与空输入。

## 0.2.0 — 2026-09-20

- 对接 `cad-file-reader >= 0.18.0`，扫描结果记录底座版本和测量候选兼容状态。
- `mep_plan.py --cad-measurement` 支持导入“CAD测量候选核对”工作表；候选固定 `final_quantity=false`，不参与算量。
- 补充安装识图与算量边界说明，不输出金额、结算量或竣工计量。

## 0.1.0

- 首次发布安装算量技能。
- 支持 DWG 扫描索引与概算清单底稿、物资计划草稿双口径输出。
- 固化桥架 50m 异常单段阈值和剔除清单。
- 固化电线 `(路由长 + 两端预留) × 芯数` 展开。
- 增加规范约束、双口径映射、置信度分级、总量守恒和核对清单。
- 将 DWG 依赖重构为 `cad-file-reader` 动态发现，支持 `CAD_SKILL_DIR`。

## 0.4.31（2026-10-30）
- municipal_pipe_length.drawn_lengths：图面线段管径改为读识图层就近挂接的 diameter 字段（cad-file-reader 0.38.8 attach_diameters），按 系统×管径 分组输出；取不到仍记「未标注」。真图（范村管网总图）438.0m 拆出 DN100/DN300/DN50 等规格行。
