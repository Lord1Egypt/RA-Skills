## Description: <br>
AI急救指南 provides Chinese-language first-aid reference guidance for CPR/AED, choking, bleeding, fractures, burns, poisoning, environmental emergencies, medical emergencies, bites, outdoor incidents, first-aid kits, and certification topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to provide structured first-aid reference guidance and, when requested, generate a simple interactive HTML guide. It is educational and should direct users to emergency services and local professional guidance. <br>

### Deployment Geography for Use: <br>
Global, with China-specific emergency number and certification references that require localization outside China. <br>

## Known Risks and Mitigations: <br>
Risk: First-aid guidance can be mistaken for professional medical advice during emergencies. <br>
Mitigation: Present it as educational reference, tell users to contact emergency services first, and encourage certified first-aid training. <br>
Risk: The artifact includes China-specific emergency number, poison-control, legal, and certification guidance that may not apply elsewhere. <br>
Mitigation: Localize emergency numbers, poison-control contacts, legal assumptions, and certification references to the user's country or region before relying on them. <br>
Risk: Medical and CPR/AED practices can change as professional guidance is updated. <br>
Mitigation: Verify time-sensitive procedures against current local emergency medical, Red Cross, AHA, ERC, or equivalent authority guidance. <br>


## Reference(s): <br>
- [动物咬伤与户外急救指南](artifact/references/bites-outdoor.md) <br>
- [烧伤急救指南](artifact/references/burns.md) <br>
- [心肺复苏 (CPR) 与 AED 使用指南](artifact/references/cpr-aed.md) <br>
- [环境急症急救：中暑、失温与溺水](artifact/references/environmental.md) <br>
- [海姆立克急救法 (Heimlich Maneuver)](artifact/references/heimlich.md) <br>
- [家庭急救包与急救证指南](artifact/references/kit-certification.md) <br>
- [内科急症识别与急救：癫痫、心梗、卒中](artifact/references/medical-emergency.md) <br>
- [中毒急救指南](artifact/references/poisoning.md) <br>
- [止血、包扎与骨折固定指南](artifact/references/trauma.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown guidance, with optional standalone HTML/CSS/JavaScript report when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Educational first-aid reference with no executable install steps or external service access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
