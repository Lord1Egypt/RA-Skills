# Examples · 示例

## sample_financials.json
A sanitized example with two red-flag scenarios (AR growth >> revenue growth, OCF/NI < 0.5, Goodwill/Equity > 30%).

```bash
python3 ../scripts/run_pipeline.py --input sample_financials.json --output /tmp/analysis.json
python3 ../scripts/render_report.py --input /tmp/analysis.json --format md
```
