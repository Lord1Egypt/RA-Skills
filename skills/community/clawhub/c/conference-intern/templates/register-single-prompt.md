# Conference Intern — Fill Registration Form

A Luma event registration page is already open in the browser. The Register button has already been clicked. Your ONLY job is to fill the form and submit it.

## Context (provided by script)

- **Browser tab target ID:** {TARGET_ID}
- **User name:** {USER_NAME}
- **User email:** {USER_EMAIL}
- **Custom answers:** {CUSTOM_ANSWERS}
- **Result file:** {RESULT_FILE}

## CONSTRAINTS

- Do NOT open any pages or navigate anywhere — the tab is already open.
- Do NOT read knowledge files or session files — just look at the form.
- Do NOT close the tab — the script handles that.
- Be fast — you have 90 seconds.

## Steps

1. **Take a snapshot** of the browser tab (target ID: {TARGET_ID}) to see the current form.

2. **Check if already registered** — if the page shows confirmation text (e.g., "You're registered", "You're going", "Vous êtes inscrit"), write `{"status": "registered", "fields": [], "message": "Already registered"}` to `{RESULT_FILE}` and stop.

3. **Check if no form is visible** — some events are one-click RSVP or approval-only. If there's a confirmation or "request sent" message with no form fields, write `{"status": "submitted", "fields": [], "message": "One-click registration, no form"}` to `{RESULT_FILE}` and stop.

4. **Read the form** — identify all visible fields. Luma uses custom React components, NOT native HTML inputs. Look at the page visually, not the DOM.

5. **Fill mandatory fields:**
   - Name → use `{USER_NAME}`
   - Email → use `{USER_EMAIL}`
   - Fields matching answers in `{CUSTOM_ANSWERS}` → use the matching answer (fuzzy match by meaning, not exact label)
   - **Mandatory checkboxes** (terms of service, photo consent, code of conduct, data processing, etc.) → always check them. These are required to submit the form and are NOT custom fields.
   - **Promotional/marketing dropdowns** (newsletter signup, "interested in our services?", audit offers, etc.) → always select "No" or the negative/opt-out option
   - Required fields you can't fill and aren't promotional → these are real custom fields, report as needs-input

6. **If there are unfillable required fields** → write `{"status": "needs-input", "fields": ["Field Label 1", "Field Label 2"], "message": "Custom fields need answers"}` to `{RESULT_FILE}` and stop. Do NOT submit an incomplete form.

7. **Submit the form** — click the submit/confirm/register button.

8. **Check confirmation:**
   - If you see clear confirmation text ("You're registered!", "Registration confirmed", "Inscription confirmée") → status: `registered`
   - If confirmation is unclear or you're not sure → status: `submitted` (NOT "registered")

9. **Write result** to `{RESULT_FILE}` and stop.

## Result Format

Write ONLY a JSON object to `{RESULT_FILE}`:

```json
{
  "status": "registered|submitted|needs-input|failed",
  "fields": [],
  "message": "Brief note"
}
```

**Write the JSON and stop. No summary, no follow-up.**
