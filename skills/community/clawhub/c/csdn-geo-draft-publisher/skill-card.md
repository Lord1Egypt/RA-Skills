## Description: <br>
Turns structured AI-GEO source assets into CSDN-ready technical article drafts and can help fill a visible local CSDN editor for human review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ljseeking](https://clawhub.ai/user/ljseeking) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators, developers, and technical marketing teams use this skill to transform structured brand and product knowledge into CSDN-style tutorials, architecture explanations, summaries, tags, title options, code examples, and pre-publication checklists. Users may also run the included local Playwright example to fill a CSDN draft while keeping review, save, and publish actions under human control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate while the user is logged in to CSDN, so browser automation changes could affect an authenticated draft workflow. <br>
Mitigation: Run only in a visible local browser, keep login manual, do not save credentials or session state, and review the page before any save or publish action. <br>
Risk: Generated drafts may contain factual errors, overly promotional claims, unsafe examples, or unsuitable platform metadata. <br>
Mitigation: Use the generated publish checklist and manually verify facts, tone, code examples, tags, summary, and article formatting before publishing. <br>
Risk: Modified selectors or publishing-flow logic could weaken the intended manual-control boundary. <br>
Mitigation: Audit changes to the Playwright script against the safety rules and preserve the rule that final save or publish actions are performed by the user. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/ljseeking/csdn-geo-draft-publisher) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Description](artifact/SKILL.md) <br>
- [Automation Safety Rules](artifact/automation/safety_rules.md) <br>
- [Playwright Draft Flow](artifact/automation/playwright_draft_flow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, JSON status output, Python example code, shell command snippets, and human review checklists.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces CSDN article assets such as full drafts, markdown-ready content, titles, summaries, tags, code examples, publish checklists, and draft-fill status; publishing remains manual.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
