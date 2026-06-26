## Description: <br>
DeepEvidence循证医学AI助手 uses the DeepEvidence OpenAI-compatible API to generate traceable evidence summaries for clinical questions, drug safety review, guideline interpretation, and trial evidence synthesis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cindy8753](https://clawhub.ai/user/cindy8753) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinicians, medical researchers, and developers use this skill to ask evidence-based medicine questions and receive structured, citation-preserving reference summaries. It is suited for clinical evidence review, medication safety checks, guideline interpretation, and app integrations that call DeepEvidence through an OpenAI-compatible interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Clinical questions and related context are sent to the DeepEvidence service. <br>
Mitigation: Avoid patient-identifying details unless privacy obligations allow it; use opaque user identifiers and minimize logging of prompts, responses, and request bodies. <br>
Risk: Medical evidence summaries may be incomplete, stale, or unsuitable for a specific patient. <br>
Mitigation: Treat outputs as reference material, preserve returned citations, and require verification by a qualified clinician before clinical use. <br>
Risk: The required DeepEvidence API key could be exposed through source control, logs, shell history, or error output. <br>
Mitigation: Read DEEPEVIDENCE_API_KEY only from environment configuration, do not commit keys, and avoid printing secrets or full sensitive payloads. <br>
Risk: The skill is not appropriate for emergency triage or urgent first-aid decisions. <br>
Mitigation: For urgent symptoms, direct users to local emergency services or immediate medical care instead of relying on generated guidance. <br>


## Reference(s): <br>
- [DeepEvidence homepage](https://deepevid.medsci.cn/) <br>
- [DeepEvidence API Reference](references/api_reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/cindy8753/deepevidence) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Structured Markdown reports with preserved citation markers; may also include Python/OpenAI SDK snippets, shell commands, and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include DeepEvidence attribution, returned conversation IDs, token usage metadata, references, uncertainty notes, and clinical-use disclaimers.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release metadata; artifact frontmatter says 1.5.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
