## Description: <br>
Real-footage batch video production for TikTok/Instagram content matrix: AI script generation, TTS dubbing, footage matching, HyperFrames visual styles, QA, and social publishing automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[373246784-design](https://clawhub.ai/user/373246784-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and social media operators use this skill to turn owned real-footage libraries into scheduled TikTok and Instagram short videos across account matrices. It is aimed at batch production workflows that need script generation, voiceover, visual rendering, quality checks, and publishing support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may access social publishing accounts, Metricool tokens, local media libraries, and some OpenClaw credential or profile files. <br>
Mitigation: Run it with dedicated, least-privilege credentials and a dedicated workspace/configuration rather than broad personal or production accounts. <br>
Risk: The security summary flags under-disclosed host-level and credential-handling behavior. <br>
Mitigation: Review or remove host-level cleanup/proxy behavior before running the skill on a main machine, and prefer an isolated environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/373246784-design/clipmatrix) <br>
- [Workflow reference](references/WORKFLOW.md) <br>
- [Troubleshooting reference](references/TROUBLESHOOTING.md) <br>
- [DeepSeek platform](https://platform.deepseek.com) <br>
- [HyperFrames documentation](https://hyperframes.heygen.com/introduction) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python workflow scripts, configuration requirements, and generated media workflow artifacts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3, ffmpeg, node, a DEEPSEEK_API_KEY, a configured media library, and publishing credentials for full workflow use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
