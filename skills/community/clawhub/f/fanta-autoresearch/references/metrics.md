# Common Metrics for Autoresearch

Reference guide for defining and measuring metrics in iteration loops.

## Metric Types

### Accuracy Metrics

| Metric | Description | Measure Command |
|--------|-------------|-----------------|
| Hit Rate | % of queries returning relevant results | Benchmark script |
| Precision | % of returned results that are relevant | Evaluation script |
| Recall | % of relevant items that are returned | Evaluation script |
| F1 Score | Harmonic mean of precision and recall | Calculation |

### Performance Metrics

| Metric | Description | Measure Command |
|--------|-------------|-----------------|
| Latency | Time to complete operation | `time <command>` |
| Throughput | Operations per second | Benchmark script |
| P50/P95/P99 | Percentile latencies | Benchmark script |
| Memory Usage | Peak memory consumption | `/usr/bin/time -v` |

### Quality Metrics

| Metric | Description | Measure Command |
|--------|-------------|-----------------|
| Test Coverage | % of code covered by tests | `pytest --cov`, `npm test -- --coverage` |
| Lint Score | Code quality issues | `eslint .`, `ruff check .` |
| Type Errors | TypeScript/mypy errors | `tsc --noEmit`, `mypy .` |
| Bundle Size | Build output size | `du -b dist/` |

### Count Metrics

| Metric | Description | Measure Command |
|--------|-------------|-----------------|
| Test Failures | Number of failing tests | `npm test 2>&1 \| grep -c "FAIL"` |
| Errors | Count of errors in output | `grep -c "Error"` |
| Warnings | Count of warnings | `grep -c "Warning"` |
| TODOs | Unfinished items | `grep -c "TODO"` |

## Domain-Specific Metrics

### Memory Search

```bash
# Top-1 Hit Rate
openclaw cron runs --id <job-id> --limit 1 | jq -r '.entries[0].summary' | grep "Top1 Hit Rate" | grep -oP '\d+(?=%)'

# Top-3 Hit Rate
openclaw cron runs --id <job-id> --limit 1 | jq -r '.entries[0].summary' | grep "Top3 Hit Rate" | grep -oP '\d+(?=%)'
```

### Web Performance

```bash
# Lighthouse score
npx lighthouse <url> --output=json | jq '.categories.performance.score'

# Bundle size
npm run build && du -b dist/*.js | awk '{sum+=$1} END {print sum}'
```

### Database

```bash
# Query time
psql -c "EXPLAIN ANALYZE <query>" | grep "Execution Time"

# Index size
psql -c "SELECT pg_size_pretty(pg_indexes_size('<table>'))"
```

### API

```bash
# Response time
curl -w "%{time_total}" -o /dev/null -s <endpoint>

# Error rate
curl -s <endpoint>/metrics | grep "error_rate"
```

## Metric Extraction Patterns

### From JSON Output

```bash
# Extract nested value
cat result.json | jq '.metrics.accuracy'

# Extract from array
cat result.json | jq '.results | map(select(.pass)) | length'

# Calculate percentage
cat result.json | jq '(.passed / .total) * 100'
```

### From Text Output

```bash
# Extract number from line
grep "accuracy:" | grep -oP '[\d.]+'

# Count occurrences
grep -c "PASS"

# Extract after pattern
sed -n 's/Score: \([0-9.]*\)/\1/p'
```

### From Benchmark Output

```bash
# Extract from benchmark table
./benchmark | grep "Total:" | awk '{print $2}'

# Parse CSV output
./benchmark --format csv | tail -1 | cut -d',' -f3
```

## Baseline Establishment

Before starting iteration loop, always establish baseline:

```markdown
## Baseline Measurement

Date: [timestamp]
Metric: [name]
Value: [number]
Method: [command used]

Environment:
- [relevant config]
- [model/version]
- [hardware]
```

## Improvement Threshold

Define minimum improvement to consider a change "better":

```markdown
## Thresholds

- Minimum improvement: +1% (avoid noise)
- Significant improvement: +5%
- Breakthrough: +10%
- Regression tolerance: -0.5%
```

## Metric Comparison

When comparing metrics:

```markdown
## Comparison Template

| Metric | Before | After | Δ | Status |
|--------|--------|-------|---|--------|
| Top-1 | 65% | 70% | +5% | ✅ improved |
| Top-3 | 70% | 72% | +2% | ✅ improved |
| Latency | 150ms | 180ms | +30ms | ⚠️ regression |

Decision: KEEP (net positive)
```

## Multi-Metric Scoring

When optimizing multiple metrics:

```markdown
## Weighted Score

score = w1 * metric1 + w2 * metric2 + w3 * metric3

Example:
- Top-1: 70% (weight: 0.5)
- Top-3: 72% (weight: 0.3)  
- Latency: 180ms (weight: -0.2, lower is better)

score = 0.5 * 70 + 0.3 * 72 - 0.2 * (180/10) = 35 + 21.6 - 3.6 = 53
```

## Common Benchmarks

### OpenClaw Memory Search

```bash
# Trigger benchmark
openclaw cron run <job-id>

# Wait for completion
sleep 90

# Get results
openclaw cron runs --id <job-id> --limit 1 | jq -r '.entries[0].summary'
```

### Node.js Projects

```bash
# Test suite
npm test 2>&1 | tee test-output.txt
grep -E "passed|failed" test-output.txt

# Coverage
npm test -- --coverage --coverageReporters=text | grep "All files"

# Bundle size
npm run build && ls -la dist/
```

### Python Projects

```bash
# Test suite
pytest -v 2>&1 | tee test-output.txt
grep -E "passed|failed|error" test-output.txt

# Coverage
pytest --cov --cov-report=term | grep "TOTAL"

# Type check
mypy . 2>&1 | grep -c "error"
```