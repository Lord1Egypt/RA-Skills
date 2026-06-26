## Description: <br>
Generates an in-scope citation budget report for each H3 subsection so research drafts can improve citation diversity and density without adding new facts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WILLOSCAR](https://clawhub.ai/user/WILLOSCAR) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and writing agents use this skill when a draft is under-cited or failing a unique-citation gate and they need a scope-safe plan for adding existing BibTeX keys. The skill reads the draft, outline, context packs, and bibliography, then writes a constraint-oriented citation budget report for later editing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes broad research pipeline tooling beyond the citation-budget helper. <br>
Mitigation: Install the full package only when that broader bundle is intended; otherwise use a trimmed package containing SKILL.md, scripts/run.py, and the minimal shared helpers needed for the report. <br>
Risk: Citation suggestions can be misused as padding or can drift outside the intended subsection scope. <br>
Mitigation: Apply suggestions only when the key exists in citations/ref.bib and is allowed by the H3 context packs, then review the resulting draft for unchanged claims and scope-safe placement. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/WILLOSCAR/citation-diversifier) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report written to output/CITATION_BUDGET_REPORT.md] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses existing workspace files and citation keys; default execution requires python3 or python.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; skill frontmatter reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
