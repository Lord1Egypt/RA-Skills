# Appointments — Getting Value From Twelve Minutes

The average consultation is short and the patient speaks for about twenty seconds before the first interruption. Everything below is about surviving that structure: what to bring, what to say first, and what to leave with.

**Before preparing**, read `## Current Concerns` in `~/Clawic/data/doctor/memory.md`, the recent rows of `~/Clawic/data/doctor/episodes/<year>.md`, and `~/Clawic/data/health/profile.md` (conditions, medicines, allergies, recent measurements). The prep sheet is assembled from stored facts, not from the person's memory at the desk — that is the entire reason the record exists. Routing below follows `care_context`.

## The Prep Sheet

One page, in this order, because it matches how the clinician thinks:

1. **The one-line reason for the visit**, said first, in the person's own words.
2. **Timeline**: when it started, how it has changed, what makes it better or worse.
3. **What worries them specifically** — say it out loud. Unstated fear ("is this cancer?") is the reason people leave unsatisfied by a technically correct consultation.
4. **Current medicines and supplements**, with doses — the printed list, not a recollection.
5. **What has already been tried**, and what happened.
6. **Measurements**, with dates: home blood pressure series, glucose, weight, temperatures, peak flow.
7. **The two or three questions** they most want answered, ranked. Anything past three will not fit.

Three items maximum per appointment. A list of eight complaints guarantees the important one gets four minutes at the end.

## The Questions That Change The Answer

- **What is the most likely explanation, and what else could it be?**
- **What would need to happen for me to come back sooner?** — this converts a vague follow-up into a tripwire.
- **What are the benefits and risks of this, what happens if I do nothing, and are there alternatives?** (The BRAN frame: Benefits, Risks, Alternatives, Nothing.)
- **When and how will I get the result, and who calls whom if it is abnormal?** Results falling into a gap between systems is a routine failure mode; naming the responsibility closes it.
- **Can you write down the diagnosis and the plan?** A written plan is recalled far better than a spoken one; roughly half of spoken medical information is forgotten immediately.

**Teach-back** is the check that costs nothing: repeat the plan back in your own words and let the clinician correct it. It catches the misunderstanding while it is still free.

## Telehealth, And What It Cannot Do

Good for: medication reviews, results discussions, follow-ups on a known problem, mental-health consultations, prescriptions for a stable condition. Bad for: anything that needs hands or eyes on the body — abdominal pain, a lump, a rash whose blanching matters, an ear, a joint, a child who looks unwell. If the consultation ends with "it's hard to say without examining you", the visit was the wrong format; ask for an in-person slot rather than accepting a guess.

Before a video call: good light, the affected area visible, medicines to hand, measurements written down, and a phone number in case the video drops.

## Referrals And Waiting

- Ask **which pathway** the referral goes on and its expected wait; urgent-suspected-cancer pathways have target times, routine ones do not.
- Ask what to do while waiting, and what would justify escalating the referral.
- Cancellation lists are real and under-used: asking to be called for short-notice slots often halves the wait.
- If the referral does not arrive as a letter or appointment within the stated window, chase it — referrals fail silently more often than anyone admits.

## Second Opinions

Legitimate, and best framed as adding information rather than as distrust: "I'd like another perspective before deciding." Worth seeking when the diagnosis does not explain all the findings, when the treatment is major or irreversible, when the condition is rare, when the recommendation is to do nothing and symptoms persist, or when the first clinician's own confidence is low.

Bring the whole file — the imaging on disc, the reports, the timeline. A second opinion built on a summary is a second opinion on the summary. When two opinions conflict, the productive question is "what fact would change your view?", asked of both; a difference in weighting a known trade-off is a genuinely different situation from a difference about what is going on.

## Records, And Getting Them

- Requesting a copy of the record is a right in most jurisdictions and usually free.
- The ones that keep mattering — discharge summaries, operation notes, imaging reports, allergy documentation, vaccination history, biopsy results — each get a summary file at `~/Clawic/data/doctor/artifacts/<kebab-name>.md`: what it says, its date, the clinician, and where the original is held. Its `## Boxes` line goes in the same turn. The original document itself is never copied in.
- **Check them.** Errors in the medication and allergy lists are common, and both propagate through every future encounter.
- Anything corrected — a wrong allergy label, a condition that was excluded — gets corrected in the stored profile as well, with the date.

## When It Goes Wrong

If the person feels dismissed, three sentences that reliably reopen a consultation: "I do not think I have explained this well — can I start again?" · "What is the worst thing this could be, and how have we excluded it?" · "Please record in my notes that I raised this and that we agreed not to investigate it." The third is not a threat; it changes the clinician's own risk calculation, and it creates the paper trail that matters if the picture changes.

Formal routes — the practice's complaints process, a patient advocate, the professional regulator — exist for behaviour and safety, not for disagreement about clinical judgement.

## Cost And Coverage

Where `care_context` is `insurance-gated`, add three questions to the prep sheet: is this provider in network, is prior authorisation needed for this test or drug, and is there a generic or a lower-tier alternative. Ask for the procedure code when a cost estimate matters. The insurance plan itself, and its monthly premium, are financial facts and belong in the shared finances box, not in the health record.

## Where This Goes

**Write in the same turn** (`memory-template.md`):

- The prep sheet → `~/Clawic/data/doctor/artifacts/visit-prep-<topic>.md`, with its `## Boxes` line and the read condition "read before the appointment and update after it".
- The appointment → the shared `~/Clawic/data/bookings/<year>.md`: `Date | Type (medical) | Locator | Provider | Status | Notes`. Identity is the locator; when the clinic gives none, use `<clinic-kebab>-<date>` so the same appointment is never entered twice. Read the file before adding, update in place, and a cancelled appointment keeps `status: cancelled` with its reason rather than vanishing. If the file already exists with different columns, match its columns and add anything missing as a trailing note — never rewrite its header.
- The clinician → the shared `~/Clawic/data/contacts/contacts.md`: `Name | Key | Role | Preferred channel | Context | Last contact | File`. The key is the lowercase email, else the handle, else `<kebab-name>` plus a stable disambiguator; `Role` carries the specialty ("GP", "cardiologist", "pharmacy"). Read before adding, update the existing row in place, and past 15 people each gets `~/Clawic/data/contacts/<name>.md` with `contacts.md` left as the index. A clinician no longer involved has their row updated, not deleted. Never touch rows this skill did not create, and if the file already exists with different columns, match its columns and add anything missing as a trailing note — never rewrite its header.
- What was said and decided → an episode row in `~/Clawic/data/doctor/episodes/<year>.md`, plus any new diagnosis into `## Conditions` and any medicine change into `## Medications` of `~/Clawic/data/health/profile.md`.
- A health-insurance premium or plan → the shared `~/Clawic/data/finances/subscriptions.md` (`Name | Amount with currency | Cycle | Renewal | Notes`). Identity is the subscription name; read before adding, update in place, and delete the row when the policy ends — that deletion is why the file is never split, it stays one small table. The amount carries its currency inside the value (`64 EUR`, not `€64`). If the file already exists with different columns, match its columns and add anything missing as a trailing note — never rewrite its header. The member ID stays there as working data, and the portal login never leaves its pointer.
