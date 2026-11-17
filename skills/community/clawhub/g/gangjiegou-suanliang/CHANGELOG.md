# Changelog

## 0.4.3 · 2026-11-10 · S9 发布准备：版本收口

- 版本 patch bump；同步套件最低版本。s9 发布准备，未改算量逻辑。

## 0.4.2 · 2026-11-10 · 入口闸门 vendored（只吃契约，不解图）

- **新增 `scripts/entry_gate.py`**（与 `lis-skill-bus/lib/entry_gate.py` 同源 vendor，纯 stdlib）：统一退出码 `20` 缺 reader、`21` 缺 bus、`22` 契约无效、`23` 图纸输入、`24` 证据不足。
- **`--check-deps` 改为稳定码**：齐全 `0`，缺 `cad-file-reader>=0.41.0` 返回 `20`，缺 `lis-skill-bus>=0.1.11` 返回 `21`，并打印安装命令。
- **图纸入口封死**：DWG/DXF/DWT 直接退出 `23`，打印固定中文提示；删除 `CAD_ALLOW_DIRECT` 等“开发直读”说法，不提供任何直读逃生开关。
- **SKILL.md** 顶部新增退出码表与固定提示；`manifest.scripts` 登记 `scripts/entry_gate.py`。

## 0.4.1 · 2026-11-09 · 统一 contract_support 与 site_handoff

- **统一支撑层**：`--check-deps` 改用 `contract_support.check_deps()`（版本门槛 0.41.0 / 0.1.11）；`run_manifest` 改用 `contract_support.run_manifest()`，固定 `entry_policy=contract-only`、`manual_requires_flag=true`。
- **新增 `site_handoff.json`**（`specialty=steel`）：成员来自 `member_merge`；坐标 mm→m，缺失写 `null`/`coord_status=missing`；吨位带取上限作为吊装保守重量（`weight_basis=estimate_band_upper`），无吨位写 `weight_t=null`/`weight_basis=unknown`。
- **manifest 统一**：`requires.skills={cad-file-reader>=0.41.0, lis-skill-bus>=0.1.11}`，`entry_policy=contract-only`。
- **验证**：`tests/test_steel_tonnage.py` 49 项、`tests/test_entry_gate.py` 7 项全 PASS。

## 0.4.0 · 2026-11-09 · 主门闸：正式量只走 bus 契约

- **BREAKING：文件入口必须显式授权**。`--steel`/位置参数不再默认可用，缺少 `--allow-manual` 时直接退出 3，不产出任何文件。
- **正式量只认 bus 契约**：新增 `--from-contract <contract_id>` + `--project <项目>`，按 `contract_id` 从 `lis-skill-bus` 取契约；取不到退出 1，来源不是 reader/bus 退出 3，契约版本不符退出 4。不退回本地文件，也不另开解析路径。
- **文件入口强制降级**：走 `--steel`/位置参数时，即使 JSON 自称 `provenance=reader` 且带 `contract_id`，也一律改写为 `provenance=manual`、`formal_ledger_eligible=false`、`final_quantity=false`，不能进正式台账。
- **新增溯源字段**：输出固定带 `provenance`、`contract_id`、`source_sha256`、`contract_sha256`、`reader_version`、`formal_ledger_eligible`、`run_manifest`，报告头部同步说明来源与降级状态。
- **代码闸门落地**：新增 `scripts/contract_guard.py`（`guard_contract` 调用点），统一校验契约版本、来源和必需 section，替换原先分散在入口的隐式判断。
- **文案纠正**：`--check-deps` 与报告里的“已有契约计算不受影响”改为“文件契约必须加 `--allow-manual`，结果按 manual 降级，不是正式量”。
- **测试**：新增 `tests/test_entry_gate.py` 入口闸门 7 项（`--check-deps` 齐全、缺开关 exit 3、`--allow-manual` 降级、伪造 reader 拒绝、bus 缺契约 exit 1、`cad-contract/v0` 拒绝、正常 reader 契约），旧合成单测 49 项继续全绿。

