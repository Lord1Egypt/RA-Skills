## Description:

Supports China mainland client investigations and banker-grade analysis with guardrails for Chinese text accuracy, source hierarchy, raw-data snapshots, and financial-number provenance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackdark425](https://clawhub.ai/user/jackdark425)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and financial-services teams use this skill to investigate China-market public or private companies and produce banker-style memos, decks, spreadsheets, and provenance files while reducing Chinese text typo and fabricated-number risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials, unsafe network defaults, or broad subprocess environments may expose secrets or weaken execution controls.

Mitigation: Remove and rotate embedded Tushare credentials, require user-provided credentials, switch Tushare and CNINFO retrieval to HTTPS, preserve proxy policy unless explicitly overridden, and pass only required environment variables to subprocesses.

Risk: Unpinned npm dependencies can reduce reproducibility and increase supply-chain exposure.

Mitigation: Pin npm dependencies with a lockfile before using the deck-generation workflow.

Risk: The workflow writes raw corporate data snapshots and generated deliverables locally.

Mitigation: Run the workflow in a contained workspace and apply local data-handling controls to raw snapshots, analysis drafts, decks, and spreadsheets.

Risk: China-market financial analysis can include unsupported numbers if validation gates are skipped.

Mitigation: Use the provenance, raw-data, source-authenticity, slide, and document audit gates before delivery; flag unavailable data instead of inventing values.

Risk: Chinese text can be corrupted when generated through Unicode escape workflows.

Mitigation: Use UTF-8 literals and the bundled lexicon for key Chinese terms, then run the typo scanner before shipping generated decks or documents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jackdark425/skills/cn-client-investigation)
- [CN data sources guide](artifact/references/data-sources.md)
- [Chinese lexicon reference](artifact/references/cn-lexicon.js)
- [Typo-gated compile template](artifact/references/compile_with_typo_gate.template.js.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python and JavaScript snippets, and generated deliverable files when the workflow is run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local QA gates for provenance, source authenticity, typo scanning, raw-data snapshots, and slide or document audit before delivery.]

## Skill Version(s):

0.9.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
