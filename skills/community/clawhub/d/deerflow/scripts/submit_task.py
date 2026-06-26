#!/usr/bin/env python3
"""
Submit a deep research task to DeerFlow.

Usage:
    python3 submit_task.py "<task description>"

Environment variables:
    DEERFLOW_URL         DeerFlow public gateway URL (default: http://localhost:2026)
    DEERFLOW_LANGGRAPH   LangGraph internal API URL (default: http://localhost:2024)
    DEERFLOW_MODEL       Model name to use (default: minimax-m2.7)
    DEERFLOW_RECURSION   Max recursion limit (default: 200)
"""
import json
import sys
import urllib.request
import urllib.error
import os

# Configuration: reads from environment variables, defaults to local DeerFlow stack.
DEERFLOW_URL = os.environ.get("DEERFLOW_URL", "http://localhost:2026")
LANGGRAPH_URL = os.environ.get("DEERFLOW_LANGGRAPH", "http://localhost:2024")
ASSISTANT_ID = os.environ.get("DEERFLOW_ASSISTANT_ID", "lead_agent")
MODEL_NAME = os.environ.get("DEERFLOW_MODEL", "minimax-m2.7")
RECURSION_LIMIT = int(os.environ.get("DEERFLOW_RECURSION", "200"))


def create_thread() -> str | None:
    """Create a new LangGraph thread. Returns thread_id or None on failure."""
    url = f"{LANGGRAPH_URL}/threads"
    data = json.dumps({}).encode("utf-8")
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            thread_id = result.get("thread_id")
            if not thread_id:
                print(f"Error: no thread_id in response: {result}")
            return thread_id
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        print(f"HTTP error creating thread ({e.code}): {body}")
    except urllib.error.URLError as e:
        print(f"Connection error creating thread: {e.reason}")
    return None


def submit_task(thread_id: str, task_description: str) -> str | None:
    """Submit a task to an existing thread. Returns run_id or None on failure."""
    url = f"{LANGGRAPH_URL}/threads/{thread_id}/runs"
    payload = {
        "assistant_id": ASSISTANT_ID,
        "input": {
            "messages": [
                {
                    "type": "human",
                    "content": [{"type": "text", "text": task_description}],
                }
            ]
        },
        "config": {
            "recursion_limit": RECURSION_LIMIT,
            "configurable": {
                "model_name": MODEL_NAME,
                "thinking_enabled": True,
                "is_plan_mode": False,
                "subagent_enabled": False,
            },
        },
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            run_id = result.get("run_id")
            if not run_id:
                print(f"Error: no run_id in response: {result}")
            return run_id
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        print(f"HTTP error submitting task ({e.code}): {body}")
    except urllib.error.URLError as e:
        print(f"Connection error submitting task: {e.reason}")
    return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 submit_task.py <task description>")
        sys.exit(1)

    print(f"DeerFlow: {DEERFLOW_URL} | LangGraph: {LANGGRAPH_URL} | "
          f"Model: {MODEL_NAME} | Recursion limit: {RECURSION_LIMIT}")

    thread_id = create_thread()
    if not thread_id:
        sys.exit(1)
    print(f"Thread created: {thread_id}")

    run_id = submit_task(thread_id, sys.argv[1])
    if not run_id:
        sys.exit(1)

    result = {
        "thread_id": thread_id,
        "run_id": run_id,
        "status": "submitted",
        "deerflow_url": DEERFLOW_URL,
    }
    print(f"\n{json.dumps(result, indent=2)}")
