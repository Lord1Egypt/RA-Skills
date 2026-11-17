# Doors / Windows / Stairs / Insulation / Waterproof Geometry

把门窗表、门窗平面、楼梯详图、保温做法和防水做法图纸读成可复核识图候选：门/窗编号、楼梯梯段/休息平台/栏杆扶手、保温层、防水层及标高证据。

只做识图候选，不计算门窗数量、面积、墙体保温体积、防水面积、材料量、造价或结算量。

## 触发
- 需要识别门窗/楼梯/保温/防水的图纸类型、系统、构件、编号/标高和图层证据。
- 需要给装饰/土建物资计划提供带坐标和证据的识图输入。

## 使用
```bash
scripts/cad_scan.sh 门窗楼梯图.dwg --with-mtext --with-insert --with-geom --with-geom-layer --detail-json 详情.json --format json -o 扫描
scripts/cad_doors_windows_stairs_insulation_waterproof.sh 详情.json --out-dir 识图
```

## 边界
- 不输出门窗数量/面积、楼梯展开长度、保温/防水面积、材料量、造价；比例/单位不明进 review。
