## Description: <br>
Data Synthesis chunks CSV corpus text, uses one LLM interface to generate questions and answers, and writes JSONL training data for QA or fine-tuning workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erxiong0](https://clawhub.ai/user/erxiong0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to inspect CSV corpora and synthesize QA pairs from document or table text for dataset preparation. It supports dry-run validation and optional OpenAI-compatible LLM endpoints when approved for the input data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CSV content may contain personal, regulated, confidential, or proprietary text that could be sent to a configured LLM endpoint when API mode is enabled. <br>
Mitigation: Run dry-run mode first and enable DATA_SYNTHESIS_USE_API=1 only after confirming the CSV is approved for the chosen endpoint. <br>
Risk: Generated JSONL records may retain original text chunks, source fields, and model-generated answers that require handling as derived training data. <br>
Mitigation: Store outputs securely and review or clean the records before using them for downstream training or sharing. <br>
Risk: Question generation depends on model output that can fail JSON parsing or produce low-quality records. <br>
Mitigation: Review the reported errors and sample the JSONL output before treating the dataset as production-ready. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/erxiong0/data-synthesis) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSONL] <br>
**Output Format:** [Markdown guidance with shell commands and JSON/JSONL file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces CSV inspection JSON, synthesis statistics JSON, and JSONL QA records with chunk, question, answer, and source metadata fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
