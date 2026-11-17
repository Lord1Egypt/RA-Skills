## Description:

AI video repurposing and digital human dubbing web tool that turns a Douyin or TikTok link into rewritten speech, synthesized audio, and a talking-head video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shylamb-token](https://clawhub.ai/user/shylamb-token)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, teams, and developers use this skill to repurpose short-form video speech into reviewed scripts, voiceover audio, and digital human talking-head videos through a local web UI or REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The service exposes media-processing and file-writing behavior with weak access controls.

Mitigation: Run it in an isolated local environment, bind it to 127.0.0.1 unless authentication is added, and do not expose the service publicly.

Risk: Uploaded or downloaded media, transcripts, rewrites, audio, and generated videos may remain on disk.

Mitigation: Assume task data persists until manually cleaned and review local data directories after each run, especially when processing sensitive content.

Risk: Browser cookies, third-party API calls, and generated likeness content can create privacy, consent, copyright, or misuse issues.

Mitigation: Do not share browser cookies with an assistant or third party, review copyright and likeness consent before processing content, and prefer local models for sensitive material.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/shylamb-token/skills/ai-recreator)
- [README](artifact/README.md)
- [Quickstart](artifact/references/quickstart.md)
- [FAQ](artifact/references/faq.md)
- [Privacy and data handling](artifact/references/privacy.md)
- [Anti-patterns](artifact/references/anti-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code, shell commands, configuration values, and generated media workflow outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create local media files, transcripts, rewritten text, synthesized audio, and final video outputs when the web service is run.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact frontmatter reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
