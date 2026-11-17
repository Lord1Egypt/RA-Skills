---
name: contracko-create
description: Takes a new contract from questionnaire to drafted, signed and filed in Contracko. Use to create, draft or generate an agreement, fill a template, send for signature, or chase a signer.
---

# Creating a contract and getting it signed

The forward half of the lifecycle: nothing exists yet, and the job is to end with a signed agreement added to Contracko.

Most of this flow is app work today. The tail of it, filing the executed copy, is a tool call, and it is the step that decides whether the contract is findable in a year. Run the whole flow with the user rather than stopping at the first step you cannot execute.

## Say this before you draft anything

**A contract a model wrote is a draft, and it needs a human with legal competence to review it before anyone signs.** Say so to the user, once, plainly, at the point they are about to act on your output rather than buried at the end. Who that human is scales with the deal: an in-house lawyer or jurist for anything material, external counsel where the value or the jurisdiction warrants it, and at minimum somebody whose job it is to read contracts.

This is not a disclaimer to recite and move past. Contract language fails in ways that read fine: a term that is unenforceable in the governing jurisdiction, a cap that does not survive local law, an indemnity that quietly swallows the cap, a clause that contradicts another clause forty lines away. Fluent prose is exactly what a model produces and exactly what hides those.

**Start from a template the organisation has already had reviewed.** A known-good precedent with your changes marked is reviewable in minutes, because a lawyer reads the delta. The same contract generated from scratch has to be read in full, by someone who has no idea which parts you invented. Ask what they already use before offering to write anything, and where they have nothing, say that the first one through this route is the one that most needs proper review.

Where the user asks for words rather than mechanics, drafting a clause, a summary, a negotiation position or a redline argument is ordinary work you can do well. Do it. Just never present it as legal advice, and never let it reach a signature without the review above.

## The flow

1. **Establish what the contract has to do.** The questionnaire below.
2. **Offer a handoff, but persist it only after an explicit destination choice and consent.**
3. **Draft it** from a template — app step.
4. **Route it for signature** — app step.
5. **Add the executed copy** — [contracko-import](../contracko-import/SKILL.md), and this one is yours.
6. **Set the reminder** that will matter in a year — [contracko-review](../contracko-review/SKILL.md).

Steps 3 and 4 have no tool yet, so name the step, say it happens in Contracko, and keep moving. The parts either side are real work you can do well.

## Step 1: the questionnaire

This is where an agent adds most of the value, because the terms people forget are the ones that cost money later. Ask in this order, and stop when the user has decided rather than when the list is done.

**The shape of the deal**
- Which entity of ours is contracting? Check `clm_list_parties` for `isOwned` records rather than asking twice.
- Who is the counterparty, and is there already a party record? `clm_list_parties`.
- What is being bought or sold, in one sentence.
- What does it cost, in which currency, and on what billing rhythm?

**The dates that decide everything later**
- Start date, and whether it is signature date or a fixed date.
- Term: fixed end date, or open-ended?
- Does it renew automatically, and for how long?
- **Notice period.** Ask this explicitly and never let it default. It is the single field that turns a cancellable contract into another year of spend, and it is months earlier than the end date.

**The terms that hurt in a dispute**
- Liability cap, and whether it is mutual.
- Governing law and jurisdiction.
- Termination for convenience: does either side have it, and on what notice?
- Confidentiality, data processing, IP ownership, where each is relevant to the subject.

**The filing question**
- Which contract type does it belong to, and are its custom fields populated? `clm_list_contract_types`.

Read the answers back before drafting. A questionnaire whose answers were never confirmed produces a contract nobody checks.

## Step 2: the handoff

Signature takes days or weeks, in an app, with the agent gone. The user comes back in a new conversation that remembers none of this, and **a drafted contract has no record in Contracko**, because nothing is filed until step 5. So unless the answers are written down, the notice period you just made someone decide is lost between the deciding and the signing.

The handoff can contain sensitive contract details. Before writing it, show the fields you plan to record and ask the user to choose a destination:

- an exact local path the user names and can secure
- an encrypted vault or notebook destination the user names
- a chat-only copy that the user saves themselves

State the exact destination and contents, then ask for explicit consent before writing. Do not write a handoff to the current working directory, a temporary directory, plugin data, logs, transcripts, a remote store, or Contracko without that choice and consent. Never add credentials or full contract text to a handoff unless the user asks for it.

If the user does not choose a destination and give consent, do not persist the handoff. Provide a redacted block in the response for the user to save themselves, and say that it is not stored by the agent.

For an explicitly approved secure destination, record at minimum:

- the parties, and which entity of ours is contracting
- start date, end date or open-ended, renewal term
- **notice period, and the date it falls due**
- value, currency, billing rhythm
- liability cap, governing law, jurisdiction
- the contract type it should be filed under
- anything the user decided against, and why

That last line is the one people skip and later need. A record of the rejected term is what stops the same negotiation happening twice.

When a later conversation picks this up, read the handoff before asking anything. Re-running the questionnaire on someone who already answered it is how an agent loses their trust in one move.

## Step 3: drafting — app step

Contract creation from a template, filling fields, and status changes are done in Contracko today, not through this connection.

Do not claim to have created anything inside Contracko: the drafting happens there, by the user, and what you produced is text they take with them.

This is also where the review rule bites hardest, so repeat it here rather than assuming it carried: whatever goes into that template needs a legally competent human over it before signature.

## Step 4: signature — app step

Sending for signature, signature status and chasing a signer have no tool. Say so, and point at the contract in the app.

Where the user asks "where is that contract", check first whether it is already filed and just unsigned: `clm_list_contracts` and `clm_get_contract` show `status`, and `entityStatus` shows whether anyone has confirmed the record. That often answers the real question without touching the signature flow at all.

## Step 5: file the executed copy — yours

This is the step that gets skipped, and the one that makes the previous three worth anything.

Once the signed PDF exists, import it with `clm_import_contracts`, which extracts dates, parties, and terms into a managed contract. [contracko-import](../contracko-import/SKILL.md) has the detail. If the user also asked for a folder, use the confirmed filing workflow in [contracko](../contracko/SKILL.md) after import.

Then reconcile against the handoff from step 2. Extraction reads what the document says; the handoff is what the user believed they agreed. Where the notice period, renewal term or liability cap differ, that gap is the most useful thing you will tell them all day, so surface it rather than quietly trusting the extraction.

New records land as `entityStatus: "pending-review"`, which means the extraction is unconfirmed. Say so when you hand back.

## Step 6: the reminder

A filed contract with no reminder is a renewal nobody sees coming. After import, list events, then add a reminder on the `end` system event (renewal) or `notice` if they care about the notice window. [contracko-review](../contracko-review/SKILL.md) has the calls. Prefer notice over end when both exist and they asked not to miss the window to get out.
