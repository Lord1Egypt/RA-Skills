## Description: <br>
Reviews Elixir code for performance issues including GenServer bottlenecks, memory usage, and concurrency patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review Elixir applications for performance risks in GenServer design, memory behavior, concurrency, ETS usage, and database access patterns before reporting findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a referenced review-verification-protocol skill before reporting substantive findings. <br>
Mitigation: Confirm that review-verification-protocol is installed locally and trusted before using this skill for performance review output. <br>
Risk: Performance issues may be overstated if claims are not supported by observed rates, item counts, ratios, profiler output, logs, or search scope. <br>
Mitigation: Require anchored evidence for each finding and downgrade unsupported bottleneck, N+1, unbounded growth, or memory-cost claims to questions or suspected issues. <br>


## Reference(s): <br>
- [Elixir Performance Review](https://clawhub.ai/anderskev/elixir-performance-review) <br>
- [Concurrency Patterns](references/concurrency.md) <br>
- [ETS Patterns](references/ets-patterns.md) <br>
- [GenServer Bottlenecks](references/genserver-bottlenecks.md) <br>
- [Memory Patterns](references/memory.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown review findings with anchored evidence and optional Elixir code suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings should include concrete file or function locators and should downgrade unverified performance claims to questions or suspected issues.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
