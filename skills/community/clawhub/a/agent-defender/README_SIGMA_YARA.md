# 🛡️ Sigma + YARA 规则集成系统

## 概述

本系统用于将 Sigma 和 YARA 安全规则统一集成到 agent-defender 中，实现：

- ✅ **统一加载** - 自动扫描和加载 Sigma/YARA 规则
- ✅ **格式转换** - 将 Sigma 转换为 Runtime 格式，YARA 转换为 JSON 格式
- ✅ **规则验证** - 检查规则语法和完整性
- ✅ **索引生成** - 生成可搜索的规则索引
- ✅ **自动同步** - 将集成规则同步到 agent-defender

## 快速开始

### 1. 运行集成脚本

```bash
cd ~/.openclaw/workspace/skills/agent-defender
python3 integrate_sigma_yara.py
```

### 2. 查看输出

```bash
# 查看集成规则
cat integrated_rules/integrated_rules.json

# 查看规则索引
cat integrated_rules/RULES_INDEX.yaml

# 查看集成日志
cat integrated_rules/integration.log
```

### 3. 验证集成

```bash
# 检查生成的规则文件
ls -la rules/*_integrated.json
```

## 目录结构

```
agent-defender/
├── integrate_sigma_yara.py       # 集成脚本
├── config/
│   └── integration_config.yaml   # 配置文件
├── integrated_rules/             # 集成规则输出目录
│   ├── integrated_rules.json     # 所有集成规则
│   ├── RULES_INDEX.yaml          # 规则索引
│   └── integration.log           # 集成日志
├── rules/                        # agent-defender 规则目录
│   ├── prompt_injection_integrated.json
│   ├── tool_poisoning_integrated.json
│   └── ...
└── README_SIGMA_YARA.md          # 本文档
```

## 支持的规则格式

### Sigma 规则

Sigma 规则会自动转换为 Runtime 格式：

**原始 Sigma:**
```yaml
title: Detect Prompt Injection
id: sigma-prompt-001
level: high
description: Detects prompt injection attempts
detection:
  selection:
    - "ignore previous instructions"
    - "disregard all safety"
  condition: any
```

**转换后 Runtime:**
```json
{
  "id": "sigma-prompt-001",
  "name": "Detect Prompt Injection",
  "type": "Runtime",
  "severity": "high",
  "detection": {
    "type": "pattern_match",
    "patterns": [".*ignore previous instructions.*", ".*disregard all safety.*"],
    "condition": "any"
  }
}
```

### YARA 规则

YARA 规则会转换为 JSON 格式并保留原始规则：

**原始 YARA:**
```yara
rule ToolPoisoning {
  meta:
    description = "Detects tool poisoning attacks"
    severity = "critical"
    mitre_id = "T1059"
  strings:
    $a = "os.system"
    $b = "subprocess.call"
  condition:
    $a or $b
}
```

**转换后 JSON:**
```json
{
  "id": "YARA-ToolPoisoning",
  "name": "Tool Poisoning Detection",
  "type": "YARA",
  "severity": "critical",
  "detection": {
    "type": "yara",
    "strings": ["$a = \"os.system\"", "$b = \"subprocess.call\""],
    "condition": "$a or $b",
    "raw_rule": "rule ToolPoisoning { ... }"
  },
  "metadata": {
    "mitre_id": "T1059",
    "attack_type": "tool_poisoning"
  }
}
```

## 命令行选项

```bash
# 基本使用
python3 integrate_sigma_yara.py

# 使用自定义配置
python3 integrate_sigma_yara.py --config config/integration_config.yaml

# 仅处理 Sigma 规则
python3 integrate_sigma_yara.py --sigma-only

# 仅处理 YARA 规则
python3 integrate_sigma_yara.py --yara-only

# 验证模式 (不保存)
python3 integrate_sigma_yara.py --dry-run

# 详细输出
python3 integrate_sigma_yara.py --verbose

# 指定规则目录
python3 integrate_sigma_yara.py \
  --sigma-dir /path/to/sigma \
  --yara-dir /path/to/yara
```

## 与 agent-defender 集成

### 在 agent-defender 中加载集成规则

```python
# defender_core.py
import json
from pathlib import Path

class DefenderCore:
    def __init__(self):
        self.rules = []
        self.load_integrated_rules()
    
    def load_integrated_rules(self):
        """加载集成规则"""
        rules_file = Path("integrated_rules/integrated_rules.json")
        if rules_file.exists():
            with open(rules_file) as f:
                data = json.load(f)
                self.rules = data.get("rules", [])
            print(f"✅ 加载 {len(self.rules)} 条集成规则")
    
    def detect(self, code: str) -> list:
        """使用集成规则检测"""
        threats = []
        for rule in self.rules:
            if rule["type"] == "Runtime":
                if self._runtime_detect(code, rule):
                    threats.append(rule)
            elif rule["type"] == "YARA":
                if self._yara_detect(code, rule):
                    threats.append(rule)
        return threats
    
    def _runtime_detect(self, code: str, rule: dict) -> bool:
        """Runtime 规则检测"""
        patterns = rule.get("detection", {}).get("patterns", [])
        for pattern in patterns:
            if re.search(pattern, code, re.IGNORECASE):
                return True
        return False
    
    def _yara_detect(self, code: str, rule: dict) -> bool:
        """YARA 规则检测"""
        raw_rule = rule.get("detection", {}).get("raw_rule", "")
        if raw_rule:
            # 使用 yara-python 库
            import yara
            compiled = yara.compile(source=raw_rule)
            matches = compiled.match(data=code.encode())
            return len(matches) > 0
        return False
```

