## Description: <br>
Claw Recall indexes agent transcripts and connected Gmail, Google Drive, and Slack sources into local SQLite search so agents can recover context, search past conversations, and share knowledge across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rodbland2021](https://clawhub.ai/user/rodbland2021) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to give OpenClaw or Claude Code agents searchable local memory for post-compaction recovery, previous decisions, cross-agent work, and optional external sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can index broad private content, including agent transcripts and connected Gmail, Drive, or Slack sources. <br>
Mitigation: Keep indexed sources tightly scoped and avoid secrets, regulated data, or content that should not be shared across agents. <br>
Risk: Shared memory across agents may reveal prior conversations or external-source content to agents that should not access it. <br>
Mitigation: Use the skill only where cross-agent memory sharing is intended, and limit data sources and agent access accordingly. <br>
Risk: Remote SSE or REST access can expose memory search over a network without enough access-control guidance. <br>
Mitigation: Keep endpoints local or behind a trusted VPN, and add authentication and TLS before exposing them beyond trusted environments. <br>
Risk: Semantic search can send query or embedding-related data through an external OpenAI API key. <br>
Mitigation: Prefer local or keyword-only search when privacy matters, and enable semantic search only after reviewing data-handling requirements. <br>
Risk: The server evidence does not provide resolved GitHub provenance for this version. <br>
Mitigation: Verify the external repository and dependencies before installation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rodbland2021/claw-recall) <br>
- [Publisher Profile](https://clawhub.ai/user/rodbland2021) <br>
- [GitHub Repository](https://github.com/rodbland2021/claw-recall) <br>
- [Full Guide](https://github.com/rodbland2021/claw-recall/blob/master/docs/guide.md) <br>
- [Changelog](https://github.com/rodbland2021/claw-recall/blob/master/CHANGELOG.md) <br>
- [Community Discord](https://discord.gg/4wGTVa9Bt6) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline bash, JSON, and tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require python3, pip3, PYTHONPATH, and optionally OPENAI_API_KEY for semantic search.] <br>

## Skill Version(s): <br>
2.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
