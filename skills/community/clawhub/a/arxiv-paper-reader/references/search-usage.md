# Search Result Handling

Use this workflow when the user asks to search arXiv or find the latest papers for a topic.

1. Run `search_arxiv.py` first.
2. Read `search_results.md`.
3. Show the first few candidates with explicit arXiv IDs.
4. Ask the user to name one or more arXiv IDs if they want full Markdown conversion or summaries.
5. For requests like "latest transformer papers", pass `--query transformer --sort submittedDate`.
6. For requests like "latest diffusion papers in computer vision", pass `--query "computer vision diffusion" --sort submittedDate`.
7. If the user gives a date window, add `--start-date YYYY-MM-DD --end-date YYYY-MM-DD`.

Keep result presentation grounded in the generated files. Do not imply that a paper has already been fetched into `paper.md` until `arxiv_to_md.py` runs.
