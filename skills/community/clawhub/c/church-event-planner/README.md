# Church Event Planner

A conversational OpenClaw skill for planning and managing church events with church-specific intelligence: ministry team coordination, volunteer rotation tracking with burnout detection, sermon series alignment, and liturgical calendar awareness.

**Current version: 1.1.0**

## What's new in 1.1.0

- **Ministry Team Coordination**: link events to teams (Worship, Children's, Hospitality, etc.) with team-level views and clean handoffs
- **Volunteer Rotation & Burnout Detection**: master volunteer roster with skills, blackout dates, preferences, and an auto-calculated burnout score that flags overcommitted volunteers before they hit the wall
- **Sermon Series Alignment**: link events to active sermon series and generate themed content, discussion questions, and promo blurbs that tie into the week's passage
- **Liturgical Calendar Intelligence**: surface upcoming Advent, Lent, Holy Week, Pentecost (and more) with typical event suggestions per season; respects the operator's tradition setting

See [CHANGELOG.md](CHANGELOG.md) for the full release history.

## What It Does

Tell it about an event in plain language and it builds a full planning record:

- **Events**: any church event from potlucks to conferences, with dates, status, and notes
- **Smart Templates**: built-in planning checklists for VBS, Easter/Christmas services, retreats, fundraisers, outreach events, weddings, and funerals. Auto-generates tasks with due dates calculated backward from the event
- **Task Tracking**: checklists with due dates, assignments, and status
- **Vendor Directory**: caterers, AV companies, rental companies, photographers, more. Reusable across events
- **Per-Event Volunteer Assignments**: who's doing what for this event
- **Master Volunteer Roster** (1.1.0): the people behind the assignments, with skills, preferences, blackout dates, and a burnout score
- **Ministry Teams** (1.1.0): which team owns each event, with team-level views
- **Sermon Series** (1.1.0): active series tracking with weekly passages and event linkage
- **Liturgical Year** (1.1.0): season-aware prompts for typical events
- **Budget Tracking**: set a budget, log expenses, see spending vs. budget at a glance

## Example Usage

**Start planning:**
> "We need to start planning VBS. June 15-19."

**Check status:**
> "Where are we on Easter planning?"

**Add a volunteer with rotation awareness (1.1.0):**
> "Who can run snacks for VBS?"
(Skill checks the master roster for skill match, blackout dates, and burnout score before suggesting names.)

**Burnout protection (1.1.0):**
> "Add Sarah to greeter rotation Sunday."
> (Skill warns if Sarah's burnout score is high before confirming.)

**Sermon series linkage (1.1.0):**
> "Tie the small group dinner to the 'Sermons in the Hills' series."

**Liturgical prompts (1.1.0):**
> "What's coming up?"
> (Surface upcoming liturgical dates and suggest typical events for the season.)

**Track a vendor:**
> "We're using Grace Catering for the banquet."

**Post-event:**
> "VBS went great!" (prompts for wrap-up tasks)

## Built-In Templates

Planning checklists with recommended timelines for:

- Vacation Bible School (8-12 weeks)
- Easter / Christmas special services (6-8 weeks)
- Retreats (8-12 weeks)
- Fundraisers (6-10 weeks)
- Community outreach (4-6 weeks)
- Church-hosted weddings (4-8 weeks)
- Funerals / memorial services (1-5 days)
- Potlucks / fellowship meals (2-3 weeks)

## Installation

Copy the `church-event-planner` folder into your OpenClaw skills directory and restart your agent.
