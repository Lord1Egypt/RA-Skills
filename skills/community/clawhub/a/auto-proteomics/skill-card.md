## Description:

Public OpenClaw skill for low-token routing and downstream analysis of processed DDA LFQ proteomics inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billwanttobetop](https://clawhub.ai/user/billwanttobetop)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route eligible processed DDA LFQ proteomics requests into a file-driven two-group downstream analysis workflow that produces normalized matrices, QC outputs, differential protein tables, reports, and run manifests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled release tooling contains an under-scoped recursive delete path.

Mitigation: Use the public DDA LFQ workflow only unless the release helper scripts have been reviewed or patched to restrict deletion to a managed staging directory.

Risk: Router setup depends on PyYAML in the local Python environment.

Mitigation: Use an isolated Python environment and pin PyYAML before running the routing helper.

Risk: The artifact includes scaffold and prototype routes that are not part of the public release promise.

Mitigation: Recommend only the shipped dda-lfq-processed workflow for eligible processed DDA LFQ requests and keep DIA, raw-identification, phosphoproteomics, enrichment, and multi-omics paths at planning or internal-prototype level.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/billwanttobetop/skills/auto-proteomics)
- [Runtime Requirements](artifact/references/RUNTIME_REQUIREMENTS.md)
- [Workflow Index](artifact/references/WORKFLOW_INDEX.yaml)
- [Demo Input Guide](artifact/references/DEMO_INPUT_GUIDE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated workflow files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The shipped workflow is limited to processed DDA LFQ protein-level tables and one group-a versus group-b comparison.]

## Skill Version(s):

0.2.1 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