旧命令迁移：

```bash
# 旧写法（0.4.0 起退出 3，不产文件）
python3 scripts/steel_tonnage.py --steel a.steel.json --out-prefix out

# 手工降级（结果 provenance=manual、final_quantity=false，不是正式量）
python3 scripts/steel_tonnage.py \
  --steel a.steel.json --allow-manual --out-prefix out

# 正式量（契约由 cad-file-reader 产出并经 lis-skill-bus 发布）
python3 scripts/steel_tonnage.py \
  --from-contract <contract_id> --project 项目 --out-prefix out
```

## 0.3.8 · 2026-11-09 · 常驻注入瘦身

- **description 精简**：技能目录注入的 description 压到 ≤45 字，保留原有触发词与「不做什么」边界；SKILL.md 正文与算法口径未变。

## 0.3.2 · 2026-11-09 · 常驻注入瘦身

- **description 精简**：技能目录注入的 description 压到 ≤45 字，保留原有触发词与「不做什么」边界；SKILL.md 正文与算法口径未变。

## 0.3.1 · 2026-11-08 · 技能层瘦身与发布完整性

- **SKILL.md 瘦身**：11,760 B → 12,593 B（+7.1%）。触发词、硬规则、能力边界保留在前置段；低频细则外移到 `references/`、`docs/`、`packs/`，按需加载，算法与业务口径不变。
- **发布完整性**：被引用文件随包存在、Python/bash/JSON 语法通过、技能自检 PASS；未实现的检查如实记 SKIP。
- **脱敏**：本机路径、真实项目名与公司资料引用替换为通用示例；平台专用入口只改发布副本。


## 0.3.0 · 2026-11-08

实测反馈整改（真实 DWG 项目，详见 `钢结构算量技能实测反馈_2026-11-08.md`）：

- **总吨位双口径**：`total_t` 改为当前主口径。全部构件有显式长度且单截面映射时取逐根台账求和并标“推荐”；
  分摊口径另存 `total_t_allocated_estimate`（不再叫 `total_t`），`total_basis`/`member_level_note`
  说明当前口径与退回原因；报告顶部并列两值并标注推荐值。
- **分摊口径不再冒充推荐值**：只有逐根台账完整时，报告/CSV 才把 `total_t` 标为“推荐”；退回分摊时标为“分摊草稿，不是答案”。
- **修牌号余量重复相加**：`grade_tonnage` 的 `unknown_grade` 只计算一次。分摊口径用总吨位扣除已分牌号；
  逐根口径对未分牌号构件与无牌号节点板求和，全部构件有牌号时不再产生虚假余量带。
- **新增 `--validate` 契约体检**：不出吨位，报告缺字段、未匹配截面的构件编号、只进 `only_count`
  的截面、长度证据和前置依赖；结构错误退出码 2；`--report` 可落盘。
- **新增 `--check-deps` 前置探测**：报告 `cad-file-reader` / `lis-skill-bus` 是否在位；输出 JSON/MD
  写入 `prerequisites`，缺依赖时在报告顶部明确提示（只影响正式识图链路）。
- **新增手工契约支持**：`examples/minimal.steel.json` + `examples/README.md`，写明必填字段、
  截面↔构件配对规则、坐标单位（mm）、`$` 嵌套图层名处理。
- **坐标透传**：`member_merge[]` 增加 `x/y/z/rotation`、`coord_unit=mm`、`location_status`，
  下游吊装覆盖/堆场/分区分析不再回读 DXF。
- **新增长度敏感性场景**：`--length-scenario`（可重复）输出多档构件长度吨位，明确标注“场景值不是结果”。
- **新增吊装/运输建议附加**：`allowance_advice` 给 3%/5%/8% 建议系数与参照总重，不并入 `total_t`。
- **空证据说明**：`steel_geometry[]`/`connections[]`/`finishes[]` 为空时报告明写“输入无证据”，
  与“技能未实现”区分；`geometry_closure` 由识图层提供时透传为 `geometry_closure_check`。
