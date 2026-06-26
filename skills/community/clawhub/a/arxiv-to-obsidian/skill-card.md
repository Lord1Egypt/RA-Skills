## Description: <br>
Fetches the latest arXiv cs.AI papers, translates titles and abstracts into Simplified Chinese, and appends a Markdown table to a configured Obsidian daily note. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SenryLee](https://clawhub.ai/user/SenryLee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers who organize AI research in Obsidian use this skill to collect current arXiv cs.AI paper metadata, translate it to Simplified Chinese, and write it into a daily literature note. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Misconfigured vault or folder settings can write the generated paper table to the wrong Obsidian location. <br>
Mitigation: Review scripts/config.sh, confirm VAULT_NAME and VAULT_FOLDER, and run with DRY_RUN=1 before first use. <br>
Risk: The translation step sends public arXiv metadata through the local Claude CLI account configured on the user's machine. <br>
Mitigation: Use only when comfortable translating public arXiv metadata with the local Claude CLI account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SenryLee/arxiv-to-obsidian) <br>
- [Publisher profile](https://clawhub.ai/user/SenryLee) <br>
- [arXiv cs.AI RSS feed](https://export.arxiv.org/rss/cs.AI) <br>
- [Obsidian](https://obsidian.md/) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown table appended to an Obsidian note, with shell command guidance for setup and dry-run execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local curl, python3, claude, and obsidian commands; supports environment-variable configuration and DRY_RUN=1 preview mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
