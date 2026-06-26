#!/bin/bash
# Bottleneck Analysis Template Spawn Prompt
# Use for: Cross-domain performance investigation

cat << 'SPAWNPROMPT'
I need to investigate a performance bottleneck across multiple systems: ${TASK_DESCRIPTION}

Target: ${TARGET_DIR}

Spawn 4 domain specialists using Sonnet (tactical investigation):

1. **Database Analyst**
   - Name: db-analyst
   - Focus: Database layer performance
   - Output: database-analysis.md
   - Investigation tasks:
     * Check slow query log
     * Analyze connection pool utilization
     * Review query execution plans
     * Check for missing indexes
     * Identify lock contention or deadlocks
     * Test query performance in isolation

2. **Network Analyst**
   - Name: network-analyst
   - Focus: Network layer performance
   - Output: network-analysis.md
   - Investigation tasks:
     * Measure API endpoint latency
     * Check for packet loss or retransmissions
     * Analyze CDN performance
     * Review network metrics
     * Test connectivity from different regions
     * Identify throttling or rate limiting

3. **Application Analyst**
   - Name: app-analyst
   - Focus: Application layer performance
   - Output: application-analysis.md
   - Investigation tasks:
     * Profile CPU/memory usage
     * Analyze APM traces
     * Review recent code changes
     * Check for N+1 queries or inefficient loops
     * Identify synchronous blocking operations
     * Test with features disabled to isolate

4. **Frontend Analyst**
   - Name: frontend-analyst
   - Focus: Frontend performance
   - Output: frontend-analysis.md
   - Investigation tasks:
     * Measure render performance and bundle size
     * Analyze API call patterns and timing
     * Check for memory leaks in browser
     * Review JavaScript execution time
     * Identify layout thrashing or reflows
     * Test with different browsers/devices

Coordination rules:
- Use delegate mode: I coordinate, analysts investigate
- Each analyst works independently on their domain
- Report findings with confidence levels and evidence
- Identify correlations across domains (e.g., slow DB → slow API → slow frontend)
- Wait for all analysts to complete before synthesis

After all teammates finish:
1. Review all analysis reports
2. Identify cross-domain correlations
3. Synthesize into synthesis-report.md with:
   - Most likely bottlenecks (ranked by impact)
   - Evidence supporting each finding
   - Cross-domain dependencies
4. Create remediation-plan.md with:
   - Prioritized actions (immediate vs. follow-up)
   - Expected impact of each fix
   - Estimated effort
5. Report completion with diagnosis and plan
SPAWNPROMPT
