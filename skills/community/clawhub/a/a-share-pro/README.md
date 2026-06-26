# A-Share Pro - A 股投资监控终极版

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

轻量级 A 股自选股管理 + 多数据源实时行情监控工具

---

## 🚀 快速开始

```bash
# 1. 安装
cd ~/.openclaw/workspace/skills/a-share-pro/scripts
./install.sh

# 2. 添加股票
python3 add_stock.py 600919 江苏银行

# 3. 查看列表
python3 list_stocks.py

# 4. 获取行情汇总
python3 summarize_performance.py
```

---

## 📊 功能对比

| 功能 | a-share-monitor (旧版) | a-share-pro (新版) |
|------|------------------------|--------------------|
| ✅ **多数据源** | ✔️ 腾讯/雪球/百度/Tushare | ✔️ 同上 |
| ✅ **持久化存储** | ❌ 无 | ✔️ 本地文本文件 |
| ✅ **自选股管理** | ❌ 需手动维护 | ✔️ 独立脚本 |
| ⚪ **技术指标** | ⏳ 待开发 | ⏳ 预留接口 |
| ✅ **轻量级** | ⚠️ 中等复杂度 | ✔️ 极简设计 |
| ✅ **易维护** | ⚠️ 需要 Python 环境 | ✔️ 开箱即用 |

---

## 💡 核心优势

### 1. 统一配置管理
所有路径和参数集中在 `scripts/config.py`，修改只需改一个地方。

### 2. 模块化设计
每个功能独立成脚本，职责清晰，易于理解和维护。

### 3. 无需 Token
主要使用免费数据源（腾讯/雪球/百度），降低使用门槛。

### 4. 纯文本存储
数据存为简单文本文件，编辑友好，版本控制友好。

---

## 📚 文档

详细说明请查看 [SKILL.md](SKILL.md)。

---

<div align="center">
<strong>Happy Investing! 📈✨</strong>
</div>
