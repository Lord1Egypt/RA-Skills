## Description: <br>
Design and optimize caching strategies for applications. Analyze data access patterns, recommend cache layers (browser, CDN, application, database), configure TTLs, invalidation policies, and measure cache hit rates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to assess existing cache layers, identify caching opportunities and anti-patterns, choose browser, CDN, application, and database cache strategies, and generate practical TTL, invalidation, and debugging guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagnostic commands may inspect the wrong host or environment if variables such as HOST are set incorrectly. <br>
Mitigation: Confirm the target host and environment before execution and run commands with the minimum privileges needed. <br>
Risk: Generated cache settings could cause stale data or production regressions if applied without validation. <br>
Mitigation: Review cache policies in staging, verify TTLs and invalidation behavior against application data-change patterns, and monitor hit rates and evictions before rollout. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/cache-strategy-advisor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with inline shell commands, cache policy tables, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include TTL recommendations, invalidation policies, cache hit-rate diagnostics, and cache issue debugging steps.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
