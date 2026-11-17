# Task Status API

## Endpoint

`GET https://scraperapi.dataify.com/task_status`

## Query Parameters

| Parameter | Required | Description |
| --- | --- | --- |
| `api_key` | Yes | User API key. Supply it from `DATAIFY_API_TOKEN`; do not print it. |
| `task_id` | Yes | ID returned when the scraper task was created. |

## Response

The success response has HTTP `200` and includes `data.task_id` and `data.status`.

| `data.status` | Meaning |
| --- | --- |
| `处理中` | The task has not completed. |
| `成功` | The task completed with a result status of `200`. |
| `失败` | The task completed with a non-`200` result status. |

An invalid or unauthorized task ID returns a JSON body such as `{"data":"Task_id is error!","code":400}`. Missing parameters or an invalid API key return HTTP `403`.

## Automatic Result Retrieval

When `data.status` is `成功`, the bundled status script immediately requests `/download` on the same host using the same `api_key` and `task_id`, plus `type=json`. This behavior is self-contained and does not require the separate `dataify-task-result` skill to be installed.
