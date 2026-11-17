# Crane Layout / 塔吊布置识图包

把施工总平面/塔吊布置图读成可复核的「塔吊位置与图面证据」候选，供吊装校核、群塔布置复核和布置图出图继续消费。

只做识图：不选型、不验算、不判断覆盖是否满足、不替代厂家资料与专项施工方案。

## 触发

- 总平面图、基础阶段平面图、塔吊布置图里出现塔吊符号、`TC/QTZ/STT/XGT/ZSL` 块名或塔吊图层。
- 需要提取塔吊插入点、块基点修正后的回转中心、旋转/缩放、型号与臂长图面候选。
- 需要把塔吊位置接进 `cad-contract/v1`，避免下游再写一套 DWG 解析。

## 快速审计

```bash
# 推荐：先由 cad_scan 出详情 JSON（含块引用），再识图
scripts/cad_scan.sh 总平面图.dwg --with-mtext --with-insert \
  --with-geom --with-geom-layer --detail-json 总平面详情.json --format json -o 总平面扫描
scripts/cad_crane_geometry.sh 总平面详情.json --source-drawing 总平面图.dwg \
  --drawing-unit mm --out-dir 塔吊识图

# 也可直接给 DXF/DWG；DWG 仍由本技能内部调 cad_scan，不自写解析器
scripts/cad_crane_geometry.sh 总平面图.dxf --drawing-unit mm --out-dir 塔吊识图
```

- 块名/图层不在默认规则内时，追加 `--block "MY-CRANE"`、`--layer "塔吊布置"`（按字面量匹配，可重复或逗号分隔）。
- 图纸单位不明确时不要传 `--drawing-unit`：脚本按 mm 解释但所有塔吊强制进 `review`，不会冒充单位已知。

输出：

- `*.crane.json`：主结果。`crane_layout[]` 为塔吊数组（兼容别名 `towers[]`），并带 `contract`。
- `*.crane.md`：人工复核表、型号/臂长/圆旁证和复核项。
- `*.crane.csv`：一行一台塔吊的台账。

## 塔吊数组字段

| 字段 | 含义 |
|---|---|
| `crane_id` | 稳定 id：`图层|块名|序号`；同一批输入稳定，不拿型号当 id |
| `block_name` / `layer` / `handle` | 原始图面证据 |
| `insert_xyz_mm` | INSERT 插入点原始图纸坐标；z 不可得时为 `null` |
| `center_xy_m` | INSERT 仿射变换（块基点+平移+旋转+缩放）后的回转中心，显式 mm→m |
| `center_status` | `insert_point`（由插入块变换得到）；中心不可算时为 `unavailable` |
| `rotation_deg` / `scale` | INSERT 旋转角与 x/y/z 缩放 |
| `transform_status` | `insert_affine` / `base_point_unavailable` / `unsupported_ocs` 等细因 |
| `model_text` / `model` / `model_status` | 型号原文与候选；`model_status` 仅 `candidate|unknown`，多型号冲突进 `model_ambiguity` |
| `jib_length_m` / `jib_length_source` | 臂长只认明确“臂长/起重臂长”文字；来源 `text|none`，多值冲突进 `jib_conflict_values` |
| `radius_circles_m[]` | 附近圆半径旁证；`source=geometry|annotation`，`used_as_jib_length=false` |
| `evidence[]` | 插入块、文字原文、坐标、图层与距离 |

## 提取口径

- **必须做 INSERT 仿射变换**：`dx=(0-bx)*sx`、`dy=(0-by)*sy`，再按旋转角变换到插入点；禁止直接拿 BLOCK 定义坐标当塔吊中心。
- 块基点来自 DXF `BLOCK` 头；非标准 DXF 若 INSERT 出现在块定义之前，扫描结束后回填一次，找不到仍保持 `null`。
- 同图/同空间 2 m 内重复符号去重，保留证据更全、置信度更高的一条；重复项写进 `duplicates[]`。
- 型号只认块名或塔吊图层/标签附近的明确型号文字，15 m 外或弱上下文不采纳；不按“QTZ80 大概就是 80 t·m”之类规则反推。
- 臂长只认“臂长/起重臂长”明确文字；`幅度`、`工作半径`、`回转半径`、`R=` 一律排除。
- 圆只作旁证：距插入点 >1 m 或落在图例/标注图层的圆标 `annotation`，任何圆都不得写进 `jib_length_m`。

## 边界

- 不判断塔吊型号是否匹配现场、不读厂家性能表、不做覆盖/吊重/基础/附着/群塔防碰撞结论。
- 不输出塔吊数量结论、选型建议、施工方案或审批意见；`final_quantity=false`。
- DWG 直读拿不到块基点时，回转中心为 `null` 并进 review；优先用 DWG→DXF 副本，或先 `cad_scan --dwg-dxf-fallback --detail-json` 再识图，不伪造中心。
- 公司图纸默认只在本机处理；未经用户明确范围、字节与同意，不把图纸字节交给云端模型、在线 OCR/转换或第三方服务。
