## Description: <br>
Browser Automation Ultra helps agents turn logged-in browser workflows into reusable Playwright scripts that manage Chrome CDP access and simulate human-like interactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[swaylq](https://clawhub.ai/user/swaylq) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to automate browser workflows such as publishing content, reading inbox or comment data, and replying through an existing logged-in Chrome session. It is best suited for workflows that require a real browser and can be reviewed before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scripts can control an already logged-in browser profile and perform actions on real accounts. <br>
Mitigation: Use a separate browser profile or test accounts, and review each script before allowing it to run against production accounts. <br>
Risk: Example workflows can read private mail or comment data. <br>
Mitigation: Add redaction, dry-run, and explicit confirmation steps before exporting or processing account data. <br>
Risk: Publishing and reply examples may submit content without a final safety check. <br>
Mitigation: Require a preview or confirmation gate before posting, replying, or changing account-visible content. <br>
Risk: Anti-detection guidance may conflict with platform rules. <br>
Mitigation: Remove or ignore platform-evasion behavior that violates applicable terms, and use automation only where it is permitted. <br>


## Reference(s): <br>
- [Anti-detection reference](references/anti-detection.md) <br>
- [ClawHub skill page](https://clawhub.ai/swaylq/browser-automation-ultra) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Playwright scripts, browser lock commands, and troubleshooting steps for workflows that reuse an existing Chrome session.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
