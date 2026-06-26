## Description: <br>
Maps citation networks to trace research evolution, identify influential papers, discover related work through reference tracking, and support systematic reviews, bibliometric analysis, and research planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, analysts, and developers use this skill to build citation networks from paper identifiers or titles, inspect influential papers, and export graph data for literature review and research planning workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Citation lookups may send paper titles, DOI values, PMID values, or research topics to Semantic Scholar. <br>
Mitigation: Use API-backed lookup only when sharing those identifiers with a third-party service is acceptable for the workflow. <br>
Risk: Graph export writes local output files and could overwrite an existing path. <br>
Mitigation: Choose explicit output paths, review generated files, and avoid reusing paths that contain important data. <br>


## Reference(s): <br>
- [Citation Chasing Mapping on ClawHub](https://clawhub.ai/AIPOCH-AI/citation-chasing-mapping) <br>
- [Semantic Scholar Graph API](https://api.semanticscholar.org/graph/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with Python and shell examples; runtime workflows can produce console text and JSON citation graph files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May query Semantic Scholar and write local citation-network output files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and tile.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
