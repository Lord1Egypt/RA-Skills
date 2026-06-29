# Finance Daily Report - HTML Template

This directory contains the HTML template assets for the finance daily report.

The report template is embedded directly in `scripts/generate_report.py` as a Python f-string template.
This keeps the skill self-contained with no external file dependencies at runtime.

## Template Features

- Responsive design (mobile-friendly)
- Chart.js for interactive data visualization
- Chinese market color convention: Red (红) = up, Green (绿) = down
- 6 data modules: indices, sectors, capital flow, forex/commodities, news, calendar
- Graceful degradation: modules with missing data show "暂无数据" placeholder
