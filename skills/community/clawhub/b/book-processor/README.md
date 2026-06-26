# Book Processor Skill

## Description
This skill automates the processing of a book when the user sends an EPUB file directly to 福德.

## Workflow
1. Receive the EPUB file from the user.
2. Create a folder under `~/workspace/books/` named after the book (filename without extension).
3. Save the uploaded EPUB into that folder.
4. If a `process_config.json` exists in the folder, use it; otherwise fall back to the default configuration.
5. Execute the script `scripts/process_book.sh <book_folder>` (relative to the skill directory) to generate all assets (cover, full text, summary, examples, etc.).
6. After processing, reply to the user with a list of generated files and a brief overview.

## Automation Hook
When a file is received, the assistant should trigger the above steps automatically. The existing `docs/book_pipeline.md` has been updated to reflect this automation.
