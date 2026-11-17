# ToS / ethics notes (x-post)

- Personal use of the X account already signed in to Ego Lite. The human confirms the draft before `--yes`.
- https://x.com/tos applies to that account. This skill does not create accounts, bypass a challenge, or solve a captcha.
- The script does not print cookie values, `ct0`, or the bearer next to session material. It does not commit a session file.
- Do not ask the user to paste cookies or a password. Login happens in Ego Lite.
- Posts are the user's own posts. `--image` uploads that user's png, jpeg, or webp only after `--yes`. No likes, follows, or DMs.
- Reply via `page.fetch` was not verified (GraphQL 226). Do not hammer retries.
- Examples do not use a home-directory path or a product directory.
- Success is the status URL returned by CreateTweet. The script does not click Publish / 发帖 and does not click unrelated confirmations.
