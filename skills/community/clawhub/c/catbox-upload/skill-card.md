## Description: <br>
Uploads user-selected files to Catbox for permanent hosting or Litterbox for temporary hosting and returns the hosted URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Microck](https://clawhub.ai/user/Microck) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to upload a chosen local file to Catbox or Litterbox and receive a shareable hosted URL. It supports temporary Litterbox uploads and permanent Catbox uploads, including optional Catbox userhash tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded files are sent to external Catbox or Litterbox infrastructure and may expose secrets, private documents, or regulated data. <br>
Mitigation: Upload only files intended for external sharing; avoid secrets, private documents, and regulated data. <br>
Risk: Catbox uploads are permanent, and a Catbox userhash can identify or track uploads for an account. <br>
Mitigation: Prefer Litterbox for temporary sharing and treat any Catbox userhash as sensitive account information. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Microck/catbox-upload) <br>
- [Publisher Profile](https://clawhub.ai/user/Microck) <br>
- [Catbox API Endpoint](https://catbox.moe/user/api.php) <br>
- [Litterbox API Endpoint](https://litterbox.catbox.moe/resources/internals/api.php) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Guidance] <br>
**Output Format:** [Markdown usage guidance and plain text hosted URL output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uploads selected file bytes to an external hosting service; Litterbox supports 1h, 12h, 24h, and 72h expirations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
