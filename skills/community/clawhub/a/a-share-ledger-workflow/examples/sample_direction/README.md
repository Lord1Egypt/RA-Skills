# 示例方向（sample_direction）

> 两个虚构标的（示例甲科技 600000、示例乙科技 600001），
> 演示"台账 ↔ 状态表 ↔ bench.json ↔ 名称缓存"四向一致的最小结构。
> ⚠️ 所有名称/代码/数值均为虚构，不构成任何推荐。

## 目录（即最小可用 $STOCK_DATA_DIR）

```
sample_direction/
├── bench.json                  # 门槛数据（两只标的 7 项字段 + constants）
├── config.yaml                 # 阈值记录（与 bench.json constants 一致；脚本不读它）
├── 股票台账/
│   ├── 候选/
│   │   ├── 示例甲科技_600000_跟踪台账.md
│   │   └── 示例乙科技_600001_跟踪台账.md
│   ├── 流程状态表.md
│   └── 模板/
│       └── 单股跟踪台账_模板.md   # 与仓库 templates/ledger_template.md 同源
└── 方向记录/
    ├── 示例行业甲_方向档案.md
    └── 数据/
        └── 代码名称映射.json     # 第 8 项离线通过的关键：预填名称缓存，免联网
```

## 验证（隔离运行，不碰你的真实数据）

```bash
rm -rf /tmp/demo && mkdir -p /tmp/demo
cp -r examples/sample_direction/* /tmp/demo/
STOCK_DATA_DIR=/tmp/demo python3 scripts/validate_ledgers.py
```

预期：`台账 2 份：无问题 2，有问题 0`，状态表/字典/名称绑定/模板自检全 ✅，
`rc=0`，另有 2 项跳过提示（无 cron、无 HERMES_HOME —— 新用户本就如此）。

## 破坏测试（改坏 → 确认报警 → 还原）

```bash
D=/tmp/demo
# 1. 台账↔数据不一致：第 7 项必须点名 600000
python3 - <<'EOF'
import json
p = "/tmp/demo/bench.json"
d = json.load(open(p, encoding="utf-8")); d["stock"]["600000"]["bench_pt"] = 9.9
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
EOF
STOCK_DATA_DIR=$D python3 scripts/validate_ledgers.py | grep "台账↔字典"
cp examples/sample_direction/bench.json $D/bench.json   # 还原

# 2. 状态表漏登记：第 6 项必须报"有台账未登记"
sed -i 's/、示例乙科技(600001)//' $D/股票台账/流程状态表.md
STOCK_DATA_DIR=$D python3 scripts/validate_ledgers.py | grep "未登记"
cp examples/sample_direction/股票台账/流程状态表.md $D/股票台账/流程状态表.md   # 还原

# 3. 还原后复验：rc=0
STOCK_DATA_DIR=$D python3 scripts/validate_ledgers.py > /dev/null; echo "rc=$?"
```

## 改数值时的铁律

一个数字散落在 4 处（bench.json ↔ 台账 §0.1 ↔ §3 ↔ §4），改一处必须同步另三处；
改完重跑上面第 1 条，确认第 7 项不报警。
