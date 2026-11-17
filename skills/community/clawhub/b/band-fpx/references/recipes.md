# band-fpx recipes

All recipes assume `B=<path>/skills/band-fpx/scripts/band.mjs` and a `band_no` in
`$BAND` taken from the first recipe. Every one was run live; field names are the
API's own (snake_case).

## Your bands

```sh
node $B get /v2.1.0/get_band_list_with_filter 'fields=band.band_no,band.name' include_restricted=false \
  | jq -r '.result_data[].band | "\(.band_no)\t\(.name)"'
```

`result_data` is an **array** of `{band: {...}}`, not an object.

## Band details

```sh
node $B get /v2.3.0/get_band_information band_no=$BAND \
  | jq '.result_data.band | {name, member_count, leader_name, open_type, chat_enabled}'
```

## Feed: posts and announcements

```sh
node $B get /v2.0.0/get_posts_and_announcements band_no=$BAND resolution_type=4 \
  | jq '.result_data.items[] | select(.type=="post") | .post
        | {post_no, created_at, author: .author.name, content, comment_count, web_url}'
```

- Each item is `{type, <type>: {...}}`, where `type` is `post` or `announcement`.
- `created_at` is epoch **ms**.
- `content` carries BAND inline markup such as `<band:refer …>`. Strip tags for plain text.
- Next page: `.result_data.paging.next_params` is `null` on the last page. Otherwise
  pass its keys back as `key=value` args.

## One post and its comments

```sh
node $B get /v2.0.0/get_post band_no=$BAND post_no=5 | jq '.result_data.post | {author: .author.name, content, comment_count}'
node $B get /v2.3.0/get_comments band_no=$BAND 'content_key={"content_type":"post","post_no":5}' \
  | jq '.result_data | {total, comments: [.items[] | {comment_id, author: .author.name, body, created_at}]}'
```

`content_key` must be the JSON object. `post_no:5` or a bare number gives result_code 200.

## Calendar: events in the next 90 days

```sh
node $B get /v1.6.0/get_schedules band_no=$BAND start_at=$(date +%Y%m%d) \
  future_end_at=$(date -v+90d +%Y%m%d) 'calendars=[{"is_default":true}]' \
  | jq '.result_data.items[] | {schedule_id, name, start_at, end_at, is_all_day, description}'
```

- Dates are `YYYYMMDD`. On Linux, use `date -d '+90 days' +%Y%m%d`.
- `calendars=[]` returns **zero** items. The default calendar has to be named.
- Omitting `calendars` gives result_code 200.

Upcoming only. This depends on the band's "upcoming events" setting and can return
`count: 0` while `get_schedules` has events, so prefer the range query:

```sh
node $B get /v1.6.0/get_upcoming_schedules band_no=$BAND limit=5 | jq '.result_data.items[] | {name, start_at}'
```

## Members

```sh
node $B get /v2.0.0/get_members_of_band band_no=$BAND \
  | jq -r '.result_data | "\(.member_count) members", (.members[] | "\(.name)\t\(.role)")'
```

## Chats

```sh
node $B get /v2.0.0/get_chat_channels band_no=$BAND | jq '.result_data.channels[] | {channel_id, name}'
node $B get /v2.0.3/sync_chat_channel channel_id=<id> resolution_type=4 \
  | jq '.result_data.channel | {name, participant_count, latest_message}'
```

`get_chat_channels` already carries `new_message_count`, `participant_count` and
`updated_at` (ms) per channel. `latest_message` may hold only `creator` when the
channel's preview is empty.

## What's new

```sh
node $B get /v1.2.0/get_news_count without_post_news=false without_album_news=false \
  with_chat_message_count=true feed_version=2 | jq .result_data
# {new_feed_count, new_chat_message_count, news_count}
```
