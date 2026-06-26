#!/usr/bin/env python3
"""
ContextClear Metric Reporter
Reports agent metrics to ContextClear API.

Usage:
  python3 report.py                          # Interactive / env-based
  python3 report.py --tokens-in 50000 --tokens-out 2000 --cost 1.25
  python3 report.py --register --name "my-agent" --owner "me@email.com"
  
Env vars:
  CONTEXTCLEAR_API_URL    (default: https://api.contextclear.com/api)
  CONTEXTCLEAR_API_KEY    (required for reporting)
  CONTEXTCLEAR_AGENT_ID   (required for reporting)
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error


def register(api_url: str, name: str, owner: str, model: str = "unknown", provider: str = "unknown") -> dict:
    """Self-register an agent with ContextClear."""
    url = f"{api_url}/metrics/register"
    payload = {
        "name": name,
        "ownerId": owner,
        "model": model,
        "provider": provider,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode())
            print(f"✅ Agent registered!")
            print(f"   Agent ID: {result['agentId']}")
            print(f"   API Key:  {result['apiKey']}")
            print(f"   ⚠️  Store the API key — it won't be shown again!")
            return result
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"❌ Registration failed {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def report(agent_id: str, api_key: str, api_url: str, metrics: dict) -> dict:
    """Send a metric event to ContextClear."""
    url = f"{api_url}/metrics/{agent_id}"
    
    payload = {
        "eventType": metrics.get("event_type", "REQUEST"),
        "inputTokens": metrics.get("tokens_in", 0),
        "outputTokens": metrics.get("tokens_out", 0),
        "cost": metrics.get("cost", 0.0),
        "latencyMs": metrics.get("latency", 0),
        "statusCode": metrics.get("status_code", 200),
        "error": metrics.get("error", False),
        "emptyResponse": metrics.get("empty", False),
        "contextUtilization": metrics.get("context_util", 0.0),
        "contextWindowSize": metrics.get("context_window", 200000),
        "contextUsed": metrics.get("context_used", 0),
    }
    
    # Tool/grounding signals for server-side hallucination scoring
    if "tool_calls" in metrics:
        payload["toolCalls"] = metrics["tool_calls"]
    if "tool_failures" in metrics:
        payload["toolFailures"] = metrics["tool_failures"]
    if "memory_searches" in metrics:
        payload["memorySearches"] = metrics["memory_searches"]
    if "grounded_responses" in metrics:
        payload["groundedResponses"] = metrics["grounded_responses"]
    if "total_responses" in metrics:
        payload["totalResponses"] = metrics["total_responses"]
    
    # Optional quality metrics (agent-provided override)
    if "hallucination" in metrics:
        payload["hallucinationScore"] = metrics["hallucination"]
    if "coherence" in metrics:
        payload["coherenceScore"] = metrics["coherence"]
    
    # Quality decay signals
    if "correction_cycles" in metrics:
        payload["correctionCycles"] = metrics["correction_cycles"]
    if "compilation_errors" in metrics:
        payload["compilationErrors"] = metrics["compilation_errors"]
    if "session_turns" in metrics:
        payload["sessionTurnCount"] = metrics["session_turns"]
    if "task_switches" in metrics:
        payload["taskSwitches"] = metrics["task_switches"]
    
    # Session timeline
    if "session_id" in metrics:
        payload["sessionId"] = metrics["session_id"]
    if "turn_number" in metrics:
        payload["turnNumber"] = metrics["turn_number"]
    if "task_category" in metrics:
        payload["taskCategory"] = metrics["task_category"]
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "X-API-Key": api_key,
        },
        method="POST",
    )
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode())
            print(f"✅ Metric reported: {result.get('id', 'ok')}")
            print(f"   Tokens: {payload['inputTokens']}in / {payload['outputTokens']}out")
            print(f"   Cost: ${payload['cost']:.4f}")
            if payload.get('toolCalls'):
                print(f"   Tools: {payload['toolCalls']} calls, {payload.get('toolFailures', 0)} failures")
            print(f"   Context: {payload['contextUtilization']:.1f}%")
            return result
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"❌ API error {e.code}: {body}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Failed: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Report metrics to ContextClear")
    
    # Registration mode
    parser.add_argument("--register", action="store_true", help="Register a new agent")
    parser.add_argument("--name", help="Agent name (for registration)")
    parser.add_argument("--owner", help="Owner email (for registration)")
    parser.add_argument("--provider", default="unknown", help="AI provider (OpenAI, Anthropic, etc.)")
    
    # Reporting mode
    parser.add_argument("--agent-id", default=os.environ.get("CONTEXTCLEAR_AGENT_ID"))
    parser.add_argument("--api-key", default=os.environ.get("CONTEXTCLEAR_API_KEY"))
    parser.add_argument("--api-url", default=os.environ.get("CONTEXTCLEAR_API_URL", "https://api.contextclear.com/api"))
    parser.add_argument("--tokens-in", type=int, default=0)
    parser.add_argument("--tokens-out", type=int, default=0)
    parser.add_argument("--cost", type=float, default=0.0)
    parser.add_argument("--latency", type=int, default=0, help="Latency in ms")
    parser.add_argument("--context-util", type=float, default=0.0, help="Context utilization 0-100")
    parser.add_argument("--context-window", type=int, default=200000)
    parser.add_argument("--context-used", type=int, default=0)
    parser.add_argument("--error", action="store_true")
    parser.add_argument("--empty", action="store_true")
    parser.add_argument("--event-type", default="REQUEST", choices=["REQUEST", "HEARTBEAT", "ERROR", "CONTEXT_RESET"])
    parser.add_argument("--model", default="unknown", help="Model name")
    
    # Tool/grounding signals
    parser.add_argument("--tool-calls", type=int, help="Total tool calls in session")
    parser.add_argument("--tool-failures", type=int, help="Failed tool calls")
    parser.add_argument("--memory-searches", type=int, help="Memory search calls")
    parser.add_argument("--grounded-responses", type=int, help="Responses backed by tools")
    parser.add_argument("--total-responses", type=int, help="Total agent responses")
    
    # Quality overrides
    parser.add_argument("--hallucination", type=float, help="Hallucination score 0-1")
    parser.add_argument("--coherence", type=float, help="Coherence score 0-1")
    
    # Quality decay signals
    parser.add_argument("--correction-cycles", type=int, help="Times user asked to fix/redo")
    parser.add_argument("--compilation-errors", type=int, help="Code that didn't compile")
    parser.add_argument("--session-turns", type=int, help="Conversation depth (turn count)")
    parser.add_argument("--task-switches", type=int, help="Topic/file context switches")
    
    # Session timeline
    parser.add_argument("--session-id", type=str, help="Session identifier for timeline tracking")
    parser.add_argument("--turn-number", type=int, help="Turn number within session")
    parser.add_argument("--task-category", type=str, help="Task type: coding, email, search, chat")
    
    args = parser.parse_args()
    
    # Registration mode
    if args.register:
        if not args.name:
            print("❌ --name required for registration", file=sys.stderr)
            sys.exit(1)
        if not args.owner:
            print("❌ --owner required for registration", file=sys.stderr)
            sys.exit(1)
        register(args.api_url, args.name, args.owner, args.model, args.provider)
        return
    
    # Reporting mode
    if not args.agent_id:
        print("❌ Set CONTEXTCLEAR_AGENT_ID or use --agent-id", file=sys.stderr)
        sys.exit(1)
    if not args.api_key:
        print("❌ Set CONTEXTCLEAR_API_KEY or use --api-key", file=sys.stderr)
        sys.exit(1)
    
    metrics = {
        "event_type": args.event_type,
        "tokens_in": args.tokens_in,
        "tokens_out": args.tokens_out,
        "cost": args.cost,
        "latency": args.latency,
        "context_util": args.context_util,
        "context_window": args.context_window,
        "context_used": args.context_used,
        "error": args.error,
        "empty": args.empty,
    }
    if args.tool_calls is not None: metrics["tool_calls"] = args.tool_calls
    if args.tool_failures is not None: metrics["tool_failures"] = args.tool_failures
    if args.memory_searches is not None: metrics["memory_searches"] = args.memory_searches
    if args.grounded_responses is not None: metrics["grounded_responses"] = args.grounded_responses
    if args.total_responses is not None: metrics["total_responses"] = args.total_responses
    if args.hallucination is not None: metrics["hallucination"] = args.hallucination
    if args.coherence is not None: metrics["coherence"] = args.coherence
    if args.correction_cycles is not None: metrics["correction_cycles"] = args.correction_cycles
    if args.compilation_errors is not None: metrics["compilation_errors"] = args.compilation_errors
    if args.session_turns is not None: metrics["session_turns"] = args.session_turns
    if args.task_switches is not None: metrics["task_switches"] = args.task_switches
    if args.session_id is not None: metrics["session_id"] = args.session_id
    if args.turn_number is not None: metrics["turn_number"] = args.turn_number
    if args.task_category is not None: metrics["task_category"] = args.task_category
    
    report(args.agent_id, args.api_key, args.api_url, metrics)


if __name__ == "__main__":
    main()
