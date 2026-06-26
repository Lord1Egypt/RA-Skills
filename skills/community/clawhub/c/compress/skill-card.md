## Description: <br>
Compress text semantically with iterative validation, anchor checksums, and verified information preservation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and prompt authors use this skill to compress prompts, documentation, code, configuration, or conversation history while preserving critical facts through anchor extraction and reconstruction validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Semantic compression can omit or distort subtle information, especially at aggressive compression levels. <br>
Mitigation: Use L1-L2 for production work, keep original source text, and validate compressed output through reconstruction, anchor matching, and semantic diff checks. <br>
Risk: Compressed prompts or instructions may preserve wording less exactly than safety-critical, legal, financial, or medical content requires. <br>
Mitigation: Avoid using this skill for medical dosages, legal text, financial figures, safety-critical data, or other cases where exact wording and values are required. <br>
Risk: Manual shell examples can expose sensitive text if copied directly into unsafe temporary-file workflows. <br>
Mitigation: Treat shell snippets as examples, review them before use, and apply safer handling for sensitive inputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/compress) <br>
- [Compression levels](artifact/levels.md) <br>
- [Validation algorithm](artifact/validation.md) <br>
- [Format-specific compression](artifact/formats.md) <br>
- [Metrics and token budgeting](artifact/metrics.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with examples, compact text outputs, code snippets, shell command examples, and compression reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should include validation status, iteration count, anchor match rate, and confidence when compression is performed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
