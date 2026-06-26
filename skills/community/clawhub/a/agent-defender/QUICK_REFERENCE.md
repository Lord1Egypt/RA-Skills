# 📋 Sigma/YARA 规则集成 - 快速参考

## 一键命令

```bash
# 运行集成
cd ~/.openclaw/workspace/skills/agent-defender && python3 integrate_sigma_yara.py

# 测试规则
python3 test_integrated_rules.py

# 查看统计
cat integrated_rules/integrated_rules.json | jq '.stats'

# 查看规则索引
cat integrated_rules/RULES_INDEX.yaml | head -50

# 查看日志
tail -f integrated_rules/integration.log
```

## 规则统计 (当前)

| 类型 | 数量 |
|------|------|
| Sigma (Runtime) | 6 |
| YARA (JSON) | 10 |
| **总计** | **16** |

## 攻击类型覆盖

| 攻击类型 | 规则数 | 文件 |
|---------|--------|------|
| Prompt Injection | 4 | `prompt_injection_integrated.json` |
| Tool Poisoning | 6 | `tool_poisoning_integrated.json` |
| Data Exfiltration | 4 | `data_exfil_integrated.json` |
| Resource Exhaustion | 2 | `resource_exhaustion_integrated.json` |

## 文件位置

```
~/.openclaw/workspace/skills/agent-defender/
├── integrate_sigma_yara.py          # 集成脚本
├── test_integrated_rules.py         # 测试脚本
├── config/integration_config.yaml   # 配置
├── integrated_rules/                # 输出目录
│   ├── integrated_rules.json        # 所有规则
│   ├── RULES_INDEX.yaml             # 索引
│   └── integration.log              # 日志
└── rules/                           # 同步规则
    └── *_integrated.json            # 分类规则
```

## Python 使用示例

```python
from pathlib import Path
import json

# 加载规则
rules_file = Path("~/.openclaw/workspace/skills/agent-defender/integrated_rules/integrated_rules.json").expanduser()
with open(rules_file) as f:
    rules = json.load(f)["rules"]

# 检测代码
def detect(code: str) -> list:
    threats = []
    for rule in rules:
        if rule["type"] == "Runtime":
            patterns = rule.get("detection", {}).get("patterns", [])
            for pattern in patterns:
                if re.search(pattern, code, re.IGNORECASE):
                    threats.append(rule)
                    break
        elif rule["type"] == "YARA":
            # 使用 yara-python
            import yara
            raw_rule = rule.get("detection", {}).get("raw_rule", "")
            if raw_rule:
                compiled = yara.compile(source=raw_rule)
                matches = compiled.match(data=code.encode())
                if matches:
                    threats.append(rule)
    return threats
```

## 命令行选项

```bash
# 基本使用
python3 integrate_sigma_yara.py

# 自定义配置
python3 integrate_sigma_yara.py --config config/integration_config.yaml

# 仅 Sigma
python3 integrate_sigma_yara.py --sigma-only

# 仅 YARA
python3 integrate_sigma_yara.py --yara-only

# 验证模式
python3 integrate_sigma_yara.py --dry-run

# 详细输出
python3 integrate_sigma_yara.py --verbose
```

## 定时更新 (Cron)

```bash
# 编辑 crontab
crontab -e

# 每天凌晨 2 点更新
0 2 * * * cd ~/.openclaw/workspace/skills/agent-defender && python3 integrate_sigma_yara.py >> logs/integration.log 2>&1
```

## 故障排除

```bash
# 查看错误
grep "ERROR" integrated_rules/integration.log

# 验证规则
python3 -c "import yaml; yaml.safe_load(open('rule.yaml'))"

# 重新生成
rm -rf integrated_rules/*
python3 integrate_sigma_yara.py
```

## 文档链接

- 📖 [完整文档](README_SIGMA_YARA.md)
- 📊 [集成报告](INTEGRATION_REPORT.md)
- 📝 [总结](COMPLETION_SUMMARY.md)
- ⚙️ [配置](config/integration_config.yaml)

---

**最后更新:** 2026-03-23  
**版本:** 1.0
