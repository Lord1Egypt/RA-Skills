## Description:

Download ebooks (epub/pdf) from Anna's Archive and upload them to MEGA automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zerone0x](https://clawhub.ai/user/zerone0x)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to search for ebook titles, download selected epub/pdf/mobi files, and add them to a configured MEGA library.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads ebook files from third-party archive sites, which may create copyright, content safety, or malware exposure.

Mitigation: Use only when the requested download is authorized, review the selected source before downloading, and scan downloaded files before opening or sharing them.

Risk: The skill uploads downloaded files to a configured MEGA destination using local MEGA or rclone credentials.

Mitigation: Confirm the upload destination before execution, use least-privilege credentials, and disable automatic upload when search-only behavior is desired.

Risk: Broad activation wording may trigger download-and-upload behavior when a user intended only to search.

Mitigation: Prefer dry-run search first and add an explicit confirmation step before any download or cloud upload.

Risk: The downloader follows links from Anna's Archive and libgen.li without strict allowlisting beyond the implemented URL patterns.

Mitigation: Restrict outbound requests to expected domains and reject unexpected redirect targets before downloading files.

## Reference(s):

- [Book Fetch ClawHub release](https://clawhub.ai/zerone0x/skills/book-fetch)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Console text with downloaded ebook files and MEGA upload status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads are cached under /tmp/books and uploads target mega:/Books/ when MEGA or rclone is configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
