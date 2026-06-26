## Description: <br>
Reads QR codes and common barcodes from local image files and prints or saves the decoded contents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect local image files for QR code or barcode data, including URLs, text, and contact-style payloads. It is useful for quick command-line decoding and optional result export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Decoded QR and barcode contents may contain links, sensitive text, or misleading payloads. <br>
Mitigation: Treat decoded content cautiously, especially before opening links or sharing saved output. <br>
Risk: The tool depends on local image-decoding libraries and barcode dependencies from the runtime environment. <br>
Mitigation: Install Pillow, pyzbar, and zbar only from trusted package sources and run the tool only on image files you intend to inspect. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-qrcode-reader) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text and Markdown with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Decoded QR or barcode contents may be printed to stdout or saved to a text file when requested.] <br>

## Skill Version(s): <br>
1.2.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
