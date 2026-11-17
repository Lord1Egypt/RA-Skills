# Message standard

Every buyer-facing draft, including a direct note, referral request, listing,
public post, partnership proposal, or inbound response, must pass every check
below before it can be presented for approval. A passing draft is still staged;
the human must review it and separately approve the exact external action
immediately before sending or publishing.

Run Authorization permits this private drafting and review without another
approval; it never permits delivery of the message. Return the reviewed draft
to `moneyprinter` with Money Machine Run state rather than stopping at a
report-only handoff.

## Required standards

- **Specific observed situation**: name one real, relevant situation observed
  through permitted access. Do not claim a problem, history, or result that is
  not known.
- **Honest identity and intent**: identify the sender or represented business
  truthfully and state the commercial or helpful intent plainly.
- **Short enough to read once**: use one compact purpose, context, offer, and
  next step; remove background that does not help a recipient decide.
- **No fake familiarity**: do not imply a relationship, referral, shared
  experience, personal research, or prior conversation that did not occur.
- **Easy to decline**: include a plain, pressure-free opt-out or no-response
  path; do not use threats, repeated follow-up, or deceptive urgency.
- **No unverified performance claims**: remove or qualify outcome, benchmark,
  testimonial, availability, price-saving, or conversion claims that lack
  evidence. Describe the bounded deliverable instead of guaranteeing a result.
- **Human reviewed before sending**: mark the draft as unapproved until a human
  reviews the final exact payload, destination, cost, and correction path.

## Review record

Attach this short record to every staged draft:

```markdown
Observed situation and permitted source: [fact/source]
Identity and intent disclosed: [yes/no, exact wording]
Once-readable: [yes/no]
Easy decline: [exact wording]
Claims verified or removed: [list]
Human review: pending
External action approval: pending
```

After an immediately preceding exact approval, the current host may perform
only that approved action, record an `Action receipt`, and return it to
`moneyprinter`. The receipt replaces `pending` with the exact payload,
destination, channel/account, execution time, cost, observed result or error,
evidence label, and rollback or correction status. Broad, batch, stale, or
materially changed permission is invalid.

## Negative example

Do not write: "I saw your business is losing thousands every week. My proven
system guarantees revenue—reply today before the last slots disappear."

It asserts an unverified result, uses pressure, and may falsely imply research
or scarcity. Replace it with a short, truthful, specific draft that names the
bounded deliverable, qualification, price/payment condition where appropriate,
and an easy decline.
