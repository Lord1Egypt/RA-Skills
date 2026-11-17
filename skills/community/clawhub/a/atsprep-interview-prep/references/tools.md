# ATSPrep MCP tools

Endpoint: `https://atsprep.com/mcp` (MCP streamable HTTP, no auth). Call any tool with:

```sh
node scripts/atsprep.mjs <tool> key=value key=@file.txt
```

Or, if the ATSPrep MCP server is connected to your agent, call the tool directly by name.
Tools marked **AI** also send their text to Cloudflare Workers AI (see privacy.md); all others are rule-based.

## check_resume

Use this when the user shares a resume (pasted text or a file's text) and wants it checked, scored, reviewed for ATS problems, or wants to know what to fix. Score a resume from 0 to 100 with ATSPrep's fixed rules and list each issue with a stable code, where it is and how to fix it. Also reports how the text parsed (roles, experience and project bullets, education, skills and skill groups, input and scored word counts, with definitions). Role-specific advice, such as seniority signals, is given only when the resume names a target title or you pass target_role or job_description; with job_description the score becomes the fit for that job (0.5 requirements met, 0.3 evidence, 0.2 readability, capped for missing hard requirements or impossible claims) and it also returns job_fit and a keyword match summary. Resume up to 30,000 characters. Rules version 2026-10-23.5.

| Argument | Type | Required | Notes |
| --- | --- | --- | --- |
| `resume_text` | string | yes | The whole resume as plain text, one heading, role or bullet per line. max 30000 chars |
| `target_role` | string | no | Optional. The job title the candidate is applying for. max 120 chars |
| `job_description` | string | no | The full job posting as plain text, including its requirements (120–20,000 characters). For a link, call fetch_job_post first. max 20000 chars |

## match_job

Use this when the user has a resume and a job posting and asks how well they match, what keywords are missing, or whether to apply. For rewrites, use tailor_resume instead. Compare a resume with a job posting: the posting's keywords found in the resume (with how they matched: exact, normalized, alias or stem, and the matched span), the ones missing with the posting sentence they come from, each term's weight and whether the posting lists it as required or preferred, and weighted overall, required and preferred coverage. Posting 120–20,000 characters. Rules version 2026-10-23.5.

| Argument | Type | Required | Notes |
| --- | --- | --- | --- |
| `resume_text` | string | yes | The whole resume as plain text, one heading, role or bullet per line. max 30000 chars |
| `job_description` | string | yes | The full job posting as plain text, including its requirements (120–20,000 characters). For a link, call fetch_job_post first. max 20000 chars |

## check_bullets

Use this when the user wants a few resume bullet points checked without sending the whole resume. Give each resume bullet a score, a verdict and specific fixes with stable codes: weak openers, missing scale or result, numbers that show neither, hard-to-believe claims, first person, vague claims. The same rules and severities as check_resume. Up to 30 bullets of up to 600 characters each; blank items are skipped and reported by index. Rules version 2026-10-23.5.

| Argument | Type | Required | Notes |
| --- | --- | --- | --- |
| `bullets` | array | yes | One resume bullet per item, at most 30. |

## open_in_studio

Use this when the user wants to edit their resume in an editor, apply a template, or download it as a PDF or Word file. Make a link that opens this resume in ATSPrep Studio, the free editor, so the user can fix it, pick a template and download a PDF. The text travels in the link's #fragment, which is never sent to a server.

| Argument | Type | Required | Notes |
| --- | --- | --- | --- |
| `resume_text` | string | yes | The whole resume as plain text, one heading, role or bullet per line. max 30000 chars |

## list_templates

Use this when the user asks for resume templates, designs or example resumes for a role. List ATSPrep's resume designs, each with a link that opens Studio in that design, and the example resumes by role, each with a link that opens it in Studio and a preview image.

No arguments.

## fetch_job_post

Use this when the user gives a job posting link instead of its text; then pass the result to the job tools. Read a public job posting from its link and return the title, company, location and full description as plain text, ready for match_job, tailor_resume, keyword_scan or interview_questions. Reads LinkedIn, Greenhouse, Lever, Ashby, SmartRecruiters, Workable, Workday and most company careers pages. Some sites block reading; then ask the user to paste the text.

| Argument | Type | Required | Notes |
| --- | --- | --- | --- |
| `url` | string | yes | The job posting's public link (https). max 2000 chars |

## keyword_scan

Use this when the user has only a job posting (no resume yet) and wants its key skills and keywords. List the skills, tools and requirements a job posting asks for, ranked by how hard it leans on each (repetition, position, required or preferred headings), with the high-priority ones flagged. Use match_job to see which a resume already shows. Posting 120–20,000 characters. Rules version 2026-10-23.5.

| Argument | Type | Required | Notes |
| --- | --- | --- | --- |
| `job_description` | string | yes | The full job posting as plain text, including its requirements (120–20,000 characters). For a link, call fetch_job_post first. max 20000 chars |

## tailor_resume (AI)

Use this when the user wants their resume rewritten or tailored for a specific job posting. Tailor a resume to a job posting: the posting's keywords the resume is missing (from match_job's rules) and suggested rewrites of the user's own summary and bullets that bring in the posting's terms only where the existing line already supports them. Each suggestion lists the posting terms it borrowed and confirm_with_user lists terms to ask about, never to add unasked. End the reply with next_step: the link that opens the resume in ATSPrep to check the edits and download. Part of the answer is drafted by an AI model (Gemma 4, with Llama 3.3 70B as a backup, on Cloudflare Workers AI) behind ATSPrep's guard, which drops any figure, name or tool the user's text doesn't contain. If the AI part is unavailable, the rule-based part still comes back and ai.message says why.

