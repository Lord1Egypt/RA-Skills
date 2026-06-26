---
name: auto-summarizer
description: Automatically summarizes articles or PDF documents based on user-defined preferences for format and analysis type. Use this when a user requests a summary of a document or text.
---

# Automatic Article/PDF Summarizer

This skill enables the agent to generate concise summaries of articles or PDF documents. It offers flexibility in summary format and analysis type, tailored to the user's specific needs.

## Prerequisites

To use this skill, the user MUST provide the content to be summarized. This can be:
- A direct text input (e.g., copy-pasted article content).
- A URL to an online article.
- A path to a local PDF file in the sandbox.

## Workflow

When a user requests a summary of an article or PDF, follow these steps:

### 1. Obtain Content and User Preferences

- **Get Content**: Ask the user to provide the article text, a URL, or a PDF file path. If a PDF is provided, use appropriate tools (e.g., `manus-md-to-pdf` if it's markdown, or `pdftotext` via `shell` if it's a raw PDF) to extract the text content.
- **Ask for Summary Format**: Prompt the user to choose their preferred summary format from the following options:
    - **Key Points**: A bulleted list of the most important facts.
    - **Executive Summary**: A brief, high-level overview suitable for busy professionals.
    - **Structured Format**: A more detailed summary with an introduction, body analysis, and conclusion.
    Refer to `templates/summary_templates.md` for examples of each format.
- **Ask for Analysis Type**: Inquire if the user prefers a:
    - **Purely Factual** summary: Focuses solely on the information presented in the document.
    - **Critical Analysis**: Includes an evaluation of arguments, potential biases, and overall validity.

### 2. Generate Summary

- **Process Content**: Based on the extracted text and user preferences, generate the summary. Ensure the summary accurately reflects the original content while adhering to the chosen format and analysis type.
- **Apply Analysis**: If a critical analysis is requested, incorporate an objective evaluation of the document's strengths, weaknesses, and implications.

### 3. Present Summary to User

Deliver the generated summary to the user. Clearly indicate the chosen format and analysis type. Offer to make adjustments or provide alternative summaries if the user is not satisfied.

## References

- `templates/summary_templates.md`: Contains detailed examples and descriptions of the available summary formats and analysis types.