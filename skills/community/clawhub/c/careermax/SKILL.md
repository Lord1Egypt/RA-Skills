---
name: careermax
description: Use CareerMax when the user wants to review their career context, manage their job pipeline, improve career materials, prepare for interviews, find referrals, or build skills.
version: 0.2.0
metadata:
  openclaw:
    requires:
      env:
        - CAREERMAX_API_KEY
      bins:
        - npx
    primaryEnv: CAREERMAX_API_KEY
    homepage: https://careermax.ai/ai-agent
---

# CareerMax

Use the CareerMax MCP tools to work with the user's connected CareerMax account.

## Conversation Rules

- Ask only for information needed by the selected tool.
- Read-only requests and clearly requested draft generation can proceed directly.
- Do not announce credit usage in normal responses. Use `get_credits` or
  `get_action_costs` when the user asks. Explain required and available balance
  when insufficient credits block a request.
- Before creating or changing a lasting CareerMax record, show the important
  details in plain language and ask the user to confirm.
- For `add_job` and `update_job`, call once without `confirmationToken`, show the
  returned details, and repeat the exact request with the returned token only
  after the user confirms.
- For `create_interview_session`, call once without `confirmationToken`, show
  the role, company, mode, duration, and round, and repeat the exact request
  with the returned token only after the user confirms.
- If CareerMax says a confirmation expired or does not match, show the current
  details and ask again. Never rewrite or guess the intended action.
- Never expose, repeat, or log the user's API key.

## Supported Workflows

- Account: `careermax_info`, `get_profile`, `get_credits`, `get_action_costs`
- Pipeline: `list_jobs`, `get_job`, `add_job`, `update_job`
- Resume and cover letter: `get_resume`, `review_resume`,
  `optimize_resume_text`, `generate_cover_letter`
- Interviews and research: `list_interviews`, `get_interview_feedback`,
  `create_interview_session`, `get_company_prep`, `generate_company_prep`
- Referrals and outreach: `search_mentors`, `list_bookmarked_mentors`,
  `generate_outreach`
- LinkedIn and learning: `get_linkedin_analysis`,
  `get_linkedin_optimizations`, `analyze_linkedin`,
  `optimize_linkedin_section`, `get_learning_plan`, `list_quiz_sessions`,
  `generate_learning_resources`, `generate_quiz`

## Boundaries

The public toolkit does not expose auto-apply. It also does not currently expose
CareerMax job search, profile editing, dashboard Career Coach actions,
professional-photo generation, or protected tailored-resume PDF delivery. Say
so plainly and point the user to the CareerMax dashboard when needed.

## Setup

1. Create a dedicated agent key in CareerMax Settings.
2. Set it through the agent's secure environment configuration as
   `CAREERMAX_API_KEY`.
3. Run `npx -y @careermax/agent-toolkit mcp`.
4. Verify the connection with a read-only request such as “list my pipeline.”
