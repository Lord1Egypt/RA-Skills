## Description: <br>
Converts X (Twitter) tweets and articles to markdown with YAML front matter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimliu](https://clawhub.ai/user/jimliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and content archivists use this skill to convert X posts, threads, and articles into local Markdown files with front matter. It can also optionally localize referenced media when the user chooses to download it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to an X session and may use or store sensitive X authentication cookies. <br>
Mitigation: Prefer X_AUTH_TOKEN and X_CT0 environment variables, review or delete the local cookies cache after use, and avoid running the skill in shared or sensitive workspaces. <br>
Risk: The skill uses a reverse-engineered X API that may break or trigger account restrictions if X changes behavior or policy. <br>
Mitigation: Require explicit user consent before conversion and stop when the user declines the reverse-engineered API disclaimer. <br>
Risk: Optional media localization downloads remote image or video files into the workspace. <br>
Mitigation: Download media only when expected, keep the ask-each-time preference for normal use, and review downloaded files before sharing or committing output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jimliu/baoyu-danger-x-to-markdown) <br>
- [Homepage](https://github.com/JimLiu/baoyu-skills#baoyu-danger-x-to-markdown) <br>
- [First-time setup reference](references/config/first-time-setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files with YAML front matter, optional JSON command output, and optional downloaded media files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are organized under an X-to-Markdown directory by account and content identifier unless the user supplies an output path.] <br>

## Skill Version(s): <br>
1.117.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
