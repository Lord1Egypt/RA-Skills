# Feedback & Revision Planner



## Purpose



This skill helps users interpret feedback and turn it into a clear and practical revision plan.



It is especially useful when feedback is vague, incomplete, or low-information, such as "make it better", "not good enough", "too vague", "needs improvement", "optimize this", or "revise it again".



The goal is not only to rewrite text, but to help users understand the feedback, identify possible problems, plan revisions, ask clarification questions when needed, and produce a safer revised draft.



---



## When to use



Use this skill when the user provides a draft, document, message, proposal, essay, report, presentation text, email, review response, or workplace document that needs revision based on feedback.



This skill is useful for feedback from teachers, supervisors, managers, reviewers, clients, teammates, or collaborators.



---



## Core principles



The agent should:



1. Do not blindly agree with the feedback.

2. Do not assume the feedback provider's intention when the feedback is vague.

3. Do not invent problems that are not visible in the user's text.

4. Distinguish clearly between confirmed feedback and possible interpretation.

5. Separate required revisions from optional improvements.

6. Mark missing information as "not specified" or "needs clarification".

7. Preserve the user's original meaning unless the user asks for a stronger rewrite.

8. Improve clarity, logic, structure, evidence, tone, specificity, and actionability.

9. Avoid making the text sound polished but empty.

10. Provide practical revision steps, not only general advice.



---



## Required input



The user should provide when possible:



1. The original text or draft.

2. The feedback received.

3. The context of the text.

4. The target audience.

5. The expected style or tone.

6. Any word limit or format requirement.



If the original text is missing, do not produce a final revised draft. Instead, explain what can be inferred from the feedback and ask the user to provide the draft.



If the feedback is missing, perform a general revision diagnosis based on the visible text and clearly state that no external feedback was provided.



---



## Handling clear feedback



When the feedback is clear and specific, the agent should:



1. Summarize the feedback.

2. Identify what exactly needs to be revised.

3. Explain why the issue matters.

4. Convert the feedback into concrete revision tasks.

5. Provide a step-by-step revision plan.

6. Rewrite the relevant text when enough original text is available.

7. Explain how the revised version responds to the feedback.



---



## Handling vague or low-information feedback



When the feedback is vague, incomplete, or low-information, the agent should not pretend to know the feedback provider's exact intention.



Instead, the agent should:



1. State that the feedback is vague.

2. Provide possible interpretations of the feedback.

3. Diagnose visible problems in the original text based on structure, clarity, logical flow, specificity, evidence, tone, audience fit, and actionability.

4. Provide low-risk revision options that improve the text without changing the core meaning.

5. Mark uncertain assumptions clearly.

6. Suggest clarification questions the user can ask the feedback provider.

7. Produce a revised draft based on the safest improvement direction when enough original text is available.



Use cautious wording such as:



- "The feedback is not specific enough to determine the exact revision intention."

- "Based on the visible text, the most likely issues are..."

- "This is an interpretation, not a confirmed requirement."

- "A low-risk revision would be..."

- "You may want to ask the feedback provider..."



---



## Output format



Use the following structure when relevant:



### 1. Feedback diagnosis



State whether the feedback is clear, partly clear, vague, or low-information.



### 2. Possible meaning of the feedback



Explain what the feedback may mean. If the feedback is vague, provide multiple possible interpretations.



### 3. Visible problems in the original text



Identify problems that can be observed directly from the text.



### 4. Required revisions



List revisions that directly respond to the feedback. If the feedback does not clearly require a specific revision, say so.



### 5. Optional improvements



List improvements that may strengthen the text but are not necessarily required.



### 6. Revision plan



Provide a practical step-by-step plan.



### 7. Clarification questions



Provide questions the user can ask the feedback provider when the feedback is vague or incomplete.



### 8. Revised draft



Provide a revised version only when enough original text is available.



### 9. Explanation of changes



Briefly explain how the revised version responds to the feedback.



---



## Special handling for vague authority feedback



When vague feedback comes from a supervisor, manager, teacher, reviewer, or client, the agent should be especially careful.



The agent should not over-interpret the authority figure's intention.



The agent should provide:



1. A safe revision direction.

2. A more substantial revision option.

3. Clarification questions.

4. A polite response message the user can send back.



The response message should be professional, concise, and non-defensive.



---



## Avoid



The agent should avoid:



- pretending vague feedback is clear

- inventing the feedback provider's intention

- changing the user's core meaning without permission

- over-rewriting the text

- making the text sound polished but less accurate

- giving only general advice such as "make it clearer"

- ignoring missing information

- treating all feedback as correct

- producing a final revised draft when the original text is not provided



---



## Example



**User input:**



"My manager said this project plan is too vague and not convincing enough, but did not give specific comments."



**Expected behavior:**



The agent should state that the feedback is vague and cannot fully reveal the manager's exact intention. The agent should then diagnose the visible text, identify possible issues such as unclear objectives, lack of concrete evidence, weak structure, missing action steps, or insufficient risk analysis. The agent should provide safe revision options, clarification questions, and a revised draft if the original project plan is provided.



---



## Quality standard



A good response should help the user understand:



1. What the feedback probably means.

2. What is directly supported by the feedback.

3. What is only an interpretation.

4. What should be revised first.

5. What remains unclear.

6. How to revise the text safely and effectively.

