# Tools and document delivery

Use the user's configured model and available tools. One agent can perform the five logical writing stages. A separate reviewer is optional; supply actual source contents and the draft when using one.

## Research and handoffs

Use available search, fetch or browser tools to collect the JD and role-relevant employer material. Pass readable source content and dated URLs to a worker that cannot browse. Reuse applicable research and update material facts. A URL alone does not supply its contents.

If a chosen reviewer is unavailable, explain the gap and offer local review or a usable handoff. Preserve accepted preferences and the full career reference.

## Produce the requested files

Use PDF or Word (.docx) as requested, following the employer's accepted file types. Default to PDF for submission when no preference is saved; provide Word for an editable copy when requested. Preserve the final wording and working links in either format. Follow [formatting](formatting.md). The bundled layouts use US Letter; use another available document tool for a different page size or house style.

For the bundled builder, choose the output format:

~~~sh
python3 {baseDir}/scripts/render_documents.py packet.json output-directory
python3 {baseDir}/scripts/render_documents.py packet.json output-directory --format pdf
python3 {baseDir}/scripts/render_documents.py packet.json output-directory --format both
~~~

The first command creates Word files using Python's standard library. The PDF option creates Resume.pdf and Letter.pdf from the same text and layout; Word files remain available as working copies. `--format both` prepares both formats for delivery. Microsoft Word is not needed to build either format.

The included PDF exporter uses WeasyPrint. Use an existing document environment with it installed, or install `requirements-pdf.txt` there. Platform setup is in the [WeasyPrint installation guide](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation). Existing PDF tools can also export the finished documents. For browser PDF export, prepare printable HTML with:

~~~sh
python3 {baseDir}/scripts/pdf_layout.py output-directory/Resume.docx output-directory/Resume.html
~~~

Repeat for the letter, then use the available browser PDF tool to save the PDFs.

This helper alone requires a JSON packet with resume_blocks, cover_letter_lines, contact_lines_count and optional application_answers. Résumé block kinds are name, contact, headline, summary, section, role_header, context, achievement, publication, skills and education. Role blocks share their role_id. Each block is one paragraph.

Letter lines follow name, contact paragraphs, date, recipient, salutation, body, closing and signature. Set contact_lines_count to the actual number of contact paragraphs, including zero; the agent supplies it. Optional letter_spacing is standard or compact. These are this helper's requirements, not universal writing rules or user setup questions.

If the selected PDF tool is unavailable, use another available exporter or identify the setup needed to finish that format. Keep the completed documents for the next attempt.

## Inspect and deliver

Compare actual file text with the final draft. Inspect rendered pages when a preview is available: paragraph gaps, section grouping, page breaks, clipping and the signature. Correct mechanical defects within delivery.

Deliver the selected PDF or Word files through the current channel's native attachment route. OpenClaw supports structured media fields; in automatic reply mode, standalone `MEDIA:/absolute/path/to/Resume.pdf` or `MEDIA:/absolute/path/to/Resume.docx` lines can attach local files. Follow the installed runtime's delivery mode and file-access rules. Attach the requested finished documents.

A Markdown link to a filesystem path does not deliver a file. If attachments are unavailable, return the complete finished text in the conversation and identify the missing file-delivery route. Layout checks do not add another editorial approval stage.

## Recover without replaying good work

The document helper validates both documents, saves the UTF-8 packet and prepares complete files before publishing them. Resume the identical saved packet with:

~~~sh
python3 {baseDir}/scripts/render_documents.py packet.json output-directory --resume
python3 {baseDir}/scripts/render_documents.py packet.json output-directory --resume --format pdf
~~~

The second command adds missing PDFs while reusing completed Word files and PDFs. A failed PDF export preserves the Word files, so adding the PDF tool and resuming does not require drafting or building them again.

It verifies saved receipts, preserves valid files and builds missing ones. It saves a pending receipt before publishing each document. On resumption, it can finish the receipt without rebuilding the completed file. Preserve changed files or files without verified receipts or matching pending recovery evidence and use a new revision directory. A changed packet is a new revision; do not overwrite an approved pair to recover another operation.

The bundled helper publishes through filesystem hard links. Its output directory needs hard-link support and write permission. If publication is unsupported, keep the packet, completed files and pending receipts; use supported storage or another available document tool. Do not treat a failed publication as completed delivery.

Keep accepted drafts, source material and completed files at meaningful boundaries. Inspect actual process/output state after a timeout before retrying. Adjust an insufficient allowance from observed execution; resume the failed step.

## Continue when requested

After document preparation, follow [application management](application-management.md) for tracking, submission and follow-up. Interview, profile/outreach and offer requests can start directly at their own guides.

