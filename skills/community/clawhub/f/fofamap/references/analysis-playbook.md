# Analysis Playbook

This reference captures the original project's practical tactics so the skill can preserve its style of operation without embedding a second model backend.

## Action routing

Choose the operation that matches the user's intent before writing queries.

- `search`: user wants a concrete asset list
- `host`: user gives one IP or one domain and wants a profile
- `stats`: user wants distributions, rankings, or macro patterns
- `icon-hash`: user wants a favicon pivot
- `alive-check`: user wants a reachable subset or current HTTP reachability

This routing came from the original MCP tool design and is one of the main reasons the workflow feels like an operator assistant instead of a raw API wrapper.

## Query tactics

### 1. Permission-aware fields

Do not assume premium fields are available. Start with safe fields unless the user explicitly needs more detail. If FOFA rejects a field set, rerun with a safer baseline and explain the downgrade.

### 2. Zero-result reflection

When a query returns nothing useful, do not just say "no results." Use a deliberate broadening ladder:

1. remove the most brittle filter
2. swap exact host assumptions for content or product pivots
3. reduce to the strongest signal plus coarse scope

The skill should frame later attempts as broader fallback logic, not equivalent matches.

### 3. Human-language intent to search strategy

When the user asks in natural language, map the request to:

- target technology or product
- scope such as country, region, organization, or certificate
- whether they need list, profile, or statistics
- whether they need active follow-up later

## Host profiling tactics

When analyzing one host, preserve the original project's structure:

1. exposed surface
2. likely risk
3. plausible attack path
4. one-line overall rating

Useful cues:

- high-risk management ports such as `22`, `3389`, `445`
- common database exposure
- product hints in FOFA port products
- recency of `update_time`

Good host writeups separate what FOFA directly observed from what still needs live verification.

## Statistical analysis tactics

When writing up statistics, avoid dumping raw rankings without interpretation. Focus on:

- geographic concentration
- unusual port choices
- dominant titles or organizations
- what the distribution implies operationally

Recommended structure:

1. distribution traits
2. anomalies
3. macro impact
4. short conclusion

## Live verification tactics

Live checks are not mandatory for every search. Use them when:

- the user needs an actionable subset
- FOFA data may be stale for the task
- the output is being handed to another operator

If you run live checks:

- keep them lightweight
- treat HTTP status as a freshness signal, not as security proof
- export the checked results when the user needs deliverables

## Export tactics

The original project cared about operator handoff, not only terminal output. Preserve that.

- choose `xlsx` for analyst handoff and review
- choose `csv` for automation pipelines
- include `HTTP_STATUS` when live verification was used
- keep column names stable and obvious
- prefer a project directory with exports, `targets.txt`, command hints, and a report when the task spans multiple queries

## Nuclei suggestion heuristics

When the user wants next steps after FOFA analysis, use soft recommendations before active execution.

Examples:

- Java, Spring, Shiro: `spring`, `java`, `shiro`
- WebLogic, JBoss: `weblogic`, `jboss`
- ThinkPHP, Laravel: `thinkphp`, `laravel`
- Exchange or OA: `exchange`, `oa`

If the request is broad recon, suggest general categories such as `cves` or `misconfig`. If the request names a specific vulnerability, align the recommendation to that CVE or technology directly.

## Active scan integration

The original project did not stop at advice. It could hand off or trigger Nuclei. Preserve that shape carefully:

- passive FOFA collection first
- live reachability verification second when useful
- explicit Nuclei command suggestion third
- actual scan only when the user has authorization and explicitly wants it

In project mode, the ideal handoff bundle is:

- merged export
- optional per-query exports
- `targets.txt`
- suggested or executed Nuclei command
- Markdown report

## Reporting style

The strongest reports in the original project had two layers:

1. concise analysis for the operator
2. raw-data appendix for auditability

Keep that pattern in this skill:

- top section: insight
- lower section: supporting FOFA facts, used query, live-check results, and caveats
