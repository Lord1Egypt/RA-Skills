# gangjiegou-suanliang 详细说明（由 SKILL.md 原样外移）

> 2026-11-10 瘦身：只搬未删。SKILL.md 保留硬规则、入口闸门、边界与口径摘要；命中下列主题时按需读取本文对应小节。

## 输入契约

唯一接受的计算输入是 `cad_steel_geometry` 生成的 `*.steel.json`，顶层应为：

| 字段 | 用途 |
|---|---|
| `sections[]` | 截面候选；至少含 `section_type`、`text` 和证据。识别层保留 `status=candidate/review`、`confidence`、坐标与原文证据，本技能只读取可见标注。 |
| `members[]` | 构件候选；`code/name` 与证据中的 `L=...` 或 `长度...` 用于显式长度。`x/y/z/rotation`（mm）可选，用于下游吊装覆盖、堆场、分区等空间分析；缺失时台账记 `location_status=missing`。 |
| `materials[]` | 契约字段可选（bus 链路本身必需）的钢材牌号候选；用于 Q235/Q345/Q355/Q390/Q420/Q460/S235/S355/A36/16Mn 分档，不用于调整单位重量。 |
| `steel_geometry[]` | 钢构件图层几何段；`layer` 和 `geometry` 用于图面长度证据。 |
| `connections[]` | 契约字段可选的连接候选；用于高强螺栓、普通螺栓、锚栓、栓钉、节点板、加劲肋计数；有证据的节点板可进吨位。 |
| `finishes[]` | 契约字段可选的涂装候选；用于底漆、面漆、热浸镀锌、防火涂料面积分档；防火等级不做默认推断。 |
| `geometry_closure` | 契约字段可选的圆/线段闭合校核结果（由 `cad-file-reader` 识图层给出），原样透传到输出 `geometry_closure_check`；本技能不做识图，缺省记 `not_provided`。 |

本技能消费的截面类型为 `h_section`、`channel`、`angle`、`tube`、`rect_tube`、`purlin_section`、`plate`；未映射或解析失败的截面只进截面谱并标“仅计数”。识别层报出的 `review`、置信度和缺口不由本技能改成确定量。

## 调用链路

```bash
# 0) 正式识图链路要求先安装 lis-skill-bus；缺 bus 时本步骤以退出码 2 停止
bash skills/gangjiegou-suanliang/scripts/gangjiegou_statesync.sh pull --project 项目

# 1) cad-file-reader 负责唯一一次识图；钢结构包产出契约 JSON
bash skills/cad-file-reader/scripts/cad_scan.sh 钢结构图.dwg \
  --with-mtext --with-insert --with-geom --with-geom-layer \
  --detail-json 钢结构详情.json --format json -o 钢结构扫描

bash skills/cad-file-reader/scripts/cad_steel_geometry.sh \
  钢结构详情.json --out-dir 钢结构识图

# 2) cad-file-reader 把识别契约经 bus 发布，后续算量技能复用同一份契约
bash skills/cad-file-reader/scripts/cad_statesync.sh push \
  --entry-file 钢结构识图/钢结构详情.steel.json --project 项目 --specialty 钢结构

# 3) 出数前先体检契约（不出吨位，只查字段/配对/仅计数）
python3 skills/gangjiegou-suanliang/scripts/steel_tonnage.py \
  --validate 钢结构识图/钢结构详情.steel.json

# 4) 正式量：从 bus 按 contract_id 取契约（contract_id 见 push 输出或 bus pull 结果）
python3 skills/gangjiegou-suanliang/scripts/steel_tonnage.py \
  --from-contract <contract_id> --project 项目 --out-prefix 钢结构吨位
```

前置依赖可单独探测；非 0 必须停止，并原样回显安装命令：

```bash
python3 skills/gangjiegou-suanliang/scripts/steel_tonnage.py --check-deps
```

