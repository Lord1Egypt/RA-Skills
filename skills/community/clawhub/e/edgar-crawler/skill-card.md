## Description: <br>
Edgar Crawler helps agents collect SEC EDGAR 10-K and 10-Q filings in bulk, with quarterly incremental updates and local caching for financial analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and financial analysts use this skill to guide SEC EDGAR filing retrieval and local data-pipeline setup for downstream financial analysis. Review requests carefully because the release also contains unrelated quant trading and ZVT workflow material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is labeled as an SEC filing crawler, but evidence.security reports that its instructions also steer users into unrelated quant trading and ZVT workflows. <br>
Mitigation: Review the requested workflow before execution and only run SEC filing download steps when that is the intended task. <br>
Risk: The security guidance warns against providing broker, wallet, JoinQuant, QMT, or paid-provider credentials for SEC filing downloads. <br>
Mitigation: Do not provide those credentials or run ZVT setup or backtesting commands unless intentionally using that separate quant workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tangweigang-jpg/edgar-crawler) <br>
- [Use Cases](references/USE_CASES.md) <br>
- [Component Capability Map](references/COMPONENTS.md) <br>
- [Constraints](references/CONSTRAINTS.md) <br>
- [Anti-Patterns](references/ANTI_PATTERNS.md) <br>
- [Semantic Locks](references/LOCKS.md) <br>
- [Source Seed](references/seed.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with code blocks and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose data collection, parsing, caching, setup, or validation steps for SEC filing workflows.] <br>

## Skill Version(s): <br>
0.3.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
