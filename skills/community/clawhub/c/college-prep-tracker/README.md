# College Prep Tracker

A conversational OpenClaw skill that manages the entire college application process for one or more students. Tracks schools, applications, essays, test scores, recommendation letters, scholarships, financial aid, and every deadline. Built-in junior/senior year timeline.

## What It Does

- **Student Profiles** -- GPA, test scores, extracurriculars, intended major, and academic snapshot
- **College List** -- safety/match/reach categorization with deadlines, application status, and campus visit notes
- **Application Tracking** -- essays, supplementals, and rec letters with per-component status
- **Recommendation Letters** -- who's been asked, what's submitted, what's overdue
- **Scholarship Tracker** -- external scholarships with amounts, deadlines, requirements, and essay status
- **Financial Aid** -- FAFSA tracking, CSS Profile, and side-by-side aid package comparison across schools
- **Built-In Timeline** -- junior and senior year milestones auto-suggested when a student is added
- **Multi-Student** -- track multiple kids through the process simultaneously
- **Proactive Nudges** -- flags approaching deadlines, unfiled FAFSA, and incomplete applications

## Privacy and Data Handling

This skill keeps an ongoing record about students, who are often minors, including grades, test scores, and financial-aid details. Here's how it's handled:

- **Local only.** Everything is saved in one file, `college-data.json`, in the skill's data directory. The skill makes no network calls. The file isn't encrypted, so anyone with access to the computer or its backups can read it.
- **You're told before anything is saved.** The first time you add a student, the assistant says what it will store and where.
- **Only what's needed.** First names only. For financial aid it keeps filing status, deadlines, and aid amounts, never FSA IDs, passwords, tax returns, account numbers, or detailed household finances.
- **See it or delete it anytime.** Ask to see everything saved about a student, delete one student's data, or clear the whole tracker. After decisions are final, the assistant offers once to clear the record.
- **Not shared.** Tracker contents aren't sent to other people, services, or skills unless you ask for that specific thing.
- **Only when you're tracking.** The skill is meant to activate when you're setting up or updating a specific student's tracker, not on general college questions.

## Example Usage

**Set up a student:**
> "Emma is a junior, class of 2027. GPA 3.8 weighted. ACT 28. Interested in nursing."

**Build a college list:**
> "Add UNC as a reach, NC State as a match, ECU as a safety."

**Track an essay:**
> "Emma started her UNC essay. She has a rough draft."

**Log a rec letter:**
> "Emma asked Mrs. Johnson for a rec letter today."

**Track scholarships:**
> "She's applying for the Rotary Club scholarship. $2,500, due Feb 1."

**Compare aid packages:**
> "UNC offered $8,000/year, NC State offered $12,000/year."

## Installation

Copy the `college-prep-tracker` folder into your OpenClaw skills directory and restart your agent.
