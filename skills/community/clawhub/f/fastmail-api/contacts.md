# Contacts

The address book is the part of this API where a bad write destroys data that was never backed up anywhere. Read broadly, write narrowly, and never let a sync loop touch it.

**Before writing a person anywhere**, read the shared `~/Clawic/data/contacts/contacts.md` and look for the address — the person may already be recorded by another skill, and a duplicate row is how two skills start contradicting each other. **After a person comes up who the user will deal with again**, add or update their row in that shared file, in place, keyed by email or handle; the full protocol travels in `memory-template.md`. Address book ids resolved along the way go in the address-book sub-table of `## Account Map` in `~/Clawic/data/fastmail-api/memory.md`; individual card ids are re-resolved by email query every time and never stored, because a card deleted and recreated keeps the name and changes the id.

**Contents:** [Which Object Model](#which-object-model) · [Reading](#reading) · [Writing Safely](#writing-safely) · [Duplicates](#duplicates) · [Groups](#groups) · [The Shared Contacts Box](#the-shared-contacts-box) · [What Never Gets Copied](#what-never-gets-copied)

## Which Object Model

Two generations exist, and they are not interchangeable:

| Model | Object | Shape |
|---|---|---|
| JSContact | `ContactCard` | Structured JSContact: `name` with components, `emails`/`phones`/`addresses` as keyed maps, `preferredLanguages`, `links` |
| Legacy | `Contact` | Flat: `firstName`, `lastName`, `emails: [{type, value}]`, `phones`, `addresses` |

**The session decides.** Read the contacts capability URN and the account's `accountCapabilities` (`session.md`) and use the object model that matches; a `Contact/get` against a server exposing only `ContactCard` returns `unknownMethod`, which is a model mismatch and not a permissions problem. Never mix them in one request, and never assume from a code sample which one is in play.

Everything below is stated in terms of the concepts both share — cards, emails, groups — with the property names resolved from whichever model the session advertises.

## Reading

- `ContactCard/get` (or `Contact/get`) with `ids: null` returns the whole address book. On a real address book that is thousands of objects and can exceed `maxObjectsInGet`; page it, or use `/query` with a filter first.
- Filter narrowly for a lookup: matching on the address the user just mentioned beats fetching everything and searching locally, and it keeps the address book out of context.
- `AddressBook/get` lists the address books; an account can have several, and a shared one may be read-only per `myRights`.
- For "who is this" during mail work, the fetched message's `from` field usually answers it. Reach into contacts only when the question is about the *person*, not the message.

## Writing Safely

- **Patch, never replace.** `{"emails/work/address": "new@example.com"}` changes one thing; sending a whole card object replaces every field, and the fields you did not include are gone. There is no undo and no Trash for contacts.
- **Snapshot before any destructive contact write** — a merge, a delete, a bulk field rewrite — to `~/Clawic/data/fastmail-api/snapshots/<date>-contacts-<what>.md` with the full prior card of every affected id. This is stricter than the mail rule because mail has a Trash and contacts do not.
- Creating is low risk; updating existing cards is where the loss happens. Treat any batch update of more than a handful of cards as an irreversible operation and confirm it as one.
- Preserve unknown properties. A card written by another client can carry fields this skill has no opinion about; a patch leaves them alone, a replace erases them.

## Duplicates

Deduplication by email address is wrong and it is the default thing everyone tries.

| Case | Why address-matching fails | Correct move |
|---|---|---|
| One person, three addresses | Produces three "people"; merging by address never joins them | Match on name plus any shared address, then merge |
| Two people, one shared family address | Collapses two real people into one | Never merge on address alone |
| Same person, one card from a phone sync and one typed | Fields differ in formatting, not content | Merge field by field, preferring the more complete value |
| A card with no email at all | Invisible to address-based dedupe entirely | Match on name and phone |

The merge procedure: snapshot both cards → build the merged card as a patch onto the one being kept (the older id, so references survive) → verify by reading it back → then destroy the other. Destroying first and rebuilding second is how a merge loses a phone number.

Report duplicates as a proposed list with the merge for each one shown. Never auto-merge a set larger than `confirm_threshold`.

## Groups

Groups are membership objects referencing card ids — a card belongs to a group, the group does not contain the card's data.

- Deleting a group does not delete its members. Deleting a member removes it from every group silently.
- Groups are the sane target for a mailing list of real people: resolve the group to its members, then verify each address before a send (`sending.md`).
- A group with a stale member is invisible until a send goes to the wrong person. Re-resolve at send time, never from a cached list.

## The Shared Contacts Box

The Fastmail address book and `~/Clawic/data/contacts/contacts.md` are different things and the distinction is load-bearing:

| | Fastmail address book | Shared contacts box |
|---|---|---|
| Holds | Everything, including autocompleted addresses | People the user will deal with again |
| Written by | Mail clients, phone sync, this skill | Every Clawic skill that deals with people |
| Purpose | Autocomplete and card storage | Cross-skill context: role, channel, relationship |

**Never mirror one into the other.** A bulk import of the address book into the shared box replaces a curated file with thousands of autocompleted strangers, and it cannot be undone from the JMAP side. Write a row when a person actually matters — a client, a counterparty in an ongoing thread, someone the user asked you to remember.

Row shape, identity key, retirement, scale cut and the foreign-column rule are all in `memory-template.md`, so they work whether or not any other skill is installed.

## What Never Gets Copied

Contact notes are where people paste things they should not. When writing a card into the shared box, or a snapshot, or any summary:

- Never a password, PIN, security answer, door code, or account number found in a contact's notes field.
- Never a full date of birth or national id unless the user asked for exactly that to be kept, and then only in the Fastmail card, never in the shared box.
- Health details, when they appear in a card, stay in the card. They are not summarized into the shared box and not repeated in a session summary.

The card itself can hold whatever the user put there; what leaves the address book and lands in a Clawic file is a deliberate, minimal subset.
