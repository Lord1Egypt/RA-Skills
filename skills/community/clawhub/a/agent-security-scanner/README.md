# Agent Security Scanner v4.1.0

**企业级 AI Agent 安全扫描器**

[![Version](https://img.shields.io/badge/version-4.1.0-blue.svg)](https://github.com/agent-security/scanner/releases/tag/v4.1.0)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Detection Rate](https://img.shields.io/badge/detection-100%25-brightgreen.svg)](docs/DELIVERY_REPORT.md)
[![False Positive Rate](https://img.shields.io/badge/fpr-7.77%25-brightgreen.svg)](docs/DELIVERY_REPORT.md)
[![Speed](https://img.shields.io/badge/speed-5019/s-brightgreen.svg)](docs/DELIVERY_REPORT.md)

---

## 🎯 快速开始

```bash
# 安装
git clone https://github.com/agent-security/scanner.git
cd scanner/release/v4.1
pip install -r requirements.txt

# 扫描
python3 src/fast_batch_scan.py

# 验证
python3 -c "from src.multi_language_scanner_v4 import MultiLanguageScanner; print('✅ OK')"
```

## 📊 性能指标

| 指标 | 值 | 目标 | 状态 |
|------|-----|------|------|
| 检测率 | **100%** | ≥85% | ✅ |
| 误报率 | **7.77%** | ≤15% | ✅ |
| 速度 | **5019/s** | ≥4000/s | ✅ |

## 🏗️ 架构

```
三层检测架构:
├─ 一层：白名单/黑名单 (快速筛查)
├─ 二层：智能评分 + 意图分析 (边界判定)
└─ 三层：LLM 深度分析 (不确定样本)
```

## 📁 目录

```
release/v4.1/
├── src/           # 核心源代码
├── config/        # 配置文件
├── docs/          # 文档
├── examples/      # 示例
├── tests/         # 测试
├── *.sh           # 脚本
├── package.json   # npm 配置
├── SKILL.md       # 技能规范
└── README.md      # 本文件
```

## 🚀 使用

```bash
# 单个文件
python3 src/multi_language_scanner_v4.py sample.py

# 批量扫描
python3 src/fast_batch_scan.py

# 灵顺优化
bash lingshun_optimize.sh
```

## 📖 文档

- [用户指南](docs/USER_GUIDE.md)
- [交付报告](docs/DELIVERY_REPORT.md)
- [技能规范](SKILL.md)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License
