# Check-in Procedure

Prompt the user for progress updates on projects that haven't been checked in recently.

## Steps

1. **Load projects** — Read `workspace/projects/README.md` for active projects.
2. **No projects?** — If no active projects exist and you haven't already asked about projects today (check today's daily notes):
   - Ask the user what projects they're working on.
   - Stop here.
3. **Pick stalest project** — Read each active project file. Pick the one with the oldest `Last Check-in` date. Note any open Action Items, especially blocked ones.
4. **Ask** — Ask the user for a brief progress update:
   - If there are blocked action items, ask about those specifically (e.g., "Did the client send the advance payment?" rather than "How's it going?").
   - Otherwise, reference the project phase and last known status.
   - Ask ONE focused question, not a checklist.
5. **Update** — After the user responds:
   - Update the project file's `Last Check-in` date to today.
   - Append their response to the `Notes` section with today's date.

## Guidelines

- Only check in on 1 project per invocation.
- If the user seems busy or gives a short answer, acknowledge and move on.
- If a project hasn't been checked in for >7 days, mention it gently.
