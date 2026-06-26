## Description: <br>
Ccy Ocr Local helps agents run offline OCR and chart recognition on local images, extracting Chinese or English text and structured chart data without external APIs by default. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenchongyong](https://clawhub.ai/user/chenchongyong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to process local screenshots, scanned documents, tables, charts, and dashboards for text extraction or rough structured chart data. It is useful when files should remain local and results need JSON, TSV, text, or visualization-assisted review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images and chart screenshots may contain sensitive business or personal data. <br>
Mitigation: Run the skill only on images you are authorized to process, keep outputs local, and avoid using private screenshots in training datasets without consent. <br>
Risk: OCR and heuristic chart extraction can produce low-confidence or imprecise results. <br>
Mitigation: Review confidence fields, quality warnings, suggestions, and visualization outputs before relying on extracted text or chart values. <br>
Risk: Future releases could add data collection, training, or upload behavior not present in this scanned version. <br>
Mitigation: Review and rescan future versions before installation or use, especially if they add collection or model-training workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenchongyong/ccy-ocr-local) <br>
- [Publisher profile](https://clawhub.ai/user/chenchongyong) <br>
- [README](artifact/README.md) <br>
- [OCR configuration](artifact/OCR-CONFIG.md) <br>
- [ICDAR 2019 chart recognition challenge dataset](https://rrc.cvc.uab.es/?ch=14&com=downloads) <br>
- [ICDAR 2021 chart recognition challenge dataset](https://rrc.cvc.uab.es/?ch=15&com=downloads) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON, TSV, text, or debug image outputs from the OCR scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include confidence scores, low-confidence word lists, quality warnings, suggestions, structured chart JSON, and optional visualization files.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
