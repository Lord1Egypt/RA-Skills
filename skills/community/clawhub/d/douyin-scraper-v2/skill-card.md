## Description: <br>
Retrieves Douyin hot-search topics and search suggestions, supports keyword matching against hot lists, and can run without login for supported endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and content research agents use this skill to fetch Douyin hot-search topics, search suggestions, and keyword-matched trend summaries from command-line workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup can download Playwright and Chromium, and runtime commands contact Douyin APIs. <br>
Mitigation: Install only when those downloads and network calls are acceptable for the environment; prefer the documented install path or official sources. <br>
Risk: The optional --output argument writes results to a user-specified path. <br>
Mitigation: Review the requested output path before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/douyin-scraper-v2) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [CLI text summaries with optional JSON file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports hot-list, suggestion, and keyword search modes; optional --output writes JSON results.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
