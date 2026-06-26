## Description: <br>
Automates Midjourney Alpha image generation through an authenticated browser session, including prompt submission, V8-oriented prompt defaults, result collection, and local downloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Standed](https://clawhub.ai/user/Standed) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative operators use this skill to submit user-triggered Midjourney Alpha image jobs, refine prompts, collect generated assets, and run conservative batch workflows through a logged-in browser session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a logged-in Midjourney browser session and can depend on sensitive session cookies. <br>
Mitigation: Use a dedicated Chrome profile, keep MJ_COOKIE out of chats and repositories, and review environment files and logs before sharing them. <br>
Risk: Browser-control helpers can access data available to the authenticated session. <br>
Mitigation: Review helper scripts before live use and avoid running raw eval or fetch helpers directly unless their session access is understood. <br>
Risk: Automated generation can create accidental bursts, duplicate submits, or account-policy exposure if used without limits. <br>
Mitigation: Keep generation user-triggered, set explicit rate limits, and review output directories after each run. <br>


## Reference(s): <br>
- [Auto Midjourney ClawHub Listing](https://clawhub.ai/Standed/auto-midjourney) <br>
- [Midjourney Alpha](https://alpha.midjourney.com) <br>
- [API Notes](references/api-notes.md) <br>
- [Operating Model](references/operating-model.md) <br>
- [Prompt Craft](references/prompt-craft.md) <br>
- [System Requirements](references/system-requirements.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown status summaries with inline shell commands and JSON-producing helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May download generated image assets locally when the user enables result collection.] <br>

## Skill Version(s): <br>
0.1.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
