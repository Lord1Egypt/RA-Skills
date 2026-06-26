# Family Health Tracker

A conversational OpenClaw skill that keeps medical records organized for your whole family. Tracks medications, allergies, doctor visits, immunizations, insurance, prescriptions, chronic conditions, and growth milestones. Smart reminders for checkups, refills, and immunization schedules. All data stored locally on your device.

## What It Does

- **Family Profiles** -- each person gets a full health record with allergies, medications, conditions, and emergency notes
- **Visit Logging** -- log doctor, dentist, specialist, and urgent care visits with notes, prescriptions, and follow-ups
- **Immunization Tracking** -- full CDC childhood schedule built in, flags when doses are due
- **Medication Management** -- track dosages, prescribers, pharmacies, and refill dates with reminders
- **Insurance Info** -- carrier, plan type, and PCP on file for each family member (no sensitive IDs stored)
- **Growth Log** -- track height, weight, and percentiles for kids over time
- **Provider Directory** -- doctors, dentists, specialists with contact info and notes
- **Smart Reminders** -- proactive nudges for checkups, dental cleanings, immunizations, and refills
- **Pre-Appointment Prep** -- pull up everything you need before a visit in one shot

## Permissions and Privacy (read before installing)

This skill is instruction-only — it directs the assistant to read and write a single local file. It does not bundle any executable code, runs no background processes, makes no network calls of its own, and has no telemetry.

**What the skill touches**

- **Local file write**: creates and updates `health-data.json` in your working directory. No writes outside that directory.
- **No external tool calls**: the skill does not direct the assistant to use Gmail, browser automation, web search, or any third-party API. If your assistant has those tools, the skill simply doesn't reach for them.
- **No transmission**: nothing is sent to the skill's author, ClawHub, or any third party.

**Sensitive data the skill will refuse to store**

- Social Security numbers
- Full insurance policy numbers (carrier and last 4 digits are sufficient)
- Bank, credit card, or HSA account numbers (copay amounts are fine)
- Verbatim therapy notes (severity flags and provider names are fine)

If you volunteer any of the above, the assistant will redirect you and skip the storage.

**Sharing or exporting**

When you ask for a printable summary, emergency card, or school form, the assistant generates it locally or in chat. Nothing is auto-shared anywhere.

**Not a medical advisor**

This skill records information. It is not a substitute for a clinician. Questions about safety, diagnosis, or what a symptom means should go to your healthcare provider.

## Example Usage

**Log a visit:**
> "Took Emma to Dr. Patel today for her checkup. 42 inches, 38 pounds. Everything looks good."

**Quick lookup:**
> "What are Emma's allergies?"

**Prep for an appointment:**
> "We have a dentist appointment for the kids tomorrow."

**Family overview:**
> "Give me a health summary for the whole family."

**Log a medication:**
> "Emma started Zyrtec today. 5mg daily."

## Installation

Copy the `family-health-tracker` folder into your OpenClaw skills directory and restart your agent.
