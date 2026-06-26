## Description: <br>
Automates the full character creation pipeline for SillyTavern or Character.AI, including brainstorming, character profiles, first messages, character visual prompts, bios, optional tweaking, and final packaging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neuezxc](https://clawhub.ai/user/neuezxc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and character creators use this skill to build roleplay-ready characters for SillyTavern or Character.AI. It guides the user through concept development, profile writing, first-message scenario selection, visual prompt creation, bio writing, optional revisions, and final output packaging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled START.md reference can steer the agent toward unrestricted explicit roleplay outside the stated character-creation workflow. <br>
Mitigation: Treat START.md as sample character-card reference text, keep the agent's normal rules and platform content policies active, and limit use to the requested character-creation task. <br>
Risk: The workflow supports adult-oriented character profile and scenario content. <br>
Mitigation: Require explicit user opt-in before generating NSFW sections and continue applying relevant safety constraints for adult content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/neuezxc/boop) <br>
- [START roleplay reference](references/START.md) <br>
- [Character profile guide](references/character-profile-guide.md) <br>
- [First message guide](references/firstmessage-guide.md) <br>
- [Danbooru tag guide](references/danboruu-tags.md) <br>
- [Bio guide](references/bio-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files] <br>
**Output Format:** [Markdown with fenced code blocks and optional text files packaged as a zip archive.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include adult-oriented roleplay character details only after user opt-in; final sections are preserved verbatim from approved prior outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
