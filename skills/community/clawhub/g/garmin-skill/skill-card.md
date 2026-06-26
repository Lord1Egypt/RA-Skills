## Description: <br>
Talk to your Garmin data - ask questions about your activities, training load, VO2 Max, heart rate zones, and more using AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nftechie](https://clawhub.ai/user/nftechie) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to let an agent query Garmin-derived training data through Transition, answer fitness questions, inspect performance metrics, retrieve or generate workouts, and push selected workouts to Garmin. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can involve personal fitness data and coaching prompts from Garmin-derived activity history. <br>
Mitigation: Install only if you trust Transition with this data, and review Transition's privacy and deletion practices before use. <br>
Risk: The Transition API key grants access to personalized Garmin-connected features. <br>
Mitigation: Keep TRANSITION_API_KEY private and avoid exposing it in shared logs, repositories, screenshots, or chat transcripts. <br>
Risk: The skill can push scheduled workouts to Garmin. <br>
Mitigation: Require explicit user confirmation before an agent pushes any workout to Garmin. <br>


## Reference(s): <br>
- [Garmin Skill on ClawHub](https://clawhub.ai/nftechie/garmin-skill) <br>
- [Transition](https://www.transition.fun) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with curl examples, natural-language answers, and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses TRANSITION_API_KEY for personalized Garmin data; the Workout of the Day endpoint can be used without authentication.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
