## Description:

Generate images from ChatGPT using Playwright browser automation. Opens ChatGPT, sends prompts, waits for generation, and saves the resulting images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amian](https://clawhub.ai/user/amian)

### License/Terms of Use:


## Use Case:

Developers and content-production users can use this skill to automate ChatGPT image-generation prompts through a browser session and save generated images plus per-prompt results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and generated content are submitted through a logged-in ChatGPT browser session, which can expose sensitive or regulated input to that account's service context.

Mitigation: Avoid sensitive or regulated prompts unless account and organization policies allow it, and use an isolated browser profile or disposable workspace for stronger separation.

Risk: The workflow depends on Playwright and Chromium browser automation.

Mitigation: Install it only in a trusted environment and pin Playwright with a lockfile before routine use.

Risk: Browser UI automation may fail when ChatGPT page structure, availability, login state, or generation behavior changes.

Mitigation: Review the generated images and results.jsonl log, rerun failed prompts with the start index option, and keep the automation under operator supervision for important batches.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/amian/skills/chatgpt-image-generation)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown instructions with inline shell commands; generated PNG files and JSONL results when executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a prompt file containing either an array of prompts or an object with a prompts array.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
