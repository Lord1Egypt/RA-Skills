# 钢结构算量（gangjiegou-suanliang）

**[English](./README.en.md) | [中文](./README.md)**

**v0.4.0** · 正式量只从 `lis-skill-bus` 按 `contract_id` 取契约；不碰图纸解析，只把 `cad-file-reader` 的钢结构契约变成 **截面谱 + 吨位估算带 + 构件台账**。

正式识图链路固定为 `cad-file-reader -> cad-contract/v1 -> lis-skill-bus -> gangjiegou-suanliang`。本技能不读取 DWG/DXF/PDF，也不提供绕开 `cad-file-reader` 或 `lis-skill-bus` 的第二套识图路径。`--steel`/位置参数是文件入口，必须显式 `--allow-manual`，一律按 `manual` 降级，不是正式量。

## 先确认能不能用

单独安装本技能，**不会自动带入** `cad-file-reader` 和 `lis-skill-bus`。从市场安装后先跑一次：

```bash
python3 scripts/steel_tonnage.py --check-deps
```

- 两项都找到：退出码 0，正式识图链路可开工。
- 缺任意一项：退出码 20/21（缺 reader 20、缺 bus 21），明确列出缺什么，并给一条可复制安装命令；此时不能从 DWG 开始识图。文件契约仍可计算，但必须显式 `--allow-manual`，结果 `final_quantity=false`，不是正式量。
- `manifest.json` 的 `requires.skills` 已声明最低版本：`cad-file-reader>=0.41.0（含 cad-file-reader:packs/steel-geometry）`、`lis-skill-bus>=0.1.11`。

## 能做什么

- 消费 `cad-steel-geometry/v1` 契约 JSON，输出 `cad-steel-tonnage/v0.2` 的 `json + md + csv`。
- 4 段式 H 型钢、圆管、方/矩管、角钢、C/Z 檩条、给足尺寸的槽钢和钢板按几何公式估米重。
- 号数型热轧槽钢 `[5`~`[40`、工字钢 `I10`~`I63`（含 a/b/c 分档）按 GB/T 706 理论重量查表。
- 按 `materials[]` 输出十类钢材牌号吨位带；无牌号证据归 `unknown_grade`，不默认指定牌号。
- 按 `members[].code/name` 归并构件实例、截面集合、显式长度和坐标证据；冲突与无法映射项进入复核清单。
- 按 `connections[]` 统计高强螺栓、普通螺栓、锚栓、栓钉、节点板、加劲肋；有厚宽长或板厚×面积证据的节点板进入吨位，其余不硬凑。
- 按 `finishes[]` 输出底漆、面漆、热浸镀锌、防火涂料面积带；缺面积或范围时 `unavailable`，防火等级不默认推断。
- 长度分两档：优先用构件标注里的显式长度；否则用钢构件图层线段合计；都没有时只出截面谱。
- 总吨位优先取逐根台账，分摊值只作草稿参考；统一输出 `±15%` 吨位带，`final_quantity=false`。
- 未映射截面只计数；缺厚度、缺宽度、表外规格同样只计数，不用默认值硬凑。

## 总吨位两个口径

| 情况 | `total_t` | `total_t_allocated_estimate` |
|---|---|---|
| 全部构件编号都有显式长度，且每个编号只映射一个可计米重截面 | 逐根 `member_merge[].tonnage_t` 求和，`total_basis=member_level` | 同时保留，供草稿对照 |
| 逐根台账不完整（缺长度、缺截面、多截面冲突） | 按 `米重 x 标注次数` 加权分摊，`total_basis=allocated_estimate`，报告顶部明确警告 | 与 `total_t` 相同 |
| 无长度或无可计米重截面 | 空数组 | 空数组或仅有节点板证据 |

`member_level_note` 会写明为什么没有采用逐根口径。只有 `total_basis=member_level` 时，报告和 CSV 才把 `total_t` 标为“推荐”；退回分摊时标为“分摊草稿，不是答案”，并保留 `total_t_allocated_estimate` 限定词。

## 快速开始

### 1. 正式识图链路

