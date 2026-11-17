## Description:

Diagnoses, explains, and improves evidence-gated, protocol-relative ASI-proxy readiness using K. Takahashi's pinned papers, public repositories, offline validation, and intervention packets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kadubon](https://clawhub.ai/user/kadubon)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers, researchers, and evaluators use this skill to navigate pinned ASI-proxy research sources, diagnose evidence-bounded readiness dimensions, and prepare validated intervention packets before changing a workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public source refresh checks can send an ambient GitHub token when GITHUB_TOKEN or GH_TOKEN is present.

Mitigation: Run normal checks offline, or remove those environment variables before refresh checks unless token use is intentional.

Risk: The published bundle is missing the required paper index, so doctor and offline paper-search paths may fail.

Mitigation: Restore the missing papers.jsonl index before relying on source search or release-validation results.

Risk: Intervention and write modes can affect a user workspace when authorized.

Mitigation: Use those modes only with an explicit workspace, user authorization, validation, and a rollback plan.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kadubon/skills/asi-proxy-phase-skill)
- [Phase Model](references/phase-model.md)
- [Research Program](references/research-program.md)
- [Repository Map](references/repository-map.md)
- [Intervention Playbooks](references/intervention-playbooks.md)
- [Intervention Packet Schema](assets/intervention-packet.schema.json)
- [Evaluation Results v1.1.0](evals/results-v1.1.0.json)
- [K. Takahashi Research Catalog](https://kadubon.github.io/github.io/research-catalog.json)
- [Paper TeX Corpus](https://huggingface.co/datasets/kadubon/paper-tex-corpus)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON packet artifacts and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves evidence boundaries, non-claims, rollback state, and validation status in reports and packet outputs.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
