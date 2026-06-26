## Description: <br>
Turns a judicial opinion into a structured IRAC case brief with facts, procedural posture, issues, rules, holding, separate-opinion summary, and unresolved-information flags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External law students, paralegals, and junior associates use this skill to turn supplied judicial opinions into study or work case briefs for class prep, research memos, moot court, or matter reading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may over-rely on a generated brief as legal advice or as an authoritative substitute for the original opinion. <br>
Mitigation: The skill labels the output as a draft study/work aid and directs users to verify quotations and citations against the official reporter. <br>
Risk: Matter-reading use could expose confidential client-identifying information if users paste unnecessary details. <br>
Mitigation: The skill instructs users not to store, transmit, or include client-identifying information and to redact names and identifiers when summarizing. <br>
Risk: Partial or missing opinion text can produce an incomplete brief, especially for separate opinions or pinpoint citations. <br>
Mitigation: The skill accepts incomplete materials only with explicit unresolved-information flags and asks users to confirm the source summary before drafting. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown case brief draft with labeled sections and unresolved-information notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-supplied opinion text and source-summary confirmation before drafting.] <br>

## Skill Version(s): <br>
0.5.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
