#!/usr/bin/env python3
"""
Mock A2A Server — a local A2A agent for testing and experimentation.

This server implements a complete A2A agent endpoint. Once running, other A2A clients
(can be AI agents using the a2a-protocol skill) can discover and interact with it.

Usage:
    python3 mock_a2a_server.py [--port 8080] [--name string] [--skills id:name:desc ...]

The server automatically serves its AgentCard at /.well-known/agent.json.

Examples:
    # Basic server on port 8080
    python3 mock_a2a_server.py --port 8080

    # Custom named agent with specific skills
    python3 mock_a2a_server.py --port 8080 --name helper-agent --skills "code:Coding:Reviews and writes code" "doc:Documentation:Generates docs"

    # Start and test from another terminal:
    #   curl http://localhost:8080/.well-known/agent.json
    #   python3 scripts/validate_agent_card.py /tmp/card.json  (fetch it first)
"""

import argparse
import json
import re
import sys
import time
import uuid
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timezone


# ─── Configuration ────────────────────────────────────────────────────────────

DEFAULT_PORT = 8080
DEFAULT_NAME = "mock-a2a-agent"
DEFAULT_DESCRIPTION = "A helpful mock A2A agent for testing. Echoes structured data back with simulated processing."
DEFAULT_VERSION = "1.0"
DEFAULT_SKILLS = [
    ("echo", "Echo", "Echoes back the input data as output (for testing connectivity)"),
    ("capitalize", "Capitalize Text", "Capitalizes all text in the input string"),
    ("word-count", "Word Count", "Returns a word-count summary of the input text"),
]

TASKS = {}  # taskId -> task object (in-memory store)


# ─── JSON-RPC Helpers ────────────────────────────────────────────────────────

def jsonrpc_response(result, req_id):
    return {"jsonrpc": "2.0", "result": result, "id": req_id}


def jsonrpc_error(code, message, req_id, data=None):
    err = {"jsonrpc": "2.0", "error": {"code": code, "message": message}, "id": req_id}
    if data:
        err["error"]["data"] = data
    return err


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# ─── Task Lifecycle ──────────────────────────────────────────────────────────

def make_task(task_id, session_id, context_id, message):
    return {
        "taskId": task_id,
        "sessionId": session_id,
        "contextId": context_id,
        "status": {"state": "submitted", "message": "Task received", "timestamp": now_iso()},
        "metadata": {"receivedAt": now_iso()},
        "artifacts": [],
        "messages": [message] if message else [],
    }


def process_task(task):
    """
    Simulate work and produce an artifact.
    Reads the input parts and produces a response based on message content.
    """
    msg = task["messages"][-1] if task["messages"] else {}
    parts = msg.get("parts", [])

    # Extract text from parts
    text_input = ""
    data_input = {}
    for part in parts:
        kind = part.get("kind")
        if kind == "text":
            text_input += part.get("text", "")
        elif kind == "data":
            data_input.update(part.get("data", {}))

    instruction = data_input.get("instruction", text_input.strip())
    skill_id = data_input.get("skill", "")

    # Infer skill from content if not explicitly specified
    if not skill_id and instruction:
        lowered = instruction.lower()
        if "capitalize" in lowered:
            skill_id = "capitalize"
        elif "word count" in lowered or "word-count" in lowered or "count words" in lowered:
            skill_id = "word-count"
        elif "echo" in lowered:
            skill_id = "echo"
        else:
            skill_id = "echo"  # default

    # ── Skill routing ─────────────────────────────────────────────────────
    if skill_id == "capitalize":
        output_data = {"result": instruction.upper()}
        artifact_name = "capitalized-text"
    elif skill_id == "word-count":
        words = instruction.split()
        output_data = {
            "word_count": len(words),
            "char_count": len(instruction),
            "char_count_no_spaces": len(instruction.replace(" ", "")),
            "preview": instruction[:50] + "..." if len(instruction) > 50 else instruction,
        }
        artifact_name = "word-count-result"
    else:  # echo
        output_data = {
            "echo": instruction,
            "skill_used": skill_id,
            "processing_time_ms": round((time.time() % 1) * 1000),
            "server": args.name,
        }
        artifact_name = "echo-response"

    task["artifacts"] = [{
        "artifactId": f"art-{uuid.uuid4().hex[:8]}",
        "name": artifact_name,
        "description": f"Result from {skill_id} skill",
        "parts": [{"kind": "data", "data": output_data}],
    }]
    task["status"] = {"state": "completed", "message": "Task completed successfully", "timestamp": now_iso()}