0) 未命中只表示当前没有可复用契约，随后仍按 1)→2)→3) 由 `cad-file-reader` 解图并经 bus 发布。没装 bus 时停止正式识图链路并安装 bus，不允许由本技能自行解图或用其它解析器兜底。

正式量最小消费示例：

```bash
python3 skills/gangjiegou-suanliang/scripts/steel_tonnage.py \
  --from-contract <contract_id> --project 项目 --out-prefix /tmp/steel-tonnage
```

文件/手工降级必须显式加 `--allow-manual`；即使 JSON 自称 `provenance` 为 `reader`，只要是文件路径也按 `manual` 处理：

```bash
python3 skills/gangjiegou-suanliang/scripts/steel_tonnage.py \
  --steel 已有产物.steel.json --allow-manual --out-prefix /tmp/steel-tonnage-manual
```

## 口径

- 输出是估算带：总吨位按 `-15%~+15%` 表达，`final_quantity=false`。
- 米重使用 `rho=7.85`，即面积 `mm^2 x 0.00785 kg/m`：
  - 4 段式 H 型钢、圆管、方/矩管、角钢、C/Z 檩条、给足尺寸的槽钢和钢板走几何近似公式。
  - H 型近似不含圆角，约偏低 1~2%；冷弯 C/Z 檩条约偏低 2~5%。
  - GB/T 706 查表只用于号数型无几何公式的热轧槽钢 `[5`~`[40` 和工字钢 `I10`~`I63`，含 a/b/c 分档；无分档的号数默认按 a 档查表。
  - 2 段式 H 型缺腹板/翼缘厚度，只计数，不进吨位。
  - GB/T 706 表外号数、缺宽钢板、未知截面都只计数，不用默认值硬凑。
- 长度分两档：
  1. `explicit`：构件标注里的 `L=6000`、`长度4500` 等，单位按 mm 转 m；有显式长度时优先使用。
  2. `drawn`：没有显式长度时，合计钢构件图层线段长度；这是图面口径，不含节点板、加劲肋、下料余量，通常偏低。
  3. `none`：无长度证据时不出吨位，只出截面谱。
- 总吨位分两个口径，`total_t` 是当前主口径：逐根台账完整时为推荐值，否则为分摊草稿并明示不得当答案：
  1. `member_level`（推荐）：全部构件编号都有显式长度且为单截面映射时，`total_t` = 逐根台账 `tonnage_t` 求和。
  2. `allocated_estimate`（草稿）：逐根台账不完整时，才按 `米重 x 标注次数` 加权分摊总长度；该值始终另存到 `total_t_allocated_estimate`，并在报告顶部标注“草稿，不作推荐值”。
  `total_basis` 标明当前采用哪个口径，`member_level_note` 说明为何退回分摊。
- 构件归并只使用 `members[].code/name` 证据和识图层保留的类别/系统；同编号多实例合并实例数，类别或系统冲突、无编号、无截面映射进入归并复核。
- 牌号只按 `materials[]` 证据归档；证据无法关联到构件时归 `unknown_grade`，多牌号证据归 `mixed_grade` 并复核，不默认指定牌号。
- 连接候选按高强螺栓、普通螺栓、锚栓、栓钉、节点板、加劲肋六类归档；全部候选有显式数量证据时合计，只有部分证据或无证据时总量进入复核，不外推。节点板仅在厚宽长或板厚×面积证据下进入吨位。
- 涂装按底漆、面漆、热浸镀锌、防火涂料分类；仅显式面积证据输出 ±15% 面积带，缺面积/范围时 `unavailable`，不默认防火等级。

## 钢结构专属口径现状