| Argument | Type | Required | Notes |
| --- | --- | --- | --- |
| `resume_text` | string | yes | The whole resume as plain text, one heading, role or bullet per line. max 30000 chars |
| `job_description` | string | yes | The full job posting as plain text, including its requirements (120–20,000 characters). For a link, call fetch_job_post first. max 20000 chars |

## improve_bullet (AI)

Use this when the user wants one resume bullet rewritten or made stronger. Check one resume bullet with the fixed rules (score, verdict, fixes) and suggest up to three stronger rewrites that keep every fact as given. ask_user names the one fact to ask the user for; never invent it. Part of the answer is drafted by an AI model (Gemma 4, with Llama 3.3 70B as a backup, on Cloudflare Workers AI) behind ATSPrep's guard, which drops any figure, name or tool the user's text doesn't contain. If the AI part is unavailable, the rule-based part still comes back and ai.message says why.

| Argument | Type | Required | Notes |
| --- | --- | --- | --- |
| `bullet` | string | yes | One resume bullet. max 600 chars |
| `role` | string | no | Optional. The job title this bullet sits under. max 200 chars |
| `company` | string | no | Optional. The employer this bullet sits under. max 200 chars |

## write_summary (AI)

Use this when the user wants a resume summary or professional profile written from their resume. Draft professional summaries from a resume: rule-based drafts built from its title, skills and the bullets that carry a figure, plus AI drafts that use only facts in the resume. Part of the answer is drafted by an AI model (Gemma 4, with Llama 3.3 70B as a backup, on Cloudflare Workers AI) behind ATSPrep's guard, which drops any figure, name or tool the user's text doesn't contain. If the AI part is unavailable, the rule-based part still comes back and ai.message says why.

| Argument | Type | Required | Notes |
| --- | --- | --- | --- |
| `resume_text` | string | yes | The whole resume as plain text, one heading, role or bullet per line. max 30000 chars |
| `target_title` | string | no | Optional. The job title the summary should aim at. max 200 chars |

## action_verbs

Use this when the user wants stronger verbs or synonyms for resume wording. Suggest resume action verbs. Pass a weak opener ("responsible for", "helped") for direct swaps and why they read weak, or the work in plain words ("trained new staff", "cut costs") for the matching verb groups with an example bullet. Leave query empty for every group.

| Argument | Type | Required | Notes |
| --- | --- | --- | --- |
| `query` | string | no | Optional. A weak verb or phrase, or the kind of work in plain words. max 200 chars |

## generate_linkedin_headline

Use this when the user wants new LinkedIn headline ideas. Write LinkedIn headline options from the user's answers, each in a proven pattern (title and focus, title and result, title and who you help…), with its length and roughly what shows in search before the cut. Uses only the answers given.

| Argument | Type | Required | Notes |
| --- | --- | --- | --- |
| `role` | string | yes | The job title the user wants to be found for. max 200 chars |
| `years` | string | no | Optional. Years of experience, as a number. max 20 chars |
| `focus` | string | no | Optional. Their specialty or industry, e.g. "B2B SaaS onboarding". max 200 chars |
| `skills` | string | no | Optional. Main skills, comma separated. max 200 chars |
| `results` | string | no | Optional. One or two real results, one per line, with the numbers the user gave. max 600 chars |
| `audience` | string | no | Optional. Who they help, e.g. "early-stage startups". max 200 chars |
| `next` | string | no | Optional. What they want next, e.g. "open to product roles in London". max 200 chars |

## check_linkedin_headline

Use this when the user wants their existing LinkedIn headline reviewed. Check a LinkedIn headline: length against the 220-character limit, what shows in search results before the cut, whether it leads with a searchable job title, and buzzwords or vague claims to replace.

| Argument | Type | Required | Notes |
| --- | --- | --- | --- |
| `headline` | string | yes | The headline as it reads now. max 400 chars |
| `role` | string | no | Optional. The job title the user wants to be found for. max 200 chars |
| `focus` | string | no | Optional. Their specialty or industry. max 200 chars |
| `skills` | string | no | Optional. Main skills, comma separated. max 200 chars |

## check_linkedin_about

Use this when the user wants their LinkedIn About or summary section reviewed. Check a LinkedIn About section: what shows before "see more" on a phone and on a computer, whether the opening says who they are, results with numbers, buzzwords, a clear next step, and the 2,600-character limit.

