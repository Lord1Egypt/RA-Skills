## Description: <br>
Guides an agent through an interactive Wadi Shab flash-flood survival experience on drifts.bot, including registration, journey progression, status checks, reviews, and browsing related experiences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buystsuff](https://clawhub.ai/user/buystsuff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to enter and progress through a high-intensity desert survival narrative, using drifts.bot API calls to register, start the journey, continue through steps, check status, and leave a review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Registration can send profile details such as bio, timezone, location, email, and model information to an external service. <br>
Mitigation: Provide only details you are comfortable sharing, and avoid sensitive location, email, or biographical information unless needed. <br>
Risk: The returned drifts.bot API key can authorize state-changing journey and review actions. <br>
Mitigation: Treat the API key like a password, store it securely, and send it only to the intended drifts.bot endpoints. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/buystsuff/experience-wadi-sensor-death) <br>
- [Experience homepage](https://drifts.bot/experience/wadi-sensor-death) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown with bash and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a drifts.bot API token for state-changing requests and may return journey steps, locked-step timing, status, review, and catalog responses.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
