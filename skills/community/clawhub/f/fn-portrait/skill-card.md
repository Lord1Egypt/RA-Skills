## Description: <br>
Financial report footnote extraction and analysis tool for Chinese A-share listed companies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mapufan](https://clawhub.ai/user/mapufan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to download Chinese A-share annual reports from CNINFO, extract financial footnote data, run optional LLM-assisted analysis, and generate financial portrait outputs for a listed company. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: External LLM providers may receive extracted annual report text and derived financial summaries when DeepSeek or Moonshot credentials are configured. <br>
Mitigation: Only set DEEPSEEK_API_KEY or KIMI_API_KEY when that data sharing is acceptable; use local Ollama or --skip-llm for private PDFs. <br>
Risk: Unpinned Python dependencies can change behavior or supply-chain exposure over time. <br>
Mitigation: Install in an isolated Python environment and pin or lock dependency versions before production use. <br>
Risk: Downloaded PDFs, extracted spreadsheets, text, and portrait images are written to local output directories. <br>
Mitigation: Review and manage RAWPDF, output2, and portraits locations before and after running the pipeline. <br>


## Reference(s): <br>
- [FN Portrait Toolkit on ClawHub](https://clawhub.ai/mapufan/fn-portrait) <br>
- [mapufan ClawHub Profile](https://clawhub.ai/user/mapufan) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, code, files] <br>
**Output Format:** [Command-line guidance and generated PDF, Excel, text, and PNG files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads PDFs into RAWPDF, writes extracted data and LLM analysis under output2, and writes portrait images under portraits.] <br>

## Skill Version(s): <br>
3.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
