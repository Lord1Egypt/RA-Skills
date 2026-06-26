## Description: <br>
Draft SOAP clinical notes, generate Medicare MBS item number reference tables, write patient recall SMS and email templates, and produce GP report letters for Australian allied health practitioners including physiotherapy, OT, psychology, speech pathology, and podiatry. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arbazex](https://clawhub.ai/user/arbazex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Australian allied health practitioners and practice staff use this skill to draft clinical documentation, Medicare item number reference tables, recall messages, and GP report letters for review before use in patient records or billing workflows. <br>

### Deployment Geography for Use: <br>
Australia <br>

## Known Risks and Mitigations: <br>
Risk: Generated clinical notes could contain incorrect clinical facts, placeholders, or patient identifiers. <br>
Mitigation: Require a qualified practitioner to check every generated note against the actual patient file before it is copied into a clinical record. <br>
Risk: Medicare item numbers, rebates, session counts, and eligibility rules may be wrong or out of date. <br>
Mitigation: Verify all billing details against MBS Online, HPOS, Services Australia, and the current referral before billing. <br>
Risk: Broad healthcare triggers may cause the skill to respond in contexts that need clinical, legal, or billing expertise. <br>
Mitigation: Use the skill only as a drafting and reference aid for qualified Australian allied health workflows, and escalate clinical decisions, legal questions, and billing disputes to the appropriate professional or authority. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/arbazex/au-allied-health-notes-recall) <br>
- [MBS Online](https://www.mbsonline.gov.au) <br>
- [Services Australia - Medicare Benefits Schedule](https://www.servicesaustralia.gov.au/medicare-benefits-schedule-mbs) <br>
- [AHPRA - Managing health records](https://www.ahpra.gov.au/Resources/Managing-health-records.aspx) <br>
- [Services Australia - Allied health referrals for GP chronic condition management plans](https://www.servicesaustralia.gov.au/allied-health-and-other-primary-health-care-referrals-for-gp-chronic-condition-management-plans) <br>
- [Australian Government Department of Health - Better Access initiative](https://www.health.gov.au/topics/mental-health-and-suicide-prevention/what-were-doing/better-access-initiative) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Configuration instructions] <br>
**Output Format:** [Markdown with tables, templates, checklists, and short message drafts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No external API calls; generated clinical and billing content must be checked against official sources and the patient file before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
