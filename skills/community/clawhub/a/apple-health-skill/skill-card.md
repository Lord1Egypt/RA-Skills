## Description: <br>
Talk to your Apple Health data - ask questions about your workouts, heart rate, activity rings, and fitness trends using AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nftechie](https://clawhub.ai/user/nftechie) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agent developers use this skill to connect an AI assistant to Transition APIs for Apple Health-derived workout history, activity, heart rate, performance metrics, and coach chat workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends sensitive Apple Health-derived fitness data, profile information, and coach messages to Transition's external service. <br>
Mitigation: Install only when that data sharing is acceptable, review Transition privacy and deletion controls, and avoid sending unnecessary medical or personal details. <br>
Risk: Authenticated endpoints rely on a Transition API key that can expose personal fitness data if mishandled. <br>
Mitigation: Store the API key outside source files, avoid logging it, and rotate or revoke it if it may have been exposed. <br>


## Reference(s): <br>
- [Apple Health Skill on ClawHub](https://clawhub.ai/nftechie/apple-health-skill) <br>
- [Transition](https://www.transition.fun) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and HTTP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses TRANSITION_API_KEY for authenticated Transition API requests; the workout-of-the-day endpoint can be used without authentication.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
