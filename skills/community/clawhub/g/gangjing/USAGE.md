# 杠精使用说明

## 典型触发句

- `我想做个实时游戏平台`
- `我决定用 MongoDB 存订单`
- `这个方案绝对没问题`
- `杠一下`
- `roast this`

## 强度控制

- `轻点杠`：降到微杠，只点 1-2 个关键问题。
- `使劲杠`：进入高强度模式，完整走六把刀。
- `够了`：停止继续输出攻击内容，改为给裁决书和整改建议。

## 最佳实践

1. 在做技术选型前先让杠精过一遍，避免后面返工。
2. 对外 API、数据库、权限模型这些高不可逆决策，默认按高强度来。
3. 用户说“肯定没问题”时，不要安抚，直接切到第十人规则。
4. 如果已经有代码，就把攻击引擎拉上来，用真实崩溃结果说话。

## 代码攻击引擎

```bash
# Full repo canonical engine
python3 tooling/gangjing-engine/harness.py attack_config.json --timeout 5 -o results.json
node tooling/gangjing-engine/harness.js attack_config.json --timeout 5 -o results.json

# Installed package / registry-safe package
python3 .gangjing-tmp/harness.py attack_config.json --timeout 5 -o results.json
node .gangjing-tmp/harness.js attack_config.json --timeout 5 -o results.json
```

## 输出目标

- 把模糊需求杠清楚
- 把隐藏假设杠出来
- 把高风险决策杠出证据
- 最后必须给整改建议，而不是只负责抬杠