```bash
# 先探测前置；缺依赖时退出码 20/21
python3 scripts/steel_tonnage.py --check-deps

# 复用同项目/楼栋/楼层的契约；命中则不再解图
bash scripts/gangjiegou_statesync.sh pull --project 项目

# 未命中时由 cad-file-reader 唯一一次识图并产出钢结构契约
bash skills/cad-file-reader/scripts/cad_scan.sh 钢结构图.dwg \
  --with-mtext --with-insert --with-geom --with-geom-layer \
  --detail-json 钢结构详情.json --format json -o 钢结构扫描

bash skills/cad-file-reader/scripts/cad_steel_geometry.sh \
  钢结构详情.json --out-dir 钢结构识图

# 经 bus 发布识别契约
bash skills/cad-file-reader/scripts/cad_statesync.sh push \
  --entry-file 钢结构识图/钢结构详情.steel.json --project 项目 --specialty 钢结构

# 出数前先体检；结构错误退出码 2，不出吨位
python3 scripts/steel_tonnage.py \
  --validate 钢结构识图/钢结构详情.steel.json --report 契约体检.json

# 正式量：从 bus 按 contract_id 取契约并落盘 json/md/csv
# contract_id 见 push 输出或 bus pull 结果
python3 scripts/steel_tonnage.py \
  --from-contract <contract_id> --project 项目 --out-prefix 钢结构吨位
```

### 2. 从 bus 取正式契约

```bash
python3 scripts/steel_tonnage.py \
  --from-contract <contract_id> --project 项目 --out-prefix /tmp/steel-tonnage
```

这是正式量入口，不是第二套识图路径。契约必须由正式链路生成并经 `lis-skill-bus` 保存；不要把 bus 产物另存成本地文件后当正式契约送入，文件入口会强制降级为 manual。

### 3. 手工契约（受支持的降级路径）

识图层不可用时，允许按公开字段手工构造 `*.steel.json`，不是灰色地带：

```bash
python3 scripts/steel_tonnage.py --validate examples/minimal.steel.json
python3 scripts/steel_tonnage.py \
  --steel examples/minimal.steel.json --allow-manual --out-prefix /tmp/minimal-ton
```

`examples/minimal.steel.json` 是最小样本；`examples/README.md` 写明必填字段、截面↔构件配对规则、坐标单位（mm）和 `$` 嵌套图层名处理。

### 4. 长度证据不足时看敏感性

```bash
python3 scripts/steel_tonnage.py \
  --from-contract <contract_id> --project 项目 --out-prefix 钢结构吨位 \
  --length-scenario 4.5 --length-scenario 6 --length-scenario 9
```

`length_scenarios[]` 是统一构件长度下的对比场景，报告明确写“不是结果”，不得当成缺长度证据的替代答案。

## 常用参数

| 参数 | 作用 | 退出码 |
|---|---|---|
| `--check-deps` | 只探测 `cad-file-reader` / `lis-skill-bus`，不出数；缺失时回显一条安装命令 | 齐全 0，缺依赖 1 |
| `--validate <json>` | 只体检契约：缺字段、未匹配截面、仅计数、长度证据、依赖状态 | 可计算 0，结构错误 2 |
| `--report <json>` | 把体检结果另存为 `cad-steel-contract-health/v1` | 随 `--validate` |
| `--from-contract <id>` | 正式入口：从 `lis-skill-bus` 按 `contract_id` 取契约 | 成功 0；取不到或来源不符 1/3/4 |
| `--project <项目>` | `--from-contract` 使用的 bus 项目标识 | 随 `--from-contract` |
| `--steel <json>` | 文件/手工契约入口，必须同时给 `--allow-manual` | 成功 0；缺开关 3 |
| `--allow-manual` | 显式允许文件契约；强制 `provenance=manual`、`formal_ledger_eligible=false` | 随文件入口 |
| `--out-prefix <前缀>` | 输出 `.json/.md/.csv` 前缀 | 成功 0 |
| `--length-scenario <m>` | 可重复，输出长度敏感性场景 | 成功 0 |

## 口径要点

