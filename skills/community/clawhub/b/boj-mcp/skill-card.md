## Description: <br>
Access Bank of Japan (BOJ) statistical data, including price indices, flow of funds, balance of payments, BIS statistics, interest rates, money supply, and exchange rates, with no API key required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ajtgjmdjp](https://clawhub.ai/user/ajtgjmdjp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and agents use Boj Mcp to discover, search, and retrieve public Bank of Japan time-series datasets for monetary policy, prices, interest rates, and financial statistics analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing an unintended package or version could run code outside the expected boj-mcp release. <br>
Mitigation: Verify that the uv or PyPI package name and version match the intended boj-mcp release before installation. <br>
Risk: Downloaded public BOJ datasets may remain cached locally after retrieval. <br>
Mitigation: Review cache location and retention behavior for the runtime environment and clear cached files when local persistence is not desired. <br>


## Reference(s): <br>
- [Bank of Japan Statistical Data Search](https://www.stat-search.boj.or.jp/) <br>
- [ClawHub Skill Page](https://clawhub.ai/ajtgjmdjp/boj-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text, Configuration] <br>
**Output Format:** [Markdown with inline bash commands; referenced CLI output may be tabular text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the boj-mcp CLI to access public BOJ flat-file datasets and may rely on local caching after first download.] <br>

## Skill Version(s): <br>
0.1.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
