## Description: <br>
Alembic turns ChatGPT shared links or pasted LLM conversations into structured Markdown knowledge notes for Obsidian or a chosen local folder. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyang-yao75](https://clawhub.ai/user/yuyang-yao75) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, knowledge workers, and Obsidian users use this skill to distill raw AI conversations into reusable concept notes. It supports ChatGPT shared links, pasted conversation text, optional keyword selection, and local Markdown output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read sensitive conversation content and write notes into the configured output directory. <br>
Mitigation: Use only conversation content you are comfortable processing locally, and choose an explicit output directory when you do not want notes written under OBSIDIAN_VAULT_PATH. <br>
Risk: Fetching ChatGPT shared links requires network access to chatgpt.com or chat.openai.com. <br>
Mitigation: Use pasted conversation text or a local HTML file when you want to avoid network fetching. <br>


## Reference(s): <br>
- [Alembic ClawHub Skill Page](https://clawhub.ai/yuyang-yao75/distill-conversation) <br>
- [Publisher Profile: yuyang-yao75](https://clawhub.ai/user/yuyang-yao75) <br>
- [README.en.md](artifact/README.en.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown notes with YAML frontmatter, plus optional JSON from the ChatGPT share parser] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs one Markdown note per selected or extracted keyword and writes only to the selected output directory, OBSIDIAN_VAULT_PATH/00.Inbox, or the current directory.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
