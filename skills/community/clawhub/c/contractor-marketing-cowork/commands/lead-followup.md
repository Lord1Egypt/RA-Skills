---
description: Generate lead follow-up sequences for new inquiries. Text and email templates with timing. Speed wins -- first to respond gets the job.
disable-model-invocation: true
---

# Lead Follow-Up System

Read the user's business profile for phone number, services, and CRM.

## When user says "new lead" + details

Generate the full follow-up sequence:

### Website/form lead
- Minute 0: Auto-SMS confirming receipt + ask for property photos
- Minute 0: Auto-email confirming receipt with next steps
- Hour 1: Call attempt (remind user via notification)
- Day 1: SMS with scheduling options ("Reply 1 for morning, 2 for afternoon")
- Day 3: Email with recent project showcase near their area
- Day 5: SMS check-in ("Still interested in getting that quote?")
- Day 7: Closing email ("Just checking in one last time")

### Missed call
- Immediate: SMS ("Sorry I missed your call. I'm [name] from [business]. How can I help?")
- Next day: Call back attempt
- Day 2: SMS with easy reply option

### Facebook/social lead
- Reply on platform first (within 1 hour)
- Then SMS to move off-platform
- Follow day 1-7 sequence

## Template rules
- Texts under 160 characters
- 1 text per day maximum
- Always identify yourself by name and business
- STOP entire sequence the moment they respond
- "Not interested" = one polite reply + permanent stop
- Never more than 7 total touches
- Never send before 8am or after 8pm

## Output
Provide all templates ready to paste into CRM or Twilio. Include timing instructions.