def streaming_events(task, stream=True):
    """
    Yield SSE-formatted lines for a streaming response.
    Simulates working state -> artifact updates -> completed.
    """
    task["status"] = {"state": "working", "message": "Processing task...", "timestamp": now_iso()}

    yield f"event: task_status_update\ndata: {json.dumps({
        'kind': 'TaskStatusUpdateEvent',
        'taskId': task['taskId'],
        'status': task['status'],
        'final': False
    })}\n\n"

    # Simulate partial artifact update
    yield f"event: task_artifact_update\ndata: {json.dumps({
        'kind': 'TaskArtifactUpdateEvent',
        'taskId': task['taskId'],
        'artifact': {
            'artifactId': f'art-{uuid.uuid4().hex[:8]}',
            'name': 'partial-result',
            'parts': [{'kind': 'data', 'data': {'status': 'processing'}}]
        },
        'final': False
    })}\n\n"

    time.sleep(0.05)

    # Process the task
    process_task(task)

    # Final artifact update
    if task["artifacts"]:
        yield f"event: task_artifact_update\ndata: {json.dumps({
            'kind': 'TaskArtifactUpdateEvent',
            'taskId': task['taskId'],
            'artifact': task["artifacts"][0],
            'final': True
        })}\n\n"

    # Terminal status
    yield f"event: task_status_update\ndata: {json.dumps({
        'kind': 'TaskStatusUpdateEvent',
        'taskId': task['taskId'],
        'status': task['status'],
        'final': True
    })}\n\n"


# ─── Request Parser ──────────────────────────────────────────────────────────

def parse_jsonrpc(body):
    try:
        req = json.loads(body)
        return req
    except json.JSONDecodeError:
        return None


# ─── AgentCard ───────────────────────────────────────────────────────────────

def build_agent_card():
    skills = []
    for sid, sname, sdesc in args.skills or DEFAULT_SKILLS:
        skills.append({
            "id": sid,
            "name": sname,
            "description": sdesc,
            "tags": sid.split("-"),
            "examples": [f"Use the {sname} skill"]
        })

    return {
        "name": args.name or DEFAULT_NAME,
        "description": args.description or DEFAULT_DESCRIPTION,
        "version": DEFAULT_VERSION,
        "provider": {
            "organization": "mock-a2a-server",
            "url": f"http://localhost:{args.port}"
        },
        "capabilities": {
            "streaming": "SUPPORTED",
            "pushNotifications": "SUPPORTED",
            "agentPrivilege": False,
            "signedAgentCard": False,
            "dataStreamingSupported": True,
            "supportsAuthenticatedExtendedAgentCard": False,
        },
        "skills": skills,
        "authentication": {
            "schemes": [],
            "credentials": "optional"
        },
        "defaultInputModes": ["text", "json"],
        "defaultOutputModes": ["json", "text"],
        "endpoint": f"http://localhost:{args.port}/a2a/",
        "url": f"http://localhost:{args.port}",
    }


# ─── HTTP Handler ────────────────────────────────────────────────────────────

