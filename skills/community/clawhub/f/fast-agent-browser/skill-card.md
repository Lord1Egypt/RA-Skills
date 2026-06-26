## Description: <br>
Python CLI tool for AI agents to automate web browsers with Playwright, supporting navigation, interaction, snapshots, screenshots, and form handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leohuang8688](https://clawhub.ai/user/leohuang8688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent builders use this skill to let agents drive browser workflows such as navigation, element interaction, screenshots, snapshots, form handling, and data extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad browser-control authority, including navigation, page interaction, screenshots, file upload, cookie or storage handling, and custom JavaScript execution. <br>
Mitigation: Use isolated browser profiles or test accounts, avoid sensitive sessions unless necessary, and require explicit confirmation before submissions, uploads, purchases, account changes, or custom JavaScript execution. <br>
Risk: Saved cookies, storage state, or persistent browser profiles can expose authenticated sessions if they are reused or shared casually. <br>
Mitigation: Store authentication state only when needed, restrict access to those files, and delete or rotate them after the task is complete. <br>
Risk: Server security evidence flags the release as suspicious because the browser-control surface is broad and the artifact makes overly broad safety claims. <br>
Mitigation: Review the skill before deployment, scan it in the target environment, and constrain use to workflows where browser automation authority is acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/leohuang8688/fast-agent-browser) <br>
- [README](artifact/README.md) <br>
- [API documentation](artifact/docs/api.md) <br>
- [Playwright](https://playwright.dev/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python examples, browser snapshots, screenshots, and text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local browser artifacts such as screenshots, PDFs, cookies, storage state, and uploaded-file interactions when the agent invokes those commands.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
