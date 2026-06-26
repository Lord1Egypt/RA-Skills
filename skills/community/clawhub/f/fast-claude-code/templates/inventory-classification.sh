#!/bin/bash
# Inventory Classification Template Spawn Prompt
# Use for: Data-parallel processing of many independent items

cat << 'SPAWNPROMPT'
I need to process many independent items in parallel: ${TASK_DESCRIPTION}

Target: ${TARGET_DIR}

This is a data-parallel task where items have no dependencies. We'll divide items among teammates for linear speedup.

Spawn 3 teammates using Sonnet (tactical processing):

1. **Worker 1**
   - Name: worker-1
   - Focus: Process assigned subset of items
   - Output: worker-1-results.md
   - Tasks:
     * Wait for item assignment from lead
     * Process each item according to the task criteria
     * Document results in specified format
     * Report completion with statistics
     * Flag any items that need manual review

2. **Worker 2**
   - Name: worker-2
   - Focus: Process assigned subset of items
   - Output: worker-2-results.md
   - Tasks:
     * Wait for item assignment from lead
     * Process each item according to the task criteria
     * Document results in specified format
     * Report completion with statistics
     * Flag any items that need manual review

3. **Worker 3**
   - Name: worker-3
   - Focus: Process assigned subset of items
   - Output: worker-3-results.md
   - Tasks:
     * Wait for item assignment from lead
     * Process each item according to the task criteria
     * Document results in specified format
     * Report completion with statistics
     * Flag any items that need manual review

Coordination rules:
- Use delegate mode: I coordinate and divide work, workers process
- First, I'll create items manifest and assign ranges to each worker
- Workers must wait for assignments before starting (avoid duplicate work)
- Each worker processes only their assigned items (no crossover)
- Report progress periodically (every 10-20 items)
- Workers should flag edge cases or items they're unsure about

Workflow:
1. I create manifest and assign items to each worker (e.g., worker-1: items 1-100, worker-2: 101-200, worker-3: 201-300)
2. Signal workers to start processing
3. Workers process items independently and report results
4. After all workers complete, I aggregate results

After all teammates finish:
1. Collect all worker results
2. Aggregate into aggregated-results.md with:
   - Complete item inventory with classifications
   - Statistics by category
   - Items flagged for manual review
3. Create summary-report.md with:
   - Total items processed
   - Distribution across categories
   - Recommendations for follow-up
4. Report completion with summary statistics

Expected speedup: 3 workers ≈ 3x faster than sequential processing
SPAWNPROMPT
