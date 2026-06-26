## Description: <br>
Generates native eNSP .topo topology files for Huawei network simulations from natural-language topology requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[forealmy](https://clawhub.ai/user/forealmy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, network engineers, instructors, and students use this skill to turn requested Huawei eNSP network designs into ready-to-open .topo files with devices, links, labels, and layout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated .topo files may contain incorrect topology, interface, Cloud, IP, or UDP port settings. <br>
Mitigation: Review the generated .topo file before opening it in eNSP, especially when prompts include Cloud, IP, UDP port, or interface settings. <br>
Risk: The skill writes a new topology file in the active workspace. <br>
Mitigation: Use a workspace where creating a .topo file is acceptable and choose a clear filename. <br>


## Reference(s): <br>
- [eNSP .topo File Format Reference](references/topo-reference.md) <br>
- [Huawei eNSP Support Page](https://support.huawei.com/enterprise/en/cloud-computing/ensp-pid-21602604) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Code, Guidance] <br>
**Output Format:** [eNSP .topo XML file with a brief Markdown path note] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates user-requested topology files in the current workspace.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
