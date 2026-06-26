## Description: <br>
Track dog health, walks, training, routines, travel, and vet coordination with species-aware memory and emergency triage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and caretakers use this skill to coordinate real-world dog care, including symptom triage, walk and routine tracking, training progress, behavior notes, travel preparation, vet logistics, and optional local records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store sensitive household, veterinary, medication, microchip, insurance, sitter, and dog-care details in local files. <br>
Mitigation: Install only if local dog-care memory is desired, approve storage explicitly, and keep only details the user is comfortable storing in ~/dog/. <br>
Risk: Casual dog mentions may activate care workflows if the activation preference is broad. <br>
Mitigation: Choose explicit or dog-specific activation during setup when casual dog mentions should not trigger the skill. <br>
Risk: Dog health and behavior guidance can be mistaken for diagnosis or emergency care. <br>
Mitigation: Use the skill's conservative triage posture, escalate emergency red flags to veterinary care, and do not rely on chat for definitive diagnosis or medication dosing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/dog) <br>
- [Skill Homepage](https://clawic.com/skills/dog) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with optional inline shell commands and local file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local records under ~/dog/ only with user approval; does not make external network requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
