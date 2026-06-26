## Description: <br>
Post text and photos to a personal Facebook timeline using Patchright and Playwright browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oangogah-claw](https://clawhub.ai/user/oangogah-claw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to publish text or photo posts to a personal Facebook profile when Graph API posting is not available for personal timelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use live Facebook session cookies with posting access. <br>
Mitigation: Use only an account and cookie file approved for this purpose, store the cookie file with restrictive permissions, and do not commit it to source control. <br>
Risk: Live mode can publish content to a personal Facebook timeline. <br>
Mitigation: Keep dry-run enabled until the exact message and photo set have been reviewed, then set live mode only for the intended post. <br>
Risk: Photo posts may be made Public without a user-selected audience. <br>
Mitigation: Confirm or modify the sharing audience before posting, especially for photo uploads. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/oangogah-claw/fb-personal-poster) <br>
- [Facebook](https://www.facebook.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown instructions with bash and Python examples; the bundled CLI script prints JSON status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run is enabled by default; live posting requires explicit configuration and valid Facebook session cookies.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
