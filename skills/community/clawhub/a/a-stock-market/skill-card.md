## Description: <br>
Provides real-time A-share stock and index quotes from Tencent Finance using Shanghai and Shenzhen stock codes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ra1nzzz](https://clawhub.ai/user/ra1nzzz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to query current A-share stock and index quotes from the command line by providing Shanghai or Shenzhen stock symbols. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried stock symbols are sent to Tencent Finance when the skill retrieves quotes. <br>
Mitigation: Use the skill only when sending requested symbols to Tencent Finance is acceptable. <br>
Risk: The documented symlink installation writes a global command under /usr/local/bin. <br>
Mitigation: Run the Python script directly from the skill directory when a global command entry is not needed. <br>
Risk: Quotes depend on a free public finance endpoint and may be delayed, unavailable, or unsuitable for trading decisions. <br>
Mitigation: Verify market data with an authoritative financial source before acting on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ra1nzzz/a-stock-market) <br>
- [Publisher profile](https://clawhub.ai/user/ra1nzzz) <br>
- [Tencent Finance quote endpoint](https://qt.gtimg.cn/q={stock_code}) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text output with Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires one or more stock symbols prefixed with sh or sz; contacts Tencent Finance over HTTPS.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
