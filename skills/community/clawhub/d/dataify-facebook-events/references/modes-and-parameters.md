# Modes and parameters

Read this reference only when selecting a non-default mode or mapping advanced fields.

## Event List URL Mode Parameters

Use this section only when the user chooses `eventlist-url`.

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `url` | Yes | `https://www.facebook.com/nohoclub/events` | Facebook event list URL. |
| `file_name` | No | `{{TasksID}}` | Builder form field. Use the default when the user does not change it. |


Also ask: "Do you want to collect multiple Facebook event list URL groups? If yes, provide multiple `url` values."

Submit `spider_id=facebook_event_by-eventlist-url`.

## Event Search URL Mode Parameters

Use this section only when the user chooses `search-url`.

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `url` | Yes | `https://www.facebook.com/events/explore/us-atlanta/107991659233606` | Facebook event search URL. |
| `file_name` | No | `{{TasksID}}` | Builder form field. Use the default when the user does not change it. |


Also ask: "Do you want to collect multiple Facebook event search URL groups? If yes, provide multiple `url` values."

Submit `spider_id=facebook_event_by-search-url`.

## Event URL Mode Parameters

Use this section only when the user chooses `events-url`.

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `url` | Yes | `https://www.facebook.com/events/1546764716269782` | Facebook event URL. |
| `file_name` | No | `{{TasksID}}` | Builder form field. Use the default when the user does not change it. |


Also ask: "Do you want to collect multiple Facebook event URL groups? If yes, provide multiple `url` values."

Submit `spider_id=facebook_event_by-events-url`.
