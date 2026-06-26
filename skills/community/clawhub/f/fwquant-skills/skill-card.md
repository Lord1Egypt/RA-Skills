## Description: <br>
FWQuant Skills provides a quantitative trading analysis stub that accepts symbol, timeframe, and strategy inputs and returns a structured analysis message. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuwenquant](https://clawhub.ai/user/fuwenquant) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantitative trading practitioners can use this skill as a lightweight ClawHub skill scaffold for crypto strategy analysis prompts and structured signal messaging. It should not be treated as a complete trading system. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The current release is a minimal analysis stub, not a complete trading system. <br>
Mitigation: Use it for analysis scaffolding only and do not rely on it for live trading decisions or order execution. <br>
Risk: Future versions may add exchange connectivity or live trading behavior. <br>
Mitigation: Use paper trading first, prefer read-only or tightly scoped API keys, require explicit confirmation before orders, and enforce position limits. <br>
Risk: Future web UI behavior could unintentionally expose local services if remote access is enabled. <br>
Mitigation: Bind web services to 127.0.0.1 unless remote access is intentional and protected. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fuwenquant/fwquant-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [JSON-like structured result with success, message, and data fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes symbol, timeframe, strategy, analysis text, and timestamp; the current implementation does not execute trades.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
