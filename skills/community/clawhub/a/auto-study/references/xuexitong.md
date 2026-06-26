# xuexitong

## Default profile

Use profile:

```bash
xuexitong
```

## Site

`https://i.chaoxing.com/`

## Core policy

- Do not enter a full-screen homework page.
- Do not perform actions that a normal user could not perform.
- **Do not skip the process unless explicitly instructed otherwise; just follow it.**

## Chapter quiz workflow

### Process order

1. `locate questions`
2. `answering workflow`
3. `apply answers on page`
4. `submission workflow`

### Locate Questions

#### Target page structure

- The title may be `学生学习页面` or `studentstudy`
- Outer wrapper page: `studentstudy`
- The top-level page contains the main content `iframe` `#iframe`

#### What to do

- **First**, click a chapter link to enter the target page, or continue if you are already on it.
- You do not need to analyze the full page; it is enough to detect `studentstudy` and `iframe` -> `#iframe`.
- If the `#iframe` sub-document title is `视频` instead of `章节测验`, click `章节测验` to switch from the video page to the quiz page, with a URL like `/mooc-ans/knowledge/cards?...&num=1...`.

### Answering Workflow

1. Create the task directory using the common storage rule, for example `workspace/auto-study/xuexitong/10.3-以世界为方法/`, then take a full-page (`--full`) screenshot and immediately save it to `workspace/auto-study/xuexitong/<task>/images/full.png` before doing anything else.
2. Read the questions from the screenshot rather than from the DOM, then immediately record them in markdown and save the file to `workspace/auto-study/xuexitong/<task>/record.md` before moving to the next step.
3. Read `record.md`, carefully analyze each question one by one, and immediately append the final answers to the end of the same file before proceeding any further.

### Apply Answers On Page (if required)

- **Do not** apply answers on page until the markdown file has been created and the final answers have been appended to it.

1. Actual `iframe` path to the quiz content
   `#iframe` -> `work/index.html` -> `#frame_content` -> `doHomeWorkNew`
2. In the innermost document, locate the question blocks.
   Prefer `#form1` `.TiMu.newTiMu`.
3. Inside each question block, locate the target option.
   The option node is usually `li.font-cxsecret.before-after`.
   The option label is usually in `.num_option`, such as A or B.
4. Before clicking, check whether it is already selected.
   Avoid duplicate clicks.
5. After each applied answer, verify that the hidden answer input for that question matches the intended markdown answer.

### Submission Workflow (if required)

- **Do not** submit until the applied answers on page have been verified against the markdown answers.

1. **Submission cannot be undone**, so carefully verify that **all options** have `check_answer` or that the hidden answer input `answer<questionId>` already has a value.
2. Trigger the native submit control on the innermost page.
   Prefer clicking `a.btnSubmit` on the page.
   If the page uses a built-in function flow, you may also call the native submit flow, such as `btnBlueSubmit()`.
3. Handle the confirmation popup.
   A second confirmation dialog usually appears, often in an outer document.
   Check the confirm button in the top-level or outer page, such as `#popok`, then confirm again.
4. If the innermost URL changes to include `selectWorkQuestionYiPiYue`, submission is successful.
5. Finally, write the actual score at the end of the markdown file you just created.
