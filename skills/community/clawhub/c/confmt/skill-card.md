## Description: <br>
Format, convert, flatten, and diff configuration files. Supports JSON, TOML (Python 3.11+), and .env formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rogue-agent1](https://clawhub.ai/user/rogue-agent1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Confmt to pretty-print, compact, sort, flatten, convert, and compare configuration files while working with JSON, TOML, .env, and dot-notation formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Formatted, converted, or diffed configuration output can reveal secrets from .env files, API keys, passwords, tokens, or private configs. <br>
Mitigation: Run the skill only on configuration files whose contents are acceptable to show in agent output, logs, or transcripts. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and formatted configuration text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May echo configuration values into agent-visible output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
