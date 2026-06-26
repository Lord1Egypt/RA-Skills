# Troubleshooting

## `not_logged_in`

- Run `python3 scripts/run.py auth_manager.py setup`
- Complete login manually in the visible browser
- Re-run `python3 scripts/run.py auth_manager.py validate`

## `login_redirected`

- Stored cookies are no longer sufficient
- Re-authenticate and save a fresh browser state

## `verification_required`

- The page is blocked by CAPTCHA, risk review, or 2FA
- Keep the browser visible and complete the challenge manually

## `profile_in_use`

- Another Chrome/Patchright process holds the persistent profile lock
- Close the conflicting process or use the existing session daemon instead of starting another one

## `input_box_missing` / `page_structure_changed`

- Run the command with `--show-browser`
- Inspect `data/screenshots/`
- Update selectors in `scripts/config.py`
- If the failure happens during model switching, re-check the model picker and `Extended thinking` selectors

## `message_submit_unconfirmed`

- The skill could not confirm that the prompt actually entered the conversation
- Check whether a blocking modal or risk-review layer appeared over the composer
- Re-run with a visible browser to inspect the page state

## `network_error` / `page_load_failed`

- On Linux hosts, direct access to ChatGPT may be blocked even when saved auth is still valid
- Re-run with `CHATGPT_PROXY_URL`, `HTTPS_PROXY`, `HTTP_PROXY`, or `ALL_PROXY` set
- The JSON error payload now reports whether a proxy was detected and which env vars were checked

## `response_timeout`

- The skill now auto-attempts one recovery path: retry button first, then conversation reload
- `Extended thinking` asks now wait longer automatically, but very long generations can still time out
- If it still times out, check network/proxy configuration and whether ChatGPT is still streaming
- Use `--show-browser` to confirm whether generation is stuck behind a Cloudflare or ChatGPT-side challenge

## `model_picker_missing` / `model_option_missing` / `extended_thinking_unavailable`

- The account may not expose that model tier or the page layout may have changed
- Re-run with `--show-browser` to confirm the exact menu text shown in your account
- Check whether the current account only shows `Instant`, `Thinking`, or `Pro` variants different from your request

## `conversation_id` stays `null` while the page URL remains `/`

- Recent ChatGPT web builds sometimes keep the conversation on `https://chatgpt.com/` instead of navigating to `/c/<id>`
- In that case the skill now falls back to a client thread id such as `WEB:...`, extracted from frontend storage/resource state
- That `WEB:...` id is stable enough for metadata and same-tab follow-up checks, but it is not reopenable as a `/c/...` URL
