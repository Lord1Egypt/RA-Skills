## Description: <br>
Generic Documentation Indexing & Search. Index any documentation site (SPA/static) and search it instantly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Pektech](https://clawhub.ai/user/Pektech) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to configure documentation profiles, index documentation sites, and retrieve ranked search results or fetched page text from the terminal or Python API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can crawl websites and cache retrieved documentation text locally. <br>
Mitigation: Use approved documentation sources, avoid confidential or authenticated content unless authorized, and clear ~/.anydocs/cache when cached content should be removed. <br>
Risk: Optional browser rendering can use a gateway token. <br>
Mitigation: Use browser gateway tokens only with trusted local or HTTPS gateways and avoid committing tokens to repositories. <br>
Risk: System-wide installation can alter the Python environment. <br>
Mitigation: Prefer installation in a virtual environment unless system-wide installation has been reviewed and approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Pektech/anydocs) <br>
- [README](artifact/README.md) <br>
- [Quick Start Examples](artifact/examples/QUICKSTART.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [CLI text and Markdown guidance with URLs, snippets, relevance scores, tags, and JSON-backed profile configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can cache fetched pages and search indexes locally; browser rendering is optional for JavaScript-heavy documentation sites.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and artifact/manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
