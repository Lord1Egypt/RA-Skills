# Interior Finish / 精装修室内深化识图中间数据包

本包把精装修/室内深化图读成可复核的识图候选：图纸类型、系统、饰面/门/固定家具构件、做法编号/材料/标高标注和图层面模型。

只做识图证据，不高定排版数量、不计算饰面面积、材料量或造价；算量交给 `zhuangshi-suanliang` 或装饰专项 skill。

## 触发
- 需要识别精装修平面、立面、节点、做法表、门表、固定家具等图纸类型和系统。
- 需要给装饰算量/物资计划提供带坐标、图层、图框和原文证据的深化识图输入。

## 快速审计
```bash
scripts/cad_scan.sh 装修图.dwg --with-mtext --with-insert \
  --with-geom --with-geom-layer --detail-json 装修详情.json --format json -o 装修扫描
scripts/cad_interior_finish_geometry.sh 装修详情.json --out-dir 装修深化识图
```

输入必须是 `cad_scan --with-mtext --with-insert --with-geom --with-geom-layer` 的详情 JSON。

输出：
- `*.interior_finish.json` / `.md` / `.csv`：精装修/室内深化识图候选与证据。

## 识别范围
- 图纸类型：精装修平面、立面、节点、做法表、门表/窗表、固定家具平面。
- 系统：地面、墙面、顶棚、踢脚、固定家具、防水。
- 构件候选：地面做法、墙面饰面、顶棚饰面、踢脚、门/窗、固定柜体/台面、防水层。
- 标注候选：标高、做法编号（DM/QM/WM/CM/JM）、材料、节点号（JD/XD/SC）。
- 复核项：缺几何、缺图纸类型、缺比例/单位、图层未分类、材料/做法未绑定。

## 边界
- 不输出饰面面积、排版数量、材料量、造价或结算量。
- 做法编号/标高只作证据候选；缺比例/单位或未绑定几何时进入 `review`。
- 不替代深化设计、清单计价和结算。
