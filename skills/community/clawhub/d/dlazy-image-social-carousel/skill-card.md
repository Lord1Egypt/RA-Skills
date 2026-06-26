## Description: <br>
A structured workflow skill dedicated to social-media carousel design. The core method is 'decide intent first, then execute,' using a 'single-confirmation + cover-first' two-phase flow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to plan and generate social-media carousel image sets with a confirmed direction, a cover-first review loop, and consistent remaining slides. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, local media paths, and uploaded assets may be sent to dLazy cloud endpoints for generation. <br>
Mitigation: Avoid submitting confidential images, unreleased campaign assets, or sensitive credentials unless the user trusts the provider and its service terms. <br>
Risk: The recommended CLI installation uses @latest, which can change the installed tool version over time. <br>
Mitigation: Review the @dlazy/cli package or source before installation, and prefer npx for per-run use when persistent global tooling is not desired. <br>
Risk: The skill requires a dLazy API key stored in CLI configuration or supplied through an environment variable. <br>
Mitigation: Use the provider's login or auth flow, keep credentials out of prompts and generated content, and rotate or revoke keys from the dLazy dashboard when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/image-social-carousel) <br>
- [dLazy CLI source](https://github.com/dlazyai/cli) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>
- [dLazy homepage](https://dlazy.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated image URLs returned by the dLazy service.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
