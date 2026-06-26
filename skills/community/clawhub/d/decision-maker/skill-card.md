## Description: <br>
Decision Maker helps agents structure personal or project decisions with pros-cons analysis, weighted matrices, blind choice prompts, framework selection, and risk assessment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to compare options, reduce decision bias, evaluate risks, and generate reusable decision-analysis templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An unrelated developer-workflow stub script may confuse users about which executable provides the advertised decision-analysis behavior. <br>
Mitigation: Use scripts/decide.sh for decision-analysis commands and verify command wiring before installation. <br>
Risk: The stub script can save command arguments to a local history file, which may expose sensitive decision names or business details on the local machine. <br>
Mitigation: Avoid passing sensitive information to scripts/script.sh, or set an appropriate local data directory and review stored history before sharing the environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ckchzh/decision-maker) <br>
- [Publisher profile](https://clawhub.ai/user/ckchzh) <br>
- [Publisher homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style text and terminal output from shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API keys are required; outputs are local templates and prompts for user review.] <br>

## Skill Version(s): <br>
2.0.0 (source: server-resolved release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
