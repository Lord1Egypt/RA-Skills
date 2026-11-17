# Pile / Foundation / Slope Geometry

把桩基、基坑支护、边坡防护和地基处理图纸读成可复核识图候选：桩位/桩型/承台、支护桩/地下连续墙/内支撑/锚索/锚杆/土钉/腰梁、挡墙/抗滑桩/护坡/格构、搅拌桩/CFG/强夯、沉降/测斜监测点。

只做识图候选，不计算桩长、方量、支护结构量、材料量、造价或结算量。

## 触发
- 需要识别桩基/基坑/边坡/地基处理的图纸类型、系统、构件、桩号/标高和图层证据。
- 需要给土建物资计划提供带坐标证据的识图输入。

## 使用
```bash
scripts/cad_scan.sh 基坑图.dwg --with-mtext --with-insert --with-geom --with-geom-layer --detail-json 详情.json --format json -o 扫描
scripts/cad_pile_foundation_slope.sh 详情.json --out-dir 识图
```

## 边界
- 不输出桩长/方量、支护结构量、土方量、材料量、造价；比例/单位不明进 review。
