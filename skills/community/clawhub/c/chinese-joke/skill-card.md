## Description: <br>
Provides a local Chinese joke library with multiple joke types, including puns, programmer jokes, everyday humor, riddles, and short stories, without relying on external APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Djttt](https://clawhub.ai/user/Djttt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to retrieve one or more Chinese jokes from a bundled local JSON database, optionally filtering by joke type. It is useful when an agent needs lightweight Chinese humor text without network calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled joke content may be unsuitable for some audiences or contexts. <br>
Mitigation: Review and edit artifact/jokes.json before deployment if content standards matter. <br>
Risk: The helper scripts execute local Bash and Python code. <br>
Mitigation: Review the small helper scripts before installation and run them in the intended skill directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Djttt/chinese-joke) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [jokes.json](artifact/jokes.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text jokes and Markdown usage guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads bundled local JSON content and supports type and count filters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