| 口径 | 当前状态 |
|---|---|
| 钢材牌号分档 | 已支持证据分档。按 Q235、Q345、Q355、Q390、Q420、Q460、S235、S355、A36、16Mn 十类输出吨位带；无牌号证据归 `unknown_grade`，多牌号证据归 `mixed_grade` 并复核。牌号不改变米重。 |
| 构件归并编号 | 已支持编号归并台账。合并实例数、截面集合、显式长度证据；冲突、无编号或无截面映射进入复核。 |
| 螺栓/锚栓/节点板计数 | 已支持连接候选分类统计；有显式数量证据时合计数量，无数量证据时只记标注次数并复核。节点板仅在厚宽长或板厚×面积证据下进入吨位。 |
| 涂装与防火表面积 | 已按底漆、面漆、热浸镀锌、防火涂料分类；仅显式面积证据输出 ±15% 面积带，缺面积/范围时 `unavailable`，不默认防火等级。 |

## 手工契约与体检（受支持降级路径）

识图层不可用时，手工构造 `*.steel.json` 是受支持的降级路径，不是灰色地带，但必须显式加 `--allow-manual`：结果固定 `provenance=manual`、`formal_ledger_eligible=false`、`final_quantity=false`，不能进正式台账。

- `examples/minimal.steel.json` 是最小可用样本，`examples/README.md` 写明必填字段、截面↔构件配对规则（文本/同 file+sheet/1500 单位邻近）、坐标单位和 `$` 嵌套图层名处理。
- 文件入口即使 JSON 内写 `provenance=reader` 且有 `contract_id`，也强制降级为 `manual`；正式量只认 bus 入口。
- `--validate` 只体检不出数：报告缺字段、匹配不到截面的构件编号、只进 `only_count` 的截面、长度证据和前置依赖；可计算时退出码 0，有结构错误时退出码 2。
- `--report out.json` 可把体检结果落盘。
- `--length-scenario 4.5 --length-scenario 6` 在长度证据不足时给多档敏感性场景，场景值明确标注“不是结果”。

## lis-skill-bus 强制契约链路

- 正式链路：`cad-file-reader -> cad-contract/v1 -> lis-skill-bus -> gangjiegou-suanliang`；本技能不读图纸，bus 缺失时不另开识图路径（formal statesync 以退出码 2 停止，提示装 `lis-skill-bus>=0.1.11`）。
- 正式算量入口是 `python3 scripts/steel_tonnage.py --from-contract <contract_id> --project 项目 --out-prefix 前缀`；旧的文件入口 `--steel` 只作为显式 `--allow-manual` 降级，不是正式量。
- 开工前 `scripts/gangjiegou_statesync.sh pull --project 项目 [--building] [--floor] [--out]`，命中且含本专业 section 时 `hit=true usable=true` 直接复用；算量落盘后 `push --entry-file <输出.json> --project 项目` 入 bus。
- 候选级命中不跳过滤：`review_required`/P2/P3 只标 `review_flagged`，长度两档、米重公式、GB/T 706 查表、牌号分档仍按本技能口径复核；`--require-core` 要求核心 section 命中。
- 路径变更设 `SKILLBUS_HOME`；安装定位优先级、section 字段清单、Windows `.cmd` 差异见 `references/bus-contract.md`。

## 验证

```bash
cd skills/gangjiegou-suanliang
python3 tests/test_entry_gate.py
cd scripts/tests
python3 -m unittest test_steel_tonnage
```

当前 v0.4.3 含 **35 项入口闸门断言 + 49 项合成数据单测**。入口测试覆盖 `--check-deps`、手工契约 exit 3、`--allow-manual` 降级、伪造 reader 拒绝、bus 缺契约、`cad-contract/v0` 版本拒绝和正常 reader 契约；49 项旧测试继续覆盖米重公式、GB/T 706 查表、长度两档、无长度降级、输入契约拒绝、重复编号提示、牌号分档、unknown_grade、构件归并复核、连接分类计数、节点板吨位、涂装面积降级、逐根/分摊双口径、坐标透传、节点板牌号余量、`--validate` 体检和长度敏感性场景。

准入边界：`provenance`/`contract_id` 是普通 JSON 字符串，当前实现防误用、不防合法格式伪造；正式验真仍需 reader/bus 的签名或 `contract_id` 白名单。
