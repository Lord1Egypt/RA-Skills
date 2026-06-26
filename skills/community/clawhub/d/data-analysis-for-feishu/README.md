---
name: data-analysis-for-feishu
description: "📊 Powerful ECharts-based data visualization skill optimized for Feishu (Lark) ecosystem. Supports 12+ chart types, 6+ data sources (Excel/CSV/Bitable/Sheet/Markdown), auto chart recommendation, auto analysis reports, generates high-definition PNG charts perfectly displayed in Feishu. No configuration required, works out of the box."
---

<div align="center">
  <h1>📊 Data Analysis for Feishu</h1>
  <p>
    <strong>Open-source data visualization skill for OpenClaw, built for Feishu ecosystem</strong>
  </p>
  <p>
    <a href="https://github.com/openclaw/skills"><img src="https://img.shields.io/badge/OpenClaw-Skill-blue.svg" alt="OpenClaw Skill"></a>
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License MIT"></a>
    <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/Python-3.8+-yellow.svg" alt="Python 3.8+"></a>
    <img src="https://img.shields.io/badge/Feishu-5.15+-brightgreen.svg" alt="Feishu 5.15+">
  </p>
  <p>
    <a href="#features">✨ Features</a> •
    <a href="#installation">🚀 Installation</a> •
    <a href="#quick-start">⚡ Quick Start</a> •
    <a href="#chart-types">📊 Chart Types</a> •
    <a href="#data-sources">📥 Data Sources</a> •
    <a href="#examples">📖 Examples</a> •
    <a href="#faq">❓ FAQ</a> •
    <a href="#contributing">🤝 Contributing</a>
  </p>
</div>

---

## ✨ Features
### 📊 Rich Chart Support
12+ professional chart types cover 99% of data visualization scenarios:
- **Basic**: Line, Area, Bar, Stacked Bar, Pie, Donut, Gauge, Radar
- **Advanced**: Scatter (correlation analysis), Funnel (conversion analysis), Waterfall (financial analysis), Dual Axis (multi-metric comparison)
- **Multi-series**: All charts support multiple data series comparison
- **Customizable**: Support stacked mode, area fill, custom colors, etc.

### 🧠 AI-Powered Intelligence
- **Auto Chart Recommendation**: Upload data, AI automatically analyzes characteristics and selects the optimal chart type
- **Auto Data Cleaning**: Automatically handle null values, outliers, date/percent format conversion
- **Auto Analysis Report**: Generate natural language analysis conclusions while generating charts (trends, extremes, proportions, etc.)
- **Auto Title Generation**: No need to manually enter titles, automatically generate appropriate titles based on data

### 📥 Multiple Data Sources
No manual data conversion required, support 6+ common data sources:
- Local files: Excel (.xlsx/.xls), CSV/TSV
- Feishu ecosystem: Bitable (multi-dimensional table), Sheet (spreadsheet)
- Text formats: Markdown tables, raw JSON/2D arrays, pasted table text

### 🖼️ Perfect Feishu Compatibility
- **Ultra HD Output**: 2x Retina DPI rendering, 1200x750 default resolution, sharp text and lines
- **Precise Cropping**: Automatically capture only the chart area, no extra whitespace
- **Feishu Optimized**: Perfect display in Feishu conversations, documents, and wiki pages
- **Dual Mode Support**: 
  - ✅ Screenshot mode: 100% compatible with all Feishu versions, no permissions required
  - ✅ Interactive card mode: Support hover to view values, toggle series (requires Feishu ECharts component permission)

### ⚡ Excellent Experience
- **Zero Configuration**: Works out of the box, dependencies automatically installed on first run
- **Fast Generation**: First run ~10s (download browser), subsequent generation only takes 1-3 seconds
- **User-friendly**: Clear error prompts, perfect log output, easy to troubleshoot
- **Exportable**: Support export analysis conclusions as separate text files, easy to copy and use

---

