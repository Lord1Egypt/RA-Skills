## Description: <br>
Reviews Elixir documentation for completeness, quality, and ExDoc best practices when auditing @moduledoc, @doc, @spec coverage, doctest correctness, and cross-reference usage in .ex files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review Elixir project documentation for missing or weak @moduledoc, @doc, @spec, @type, doctest, and ExDoc cross-reference coverage. It helps produce scoped, evidence-backed documentation findings before a report is finalized. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Doctest-failure findings may require running local project tests, which executes project code. <br>
Mitigation: Run mix test only with explicit user approval and cite the relevant test output when using it as evidence. <br>
Risk: Documentation findings can be misleading if they are based on snippets, incomplete function clauses, or inferred module intent. <br>
Mitigation: Lock the review scope, read the full surrounding definition, and include file-line evidence before reporting an issue. <br>


## Reference(s): <br>
- [Documentation Quality](artifact/references/doc-quality.md) <br>
- [Spec Coverage](artifact/references/spec-coverage.md) <br>
- [Elixir Docs Review on ClawHub](https://clawhub.ai/anderskev/elixir-docs-review) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Shell commands] <br>
**Output Format:** [Markdown review findings with file-line anchors, quoted documentation evidence, and optional shell command output references.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings should be scoped to exact .ex or .exs files or modules, based on full-context reading, and checked against the review-verification protocol before final reporting.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
