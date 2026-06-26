# 🔍 ClawScan - OpenClaw Skill 安全扫描器

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一键扫描 OpenClaw Skill 安全风险，静态 + 动态双重检测。

## 为什么需要 ClawScan？

- **341 个恶意 Skill** 已被发现可窃取 API Key、加密货币钱包
- ClawHub 审核机制薄弱，**12% Skill 存在恶意行为**
- 安装前无法判断代码安全性

ClawScan 让你在安装前识别风险。

## 快速开始

```bash
# 安装
pip install clawscan

# 扫描本地 Skill
clawscan scan /path/to/skill

# 扫描 ClawHub 上的 Skill（需先安装）
clawscan scan ~/.claw/skills/mcp-server-prompts

# 详细报告
clawscan scan /path/to/skill --verbose

# JSON 输出（用于 CI/CD 集成）
clawscan scan /path/to/skill --json
```

## 风险分级

| 等级 | 图标 | 描述 | 示例 |
|------|------|------|------|
| 🔴 高危 | HIGH | 网络请求、文件写入、命令执行 | `requests.post()`, `subprocess.run()`, `open(..., 'w')` |
| 🟡 中危 | MEDIUM | 子进程导入、API Key 处理 | `import subprocess`, `os.getenv("API_KEY")` |
| 🟢 低危 | LOW | 纯计算逻辑 | 数学运算、字符串处理 |

## 检测能力

### 静态分析
- AST 解析识别危险函数调用
- 正则模式匹配可疑代码
- 检测加密钱包相关代码

### 动态分析
- RestrictedPython 沙箱执行
- 监控运行时导入和函数调用
- 识别实际触发的外部行为

## 示例输出

```
╭────────────────────────── Scan Summary ──────────────────────────╮
│ 🔴 malicious-skill                                               │
│                                                                  │
│ Overall Risk: HIGH                                               │
│ Files Scanned: 3                                                 │
│ Scan Duration: 15ms                                              │
│                                                                  │
│ Findings: 8 total                                                │
│   🔴 High: 4                                                     │
│   🟡 Medium: 3                                                   │
│   🟢 Low: 1                                                      │
╰──────────────────────────────────────────────────────────────────╯

🔴 HIGH RISK (4)
==================================================

network
  Network module imported: requests
  /skill/malicious.py:7

subprocess
  Subprocess execution: subprocess.run()
  /skill/malicious.py:24

📋 Recommendations
==================================================
  ⚠️  This Skill can make network requests...
  🚨 This Skill can execute system commands...
```

## Exit Codes

| Code | 含义 |
|------|------|
| 0 | 低危，安全 |
| 1 | 高危风险 |
| 2 | 中危风险 |
| 3 | 扫描错误 |

## CI/CD 集成

```yaml
# .github/workflows/security.yml
- name: Scan Skills
  run: |
    for skill in ~/.claw/skills/*/; do
      clawscan scan "$skill" --json
    done
```

## 技术架构

```
clawscan/
├── core/
│   ├── static_analyzer.py   # AST + 正则分析
│   ├── dynamic_tracer.py    # 沙箱动态执行
│   ├── risk_engine.py       # 风险评分
│   └── scanner.py           # 主扫描器
├── cli.py                    # 命令行界面
└── skill/                    # OpenClaw Skill 包装
```

## 开发

```bash
git clone https://github.com/yourname/clawscan.git
cd clawscan
pip install -e ".[dev]"
pytest
```

## Roadmap

- [ ] 规则库自动更新
- [ ] 社区风险情报共享
- [ ] Skill 签名验证
- [ ] Web 可视化报告

## 许可证

MIT
