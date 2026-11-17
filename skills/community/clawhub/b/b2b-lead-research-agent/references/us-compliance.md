# US outbound compliance (B2B)

This is a practical baseline, not legal advice. Rules differ by state and change;
when volume, industry, or jurisdiction matters, confirm with counsel.

## CAN-SPAM (commercial email, 15 U.S.C. 7701-7713)

Applies to commercial email. B2B is not exempt.

Required elements:

1. **Truthful headers** - From, To, Cc, and Reply-To must not be false or
   misleading. "From" must identify the sender.
2. **Non-deceptive subject line** - no fake "Re:", "Fwd:", "FW:", no misleading
   topic, no fake account update.
3. **Ad identification** - if the message is an ad, the message must disclose
   it clearly and conspicuously. Applies to messages whose primary purpose is
   commercial; in practice: disclose plainly when the recipient did not expect
   the message.
4. **Valid physical postal address** - the sender's valid physical address.
5. **Clear and conspicuous opt-out** - a valid email address or other mechanism
   to stop receiving messages, displayed clearly and conspicuously.
6. **Honor the opt-out within 10 business days** - no charge, no hoops, no
   "reply to confirm".
7. **Monitor what others do on your behalf** - if a vendor sends on your
   behalf, you are responsible.

Practical consequences:

- The opt-out address must be monitored and answered by a human within 10
  business days.
- Keep a permanent suppression list. Check it before every send.
- One click, no retention, no "are you sure" loops.
- Never charge for an unsubscribe.

## TCPA (calls and SMS)

- Marketing texts and automated calls generally require **prior express written
  consent** (TCPA and the 2024 FCC consent ruling tightened the standard).
- Consent for email is not consent for SMS. A website form that says "you
  agree to receive texts" is explicit; a generic privacy-policy agreement is
  not.
- Keep the consent record: timestamp, IP or form source, exact wording, and
  the phone number.
- Honor STOP keywords immediately (TCPA requires prompt opt-out - treat
  "STOP" as immediate).
- Do not use an SMS sender ID that impersonates a company the user did not
  consent to.

Practical consequence: for most US B2B outbound, **email plus LinkedIn manual
touch** is the safe default. Add SMS only where you have documented consent.

## State laws (stricter than CAN-SPAM)

- **California (CCPA/CPRA)**: opt-out of "sharing" for cross-context behavioral
  advertising; data broker registration; California privacy notice for
  qualifying businesses.
- **Colorado, Connecticut, Utah, Virginia, and others**: opt-in consent for
  many marketing uses, plus universal opt-out recognition.
- **Massachusetts, Illinois, and others**: written opt-in plus a data
  retention limit.
- **Texas, Florida, and others**: email-specific consent statutes.

Default to opt-in everywhere unless counsel says otherwise. That is more work
and much less risk.

## Platform rules that are not law but decide whether you deliver

- **LinkedIn**: automation that scrapes or sends through the platform can get
  the account and the domain banned. Manual, low-volume, personalized.
- **Gmail and Microsoft 365**: bulk senders need SPF, DKIM, and DMARC aligned,
  a low spam rate, and one-click unsubscribe support. Volume ramps slowly.
- **Major inboxes**: an address sent to twice without a reply degrades
  reputation quickly. One follow-up, then stop.

## Record keeping

Keep, per contacted account: date, time (ET), source URL of the contact data,
the exact copy sent, the opt-out date if any, and the reason for contact.
If a recipient complains, you need this record to answer "why did you contact
me" and to prove a timely opt-out.

## The suppression list

- One file, append-only, never deleted.
- Columns: email, date, source, reason.
- Checked automatically before every send.
- Includes: prior opt-outs, hard bounces, complaints, anyone who asked not to
  be contacted, role accounts (`info@`, `sales@` when the user asked to
  unsubscribe).
- Retained for the life of the business plus the limitation period.

## What this skill will not do

- Send email. It produces drafts; a human sends.
- Scrape personal data, buy lists, or use leaked databases.
- Circumvent a platform's anti-automation controls.
- Send to a list without a human reviewing each message.
- Continue after an opt-out.
