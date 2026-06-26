## Description: <br>
Get an independent risk assessment for any proposed Uniswap operation, including swaps, LP positions, bridges, and token interactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and DeFi operators use this skill to get a second-opinion risk check before proposed Uniswap swaps, LP positions, bridges, or token interactions. It summarizes slippage, impermanent loss, liquidity, smart contract, and bridge risks into a clear decision and mitigation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A favorable risk decision can still be mistaken for proof that a trade is risk-free. <br>
Mitigation: Treat the assessment as decision support, verify the operation details, and avoid relying on APPROVE as a guarantee. <br>
Risk: The skill delegates analysis to a configured risk-assessor subagent. <br>
Mitigation: Confirm the configured risk-assessor subagent is trusted before using the skill for real DeFi decisions. <br>
Risk: Prompts may include sensitive portfolio or account details. <br>
Mitigation: Keep prompts specific to the operation and avoid sharing unnecessary account or portfolio information. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown risk assessment with per-dimension scores and a final decision] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return APPROVE, CONDITIONAL_APPROVE, VETO, or HARD_VETO decisions; does not execute trades.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
