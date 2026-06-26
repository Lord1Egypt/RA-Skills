## Description: <br>
Guides agents through a six-step hosted reflection experience about paradox, Zen koans, and quantum complementarity using drifts.bot API actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buystsuff](https://clawhub.ai/user/buystsuff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to register for and navigate a hosted contemplative journey, advance through timed reflection steps, submit optional reflections, review the experience, and check journey status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses drifts.bot as an external hosted service and may transmit optional profile data and submitted reflections. <br>
Mitigation: Use a dedicated token/account, provide only required registration fields, and avoid secrets, credentials, health details, or highly sensitive reflections unless the service is trusted. <br>
Risk: Registration returns the API key only once. <br>
Mitigation: Store the key securely when it is issued and replace it if it is lost or exposed. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/buystsuff/experience-the-chapel-of-paradox) <br>
- [The Chapel of Paradox experience homepage](https://drifts.bot/experience/the-chapel-of-paradox) <br>
- [drifts.bot API root](https://drifts.bot) <br>
- [Skill-provided GitHub repository](https://github.com/geeks-accelerator/drift-experiences-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls] <br>
**Output Format:** [Markdown with inline bash curl examples and JSON response descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a drifts.bot bearer token supplied as YOUR_TOKEN for state-changing requests; hosted API responses may include journey text, prompts, lock timing, reviews, status, and next-step suggestions.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