class A2AHandler(BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        sys.stdout.write(f"[{now_iso()}] {fmt % args}\n")
        sys.stdout.flush()

    # ── Utility ──────────────────────────────────────────────────────────

    def send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False)
        self.send_response(status)
        self.send_header("Content-Type", "application/a2a+json; charset=utf-8")
        self.send_header("Content-Length", str(len(body.encode("utf-8"))))
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def send_sse(self, event_generator):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        try:
            for line in event_generator:
                self.wfile.write(line.encode("utf-8"))
                self.wfile.flush()
        except BrokenPipeError:
            pass

    def read_body(self):
        content_len = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(content_len).decode("utf-8")

    # ── Routes ───────────────────────────────────────────────────────────

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path == "/.well-known/agent.json":
            card = build_agent_card()
            self.send_json(200, card)
            return

        if path == "/a2a/agent/extendedCard":
            # No auth in mock server, just echo the card
            self.send_json(200, build_agent_card())
            return

        if path == "/a2a/tasks/list":
            self.send_json(200, jsonrpc_response({
                "tasks": list(TASKS.values()),
            }, req_id=1))
            return

        self.send_json(404, {"error": f"GET {path} not found"})

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")
        body = self.read_body()
        req = parse_jsonrpc(body)

        if req is None:
            self.send_json(400, jsonrpc_error(-32700, "Parse error", req_id=None))
            return

        method = req.get("method", "")
        params = req.get("params", {})
        req_id = req.get("id")

        # ── tasks/send ─────────────────────────────────────────────────
        if method == "tasks/send":
            task_id = params.get("taskId") or f"task-{uuid.uuid4().hex[:8]}"
            session_id = params.get("sessionId", "")
            context_id = params.get("contextId", "")
            message = params.get("message", {})
            configuration = params.get("configuration", {})

            task = make_task(task_id, session_id, context_id, message)
            TASKS[task_id] = task

            # Sync execution: process immediately
            process_task(task)
            self.send_json(200, jsonrpc_response({
                "task": task,
                "artifacts": task["artifacts"],
            }, req_id=req_id))
            return

        # ── tasks/sendSubscribe ─────────────────────────────────────────
        if method == "tasks/sendSubscribe":
            task_id = params.get("taskId") or f"task-{uuid.uuid4().hex[:8]}"
            session_id = params.get("sessionId", "")
            context_id = params.get("contextId", "")
            message = params.get("message", {})
            configuration = params.get("configuration", {})

            task = make_task(task_id, session_id, context_id, message)
            TASKS[task_id] = task

            self.send_sse(streaming_events(task))
            return

        # ── tasks/get ───────────────────────────────────────────────────
        if method == "tasks/get":
            task_id = params.get("taskId", "")
            task = TASKS.get(task_id)
            if not task:
                self.send_json(404, jsonrpc_error(-32603, f"Task not found: {task_id}", req_id=req_id))
                return
            self.send_json(200, jsonrpc_response({"task": task}, req_id=req_id))
            return

        # ── tasks/list ──────────────────────────────────────────────────
        if method == "tasks/list":
            session_id = params.get("sessionId")
            tasks = list(TASKS.values())
            if session_id:
                tasks = [t for t in tasks if t.get("sessionId") == session_id]
            self.send_json(200, jsonrpc_response({"tasks": tasks}, req_id=req_id))
            return

        # ── tasks/cancel ────────────────────────────────────────────────
        if method == "tasks/cancel":
            task_id = params.get("taskId", "")
            task = TASKS.get(task_id)
            if not task:
                self.send_json(404, jsonrpc_error(-32603, f"Task not found: {task_id}", req_id=req_id))
                return
            task["status"] = {"state": "canceled", "message": "Canceled by client", "timestamp": now_iso()}
            self.send_json(200, jsonrpc_response({"task": task}, req_id=req_id))
            return

        # ── tasks/subscribe ────────────────────────────────────────────
        if method == "tasks/subscribe":
            task_id = params.get("taskId", "")
            push_config = params.get("pushConfig", {})
            task = TASKS.get(task_id)
            if not task:
                self.send_json(404, jsonrpc_error(-32603, f"Task not found: {task_id}", req_id=req_id))
                return
            # Mock: immediately push result to the push URL
            push_url = push_config.get("pushProviderUrl")
            if push_url:
                try:
                    import urllib.request
                    payload = json.dumps({
                        "taskId": task_id,
                        "result": {"task": task, "artifacts": task["artifacts"]},
                        "pushNotificationConfigId": push_config.get("id", "mock-config"),
                    })
                    req = urllib.request.Request(
                        push_url,
                        data=payload.encode("utf-8"),
                        headers={"Content-Type": "application/a2a+json"},
                        method="POST"
                    )
                    urllib.request.urlopen(req, timeout=5)
                except Exception as e:
                    sys.stdout.write(f"[mock server] push notification failed: {e}\n")
            self.send_json(200, jsonrpc_response({"taskId": task_id, "subscribed": True}, req_id=req_id))
            return

        # ── tasks/push (incoming webhook — stub) ───────────────────────
        if method == "tasks/push":
            # This is what the mock server calls when it pushes to a client
            self.send_json(200, jsonrpc_response({"received": True}, req_id=req_id))
            return

        # ── pushNotificationConfig/* ──────────────────────────────────
        if method.startswith("pushNotificationConfig/"):
            # Mock implementation — store config in memory (not persisted)
            action = method.split("/", 1)[1]
            if action == "create":
                cfg = params
                cfg["id"] = f"cfg-{uuid.uuid4().hex[:8]}"
                self.send_json(200, jsonrpc_response(cfg, req_id=req_id))
            elif action == "get":
                self.send_json(200, jsonrpc_response(params, req_id=req_id))
            elif action == "list":
                self.send_json(200, jsonrpc_response({"configs": []}, req_id=req_id))
            elif action == "delete":
                self.send_json(200, jsonrpc_response({"deleted": True}, req_id=req_id))
            return

        # ── agent/getExtendedAgentCard ────────────────────────────────
        if method == "agent/getExtendedAgentCard":
            self.send_json(200, jsonrpc_response(build_agent_card(), req_id=req_id))
            return

        self.send_json(404, jsonrpc_error(-32603, f"Unknown method: {method}", req_id=req_id))


