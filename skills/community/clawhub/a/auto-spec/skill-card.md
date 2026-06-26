## Description: <br>
Spec-driven development assistant that helps developers write precise behavioral specs before coding or reverse-engineer specs from existing code for understanding and alignment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuanyan](https://clawhub.ai/user/yuanyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use AutoSpec to align on behavioral contracts before implementation, or to extract factual module, feature, or function behavior from existing code before changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated specs or implementation suggestions may be incorrect or incomplete for sensitive features, persistence flows, external URLs, network validation, or conversation history handling. <br>
Mitigation: Review generated specs and code before adoption, especially where sensitive data, network behavior, or persistence is involved. <br>
Risk: Reverse-engineered specs can reflect current code behavior, including bugs or legacy behavior, rather than intended product behavior. <br>
Mitigation: Treat reverse specs as a pre-change baseline and confirm flagged notes or open questions before using them as requirements. <br>


## Reference(s): <br>
- [AutoSpec ClawHub release](https://clawhub.ai/yuanyan/auto-spec) <br>
- [Publisher profile](https://clawhub.ai/user/yuanyan) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown behavioral specs in chat, with code output when implementation is explicitly requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Specs are conversational by default and are only written to files when the user explicitly asks.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
