## Description: <br>
Legal Risk Assistant supports first-pass China civil and labor legal triage by scanning contract risk, estimating litigation or labor-dispute costs, and drafting editable complaint, defense, and evidence-outline skeletons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, freelancers, and small businesses use this skill before formal lawyer review to structure common China civil and labor matters: contract risk screening, litigation-cost or compensation estimates, and legal document skeletons. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: User-provided legal documents and dispute facts may contain sensitive personal, financial, business, or case information. <br>
Mitigation: Use redacted or sample facts where possible, and avoid sharing IDs, bank details, addresses, trade secrets, and case numbers unless necessary. <br>
Risk: The skill may be mistaken for formal legal advice or a substitute for legal representation. <br>
Mitigation: Treat outputs as preliminary legal information only and have important matters reviewed by a qualified lawyer using the full facts and current local rules. <br>
Risk: Incomplete facts can produce misleading risk ratings, compensation estimates, or litigation-cost conclusions. <br>
Mitigation: Collect minimum necessary facts first, separate confirmed and missing facts, state assumptions, and prefer ranges or scenario tables when facts are uncertain. <br>
Risk: Generated complaint, defense, or evidence-outline skeletons may be used without adequate case-specific review. <br>
Mitigation: Use generated documents as editable first drafts and review jurisdiction, evidence, claims, and procedural requirements before filing or relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/ai-legal-assistant-pro) <br>
- [Contract risk patterns](references/risk-patterns.md) <br>
- [Contract type guides](references/contract-type-guides.md) <br>
- [Calculation formulas](references/calculation-formulas.md) <br>
- [Labor dispute scenarios](references/labor-dispute-scenarios.md) <br>
- [Labor compensation output template](references/labor-compensation-output-template.md) <br>
- [Litigation worth-it template](references/litigation-worth-it-template.md) <br>
- [Document skeletons](references/document-skeletons.md) <br>
- [Output acceptance criteria](references/output-acceptance-criteria.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured Markdown with tables, calculations, checklists, and editable legal-document skeletons] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes preliminary-information disclaimers, prompts for missing facts, and cost estimates that exclude lawyer fees and other incidental costs.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
