# Examples · 示例

```bash
python3 ../scripts/run_pipeline.py \
  --input sample_homework.json --answer-key sample_key.json --output /tmp/graded.json
python3 ../scripts/render_report.py --grading-result /tmp/graded.json --format student
```

Expected: total 15/15, all items correct.
