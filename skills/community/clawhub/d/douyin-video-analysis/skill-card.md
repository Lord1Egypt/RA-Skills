## Description:

Analyze a Douyin video from a shared URL by extracting page metadata, capturing audio when possible, transcribing speech into readable text, summarizing content, extracting useful information plus evidence, applying critical analysis, and saving both transcript and analysis into Obsidian.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzmbobby](https://clawhub.ai/user/zzmbobby)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, creators, operators, and critical readers use this skill to turn a Douyin URL into a transcript, structured notes, evidence-backed summary, and critique of the video's claims, hook, persuasion tactics, and reasoning quality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may reuse live browser cookies while attempting to download Douyin media.

Mitigation: Run it from an isolated Chrome profile with no important logged-in sessions, validate Douyin/CDN destinations before download, and avoid cookie replay where possible.

Risk: The workflow writes persistent transcript and analysis notes into a configured Obsidian vault.

Mitigation: Ask for confirmation before writing notes, scope allowed output paths, and use private per-run temporary files for media processing.

Risk: Untrusted Douyin links can trigger browser automation and local file creation.

Mitigation: Use only Douyin links the user trusts and review the skill before installing or running it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zzmbobby/skills/douyin-video-analysis)
- [Douyin](https://www.douyin.com)
- [README](artifact/README.md)
- [Analysis Template](artifact/analysis_template.md)
- [Douyin Analysis Workflow](artifact/douyin_analysis_workflow.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown notes, JSON helper results, shell commands, and chat summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates transcript and analysis notes in Obsidian when the local environment and media access path are available.]

## Skill Version(s):

0.1.4 (source: server release evidence and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
