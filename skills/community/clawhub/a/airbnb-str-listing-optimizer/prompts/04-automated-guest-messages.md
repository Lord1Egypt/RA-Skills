# Prompt 4: Automated Guest Message Templates

**What it produces:** A 6-message automated communication sequence (booking confirmation → post-stay review request) that sounds personal, reduces host time to near-zero, and consistently earns 5-star reviews.

---

## The Prompt

```
You are a Superhost with a 4.95-star average across 800+ stays. Your secret: an automated message sequence that feels personal, solves problems before they happen, and consistently generates 5-star reviews.

Write 6 guest message templates for this property:

**Property name:** [e.g., "The Desert Oasis" / "Sunrise Condo at the Strip"]
**Host first name:** [e.g., Marcus / Sara / Frank]
**Property type:** [condo / house / cabin / etc.]
**Location city/neighborhood:** [e.g., Las Vegas — Paradise neighborhood]

**Check-in details:**
- Check-in time: [e.g., 4:00 PM]
- Check-in method: [lockbox code / smart lock app / keypad / in-person]
- Access code or instructions: [e.g., lockbox code is 4821 — located at front door right side / smart lock code sent 24 hrs before / app: Schlage Access, code 7734]

**Key property info:**
- WiFi name: [SSID]
- WiFi password: [password]
- Parking: [e.g., Unit #14 in underground garage, Level B1 / driveway / street]
- Checkout time: [e.g., 11:00 AM]
- Checkout instructions: [e.g., leave key on kitchen counter / return lockbox to same position / leave doors unlocked]
- Trash instructions: [e.g., bag trash and leave at front door / bins in garage left side]

**Host contact:** [Airbnb/VRBO message thread only / phone number for emergencies: XXX-XXX-XXXX]

**Local recommendations (optional — add 2–3 or leave blank for placeholders):**
- Restaurant: [e.g., Lotus of Siam — best Thai in Las Vegas, 10 min drive]
- Coffee: [e.g., PublicUs — walkable, great for remote work]
- Must-do: [e.g., Fremont Street Experience — free, 15 min drive, better at night]

---

OUTPUT FORMAT:

---

**MESSAGE 1 — Booking Confirmation**
*Send: Immediately after booking confirmed*
*Trigger: Booking confirmed*

[Message — 80–100 words. Warm welcome, confirm dates, set expectation that full check-in details arrive 48 hrs before arrival, invite questions.]

---

**MESSAGE 2 — Pre-Arrival Info (48 Hours Before)**
*Send: 48 hours before check-in*
*Trigger: 2 days before arrival*

[Message — 150–180 words. All the logistics: check-in time, access code, parking, WiFi. Keep it scannable — use short paragraphs, not bullets (Airbnb renders bullets oddly on mobile). Close with a line of excitement about their visit.]

---

**MESSAGE 3 — Check-In Day Welcome**
*Send: Day of arrival, 1 hour before check-in time*
*Trigger: Day of arrival, 3:00 PM (or 1 hr before check-in time)*

[Message — 80–100 words. Confirm check-in time, remind of access code, mention the welcome basket or any "surprise and delight" touch, invite them to reach out if anything is off. Warm tone — they're arriving soon.]

---

**MESSAGE 4 — Mid-Stay Check-In**
*Send: Day 2 of stay (or Day 1 for 1-night stays)*
*Trigger: 24 hours after check-in*

[Message — 60–80 words. "How's everything going?" + one local recommendation they might not know about. This is the message that catches small problems before they become bad reviews. Keep it brief — guests are busy traveling.]

---

**MESSAGE 5 — Checkout Reminder**
*Send: Evening before checkout*
*Trigger: 1 day before checkout*

[Message — 80–100 words. Remind of checkout time, give the 3-item checkout checklist (keep it short), offer late checkout if open (or say to ask), thank them for the stay, hint at the review request coming.]

---

**MESSAGE 6 — Post-Stay Review Request**
*Send: 2 hours after checkout time*
*Trigger: Day of checkout, 1:00 PM*

[Message — 80–100 words. Thank them for staying, mention something specific about their trip (use a placeholder: "[personalize: reference something from your message thread — their occasion, where they were visiting from, etc.]"), ask for a review, and offer to host them again. Include your direct Airbnb/VRBO profile link or just reference the platform.]

---

RULES:
- Use the host's first name as the sign-off on every message (not "The Team" or the property name).
- Never use exclamation points more than once per message. Overuse reads as fake.
- Messages 2 and 5 are operational. Messages 1, 3, 4, and 6 are relational. Balance tone accordingly.
- Message 4 (mid-stay) is the most important for review management. A guest who gets a genuine "how's it going?" almost never leaves a bad review without reaching out first.
- Message 6: never explicitly say "please leave a 5-star review." Airbnb prohibits review manipulation. Ask for "a review" and let the great experience do the work.
```

---

## Usage Notes

- Set these up in Airbnb → Inbox → Scheduled Messages (or VRBO's Auto-Messages feature).
- All 6 can be fully automated — set the trigger and forget.
- Message 4 (mid-stay) is the ROI message. Catching a broken A/C or missing towels before checkout = 5 stars instead of 3.
- For property managers with 10+ units: use these as your template bank and personalize with a merge field for property name and host name.
