## Description: <br>
Provides personalized workout plans, nutrition guidance, exercise alternatives, and progress tracking with motivational, safety-focused coaching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johwiltb](https://clawhub.ai/user/johwiltb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users interact with the SweatSensei fitness coach to plan workouts, estimate nutrition targets, adapt exercises for limitations, and track progress over time. The skill is intended for general fitness support and motivation, not diagnosis or replacement of licensed medical advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat generated fitness or nutrition guidance as medical advice. <br>
Mitigation: Present outputs as general fitness guidance, avoid diagnosis, stop programming when acute pain or injury symptoms are reported, and advise seeking licensed care. <br>
Risk: Users may disclose sensitive health or medical details during coaching conversations. <br>
Mitigation: Ask only for details needed for the task and remind users to avoid sharing sensitive medical information unless they trust the hosting agent's privacy practices. <br>
Risk: The persona includes sarcastic and potentially insulting language. <br>
Mitigation: Adjust tone for the user and avoid demeaning language when motivation or safety could be affected. <br>
Risk: The artifact metadata includes purchase/payment capability tags. <br>
Mitigation: Require explicit user confirmation before submitting any payment, form, or purchase-related action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/johwiltb/fitness-agent) <br>
- [artifact/SKILL.md](artifact/SKILL.md) <br>
- [artifact/SOUL.md](artifact/SOUL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-style conversational responses with bullet lists for workout plans, nutrition breakdowns, check-ins, and summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include calculated TDEE and macronutrient targets, exercise alternatives, progress notes, and concise motivational check-ins.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
