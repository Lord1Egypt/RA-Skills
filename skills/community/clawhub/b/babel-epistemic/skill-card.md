## Description: <br>
Prevents metacognitive poisoning in multi-agent handoffs by guiding agents to tag confidence and provenance so downstream agents maintain calibration without promoting inferences to verified facts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mdiskint](https://clawhub.ai/user/mdiskint) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and developers use this skill in multi-agent workflows to label assertion confidence, intent, register, affect, grounds, and trajectory so downstream agents do not treat inherited inferences as verified facts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The forwarding block intentionally asks downstream agents to copy protocol text into future handoffs, which can spread beyond the installer's direct control. <br>
Mitigation: Install only for controlled multi-agent workflows where all participants agree to the convention; remove or constrain the forwarding block before using it with outside agents, customers, or unrelated workflows. <br>
Risk: Downstream agents may treat inherited confidence labels as proof rather than provenance. <br>
Mitigation: Require independent confirmation before promoting DERIVED, REPORTED, PATTERN_MATCH, SPECULATION, or UNKNOWN assertions to VERIFIED_DATA. <br>


## Reference(s): <br>
- [Babel specification and research](https://hearth.so/babel) <br>
- [Babel validation package](https://www.npmjs.com/package/babel-validate) <br>
- [ClawHub release page](https://clawhub.ai/mdiskint/babel-epistemic) <br>
- [Publisher profile](https://clawhub.ai/user/mdiskint) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance and protocol text for agent handoffs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; no code execution, tool calls, or credential access are described in the security evidence.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata; artifact frontmatter version is 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
