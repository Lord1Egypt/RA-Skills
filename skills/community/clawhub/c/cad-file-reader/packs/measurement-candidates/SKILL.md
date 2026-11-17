# Measurement Candidates / 识图测量候选层

本包是 `cad-file-reader` 的薄测量层：把已经提取的识图中间数据转成**长度、面积、体积候选值**，同时保留比例、单位、图面数值、计算式、证据坐标和复核原因。

它不输出最终工程量。扣减、重叠、做法映射、洞口侧壁、损耗、分账、清单量、材料量和结算量仍由 `tujian-suanliang`、`zhuangshi-suanliang`、`anzhuang-suanliang` 或对应专项 skill 负责。

## 触发

- 用户问某个房间、墙段、洞口、吊顶分区、路由段或构件线段的长度/面积/体积候选。
- 用户需要把 `cad_scan` 详情或专业识图 JSON 转成可追溯测量台账。
- 专项算量 skill 需要识图底座先给一个带比例单位依据的复核基准。

## 快速使用

```bash
# 先做识图
scripts/cad_scan.sh 图纸.dwg --with-mtext --with-insert --with-geom --with-geom-layer \
  --detail-json 图纸详情.json --format json -o 图纸扫描
scripts/cad_descriptive_geometry.sh 图纸详情.json --out-dir 描述几何

# 再生成测量候选；比例/单位默认读取 scale_unit_audit
scripts/cad_measure.sh 描述几何/图纸详情.descriptive.json --out-dir 测量候选

# 也可显式覆盖比例/单位；缺比例或单位时只保留图面数值并转 review
scripts/cad_measure.sh 描述几何/图纸详情.descriptive.json \
  --scale 1:100 --unit mm --coordinate-space model --out-dir 测量候选

# 只有在已有面积候选且设计明确厚度/高度时，才生成待复核体积候选
scripts/cad_measure.sh 描述几何/图纸详情.descriptive.json \
  --thickness-m 0.10 --out-dir 测量候选
```

## 输出契约

`*.json` 顶层：

- `schema`：`cad-measurement-candidates/v1`
- `summary`：长度、面积、体积候选数、待复核数；`final_quantities` 固定为 `0`
- `measurements[]`：每条候选包含
  - `kind`：`length` / `area` / `volume`
  - `value`、`unit`：换算后的候选值和 `m` / `m2` / `m3`
  - `value_drawing_units`、`drawing_unit`：原始图面数值和单位
  - `scale`、`space`、`scale_applied`：比例与空间依据
  - `basis`、`method`、`formula`：多边形鞋带公式、线段合计、原文显式值或面积×厚度
  - `status`：`candidate` / `review`
  - `confidence`、`review_reason`、`evidence`
  - `source_schema`、`source_id`
  - `final_quantity=false`
- `review[]`：所有待复核测量
- `contract`：`cad-file-reader/v0` 统一契约；`confirmed_evidence` / `inferred_candidate` 进入 `candidates[]`，`review_required` 进入 `review_candidates[]`
- `boundary`：固定说明本层不做最终工程量

## 计算边界

- 长度：单段或图层线段合计候选；MEP、钢结构、市政单段长度一律是识图证据，不是最终管长/构件长度。
- 面积：显式文字面积可直接作为高置信候选；闭合多边形用鞋带公式；外接框面积只能作定位证据，始终 `review`。
- 体积：只接受原文显式体积，或“面积候选 × 显式厚度/高度”；不做洞口、构件相交、降板、层高、做法、损耗和分账。
- 比例与单位：`model` 空间只按坐标单位换算；只有 `paper/layout` 空间且比例明确时才应用 `1:N` 比例。缺比例或单位时 `value=null`，保留图面数值并转 `review`。
- 不做回路匹配、管径推断、芯数展开、钢筋重量、钢材重量、材料量、清单计价或结算。

## 与专项算量 skill 的交接

专项 skill 读取本包 JSON 时只把 `measurements[]` 当作带证据的复核基准：

- `tujian-suanliang`：复核梁板柱墙、楼梯、洞口等专项净量，最终扣减和分账仍由本技能计算。
- `zhuangshi-suanliang`：复核房间面积、墙段长度、顶棚分区和洞口位置，做法映射、侧壁、损耗和材料台账仍由本技能计算。
- `anzhuang-suanliang`：复核路由段和系统拓扑证据，规格匹配、竖向路由、预留、损耗和材料量仍由本技能计算。
- 任何专项 skill 都不得把 `final_quantity=false` 的候选直接改名为清单量或结算量。

## 边界

- 不输出最终工程量、材料量、造价、结算量。
- 不替代设计单位、翻样、下料、清单编制和专业算量软件。
- 不把公司项目路径或真实图纸内容写入技能发布内容。
