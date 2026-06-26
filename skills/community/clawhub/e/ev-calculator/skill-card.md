## Description: <br>
EV Calculator helps agents calculate expected value, Polymarket edge, win/loss ratios, and related trading decision metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinboh68-prog](https://clawhub.ai/user/jinboh68-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to compute expected value for trading, betting, and Polymarket-style probability decisions. It can return local command-line calculations or JSON-formatted analysis for downstream agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes an optional paid external API path using x402 payment details. <br>
Mitigation: Confirm the payment destination, price, chain, and endpoint before invoking the API path. <br>
Risk: Trading assumptions and probability estimates may be sensitive if sent to an external endpoint. <br>
Mitigation: Use local calculations for confidential scenarios or avoid submitting sensitive trading assumptions unless sharing them is acceptable. <br>
Risk: Expected value outputs are estimates and may be misleading if fees, slippage, funding costs, or weak probability inputs are omitted. <br>
Mitigation: Review inputs and account for market friction before using results in trading or betting decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jinboh68-prog/ev-calculator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with Python command examples and optional JSON calculator output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports basic EV, Polymarket edge, and half-Kelly position suggestions when the relevant inputs are provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
