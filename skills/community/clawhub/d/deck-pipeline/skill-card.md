## Description: <br>
Deck Pipeline helps an agent translate Chinese presentation decks into polished English, audit layout integrity, maintain glossary consistency, and produce handoff artifacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tinadu-ai](https://clawhub.ai/user/tinadu-ai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, employees, and developers use this skill to run a structured deck globalization or polish-only workflow for PowerPoint presentations, including translation, layout audit, bilingual Excel review, and session handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can read and modify local presentation and spreadsheet files. <br>
Mitigation: Run it on copies of important or confidential decks, confirm output paths before writes, and close PowerPoint or Excel before execution. <br>
Risk: Automated layout checks cannot fully render slides and may miss visual issues. <br>
Mitigation: Export the deck to PDF or images and review the relevant pages before relying on the final presentation. <br>
Risk: Translation, glossary, and numeric-magnitude choices can introduce business meaning errors. <br>
Mitigation: Review the bilingual diff workbook, confirm glossary decisions, and verify Chinese magnitude conversions before delivery. <br>


## Reference(s): <br>
- [Deck Pipeline release page](https://clawhub.ai/tinadu-ai/deck-pipeline) <br>
- [DeckGlobalizer upstream credit](https://clawhub.ai/tinadu-ai/deckglobalizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON edit batches, PowerPoint files, Excel workbooks, and handoff Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and modify local .pptx and .xlsx files; users should run on copies and verify generated decks before use.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
