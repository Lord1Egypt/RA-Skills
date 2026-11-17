# ToS / ethics notes (xiaohongshu-ego)

- Personal use of the creator account already signed in to Ego Lite. The human confirms the plan before `--yes`.
- https://www.xiaohongshu.com/terms and the creator-platform rules apply to that account. This skill does not create accounts, bypass a challenge, or solve a captcha.
- The script does not print cookie values and does not commit a session file.
- Do not ask the user to paste cookies or a password. Login happens in Ego Lite.
- One video note per invocation. No batch posting, no comment farming, no deletes.
- A provided `--cover` is applied through the 「编辑封面」 dialog as the main cover. If the main-cover preview does not change, the skill does not click 发布. PK slots are not used for this.
- Without `--cover`, the platform's first-frame default is left as-is. The skill does not generate or download a cover.
- `edit-cover.mjs` is best-effort. A save can return a note to review. A failed update page is not retried into a second publish.
- Examples use `/absolute/path/to/video.mp4` and `/absolute/path/to/cover-3x4.png`. No home-directory paths and no product directories.
