## Description: <br>
All-skill-list catalogs local OpenClaw skills by scanning the local skills directory, extracting descriptions and paths, caching results, and exporting JSON or Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fantasywoc](https://clawhub.ai/user/fantasywoc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inventory locally installed skills, inspect descriptions and paths, and export the catalog for sharing or integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent Pickle cache loading can execute code if the cache file is tampered with. <br>
Mitigation: Use only in a trusted local skills workspace, prefer JSON cache storage, and delete skills_cache.pickle before running if cache integrity is uncertain. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fantasywoc/all-skill-list) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Markdown, Files] <br>
**Output Format:** [Console text, JSON, or Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write skills_cache.pickle, skills_export.json, and all_skills.md under the skill scripts directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
