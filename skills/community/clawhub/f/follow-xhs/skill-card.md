## Description: <br>
Xiaohongshu note search and content retrieval tool that helps users find target content, fetch note details, and generate structured analysis reports. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[champagne315](https://clawhub.ai/user/champagne315) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to search Xiaohongshu notes, retrieve note details, and produce structured content analysis reports from the results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled account-session data may expose or reuse an account-linked Xiaohongshu session. <br>
Mitigation: Delete the bundled web_session value before use, rotate it if it belongs to you, and prefer a separate low-risk account. <br>
Risk: Unofficial authenticated browser-style requests and fingerprinting may trigger platform rate limits, verification, or account controls. <br>
Mitigation: Use conservative request rates, avoid untrusted proxies, and expect manual verification or request failures. <br>
Risk: Unpinned Python dependencies can change behavior or introduce supply-chain risk. <br>
Mitigation: Pin and review dependencies before installation in a controlled environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/champagne315/follow-xhs) <br>
- [Artifact README](artifact/README.md) <br>
- [Xiaohongshu Web](https://www.xiaohongshu.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown, Analysis] <br>
**Output Format:** [Markdown with inline Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce structured analysis reports, configuration updates, and local command snippets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
