# /kickoff

Default entry. Figure out what the user is prepping for, confirm Four-Leaf has data for it, route to the right command.

## When to run

- User opens a fresh conversation and says something generic like "help me with my job search" or "I have an interview coming up".
- User's intent doesn't map cleanly to one of the other six workflows.

## Flow

1. **Verify the MCP is connected.** Call `list_roles`. If it fails with a not-connected error, tell the user how to install the MCP (see `mcp-tools.md` for the message) and offer coaching-only mode while they fix it. Step 2's `list_applications` call proves the connection just as well, so if you're doing both, one of them is enough.

2. **Check whether they're already mid-search.** Call `list_applications`. It's free, unmetered, and takes no arguments, so it costs nothing to ask. If it comes back with rows, the user isn't starting from zero and the greeting shouldn't pretend they are. Open on what's actually live:
   > You've got three applications open, one interviewing at Stripe. Want to prep that one, or are we adding to the pile?

   If it comes back empty, greet briefly instead. One sentence, not a wall of text:
   > Four-Leaf coach here. What are you working on? Finding jobs, prepping for a specific interview, scoring your resume, or thinking about negotiation?

   Don't read the whole list out. Name the one or two that matter (anything `interviewing`, then the most recently updated) and let them pick. If the user asked a direct question like "where am I", answer it with the list and skip the routing question entirely.

3. **Get the four pieces of context that matter.** Don't ask all of them upfront, and don't ask for what the tracker already told you. Ask the one that's most relevant to whatever the user said:
   - **Role**, the position they're targeting (data scientist, software engineer, product manager, etc.). If they name a role, validate it against `list_roles`.
   - **Company**, the specific target if they have one.
   - **Seniority**, one of entry, mid, senior, or staff.
   - **Timeline**, since interview tomorrow vs. browsing the market matters a lot.

4. **Route.** Based on what they said, pick the right command:

| User wants | Route to |
|---|---|
| Find jobs / discover roles | find-jobs |
| Understand a specific role's interview format | prep-role |
| Practice answering questions | practice |
| Check resume fit against a JD | analyze-jd |
| Comp negotiation | negotiate-prep |
| Generic "what are interviews like at X" | interview-strategy |
| "Where am I", "what have I applied to" | answer here from `list_applications`, then route into whichever one they pick |

Transition into the workflow in plain language. Don't announce it to the user by name. Just start doing the work.

## What not to do

- Don't make the user fill out a form. Conversational.
- Don't ask for their full resume in the kickoff workflow. Save that for analyze-jd.
- Don't try to be helpful on every topic at once. Pick the one that matters and dig in.
- Don't recite the tracker. It's context for a better opening question, not the answer to one.
- Don't treat an empty tracker as a problem to solve. Plenty of users search without tracking anything.
