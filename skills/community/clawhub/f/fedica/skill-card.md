## Description: <br>
Compose and schedule cross-platform social posts on Fedica (X, LinkedIn, Threads, Mastodon, Bluesky) via agent-browser, including login, image upload, scheduling, character limits, and Fedica's UTC-only time display. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jkobject](https://clawhub.ai/user/jkobject) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and social media operators use this skill to guide an agent through Fedica's browser UI for composing, scheduling, verifying, editing, and rescheduling posts across connected social platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a logged-in Fedica account that publishes or schedules public social media posts. <br>
Mitigation: Review the exact post text, media, target platforms, and local scheduled time with the user before any publish, schedule, or update action. <br>
Risk: Fedica displays and accepts scheduled times in GMT+00, which can cause posts to be scheduled at the wrong local time. <br>
Mitigation: Convert the user's local time to UTC before scheduling, then re-verify the displayed scheduled time and restate the local time to the user. <br>
Risk: Using the browser workflow may require access to Fedica credentials or existing authenticated sessions. <br>
Mitigation: Use only the credential source the user explicitly chooses and avoid exposing broad local secret stores. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jkobject/fedica) <br>
- [Fedica](https://fedica.com) <br>
- [agent-browser](https://github.com/vercel-labs/agent-browser) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires agent-browser, a Fedica account with connected platforms, and explicit user confirmation before publishing or scheduling.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
