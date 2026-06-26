## Description: <br>
Deep Research Agent guides an agent through multi-source research, fact-checking, literature review, competitive analysis, and trend analysis with citations and confidence ratings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sharoonsharif](https://clawhub.ai/user/sharoonsharif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, analysts, and agents use this skill to plan and conduct multi-source research, literature reviews, competitive analyses, fact-checks, and trend analyses. It emphasizes source triangulation, confidence-rated findings, counterarguments, and citation-backed reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research topics and fetched sources may be sent through external search or fetch tools. <br>
Mitigation: Do not use the skill for confidential topics unless external lookup is acceptable for the use case. <br>
Risk: Deep and exhaustive runs may retain reports and an index under ~/research. <br>
Mitigation: Review retained files after use and remove ~/research reports manually when persistent history is not wanted. <br>
Risk: Research summaries can still include outdated, incomplete, or misleading conclusions. <br>
Mitigation: Review confidence ratings, source quality, counterarguments, and knowledge gaps before relying on the output for decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sharoonsharif/claw-researcher) <br>
- [Research methodology reference](references/methodology.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance, files] <br>
**Output Format:** [Markdown research plans and reports with inline citations; deep and exhaustive runs may save Markdown files plus an index.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes confidence ratings, source lists, methodology notes, counterarguments, knowledge gaps, and optional local report indexing under ~/research.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
