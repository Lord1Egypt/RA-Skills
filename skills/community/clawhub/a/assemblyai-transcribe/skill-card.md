## Description: <br>
Transcribe, diarise, translate, post-process, and structure audio/video with AssemblyAI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tristanmanchester](https://clawhub.ai/user/tristanmanchester) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run AssemblyAI transcription workflows, including diarisation, translation, transcript exports, speaker mapping, and structured transcript post-processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents with autonomous command execution could delete remote transcripts without an additional confirmation safeguard. <br>
Mitigation: Disable or restrict use of the delete command unless deletion is an intentional workflow requirement. <br>
Risk: Media, transcripts, and LLM prompts are sent to AssemblyAI services and may be sensitive. <br>
Mitigation: Process only content that is permitted to be sent to AssemblyAI and use a scoped AssemblyAI API key where possible. <br>
Risk: Base URL overrides can redirect requests away from the expected AssemblyAI endpoints. <br>
Mitigation: Avoid untrusted ASSEMBLYAI_BASE_URL and ASSEMBLYAI_LLM_BASE_URL values, and set the EU endpoints only when regional processing is required. <br>


## Reference(s): <br>
- [AssemblyAI Documentation](https://www.assemblyai.com/docs) <br>
- [Capabilities Reference](references/capabilities.md) <br>
- [Workflows and Recipes](references/workflows.md) <br>
- [Output Formats](references/output-formats.md) <br>
- [Speaker Mapping](references/speaker-mapping.md) <br>
- [LLM Gateway Notes](references/llm-gateway.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, plain text, SRT, VTT, manifest files, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write transcript bundles with Markdown, agent JSON, raw JSON, subtitle, paragraph, sentence, and manifest outputs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
