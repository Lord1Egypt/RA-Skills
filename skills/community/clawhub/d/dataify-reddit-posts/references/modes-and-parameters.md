# Modes and parameters

Read this reference only when selecting a non-default mode or mapping advanced fields.

## Post URL Mode Parameters

Use this section only when the user chooses `url`.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `url` | Yes | `https://www.reddit.com/r/battlefield2042/comments/1cmqs1d/official_update_on_the_next_battlefield_game/` | `spider_parameters` | Reddit post URL. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |


Also ask: "Do you want to collect multiple Reddit post URL groups? If yes, provide multiple `url` values."

Post URL mode handling:

- Trim leading and trailing whitespace from `url`.
- `url` cannot be empty.
- `url` must start with `https://www.reddit.com/`.
- Submit `spider_id=reddit_posts_by-url`.
- Submit `spider_parameters` as a JSON string containing one or more objects like:

```json
[{"url":"https://www.reddit.com/r/battlefield2042/comments/1cmqs1d/official_update_on_the_next_battlefield_game/"}]
```

## Keyword Mode Parameters

Use this section only when the user chooses `keywords`.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `keyword` | Yes | `datascience` | `spider_parameters` | Reddit post search keyword. |
| `num_of_posts` | No | `10` | `spider_parameters` | Maximum number of posts to collect. Must be an integer greater than or equal to `0`. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |


Also ask: "Do you want to collect multiple Reddit keyword groups? If yes, provide multiple groups with `keyword` and `num_of_posts`."

Keyword mode handling:

- Trim leading and trailing whitespace from `keyword`.
- `keyword` cannot be empty.
- `num_of_posts` must be an integer greater than or equal to `0`.
- Submit `spider_id=reddit_posts_by-keywords`.
- Submit `spider_parameters` as a JSON string containing one or more objects like:

```json
[{"keyword":"datascience","num_of_posts":"10"}]
```

## Subreddit URL Mode Parameters

Use this section only when the user chooses `subredditurl`.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `url` | Yes | `https://www.reddit.com/r/battlefield2042` | `spider_parameters` | Subreddit URL. |
| `sort_by` | No | `Hot` | `spider_parameters` | Post sort option. |
| `num_of_posts` | No | `10` | `spider_parameters` | Maximum number of posts to collect. Must be an integer greater than or equal to `0`. |
| `sort_by_time` | No | `Now` | `spider_parameters` | Time sort option. Time fields do not take effect with `Hot` and `New`. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |

Dropdown options for `sort_by`:

| Label | Value |
| --- | --- |
| Hot | `Hot` |
| Top | `Top` |
| New | `New` |
| Rising | `Rising` |

Dropdown options for `sort_by_time`:

| Label | Value |
| --- | --- |
| Now | `Now` |
| Today | `Today` |
| This Week | `This Week` |
| This Month | `This Month` |
| This Year | `This Year` |
| All Time | `All Time` |


Also ask: "Do you want to collect multiple Reddit subreddit URL groups? If yes, provide multiple groups with `url`, `sort_by`, `num_of_posts`, and `sort_by_time`."

Subreddit URL mode handling:

- Trim leading and trailing whitespace from `url`.
- `url` cannot be empty.
- `url` must start with `https://www.reddit.com/`.
- `sort_by` must be one of `Hot`, `Top`, `New`, or `Rising`.
- `sort_by_time` must be one of `Now`, `Today`, `This Week`, `This Month`, `This Year`, or `All Time`.
- `num_of_posts` must be an integer greater than or equal to `0`.
- Time fields do not take effect with `Hot` and `New`; keep the submitted value if the user provides it.
- Submit `spider_id=reddit_posts_by-subredditurl`.
- Submit `spider_parameters` as a JSON string containing one or more objects like:

```json
[{"url":"https://www.reddit.com/r/battlefield2042","sort_by":"Rising","num_of_posts":"10","sort_by_time":"Now"}]
```
