slug: cn-percentage-tool
name: 百分比工具
description: "cn-percentage-tool。纯Python标准库，无需API Key。"
keywords: percentage, tool
version: "1.0.0"
author: 千策

# 百分比工具

纯 Python 标准库实现的百分比计算工具。

## 功能

- **百分比计算**：计算 A 是 B 的百分之多少
- **反向计算**：已知百分比和部分，求整体
- **比例计算**：已知整体和百分比，求部分
- **增减百分比**：计算增长/下降百分比
- **格式化输出**：带千分位分隔符和精度控制

## 使用方式

```bash
# 百分比：A 是 B 的百分之几
python3 cn_percentage_tool.py percent 25 200
# 输出：12.5% （25 占 200 的百分比）

# 反向计算：已知百分比和部分，求整体
python3 cn_percentage_tool.py from-part 50 25
# 输出：200 （50 的 25% 是多少 → 50/0.25 = 200）

# 比例计算：已知整体和百分比，求部分
python3 cn_percentage_tool.py of-part 200 25
# 输出：50 （200 的 25% 是多少）

# 增减百分比：增长了多少
python3 cn_percentage_tool.py change 100 150
# 输出：50.0% （从 100 增长到 150）

# 格式化精度
python3 cn_percentage_tool.py percent 1 3 --precision 4
# 输出：33.3333%
```

## 技术说明

- 纯 Python 标准库（`argparse`）
- 无外部依赖
- 默认精度 2 位小数

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
