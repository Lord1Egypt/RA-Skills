## Description: <br>
Public-safe FitClaw coaching workflow covering onboarding, hydration, nutrition, and training structure. Use when demonstrating a reusable AI fitness coaching method without exposing private user data or live production configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BeAChanger](https://clawhub.ai/user/BeAChanger) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and AI fitness coaching builders use this skill to demonstrate a public-safe coaching method for onboarding, hydration, nutrition, and training structure without exposing private user data or live production configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may handle body metrics, nutrition habits, injuries, progress details, or other personal fitness information that could be retained by an agent with memory enabled. <br>
Mitigation: Check memory settings before use, share only information you are comfortable retaining, and clear or disable memory for session-only coaching. <br>
Risk: Fitness, hydration, nutrition, and training recommendations can be over-specific when baseline data is missing or uncertain. <br>
Mitigation: Label estimates clearly, ask only the next necessary clarifying questions, keep starting guidance conservative, and avoid presenting coaching estimates as medical prescriptions. <br>
Risk: Packaging or adapting the skill could expose private user data or operational material if sanitization is skipped. <br>
Mitigation: Apply the bundled public sanitization checklist and review the package before publication or reuse. <br>


## Reference(s): <br>
- [FitClaw Onboarding Public](references/fitclaw-onboarding-public.md) <br>
- [FitClaw Hydration Public](references/fitclaw-hydration-public.md) <br>
- [FitClaw Nutrition Public](references/fitclaw-nutrition-public.md) <br>
- [FitClaw Training Public](references/fitclaw-training-public.md) <br>
- [FitClaw Public Sanitization Checklist](templates/public-sanitization-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with structured coaching recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include practical estimates, intake questions, coaching next steps, and public-safe memory guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, created 2026-03-18) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
