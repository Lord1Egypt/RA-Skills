## Description: <br>
Bird-watching log workflow: ask for place on enable, resolve eBird region via superpicky-cli region-query, persist to workspace/bird.json; record sightings from user text or BirdID photo identify; export CSV summaries for the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yoshino-s](https://clawhub.ai/user/yoshino-s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to keep a local bird-watching log, resolve an eBird region, record sightings from text or photos, and export observations or per-species summaries as CSV files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local birding log and CSV exports may include sensitive notes, timestamps, location context, local image paths, or raw photo-identification output. <br>
Mitigation: Review workspace/bird.json and exported CSV files before sharing them. <br>
Risk: Region lookup and photo identification depend on the external SuperPicky CLI helper. <br>
Mitigation: Use only a trusted SuperPicky CLI installation and confirm uncertain photo-identification results before appending a sighting. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yoshino-s/bird-watching-mode) <br>
- [bird.json schema](scripts/bird_log_schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, plus local JSON and CSV files created by bundled scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes workspace/bird.json and optional CSV exports; photo identification depends on a trusted SuperPicky CLI installation.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
