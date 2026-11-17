## Description:

Abstract Logic Writer helps agents draft, critique, score, compare, and revise English academic abstracts for AI, systems, and computer science papers using symbolic discourse rules, lightweight ontology checks, and sentence-level constraints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhiweiwei-nami](https://clawhub.ai/user/zhiweiwei-nami)

### License/Terms of Use:

MIT

## Use Case:

Developers, researchers, and technical writers use this skill to turn paper notes or draft abstracts into logically ordered, ontology-aware abstracts and to lint or score alternative abstract fragments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional ontology downloader can fetch arbitrary network or local-file URLs.

Mitigation: Use only trusted HTTPS ontology sources, avoid untrusted or local-file URLs, and inspect downloaded or generated ontology files before reuse or publication.

Risk: Rule-based linting and scoring can miss domain-specific claims or overstate abstract quality.

Mitigation: Treat diagnostics and scores as review aids and check final abstracts against the source paper, evidence, and expert judgment.

## Reference(s):

- [Computable Rules for Abstract Construction](references/computable-rules.md)
- [Lexeme Typing and Selection Rules](references/lexeme-typing.md)
- [Domain Ontology Bootstrap and Download Workflow](references/ontology-bootstrap.md)
- [Negative Examples](references/negative-examples.md)
- [Source Abstract Corpus](references/source-abstract-corpus.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with optional plain-text abstracts, rule diagnostics, score summaries, and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create ontology_seed.json and ontology_seed.ttl when the optional ontology bootstrap script is run.]

## Skill Version(s):

0.1.1 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
