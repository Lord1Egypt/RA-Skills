## Description: <br>
Big8 is an entertainment-focused Chinese metaphysics assistant for BaZi readings, face reading, feng shui image analysis, zodiac horoscopes, I Ching-style daily divination, and Chinese almanac guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kobenfang](https://clawhub.ai/user/kobenfang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Chinese-speaking users use this skill for entertainment-oriented fortune-telling, feng shui, face reading, horoscope, BaZi, divination, and almanac responses. Agents can route text, birth dates, and optional face or room images into the appropriate mode, call the bundled Python helper for structured calculations, and present concise Chinese readings and suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to submit face photos or room images for analysis, and the security summary flags unclear privacy claims about image processing and retention. <br>
Mitigation: Use it only when the runtime clearly explains where images are processed and whether they are retained; avoid uploading images of other people without consent. <br>
Risk: Face reading, feng shui, fortune-telling, zodiac, divination, and almanac outputs may be mistaken for authoritative personal guidance. <br>
Mitigation: Present readings as entertainment and cultural reference only, and do not rely on them for medical, legal, financial, or major life decisions. <br>
Risk: Birth dates, face images, and room photos can reveal sensitive personal information. <br>
Mitigation: Minimize submitted personal details, prefer non-identifying images where possible, and remove or redact unnecessary sensitive context before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kobenfang/big8) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown-formatted Chinese responses, with JSON returned by helper commands for BaZi, zodiac, divination, and almanac calculations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use user-provided birth date, time, optional gender, timezone or country, text questions, and optional face or room images; readings should remain entertainment-oriented and avoid medical, legal, or financial advice.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
