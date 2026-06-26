## Description: <br>
CBT-based therapy for anxiety, depression, stress, and trauma. Provides structured cognitive behavioral therapy using Beck's model with validated clinical assessments (GAD-7, PHQ-9, DASS-21, PCL-5). Includes crisis detection, thought records, differential diagnosis, and session tracking. Activate with "therapy mode", "fearbot", or "start therapy". <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Samoppakiks](https://clawhub.ai/user/Samoppakiks) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users use FearBot through an OpenClaw agent for structured CBT-style support around mild-to-moderate anxiety, depression, stress, and trauma. It guides assessments, thought records, session continuity, homework, and crisis escalation prompts while reminding users to seek licensed care for serious or urgent needs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive mental-health history and monitors for crisis signals. <br>
Mitigation: Install only where the user is comfortable with that scope, and treat the skill as support rather than a substitute for licensed professionals or emergency services. <br>
Risk: Local therapy records and plaintext exports may expose private information on shared or synced machines. <br>
Mitigation: Review the local database and export locations before use, restrict access to the machine, and avoid exporting unless the user intentionally needs a shareable record. <br>
Risk: The skill may be used during urgent or serious mental-health situations beyond its intended support role. <br>
Mitigation: Follow the included crisis resources and professional referral prompts, and rely on local emergency services or qualified clinicians for urgent or severe concerns. <br>


## Reference(s): <br>
- [ClawHub FearBot release](https://clawhub.ai/Samoppakiks/fearbot) <br>
- [Assessment Administration Prompts](references/assessment-items.md) <br>
- [Crisis Detection & Response Layer](references/crisis-layer.md) <br>
- [Session Context Assembly Template](references/session-context-template.md) <br>
- [Base Therapist System Prompt](references/therapist-prompt.md) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [International Association for Suicide Prevention crisis centres](https://www.iasp.info/resources/Crisis_Centres/) <br>
- [Befrienders Worldwide](https://www.befrienders.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Files] <br>
**Output Format:** [Conversational guidance with local database records and optional Markdown exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores therapy session data locally and can export plaintext Markdown summaries on request.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
