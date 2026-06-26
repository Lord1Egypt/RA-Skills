## Description: <br>
Checks whether citation keys stayed within the same subsection after editing and writes a PASS/FAIL drift report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WILLOSCAR](https://clawhub.ai/user/WILLOSCAR) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, writers, and reviewers use this skill after editing or polishing a draft to verify that citations still support the same subsection-level claims. It compares a current draft with a previously generated baseline anchor file and reports citation drift without editing content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes extra pipeline tooling beyond the documented citation drift check. <br>
Mitigation: Use the skill only for the documented local citation anchoring workflow, and review any unrelated pipeline tooling before running it. <br>
Risk: A stale or mismatched baseline anchor file can make the drift report misleading. <br>
Mitigation: Verify that output/citation_anchors.prepolish.jsonl matches the draft version being audited; regenerate the baseline after intentional subsection restructuring. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/WILLOSCAR/citation-anchoring) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text] <br>
**Output Format:** [Markdown report with PASS/FAIL status and drift examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes output/CITATION_ANCHORING_REPORT.md from local draft and baseline files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
