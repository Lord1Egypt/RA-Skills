## Description: <br>
Provides agents with structured, simulated global financial market data documents and quantitative strategy reference material for market monitoring and analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[airoom-ai](https://clawhub.ai/user/airoom-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI operators use this skill to download and review airoom.ltd financial data files, environment scores, and strategy reference material for market monitoring workflows. It should be used for information gathering only, with human review before any financial action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automates browser-based downloads from a configured financial data page and may retrieve unexpected or unsafe files. <br>
Mitigation: Use only manual, user-directed downloads from authorized pages, prefer HTTPS, set a small WP_MAX_FILES value, and scan downloaded files before opening them. <br>
Risk: The documentation encourages risky AI-driven investing workflows and strategy signals. <br>
Mitigation: Treat all data and signals as informational only; do not let an agent place trades or act on strategy signals without explicit human and regulatory review. <br>
Risk: Optional WordPress credentials can be supplied for authenticated pages. <br>
Mitigation: Avoid storing credentials in config, use scoped credentials only when required, and remove credentials after the download task completes. <br>
Risk: The default target configuration uses HTTP. <br>
Mitigation: Prefer HTTPS endpoints when available and verify the source page before downloading files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/airoom-ai/finance-airoom) <br>
- [Publisher profile](https://clawhub.ai/user/airoom-ai) <br>
- [airoom.ltd public data page](http://airoom.ltd/index.php/airoom/) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with Python commands, configuration JSON, and downloaded local data files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require WP_URL, WP_TARGET_URL, optional WordPress credentials, WP_OUTPUT_DIR, and WP_MAX_FILES.] <br>

## Skill Version(s): <br>
1.0.0 (source: target metadata and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
