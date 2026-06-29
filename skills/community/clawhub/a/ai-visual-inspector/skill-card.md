## Description: <br>
AI视觉检测大师 helps agents guide computer-vision inspection workflows for defect detection, OCR quality checks, medical image assistance, satellite imagery analysis, security monitoring, and YOLO/ResNet model use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-gaoqian](https://clawhub.ai/user/ai-gaoqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, quality engineers, and operations teams can use this skill to plan and document visual inspection tasks across industrial defects, OCR checks, medical-image assistance, aerial imagery analysis, and monitoring workflows. Human review remains necessary for critical, medical, safety, legal, or surveillance decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may be used with highly sensitive images or in medical, safety, legal, or surveillance contexts. <br>
Mitigation: Use only images the user is authorized to process and require qualified human review before acting on critical results. <br>
Risk: Computer-vision outputs can be incomplete, incorrect, or overconfident. <br>
Mitigation: Treat outputs as decision support, validate against source images and domain standards, and avoid using the skill as the sole authority. <br>
Risk: Declared Python packages alter the local execution environment. <br>
Mitigation: Review opencv-python, numpy, pillow, ultralytics, and pytesseract before installation and install them in an isolated environment when possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ai-gaoqian/ai-visual-inspector) <br>
- [Publisher profile: ai-gaoqian](https://clawhub.ai/user/ai-gaoqian) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inspection plans, report structures, dependency guidance, and code or shell command snippets when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference Python, OpenCV, NumPy, Pillow, Ultralytics, and pytesseract dependencies declared in release metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
