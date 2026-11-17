---
name: chinamoney-cd
version: 1.0.1
description: 查询中国货币网同业存单发行信息，支持全市场所有银行机构，精准匹配，一键获取待发行存单列表
author: Avalon
homepage: https://github.com/avalon/chinamoney-cd
keywords:
  - 同业存单
  - 存单查询
  - 银行存单
  - 中国货币网
  - chinamoney
  - certificate of deposit
  - interbank CD
requires:
  python: ">=3.8"
  packages:
    - playwright>=1.40.0
  binaries:
    - python3
    - chromium
env: []
---

# Chinamoney CD Query

查询中国货币网(chinamoney.com.cn)同业存单发行信息，支持全市场所有银行机构。

## 功能特点

- 🔍 **全市场覆盖** - 支持查询所有银行机构的同业存单（国有大行、股份制、城商行、农商行、外资行、政策性银行）
- 🎯 **智能精准匹配** - 输入"中国"只匹配"中国银行"
- 📊 **结构化输出** - 存单代码、发行日期、期限、发行方式、计划发行量(亿元)、参考收益率(%)、主体评级一目了然
- 📸 **自动截图保存** - 查询结果自动截图
- 🪟 **跨平台兼容** - v1.0.1 起截图路径改用 `tempfile.gettempdir()`，Windows / Linux / macOS 均可直接运行

## 支持的银行类型

**国有大行**: 工商、农业、中国、建设、交通、邮储
**股份制**: 招商、民生、光大、中信、兴业、浦发、平安、华夏等
**城商行**: 北京、上海、江苏、南京、杭州、宁波、苏州等
**农商行**: 重庆农商、上海农商、北京农商等
**外资行**: 汇丰、渣打、花旗、东亚等
**政策性银行**: 国开行、进出口行、农发行

> 💡 理论上支持查询中国货币网收录的**所有银行机构**同业存单。

## 安装

```bash
pip install playwright
playwright install chromium
openclaw skill install chinamoney-cd
```

## 使用方法

### 命令行
```bash
python3 scripts/query_cd.py 民生
python3 scripts/query_cd.py 建设
python3 scripts/query_cd.py 工商
```

### 对话中
```
用户：查一下民生银行的同业存单
→ 返回查询结果和截图
```

## 输出示例

```
中国民生银行同业存单发行计划:

找到 1 条记录:

[1] 26民生银行CD080
    代码: 112615080
    发行日期: 2026/03/30
    发行方式: 报价发行
    期限: 9月
    计划发行量(亿元): 0.5
    参考收益率(%): 1.5100
    主体评级: AAA
```

## 数据来源

- **中国货币网**: https://www.chinamoney.com.cn/chinese/tycdfxxx/
- **数据类型**: 同业存单待发行信息
- **更新频率**: 实时

## 更新日志

- **v1.0.1** (2026-09-09): 截图路径兼容 Windows（`/tmp` → `tempfile.gettempdir()`），并过滤文件名非法字符
- **v1.0.0** (2026-03): 初始版本

## 许可证

MIT License
