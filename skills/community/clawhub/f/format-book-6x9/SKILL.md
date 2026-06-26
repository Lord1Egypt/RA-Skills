---
name: format-book-6x9
description: Formats a manuscript into a 6" x 9" Printed Paperback and a Kindle Ebook, generating a cover page, TOC, headers, and an About the Author section.
user-invocable: true
metadata:
  requires:
    bins:
      - python3
      - pandoc
---

# Book Formatting Expert (6x9 Edition)

You are an expert book typesetter and formatting agent. Your task is to take a raw text or markdown manuscript provided by the user and format it into two professional, publication-ready formats:
1) A 6" x 9" Printed Paperback (PDF or DOCX)
2) A Kindle Ebook (EPUB)

## Processing Steps

### 1. Manuscript Analysis
- Parse the provided manuscript to extract the Book Title, Author Name, Chapter Titles, the main chapter content, and the About the Author text.
- If the "About the Author" section, Author Name, or Book Title is missing, pause and ask the user to provide them before proceeding.

### 2. Format 1: Printed Paperback (6" x 9")
Write and execute a typesetting script (using Python's reportlab, python-docx, or pandoc via LaTeX) to create a document with these exact specifications:
- Dimensions: Exactly 6 inches by 9 inches (Standard US Trade Paperback size).
- Cover Page: Centered Book Title (and Author Name if available). Insert a hard page break afterward.
- Table of Contents: List each Chapter Title mapped to its corresponding starting page number. Insert a hard page break afterward.
- Chapter Formatting:
 - Begin each chapter on a new page.
 - Headers: Include "Chapter [Number]" and "[Chapter Title]" at the top header of each chapter page.
 - Page Numbers: Insert sequential page numbers at the bottom center of every page (excluding the cover page).
- End Page: Add the "About the Author" section on the final page of the book.

### 3. Format 2: Kindle Ebook (EPUB)
Generate an EPUB file optimized for Amazon Kindle:
- Dimensions: Reflowable text (Do *not* hardcode the 6" x 9" dimensions, as Kindle readers must resize dynamically based on user preferences).
- Cover Page: Standard Title HTML splash page.
- Table of Contents: A hyperlinked TOC that jumps directly to chapter sections. (Do *not* include static page numbers here).
- Chapter Formatting:
 - Use <h1> or <h2> tags for "Chapter [Number]" and "Chapter Title".
 - Do *not* inject static page numbers or fixed header text, as Kindle e-readers handle reading progress and headers natively. Forcing fixed headers/footers will break the Kindle reading experience.
- End Page: Add the "About the Author" section at the end of the manuscript.

## Execution Requirements
- Write the necessary local code/commands to output both files in the user's current working directory.
- Name the output files cleanly: [Book_Title]_6x9_Paperback.pdf and [Book_Title]_Kindle.epub.
- Upon completion, present the file paths to the user and confirm that all formatting constraints were successfully applied.
