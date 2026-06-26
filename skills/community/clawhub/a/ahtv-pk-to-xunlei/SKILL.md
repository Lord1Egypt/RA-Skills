---
name: ahtv-pk-to-xunlei
description: Find 安徽网络电视台《快乐无敌大PK》 full-episode pages from a user-provided date expression, extract each episode's real video URL, and save the episodes into 迅雷云盘. Use this skill when the user asks for one or more 快乐无敌大PK episodes by date, date list, closed date range, or open range such as “3月5日之后”, and the task includes deduping existing 迅雷云盘 files, naming each episode as 快乐无敌大PK.2026.S02E{MMDD}.mp4, and using sms-login-dom-first for 迅雷云盘 SMS login.
---

# AHTV PK To Xunlei

Use this skill only for 《快乐无敌大PK》 on 安徽网络电视台. Treat all unspecified years as `2026`.

## Quick Start

1. Run the date parser first.
   Windows:
   ```powershell
   python "{baseDir}\scripts\parse_date_expr.py" --date-expr "<date_expr>"
   ```
   If `python` is unavailable, retry with:
   ```powershell
   py -3 "{baseDir}\scripts\parse_date_expr.py" --date-expr "<date_expr>"
   ```
2. Run the resolver on the same expression.
   ```powershell
   python "{baseDir}\scripts\resolve_episodes.py" --date-expr "<date_expr>"
   ```
3. Use the resolver JSON as the source of truth for `expanded_dates`, `episode_url`, `video_url`, and `target_filename`.

## Supported Date Expressions

- Single date: `3月5日`, `2026-03-05`
- Multi-date list: `3月5、6、7、8日`, `3月5日,3月6日,3月7日`
- Closed range: `3月5-10日`, `3月5日至3月10日`, `2026-03-05~2026-03-10`
- Open range: `3月5日之后`, `3月5日以后`

Interpretation rules:

- Default missing years to `2026`
- For `3月5、6、7、8日`, inherit month and year from the first date
- For `3月5-10日`, inherit month and year for the end date from the start date
- For `3月5日之后` and `3月5日以后`, exclude the day itself and start from `2026-03-06`
- For open ranges, stop at the latest currently discoverable 快乐无敌大PK episode date on 安徽网络电视台

Reject these requests as unsupported instead of guessing:

- `起`, `以来`, `前后`, `本周`, `最近几天`
- Cross-year shorthand without an explicit year
- Requests that mix 快乐无敌大PK with a different program

## Resolution Workflow

Run the resolver before opening 迅雷云盘. The resolver already does the deterministic parts:

- Search `https://www.ahtv.cn/search` for `快乐无敌大PK`
- Filter candidates to `https://www.ahtv.cn/pindao/ahzh/pk/split/...`
- Match by the episode date embedded in the title, not by the search result publish time
- Prefer titles containing `整期`
- Cross-check ambiguous dates against `https://www.ahtv.cn/pindao/ahzh/pk` and its paginated index pages
- Extract the real media URL from the single-episode page hidden input `#m3u8`

Treat the resolver output like this:

- `status=ready`: proceed to 迅雷云盘
- `status=not-found`: record the failure and continue with the next date
- `status=ambiguous`: record the failure and continue with the next date
- `status=video-url-missing`: record the failure and continue with the next date
- `status=error`: record the failure and continue with the next date

## 迅雷云盘 Workflow

Process dates one by one and continue even if one date fails.

For every resolver item with `status=ready`:

1. Open `https://pan.xunlei.com/`.
2. If the user is not logged in, use `$sms-login-dom-first` to complete 迅雷云盘 login with phone number plus SMS code, then return to the cloud drive page.
3. Search the whole cloud drive for the exact `target_filename`.
4. If an exact same file already exists anywhere in 迅雷云盘, mark the item as `skipped-existing` and do not add it again.
5. If it does not exist, ensure the folder path `/快乐无敌大PK/2026` exists.
6. Use 迅雷云盘's link-based add flow. UI labels can vary, so look for controls such as `链接添加`, `添加链接`, `云添加`, `添加任务`, or a plus menu with a chain/link icon.
7. Paste the resolver `video_url` exactly as returned.
8. Save into `/快乐无敌大PK/2026` if the dialog lets you choose the destination. If it saves elsewhere first, move it into `/快乐无敌大PK/2026` immediately after creation.
9. Wait until the file becomes visible in the target folder.
10. If 迅雷 keeps the source file name, rename it to `target_filename`.

Do not download to local disk as a fallback in v1. Only use 迅雷云盘 link add / cloud add.

## Naming Rules

- Basename format: `快乐无敌大PK.2026.S02E{MMDD}`
- Final filename format: `快乐无敌大PK.2026.S02E{MMDD}.mp4`
- Example: `快乐无敌大PK.2026.S02E0315.mp4`

Use the resolver's `target_filename` directly. Do not invent an alternate naming scheme.

## Final Output Format

Return one compact JSON-like summary in Markdown. Include these top-level fields:

- `input_expr`
- `expanded_dates`
- `summary`
- `items`

`summary` must include:

- `total`
- `added`
- `skipped_existing`
- `not_found`
- `failed`

Each item must include:

- `date`
- `status`
- `episode_url`
- `video_url`
- `target_filename`
- `xunlei_path`
- `message`

Status values for the final answer:

- `added-and-renamed`
- `skipped-existing`
- `not-found`
- `add-failed`

Map resolver failures into the final response like this:

- `not-found` stays `not-found`
- `ambiguous`, `video-url-missing`, and `error` become `add-failed`

## Notes

- Prefer the resolver scripts over ad-hoc parsing in the model.
- Treat the site structure as authoritative as of the current run. If the resolver fails because the site changed, report the failure clearly instead of fabricating URLs.
- Keep the browser workflow deterministic: exact filename search first, then add, then rename if needed.