| Argument | Type | Required | Notes |
| --- | --- | --- | --- |
| `about` | string | yes | The whole About section. max 6000 chars |
| `role` | string | no | Optional. The job title the user wants to be found for. max 200 chars |

## draft_cover_letter

Use this when the user wants a cover letter for a job. Draft a cover letter from the user's resume and the job posting with fixed rules: name, contact details and up to two results from the resume, the job title and top keywords from the posting. Facts that are missing show as [square-bracket] gaps for the user to fill, never as stand-ins. Returns the letter, the gaps and a checklist.

| Argument | Type | Required | Notes |
| --- | --- | --- | --- |
| `resume_text` | string | no | The whole resume as plain text, one heading, role or bullet per line. max 30000 chars |
| `job_description` | string | no | The full job posting as plain text, including its requirements (120–20,000 characters). For a link, call fetch_job_post first. max 20000 chars |
| `style` | classic \| direct \| career-change | no | classic (default), direct, or career-change. |
| `name` | string | no | Optional. Overrides the name read from the resume. max 200 chars |
| `email` | string | no | Optional. max 200 chars |
| `phone` | string | no | Optional. max 200 chars |
| `current_title` | string | no | Optional. The user's current or last job title. max 200 chars |
| `company` | string | no | Optional. The company they are applying to. max 200 chars |
| `role` | string | no | Optional. The job title they are applying for. max 200 chars |
| `hiring_manager` | string | no | Optional. The hiring manager's name, if known. max 200 chars |
| `results` | string | no | Optional. One or two real results, one per line. max 600 chars |
| `why` | string | no | Optional. Why this company, in the user's words. max 600 chars |

## draft_resignation_letter

Use this when the user wants to resign and needs a resignation letter or their last working day. Draft a short, professional resignation letter and work out the last working day from the notice period. Missing facts show as [square-bracket] gaps. Returns the letter, the last day and a checklist (notice stated, no complaints, length).

| Argument | Type | Required | Notes |
| --- | --- | --- | --- |
| `tone` | formal \| warm \| short | no | formal (default), warm or short. |
| `name` | string | no | Optional. The user's name. max 200 chars |
| `manager` | string | no | Optional. Their manager's name. max 200 chars |
| `company` | string | no | Optional. max 200 chars |
| `role` | string | no | Optional. Their job title. max 200 chars |
| `notice` | 1w \| 2w \| 4w | no | Notice period: 1w, 2w (default) or 4w. Use notice_days for anything else. |
| `notice_days` | integer | no | Optional. A notice period in days, instead of notice. |
| `working_days_only` | boolean | no | Count notice in working days (Monday to Friday). Default false: calendar days. |
| `date` | string | no | Optional. The day the letter is handed in, YYYY-MM-DD. Default today (UTC). |
| `reason` | none \| new-role \| relocation \| study | no | Optional. A one-line reason; none (default) gives no reason. |
| `offer_handover` | boolean | no | Offer to help hand over. Default true. |
| `thanks` | string | no | Optional. Something specific to thank them for. max 600 chars |

## interview_questions

Use this when the user is preparing for an interview and wants likely questions, for a specific job or in general. Interview questions to practise, each with what the interviewer is listening for, plus STAR answer tips. With a job_description, questions come from its skills and duties, along with what to research and questions to ask; with resume_text, from the user's own roles. Rule-based.

| Argument | Type | Required | Notes |
| --- | --- | --- | --- |
| `job_description` | string | no | Optional. The job posting as plain text. max 20000 chars |
| `resume_text` | string | no | The whole resume as plain text, one heading, role or bullet per line. max 30000 chars |
| `kind` | all \| posting \| resume \| about \| behavioural \| role \| closing | no | Optional. One group: posting, resume, about, behavioural, role or closing. Default all. |
| `limit` | integer | no | How many questions. Default 12. |

## review_interview_answer (AI)

Use this when the user gives an answer to an interview question and wants feedback on it. Review the user's answer to an interview question: a rating, length and speaking time, STAR coverage for stories, filler words, specific checks, the follow-up an interviewer would likely ask, and a stronger version that keeps to the user's own facts. Part of the answer is drafted by an AI model (Gemma 4, with Llama 3.3 70B as a backup, on Cloudflare Workers AI) behind ATSPrep's guard, which drops any figure, name or tool the user's text doesn't contain. If the AI part is unavailable, the rule-based part still comes back and ai.message says why.

| Argument | Type | Required | Notes |
| --- | --- | --- | --- |
| `question` | string | yes | The interview question. max 400 chars |
| `answer` | string | yes | The user's answer, as they would say it. max 4000 chars |
| `kind` | story \| pitch \| plan \| number \| close | no | story (default: a past example, scored on STAR), pitch (tell me about yourself), plan (how would you…), number (salary or a figure) or close (questions for them). |
| `resume_text` | string | no | Optional. The resume, so the stronger answer can use real facts from it. max 30000 chars |

