# Match Form Fields to Answers

You are matching registration form field labels to available answers. This is a text-only task — no browser needed.

Form fields may use different wording than the answer keys. Use your judgment to match them. For example:
- "What company do you work for?" matches "Company"
- "Your role" matches "Role"
- "Telegram handle" matches "Telegram"

## Instructions

1. For each EMPTY REQUIRED FIELD label below, check if any AVAILABLE ANSWER matches it (even if the wording differs).
2. Return a JSON object with:
   - `matches`: object mapping field labels to their matched answer values
   - `unknown`: array of field labels that couldn't be matched to any answer

## Example

EMPTY REQUIRED FIELDS:
- What company do you work for?
- Your role in the organization

AVAILABLE ANSWERS:
{"Company": "f(x) Protocol", "Role": "Engineer"}

Response:
{"matches": {"What company do you work for?": "f(x) Protocol", "Your role in the organization": "Engineer"}, "unknown": []}

## Your task

Return ONLY the JSON object. No explanation, no markdown.
