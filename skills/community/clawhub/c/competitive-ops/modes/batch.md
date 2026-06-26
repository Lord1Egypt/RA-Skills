# Mode: batch -- Batch Processing

Process multiple competitors in parallel.

## Usage

```
/comp batch <company1> <company2> ... <companyN>
/comp batch --file <csv-path>
```

## Input Formats

### Command Line
```
/comp batch Anthropic OpenAI Google Microsoft
```

### CSV File
```csv
company,priority,notes
Anthropic,HIGH,Direct competitor
OpenAI,HIGH,Direct competitor
Google,MEDIUM,Potential threat
```

## Architecture

```
competitive-ops batch
  │
  ├─ Company 1: claude -p worker → analyze + report
  │    └─► data/profiles/{slug}/
  │    └─► reports/{num}-{slug}-{date}.md
  │
  ├─ Company 2: claude -p worker → analyze + report
  │    └─► data/profiles/{slug}/
  │    └─► reports/{num}-{slug}-{date}.md
  │
  └─ Merge: consolidated report + tracker update
```

## Process

### 1. Input Parsing
- Parse company names from command line
- Or read CSV file
- Normalize company names

### 2. State Management
- Check `data/competitors.md` for existing entries
- Determine new vs existing companies
- Skip completed if already analyzed (with --force to override)

### 3. Parallel Workers
- [ ] **TODO: Worker Implementation**
  ```javascript
  for (const company of companies) {
    await Promise.all(
      companies.map(company =>
        claudeWorker({ mode: 'analyze', company })
      )
    )
  }
  ```

### 4. Individual Processing
Each worker:
1. Run `analyze` mode for company
2. Generate report
3. Save to `reports/`
4. Update `data/profiles/`
5. Return result summary

### 5. Consolidation
After all workers complete:
- Merge results into `reports/batch-{date}.md`
- Update `data/competitors.md`
- Generate summary statistics

## Batch Report Format

```markdown
# Batch Analysis: [Date]

**Companies:** N
**Completed:** X
**Failed:** Y

## Summary

| Company | Score | Archetype | Status |
|---------|-------|-----------|--------|
| [Company 1] | X.X | [Type] | ✓ |
| [Company 2] | X.X | [Type] | ✓ |
| [Company 3] | - | - | ✗ |

## Top Threats

1. **[Company]** (Score: X.X) - [Why]
2. **[Company]** (Score: X.X) - [Why]

## Feature Gaps

| Feature | Companies with it | Companies without |
|---------|-----------------|-------------------|
| [Feature] | X | X |

## Consolidated Scores

| Dimension | Avg Score | Range |
|-----------|-----------|-------|
| Product Maturity | X.X | X.X - X.X |
| ... | ... | ... |

## Failed Analyses

- **[Company]:** [Error reason]

## Next Steps

- [ ] Run full analysis: `/comp analyze [Company]`
- [ ] Update all: `/comp update all`
```

## Options

| Option | Description |
|--------|-------------|
| `--force` | Re-analyze even if recent analysis exists |
| `--parallel N` | Run N workers in parallel (default: 3) |
| `--priority` | Process high priority first |
| `--dry-run` | List companies without processing |
| `--report-type` | Type of report: full/brief/summary |

## State File

```csv
id,company,status,started_at,completed_at,report_num,score,error,retries
1,anthropic,completed,2026-...,2026-...,001,4.2,-,0
2,openai,failed,2026-...,2026-...,-,-,Error msg,1
3,google,pending,-,-,-,-,-,0
```

## Error Handling

| Error | Recovery |
|-------|----------|
| Network error | Retry up to 3 times |
| Company not found | Mark failed, continue |
| Rate limit | Pause, then retry |
| Worker crash | Mark failed, continue |

## Output Files

- Individual reports: `reports/{###}-{company}-{date}.md`
- Batch summary: `reports/batch-{date}.md`
- State: `data/batch-state.csv`

## Example

```
/comp batch Anthropic OpenAI Google
/comp batch --file competitors.csv
/comp batch Anthropic OpenAI --parallel 5 --force
```

## TODO Checklist

- [ ] Implement batch runner script
- [ ] Add worker pool management
- [ ] Implement state file persistence
- [ ] Add progress reporting
- [ ] Add error recovery
- [ ] Implement rate limiting
