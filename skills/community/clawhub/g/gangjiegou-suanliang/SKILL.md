---
name: gangjiegou-suanliang
slug: gangjiegou-suanliang
displayName: 钢结构算量 · 吨位估算带
version: 0.4.3
platforms: [macos, windows, linux]
author: lis
license: CC-BY-NC-SA-4.0
description: "钢结构出吨位估算；不识图、不替代结算。触发词：钢结构算量、钢构、H型钢。"
i18n:
  en: README.en.md
  zh: README.md
locale: zh-CN
---

# 钢结构算量

本技能只做一件独立的事：把 `cad-file-reader` 的 `cad-steel-geometry/v1` 产物转成可复核的钢结构吨位估算带。识图、图纸解析、证据提取都归 `cad-file-reader`；本技能不读取 DWG/DXF/DWT/PDF，也不复制识别实现。

你（智能体）不得自行实现 DWG/DXF 解析。`--check-deps` 返回 `20`（缺 reader）或 `21`（缺 bus）时停止，原样回显安装命令，不得用其它解析器兜底。
代码闸门位置：`scripts/steel_tonnage.py` 的入口闸门与 `guard_contract` 调用

## 入口闸门（固定退出码，禁止 fallback）

未安装依赖时唯一正确行为是**停止**：打印固定提示并原样回显安装命令，不得改用其它解析器，也不得内置解析图纸。

| 退出码 | 含义 | 处理 |
|---|---|---|
| `0` | 依赖就绪 | 继续 |
| `20` | 缺 `cad-file-reader` 或版本 < 0.41.0 | 停止，回显安装命令 |
| `21` | 缺 `lis-skill-bus` 或版本 < 0.1.11 | 停止，回显安装命令 |
| `22` | 契约无效（版本/结构/来源/哈希/单位） | 停止，回 `cad-file-reader` 重新生成 |
| `23` | 直接传入 DWG/DXF/DWT | 停止，改走契约 |
| `24` | 证据不足，或只有手工来源却要求正式量 | 停止；仅手工契约可出 `final_quantity=false` 草稿 |

固定提示：`本技能不直接识图，请先安装并调用 cad-file-reader 生成 cad-contract.json，再经 lis-skill-bus 传入；不许 fallback 到内置解析。`


正式识图链路固定为 `cad-file-reader -> cad-contract/v1 -> lis-skill-bus -> gangjiegou-suanliang`：

- `cad-file-reader` 是唯一图纸解析器，只解图一次并生成 `cad-contract/v1`。
- `lis-skill-bus` 是唯一定接线，不解析图纸，只传递和复用契约。
- 本技能不提供第二套识图路径。bus 缺失时正式识图链路停止并提示安装；正式量必须从 bus 按 `contract_id` 用 `--from-contract` 取用，从文件路径送入一律走 `--allow-manual` 降级。
- 算量结果必须带契约来源（图号/坐标证据）。
- 首次使用或换机后先运行 `python3 scripts/steel_tonnage.py --check-deps`：齐全退出 0，缺 reader 退出 20，缺 bus 退出 21，并明确列出门槛（`cad-file-reader >= 0.41.0`、`lis-skill-bus >= 0.1.11`、Python >= 3.10）。缺依赖时停止正式识图链路，原样回显安装命令；文件契约只有显式 `--allow-manual` 才能计算，且结果不是正式量。
- 每次出数在输出目录写 `site_handoff.json`（`specialty=steel`），供下游平面布置/吊装校核；缺坐标写 `coord_status=missing`，吨位缺失写 `weight_t=null`、`weight_basis=unknown`，不补 0。

## 口径摘要（全文见 `references/on-demand.md`「口径」）

- 输出是估算带 ±15%，`final_quantity=false`；米重 `rho=7.85`，即面积 `mm^2 × 0.00785 kg/m`。
- H 型/圆管/方矩管/角钢/C/Z 檩条走几何近似；GB/T 706 只查号数型热轧槽钢 `[5`~`[40`、工字钢 `I10`~`I63`。
- 长度优先级：显式标注 `explicit` > 图面线长 `drawn` > 无证据 `none`（只出截面谱）。
- 总吨位主口径 `member_level`（逐根台账完整）；不完整才退回 `allocated_estimate`，并标“草稿，不作推荐值”。
- 2 段式 H 型缺厚度、表外号数、缺宽钢板、未知截面只计数不硬凑；牌号只按 `materials[]` 证据，冲突进复核。

输入契约、调用链路、专属口径表、手工降级路径、bus 强制链路与验证命令见 `references/on-demand.md`。
## 输出

每次运行写三个文件：

- `*.json`：`cad-steel-tonnage/v0.2`，含 `final_quantity`、长度口径、牌号吨位带、构件归并台账、连接清单、涂装清单、复核清单、分截面吨位带、截面谱和仅计数截面。
- `*.md`：可读复核报告，置顶显示口径、长度依据、总吨位带和需复核项。
- `*.csv`：总吨位带、分截面吨位和截面谱的表格摘要。

JSON 关键字段包括 `provenance`、`contract_id`、`source_sha256`、`contract_sha256`、`reader_version`、`formal_ledger_eligible`、`run_manifest`、`length_basis`（`explicit/drawn/none`）、`length_used_m`、`rows`、`spec_rows`、`only_count`、`total_t`、`total_basis`、`total_t_member_level`、`total_t_allocated_estimate`、`member_merge`、`length_scenarios`、`allowance_advice`、`geometry_closure_check`、`prerequisites`、`input_evidence` 和 `summary`。长度为 `none` 或无可计截面时 `rows` 与 `total_t` 为空。

报告里对 `steel_geometry[]`、`connections[]`、`finishes[]` 为空的情况会明写“输入无证据”，与“技能未实现”区分。

## 使用边界

- 这是图面证据驱动的草稿估算，不替代深化设计、结构计算、翻样、下料、清单编制、结算、竣工计量或报价。
- 不做节点承载力、稳定性、防火等级、规范符合性或构件级精确净量判断。
- 不承诺识别任何图纸；没有 `cad-file-reader` 钢结构识图包产物时不出数，也不用 DWG 文件代替输入。
- 缺长度、缺厚度、缺宽度或表外规格时如实“仅计数”；识别层标记的 `review` 和缺口必须保留给人工复核。
- 暂不支持：除节点板以外的连接件吨位、焊缝吨位、构件级精确截面对应与净量、牌号对米重的影响、曲线或多段几何展开长度、三维模型涂装面积计算、防火等级推断。这些能力都按“暂不支持”或复核处理，不用默认值硬算。

