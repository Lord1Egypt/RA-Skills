# FSM: Full State Transition Table

## States and Transitions

```
STATE: idle
  → on input received
    → STATE: loading_config

STATE: loading_config
  → EXTEND.md found
    → STATE: resolving_account
  → EXTEND.md missing
    → ACTION: run_first_time_setup
    → STATE: loading_config (retry after setup)

STATE: resolving_account
  → no accounts block in EXTEND.md
    → single-account mode
    → STATE: classifying_input
  → accounts with 1 entry
    → auto-select only account
    → STATE: classifying_input
  → accounts with 2+ entries, --account <alias> supplied
    → select matching account
    → STATE: classifying_input
  → accounts with 2+ entries, one has default: true
    → pre-select default account, show name
    → STATE: classifying_input
  → accounts with 2+ entries, no default
    → ACTION: prompt_account_choice
    → STATE: classifying_input

STATE: classifying_input
  → path ends with .html and file exists
    → input_type: html
    → STATE: editorial_pass [mode: light unless --raw or user requests full]
  → path ends with .md and file exists
    → input_type: markdown
    → STATE: editorial_pass
  → --turbo flag or turbo: true in frontmatter
    → STATE: editorial_pass [mode: turbo]
  → --raw flag
    → STATE: metadata_validation [skip editorial]
  → plain text (not a file path)
    → ACTION: save_as_markdown (see slug rules below)
    → STATE: editorial_pass

STATE: editorial_pass [mode: light | medium | strong | turbo]
  → turbo mode
    → ACTION: light_structural_check_only
    → quality_score computed
    → score >= 50
      → STATE: metadata_validation
    → score < 50
      → ACTION: warn + minimal_repair
      → STATE: metadata_validation
  → standard mode
    → ACTION: run_parallel_side_computations (slug, tail keywords, profile block, image count)
    → ACTION: humanize_content (blocking)
    → quality_score computed
    → score >= 70
      → STATE: metadata_validation
    → score 60–69
      → editorial_iteration_count += 1
      → iteration_count == 1
        → ACTION: targeted_improvement
        → re-score
        → STATE: metadata_validation (regardless of new score, with warning)
      → iteration_count == 2
        → ACTION: warn("quality below threshold, proceeding with best effort")
        → STATE: metadata_validation
    → score < 60
      → editorial_iteration_count += 1
      → iteration_count < 2
        → ACTION: full_improvement_pass
        → re-score
        → loop back to quality check
      → iteration_count >= 2
        → ACTION: warn("could not reach quality threshold after 2 passes")
        → STATE: metadata_validation

STATE: metadata_validation
  → all fields (title, summary, author) resolved
    → STATE: packaging_check
  → title missing
    → ACTION: auto_generate_title
    → STATE: metadata_validation
  → summary missing
    → ACTION: auto_generate_summary
    → STATE: metadata_validation
  → author missing
    → ACTION: resolve_from_account_or_global
    → STATE: metadata_validation

STATE: packaging_check
  → all packaging requirements met
    → STATE: pre_publish_confirm
  → body over default_article_length
    → not --raw
      → ACTION: compress_repetition (LEVEL 2 repair)
      → re-check
    → --raw
      → warn + continue
  → long-tail keyword block missing
    → not --raw
      → ACTION: generate_tail_keywords (LEVEL 2 repair)
  → profile block missing
    → not --raw
      → ACTION: generate_profile_block (LEVEL 2 repair)
  → image count below preferred range
    → ACTION: warn in confirmation (do not block)
  → cover image missing (API mode, article_type=news)
    → attempt cover fallback chain (frontmatter → imgs/cover.png → first inline)
    → still missing
      → ACTION: halt + request cover image (LEVEL 3)

STATE: pre_publish_confirm
  → confirm_before_publish: false AND no warnings
    → skip confirmation UI
    → STATE: publishing
  → confirm_before_publish: true OR any warnings present
    → ACTION: show_confirmation_summary (see SKILL.md format)
    → user confirms (y)
      → STATE: publishing
    → user edits (e)
      → editorial_iteration_count = 0
      → STATE: editorial_pass [mode based on user request]
    → user cancels (n)
      → STATE: idle

STATE: publishing [method: api | browser]
  → api method
    → ACTION: check_token_cache
      → token valid
        → ACTION: run_wechat_api_script
      → token expired
        → ACTION: refresh_token (LEVEL 1)
        → ACTION: run_wechat_api_script
    → script succeeds
      → publish_result = {media_id, ...}
      → STATE: reporting
    → script fails, LEVEL 1 error
      → retry_count += 1
      → retry_count <= 2
        → wait (3s first retry, 10s second)
        → loop back to run script
      → retry_count > 2
        → STATE: error_report [level: 4]
    → script fails, LEVEL 3 error (credentials)
      → STATE: error_report [level: 3]
    → script fails, LEVEL 4 error (unrecoverable API)
      → STATE: error_report [level: 4]
  → browser method
    → ACTION: run_wechat_article_script or run_wechat_browser_script
    → script succeeds
      → STATE: reporting
    → Chrome not found
      → STATE: error_report [level: 3]
    → not logged in
      → ACTION: open_browser_for_qr_scan (first run)
      → retry once
    → other failures
      → STATE: error_report [level: 4]

STATE: reporting
  → ACTION: write_publish_log (append to amiao/.publish-log.yaml)
  → ACTION: check_auto_tune_trigger (every 10th cycle)
    → trigger reached
      → ACTION: compute_auto_tune_suggestions
      → ACTION: append_suggestions_to_completion_report
  → ACTION: show_completion_report (see SKILL.md format)
  → STATE: idle

STATE: error_report
  → ACTION: show_failure_report (level-appropriate message + fix path)
  → level 1–2 already handled inline; this state handles level 3–4 only
  → level 3: show exact setup/fix steps
  → level 4: show error code + link to mp.weixin.qq.com + suggest browser method as fallback
  → STATE: idle
```

---

## Slug Generation Rules

| Input | Rule |
|-------|------|
| English title | Slugify first 4–6 meaningful words: `Understanding AI Models` → `understanding-ai-models` |
| Chinese title, transliteration confident | Convert 3–4 meaningful words to pinyin: `人工智能的未来` → `rengong-zhineng-weilai` |
| Chinese title, transliteration uncertain | Timestamp fallback: `article-YYYYMMDD-HHMMSS` |

Save location: `$(pwd)/post-to-wechat/YYYY-MM-DD/<slug>.md`

---

## Multi-Account Credential Resolution (API)

For selected account `{alias}`:
1. `app_id` / `app_secret` inline in account block
2. `WECHAT_{ALIAS}_APP_ID` / `WECHAT_{ALIAS}_APP_SECRET` (alias: uppercase, `-` → `_`)
3. `amiao/.env` with prefixed keys
4. `~/amiao/.env` with prefixed keys
5. Fallback: `WECHAT_APP_ID` / `WECHAT_APP_SECRET`

Browser profile per account: `chrome_profile_path` in account → `{shared_parent}/wechat-{alias}/` → shared default
