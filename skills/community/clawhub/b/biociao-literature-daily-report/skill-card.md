## Description: <br>
Generates Chinese daily research literature reports by collecting recent PubMed, bioRxiv, and arXiv papers, categorizing life-science and AI topics, summarizing papers, and syncing results to Zotero and a knowledge graph. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[biociao](https://clawhub.ai/user/biociao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers and research-support agents use this skill to collect recent life-science and AI literature, create a curated Chinese Markdown daily report, and update connected research repositories such as Zotero or a knowledge graph. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can load Zotero credentials from the shell environment and update shared Zotero data. <br>
Mitigation: Use a limited Zotero API key, verify the group ID, and confirm helper scripts before running. <br>
Risk: Generated reports and literature facts may be persisted to workspace directories and OpenClaw memory. <br>
Mitigation: Run only when those persistent destinations are intended and review output paths and knowledge graph entity targets first. <br>
Risk: The report may be sent to Matrix as an outbound side effect. <br>
Mitigation: Confirm the Matrix destination and avoid scheduled runs unless outbound sharing is expected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/biociao/biociao-literature-daily-report) <br>
- [Category Standards](references/categories.md) <br>
- [Workflow Guide](references/workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with optional Python code edits, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes report files and may sync results to Zotero, OpenClaw knowledge graph memory, ClawLib, and Matrix when configured.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
