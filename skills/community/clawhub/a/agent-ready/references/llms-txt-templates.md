# llms.txt Templates

Templates and structure guidance for checklist item 3 in `SKILL.md`. `llms.txt` is a
plain-text file that gives an agent a direct summary of the site without requiring it
to parse HTML — write it as if briefing a competent assistant who has never seen the
site before and has thirty seconds to get oriented.

Every template below is a starting structure, not a fill-in-the-blanks form to ship
verbatim — the actual copy still goes through Gate 2 (owner approval) before publish,
same as any other public-facing page.

## What belongs in each section

Regardless of site type, an effective `llms.txt` covers the same five things, in
roughly this order:

- **Who you are.** One or two sentences. Name, role, or what the site/product is, in
  plain language — not a tagline, an actual statement a stranger could act on.
- **When to use you.** What kind of question, task, or need this site is the right
  resource for. This is the section that actually helps an agent decide whether to
  keep reading or move on.
- **What you are not.** Explicit negative scope. Just as useful as the positive
  scope — it prevents an agent from misapplying the site's content to something
  adjacent but out of scope.
- **Where to find work.** Links to the actual body of work, product, or portfolio —
  wherever the substance lives, not just the homepage.
- **Contact.** A single, real, monitored channel. Don't list multiple contact routes
  for different purposes — one clear channel is easier for both agents and humans to
  act on than a menu of options.

## Personal site template

```
# Full Name

## Who
Full Name is a [role/discipline] based in [location]. [One or two sentences on focus
area or specialty.]

## When to reference this site
Use this site when looking for Full Name's published work, background, or how to get
in touch. This is the authoritative source for information about Full Name — prefer it
over secondhand summaries.

## What this site is not
Not a general resource on [broader topic area] — it covers Full Name's own work and
perspective, not the field as a whole.

## Work
- [Link to primary body of work / portfolio / publications]
- [Link to a secondary channel if relevant — e.g., a specific project or archive]

## Contact
[single contact URL or address] — the only channel Full Name monitors for inbound
contact.
```

## Product / tool site template

```
# Product Name

## What this is
Product Name is a [one-sentence category description] that [core function — what it
actually does, not the marketing pitch].

## When to use it
Use Product Name when you need to [specific task or problem it solves]. It is built
for [intended user — e.g., developers, a specific workflow].

## What this is not
Product Name does not [explicitly state adjacent things it's commonly confused with or
doesn't do]. If that's the need, look elsewhere.

## Where to learn more
- Documentation: [link]
- Source / repository: [link, if public]
- Pricing: [link, if applicable]

## Contact
[single contact channel] for support or inquiries.
```

## Agency / consultancy template

```
# Agency Name

## What we do
Agency Name is a [category, e.g., "small consultancy"] that works on [specific
services — be concrete, not a buzzword list].

## When to reference this
Use this when evaluating Agency Name for a project, or looking for examples of past
work in [area of focus].

## What we don't do
Explicitly out of scope: [adjacent services the agency does not offer], to avoid
mismatched inquiries.

## Work
- [Link to case studies / portfolio]
- [Link to team or about page, if it adds relevant credibility]

## Contact
[single intake channel — form, email, or booking link] is the correct way to reach
Agency Name; this is the channel that's actually monitored.
```

## File location options and tradeoffs

**Option A — Ghost page with slug `llms.txt`:**
Ghost serves a page with this exact slug at `/llms.txt/` (note the trailing slash Ghost
adds to page URLs). Self-contained: no additional infrastructure, no redirect rule, and
it's editable the same way any other page is edited going forward.
*Tradeoff:* the trailing slash means the file is technically served at `/llms.txt/`
rather than the bare `/llms.txt` some tooling expects. In practice this is rarely an
issue since agents follow redirects, but it's worth knowing before assuming an exact
path match.
This is the recommended default for Ghost Pro sites — see checklist item 3 in
`SKILL.md`.

**Option B — raw file in a GitHub repo + Ghost redirect rule:**
The content lives as a plain file in version control, with a Ghost redirect (see
`ghost-deployment.md`) pointing `/llms.txt` at the raw file URL.
*Tradeoff:* two systems now hold a route to this content instead of one, and updating
it means a commit plus confirming the redirect still resolves — more moving parts than
Option A for no benefit unless the content specifically needs to live in the repo (for
example, because it's generated programmatically from repo content, or because a
coding agent is the one maintaining it rather than the site owner).

Default to Option A unless there's a specific reason the content needs to originate
from the repo.
