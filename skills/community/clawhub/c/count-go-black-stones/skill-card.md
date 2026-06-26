## Description: <br>
Counts black Go/Weiqi stones from source board photos, estimates black Chinese-area scoring, and renders a clean static 19x19 result board image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imcaptor](https://clawhub.ai/user/imcaptor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Go players, reviewers, and agents use this skill to process original 19x19 Go board photos, count visible black stones, estimate black Chinese-area score, and optionally produce a clean result-board image for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Blurry, cropped, obstructed, or low-confidence board photos can lead to incorrect stone classification or scoring. <br>
Mitigation: Review the generated overlay and result board before trusting the count, and rerun with explicit board corners when automatic board detection is wrong. <br>
Risk: Chinese-area scoring is rules-based and does not independently resolve unsettled dead stones. <br>
Mitigation: Treat the score as an estimate when dead groups remain on the board and request manual confirmation for life-and-death status. <br>
Risk: Dependency versions can affect reproducibility in controlled environments. <br>
Mitigation: Pin or lock Python dependencies before deployment when reproducible installs matter. <br>


## Reference(s): <br>
- [Chinese README](README.md) <br>
- [English README](README.en.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, image files, shell commands, guidance] <br>
**Output Format:** [Markdown or text responses with optional JSON data, shell commands, verification overlays, and static result-board images.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a source 19x19 Go board photo; automatic detection can be guided with explicit board corners.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
