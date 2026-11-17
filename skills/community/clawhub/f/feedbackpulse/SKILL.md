---
name: feedbackpulse
description: "FeedbackPulse (feedbackpulse.com) for HR teams: design employee surveys with no sign-in, and read engagement survey results, eNPS, review cycles, peer reviews and recognition through the FeedbackPulse MCP server. Use this skill for any FeedbackPulse request or when the user wants to draft an employee survey."
metadata:
  title: "FeedbackPulse"
  author: "FeedbackPulse"
  homepage: "https://feedbackpulse.com/"
---

# FeedbackPulse

[FeedbackPulse](https://feedbackpulse.com/) is an HR platform for performance reviews, 360 and peer feedback, engagement and pulse surveys, recognition, and eNPS analytics. It is free for up to 10 people. Sign up at https://app.feedbackpulse.com/register

FeedbackPulse offers two remote MCP servers (streamable HTTP). Pick the one that fits the task.

## 1. Employee Surveys MCP (no sign-in)

Endpoint: `https://app.feedbackpulse.com/mcp/employee-surveys` (no auth)

Use it to design an employee survey with the user. Connect it as a remote MCP server, or through a stdio bridge:

```bash
npx -y mcp-remote https://app.feedbackpulse.com/mcp/employee-surveys
```

Tools:

- `preview_survey`: validate and store a complete survey proposal you composed with the user. Requires `disclosure_accepted`, `context` and `proposal`.
- `prepare_survey_save`: only after the user approves a preview and chooses template or draft.
- `save_survey`: creates the approved template, or template plus an unlaunched draft, after FeedbackPulse OAuth. It never launches a survey, adds respondents or sends notifications.

Workflow:

1. Read the `instructions` the server returns on `initialize` and follow them. They include a disclosure the user must accept before `preview_survey`.
2. Gather the survey goal, audience, intended use and sensitivity in conversation.
3. Call `preview_survey` with the full proposal, show the user the result, and revise on request.
4. Save only after the user explicitly approves and picks template or draft.

## 2. FeedbackPulse MCP (workspace data, sign-in required)

Endpoint: `https://app.feedbackpulse.com/mcp`

Gives an assistant read access to the user's own FeedbackPulse workspace: surveys and results, review cycles, performance and peer reviews, recognition, and employees. Admins can also create survey templates and survey drafts.

Auth: OAuth for clients that support it. Other clients use a personal API token sent as `Authorization: Bearer <token>`. An Admin enables AI Integration in Settings > Features, then creates a token in Settings > Integrations. Store the token in your client's credential settings, never in the conversation.

Docs:

- MCP overview: https://feedbackpulse.com/help/integrations/mcp-overview/
- Tools reference: https://feedbackpulse.com/help/integrations/mcp-tools-reference/
- API tokens: https://feedbackpulse.com/help/integrations/token-management/
- Troubleshooting: https://feedbackpulse.com/help/integrations/mcp-troubleshooting/

## Rules

- Write actions (template and draft creation) need the user's explicit approval first.
- A 401 means the token is missing, wrong or revoked, or the account lacks MCP access. Ask the user to check Settings > Integrations. Do not retry with a guessed token.
- Anonymous survey responses stay protected: individual text answers are withheld below the workspace privacy threshold.