### 在扫描器中使用

```bash
# 使用 defenderctl 扫描
./defenderctl.sh scan --rules integrated_rules/integrated_rules.json target_code.py

# 或使用 API
curl -X POST http://localhost:8080/scan \
  -H "Content-Type: application/json" \
  -d '{"code": "...", "rules": "integrated"}'
```

## 规则管理

### 查看规则统计

```bash
# 使用 jq 查看统计
cat integrated_rules/integrated_rules.json | jq '.stats'

# 按类型统计
cat integrated_rules/integrated_rules.json | jq 'group_by(.type) | map({type: .[0].type, count: length})'

# 按严重程度统计
cat integrated_rules/integrated_rules.json | jq 'group_by(.severity) | map({severity: .[0].severity, count: length})'
```

### 搜索规则

```bash
# 使用 grep 搜索
grep -r "prompt_injection" integrated_rules/

# 使用 Python 搜索
python3 -c "
import json
with open('integrated_rules/integrated_rules.json') as f:
    rules = json.load(f)['rules']
    for r in rules:
        if 'prompt' in r.get('description', '').lower():
            print(r['id'])
"
```

### 更新规则

```bash
# 重新运行集成 (会覆盖现有规则)
python3 integrate_sigma_yara.py

# 增量更新 (保留现有规则)
python3 integrate_sigma_yara.py --incremental

# 验证规则更新
python3 integrate_sigma_yara.py --validate-only
```

## 自动化

### Cron 定时更新

```bash
# 编辑 crontab
crontab -e

# 添加定时任务 (每天凌晨 2 点)
0 2 * * * cd ~/.openclaw/workspace/skills/agent-defender && python3 integrate_sigma_yara.py >> logs/integration.log 2>&1
```

### Systemd 服务

```ini
# /etc/systemd/system/defender-rules.service
[Unit]
Description=Agent Defender Rules Integration
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /home/cdy/.openclaw/workspace/skills/agent-defender/integrate_sigma_yara.py
WorkingDirectory=/home/cdy/.openclaw/workspace/skills/agent-defender
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

```bash
# 启用服务
sudo systemctl enable defender-rules.service

# 定时运行 (配合 timer)
sudo systemctl start defender-rules.service
```

## 故障排除

### 常见问题

#### 1. 规则加载失败

**症状:** `ERROR: 加载 Sigma 规则失败 xxx.yaml`

**解决:**
```bash
# 验证 YAML 语法
python3 -c "import yaml; yaml.safe_load(open('rule.yaml'))"

# 检查文件编码
file rule.yaml  # 应该是 UTF-8
```

#### 2. 转换错误

**症状:** `ERROR: 转换 Sigma 规则失败 xxx: missing 'detection'`

**解决:**
- 确保 Sigma 规则包含 `detection` 字段
- 检查规则格式是否符合 Sigma 规范

#### 3. 性能问题

**症状:** 集成过程缓慢

**解决:**
```yaml
# 在配置文件中调整
performance:
  parallel_count: 8  # 增加并发数
  use_cache: true    # 启用缓存
```

### 日志分析

```bash
# 查看错误日志
grep "ERROR" integrated_rules/integration.log

# 查看警告
grep "WARNING" integrated_rules/integration.log

# 实时查看日志
tail -f integrated_rules/integration.log
```

## 性能基准

在典型配置下的性能表现：

| 规则数量 | 处理时间 | 内存使用 |
|---------|---------|---------|
| 100     | <5s     | <50MB   |
| 500     | <20s    | <100MB  |
| 1000    | <40s    | <200MB  |

## 贡献

欢迎提交新的规则格式支持或改进建议！

### 添加新的规则格式

1. 在 `RuleIntegrator` 类中添加新的加载方法
2. 实现格式转换逻辑
3. 更新配置文件支持
4. 添加测试用例

## 许可证

与 agent-defender 保持一致

## 参考资料

- [Sigma 规范](https://github.com/SigmaHQ/sigma)
- [YARA 文档](https://virustotal.github.io/yara/)
- [agent-defender 文档](../README.md)
- [MITRE ATT&CK](https://attack.mitre.org/)

---

**最后更新:** 2026-03-23
**版本:** 1.0
