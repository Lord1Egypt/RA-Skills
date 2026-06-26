#!/bin/bash
# Competing Hypotheses Template Spawn Prompt
# Use for: Debugging with competing theories

cat << 'SPAWNPROMPT'
I need to debug a complex issue with multiple plausible causes: ${TASK_DESCRIPTION}

Context:
- Project: ${TARGET_DIR}

Spawn 3 investigators using Sonnet (tactical investigation):

1. **Hypothesis A: Database Performance**
   - Name: db-investigator
   - Theory: Slow queries or connection pool exhaustion
   - Output: hypothesis-A-investigation.md
   - Investigation tasks:
     * Check slow query logs (queries >1s)
     * Monitor connection pool utilization
     * Review recent schema changes or missing indexes
     * Check for lock contention or deadlocks
     * Test query performance in isolation

2. **Hypothesis B: Application Logic**
   - Name: app-investigator
   - Theory: Inefficient algorithm or memory leak in new code
   - Output: hypothesis-B-investigation.md
   - Investigation tasks:
     * Profile CPU/memory usage during high latency
     * Review code for O(n²) patterns
     * Check for synchronous external API calls in request path
     * Test algorithm performance with production data volume
     * Look for caching misses or cache invalidation issues

3. **Hypothesis C: Infrastructure/Network**
   - Name: infra-investigator
   - Theory: Network latency or resource limits
   - Output: hypothesis-C-investigation.md
   - Investigation tasks:
     * Check network latency between services
     * Monitor disk I/O and CPU utilization
     * Review resource limits (memory, file descriptors, connections)
     * Check for DNS resolution issues
     * Verify load balancer health and configuration

Coordination rules:
- Use delegate mode: I coordinate, investigators research
- Each investigator works independently (no blocking dependencies)
- Investigators should report:
  * Confidence level (High / Medium / Low)
  * Evidence found (logs, metrics, traces)
  * Recommended next steps
- Wait for all 3 investigators to complete before synthesis

After all teammates finish:
1. Read all 3 investigation reports
2. Facilitate debate: Compare findings and identify contradictions
3. Synthesize into root-cause-conclusion.md with:
   - Most likely root cause with confidence level
   - Evidence supporting the conclusion
   - Remediation plan with priority
4. Report completion with diagnosis
SPAWNPROMPT
