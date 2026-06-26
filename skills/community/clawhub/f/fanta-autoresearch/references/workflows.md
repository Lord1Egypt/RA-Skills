# Autoresearch Workflows

Advanced workflow patterns for autonomous iteration loops.

## Workflow 1: Config Optimization

Optimize configuration parameters for best performance.

```markdown
1. BASELINE: Run verification with current config, record metric
2. FOR each parameter to tune:
   a. Try increasing value
   b. Verify, compare, keep/revert
   c. Try decreasing value
   d. Verify, compare, keep/revert
3. Try combinations of best individual values
4. Report optimal configuration
```

**Example:** Memory search config optimization
- Parameters: minScore, chunkSize, overlap
- Metric: Top-1 hit rate
- Scope: openclaw.json memorySearch section

## Workflow 2: Corpus Improvement

Iteratively improve indexed content for better retrieval.

```markdown
1. BASELINE: Run benchmark, identify worst queries
2. FOR each failing query:
   a. Analyze why it fails (corpus gap vs retrieval)
   b. If corpus gap: add/expand content
   c. If retrieval: try different embedding or chunking
   d. Verify improvement
   e. Keep if query now passes
3. Re-run full benchmark
```

**Example:** Memory corpus optimization
- Worst queries: "Git identity", "PR merge strategy"
- Action: Expand entries with context
- Verify: Query now returns correct result

## Workflow 3: Iterative Debugging

Fix issues one at a time until all resolved.

```markdown
1. BASELINE: Count failures (tests, errors, warnings)
2. WHILE failures > 0:
   a. Pick one failure (highest priority/impact)
   b. Analyze root cause
   c. Implement fix
   d. Verify fix (failure gone, no new failures)
   e. Commit or revert
   f. Log result
3. Report final state
```

**Example:** Test suite fixing
- Failures: 5 tests failing
- Each iteration: Fix one test
- Stop: All tests pass

## Workflow 4: A/B Comparison

Compare two approaches and keep the better one.

```markdown
1. BASELINE: Current approach metric
2. IMPLEMENT: Alternative approach (branch/separate)
3. VERIFY: Run both, compare metrics
4. DECISION: Keep better approach, discard other
5. CLEANUP: Remove unused code
```

**Example:** Embedding model comparison
- A: qwen3-embedding (current)
- B: nomic-embed-text (alternative)
- Metric: Benchmark score
- Winner: nomic-embed-text

## Workflow 5: Binary Search Optimization

Find optimal value using binary search.

```markdown
1. DEFINE: Search range [min, max]
2. WHILE range > threshold:
   a. Try midpoint value
   b. Verify metric
   c. If better than current best:
      - Narrow to upper half
   d. Else:
      - Narrow to lower half
3. Report optimal value found
```

**Example:** Finding optimal minScore
- Range: [0.1, 0.5]
- Midpoints: 0.3, 0.2, 0.25, ...
- Stop: Range < 0.05

## Workflow 6: Multi-Objective Optimization

Optimize multiple metrics simultaneously.

```markdown
1. DEFINE: Primary metric + constraints
2. FOR each candidate change:
   a. Measure all metrics
   b. Check constraints satisfied
   c. Score = weighted combination
   d. Keep if score improved AND constraints met
3. Report Pareto-optimal configuration
```

**Example:** Model selection
- Primary: Accuracy
- Constraints: VRAM < 500MB, latency < 100ms
- Score: accuracy - 0.1 * (VRAM / 100MB)

## Workflow 7: Regression Prevention

Ensure changes don't break existing functionality.

```markdown
1. BASELINE: Run full test suite, record all passing
2. FOR each change:
   a. Make change
   b. Run tests
   c. IF any previously-passing test fails:
      - REVERT immediately
      - Log regression
   d. ELSE:
      - Keep change
      - Update baseline
```

**Example:** Config changes with guard
- Guard: npm test
- Change must not break any existing test
- Auto-revert on regression

## Combining Workflows

For complex tasks, combine workflows:

```
1. Workflow 4 (A/B Comparison) to choose embedding model
2. Workflow 1 (Config Optimization) to tune parameters
3. Workflow 2 (Corpus Improvement) to fill gaps
4. Workflow 7 (Regression Prevention) as guard throughout
```

## Workflow Selection Guide

| Task | Recommended Workflow |
|------|---------------------|
| Tune parameters | Workflow 1 |
| Improve content | Workflow 2 |
| Fix failures | Workflow 3 |
| Compare alternatives | Workflow 4 |
| Find optimal value | Workflow 5 |
| Balance tradeoffs | Workflow 6 |
| Safe refactoring | Workflow 7 |