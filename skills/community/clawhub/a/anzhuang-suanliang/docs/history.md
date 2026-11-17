# 安装算量版本与口径演进

原 SKILL.md「0.2.0 优化概况」，按需查阅。

## 0.2.0 优化概况

- 对接 `cad-file-reader >= 0.25.0`，扫描结果记录底座版本和测量候选兼容状态。
- `mep_plan.py --cad-measurement` 可把长度/面积/体积识图候选导入“CAD测量候选核对”工作表；候选固定 `final_quantity=false`，不参与本技能算量。
- 保留安装专业双口径输出、回路规格匹配、水系统分区、立管识别、支架估算和核对清单；不输出金额、结算量或竣工计量。

两步出表：先扫描 DWG 建索引，再用索引生成 xlsx。

```bash
# 1. 识图与扫描两条路（识图契约红线）：识图只由 cad-file-reader 产出契约，同一张图只解析一次
#    a) 已有 cad-file-reader 契约（cad_scan/cad_mep_geometry 产物）时只消费契约，不再打开 DWG：
bash scripts/mep_scan.sh 平面_契约.json --contract --out 平面.json
bash scripts/mep_scan.sh 系统_契约.json --contract --out 系统.json
bash scripts/mep_scan.sh 说明_契约.json --contract --out 说明.json
bash scripts/mep_scan.sh 干线_契约.json --contract --out 干线.json
#    b) 直接传 DWG 默认被拒（exit 2，提示先走 cad-file-reader）；仅回归/调试可用 CAD_ALLOW_DIRECT=1 逃生

# 2. 生成双口径表；已有 .scan.json 时不要重新扫 DWG
bash scripts/mep_plan.sh \
  --scan 平面.json \
  --system 系统.json 说明.json \
  --trunk-scan 干线.json \
  --out-prefix 安装计划
```

输出包含：口径、规范约束、双口径映射、导管与桥架、电线电缆、干线电缆、设备、图层分档、配电箱回路、未匹配坐标簇、分层、水专业、水系统分区、连通性核对、立管识别、支架估算、置信度分级、总量守恒、材料表提取、材料归并、立管估算、核对清单。

