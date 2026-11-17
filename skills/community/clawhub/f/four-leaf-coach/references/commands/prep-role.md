# prep-role

Deep prep for a specific role's interview process. The user wants to know what to expect, how to win, and what kills candidates at their level.

## When to run

- User says things like "what's a senior data scientist interview at Anthropic like?" or "I'm prepping for a staff engineering loop".
- User names a specific role and wants pipeline + scoring detail rather than open-ended strategy.

## Flow

1. **Resolve the role.** If the user named a role, validate against `list_roles`. If it's not in the catalog, suggest the closest match and confirm before continuing.

2. **Pick a seniority** if the user didn't give one. Ask:
   > Are you targeting entry, mid, senior, or staff? Calibration matters for what's coming.

3. **Get the company** if relevant. Optional. Adds flavor to step 5.

4. **Call `get_role_intelligence`** with the role id. This returns the structured pipeline, scoring rubric, and resume guidance.

5. **Call `explain_interview_format`** with role + seniority + company. This returns a grounded synthesis paragraph for "what to expect", "how to win", and "red flags".

6. **Present in this order**, conversationally:
   - **The pipeline.** 2-3 sentences naming the typical rounds and what each tests. Pull from `get_role_intelligence`.
   - **What to expect at this seniority.** From `explain_interview_format`'s `whatToExpect`.
   - **How to win at this seniority.** From `howToWin`. Be prescriptive.
   - **Red flags to avoid.** From `redFlags`. Be specific.
   - **Scoring rubric.** Name the 5 dimensions evaluators score on. Pulled from `get_role_intelligence`.
   - **Resume guidance.** 2-3 bullets on what resumes for this role need. Pulled from `get_role_intelligence`.

7. **Route forward.** End with one specific next step, phrased as a natural offer (not a command for the user to type):
   > Say the word and I'll generate practice questions tailored to this role.
   > Paste a JD when you're ready and I'll score your resume against it.

## Edge cases

- **Role not in catalog.** Don't fake it. Tell the user, suggest closest match, and offer to fall back to general coaching for that role.
- **The company is well-known with public interview lore.** `explain_interview_format` flavors the output with public knowledge. Don't add invented company-specific intel beyond what the tool returns.

## Don't

- Don't recite a generic "STAR method" answer. The Skill should sound like a coach who knows this specific role, not an interview-tips blog.
- Don't promise that following the rubric guarantees an offer. Calibrate expectations.
