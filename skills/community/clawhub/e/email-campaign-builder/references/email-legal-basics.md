# What a US marketing email has to carry before it sends

Reference for the Email Campaign Builder skill. Every limit and rule below is a US-facing constraint the workflow has to respect.

## Required by CAN-SPAM

- Accurate header information: the from name, the from address and the reply-to address.
- A subject line that reflects the content of the message.
- A valid physical postal address of the sender.
- A clear opt-out notice, honored within 10 business days, and the mechanism has to work for at least 30 days.

## Delivery requirements at Gmail

- SPF, DKIM and DMARC records for every sending domain, with the From domain aligned.
- One-click unsubscribe headers on marketing and subscribed-list sends from bulk senders.
- A spam rate reported in Postmaster Tools that stays under 0.30%.
- Unsubscribe requests handled promptly; providers ask for same-day handling.

## Claims in the body

- A price, a discount, a comparison and a performance number are all advertising claims.
- A testimonial is an endorsement; the material connection has to be disclosed.
- The disclosure has to sit next to the claim, in plain language.
