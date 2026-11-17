# Modes and parameters

Read this reference only when selecting a non-default mode or mapping advanced fields.

## Detail URL Mode Parameters

Use this section only when the user chooses `detail-url`.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `url` | Yes | `https://www.instagram.com/reel/C5Rdyj_q7YN/` | `spider_parameters` | Instagram Reel detail URL. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |


Also ask: "Do you want to collect multiple Instagram Reel detail URL groups? If yes, provide multiple `url` values."

Detail URL mode handling:

- Trim leading and trailing whitespace from `url`.
- `url` cannot be empty.
- `url` must start with `https://www.instagram.com/`.
- Submit `spider_id=ins_reel_by-url`.
- Submit `spider_parameters` as a JSON string containing one or more objects like:

```json
[{"url":"https://www.instagram.com/reel/C5Rdyj_q7YN/"}]
```

## List URL Mode Parameters

Use this section only when the user chooses `allreel-url`.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `url` | Yes | `https://www.instagram.com/billieeilish` | `spider_parameters` | Instagram list/profile URL. |
| `num_of_posts` | No | `10` | `spider_parameters` | Maximum number of Reels to collect. Must be an integer greater than or equal to `0`. |
| `posts_to_not_include` | No | `DP861NijuwE` | `spider_parameters` | Reel post IDs or PK values to exclude. Use English commas for multiple values. |
| `start_date` | No | `01-28-2025` | `spider_parameters` | Start date in `mm-dd-yyyy` format. Must be on or before `end_date`. |
| `end_date` | No | `01-28-2026` | `spider_parameters` | End date in `mm-dd-yyyy` format. Must be on or after `start_date`. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |


Also ask: "Do you want to collect multiple Instagram Reel list URL groups? If yes, provide multiple groups with `url`, `num_of_posts`, `posts_to_not_include`, `start_date`, and `end_date`."

List URL mode handling:

- `url` must start with `https://www.instagram.com/`.
- `num_of_posts` must be an integer greater than or equal to `0`.
- `start_date` and `end_date` must use `mm-dd-yyyy` format.
- `start_date` must be on or before `end_date`.
- Submit `spider_id=ins_allreel_by-url`.
- Submit `spider_parameters` as a JSON string containing one or more objects like:

```json
[{"url":"https://www.instagram.com/billieeilish","num_of_posts":"10","posts_to_not_include":"DP861NijuwE","start_date":"01-28-2025","end_date":"01-28-2026"}]
```

## Website URL Mode Parameters

Use this section only when the user chooses `listurl`.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `url` | Yes | `https://www.instagram.com/espn` | `spider_parameters` | Instagram website/list URL. |
| `num_of_posts` | No | `10` | `spider_parameters` | Maximum number of Reels to collect. Must be an integer greater than or equal to `0`. |
| `posts_to_not_include` | No | `DP861NijuwE` | `spider_parameters` | Reel post IDs or PK values to exclude. Use English commas for multiple values. |
| `start_date` | No | `01-28-2025` | `spider_parameters` | Start date in `mm-dd-yyyy` format. Must be on or before `end_date`. |
| `end_date` | No | `01-28-2026` | `spider_parameters` | End date in `mm-dd-yyyy` format. Must be on or after `start_date`. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |


Also ask: "Do you want to collect multiple Instagram Reel website URL groups? If yes, provide multiple groups with `url`, `num_of_posts`, `posts_to_not_include`, `start_date`, and `end_date`."

Website URL mode handling:

- `url` must start with `https://www.instagram.com/`.
- `num_of_posts` must be an integer greater than or equal to `0`.
- `start_date` and `end_date` must use `mm-dd-yyyy` format.
- `start_date` must be on or before `end_date`.
- Submit `spider_id=ins_reel_by-listurl`.
- Submit `spider_parameters` as a JSON string containing one or more objects like:

```json
[{"url":"https://www.instagram.com/espn","num_of_posts":"10","posts_to_not_include":"DP861NijuwE","start_date":"01-28-2025","end_date":"01-28-2026"}]
```
