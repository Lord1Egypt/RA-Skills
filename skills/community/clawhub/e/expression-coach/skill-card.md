## Description:

Expression Coach is a Chinese-first personal speech coaching skill for impromptu practice, role-play scenarios, communication-framework lookup, custom topics, progress analytics, and daily expression tips, with voice-first feedback powered by Whisper transcription.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andrelyl](https://clawhub.ai/user/andrelyl)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to practice spoken workplace and social communication through voice answers, simulated conversations, practical frameworks, scored feedback, and progress reports. Optional Feishu Bitable configuration supports persistent custom topics and practice history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional Feishu Bitable integration can persist raw voice recordings, transcripts, scores, and analytics outside the agent environment.

Mitigation: Enable Bitable only when persistent cloud history is needed, confirm what data is saved and who can access it, and verify deletion paths before use.

Risk: Feishu app permissions may expose more practice data than intended if configured broadly.

Mitigation: Use least-privilege Feishu permissions and restrict table access to the intended users or workspace administrators.

Risk: Daily tips and automatic recording can create ongoing data collection or notifications beyond the user's immediate practice session.

Mitigation: Keep Bitable and daily tips disabled unless explicitly desired, and document how users can pause notifications and remove stored records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andrelyl/skills/expression-coach)
- [README](artifact/README.md)
- [Expression frameworks](artifact/references/frameworks.md)
- [Impromptu topic library](artifact/references/topics.md)
- [Role-play scenarios](artifact/references/scenarios.md)
- [Daily expression tips](artifact/references/daily-tips.md)
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu media upload API](https://open.feishu.cn/open-apis/drive/v1/medias/upload_all)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown coaching responses with structured scoring, spoken-expression analysis, practical examples, shell command snippets, and JSON configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Voice-first interaction; optional Feishu Bitable persistence for recordings, transcripts, scores, analytics, custom topics, and daily-tip scheduling.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
