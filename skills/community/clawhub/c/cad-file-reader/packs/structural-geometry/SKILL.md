# Structural Geometry / 结构识图中间数据包

版本：0.41.0

本包把结构施工图读成“专项算量可复核”的结构/配筋/节点/洞口识图候选：结构平面、配筋图、基础图、楼梯、节点详图、结构说明。

只做识图证据，不做混凝土/钢筋算量；钢筋直径等级、锚固、搭接和洞口加强只出候选，最终数量交给 `tujian-suanliang` 或结构专项 skill。

## 触发
- 需要识别结构图纸类型、结构系统、构件（梁/板/柱/墙/基础/楼梯/洞口）、配筋、节点和轴网候选。
- 需要给土建算量/物资计划提供带坐标、图层、图框和原文证据的结构识图输入。

## 快速审计
```bash
scripts/cad_scan.sh 结构图.dwg --with-mtext --with-insert \
  --with-geom --with-geom-layer --with-block-expand \
  --detail-json 结构详情.json --format json -o 结构扫描
scripts/cad_structural_geometry.sh 结构详情.json --out-dir 结构识图
```

输入必须是 `cad_scan --with-mtext --with-insert --with-geom --with-geom-layer --with-block-expand` 的详情 JSON。`--with-block-expand` 把模型空间直画实体和 INSERT 块内 LINE/LWPOLYLINE 写入 `block_geometry[].segments[]`，默认最多 200000 段；截断或异常写 review，不中断整批。未开块展开时结构输出仍可出语义图层候选，并追加 `block_geometry_unavailable` 复核项，不伪造块内几何。

输出：
- `*.structural.json`：结构识图候选与证据；新增 `structural_geometry[]` 的 `category=raw_geometry` 行、`blocks[]`、`units`、`review[]`。
- `*.structural.md`：可读复核报告。
- `*.structural.csv`：候选台账。

原始块几何保留 6 位坐标和 `handle/source_block/entity_kind`；块基点、handle 缺失只进 review，不补造。语义图层行 `source=semantic_layer`、`handle=null`；块内行 `source=modelspace` 或 `block:<块名>`。

## 识别范围
- 图纸类型：结构/梁/板/柱/墙平面图、配筋图、基础图、楼梯详图、节点详图、柱表、结构说明。
- 系统：混凝土、钢筋、基础、楼梯、预制、加固。
- 构件候选：梁、板、柱、墙、基础（承台/筏板/桩）、楼梯、洞口加强、节点加强。
- 配筋候选：HPB300/HRB400 等等级、直径@间距、纵筋/箍筋/附加筋/负筋/拉筋/分布筋。
- 编号候选：KL/WKL/KZ/YBZ/GBZ/LB/WB/Q/CT/FB/JZL 等结构编号。
- 节点/轴网：节点号、轴线与标高候选。
- 复核项：缺几何、缺图纸类型、缺比例/单位、缺图层、配筋未绑定构件。

## 边界
- 不计算体积、面积、长度汇总、混凝土方量、钢筋吨位、锚固长度、接头数量或造价。
- 不把钢筋标注自动换算成下料/翻样量；只保留原文、坐标和图层证据。
- 比例/单位不明时进入 `review`，不用默认比例推算。
- 不替代设计审查、平法深化、翻样下料、清单计价和结算。
