## Description: <br>
从 Get 笔记 (biji.com) 同步语音笔记到本地 Markdown。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skychentian](https://clawhub.ai/user/skychentian) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users with a Get 笔记 account use this skill to sync voice-note transcripts and summaries into a local Markdown archive. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores reusable biji.com login and session data locally. <br>
Mitigation: Use a private, non-shared, non-repository directory and add .token-cache.json, .auth-state.json, and .sync-state.json to ignore rules. <br>
Risk: The dedupe helper can delete local note files. <br>
Mitigation: Run dedupe only after backing up notes and reviewing what it will delete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/skychentian/get-biji) <br>
- [Get 笔记](https://biji.com) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown files with YAML frontmatter, optional transcript Markdown files, and local JSON state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are organized under Get笔记/YYYY-MM and can be limited by OUTPUT_DIR, SINCE_DATE, and TEST_LIMIT.] <br>

## Skill Version(s): <br>
3.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