| 项目 | 当前口径 |
|---|---|
| 量级 | `±15%` 估算带，草稿复核用 |
| H 型 | 4 段式走公式；2 段式 H 只计数 |
| 槽钢 | 给足尺寸走几何公式；号数型走 GB/T 706 查表 |
| 工字钢 | 号数型走 GB/T 706 查表，`I10`~`I63`，含 a/b/c |
| 长度 | `explicit` 优先，`drawn` 次之，`none` 不出吨位 |
| 总吨位 | 逐根台账完整时 `member_level`；否则 `allocated_estimate` 草稿 |
| 牌号 | Q235/Q345/Q355/Q390/Q420/Q460/S235/S355/A36/16Mn 证据分档；`unknown_grade` 和 `mixed_grade` 不默认归入任一钢号 |
| 构件归并 | 同编号合并实例数；类别/系统冲突、无编号或无截面映射复核 |
| 坐标 | `members[].x/y/z/rotation` 单位为 mm；缺失时 `location_status=missing` |
| 连接 | 六类计数；显式数量优先，缺数量只记标注次数并复核 |
| 涂装 | 四类面积带；缺显式面积/范围 `unavailable`，防火等级不默认推断 |
| 吊装附件 | `allowance_advice` 给 3%/5%/8% 建议，不并入 `total_t` |
| 闭合校核 | 识图层提供 `geometry_closure` 时透传为 `geometry_closure_check`；本技能不自行识图 |

## 输出

每次计算写三个文件：

- `*.json`：`cad-steel-tonnage/v0.2`，含 `final_quantity`、长度口径、牌号吨位带、构件归并台账、连接清单、涂装清单、复核清单、分截面吨位带、截面谱和仅计数截面。
- `*.md`：可读复核报告，置顶显示推荐吨位、分摊参考、长度依据、前置状态和需复核项。
- `*.csv`：总吨位带、分截面吨位、构件台账、连接/涂装和截面谱摘要。

关键字段：`provenance`、`contract_id`、`source_sha256`、`contract_sha256`、`reader_version`、`formal_ledger_eligible`、`run_manifest`、`length_basis`、`length_used_m`、`rows`、`spec_rows`、`only_count`、`total_t`、`total_basis`、`total_t_member_level`、`total_t_allocated_estimate`、`member_merge`、`length_scenarios`、`allowance_advice`、`geometry_closure_check`、`prerequisites`、`input_evidence`、`summary`。

`steel_geometry[]`、`connections[]`、`finishes[]` 为空时，报告明写“输入无证据”，与“技能未实现”区分。

## 不能做什么

- **不做识图**：不读取 DWG/DXF/DWT/PDF；识图必须先走 `cad-file-reader`。
- **不替代专业成果**：不用于深化设计、翻样、下料、结算、报价或竣工计量。
- **不硬凑**：缺长度、缺厚度、缺宽度、表外规格或未知截面只计数；识别层标记的 `review` 和缺口必须保留给人工复核。
- **暂不支持**：除节点板以外的连接件吨位、焊缝吨位、构件级精确截面对应与净量、牌号对米重的影响、曲线或多段几何展开长度、三维模型涂装面积计算、防火等级推断。

## 依赖

- Python 3.10+；主计算入口只用标准库。
- 正式识图：`cad-file-reader>=0.41.0`（含 `cad-file-reader:packs/steel-geometry`）与 `lis-skill-bus>=0.1.11`。
- 已有契约或手工契约：不需要上述两个技能在位，但文件入口必须显式 `--allow-manual`；结果不是正式量。`--from-contract` 需要 `lis-skill-bus` 在位。

## 验证

```bash
python3 tests/test_entry_gate.py
cd scripts/tests
python3 -m unittest test_steel_tonnage
```

当前 v0.4.3 含 **35 项入口闸门断言 + 49 项合成数据单测**。入口测试覆盖 `--check-deps`、手工契约 exit 3、`--allow-manual` 降级、伪造 reader 拒绝、bus 缺契约、`cad-contract/v0` 版本拒绝和正常 reader 契约；49 项旧测试覆盖米重公式、GB/T 706 查表、长度两档、无长度降级、输入契约拒绝、重复编号提示、牌号分档、`unknown_grade`、节点板吨位与牌号余量、构件归并复核、连接分类计数、涂装面积降级、逐根/分摊双口径、坐标透传、`--validate` 体检和长度敏感性场景。

准入边界：`provenance`/`contract_id` 仍不是密码学防伪；当前实现防误用，不防合法格式伪造，正式验真需 reader/bus 的签名或 `contract_id` 白名单。

示例烟雾测试：

```bash
cd ../..
python3 scripts/steel_tonnage.py --validate examples/minimal.steel.json
python3 scripts/steel_tonnage.py \
  --steel examples/minimal.steel.json --allow-manual --out-prefix /tmp/minimal-ton
```

## 许可

采用 `CC-BY-NC-SA-4.0`；企业或经营性使用需按 `LICENSE.md` 另行取得作者授权。
