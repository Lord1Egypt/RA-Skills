# Reply Execution Plan

This file documents the intended execution contract for browser-based comment replying.

Input JSON item shape:
- comment
- intent
- priority
- suggested_action
- public_reply
- dm_follow_up
- notes

Execution policy:
- only send when `suggested_action` is `public_reply` or `public_reply_plus_dm`
- skip `public_reply_review` unless user explicitly requests force mode
- skip `skip_or_hide`
- default to max 20 replies per run
- preserve a sent log with timestamp and original comment text

Recommended operator model:
1. open Douyin creator comment page
2. snapshot interactives
3. operator identifies reusable selectors / refs
4. script uses those selectors/refs for repeated reply actions
5. sample-check replies every 5-10 comments
