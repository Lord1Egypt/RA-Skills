## Description: <br>
OCR documents (PDFs and images) using Gemini 2.5 Flash, PaddleOCR (local), or RapidOCR (local). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scottkiss](https://clawhub.ai/user/scottkiss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and operations teams use this skill to extract text from scanned PDFs and images. It supports local OCR engines for private processing and a Gemini engine when cloud OCR is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer downloads a prebuilt binary, which creates supply-chain trust considerations. <br>
Mitigation: Inspect the installer before running it, build from source when possible, or verify checksums if the publisher provides them. <br>
Risk: Using the Gemini engine may send selected document contents to a cloud service. <br>
Mitigation: Use RapidOCR or PaddleOCR for private documents, and use Gemini only when cloud processing is acceptable. <br>
Risk: The Gemini API key is stored in a local configuration file. <br>
Mitigation: Protect ~/.ocr/config with appropriate file permissions and avoid sharing the key in logs, prompts, or support artifacts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/scottkiss/doc-ocr-skills) <br>
- [Go documentation](https://golang.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text OCR output, with Markdown instructions and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write recognized text to a file or output directory and can batch process supported document files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
