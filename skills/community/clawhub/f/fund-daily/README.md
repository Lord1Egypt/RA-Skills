# 基金日报 Skill 使用文档

## 📋 简介

这个 Skill 会自动生成基金日报，包含：
- 基金净值数据
- 估值涨跌
- 财经新闻
- Word 详细报告

## 🚀 快速开始

### 1. 安装依赖

```bash
cd skills/fund-daily
pip install -r requirements.txt
```

### 2. 配置基金代码

编辑 `fund_daily.py`，找到这一行：

```python
FUND_CODES = ['001407', '017091', '050025']
```

改成你的基金代码。

### 3. 配置 Telegram（可选）

如果想通过 Telegram 接收日报，编辑 `fund_daily.py`：

```python
TELEGRAM_BOT_TOKEN = "你的 Bot Token"
TELEGRAM_CHAT_ID = "你的 Chat ID"
```

### 4. 运行

**手动运行：**
```bash
python fund_daily.py
```

**自动运行（Windows）：**
```bash
schtasks /Create /TN "基金日报" /TR "python C:\完整路径\fund_daily.py" /SC DAILY /ST 16:00 /F
```

**自动运行（Linux/Mac）：**
```bash
crontab -e
# 添加：0 16 * * * python /完整路径/fund_daily.py
```

## 📊 输出内容

### Telegram 消息
- 基金代码
- 单位净值
- 估值涨跌
- 数据日期
- 财经新闻（5 条）

### Word 文档
- 基金数据表格
- 走势分析
- 财经新闻（10 条）
- 总结点评

## ⏰ 运行时间

**默认：** 每天下午 4:00

**原因：**
- 国内股市 3:00 收盘
- 4:00 已有较准确的估值数据
- 晚上 8:00 后会自动获取实际净值

## 📁 文件保存位置

**Word 文档：**
```
D:\System\Desktop\基金日报\YYYYMMDD_MM 月 DD 日基金日报\基金日报_YYYYMMDD.docx
```

## 🔧 自定义配置

### 修改运行时间

**Windows：**
```bash
schtasks /Change /TN "基金日报" /ST 17:00
```

**Linux：**
编辑 crontab，修改时间。

### 添加更多基金

在 `FUND_CODES` 列表中添加：
```python
FUND_CODES = ['001407', '017091', '050025', '你的基金代码']
```

### 修改新闻数量

编辑 `get_finance_news` 调用：
```python
news_list = get_finance_news(limit=20)  # 改成 20 条
```

## ❓ 常见问题

### Q: 数据不准确怎么办？

A: 
1. 检查网络连接
2. QDII 基金净值会延迟 1-2 天
3. 以天天基金 App 为准

### Q: 收不到 Telegram 消息？

A:
1. 检查 Bot Token 是否正确
2. 确认 Chat ID 正确
3. 在 Telegram 中给 Bot 发送过消息

### Q: Word 文档打不开？

A:
1. 检查是否安装了 Microsoft Word
2. 确认保存路径存在
3. 检查文件是否被占用

## 📞 技术支持

如有问题，请查看：
- SKILL.md - 技能说明
- 天天基金网 - 数据源

---

**祝你投资顺利！** 📈💰
