## Description: <br>
Scan photographed documents into searchable PDFs with OCR and stable file naming. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kimjoohyeon-wq](https://clawhub.ai/user/kimjoohyeon-wq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn phone photos of documents into locally stored searchable PDFs, archive them with stable date-and-title filenames, and find prior scans by date, title, or keyword. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scanned document outputs are saved locally for later lookup and may contain sensitive information. <br>
Mitigation: Use the skill only where local file permissions and a retention or deletion process are controlled. <br>
Risk: Highly sensitive records could remain in daily-scan-storage after processing. <br>
Mitigation: Avoid scanning highly sensitive records unless storage access and deletion practices are appropriate for the use case. <br>
Risk: VirusTotal analysis is pending in the security evidence. <br>
Mitigation: Review the final security status before deploying in environments that require VirusTotal clearance. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, files, shell commands] <br>
**Output Format:** [Concise text plus local searchable PDF files; helper scripts return JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Korean and English OCR by default, stores outputs under daily-scan-storage/YYYY-MM, and returns filename, save location, and extracted title line when available.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