## 🚀 Installation
### Prerequisites
- OpenClaw instance (version >= 0.8.0)
- Python 3.8+
- Feishu integration enabled (optional, for Feishu data sources)

### Install Steps
1. **Download the skill package**:
   ```bash
   wget https://github.com/openclaw/skills/releases/download/data-analysis-for-feishu-v1.0.0/data-analysis-for-feishu.skill
   ```
   
2. **Install in OpenClaw**:
   Go to OpenClaw Admin → Skills → Install → Upload the `.skill` file

3. **Done!** Dependencies are automatically installed on first use.

### Manual Installation (for developers)
```bash
cd /path/to/openclaw/skills
git clone https://github.com/openclaw/data-analysis-for-feishu.git
cd data-analysis-for-feishu
pip install -r requirements.txt
```

---

## ⚡ Quick Start
### 1-Minute Test Run
Generate your first chart in 1 minute:
```bash
# Go to skill directory
cd skills/data-analysis-for-feishu

# Generate a demo funnel chart
python scripts/main.py \
  --type funnel \
  --title "User Conversion Funnel" \
  --labels "Visit" "Register" "Add to Cart" "Purchase" "Repurchase" \
  --values 10000 4500 2200 1200 500 \
  --output demo_funnel.png
```
You will get a high-definition funnel chart and automatic analysis report.

### Auto Mode (Recommended)
Let AI do all the work, just provide data:
```bash
# Auto analyze Excel data, recommend chart type, generate chart + analysis
python scripts/main.py \
  --excel your_data.xlsx \
  --output result.png \
  --analysis-output analysis.txt
```

---

## 📊 Chart Types
| Chart Type | Best For | Example |
|------------|----------|---------|
| Line Chart | Time series trend analysis | Daily sales trends for the past month |
| Area Chart | Multi-series trend comparison | 2023 vs 2024 monthly sales comparison |
| Bar Chart | Category comparison/ranking | Sales ranking by region |
| Stacked Bar Chart | Multi-dimensional proportion | Product category composition in each region |
| Pie Chart | Proportion/distribution | Revenue composition of each business line |
| Donut Chart | Ring-style proportion | Market share of each competitor |
| Gauge Chart | Progress/KPI completion | Annual sales target completion rate |
| Radar Chart | Multi-dimensional comparison | Product capability assessment |
| Scatter Chart | Correlation analysis | Correlation between advertising spend and sales |
| Funnel Chart | Conversion analysis | User conversion from visit to purchase |
| Waterfall Chart | Financial change analysis | Monthly profit and loss changes |
| Dual Axis Chart | Multi-metric comparison | Monthly sales and growth rate |

---

## 📥 Data Sources
| Data Source | Usage |
|-------------|-------|
| Excel (.xlsx/.xls) | `--excel data.xlsx --sheet Sheet1` |
| CSV/TSV | `--csv data.csv` |
| Feishu Bitable | `--bitable-records '[{"fields": {...}}]'` |
| Feishu Sheet | `--sheet-data '[["Header1", "Header2"], ["val1", "val2"]]'` |
| Markdown Table | `--markdown-table "| Col1 | Col2 |\n|---|---|\n| a | 1 |"` |
| Raw Data | `--x-axis "Jan" "Feb" --y-axis 100 200` |

---

## 📖 Usage Examples
### Example 1: Multi-series Area Chart
```bash
python scripts/main.py \
  --type area \
  --title "2023 vs 2024 Sales Trend" \
  --excel sales_comparison.xlsx \
  --x-axis-field "Month" \
  --y-axis-field "2023 Sales,2024 Sales" \
  --series-names "2023,2024" \
  --output sales_trend.png
```

### Example 2: Dual Axis Chart (Sales + Growth Rate)
```bash
python scripts/main.py \
  --type dual_axis \
  --title "Monthly Performance" \
  --x-axis "Jan" "Feb" "Mar" "Apr" "May" "Jun" \
  --y1-axis 120 150 135 180 210 240 \
  --y1-name "Sales (k)" \
  --y2-axis 0 25 -10 33.3 16.7 14.3 \
  --y2-name "Growth Rate (%)" \
  --output performance.png
```

