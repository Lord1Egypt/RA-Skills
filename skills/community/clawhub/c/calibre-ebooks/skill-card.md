## Description: <br>
Manage and query a local Calibre library through a local Books API, Python helper client, and optional semantic RAG workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[carlosdelfino](https://clawhub.ai/user/carlosdelfino) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and library administrators use this skill to let an agent search a configured Calibre catalog, inspect metadata and formats, retrieve local book files or covers, and query indexed book content. It is suited to environments that intentionally run the companion Books API and related local services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes network-capable API, upload, download, external search, and background-service behavior beyond a simple local catalog helper. <br>
Mitigation: Install it only when those gateway capabilities are intended, keep the API bound to localhost or a trusted network, and review enabled services before use. <br>
Risk: Weak or unauthenticated API access could expose local library metadata or file operations. <br>
Mitigation: Set a strong API key, keep unauthenticated access disabled, and avoid exposing the Books API beyond localhost unless protected by additional controls. <br>
Risk: OpenLibrary, download queue, upload, VirusTotal scanning, and background RAG workers can send data to external services or perform persistent processing. <br>
Mitigation: Review these defaults explicitly, disable VirusTotal unless third-party file submission is acceptable, and treat systemd workers and upload/download features as administrative capabilities. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/carlosdelfino/calibre-ebooks) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Books API and gateway README](artifact/calibre-openclaw-gateway/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Files, Guidance] <br>
**Output Format:** [Markdown responses with inline shell commands, JSON API results, and local file or cover artifacts when authorized] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local Books API and environment-based configuration; file outputs are expected to stay in skill-specific temporary directories.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
