# Pintia

## Use this file when

The current task is on Pintia / PTA pages.

## Default profile

Use profile:

```bash
pintia
```

## Site

`https://pintia.cn`

## Behavior

- Treat Pintia as an ordinary practice site unless the user explicitly says it is a contest or exam.
- Do not submit automatically unless the user explicitly asks.
- Once the real problem page is visible, stay scoped to the current problem. Do not keep rescanning the outer list, ranking area, or sidebar.
- Before any submit action, verify the current problem title or id, selected language, and current answer or editor state.
- Do not retry, reset, or switch to another problem unless the user explicitly asks.

## Common task types

- Objective questions: return or select only the final answer.
- Program fill, function, and programming questions: read the full statement, input and output format, samples, and limits before answering.
- If the page is a contest-style set, avoid casual trial submissions. Treat each submission as consequential.

## Problem workflow

1. verify the active tab and current problem
2. read the full statement from the main content area in one pass
3. locate the active answer control: options, blank input, or code editor
4. apply the requested action once, then verify that the page state actually changed

## Coding tasks

- Prefer the normal page flow: select the language, fill the editor, then use the page's native run or submit control.
- Do not guess from the title alone. Read the samples and constraints before producing code.
- If a built-in run, sample test, or compile action is available, prefer it before final submit when the user asks for page actions.
- If the editor is a rich code editor, verify the visible editor content after writing. Do not assume a synthetic input event succeeded.
- Keep the code compatible with the selected language and the required input and output format.

## Submission and result checks

- After submission, wait for the visible verdict or score area to update before reporting success.
- Typical result states include `Accepted`, `Wrong Answer`, `Compile Error`, `Runtime Error`, `Time Limit Exceeded`, `Memory Limit Exceeded`, or a visible score.
- If the page shows a submissions list or latest record panel, prefer the newest visible record for confirmation.
- Once the page clearly shows the verdict or score, stop probing and report the result.

## Note

- Pintia includes several code-judged problem types. It is normal for an AI assistant to make mistakes on some questions or code submissions.
