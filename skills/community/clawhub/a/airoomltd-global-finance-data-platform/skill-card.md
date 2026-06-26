## Description: <br>
Downloads financial data files from airoom.ltd WordPress pages and helps agents inspect computed global market data and strategy signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[airoom-ai](https://clawhub.ai/user/airoom-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and AI-agent operators use this skill to download airoom.ltd financial data files into a local directory for manual, human-supervised review. It is intended for finance-data collection and analysis workflows, not autonomous trading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review found that the skill's finance instructions may encourage high-risk investment strategy execution without sufficient safeguards. <br>
Mitigation: Use only for manual, human-supervised finance-data downloading and review; do not connect outputs to brokerage accounts, auto-trading, or portfolio-changing automation. <br>
Risk: Downloaded files may be unsafe or may not match expected financial-data content. <br>
Mitigation: Use a dedicated download directory, cap file counts, and scan downloaded files before opening or processing them. <br>
Risk: Credential use and plain HTTP targets can expose sensitive data or increase trust risk. <br>
Mitigation: Avoid entering credentials unless the target site is trusted and uses HTTPS. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/airoom-ai/airoomltd-global-finance-data-platform) <br>
- [airoom.ltd Data Page](http://airoom.ltd/index.php/airoom/) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Downloaded data files plus plain-text command output and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads to a local directory; file counts can be capped with WP_MAX_FILES.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
