# Task Result API

## Endpoint

`GET https://scraperapi.dataify.com/download`

## Query Parameters

| Parameter | Required | Value |
| --- | --- | --- |
| `api_key` | Yes | Read from `DATAIFY_API_TOKEN`; never print it. |
| `task_id` | Yes | The scraper task ID. |
| `type` | Yes | `json` |

The endpoint returns the JSON result associated with the task. Use it only after the task reports `成功`, unless the user explicitly requests direct retrieval.
