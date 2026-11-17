## Description:

Calibre Converter helps an agent identify a registered Calibre book or document and request conversion to another ebook or document format through calibre-openclaw-server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[carlosdelfino](https://clawhub.ai/user/carlosdelfino)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Calibre library administrators use this skill to convert books already registered in a local Calibre catalog, choose target formats such as EPUB, AZW3, MOBI, PDF, DOCX, or TXT, and report the server-returned conversion result to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled gateway has broad access to a local Calibre library and persistent server behavior.

Mitigation: Install only when you intend to administer a local Calibre gateway, keep it bound to loopback, and require a strong API key.

Risk: Network exposure and credential-handling weaknesses could increase the impact of unauthorized access.

Mitigation: Avoid exposing the service on a network and review dashboard API-key storage, query transport, and network binding settings before broader use.

Risk: Download and file path behavior may broaden local file and remote content handling beyond simple conversion.

Mitigation: Patch or disable arbitrary download URLs and manual server file paths unless they are required and reviewed.

Risk: Unpinned dependencies can change behavior or introduce supply-chain risk.

Mitigation: Pin and review dependencies before production or multi-user deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/carlosdelfino/skills/calibre-converter)
- [Server-Resolved Publisher Profile](https://clawhub.ai/user/carlosdelfino)
- [SKILL.md](artifact/SKILL.md)
- [calibre-openclaw-gateway README](artifact/calibre-openclaw-gateway/README.md)
- [Calibre Converter Client](artifact/scripts/calibre_converter_client.py)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown prose with optional shell commands and JSON conversion results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Conversion requests depend on a reachable calibre-openclaw-server and may include book identifiers, target format, optional source format, and force flag.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
