## Description: <br>
Relative binding free-energy and activity-label prediction workflows using PBCNet 2.0 on SciMiner, with Gnina docking and PDB/database retrieval to complete missing inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sciminer](https://clawhub.ai/user/sciminer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and computational chemistry teams use this skill to prepare and run PBCNet 2.0 relative binding-affinity or activity-label predictions, using Gnina docking and RCSB PDB retrieval when receptor, pocket, or ligand-pose inputs are missing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a SciMiner API key and uploads scientific input files to SciMiner. <br>
Mitigation: Store the API key only at ~/.config/sciminer/credentials.json, avoid printing or persisting it, and review files before upload. <br>
Risk: The bundled RCSB helper can make broader HTTP requests and save raw responses. <br>
Mitigation: Use it only for the documented SciMiner and RCSB workflows, avoid passing secrets in headers or bodies, and choose raw output paths intentionally. <br>
Risk: Incorrect receptor selection, reference ligand poses, activity-label order, or ligand bond orders can produce misleading predictions. <br>
Mitigation: Build the input ledger, preserve reference label order and ligand chemistry, rank docked poses by centroid deviation, and ask for clarification when mappings are ambiguous. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sciminer/fep-alternative) <br>
- [SciMiner tool API files](https://sciminer.tech/tool_api_files/) <br>
- [SciMiner API key setup](https://sciminer.tech/utility) <br>
- [RCSB PDB Data API](https://data.rcsb.org/rest/v1) <br>
- [RCSB PDB Search API](https://search.rcsb.org/rcsbsearch/v2) <br>
- [RCSB PDB](https://www.rcsb.org) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline JSON, bash, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SciMiner task IDs and share URLs, compact RCSB summaries, and raw response files only when intentionally requested.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
