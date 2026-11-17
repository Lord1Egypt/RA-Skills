# Modes and parameters

Read this reference only when selecting a non-default mode or mapping advanced fields.

## URL Mode Parameters

Use this section only when the user chooses `url`.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `url` | Yes | `https://www.google.com/maps/place/Pizza+Inn+Magdeburg/data=!4m7!3m6!1s0x47a5f50c083530a3:0xfdba8746b538141!8m2!3d52.1263086!4d11.6094743!16s%2Fg%2F11kqmtk3dt!19sChIJozA1CAz1pUcRQYFTa3So2w8?authuser=0&hl=en&rclk=1` | `spider_parameters` | Google Maps URL. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |

Ask whether the user wants to change any value, and whether they want multiple URL groups.

Submit `spider_id=google_map-details_by-url` and `spider_parameters` like:

```json
[{"url":"https://www.google.com/maps/place/Pizza+Inn+Magdeburg/data=!4m7!3m6!1s0x47a5f50c083530a3:0xfdba8746b538141!8m2!3d52.1263086!4d11.6094743!16s%2Fg%2F11kqmtk3dt!19sChIJozA1CAz1pUcRQYFTa3So2w8?authuser=0&hl=en&rclk=1"}]
```

## CID Mode Parameters

Use this section only when the user chooses `cid`.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `CID` | Yes | `2476046430038551731` | `spider_parameters` | Google Maps CID. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |

Ask whether the user wants to change any value, and whether they want multiple CID groups.

Submit `spider_id=google_map-details_by-cid` and `spider_parameters` like:

```json
[{"CID":"2476046430038551731"}]
```

## Location Mode Parameters

Use this section only when the user chooses `location`.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `keyword` | Yes | `pizza` | `spider_parameters` | Google Maps search keyword. |
| `country` | Yes | `us` | `spider_parameters` | Google country. Show options using `references/google_countries.md`. |
| `lat` | No | `38` | `spider_parameters` | Latitude. Must be numeric. |
| `long` | No | `77` | `spider_parameters` | Longitude. Must be numeric. |
| `zoom_level` | No | `20` | `spider_parameters` | Zoom level. Must be an integer greater than or equal to `0`. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |

Then show the full `country` dropdown table from `references/google_countries.md`.

Ask whether the user wants to change any value, and whether they want multiple location groups.

Submit `spider_id=google_map-details_by-location` and `spider_parameters` like:

```json
[{"keyword":"pizza","country":"us","lat":"38","long":"77","zoom_level":"20"}]
```

## Place ID Mode Parameters

Use this section only when the user chooses `placeid`.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `place_id` | Yes | `ChIJ3S-JXmauEmsRUcIaWtf4MzE` | `spider_parameters` | Google Maps place ID. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |

Ask whether the user wants to change any value, and whether they want multiple place ID groups.

Submit `spider_id=google_map-details_by-placeid` and `spider_parameters` like:

```json
[{"place_id":"ChIJ3S-JXmauEmsRUcIaWtf4MzE"}]
```
