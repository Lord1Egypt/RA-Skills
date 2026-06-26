## Description: <br>
Provides CCXT-based guidance for cryptocurrency exchange APIs, including order management, market data queries, balance monitoring, streaming data, and lending workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build or review agent-generated code and operating guidance for CCXT-style crypto exchange workflows, including market loading, API request construction, WebSocket streaming, order management, balance monitoring, and lending automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide real crypto account actions, including orders and lending workflows. <br>
Mitigation: Use read-only or testnet credentials first, require explicit confirmation before live orders or lending actions, and avoid withdrawal permissions unless they are strictly required. <br>
Risk: The evidence security summary flags mixed crypto scope with unrelated A-share/ZVT stock workflows and unclear safety boundaries. <br>
Mitigation: Resolve the crypto versus ZVT/A-share workflow mismatch before relying on generated trading or backtesting guidance. <br>
Risk: The artifact warns that generated results may have uncaptured requirement gaps. <br>
Mitigation: Verify critical decisions against the bundled reference files and review exchange-specific requirements before deployment. <br>


## Reference(s): <br>
- [Known Use Cases](artifact/references/USE_CASES.md) <br>
- [Anti-Patterns](artifact/references/ANTI_PATTERNS.md) <br>
- [Cross-Project Wisdom](artifact/references/WISDOM.md) <br>
- [Semantic Locks and Preconditions](artifact/references/LOCKS.md) <br>
- [Component Capability Map](artifact/references/COMPONENTS.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/tangweigang-jpg/ccxt-crypto-api) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline code, command snippets, and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request target market, data provider, strategy type, time range, and target entity IDs before producing implementation guidance.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
