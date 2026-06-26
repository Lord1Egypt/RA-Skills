# 可转债打新助手 🎯

**免费工具** - 可转债投资必备神器

[![ClawHub](https://img.shields.io/badge/ClawHub-skill-blue)](https://clawhub.com)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## ✨ 功能亮点

- 📅 **打新日历** - 每日可申购转债提醒
- 📊 **新债分析** - 基本面 + 行业对比
- 📈 **溢价预测** - 上市价格智能预测
- ⚠️ **监控提醒** - 强赎/下修/回售预警

---

## 🚀 快速开始

### 安装依赖
```bash
pip3 install -r requirements.txt
```

### 使用示例
```bash
# 今日可申购
python main.py today

# 新债分析
python main.py analyze 123205

# 溢价预测
python main.py predict 123205

# 监控提醒
python main.py alerts
```

---

## 📖 完整文档

- [用户指南](references/USER_GUIDE.md)
- [API 文档](references/API.md)
- [技能说明](SKILL.md)

---

## 💡 投资策略

### 无脑申购条件
- ✅ 评级 AA 及以上
- ✅ 规模 < 20 亿
- ✅ 正股非 ST

### 预期收益
- 平均每签赚 **200-500 元**
- 中签率约 **0.001%-0.01%**

---

## ⚠️ 风险提示

1. 约 5-10% 新债可能破发
2. 强赎忘记操作可能亏损 50%+
3. 低评级转债有违约风险

---

## 📦 项目结构

```
convertible-bond-assistant/
├── main.py                    # 主入口
├── cb_calendar.py             # 打新日历
├── cb_analysis.py             # 新债分析
├── cb_premium_predict.py      # 溢价预测
├── cb_monitor.py              # 监控提醒
├── requirements.txt           # 依赖
├── SKILL.md                   # 技能说明
├── README.md                  # 本文件
├── data/                      # 数据缓存
└── references/                # 文档
    ├── USER_GUIDE.md
    └── API.md
```

---

## 🙏 致谢

- 数据源：东方财富、新浪财经、集思录
- 平台支持：OpenClaw

---

## 📞 反馈

欢迎提交 Issue 或 Pull Request！

**版本**: 1.0.0  
**作者**: Your Name  
**更新日期**: 2026-03-07
