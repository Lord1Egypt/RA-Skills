---
name: data-chart-tool
description: 【爆款标题】数据不会说话？3步生成专业图表，让你的报告瞬间提升档次！

你是不是经常拿到一堆 CSV 数据，却不知道怎么呈现？财务报告、销售分析、市场调研...数据还在用 Excel 基础图表，low 爆了？

本工具用 3 步（加载数据 → 选择图表 → 导出），将你的 CSV/JSON 秒变专业级可视化图表（柱状/折线/饼图等），支持批量处理和多种输出格式。

✨ **核心亮点**：
- 一键生成：CSV/JSON/Excel → 图表（支持5种类型）
- 专业样式：标题、标签、颜色、字体全可调
- 多格式输出：PNG/JPEG/PDF/SVG，满足各种场景
- 批量处理：一次N个文件，自动批量生成
- 特别优化：无缝对接 tushare-finance，股票数据秒出图

📁 **典型场景**：
- 财务分析：月度/季度财报可视化
- 销售报告：KPI趋势、产品对比
- 学术研究：数据展示，论文配图
- 个人项目：数据分析爱好者

🎯 **为什么选我**：
✅ 唯一支持 tushare-finance 深度集成
✅ 批量处理 + 预览模式 = 高效工作流
✅ Python 原生，可编程扩展

👉 立即体验：`clawhub install data-chart-tool`

---

## 💎 付费功能（一次性购买，永久使用）

### 免费版功能
- ✅ 柱状图（bar）、折线图（line）、饼图（pie）、面积图（area）
- ✅ 基础自定义（标题、标签、颜色）
- ✅ 批量处理
- ✅ PNG/JPEG/PDF/SVG 输出
- ✅ 预设样式（seaborn、ggplot 等）

### 专业版功能（¥99 一次性付费）
- ✅ **散点图**（scatter）—— 唯一付费图表类型
- ✅ 无限制批量导出（无文件数量限制）
- ✅ 优先技术支持
- ✅ 未来所有新图表类型免费解锁

**购买流程**：
1. **扫码支付**（微信/支付宝）：
   ![收款码预留位置]
2. **发送付款凭证**：通过 OpenClaw 或 GitHub 联系我
3. **接收许可证**：我会发送 `license.json` 文件
4. **安装许可证**：
   ```bash
   # 复制到本地
   cp license.json ~/.data-chart-tool/license.json
   # 设置环境变量（密钥会随许可证发送）
   export SKILL_LICENSE_SECRET="your-secret-key"
   ```
5. **使用付费功能**：
   ```bash
   # 散点图（付费功能）
   python source/data_visualizer.py -i data.csv -t scatter --x-col x --y-col y --license ~/.data-chart-tool/license.json
   ```

**注意**：
- 许可证有效期：**永久**（一次性购买）
- 支持多设备：同一许可证可在个人多台机器上使用
- 不包含：企业批量授权（需要另外洽谈）

---

## 🎯 为什么选择付费版？

散点图是数据分析中**最常用**的高级图表之一，用于：
- 相关性分析（两个变量的关系）
- 聚类观察
- 异常值检测

免费版已满足 80% 日常需求，付费版解锁专业分析能力。

---

## 📦 版本历史

- **v1.1.0-premium**（2026-03-22）：新增付费模式和散点图功能，许可证系统
- **v1.0.1**（2026-03-20）：营销优化版
- **v1.0.0**（2026-03-15）：初始版本

---

# data-chart-tool - 数据可视化工具

数据可视化工具，将 CSV/JSON 数据生成美观图表，支持多种图表类型和输出格式！

## 功能特性

- ✅ **读取多种数据格式**：CSV、JSON、Excel
- ✅ **多种图表类型**：柱状图、折线图、饼图、散点图、面积图
- ✅ **自定义样式**：标题、标签、颜色、字体、图例
- ✅ **多种输出格式**：PNG、JPEG、PDF、SVG
- ✅ **预览模式**：显示图表而不保存文件
- ✅ **批量处理**：支持处理多个数据文件
- ✅ **配合 tushare-finance**：直接可视化股票数据

## 安装

```bash
# 安装依赖
pip install matplotlib pandas openpyxl
```

## 使用方法

### 基本用法

```bash
# 从 CSV 文件生成折线图
python source/data_visualizer.py --input data.csv --type line

# 从 JSON 文件生成柱状图
python source/data_visualizer.py --input data.json --type bar

# 生成饼图
python source/data_visualizer.py --input data.csv --type pie

# 预览模式（显示图表）
python source/data_visualizer.py --input data.csv --type line --preview

# 保存为 PDF
python source/data_visualizer.py --input data.csv --type line --output chart.pdf
```

### 详细参数

```
--input INPUT, -i INPUT     输入数据文件（CSV/JSON/Excel）
--type TYPE, -t TYPE        图表类型：bar（柱状图）、line（折线图）、pie（饼图）、scatter（散点图）、area（面积图）
--output OUTPUT, -o OUTPUT  输出文件路径（默认：chart.png）
--title TITLE                图表标题
--x-label X_LABEL            X 轴标签
--y-label Y_LABEL            Y 轴标签
--x-col X_COL                X 轴数据列名
--y-col Y_COL                Y 轴数据列名（逗号分隔多列）
--color COLOR                颜色（十六进制或颜色名）
--figsize FIGSIZE            图表大小，格式：宽,高（默认：10,6）
--dpi DPI                    输出 DPI（默认：100）
--grid, -g                   显示网格线
--legend, -l                 显示图例
--preview, -p                预览模式，显示图表不保存
--style STYLE                图表样式：default、seaborn、ggplot、fivethirtyeight
```

### 示例

```bash
# 股票数据可视化（配合 tushare-finance）
python source/data_visualizer.py -i stock_data.csv -t line --title "股票走势" --x-col "date" --y-col "close"

# 多列数据对比
python source/data_visualizer.py -i sales.csv -t bar --title "月度销售额" --x-col "month" --y-col "sales,profit" --legend

# 饼图展示占比
python source/data_visualizer.py -i category.csv -t pie --title "分类占比" --x-col "category" --y-col "value"

# 使用 seaborn 样式
python source/data_visualizer.py -i data.csv -t line --style seaborn --grid

# 保存为高分辨率 PDF
python source/data_visualizer.py -i data.csv -t bar --output report.pdf --dpi 300
```

## 支持的数据格式

- **CSV**：逗号分隔值文件
- **JSON**：JSON 格式数据（数组或对象）
- **Excel**：.xlsx 和 .xls 格式

## 图表样式

- `default`：默认样式
- `seaborn`：Seaborn 风格
- `ggplot`：ggplot 风格
- `fivethirtyeight`：FiveThirtyEight 风格

## 配合 tushare-finance 使用

```bash
# 1. 先用 tushare-finance 获取数据
tushare stock_daily --ts_code 000001.SZ --start_date 20240101 --end_date 20241231 -o stock_data.csv

# 2. 再用 data-visualizer 可视化
python source/data_visualizer.py -i stock_data.csv -t line --title "平安银行股价走势" --x-col "trade_date" --y-col "close" --grid
```
