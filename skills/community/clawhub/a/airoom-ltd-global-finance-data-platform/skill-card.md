## Description: <br>
Automatically downloads financial data files from a configured airoom.ltd WordPress page using Playwright, with configurable limits and blocked executable file types. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[airoom-ai](https://clawhub.ai/user/airoom-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to test access to an airoom.ltd WordPress page, download public financial data files into a local directory, and inspect downloader configuration. Human review is needed before using downloaded data or bundled finance text for financial decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Downloaded files may contain unsafe or unexpected content. <br>
Mitigation: Use a dedicated output directory, set a small WP_MAX_FILES value, and scan downloads before opening them. <br>
Risk: Bundled finance and AI-coordination text could be misused as autonomous trading guidance. <br>
Mitigation: Treat downloaded data and strategy text as reference material only, and require human review before any financial decision or trade. <br>
Risk: WordPress credentials could be exposed if entered on an HTTP page. <br>
Mitigation: Avoid entering credentials on HTTP pages; use the public target page without login unless a secure authenticated workflow is separately verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/airoom-ai/airoom-ltd-global-finance-data-platform) <br>
- [Publisher profile](https://clawhub.ai/user/airoom-ai) <br>
- [airoom.ltd target data page](http://airoom.ltd/index.php/airoom/) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown-style operational guidance, command-line output, JSON configuration, and downloaded local files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses WP_URL, WP_TARGET_URL, optional WP_USERNAME and WP_PASSWORD, WP_OUTPUT_DIR, and WP_MAX_FILES; downloaded files should be scanned before use.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
