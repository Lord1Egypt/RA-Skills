## Description: <br>
Personalized fitness planning and workout accountability coach for beginners and intermediates. Use when users want a training plan, workout logging, progress check-ins, or practical fitness guidance with a supportive coaching style. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dexterqiu-collab](https://clawhub.ai/user/dexterqiu-collab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People seeking beginner or intermediate fitness support use this skill to request sustainable training plans, log workouts, review progress, and receive practical recovery or nutrition guidance. It is intended for general coaching and accountability, not medical diagnosis, rehabilitation, or clinical nutrition advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fitness profile and workout data may be saved by the optional Python prototype. <br>
Mitigation: Use the markdown skill for ordinary coaching, review local storage behavior before running the prototype, and avoid entering unnecessary sensitive health details. <br>
Risk: Optional Feishu sync can send workout or profile data to an external service when configured. <br>
Mitigation: Keep Feishu disabled unless external sync is intentional and credentials, destination tables, and data handling expectations have been reviewed. <br>
Risk: The included publishing script can push the repository to GitHub if executed intentionally. <br>
Mitigation: Do not run the GitHub publishing script unless publishing the repository is the intended action. <br>
Risk: General fitness coaching can be mistaken for medical, rehabilitation, or clinical nutrition advice. <br>
Mitigation: Keep advice conservative, avoid medical certainty, and direct users to qualified professionals for pain, injury, eating disorder risk, or other health concerns. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dexterqiu-collab/dexter-fitness-coach) <br>
- [Feishu Open API](https://open.feishu.cn/open-apis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown coaching responses with optional shell commands, Python examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize workouts, propose plans, and provide conservative safety notes based on user-provided context.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
