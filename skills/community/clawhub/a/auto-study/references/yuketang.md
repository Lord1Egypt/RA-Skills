# yuketang

## Default profile

Use profile:

```bash
yuketang
```

## Site

`https://www.yuketang.cn/web`

## Core policy

## Page structure

- Entry pages are usually under `https://www.yuketang.cn/v2/web/...`
- Answerable exam or quiz pages are usually under `https://examination.xuetangx.com/exam/...`
- Result pages are usually under `https://examination.xuetangx.com/cover/...`
- Do not confuse the entry page, the active exam page, and the result page.
- **The target page** for answering work is the `exam/...` page.

## Practice workflow

### Process order

1. Locate problem page
2. Preprocessing
3. Analyze answers
4. Perform
5. Submit

### Locate problem page

- First confirm that the active tab is the target Yuketang tab.
- The answerable page should be `https://examination.xuetangx.com/exam/...`
- If the current page is still on `www.yuketang.cn`, navigate into the target quiz or exam first.
- If the current page is already on `cover/...`, treat it as a result page, not as an answerable page.

### Preprocessing

1. Create the task directory.
2. Record all questions in `markdown`.

### Analyze answers

1. Read `markdown` before analyzing answers
2. Analyze the recorded questions.
3. Append the final answers to the end of `markdown`.

### Perform

**Only do this if the user asks to apply answers on the page.**

1. Match each answer in `markdown` to the corresponding question on the page.
2. Avoid duplicate clicks if the correct option is already selected.
3. Re-check that the applied answers still match the markdown.

### Submit

**Only do this if the user explicitly asks for submission.**

1. Verify that all applied answers on the page match the answers in `markdown`.
2. Submit and If a second confirmation dialog appears, complete the confirmation.
3. Save a screenshot of the result page.
4. Read the result page image ad append the final score to `markdown`.
