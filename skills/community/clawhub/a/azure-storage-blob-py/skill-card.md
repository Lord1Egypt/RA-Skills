## Description: <br>
Azure Storage Blob Py helps agents use the Azure Blob Storage SDK for Python to upload, download, list, and manage blobs and containers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thegovind](https://clawhub.ai/user/thegovind) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to generate Azure Blob Storage SDK for Python guidance, including client setup, authentication, blob transfer, container management, SAS token examples, metadata handling, async usage, and performance tuning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides examples that authenticate to Azure Blob Storage and may involve credentials, SAS tokens, account URLs, or Azure roles. <br>
Mitigation: Use least-privilege Azure roles or short-lived SAS tokens, avoid broad account keys where possible, and keep credentials out of prompts, logs, and generated files. <br>
Risk: The skill includes examples for uploading, overwriting, downloading, listing, and deleting blobs and containers. <br>
Mitigation: Confirm the account, container, blob name, overwrite flag, and delete behavior before asking an agent to run generated examples against real storage. <br>


## Reference(s): <br>
- [Azure Storage Blob Py ClawHub page](https://clawhub.ai/thegovind/azure-storage-blob-py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides instructional examples for Azure Blob Storage clients, authentication, uploads, downloads, listing, deletion, SAS tokens, metadata, async clients, and performance settings.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