- **manifest 显式声明强依赖**：`requires.skills` 列出 `cad-file-reader` 与 `lis-skill-bus` 最低版本。
- 合成数据单测 40 → 49 项，全部通过。

## 0.2.1 · 2026-11-04

- 固化正式识图链路：`cad-file-reader -> cad-contract/v1 -> lis-skill-bus -> gangjiegou-suanliang`。
  本技能不读取 DWG/DXF/PDF，不提供绕开底座或总线的第二套识图路径。
- 接线 lis-skill-bus：新增 `scripts/gangjiegou_statesync.py`、`scripts/gangjiegou_statesync.sh`、`scripts/gangjiegou_statesync.cmd`（薄壳共享 `cad_statesync_core`），
  开工前 `pull` 复用 `cad-contract/v1`，落盘后 `push` 回总线；缺 bus 时 formal statesync 以退出码 2 停止并提示安装。
- 目标 sections：`members`、`sections`、`steel_geometry`、`connections`、`materials`、`finishes`；
  核心 sections 为 `members`、`sections`，`--require-core` 可收紧命中口径。
- 总线新增薄壳 `integration/gangjiegou_pull_contract.sh` / `gangjiegou_publish_contract.sh`。
- README/SKILL.md 补「lis-skill-bus 强制契约链路」章节；补系列蓝图蓝标 `icon.png`。
- 已由正式链路生成并留存的官方 `*.steel.json` 仍可直接送入 `steel_tonnage.py` 做计算或回归。

## 0.2.0 · 2026-11-03

- 输出契约升级为 `cad-steel-tonnage/v0.2`，输入契约文档补充 `connections[]` 与 `finishes[]`。
- 同步说明牌号分档、构件归并、连接计数、节点板吨位、涂装面积与防火口径。
- 明确暂不支持除节点板以外连接件吨位、焊缝吨位、构件级精确净量、牌号调米重、曲线/多段几何展开、三维涂装面积和防火等级推断。
- 修正 README 中“连接/涂装暂不支持”的过时描述；识图入口仍只写 `cad-file-reader`。
- 合成回归 40 项全绿，新增 `cad-steel-tonnage/v0.2` 输出契约断言。

## 0.1.0 · 2026-11-03

- 建立独立钢结构算量技能，实现从 `cad-steel-geometry/v1` 契约 JSON 到 `cad-steel-tonnage/v0.1` 的吨位估算。
- 支持米重几何公式：4 段式 H 型、圆管、方/矩管、角钢、C/Z 檩条、给足尺寸的槽钢和钢板。
- 新增 GB/T 706 查表：热轧槽钢 `[5`~`[40`、工字钢 `I10`~`I63`，含 a/b/c 分档。
- 建立长度两档口径：显式构件长度优先，钢构件图层线段次之；无长度证据时只出截面谱。
- 输出 JSON、Markdown、CSV，总量为 `±15%` 估算带且 `final_quantity=false`。
- 校验 `cad-steel-geometry/v1` 输入契约，拒绝非契约 JSON、缺字段/非法数组和全空识图证据；重复构件编号写入复核清单。
- 消费 `materials[]` 做十类钢材牌号分档；无牌号证据归 `unknown_grade`，多牌号证据归 `mixed_grade` 并复核。
- 消费 `members[].code/name` 建立构件归并台账，合并实例数、截面集合与显式长度证据；编号冲突、跨系统冲突或无法映射项进入复核清单。
- v0.1 当时明确暂不支持螺栓/锚栓/节点板计数、涂装与防火表面积。
- 合成数据单测 31 项全绿；牌号/归并合成冒烟通过，输出 JSON/MD/CSV 同步。
