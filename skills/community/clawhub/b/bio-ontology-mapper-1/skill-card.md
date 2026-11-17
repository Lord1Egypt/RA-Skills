## Description:

Maps biomedical terms from unstructured text to SNOMED CT and MeSH concepts using local reference data and optional UMLS or MeSH API lookups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data integration teams, and biomedical analysts use this skill to map clinical or scientific terms to ontology identifiers, inspect confidence scores, and produce reviewable JSON or text outputs. Mappings require domain review before use in clinical or other high-stakes workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented scope and install dependencies are not cleanly aligned with the shipped artifact.

Mitigation: Review the artifact before installation, prefer running the script without installing requirements, and remove unnecessary dependency entries before deployment.

Risk: Sensitive clinical text could be sent to external ontology APIs when API mode is enabled.

Mitigation: Use local-only mode for sensitive text; if API mode is necessary, de-identify inputs first and provide the UMLS key through an environment variable rather than a command-line argument.

Risk: Biomedical ontology mappings can be ambiguous, outdated, or falsely high-confidence.

Mitigation: Review low-confidence and top candidate mappings, track ontology versions where relevant, and require domain expert validation for clinical or other high-stakes use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/bio-ontology-mapper-1)
- [UMLS UTS API](https://uts-ws.nlm.nih.gov/rest)
- [MeSH API](https://id.nlm.nih.gov/mesh)
- [snomed_sample.json](references/snomed_sample.json)
- [mesh_sample.json](references/mesh_sample.json)
- [synonyms.json](references/synonyms.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON or text mapping output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include confidence scores, ontology identifiers, source labels, and API status fields.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
