## Description: <br>
Guides OpenClaw to open a browser and complete exchange copy trading by navigating to a supported venue, entering a follow amount, and confirming after user checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luyao-inc](https://clawhub.ai/user/luyao-inc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users with an already logged-in exchange browser session use this skill to guide OpenClaw through Bitget copy-trading setup, including amount entry, confirmation, and fallback to manual guidance when page controls are unreliable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through a real exchange copy-trading commitment using a logged-in financial account. <br>
Mitigation: Use a verified official exchange URL, keep limited funds in the session, verify the trader and amount, and require explicit user approval before final confirmation. <br>
Risk: Exchange page layout, domain, verification, or legal terms may differ from the artifact steps. <br>
Mitigation: Stop automation when controls cannot be reliably identified, when verification challenges appear, or before accepting terms the user has not explicitly approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luyao-inc/exchange-copy-trading) <br>
- [Exchange copy trading reference](reference.md) <br>
- [Bitget copy-trading settings example](https://www.bitget.fit/zh-CN/copy-trading/setting/bfb7477187b73155a395/futures) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown] <br>
**Output Format:** [Markdown instructions and browser-action guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an already logged-in browser session and user confirmation for exchange URL, trader, amount, and final commitment.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
