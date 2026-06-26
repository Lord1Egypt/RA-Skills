#!/usr/bin/env python3
"""
轮询RunningHub任务状态直到完成或失败
用法: python3 poll_task.py <HOST> <API_KEY> <TASK_ID> [INTERVAL_SECONDS]
"""

import sys
import json
import time
import urllib.request
import urllib.error




def query_task(host: str, api_key: str, task_id: str) -> dict:
    """查询任务状态"""
    url = f"https://{host}/openapi/v2/query"

    headers = {
        "Host": host,
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {"taskId": task_id}

    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers=headers,
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            body = json.loads(e.read().decode("utf-8"))
            return {
                "status": "FAILED",
                "errorCode": str(e.code),
                "errorMessage": body.get("msg", str(e.reason)),
                "taskId": task_id
            }
        except:
            return {
                "status": "FAILED",
                "errorCode": str(e.code),
                "errorMessage": str(e.reason),
                "taskId": task_id
            }
    except Exception as e:
        return {
            "status": "FAILED",
            "errorCode": "-1",
            "errorMessage": str(e),
            "taskId": task_id
        }


def poll_task(host: str, api_key: str, task_id: str, interval: int = 10, max_duration: int = 1200) -> dict:
    """
    轮询任务状态直到完成或失败

    Args:
        host: RunningHub主机地址
        api_key: API密钥
        task_id: 任务ID
        interval: 轮询间隔秒数，默认10秒
        max_duration: 最长轮询时间（秒），默认1200秒（20分钟）

    Returns:
        最终的任务状态结果
    """
    start_time = time.time()
    known_statuses = ["QUEUED", "RUNNING", "SUCCESS", "FAILED", "TIMEOUT"]
    consecutive_failures = []
    last_failure_result = None
    max_consecutive_failures = 3

    while True:
        result = query_task(host, api_key, task_id)
        status = result.get("status", "UNKNOWN")
        current_time = time.time()

        if status == "SUCCESS":
            return result

        if status == "FAILED":
            consecutive_failures.append(result)
            last_failure_result = result
            if len(consecutive_failures) >= max_consecutive_failures:
                last_failure_result["errorMessage"] = f"连续{max_consecutive_failures}次查询失败，最后一次错误: {last_failure_result.get('errorMessage', 'Unknown')}"
                return last_failure_result
        else:
            consecutive_failures = []

        if status not in known_statuses:
            return {
                "status": "FAILED",
                "errorCode": "UNKNOWN_STATUS",
                "errorMessage": f"未知的状态: {status}",
                "taskId": task_id
            }

        elapsed = current_time - start_time
        if elapsed >= max_duration:
            return {
                "status": "TIMEOUT",
                "errorCode": "TIMEOUT",
                "errorMessage": f"轮询超时，已等待{int(elapsed)}秒，任务仍在运行中",
                "taskId": task_id
            }

        time.sleep(interval)


def main():
    if len(sys.argv) < 4:
        print("Usage: python3 poll_task.py <HOST> <API_KEY> <TASK_ID> [INTERVAL_SECONDS]", file=sys.stderr)
        sys.exit(1)

    host = sys.argv[1]
    api_key = sys.argv[2]
    task_id = sys.argv[3]
    interval = int(sys.argv[4]) if len(sys.argv) > 4 else 10

    try:
        result = poll_task(host, api_key, task_id, interval)
        print(json.dumps(result, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({
            "status": "FAILED",
            "errorCode": "-1",
            "errorMessage": str(e),
            "taskId": task_id
        }, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
