## Description: <br>
Aion Skill Builder generates complete AION trading skill templates from natural-language strategy descriptions, including metadata, ClawHub configuration, and Python trading code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ssj124](https://clawhub.ai/user/ssj124) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-skill authors use this skill to turn a plain-language prediction-market strategy into a starter ClawHub skill folder with AION SDK integration, environment declarations, and generated Python code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for sensitive credentials, including API keys and an optional wallet private key. <br>
Mitigation: Use limited or test credentials, avoid providing a real wallet private key, and keep generated skills in dry-run mode until reviewed. <br>
Risk: Strategy descriptions are processed with OpenAI for metadata and code generation. <br>
Mitigation: Do not enter confidential strategies or secrets in prompts, and assume strategy text may be sent to OpenAI. <br>
Risk: Generated trading files may contain incorrect or unsafe trading logic. <br>
Mitigation: Manually review generated skill.py and clawhub.json before running, publishing, or enabling recurring automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ssj124/aion-skill-builder) <br>
- [AION agents API key page](https://www.aionmarket.com/agents) <br>
- [AION building skills documentation](https://docs.aion.market/essentials/building-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, shell commands] <br>
**Output Format:** [Generated skill folder files plus conversational prompts and status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated skills declare required environment variables and default generated trading logic to dry-run behavior.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