### Example 3: Waterfall Chart for Financial Analysis
```bash
python scripts/main.py \
  --type waterfall \
  --title "Monthly Profit Breakdown" \
  --x-axis "Initial Revenue" "Cost of Goods" "Operating Expenses" "Tax" "Net Profit" \
  --y-axis 1000 -300 -200 -150 350 \
  --y-name "Amount (k)" \
  --output profit_waterfall.png
```

### Example 4: Generate from Markdown Table
```bash
python scripts/main.py \
  --type bar \
  --title "Quarterly Revenue" \
  --markdown-table "| Quarter | Revenue | Profit |
|----|----|----|
| Q1 | 1200 | 240 |
| Q2 | 1500 | 375 |
| Q3 | 1350 | 297 |
| Q4 | 1800 | 540 |" \
  --x-axis-field "Quarter" \
  --y-axis-field "Revenue,Profit" \
  --output quarterly.png
```

---

## 🔧 Configuration
### Custom Color Scheme
Edit `DEFAULT_COLORS` in `scripts/generate_echarts_screenshot.py` to use your brand colors:
```python
DEFAULT_COLORS = ["#YOUR_COLOR1", "#YOUR_COLOR2", ...]
```

### Custom Default Resolution
Change default `width`/`height` in `scripts/main.py` to adjust output size.

### Enable Interactive Card Mode
When you have Feishu ECharts component permission, use:
```bash
python scripts/generate_echarts_card.py --type line --title "Demo" --x-axis "A" "B" --y-axis 1 2 --output card.json
```
Then send the JSON as Feishu card.

---

## ❓ FAQ
### Q: Why is the picture blank when I first run it?
A: First run automatically downloads Chromium browser (about 180MB), please wait patiently. Subsequent runs will be very fast.

### Q: Can I use this without Feishu?
A: Yes! You can generate charts as local PNG files for any usage scenario, Feishu integration is optional.

### Q: How to apply for Feishu ECharts component permission?
A: Go to Feishu Open Platform → Your App → Permissions → Search for "Message Card - Use ECharts Chart Component" → Apply for permission. It's free and usually approved within 1 working day.

### Q: Does it support Chinese data?
A: Perfect support! All components use UTF-8 encoding, Chinese labels, titles, and analysis reports are displayed normally.

### Q: Can I add custom chart types?
A: Yes! Just add the chart configuration in `scripts/generate_echarts_screenshot.py`, following the existing pattern.

---

## 🤝 Contributing
Contributions are welcome! You can contribute in the following ways:
- 🐛 Report bugs and issues
- ✨ Propose new feature ideas
- 📝 Improve documentation
- 🔧 Add new chart types or data sources
- 🌐 Add multi-language support

### Development Setup
```bash
# Fork and clone the repo
git clone https://github.com/your-username/data-analysis-for-feishu.git
cd data-analysis-for-feishu

# Install dependencies
pip install -r requirements.txt

# Run tests
python scripts/main.py --type funnel --title "Test" --labels "A" "B" "C" --values 100 50 20 --output test.png
```

### Submitting PR
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License
Distributed under the MIT License. See `LICENSE` file for more information.

---

## 🙏 Acknowledgments
- [ECharts](https://echarts.apache.org/) - Powerful open-source chart library
- [Pyppeteer](https://pyppeteer.github.io/pyppeteer/) - Headless browser for Python
- [OpenClaw](https://openclaw.ai/) - Extensible AI agent platform
- [Feishu Open Platform](https://open.feishu.cn/) - Feishu API and documentation

---

<div align="center">
  <strong>If this skill helps you, please give it a ⭐ on GitHub!</strong>
  <br>
  <a href="https://github.com/openclaw/data-analysis-for-feishu/stargazers"><img src="https://img.shields.io/github/stars/openclaw/data-analysis-for-feishu.svg?style=social" alt="GitHub stars"></a>
</div>
