---
name: convertible-bond-assistant
description: 可转债打新助手 - 免费工具。提供可转债申购日历、新债分析、上市溢价预测、中签率查询、强赎下修提醒。适用于 A 股可转债投资者。
author: Your Name
contact:
  email: your@email.com
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      packages: ["requests", "pandas", "beautifulsoup4"]
---

# 可转债打新助手

一个免费的可转债投资辅助工具，提供申购日历、新债分析、溢价预测等功能。

**版本**: 1.0.0  
**许可证**: MIT  
**定价**: 免费（引流工具）

---

## 🎯 核心功能

### 1. 打新日历
- 可申购新股列表（今日、明日、本周）
- 申购代码、申购上限
- 中签缴款提醒

### 2. 新债分析
- 发行规模、转股价格
- 债券评级（AAA/AA+/AA 等）
- 正股基本面分析
- 行业对比

### 3. 上市溢价预测
- 基于同行业转债对比
- 基于正股估值分析
- 历史数据回测准确率

### 4. 中签率查询
- 历史中签率统计
- 申购户数分析
- 单账户中签概率

### 5. 强赎/下修提醒
- 强赎条件监控
- 下修公告推送
- 回售条款提示

### 6. 已上市转债追踪
- 实时价格
- 转股溢价率
- 到期收益率

---

## 🚀 使用方式

### 快速开始

```bash
# 安装依赖
pip3 install requests pandas beautifulsoup4

# 运行主程序
python3 main.py
```

### 触发词

- "可转债打新"
- "新债申购"
- "转债分析"
- "可转债日历"
- "强赎提醒"

---

## 📁 目录结构

```
convertible-bond-assistant/
├── SKILL.md                      # 技能说明
├── main.py                       # 主入口
├── cb_calendar.py                # 打新日历
├── cb_analysis.py                # 新债分析
├── cb_premium_predict.py         # 溢价预测
├── cb_monitor.py                 # 监控提醒
├── data/
│   └── cb_history.csv            # 历史数据缓存
└── references/
    ├── API.md                    # 数据源说明
    └── USER_GUIDE.md             # 用户指南
```

---

## 📊 功能示例

### 查询今日可申购转债

```python
from cb_calendar import get_today_subscribable

result = get_today_subscribable()
print(result)
```

**输出示例:**
```
今日可申购转债 (2026-03-07):
1. 赛龙转债 (123205)
   - 发行规模：7.5 亿元
   - 评级：AA-
   - 申购上限：100 万
   - 正股：赛龙科技 (300xxx)
   
2. 恒泰转债 (123206)
   - 发行规模：10 亿元
   - 评级：AA
   - 申购上限：100 万
   - 正股：恒泰股份 (600xxx)
```

### 新债分析

```python
from cb_analysis import analyze_new_cb

result = analyze_new_cb("123205")
print(result)
```

**输出示例:**
```
赛龙转债 (123205) 分析:
- 发行规模：7.5 亿（小规模，易炒作）
- 转股价格：15.23 元
- 正股 PE：25 倍（行业中低）
- 行业：汽车零部件
- 评级：AA-
- 预测上市溢价：25-35%
- 建议：积极申购
```

---

## 🔌 数据源

| 数据类型 | 来源 | 更新频率 |
|---------|------|---------|
| 发行公告 | 巨潮资讯 | 实时 |
| 申购日历 | 东方财富 | 每日 |
| 行情数据 | 新浪财经 | 实时 |
| 历史数据 | 集思录 | 每日 |

---

## ⚙️ 配置说明

### 数据缓存配置

编辑 `main.py`:
```python
CACHE_EXPIRE_MINUTES = 30  # 缓存有效期
```

### 提醒配置

编辑 `cb_monitor.py`:
```python
ALERT_THRESHOLD = {
    'premium_rate': 30,  # 溢价率超过 30% 提醒
    'strong_redemption': True,  # 强赎提醒
    'downward_revision': True,  # 下修提醒
}
```

---

## 📝 更新日志

### v1.0.0 (2026-03-07)
- 初始版本发布
- 支持打新日历查询
- 支持新债基础分析
- 支持溢价预测
- 支持强赎/下修监控

---

## 🙏 致谢

- 东方财富网提供公开数据
- 集思录提供社区参考
- OpenClaw 提供自动化平台

---

## 📬 反馈

欢迎提交问题和建议！

**作者**: Your Name  
**邮箱**: your@email.com
