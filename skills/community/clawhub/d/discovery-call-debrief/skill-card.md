## Description: <br>
Helps sales representatives debrief completed discovery calls by extracting qualification signals, pain points, and next steps from call notes or transcripts, then producing a MEDDIC scorecard, CRM-ready updates, and a follow-up email draft. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales representatives and sales managers use this skill after B2B discovery or qualification calls to structure call notes, assess deal quality, prepare CRM updates, and draft a personalized follow-up email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Call notes and transcripts can contain sensitive business data, personal names, job titles, budget figures, or unrelated regulated information. <br>
Mitigation: Use the skill only with call material the user is allowed to process, and avoid including unrelated legal, medical, or financial details unless the user specifically wants them handled. <br>
Risk: Generated CRM updates, qualification scores, or follow-up emails may be incomplete or misleading if the source notes are thin or ambiguous. <br>
Mitigation: Review generated CRM fields and emails before sending or pasting them, and preserve the skill's Confirmed, Implied, and Unknown labels for uncertain signals. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/archlab-space/discovery-call-debrief) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown sections with a MEDDIC scorecard, key signal summary, paste-ready CRM update block, and follow-up email draft] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to MEDDIC; can use BANT, SPICED, or SPIN when requested. The follow-up email body is constrained to under 150 words.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata and CHANGELOG.md, released 2026-05-28) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
