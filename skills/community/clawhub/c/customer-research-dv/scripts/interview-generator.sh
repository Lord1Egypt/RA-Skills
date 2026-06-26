#!/usr/bin/env bash
set -euo pipefail

# interview-generator.sh — Generate customer interview script
# Usage: ./interview-generator.sh --persona "description" --problem "pain point"

PERSONA=""
PROBLEM=""

# Parse args
while [[ $# -gt 0 ]]; do
  case $1 in
    --persona) PERSONA="$2"; shift 2 ;;
    --problem) PROBLEM="$2"; shift 2 ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$PERSONA" ]] || [[ -z "$PROBLEM" ]]; then
  echo "Usage: $0 --persona \"description\" --problem \"pain point\"" >&2
  exit 1
fi

echo "🎤 Generating interview script..." >&2

# Generate interview guide using structured framework
cat <<EOF
# Customer Interview Script

**Date:** $(date +"%Y-%m-%d")
**Persona:** $PERSONA
**Problem Space:** $PROBLEM

---

## Interview Guidelines

**Duration:** 30-45 minutes
**Format:** Semi-structured (follow the flow, not the script)
**Recording:** Ask permission, assure anonymity
**Goal:** Understand their world, not validate your solution

---

## Opening (5 min)

**Build rapport:**
- Thank them for their time
- Explain the purpose: "We're researching how people approach [problem space], and your experience would really help us understand it better."
- Assure confidentiality: "This is just research — nothing you say will be tied to your name."
- Get permission to record (if applicable)

**Transition:** "Let's start with understanding your current situation..."

---

## Section 1: Current State (10 min)

**Goal:** Understand their world before introducing the problem

1. "Walk me through a typical [day/week/month] in your [work/life related to problem space]."
   - *Probe:* What does that look like? Who's involved?

2. "What are your main goals or priorities right now around [problem space]?"
   - *Probe:* Why is that important to you?

3. "What does success look like for you in [problem space]?"
   - *Probe:* How do you measure that?

**Listen for:** Unprompted mentions of the problem, workarounds they've built, frustration signals

---

## Section 2: Problem Discovery (10 min)

**Goal:** Let them describe the problem in their words

4. "Tell me about a recent time when [problem situation] came up."
   - *Probe:* What triggered it? What happened?

5. "How did you handle that?"
   - *Probe:* What did you try first? Why?

6. "What's frustrating about the current way you deal with [problem]?"
   - *Probe:* What have you tried to make it better?

7. "If you could wave a magic wand and fix one thing about [problem space], what would it be?"
   - *Probe:* Why that specifically?

**Listen for:** Actual behavior vs. stated preferences, emotional language, "I wish I could...", workarounds

---

## Section 3: Solutions & Alternatives (10 min)

**Goal:** Understand what they've tried and why it didn't work

8. "What tools or methods do you currently use for [problem space]?"
   - *Probe:* What do you like/dislike about each?

9. "Have you tried [competitor product/approach]?"
   - *If yes:* "What was your experience?" 
   - *If no:* "Have you heard of it? What stopped you from trying it?"

10. "What would make you switch from your current approach to something new?"
    - *Probe:* What would have to be true?

**Listen for:** Switching costs, inertia, "good enough" mindset, deal-breakers

---

## Section 4: Validation (5 min)

**Goal:** Test specific assumptions (only if time permits)

*Only ask these if they're relevant to your hypothesis:*

11. "How important is [specific feature/benefit] to you?"
    - *Probe:* Would you pay for that?

12. "If a solution cost [price point], would that be reasonable for what you'd get?"
    - *Probe:* What would make it worth it?

**Listen for:** Value perception, willingness to pay, feature prioritization

---

## Closing (5 min)

13. "Is there anything I didn't ask that I should have?"

14. "Do you know anyone else who deals with [problem] who might be willing to chat?"

**Thank them:**
- "This was incredibly helpful. Your insights will really shape how we think about this."
- Offer to share findings (if appropriate)
- Send thank-you note within 24 hours

---

## Post-Interview Actions

**Immediate (within 1 hour):**
- Review notes/recording while fresh
- Tag quotes with themes (pain points, workarounds, deal-breakers)
- Note surprise findings that challenge assumptions

**Within 24 hours:**
- Send thank-you email
- Log insights to \`data/research/interviews/\`
- Update persona docs with validated/invalidated assumptions

**After 5+ interviews:**
- Look for patterns across interviews
- Identify must-have vs. nice-to-have features
- Update product roadmap based on validated needs

---

## Interview Tips

**Do:**
- Ask "why" at least 3 times per topic
- Let them talk (80/20 rule: they talk 80%, you talk 20%)
- Follow interesting tangents (they often lead to gold)
- Record exact quotes (real customer language = marketing gold)
- Stay curious, not defensive

**Don't:**
- Lead the witness ("Wouldn't you agree that...")
- Pitch your solution (you're here to learn, not sell)
- Fill awkward silences (silence = thinking time)
- Ask hypotheticals ("Would you use...")
- Ignore negative feedback (it's the most valuable data)

---

**Generated by:** Customer Research Skill
**Persona:** $PERSONA
**Problem:** $PROBLEM

EOF

echo "" >&2
echo "✅ Interview script generated" >&2
