# Chatbot Designer Quality Checklist

## Pre-Build
- [ ] 90 days of support ticket data pulled and categorized by intent
- [ ] Top 5 intents by volume identified (not assumed)
- [ ] Current first-response time baseline recorded
- [ ] CSAT baseline recorded (to compare post-launch)
- [ ] OMS/platform integration confirmed (can bot look up live order data?)

## Flow Design
- [ ] Main menu has no more than 6 options
- [ ] "Talk to a person" option always visible
- [ ] Every flow has a clear resolution path (bot resolves OR creates ticket — never dead-ends)
- [ ] Every flow has an escalation exit after 2 failed resolution attempts
- [ ] Escalation pre-fills ticket with full conversation transcript
- [ ] Response time communicated to customer at escalation (specific time, not "soon")
- [ ] No flow requires more data than necessary (minimum data collection per flow)

## Specific Flows
- [ ] Order status flow connected to live OMS data
- [ ] Return flow checks eligibility against order date + policy window
- [ ] Return flow generates or emails prepaid label automatically
- [ ] Cancellation flow checks fulfillment status before confirming cancellation
- [ ] Wrong item flow initiates replacement + return at no cost
- [ ] Pre-purchase compatibility questions route to FAQ lookup or human

## Escalation Rules
- [ ] Frustration keywords trigger immediate human escalation
- [ ] High-value customer tag routes to priority queue
- [ ] Explicit "human/agent" request triggers immediate handoff
- [ ] After-hours escalation gives specific response time (not vague)
- [ ] Safety/legal keywords route to senior/priority queue

## Copy and Tone
- [ ] Bot introduces itself as a bot (not pretending to be human)
- [ ] Contractions used ("I'll", "you're", "let's")
- [ ] Specific numbers used (not "soon" or "quickly")
- [ ] Frustration acknowledged before jumping to solution
- [ ] No robotic completion phrases ("Is there anything else I can help you with today?")
- [ ] Error messages always include next step (never dead-end)

## Technical
- [ ] Chatbot tested end-to-end for every flow
- [ ] Escalation tested: frustration keywords trigger handoff correctly
- [ ] Mobile display tested (readable, tappable, no horizontal scroll)
- [ ] OMS integration confirmed with live order lookup test
- [ ] CSAT survey configured (20–30% random sample, not every interaction)
- [ ] Unhandled intent logging active

## Measurement Setup
- [ ] Containment rate tracking configured
- [ ] Escalation rate tracking configured
- [ ] CSAT for bot interactions tracking configured
- [ ] Drop-off rate tracking configured
- [ ] Weekly unhandled intent review scheduled (calendar block)
- [ ] 30-day and 90-day targets documented
