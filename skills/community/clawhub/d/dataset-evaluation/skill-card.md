## Description: <br>
Evaluates miner dataset submissions by scoring content consistency across cleaned text samples and structured JSON quality against a dataset schema. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[levey](https://clawhub.ai/user/levey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Dataset evaluators and agent workflows use this skill to score miner submissions that include cleaned text samples, structured JSON, and a dataset schema. It produces deterministic sub-scores and a weighted final miner score for comparison or review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scoring weights or rubric assumptions may not match the evaluation task. <br>
Mitigation: Confirm the 40/60 weighting and sub-score criteria before using results for ranking or decisions. <br>
Risk: Similarity and value-accuracy judgments can vary if the evaluator uses unstated external knowledge. <br>
Mitigation: Base judgments only on the provided cleaned data, structured JSON, and schema, and keep all scores within the required 0 to 100 range. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/levey/dataset-evaluation) <br>
- [Publisher profile](https://clawhub.ai/user/levey) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON score report with concise evaluation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scores are bounded from 0 to 100 and include content consistency, structuring quality, final miner score, and detailed sub-scores.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
