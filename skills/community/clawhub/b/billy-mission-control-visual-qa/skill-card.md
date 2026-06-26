## Description: <br>
Run Mission Control visual QA on SAPCONET over SSH using Puppeteer screenshots and basic DOM checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Highlander89](https://clawhub.ai/user/Highlander89) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to run read-only visual QA checks against authorized Mission Control pages on SAPCONET, collecting screenshots and basic DOM health signals for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects to a configured SAPCONET SSH target and inspects supplied Mission Control URLs. <br>
Mitigation: Run it only with authorization for the SSH account, host, and target pages; review SSH_TARGET, REMOTE_RUN_DIR, OUTPUT_DIR, and CHROMIUM_PATH before execution. <br>
Risk: Generated screenshots and DOM summaries may contain sensitive internal page content. <br>
Mitigation: Store outputs in an approved location, restrict access to the output directory, and handle screenshots according to the sensitivity of the inspected pages. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, JSON, files] <br>
**Output Format:** [Markdown guidance with shell commands; runtime output is a JSON summary and PNG screenshots.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires authorized SSH access to the configured SAPCONET host and a Puppeteer/Chromium runtime on that host.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
