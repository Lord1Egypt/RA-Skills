## Description:

Clipcat helps agents use the Clipcat CLI for TikTok e-commerce video search, product insights, viral video replication, product-to-video generation, video analysis, and video download workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a2888409](https://clawhub.ai/user/a2888409)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, creators, and commerce teams use this skill to direct agents through Clipcat CLI workflows for TikTok Shop research, product video generation, viral video replication, and asynchronous task tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a third-party native Clipcat CLI without pinned checksums or signature verification.

Mitigation: Install only when the Clipcat distribution channel is trusted, and request or verify pinned checksums or signatures for platform archives before deployment.

Risk: The Clipcat CLI uses a Clipcat API key and may process local media paths or remote asset URLs supplied by the user.

Mitigation: Use a scoped API key where available, avoid sharing unnecessary local media, and review commands before exposing sensitive file paths or assets.

Risk: Some video generation commands consume paid credits.

Mitigation: Run `clipcat quote` with the same parameters, show the returned total cost, get explicit user approval, and submit with `--expected-credits`.

## Reference(s):

- [Clipcat Skill Page](https://clawhub.ai/a2888409/skills/clipcat)
- [Clipcat Homepage](https://clipcat.ai)
- [Clipcat API Key Settings](https://clipcat.ai/workspace?modal=settings&tab=apikeys)
- [Clipcat CLI macOS Apple Silicon archive](https://static.clipcat.ai/public/cli/v1.0.24/clipcat_darwin_arm64.tar.gz)
- [Clipcat CLI macOS Intel archive](https://static.clipcat.ai/public/cli/v1.0.24/clipcat_darwin_amd64.tar.gz)
- [Clipcat CLI Linux x86_64 archive](https://static.clipcat.ai/public/cli/v1.0.24/clipcat_linux_amd64.tar.gz)
- [Clipcat CLI Linux arm64 archive](https://static.clipcat.ai/public/cli/v1.0.24/clipcat_linux_arm64.tar.gz)
- [Clipcat CLI Windows x86_64 archive](https://static.clipcat.ai/public/cli/v1.0.24/clipcat_windows_amd64.zip)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI JSON output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLIPCAT_API_KEY and the Clipcat CLI; paid video commands should be quoted and explicitly confirmed before submission.]

## Skill Version(s):

1.0.24 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
