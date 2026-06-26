## Description: <br>
批量识别最多50张身份证正面照片，提取姓名、性别和身份证号，并生成排版整齐的 TXT 文件附件。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linyao58](https://clawhub.ai/user/linyao58) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operations teams use this skill to process authorized batches of ID-card front images and export extracted identity fields into a downloadable text file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes sensitive identity data from ID-card images. <br>
Mitigation: Use it only when authorized to process the submitted ID cards and align usage with applicable data-handling requirements. <br>
Risk: Tencent Cloud credentials are required for OCR access. <br>
Mitigation: Configure a dedicated Tencent Cloud key with the narrowest OCR permissions available and do not hard-code API secrets. <br>
Risk: Image URLs and generated TXT attachments can expose identity information if retained or shared too broadly. <br>
Mitigation: Avoid public or long-lived image URLs and delete the generated TXT attachment when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/linyao58/batch-id) <br>
- [Tencent Cloud CAM API Key Console](https://console.cloud.tencent.com/cam/capi) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [TXT file attachment with status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes up to 50 image URLs per invocation and extracts name, sex, and ID number from the front side of ID cards.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
