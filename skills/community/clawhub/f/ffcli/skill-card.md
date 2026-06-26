## Description: <br>
Query Fireflies.ai meeting recordings, transcripts, AI summaries, and action items through the ffcli command-line tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ruigomeseu](https://clawhub.ai/user/ruigomeseu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and agents use this skill to search Fireflies.ai meetings, retrieve transcripts, read AI summaries, and extract action items from calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a third-party ffcli package that can access Fireflies.ai meeting data. <br>
Mitigation: Install only from trusted @ruigomeseu npm or Homebrew sources and review the package or tap history before use. <br>
Risk: The skill requires FIREFLIES_API_KEY and can expose meeting metadata, transcripts, summaries, and action items. <br>
Mitigation: Use a dedicated or least-privileged key where available, scope prompts to intended meetings, avoid broad queries, and rotate the key if local config or OpenClaw settings may have been exposed. <br>


## Reference(s): <br>
- [ClawHub Ffcli Skill](https://clawhub.ai/ruigomeseu/ffcli) <br>
- [npm package @ruigomeseu/ffcli](https://www.npmjs.com/package/@ruigomeseu/ffcli) <br>
- [Homebrew tap ruigomeseu/homebrew-tap](https://github.com/ruigomeseu/homebrew-tap) <br>
- [Fireflies.ai Developer Settings](https://app.fireflies.ai/settings) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples; ffcli command output may be JSON or Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the ffcli binary and FIREFLIES_API_KEY; meeting dates in JSON output are UTC.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
