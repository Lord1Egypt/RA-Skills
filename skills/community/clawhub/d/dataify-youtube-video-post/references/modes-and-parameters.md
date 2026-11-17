# Modes and parameters

Read this reference only when selecting a non-default mode or mapping advanced fields.

## URL Mode

Use this section only when the user chooses `url`.

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `url` | Yes | `https://www.youtube.com/@stephcurry/videos` | YouTube channel Videos URL. Must use `https://www.youtube.com`. |
| `order_by` | No | `最新` | Dropdown-style option. |
| `start_index` | No | `1` | Integer greater than or equal to `0`. |
| `num_of_posts` | No | `5` | Integer greater than or equal to `0`. |
| `file_name` | No | `{{TasksID}}` | Builder form field. |

`order_by` options:

| Label | Value |
| --- | --- |
| Latest | `最新` |
| Popular | `热门` |
| Oldest | `最早` |

Submit `spider_id=youtube_video-post_by-url` with objects like:

```json
[{"url":"https://www.youtube.com/@stephcurry/videos","order_by":"最新","start_index":"1","num_of_posts":"5"}]
```

For multiple URL groups, provide multiple `url`, `order_by`, `start_index`, and `num_of_posts` objects.

## Search Filters Mode

Use this section only when the user chooses `search_filters`.

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `keyword_search` | Yes | `popular music` | Keyword used to search YouTube videos. |
| `features` | No | `All` | Dropdown-style option. |
| `type` | No | `Videos` | Dropdown-style option. |
| `duration` | No | `Under 3 minutes` | Dropdown-style option. |
| `upload_date` | No | `Last hour` | Dropdown-style option. |
| `num_of_posts` | No | `200` | Integer greater than or equal to `0`. |
| `file_name` | No | `{{TasksID}}` | Builder form field. |

`features` options:

| Label | Value |
| --- | --- |
| All | `All` |
| Live | `Live` |
| 4K | `4K` |
| HD | `HD` |
| Subtitles/CC | `Subtitles/CC` |
| Creative Commons | `Creative Commons` |
| 360° | `360°` |
| VR180 | `VR180` |
| 3D | `3D` |
| HDR | `HDR` |

`type` options:

| Label | Value |
| --- | --- |
| Video | `Videos` |
| Movie | `Movies` |

`duration` options:

| Label | Value |
| --- | --- |
| 4 分钟以内 | `4 分钟以内` |
| 4-20 分钟 | `4-20 分钟` |
| 20 分钟以上 | `20 分钟以上` |
| 全部 | `None` |

`upload_date` options:

| Label | Value |
| --- | --- |
| 上一小时 | `Last hour` |
| 今天 | `Today` |
| 本周 | `This week` |
| 本月 | `This month` |
| 今年 | `This year` |
| 全部 | `All` |

Submit `spider_id=youtube_video-post_by-search-filters` with objects like:

```json
[{"keyword_search":"popular music","features":"Subtitles/CC","type":"Videos","duration":"None","upload_date":"Last hour","num_of_posts":"200"}]
```

For multiple search-filter groups, provide multiple `keyword_search`, `features`, `type`, `duration`, `upload_date`, and `num_of_posts` objects.

## Hashtag Mode

Use this section only when the user chooses `hashtag`.

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `hashtag` | Yes | `shopping` | Topic hashtag used to filter YouTube videos. |
| `num_of_posts` | No | `10` | Integer greater than or equal to `0`. |
| `file_name` | No | `{{TasksID}}` | Builder form field. |

Submit `spider_id=youtube_video-post_by-hashtag` with objects like:

```json
[{"hashtag":"shopping","num_of_posts":"10"}]
```

For multiple hashtag groups, provide multiple `hashtag` and `num_of_posts` objects.

## Podcast URL Mode

Use this section only when the user chooses `podcast_url`.

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `url` | Yes | `https://www.youtube.com/playlist?list=RDCLAK5uy_lS3E3PgpboCkZ_PfLPCkLLNPI1uH6kfc0` | YouTube podcast or playlist URL. Must use `https://www.youtube.com`. |
| `num_of_posts` | No | `10` | Integer greater than or equal to `0`. |
| `file_name` | No | `{{TasksID}}` | Builder form field. |

Submit `spider_id=youtube_video-post_by-podcast-url` with objects like:

```json
[{"url":"https://www.youtube.com/playlist?list=RDCLAK5uy_lS3E3PgpboCkZ_PfLPCkLLNPI1uH6kfc0","num_of_posts":"10"}]
```

For multiple podcast URL groups, provide multiple `url` and `num_of_posts` objects.

## Keyword Mode

Use this section only when the user chooses `keyword`.

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `keyword` | Yes | `top videos` | Keyword used to search YouTube videos. |
| `num_of_posts` | No | `10` | Integer greater than or equal to `0`. |
| `file_name` | No | `{{TasksID}}` | Builder form field. |

Submit `spider_id=youtube_video-post_by-keyword` with objects like:

```json
[{"keyword":"top videos","num_of_posts":"10"}]
```

For multiple keyword groups, provide multiple `keyword` and `num_of_posts` objects.

## Explore Mode

Use this section only when the user chooses `explore`.

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `url` | Yes | `https://www.youtube.com/feed/storefront?bp=ogUCKAU%3D` | YouTube Explore URL. Must use `https://www.youtube.com`. |
| `all_tabs` | No | `true` | Dropdown-style option. Specifies whether to collect all tabs. |
| `file_name` | No | `{{TasksID}}` | Builder form field. |

`all_tabs` options:

| Label | Value |
| --- | --- |
| Collect all tabs | `true` |
| Do not collect all tabs | `false` |

Submit `spider_id=youtube_video-post_by-explore` with objects like:

```json
[{"url":"https://www.youtube.com/feed/storefront?bp=ogUCKAU%3D","all_tabs":"true"}]
```

For multiple Explore groups, provide multiple `url` and `all_tabs` objects.
