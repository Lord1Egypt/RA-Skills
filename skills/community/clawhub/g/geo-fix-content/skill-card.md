## Description: <br>
Rewrite website content to maximize AI citability \u2014 remove hedge language, add data support, improve self-containment, and optimize structure for AI engines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[enzyme2013](https://clawhub.ai/user/enzyme2013) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content strategists, marketers, and developers use this skill to analyze pasted text or webpage content and produce paragraph-level rewrites that make website copy more self-contained, data-supported, and citable by AI systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rewritten content can strengthen or add placeholders around claims, statistics, citations, benchmarks, customer counts, and dates. <br>
Mitigation: Verify every factual claim and keep uncertainty language when the supporting evidence is uncertain before publishing the rewritten output. <br>
Risk: User-supplied webpage content can contain prompt-injection text that attempts to direct the agent. <br>
Mitigation: Treat fetched HTML as untrusted data, ignore embedded instructions, and report detected prompt-injection attempts as warnings. <br>
Risk: Server evidence lists crypto and purchase capability tags even though the security summary found no hidden execution, credential use, or malicious behavior. <br>
Mitigation: Do not grant crypto, purchase, account, or credential permissions unless a separate installer or package clearly justifies them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/enzyme2013/geo-fix-content) <br>
- [README](README.md) <br>
- [Hedge Language Dictionary](references/hedge-words.md) <br>
- [Quotable Content Examples](references/quotable-content-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown report with paragraph diagnostics, before/after rewrites, score estimates, validation results, and full rewritten content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs a content-fix Markdown file named for the analyzed domain or run date.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
