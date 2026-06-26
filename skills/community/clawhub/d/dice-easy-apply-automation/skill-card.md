## Description: <br>
Automate Dice.com Easy Apply searches and applications with Puppeteer/Chromium, resume and cover-letter uploads, remote-role filtering, and conservative application guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ralyodio](https://clawhub.ai/user/ralyodio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers or their agents use this skill to build and run a Dice Easy Apply workflow that searches remote software roles, attaches verified application documents, and reports submitted and skipped applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can submit real job applications and upload personal documents through a logged-in Dice account. <br>
Mitigation: Start with DRY_RUN=1, require explicit approval before final submission or batches, and verify the selected resume and cover-letter filenames before submitting. <br>
Risk: A persistent browser profile may reuse an authenticated Dice session. <br>
Mitigation: Use a dedicated Dice-only Chromium profile, do not store credentials in scripts or logs, and stop for CAPTCHA, MFA, suspicious-login, or identity-verification prompts. <br>
Risk: Automated form handling could encounter unknown required questions or facts the user cannot verify. <br>
Mitigation: Skip applications with unknown required questions, salary essays, relocation or travel requirements, or any prompt that would require fabricated information. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides browser automation, state files, dry runs, and human review checkpoints; it does not include credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
