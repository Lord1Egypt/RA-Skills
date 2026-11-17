# What ATSPrep does with your text

- No account and no sign-in. ATSPrep logs only each tool's name, whether it worked and how long it took, never the text.
- Most tools run fixed rules on ATSPrep's Cloudflare Worker with no AI: scoring, keyword matching, bullet checks, LinkedIn checks, action verbs, letter drafts and question lists.
- Four tools also send the text they rewrite to an open language model on Cloudflare Workers AI (Google's Gemma 4, with Meta's Llama 3.3 70B if Gemma is busy): `tailor_resume`, `improve_bullet`, `write_summary` and `review_interview_answer`. That is resume lines without your contact details, the job post, the bullet, or the interview question and answer. Cloudflare does not use it to train models. Any AI line that adds a number, name or fact you didn't give is dropped.
- To keep within a daily AI limit, a one-way hash of the connecting IP address is counted for the rest of the day. When a limit is hit, the rule-based result still comes back.
- `fetch_job_post` reads the one public job page it is given. Some sites block it; then paste the post's text instead.
- Your assistant (Claude, ChatGPT, Codex, Copilot...) sees everything you share with it, under its own privacy terms.

Full policy: https://atsprep.com/privacy#mcp
