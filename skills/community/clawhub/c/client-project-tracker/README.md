# Client Project Tracker

A conversational OpenClaw skill for freelancers and consultants to track clients, projects, deliverables, deadlines, invoices, and client relationships. Light CRM with project history and communication notes.

## What It Does

- **Client Directory (Light CRM)** -- contact info, communication preferences, project history, and relationship notes
- **Project Tracking** -- status, deadlines, deliverables, and scope notes for every active project
- **Deliverable Management** -- track what you owe, when it's due, and approval status
- **Invoice Tracking** -- deposits, milestones, final payments, and overdue alerts
- **Communication Log** -- brief notes on key client interactions for context continuity
- **Dashboard** -- see all active work, upcoming deadlines, and revenue at a glance
- **Proactive Nudges** -- flags overdue deliverables, unpaid invoices, and quiet clients

## Privacy and Data Handling

This tracker holds client contact details, notes about your conversations, and your business finances. Here's how it's handled:

- **Local only.** Everything is saved in one file, `client-data.json`, in the skill's data directory. The skill makes no network calls. The file isn't encrypted, so anyone with access to the computer or its backups can read it.
- **You're told before anything is saved.** The first time the tracker saves something, the assistant says what it keeps and where.
- **Only what's needed.** Business contact details and short conversation summaries. It never saves payment card or bank numbers, passwords, tax IDs, or Social Security numbers.
- **Careful about what it shows.** Lookups cover the client you asked about. Anything drafted for someone else leaves out revenue and internal notes unless you ask.
- **Delete anytime.** Remove one client and everything linked to them, or clear the whole tracker.
- **Only when you're tracking.** It activates when you're recording or looking up something in your tracker, not on general talk about clients or invoicing.

## Example Usage

**Add a client:**
> "New client: Riverside Church. Contact is Pastor Mike. Sarah referred them."

**Set up a project:**
> "The website project is $3,500 fixed. Deadline April 15."

**Check what's due:**
> "What do I need to deliver this week?"

**Log communication:**
> "Had a call with Pastor Mike. He approved the homepage."

**Track payments:**
> "Sent the final invoice to Martinez Law. $2,000."

**Get an overview:**
> "What's my workload look like?"

## Installation

Copy the `client-project-tracker` folder into your OpenClaw skills directory and restart your agent.
