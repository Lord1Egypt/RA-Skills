# 代码攻击引擎 — 杠精的第六把刀

杠精自带代码攻击引擎（`scripts/` 目录），用于"代码实锤"维度。
不是观点，是事实。不是"我觉得你代码有问题"，是"你的代码在 NaN
输入下崩溃了，这是证据"。

---

## 攻击引擎用法

### Step 1: 生成攻击配置

根据目标代码自动生成 JSON 攻击配置：

```json
{
  "target_module": "./target_file.py",
  "attacks": [
    {
      "name": "攻击名称",
      "function": "目标函数名",
      "args": ["恶意输入"],
      "category": "攻击类别",
      "severity": "HIGH",
      "payload_description": "攻击描述",
      "expect_exception": false,
      "expected": null,
      "validators": ["no_nan", "no_html", "no_proto_pollution"]
    }
  ]
}
```

攻击类别和 payload 模式参考 `references/attack-patterns.md`。

### Step 2: 执行攻击

完整仓库版脚本位于 `tooling/gangjing-engine/`。
如果当前安装包没有 ready-to-run 脚本，就从 `templates/attack-engine-kit.md`
落地临时 harness 再执行。

```bash
# Python 目标 — 每次攻击自动 fork 子进程隔离
python3 tooling/gangjing-engine/harness.py attack_config.json --timeout 5 -o results.json
python3 .gangjing-tmp/harness.py attack_config.json --timeout 5 -o results.json

# JavaScript 目标 — 支持 async/Promise，每次攻击 fork 子进程
node tooling/gangjing-engine/harness.js attack_config.json --timeout 5 -o results.json
node .gangjing-tmp/harness.js attack_config.json --timeout 5 -o results.json

# Go 目标 — 写 _test.go 文件，用 go test 执行
go test -v -run "." -timeout 30s -count=1 .
```

### Step 3: 解析结果

结果 JSON 结构：
```json
{
  "target": "模块名",
  "total_attacks": 15,
  "summary": {
    "crashed": 3,
    "wrong": 5,
    "survived": 6,
    "hung": 0,
    "leaked": 1
  },
  "resilience_score": 45,
  "grade": "D",
  "results": [
    {
      "name": "攻击名",
      "category": "类别",
      "severity": "HIGH",
      "verdict": "crashed",
      "detail": "TypeError: ...",
      "semantic_findings": []
    }
  ]
}
```

verdict 类型：
- **crashed** — 代码崩溃了（异常/段错误）
- **wrong** — 返回了错误的结果
- **hung** — 超时挂起
- **leaked** — 信息泄漏（原型污染/XSS）
- **survived** — 扛住了（杠精不太高兴）

### Step 4: 转化为杠精论据

把冷冰冰的 JSON 变成扎心的杠精话术：

```
💀 代码实锤:

跑了 [N] 次攻击，你的代码挂了 [M] 次。评分 [score]/100，等级 [grade]。

"代码没问题"？[M] 次崩溃不叫问题叫什么？叫feature吗？

具体来说：
- 💥 [CRITICAL攻击名]: [崩溃描述]
  → 你的 [函数名] 连 [输入类型] 都扛不住，这叫"没问题"？
- 🔓 [LEAKED攻击名]: [泄漏内容]
  → 原型污染都漏出来了，我建议你的安全方案改名叫"安全参考"

你说"代码足够健壮"这个假设，现在可以划掉了。
```

### Step 5: 生成报告（可选）

```bash
python3 -c "
import sys, json
sys.path.insert(0, 'tooling/gangjing-engine')
from report_html import load_results, render_html
targets = load_results(['results.json'])
html = render_html(targets)
with open('destruction_report.html', 'w') as f:
    f.write(html)
"
```

生成自包含 HTML 报告，带有：
- 韧性评分和等级（A-F）
- 甜甜圈图（verdict分布）
- 分类柱状图（按攻击类别）
- 可筛选的 Kill Log
- 搜索和过滤功能

### 何时不使用

- 🟢 微杠模式下不用（杀鸡不用牛刀）
- 用户还没写代码（只有设计没有实现）
- 用户明确说"跳过代码测试"
- 代码和当前决策无关
