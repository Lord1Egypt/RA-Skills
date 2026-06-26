## Description: <br>
DiePre Vision Cognition provides a documentation-led framework for combining packaging and die-cutting machine vision inspection with SOUL-style reasoning, confidence scoring, local logging, and human review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingofzhao](https://clawhub.ai/user/kingofzhao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Manufacturing developers and quality engineers use this skill as a workflow template for die-cutting and packaging inspection: analyze dieline images, separate confident defects from uncertain regions, route low-confidence cases to human review, and record inspection outcomes for later feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is documentation-only and should not be treated as a reviewed runnable vision engine. <br>
Mitigation: Review any separate code, model files, and operational dependencies before using it with production images or automated quality decisions. <br>
Risk: Inspection logs may contain image paths, feature vectors, confidence scores, defect decisions, or manufacturing identifiers. <br>
Mitigation: Keep vision_log in a controlled workspace, define retention and deletion rules, and avoid logging raw images or sensitive manufacturing identifiers unless they are required. <br>
Risk: Low-confidence or uncertain visual detections can produce incorrect quality-control decisions. <br>
Mitigation: Preserve the documented human-review threshold and require human review for low-confidence cases before acting on inspection results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kingofzhao/diepre-vision-cognition) <br>
- [Publisher profile](https://clawhub.ai/user/kingofzhao) <br>
- [Project homepage](https://github.com/KingOfZhao/AGI_PROJECT) <br>
- [Generating CAD Code with Vision-Language Models](https://arxiv.org/abs/2410.05340) <br>
- [From 2D CAD to 3D Parametric via VLM](https://arxiv.org/abs/2412.11892) <br>
- [Efficient Vision-Language-Action Models](https://arxiv.org/abs/2510.17111) <br>
- [Vlaser: Synergistic Embodied Reasoning](https://arxiv.org/abs/2510.11027) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with Python usage examples, JSONL logging conventions, and verification checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill describes confidence scores, defect lists, human-review flags, collision logs, and local vision_log entries.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
