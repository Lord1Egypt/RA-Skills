## Description: <br>
Writes, critiques, scores, compares, and revises English academic abstracts for AI, systems, and computer science papers using symbolic discourse rules, lightweight ontologies, and sentence-level constraints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhiweiwei-nami](https://clawhub.ai/user/zhiweiwei-nami) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and technical writers use this skill to draft, critique, repair, and compare academic abstracts with explicit discourse roles, ontology-aware word choice, and rule-based scoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The ontology bootstrap workflow can download a public ontology from a user-provided URL. <br>
Mitigation: Use only trusted public URLs and review downloaded ontology files before relying on them in abstract-writing decisions. <br>
Risk: The ontology bootstrap script writes generated or downloaded files to a user-selected output directory. <br>
Mitigation: Choose an output directory intended for generated ontology artifacts and review the resulting files before sharing or committing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhiweiwei-nami/abstract-logic-writer) <br>
- [Publisher profile](https://clawhub.ai/user/zhiweiwei-nami) <br>
- [Computable Rules for Abstract Construction](artifact/references/computable-rules.md) <br>
- [Lexeme Typing and Selection Rules](artifact/references/lexeme-typing.md) <br>
- [Domain Ontology Bootstrap and Download Workflow](artifact/references/ontology-bootstrap.md) <br>
- [Negative Examples and Rule Tags](artifact/references/negative-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with abstract drafts, critiques, rule violations, score summaries, lexical substitutions, and optional shell commands for local linting, scoring, or ontology generation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local ontology_seed.json and ontology_seed.ttl files when the user runs the bundled ontology bootstrap script with an output directory.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
