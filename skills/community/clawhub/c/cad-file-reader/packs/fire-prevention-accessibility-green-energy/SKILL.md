# Fire Prevention / Accessibility / Green Energy Geometry

把防火分区、疏散平面、无障碍设计、绿建节能和海绵城市图纸读成可复核识图候选：防火分区/疏散路线/防火门/防火卷帘、无障碍坡道/通道/卫生间、屋顶绿化/雨水花园/渗透设施、光伏板和节能做法。

只做识图候选，不输出防火分区面积、疏散距离判定、无障碍等级、绿建评分、能耗或造价。

## 触发
- 需要识别防火/疏散/无障碍/绿建节能/海绵城市的图纸类型、系统、构件、分区编号/标高和图层证据。
- 需要给专项审查或物资计划提供带坐标和证据的识图输入。

## 使用
```bash
scripts/cad_scan.sh 防火节能图.dwg --with-mtext --with-insert --with-geom --with-geom-layer --detail-json 详情.json --format json -o 扫描
scripts/cad_fire_prevention_accessibility_green_energy.sh 详情.json --out-dir 识图
```

## 边界
- 不输出疏散距离/防火面积、无障碍合规结论、绿建评分、能耗量、材料量、造价；比例/单位不明进 review。
