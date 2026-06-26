---
name: cliento-booker
description: Register Cliento booking pages via URL, check availability, and execute actual service bookings. Use when the user asks to book a haircut, reserve a service, or check availability at a registered barbershop/salon.
metadata: {"openclaw": {"requires": {"bins": ["python3"]}}}
---

# Cliento Booker Skill

You manage a persistent list of Cliento booking pages, check their availability, and execute actual bookings for the user.
You maintain state using files located relative to your workspace: `./.cliento/stores.json`.

*Note: Calendar cross-referencing capabilities require you to be equipped with a separate, external calendar access tool.*

## Core Workflow

You execute up to 6 core actions depending on the user's request. **Crucially: you must use the `scripts/cliento.py` tool instead of raw curl commands to prevent bash injection vectors when handling PII data.**

### Handling the Empty State
If `./.cliento/stores.json` does not exist or is empty when the user asks to check availability, inform them that no stores are registered. Ask them to provide the public URL of a Cliento booking page to get started.

### Action 1: Registering a Store
When the user provides a Cliento URL to register:
1. Verify the URL is safe, then fetch the raw HTML by executing `python3 scripts/cliento.py register <URL>`.
2. Parse the embedded Next.js JSON (inside `<script id="__NEXT_DATA__" type="application/json">`) to extract the Company ID, available services, and barbers.
3. Present the list to the user and ask them to select a service, a barber (or "Any"), and provide a memorable alias.
4. Save the new store object to `./.cliento/stores.json`.

### Action 2 & 3: Checking Availability
When the user asks for an appointment:
1. Read `./.cliento/stores.json` to extract the saved store parameters.
2. Determine the target date range.
3. Fetch the available slots via the script: `python3 scripts/cliento.py slots <company_id> <service_id> <from_date> <to_date> [resource_id]`.
4. **Calendar Cross-Reference:** If you have access to a calendar tool, pull the user's schedule. Filter out Cliento slots that overlap with busy blocks, factoring in travel time requested by the user.
5. Present the available time slots to the user.

### Action 4: Reserving a Slot
To reserve a time slot (temporarily held for ~5 minutes):
1. Execute the reservation POST request using the `slotKey` via the script: `python3 scripts/cliento.py reserve <company_id> <slot_key>`.
2. Parse the returned `cbUuid`. Present the reservation details (expiration time, service, price) to the user. 
3. Inform the user this is only a temporary hold and proceed immediately to Action 5.

### Action 5: User Booking Preferences
Before finalizing, verify the user's contact details by checking the workspace `USER.md` file.
1. If `USER.md` does not contain them, ask the user for their First Name, Last Name, Phone Number (international format), and Email.
2. Ask if they want to permanently save these new details in `USER.md` for future use. Only save them if the user explicitly agrees.
3. Ask if the user wants to include an optional note to the service provider.

### Action 6: Confirming a Booking
*Executing this action will finalize a live booking. Always ask the user if they are ready to proceed before doing this.*
1. Execute the confirmation POST sequence to finalize the booking using the script: 
   `python3 scripts/cliento.py confirm <company_id> <cb_uuid> "<first_name>" "<last_name>" "<email>" "<phone>" "<note>" "<booked_specific_true_false>"`
2. If the API returned that a Pin is required, the script output will notify you and you must ask the user for the pin, then append it to the args.
3. Inform the user when the booking is successfully complete and `"emailConfirmSent": true` is verified.

## Stores Format Example
`./.cliento/stores.json`:
```json
[
  {
    "alias": "Barber",
    "url": "https://cliento.com/business/barber-and-friends-1697/",
    "company_id": "5qdvTnEGaI1BRv42GeTMUC",
    "service_id": 33003,
    "resource_id": null
  }
]
```

## Limitations & Disclaimer
* Slot reservation holds the time temporarily (~5 minutes).
* Fully automated booking is only supported for stores using the "NoPin" confirmation method.
* This skill interacts with undocumented, reverse-engineered API endpoints and may break at any time.