# Examples

These examples show the intended public-safe flow for `family-homework-pomodoro`.

## Parent example

```text
Parent: Today the homework is math worksheet 3 and reading 2 pages.
Assistant: Recorded as provided. What time should homework begin today?
Parent: Start at 6:30 PM.
Assistant: Understood. I will remind the child at 6:30 PM and use a 25/5 Pomodoro rhythm by default.
```

## Child reminder example

```text
Assistant: It is time to start homework now. Begin with one 25-minute study session.
Assistant: After that, take a 5-minute break.
```

## Reward approval example

```text
Assistant to parent: The homework appears to be completed well. Would you like to allow a reward today?
Parent: Yes, reward is allowed.
Assistant to child: Nice work. Your parent approved a reward for today.
```

## Notes

- Keep reminders short and friendly.
- Do not promise rewards before parent approval.
- Do not add private family details to the examples.
