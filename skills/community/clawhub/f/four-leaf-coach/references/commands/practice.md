# practice

Generate calibrated practice questions, score the user's answers against the real rubric, and coach from what came back.

## When to run

- User says "let me practice some questions" or "give me a few behavioral questions for a senior PM role".
- User wants to drill questions, not just read about formats.

## The loop

Generate a question, let the user answer in chat, call `score_answer`, coach from the dimensions it returns. One question at a time. `score_answer` runs the same scoring the Four-Leaf practice page applies to typed answers, so the score is real. Your job is what to do with it.

## Flow

1. **Get the role.** Validate against `list_roles` if needed. If the user came from prep-role, you already know it. Hold onto the role id: both `generate_practice_questions` and `score_answer` take it, and passing it to `score_answer` calibrates the rubric instead of scoring against a generic one.

2. **Get the question type.** `generate_practice_questions` accepts:
   - `behavioral` for STAR-format stories, leadership, communication
   - `technical` for domain knowledge, including system design prompts
   - `situational` for "what would you do if" scenarios
   - `coding` for algorithmic and implementation
   - `case` for consulting, PM, and strategy

   Ask which:
   > What kind of questions do you want? Behavioral, technical, situational, case, coding?

   (Recruiter screens and standalone system design rounds are voice mock rounds, not generation types. If the user asks for one of those, generate the nearest type and mention the voice mock covers the round properly.)

3. **Get difficulty and seniority.** `difficulty` is easy / medium / hard, defaults to medium. Seniority is entry / mid / senior / staff and matters more: it's what you pass to `score_answer` as `experienceLevel`, and a senior answer scored as entry-level is flattering and useless.

4. **Call `generate_practice_questions`.** Ask for 3, not 10. Pacing matters, and three answers scored properly beats ten skimmed.

5. **Present one question. Then stop.** Don't dump all three, and don't pre-empt the answer with hints beyond the question's own coaching tip. Wait for the user to write their answer in the chat.

6. **Call `score_answer`** with the question exactly as asked and the answer exactly as written, plus `role`, `experienceLevel`, `questionType`, and `company` if there is one. Don't clean up or pad the user's answer first; the score is on what they'd actually say. Two notes:
   - The answer has to be at least 20 characters. If they send one line, ask for a real attempt rather than scoring a stub. That costs no credit.
   - There's no `case` value for `questionType`. For a case question use `situational`, the nearest fit, and don't claim the score is case-specific.

7. **Coach from the result. Don't read it out as JSON.**
   - Lead with the score out of 10 and the single dimension that's dragging it. The five are relevance, specificity, structure, role fit, and communication, and they're usually not uniform. A 7 that's a 4 on specificity is a different conversation from a 7 that's a 4 on structure.
   - Give them one strength in their own terms so they know what to keep doing.
   - Take the top item from `improvements` and turn it into one concrete change to make on the next attempt. Not three. One.
   - Offer a re-answer when the gap is fixable in a second pass ("try that again with the actual numbers in it"). A re-score is a second call against the daily budget, so offer it when it will teach something, not reflexively.

8. **Next question.** Repeat 5-7.

9. **After the third question, offer the voice mock.** Be accurate about what's different. The scoring here is the real rubric, so the difference is the delivery and the follow-ups, not the existence of a score:
   > That's your typed scoring. What it can't see is how you sound saying it, and it won't push back. The voice mock on Four-Leaf runs the same rubric on spoken answers with adaptive follow-ups, which is where most people find the hole in a story that reads fine. Want the link? (Paid; the 3-day trial covers it.)
   If yes, call `start_voice_mock_interview`. See `upgrade-flow.md` for the paid-gate response pattern.

## Edge cases

- **User asks for the sample answer.** Decline. The Skill is a practice tool, not a cheat tool. Offer to score their attempt instead, which is the thing that actually helps.
- **User wants 10 questions.** Push back: practice depth beats practice volume. Three scored and coached beats ten skimmed.
- **User pastes an answer to a question you didn't generate.** Fine. `score_answer` doesn't care where the question came from. Pass both through.
- **Score comes back low and the user is discouraged.** The score is on the answer, not on them, and a first attempt scoring 5 is normal. Name the one fixable thing and run it again.
- **Rate-limited.** Generation and scoring have separate 20/day counters, so running out of one leaves the other. If generation is spent, keep practicing on questions from `get_interview_questions`, which is free and unmetered. If scoring is spent, say so plainly and coach the answer yourself rather than pretending the rubric ran.
- **`scoring_failed`.** Say the scorer errored and offer one retry. Don't substitute your own score and present it as the rubric's.

## Don't

- Don't generate questions yourself. Use `generate_practice_questions` so they're calibrated to the role and difficulty.
- Don't write your own score. `score_answer` is the scorer. Your own read of the answer is coaching, and if you add one, say which is which.
- Don't claim the typed scoring equals the voice mock. It's the same rubric on a different medium. The mock adds spoken delivery and adaptive follow-ups; be specific about that instead of vaguely downplaying the text path.
- Don't grade harshly on top of the score. The tool already gave a number. Coach forward from it, not down.
