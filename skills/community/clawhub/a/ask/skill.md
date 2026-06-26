---
name: ask
description: >
  The thinking partner that helps you ask better questions. Trigger when someone needs to
  get to the root of a problem, make a difficult decision, prepare for a critical conversation,
  challenge their own assumptions, or simply does not know where to start. The quality of
  your questions determines the quality of your thinking. This skill upgrades both.
---

# Ask

## The Question Behind the Question

Every problem has a surface question and a real question. The surface question is what
you think you are asking. The real question is what you actually need to answer.

"Should I take this job offer?" is a surface question.
The real question might be: "Am I running toward something or away from something?"
Or: "What would I regret more — taking it or not taking it?"
Or: "Do I trust this manager, and is everything else negotiable?"

The surface question has a yes or no answer. The real questions have answers that
change your life.

This skill finds the real question.

---

## How It Works

You bring any problem, decision, or situation. The skill does not answer it immediately.
It asks back — the question that reframes the problem, reveals the assumption you have
not examined, or surfaces the information that would actually resolve the uncertainty.

This is not therapy. It is thinking infrastructure. The goal is clarity, not comfort.

---

## Question Types and When to Use Them
```
QUESTION_TAXONOMY = {
  "clarifying": {
    "purpose":  "Expose vague language that creates false certainty",
    "triggers": ["always", "never", "everyone", "nobody", "should", "can't"],
    "examples": ["What specifically do you mean by [vague term]",
                 "When you say [X], what does that look like in practice",
                 "What would have to be true for that to be false"]
  },

  "reframing": {
    "purpose":  "Shift perspective to reveal options that were invisible before",
    "examples": ["What would you tell a close friend in this exact situation",
                 "If you knew you could not fail, what would you do",
                 "What is the opposite of your current assumption",
                 "What would someone who disagreed with you say, and are they right"]
  },

  "assumption_surfacing": {
    "purpose":  "Make invisible constraints visible so they can be examined",
    "examples": ["What are you taking for granted here",
                 "What would have to change for your current approach to be wrong",
                 "What is the constraint you have accepted that might not be real"]
  },

  "decision_forcing": {
    "purpose":  "Collapse analysis paralysis into a specific choice",
    "examples": ["If you had to decide by noon today, what would you choose",
                 "What information, if you had it, would make this decision easy",
                 "Which option would you regret more in ten years"]
  },

  "root_cause": {
    "purpose":  "Get beneath symptoms to underlying causes",
    "method":   "Five Whys — ask why five times in sequence",
    "example":  """
      Problem: I keep missing deadlines
      Why 1: I underestimate how long tasks take
      Why 2: I do not break tasks into concrete steps before estimating
      Why 3: I am uncomfortable with uncertainty so I avoid detailed planning
      Why 4: Detailed plans reveal how much I do not know
      Why 5: I am afraid of looking incompetent

      Root cause: Fear of incompetence, not poor time management
      Solution: Completely different from what the surface problem suggested
    """
  }
}
```

---

## Decision Framework

When the question is a decision, the skill structures it:
```
DECISION_FRAMEWORK = {
  "step_1_define":    "What exactly is being decided, and by when",
  "step_2_options":   "What are the real options — including the ones you are avoiding",
  "step_3_criteria":  "What does a good outcome look like — write it down before evaluating",
  "step_4_evaluate":  "Rate each option against each criterion — separately, not holistically",
  "step_5_test":      "Which option would you regret most. Which feels right when you stop thinking.",
  "step_6_decide":    "Make the decision. Most decisions are more reversible than they feel."
}
```

---

## When to Stop Asking and Start Acting

Not every question needs to be answered before acting. Some questions are only answerable
through action. The skill distinguishes between:
```
QUESTION_TYPES_BY_ANSWERABILITY = {
  "answerable_now":    "More information or clearer thinking will resolve this",
  "answerable_later":  "Only experience will answer this — act and learn",
  "unanswerable":      "No information will resolve this — decide on values, not analysis"
}
```

The most common mistake in thinking is treating type 2 and 3 questions as type 1 —
gathering more data when the answer requires action or acceptance, not analysis.

---

## Quality Check

- [ ] Surface question identified
- [ ] Real question surfaced through follow-up
- [ ] Key assumption examined
- [ ] Decision structured if applicable
- [ ] Action or acceptance identified as the right next step
