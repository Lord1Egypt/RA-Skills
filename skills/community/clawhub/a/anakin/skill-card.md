## Description: <br>
Convert websites into clean data at scale - scrape URLs, batch scrape, AI search, and autonomous research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Viraal-Bambori](https://clawhub.ai/user/Viraal-Bambori) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to collect web content, run AI-assisted search, and produce research outputs through the Anakin CLI. It is suited for single-page extraction, small batch scraping, source discovery, and multi-source research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted URLs, prompts, and extracted content are shared with an external Anakin service. <br>
Mitigation: Avoid confidential internal URLs, regulated data, secrets, or sensitive research prompts unless approved to send that data to Anakin. <br>
Risk: API keys may be exposed if pasted into shared chats, logs, shell history, or committed files. <br>
Mitigation: Set ANAKIN_API_KEY through a secure local environment or secret manager and review shell startup or .gitignore changes before keeping them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Viraal-Bambori/anakin) <br>
- [Anakin Website](https://anakin.io) <br>
- [Anakin Dashboard](https://anakin.io/dashboard) <br>
- [anakin-cli on PyPI](https://pypi.org/project/anakin-cli/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands; Anakin CLI runs can produce Markdown, JSON, or raw JSON files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the anakin binary and ANAKIN_API_KEY; the skill instructs agents to save command output to files.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, skill.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
