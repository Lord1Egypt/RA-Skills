## Description: <br>
Generate audiobooks, podcasts, or educational audio content on demand by drafting a script and converting approved text to MP3 audio with ElevenLabs text-to-speech. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Matttgx](https://clawhub.ai/user/Matttgx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create short-form narrated content such as audiobook chapters, podcast episodes, educational explanations, audio guides, and stories. The skill guides script drafting, user review, and MP3 generation through a dependent text-to-speech workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-influenced script text may be interpolated into a shell command without clear safe escaping. <br>
Mitigation: Review before installing and prefer passing generated script text through stdin or a temporary file instead of command interpolation. <br>
Risk: Generated scripts and audio are processed by external Anthropic and ElevenLabs services. <br>
Mitigation: Use limited API keys and avoid sensitive or proprietary content unless external processing is acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Matttgx/audio-gen-1-0-0) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/Matttgx) <br>
- [Skill homepage](https://github.com/clawdbot/clawdbot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown conversation with script text, shell command examples, and MEDIA token pointing to an MP3 file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces user-reviewed scripts and MP3 audio files; relies on ANTHROPIC_API_KEY, ELEVENLABS_API_KEY, and the sag skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
