# analyze-jd

Score a resume against a job description and point out the gaps.

## When to run

- User says "should I apply for this?" or "how does my resume look against this JD?".
- User pastes a job description and asks for a fit assessment.
- User picks one of the postings `find-jobs` just returned and wants to know if they're a fit.

## Getting the job description

`match_score` needs the posting as plain text. It does not fetch URLs and rejects a bare one with `job_description_is_a_url`. Three ways in, in order of preference:

1. **The job came from `search_jobs`.** Call `get_job` with its `id`. You get the full description back (first 12,000 characters, with `descriptionTruncated` when it was cut) and no fetching happens at all. This is the normal path when the user found the role through this Skill, and it's free and unmetered, so use it rather than asking them to paste something you can already read. If `active` comes back false the posting has come down; say so before spending a score on it.
2. **The user pasted the text.** Use it as-is.
3. **The user pasted a URL from somewhere else** (LinkedIn, a company page, a recruiter email). Nothing in the corpus knows about it, so fetch the page with your own WebFetch tool and use the result. If WebFetch isn't available or the page won't render, ask them to paste the body.

If you only have a short fragment, ask for the full posting before scoring. A stub gives an unreliable score.

## Flow

1. **Get the JD** by whichever of the three routes applies. The user's resume already lives on their Four-Leaf account, so don't ask them to paste that. When you need a posting from them, one short prompt:
   > Paste the job description (or the link) and I'll score the fit against your Four-Leaf resume.

2. **Call `match_score`** with only the `jobDescription` argument. Omit `resume`; the tool pulls the master resume from the user's account and scores against that. The output carries `resumeSource` so you know what was evaluated. If it returns `error: "no_master_resume"`, tell the user briefly there's no resume on their account yet, point them at the `uploadResumeUrl` it carries, and call the tool again once they confirm. If the user explicitly wants to score a different version (one they're drafting right now), pass it via `resume` as an override.

3. **Present the score clearly.** Lead with the headline:
   > **Match score: 72 out of 100.** Solid fit with real gaps.

   Then break it down:
   - **What matched well.** Pull the strongest 3-5 from the matched skills.
   - **What's missing.** Pull required skills the resume doesn't mention. Be specific.
   - **Calibration.** Score 80+ = apply with current resume. 60-79 = apply, but tailor first. Below 60 = either the role isn't a fit or the resume buries relevant work.

4. **Offer to save it.** A posting worth scoring is usually worth tracking, and `save_application` is free:
   > Want me to drop this in your Four-Leaf tracker so you don't lose it?

   Call `save_application` with the `jobId` when the job came from `search_jobs` (company, title, URL and description come from the corpus row). Otherwise pass `company` and `title`, plus `jobUrl` and `jobDescription` when you have them, so the posting is still there later. Use `status: "applied"` only if they've actually applied; the default `saved` is right for "I'm considering this". If the response comes back with `duplicate: true` it was already in the tracker and nothing was written. Say that, don't claim you saved it.

5. **Offer the tailoring path.** If the score is in the tailor-first range:
   > Want help addressing those gaps? I can walk you through which bullets to strengthen and which keywords to add here in chat. Or for a full AI rewrite tailored against this JD, that's a paid feature on Four-Leaf.

   If the user picks "walk me through here", coach the specific bullets without writing the full rewrite. If they want the rewrite, call `tailor_resume` with the same `jobDescription` and a `role` id (it requires one, and returns `role_not_found` for anything not in `list_roles`, so resolve the role first if you only had a pasted JD). It returns a deep link with the posting already attached. On a free account it returns `upgrade_required`; surface the URL per `upgrade-flow.md`.

## Edge cases

- **Resume is very short or very long.** Tell the user what you noticed. A one-page resume for a senior role is usually under-selling; a four-page resume for an entry role is usually noise.
- **JD is vague.** Tell the user. `match_score` works best with a real JD; if it's a stub, the score is unreliable.
- **JD URL won't fetch.** Some postings (LinkedIn, certain ATS pages) are gated or JS-rendered and WebFetch can't read them. Don't try harder; ask the user to paste the JD body directly. One short prompt, then proceed. If the same role is in the corpus, `search_jobs` plus `get_job` may get you there without the fetch.
- **`get_job` returns `job_not_found`.** The row is gone from the corpus. A posting that merely got filled still resolves, with `active: false`, so this is the harder failure. Re-run `search_jobs`, or work from the apply URL the search result already gave you.
- **`descriptionTruncated: true`.** 12,000 characters covers the requirements on essentially every posting, so score it and move on. Only mention the cut if the user asks about something that would live past it (a long benefits appendix, say).
- **No master resume on the account.** The tool returns `no_master_resume` with an upload URL. Surface it cleanly: "You don't have a resume on your Four-Leaf account yet. Upload one at `<uploadResumeUrl>` and I'll run the score." Don't try to scrape a resume from the chat history as a workaround.
- **User asks for a rewrite.** Decline writing the full resume. Coach the specific changes. Full rewrites belong on the paid surface.

## Don't

- Don't editorialize that the score is "bad" or "great". State it, calibrate against the bands above, move forward.
- Don't make up skills the resume doesn't mention. Only call out what `match_score` actually returned.
- Don't WebFetch a posting you can get from `get_job`. The corpus copy is already text, it costs nothing, and the fetch can fail.
- Don't lecture about resume best practices in general. Focus on this resume vs. this JD.
