## Description:

Converts web pages to PDF files using Playwright after loading the page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goog](https://clawhub.ai/user/goog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users can convert a chosen webpage URL into an offline PDF copy, optionally setting the output filename.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Converting untrusted URLs can expose the local browser process to unwanted web content or capture content the user did not intend to preserve.

Mitigation: Use only intentionally chosen URLs and avoid local or private-network addresses unless that is the explicit goal.

Risk: A user-provided output filename may overwrite an existing file in the working directory.

Mitigation: Run the converter from a dedicated output directory and provide simple filenames.

Risk: Unpinned Playwright or Chromium versions can change rendering behavior over time.

Mitigation: Pin Playwright versions and run the converter in a restricted environment for stronger repeatability and isolation.

## Reference(s):


## Skill Output:

**Output Type(s):** [files, shell commands, guidance]

**Output Format:** [PDF files with text guidance and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates A4 PDFs with 20px margins and saves them to the current working directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
