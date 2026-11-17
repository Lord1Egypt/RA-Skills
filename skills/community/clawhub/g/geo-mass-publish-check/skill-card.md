## Description:

GEO 待群发 - 拉取范文/仿写状态，待导出时下载 ZIP 到本机并上报，可群发时提示用户。QClaw 定时只装本 skill 即可。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chameleon-nexus](https://clawhub.ai/user/chameleon-nexus)

### License/Terms of Use:

MIT-0

## Use Case:

Operators and developers managing GEO mass-publish workflows use this skill to check pending export status, download fanwen and fangxie ZIP exports when ready, and report local paths for batch import.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically uses a local GEO API key during scheduled or manual runs.

Mitigation: Install only when the GEO service and API key are trusted, and review scheduled-run behavior before enabling it.

Risk: ZIP export paths are built from remote task metadata.

Mitigation: Sanitize brand, product, and cycle path components and verify the final path remains under ~/.qclaw/geo-exports before writing files.

Risk: Downloaded ZIP files may overwrite existing local exports unexpectedly.

Mitigation: Check for existing ZIP files before download and require an explicit overwrite or versioned output path.

Risk: Manual JSON construction for export callbacks can break or misrepresent path data.

Mitigation: Build callback payloads with a JSON serializer rather than interpolated strings.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chameleon-nexus/skills/geo-mass-publish-check)
- [Publisher Profile](https://clawhub.ai/user/chameleon-nexus)
- [GEO API Service](https://ai.gaobobo.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown status summary with inline shell commands and local ZIP file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May download fanwen.zip and fangxie.zip exports under ~/.qclaw/geo-exports when task metadata indicates an export is needed.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
