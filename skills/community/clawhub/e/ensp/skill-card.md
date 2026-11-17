## Description:

Generates native eNSP .topo topology files for Huawei network simulations from natural-language network design requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[forealmy](https://clawhub.ai/user/forealmy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, network engineers, and lab users use this skill to turn requested Huawei eNSP network simulations into ready-to-open .topo files with devices, links, labels, and area shapes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated .topo files are written to the working directory and could overwrite existing work if a filename is reused.

Mitigation: Review the target filename before writing and use a unique, descriptive .topo name.

Risk: The skill is specialized for Huawei eNSP topology files and may be inappropriate for generic network diagramming or non-eNSP simulation formats.

Mitigation: Use this skill for eNSP .topo generation only, and choose another diagramming workflow for other formats.

## Reference(s):

- [eNSP .topo File Format Reference](references/topo-reference.md)
- [Huawei eNSP Product Page](https://support.huawei.com/enterprise/en/cloud-computing/ensp-pid-21602604)

## Skill Output:

**Output Type(s):** [files, code, guidance]

**Output Format:** [Native .topo XML file plus a short text path for opening the result in eNSP]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes generated topology files to the working directory.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
