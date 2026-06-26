## Description: <br>
Create, configure, and manage UNITH digital human avatars via the UNITH API across text-to-video, open dialogue, document Q&A, Voiceflow, and plugin modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[polucas](https://clawhub.ai/user/polucas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to create hosted UNITH digital humans, choose faces and voices, generate talking-head videos, configure conversational avatars, upload knowledge documents, and embed avatars in apps or websites. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can permanently delete hosted digital humans. <br>
Mitigation: Require explicit confirmation before delete or major update actions, including the exact head ID and alias. <br>
Risk: UNITH account credentials and cached tokens can grant account access. <br>
Mitigation: Protect UNITH_SECRET_KEY and disable or relocate UNITH_TOKEN_CACHE when local token caching is not appropriate. <br>
Risk: Uploaded documents, Voiceflow keys, plugin webhooks, and conversation content may be sent to external services. <br>
Mitigation: Upload only documents approved for UNITH processing and treat integration keys, webhook URLs, and conversation data as sensitive. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/polucas/digital-clawatar) <br>
- [UNITH API Overview](https://docs.unith.ai/_lgI-overview) <br>
- [UNITH Documentation](https://docs.unith.ai) <br>
- [API Payloads Reference](references/api-payloads.md) <br>
- [Configuration Reference](references/configuration.md) <br>
- [Embedding Reference](references/embedding.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with bash commands, JSON payloads, and embedding code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl and jq scripts, UNITH credentials, and mode-specific configuration files to create, update, delete, list, upload, and embed digital humans.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
