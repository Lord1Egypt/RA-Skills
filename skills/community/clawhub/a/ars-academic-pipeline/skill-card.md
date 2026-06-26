## Description: <br>
Orchestrates a staged academic research-to-publication workflow with planning, research, drafting, review, revision, ethics, disclosure, formatting, and delivery checkpoints. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[andyrenxu7255](https://clawhub.ai/user/andyrenxu7255) <br>

### License/Terms of Use: <br>
CC BY-NC 4.0 <br>


## Use Case: <br>
Researchers, students, and academic teams use this skill to coordinate an AI-assisted manuscript pipeline from initial planning through research synthesis, drafting, review, revision, disclosure, formatting, and delivery. It is suited to structured academic workflow management where users want explicit checkpoints, integrity review, and resume support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can persist research session history, stage outputs, process records, and final packages locally. <br>
Mitigation: Use it only with material appropriate for the configured environment, decide where generated records should be stored, and remove or protect local outputs that contain confidential or unpublished work. <br>
Risk: Cross-model verification can send manuscript or research material to external AI providers when enabled. <br>
Mitigation: Disable ARS_CROSS_MODEL unless third-party verification is intended, and avoid using unpublished, regulated, or peer-review-sensitive material with external providers without approval. <br>
Risk: Generated academic guidance, references, and manuscript content may still contain mistakes despite the built-in review and integrity stages. <br>
Mitigation: Treat outputs as drafts, run the required integrity checks, and have qualified humans review claims, citations, ethics disclosures, and final submission materials before relying on them. <br>


## Reference(s): <br>
- [Attribution Notice](ATTRIBUTION.md) <br>
- [Original Academic Research Skills repository](https://github.com/Imbad0202/academic-research-skills) <br>
- [Pipeline state machine](references/pipeline_state_machine.md) <br>
- [Handoff schemas](shared/handoff_schemas.md) <br>
- [Integrity review protocol](references/integrity_review_protocol.md) <br>
- [Collaboration depth rubric](shared/collaboration_depth_rubric.md) <br>
- [Cross-model verification](shared/cross_model_verification.md) <br>
- [Wang and Zhang 2026 collaboration depth paper](https://doi.org/10.1186/s41239-026-00585-x) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown and structured text outputs, with optional local files for pipeline state, reports, and final publication packages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces stage-gated academic workflow artifacts and may store local session state for resume support.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
