## Description: <br>
Pre-generates and caches demo content before live presentations, calling configured AI, voice, and database APIs in advance to verify playback and identify coverage gaps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and demo teams use this skill to seed AI-generated story, narration, sound, and optional image content before hackathon demos, investor pitches, or other live presentations. It helps verify cached playback so the live demo does not depend on real-time generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow makes live calls to Mistral, ElevenLabs, optional Gemini, and Turso, which can incur cost and send demo prompts or generated content to external providers. <br>
Mitigation: Run it only with limited demo API keys, reviewed prompts and content, and provider accounts whose terms and cost limits are understood. <br>
Risk: Generated child-themed story and audio content is stored in an external Turso database, and cleanup or scoping expectations are incomplete. <br>
Mitigation: Use a dedicated demo database, avoid real child or personal data, verify the Turso endpoint before execution, and delete cached rows after the presentation. <br>
Risk: A live presentation can still fail if credentials, generated media, or cache contents do not match the intended demo flow. <br>
Mitigation: Run the checklist before presenting, verify all cached playback paths, and keep fallback content ready for cache misses. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nissan/demo-precacher) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured API keys and a verified demo database endpoint before running the included precache script.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
