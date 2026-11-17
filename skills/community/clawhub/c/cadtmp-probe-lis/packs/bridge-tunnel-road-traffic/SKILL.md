# Bridge / Tunnel / Road Traffic Geometry

把桥梁、隧道、道路线形、交通设施图纸读成可复核的识图候选：桥墩/桥台/盖梁/支座/伸缩缝、隧道洞口/衬砌/仰拱、道路中线/平竖曲线/横断面、交通标志标线/护栏/信号灯。

只做识图候选，不计算桥隧长度、道路面积、材料量、造价或结算量。

## 触发
- 需要识别桥梁/隧道/道路/交通的图纸类型、系统、构件、桩号/坐标和图层证据。
- 需要给交通市政类物资计划或专项算量提供带坐标和证据的识图输入。

## 使用
```bash
scripts/cad_scan.sh 桥隧图.dwg --with-mtext --with-insert --with-geom --with-geom-layer --detail-json 详情.json --format json -o 扫描
scripts/cad_bridge_tunnel_road_traffic.sh 详情.json --out-dir 识图
```

## 边界
- 不输出长度/面积汇总、工程量、材料量、造价；比例/单位不明进 review。
