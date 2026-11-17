# qto-project/v1 五件套联动契约（底座 cad-file-reader）

> 目的：让用户“只装部分算量 skill”也能联动成体系。契约、schema、校验器、目录约定全部放在必装底座 `cad-file-reader`；四算量 skill 之间互不强依赖，只在同项目发现其他专业输出时做交叉核对，缺失即跳过并标占位。
> 边界：P0 做“地图”（主键/目录/契约/校验/占位），P1 做 `算量/` 登记适配层（只登记输入/输出/缺口，不执行算量算法），P2 做汇总；P3 做跨专业仲裁。不改四算量算法与口径，不上传任何公司图纸/项目路径。

## 0. 术语与 skill 映射

| 正式 slug | 角色 | 说明 |
|---|---|---|
| `cad-file-reader` | recognition（底座，必装） | 统一契约/schema/校验器/目录约定所在地 |
| `tujian-suanliang` | quantity（土建，可选） | 本机目录名可能与 slug 不一致，统一按 slug 引用 |
| `anzhuang-suanliang` | quantity（安装，可选） | — |
| `zhuangshi-suanliang` | quantity（装饰，可选） | — |
| `yuanlin-suanliang` | quantity（园林，可选） | — |

程序读取见 `rules/skills-map.json`；发布包不携带本机绝对路径。

## 1. project_key 主键规则（三级）

统一主键：`工程 / 楼栋 / 楼层 / 分区 / 房间(部位) / 专业`

1. **显式（source=explicit）**：优先读 `项目目录/.qto/project.yaml` 的 `project_key`，字段缺失即留空不猜。
2. **图内推断（source=auto）**：从图名、图框标题、层名、块名推断，字段带 `source_evidence`（证据图框/图层/坐标），标记 `source=auto`。
3. **文件级回退（source=file）**：无法绑定楼栋/楼层/房间时，主键回退为 `{工程}/{图名}/{专业}` 语义，并把 `review_required=true`，规则为 `无法绑定主键，仅文件级对齐`。

同一张图含多图框时按图框分组；仍不能分组则整图一个文件级主键。P0 允许“部分键缺失、文件级回退成功”即算通过；禁止用空白/`未知` 硬填统计主链。

## 2. 项目目录约定

```
<项目目录>/
  .qto/project.yaml            # 项目范围、底座版本、识图时间、已识别专业（P0 必建）
  识别/<专业slug>/*.json        # cad-file-reader 识图候选/占位（P0 必建目录）
  算量/<专业slug>/              # P1 才写；P0 只建空目录说明
  汇总/                        # P2 才写；P0 只建空目录说明
```

- `.qto/` 为新增目录，不触碰项目原有文件。
- 文件名：`<project_key_safe>__<专业slug>__<YYYYMMDD>.json`；`project_key_safe` = 主键去 `/ \ : * ? " < > |`。
- 未装专业：在 `project.yaml` 的 `specialties.<slug>` 登记 `not_installed`，并在 `识别/<slug>/` 放占位 JSON（`placeholder.not_installed`），汇总时只占位不报错。

## 3. 输出契约（qto-project/v1，兼容 v0）

现有 `cad-file-reader/v0` 字段、`final_quantity=false`、`evidence`、`confidence`、`review_reasons` 均**不改名、不改语义**。新增**可选顶层字段**：

- `qto_spec = "qto-project/v1"`（新输出必填）
- `project_key {project, building, floor, zone, room, specialty, source, review_required}`
- `draft_type: "概算" | "物资计划" | "draft_type_pending"`（缺省 `draft_type_pending`）
- `specialty`（正式 slug）
- `producer`（生成本输出的 skill/角色）
- `placeholder`（`null` 或 `{kind: "not_installed", note}`）

Schema：`schemas/qto-project-v1.schema.json`。

## 4. 校验器

```bash
SKILL_DIR/cad-file-reader/scripts/qto_validate.sh <项目目录> [--report-json 报告.json]
```

规则：
- 新输出：`qto_spec` 与 `project_key` 必填校验，缺失即 fail。
- 旧输出（仅含 `cad-file-reader/v0` contract）：只 warning 不 fail，保证既有回归/历史文件不被新规范打断。
- 目录/文件名约定与占位完整性校验；`识别/<专业slug>/` 必须存在。
- 未装专业必须登记 `not_installed` 且至少一个占位 JSON；已装/已识别专业不得全是占位。
- 校验失败码非 0；`regression_pass`（契约与旧 v0 是否全通过）与 `precision_note`（P0/P2/P3 需核对清单）分开统计。

