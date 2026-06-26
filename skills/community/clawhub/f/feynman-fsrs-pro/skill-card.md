## Description: <br>
基于 FSRS 算法的费曼学习导师，通过 PostgreSQL 记忆库与 Obsidian 笔记联动，引导用户进行深度复习。严格遵循笔记同步→到期检查→针对性提问→动态追问→结算存储的五步流程。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sheldon-mmmp](https://clawhub.ai/user/sheldon-mmmp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Learners and developers use this skill as an interactive Feynman-style study tutor that synchronizes Obsidian notes, checks due review items, asks targeted questions, follows up dynamically, and records spaced-repetition progress in PostgreSQL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill embeds PostgreSQL credentials and expects access to a named local database. <br>
Mitigation: Replace hardcoded credentials before use and restrict the database account to the least privileges needed for review operations. <br>
Risk: The skill uses shell-based Obsidian CLI access and can process note filenames from the local vault. <br>
Mitigation: Avoid untrusted note filenames and patch the Obsidian CLI wrapper to avoid shell:true before deployment. <br>
Risk: The bundled schema initialization drops and recreates the feynman_memory table. <br>
Mitigation: Run schema.sql only against a database that is intended to be reset or after taking an appropriate backup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sheldon-mmmp/feynman-fsrs-pro) <br>
- [Publisher profile](https://clawhub.ai/user/sheldon-mmmp) <br>
- [ClawHub registry](https://clawhub.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Interactive Markdown text with JSON command results and shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Coordinates local Obsidian note access and PostgreSQL review-state updates.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
