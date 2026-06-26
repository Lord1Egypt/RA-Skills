## Description: <br>
Drafts chemical compatibility groupings, storage plans, and warnings for laboratory inventory review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[theresayao0614-sudo](https://clawhub.ai/user/theresayao0614-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Laboratory staff, EHS reviewers, and developers use this skill to draft chemical storage groupings and compatibility warnings for inventory review. Results should be verified against SDS documents, institutional EHS rules, authoritative compatibility charts, and qualified safety personnel before real storage decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The simple local classifier can misclassify chemicals or miss specific incompatibilities. <br>
Mitigation: Verify every result against SDS documents, institutional EHS rules, authoritative compatibility charts, and qualified safety personnel. <br>
Risk: The skill overstates chemical safety and compliance readiness. <br>
Mitigation: Treat outputs as rough educational or inventory-drafting aids, not as the basis for real lab storage, inspections, relocation, or training. <br>
Risk: The skill can work with local inventory files despite claims of no file access. <br>
Mitigation: Review any file reads or writes the agent proposes before execution, especially when inventory files may contain sensitive operational data. <br>


## Reference(s): <br>
- [OSHA Chemical Storage Guidelines](https://www.osha.gov/chemical-storage) <br>
- [SDS Search (MSDSOnline)](https://www.msdsonline.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown and plain text with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include chemical storage groups, compatibility messages, warnings, storage-plan drafts, and local command examples.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
