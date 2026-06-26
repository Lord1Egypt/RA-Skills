## Description: <br>
Generate AI music and songs with Diffrythm, Tencent Song Generation via inference.sh CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okaris](https://clawhub.ai/user/okaris) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External creators, developers, and content teams use this skill to generate background music, songs with vocals, podcast intros, game soundtracks, jingles, and other AI-assisted audio through the inference.sh CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and runs an external CLI and uses a third-party music generation service. <br>
Mitigation: Install only after reviewing or trusting the inference.sh installer, and prefer the documented manual or package-manager installation path when stronger supply-chain control is needed. <br>
Risk: Prompts, lyrics, and creative material may be sent to an external provider and may affect account or billing state. <br>
Mitigation: Avoid submitting secrets, private lyrics, proprietary prompts, or unreleased creative material unless the provider handling and billing impact are acceptable. <br>


## Reference(s): <br>
- [Ai Music Generation ClawHub Page](https://clawhub.ai/okaris/ai-music-generation) <br>
- [inference.sh](https://inference.sh) <br>
- [Running Apps](https://inference.sh/docs/apps/running) <br>
- [Content Pipeline Example](https://inference.sh/docs/examples/content-pipeline) <br>
- [Apps Overview](https://inference.sh/docs/apps/overview) <br>
- [CLI Checksums](https://dist.inference.sh/cli/checksums.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands invoke external inference.sh audio-generation apps and may create generated audio through that service.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