# ─── CLI ────────────────────────────────────────────────────────────────────

def parse_skills(skill_strs):
    """Parse 'id:name:desc' strings into skill tuples."""
    result = []
    for s in skill_strs:
        parts = s.split(":", 2)
        if len(parts) == 3:
            result.append(tuple(parts))
        elif len(parts) == 2:
            result.append((parts[0], parts[1], parts[1]))
        else:
            sys.stderr.write(f"⚠️  Ignoring malformed skill: {s} (expected id:name:description)\n")
    return result


parser = argparse.ArgumentParser(description="Mock A2A Server")
parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"Port to listen on (default: {DEFAULT_PORT})")
parser.add_argument("--name", type=str, default=None, help="Agent name")
parser.add_argument("--description", type=str, default=None, help="Agent description")
parser.add_argument("--skills", nargs="+", default=None, help="Skills as 'id:name:description' triplets")
args = parser.parse_args()
args.skills = parse_skills(args.skills) if args.skills else None


def run():
    addr = ("0.0.0.0", args.port)
    server = HTTPServer(addr, A2AHandler)
    card = build_agent_card()

    print()
    print("=" * 56)
    print(f"  🤖  A2A Mock Server")
    print("=" * 56)
    print(f"  Name:     {card['name']}")
    print(f"  Version:  {card['version']}")
    print(f"  Skills:   {', '.join(s[0] for s in (args.skills or DEFAULT_SKILLS))}")
    print(f"  Endpoint: http://localhost:{args.port}/a2a/")
    print(f"  AgentCard: http://localhost:{args.port}/.well-known/agent.json")
    print("=" * 56)
    print()
    print(f"  Available skills:")
    for sid, sname, sdesc in (args.skills or DEFAULT_SKILLS):
        print(f"    [{sid}] {sname}")
        print(f"          {sdesc}")
    print()
    print(f"  Try this from another terminal:")
    print(f"    curl http://localhost:{args.port}/.well-known/agent.json")
    print()
    print(f"  Press Ctrl+C to stop.")
    print()
    sys.stdout.flush()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Shutting down mock A2A server.")
        server.shutdown()


if __name__ == "__main__":
    run()