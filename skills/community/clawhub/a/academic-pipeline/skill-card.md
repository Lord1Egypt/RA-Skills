## Description: <br>
Orchestrates an academic research workflow from literature search through final manuscript by coordinating dependent research, writing, review, integrity-checking, and humanization skills with checkpoints and quality gates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eric-promax](https://clawhub.ai/user/eric-promax) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, researchers, and academic teams use this skill to coordinate an end-to-end paper workflow, including research handoff, drafting, integrity verification, peer review, revision, finalization, and process documentation. It is intended as an orchestrator for dependent skills rather than a standalone research, writing, or review engine. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Academic drafts, manuscript details, and session history may be shared with search or API tools during the workflow. <br>
Mitigation: Use only institution-approved tools for confidential work, remove unnecessary sensitive data before execution, and obtain consent from collaborators before processing shared materials. <br>
Risk: Process summaries may contain quotes, decisions, evaluations, and other collaboration history that could be sensitive if stored or shared broadly. <br>
Mitigation: Review and redact process records before distribution, and disable or narrow the process-summary stage when privacy or confidentiality obligations require it. <br>
Risk: De-AI or humanization stages may conflict with journal, institutional, or disclosure requirements. <br>
Mitigation: Skip or modify those stages when policy requires disclosure, and preserve an accurate record of AI assistance in the final submission materials. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/eric-promax/academic-pipeline) <br>
- [Pipeline State Machine](references/pipeline_state_machine.md) <br>
- [Integrity Review Protocol](references/integrity_review_protocol.md) <br>
- [Claim Verification Protocol](references/claim_verification_protocol.md) <br>
- [Plagiarism Detection Protocol](references/plagiarism_detection_protocol.md) <br>
- [AI Research Failure Mode Checklist](references/ai_research_failure_modes.md) <br>
- [External Review Protocol](references/external_review_protocol.md) <br>
- [Mode Advisor](references/mode_advisor.md) <br>
- [Process Summary Protocol](references/process_summary_protocol.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Files] <br>
**Output Format:** [Markdown with structured tables, status dashboards, review and integrity reports, handoff summaries, and finalization instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May coordinate paper drafts, revision roadmaps, integrity reports, final manuscript files, and process summaries through dependent skills.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 3.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
