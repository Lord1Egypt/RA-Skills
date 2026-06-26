## Description: <br>
Fetches cleaner, readable webpage body content and converts it to Markdown, with WeChat article cleanup, selector fallbacks, truncation, and optional JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jllyzzd2023](https://clawhub.ai/user/jllyzzd2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve readable article, blog, news, and announcement body text from modern webpages for downstream summarization, analysis, or citation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetching external webpages can disclose requested URLs to remote servers and may retrieve untrusted content. <br>
Mitigation: Use only public, non-sensitive URLs; avoid private, internal, authenticated, localhost, or token-containing URLs. <br>
Risk: The release evidence states that referenced helper scripts are not included in the package. <br>
Mitigation: Review or provide the missing helper script and dependencies before allowing an agent to run web-fetch commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jllyzzd2023/clean-web-fetch) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON] <br>
**Output Format:** [Markdown body text by default, with optional JSON output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output may be truncated by the requested max_chars limit.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
