# Conference Intern — Register for Events

You are registering the user for Luma events from the curated list. Use the browser to navigate RSVP pages and fill forms.

## Pre-flight

1. Load Luma session cookies from `luma-session.json` if it exists (authenticated session pre-fills forms)
2. Read `curated.md` to identify events that need registration (no status marker yet, or events the user has specifically asked to register for)
3. Read `config.json` for user info (name, email)

## For Each Luma Event

1. **Open** the event's RSVP URL in the browser
2. **Read** the page — find the registration form or "Register" / "RSVP" button
3. **Click** the register/RSVP button if needed to reveal the form
4. **Identify fields:**
   - Standard fields: name, email (fill from config)
   - Required custom fields: any field marked as required that is not name or email
   - Optional fields: leave blank
5. **Decision:**
   - If only standard required fields → fill them, submit, confirm success
   - If required custom fields are present → do NOT submit. Instead:
     - Note the event name and list all required custom field labels
     - Mark the event as "needs-input" in `curated.md`: `⏳ Needs input: [field1, field2]`
     - Move to the next event
6. **After submission:**
   - Look for a confirmation message on the page
   - If confirmed → mark as `✅ Registered` in `curated.md`
   - If error → mark as `❌ Failed` with brief reason

## Error Handling

- **CAPTCHA detected** → mark as `🔗 [Register manually](url)`, notify user
- **Event full / registration closed** → mark as `🚫 Closed`
- **Page won't load** → mark as `❌ Failed`, continue to next event
- **Session expired** (login prompt appears unexpectedly):
  - If the user is available interactively: re-do the email 2FA flow
  - Otherwise: mark remaining events as `🔒 Session expired` and stop

## After All Events

1. Update `curated.md` with all status changes
2. Summarize results:
   - X events registered successfully
   - X events need user input (list them with their custom fields)
   - X events failed or need manual registration
3. If any events need input, ask the user to provide the answers
   - When the user provides answers, re-run registration for just those events
