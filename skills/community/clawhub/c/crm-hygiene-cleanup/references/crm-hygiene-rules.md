# US contact data rules for a clean CRM

Reference for the CRM Hygiene Cleanup skill. Every limit and rule below is a US-facing constraint the workflow has to respect.

## Normalizing US contact fields

- Email: trim spaces, lowercase the domain and remove display-name brackets.
- Phone: keep the ten digits and move any extension into its own field.
- State: use the two-letter USPS code, for example CA, TX or OH.
- Name: split first and last, and keep a suffix out of the last-name field.

## Keys that identify a duplicate

- The email address is the strongest key when it belongs to a person.
- Domain plus name catches one person listed on two records.
- The phone number catches the same record imported from two systems.
- A job title change should not create a second record.

## What stays out

- No bought lists, no scraped personal emails and no guessed email patterns.
- Keep a merge log so a wrong merge can be reversed.
- Keep the consent date, because state privacy laws depend on it.
- Flag a role inbox when it is the only address you have, since many buyers never read it.