工具（生成项目/包装/占位）：

```bash
scripts/qto_project.py init <项目目录> --project 工程名 [--recognized tujian-suanliang ...]
scripts/qto_project.py wrap 已有.识图.json --specialty tujian-suanliang --project 工程名 --out 识别/...json
scripts/qto_project.py placeholder <项目目录> --specialty zhuangshi-suanliang --project 工程名
```

## 4.5 P1 算量联动适配器

底座新增 `scripts/qto_p1_link.py`（目录级登记，不执行任何专业算量算法）：

```bash
scripts/qto_p1_link.py --project-dir <项目目录> --specialty <slug> [--quantity 某专业量算.json] [--date YYYYMMDD] [--note ...]
```

- 从 `识别/<slug>/` 读底座识图候选 → 写 `算量/<slug>/<key>__<slug>__<YYYYMMDD>.json`（顶层 `qto_spec/qto_version/project_key/specialty/draft_type/producer`，`contract` 仍为 `cad-file-reader/v0`）。
- 未给 `--quantity` 且有识别结果：登记占位 `quantity_pending`（等待专业算量执行），不臆造工程量。
- 缺识别目录/无 JSON：写缺口占位 `recognition_missing`，**不解析大 DWG、不阻断体系**（`status=gap`，CLI rc=0）。
- 附 `--quantity`：把该专业既有量算结果作为 `contract.candidates[0]` 附着登记，`final_quantity=false` + `review_required=true`，仍以专业算量 skill 的复核为准。
- 单专业安装即可独立使用；多专业并存时各专业只写自己的 `算量/<slug>/`。


## 5.5 P2 汇总层

`scripts/qto_p2_summarize.py`（shell 入口 `scripts/qto_p2_summarize.sh`）只汇总、不计算量：

```bash
scripts/qto_p2_summarize.sh --project-dir <项目目录> [--date YYYYMMDD]
```

- 读 `算量/<专业>/*.json` 与 `.qto/project.yaml`，写 `<项目目录>/汇总/<key>__汇总__<date>.json`（+同路径 `.csv` 供人读）。
- 状态口径：`ok`（有量算登记候选）｜`pending`（等专业算量）｜`gap`（缺识别，写缺口占位）｜`not_installed`（未安装且无输出）｜`missing`（已装/登记 active 但缺算量输出）。
- 汇总 `totals`：专业数、文件数、状态计数、候选总数、需核对总数；不做跨专业仲裁（留 P3）。

## 5.6 P3 跨专业交叉核对

`scripts/qto_p3_clash.py`（shell 入口 `scripts/qto_p3_clash.sh`）只读不计算量：

```bash
scripts/qto_p3_clash.sh --project-dir <项目目录> [--date YYYYMMDD]
```

- 按 `project_key.(building/floor/zone)` 或文件名前缀聚合“部位”；同部位 ≥2 专业均有算量登记 → 进入 `cross_checks`，提示需按图纸人工交叉核对（不仲裁量值）。
- 同样输出“已登记 active 但算量层缺输出=missing”“未安装=not_installed”“缺识别=gap”信号。
- 输出 `<项目目录>/汇总/<key>__交叉核对__<date>.json` + `.csv`；不做最终工程量。
## 5. 验收口径

- 硬门槛 = 原回归不倒退：四算量与底座的既有真实图回归全 `pass` 才允许 P0 交付通过。
- `regression_pass` 与 `precision_note` 分开统计，不得混为一谈。
- self_test（`bash scripts/self_test.sh`：doctor + 全量 unittest + schema/cad_validate + 样例/坏文件回归 + 可选真图回归）通过。
- 发布内容只放自绘简化样本（`examples/qto-sample/`），不放真实项目素材。

## 6. Non-goals（P0 不做）

- 不实现 qto-summary 汇总层（P2）。
- 不做跨专业冲突仲裁/自动改数（P3）。
- 不要求用户五件全装；不新建“超大连体 skill”。
- 不改四算量既有算法、损耗、口径与真正回归 pass 判定。
