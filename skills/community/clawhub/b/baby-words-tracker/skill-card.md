## Description: <br>
Baby Words Tracker helps parents record, classify, deduplicate, and summarize a child's spoken words across Mandarin, Cantonese, English, and other languages, with optional Feishu document sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suiclaw](https://clawhub.ai/user/suiclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Parents and caregivers use this skill to log new baby words, classify them by language and word length, track vocabulary growth, and generate short progress summaries. It is intended for ongoing personal language-development record keeping. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a child's vocabulary history, name or birth-date metadata, and progress records over time. <br>
Mitigation: Use only the minimum child metadata needed, restrict access to the local JSON database, and delete or archive records when they are no longer needed. <br>
Risk: Feishu sync can move child language records into a cloud document with separate sharing permissions. <br>
Mitigation: Use a dedicated Feishu document with limited sharing, confirm the receiving account, and review document permissions before enabling sync. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/suiclaw/baby-words-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown summaries with structured JSON-backed records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update a local baby-words database and, when configured, synchronize records to Feishu.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
