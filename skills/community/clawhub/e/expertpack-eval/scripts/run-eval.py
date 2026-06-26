#!/usr/bin/env python3
"""
ExpertPack Eval Runner — Automated evaluation of pack-powered agents.

Sends questions from an eval set to an agent endpoint, captures responses,
and scores them using an LLM-as-judge approach.

Usage:
    python3 run_eval.py \
        --questions /path/to/questions.yaml \
        --endpoint ws://host:port/path \
        --output /path/to/results.yaml \
        --label "baseline-gemini-flash"
"""

import argparse
import asyncio
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: pyyaml required. Install with: pip install pyyaml")
    sys.exit(1)

try:
    import httpx
except ImportError:
    httpx = None

try:
    import websockets
except ImportError:
    websockets = None


# ---------------------------------------------------------------------------
# Question loading
# ---------------------------------------------------------------------------

def load_questions(path: str) -> dict:
    """Load and validate the eval question set."""
    with open(path, 'r') as f:
        data = yaml.safe_load(f)

    questions = data.get('questions', [])
    if not questions:
        print(f"Error: No questions found in {path}")
        sys.exit(1)

    # Validate required fields
    for i, q in enumerate(questions):
        for field in ('id', 'question', 'category', 'expected_answer'):
            if field not in q:
                print(f"Error: Question {i} missing required field '{field}'")
                sys.exit(1)

    print(f"Loaded {len(questions)} questions from {path}")
    return data


# ---------------------------------------------------------------------------
# Agent communication
# ---------------------------------------------------------------------------

async def send_question_ws(endpoint: str, question: str, timeout: int) -> dict:
    """Send a question via WebSocket and collect the full response."""
    if websockets is None:
        print("Error: websockets required for ws:// endpoints. Install with: pip install websockets")
        sys.exit(1)

    response_text = ""
    start_time = time.time()
    first_token_time = None

    try:
        async with websockets.connect(endpoint, close_timeout=10) as ws:
            # Send the question as a chat message
            await ws.send(json.dumps({
                "type": "message",
                "content": question
            }))

            # Collect response chunks until done
            while True:
                try:
                    raw = await asyncio.wait_for(ws.recv(), timeout=timeout)
                    msg = json.loads(raw)

                    if first_token_time is None and msg.get("type") in ("chunk", "content", "text"):
                        first_token_time = time.time()

                    if msg.get("type") == "chunk":
                        response_text += msg.get("content", "")
                    elif msg.get("type") == "content":
                        response_text += msg.get("content", "")
                    elif msg.get("type") == "text":
                        response_text += msg.get("text", "")
                    elif msg.get("type") == "done":
                        break
                    elif msg.get("type") == "error":
                        response_text = f"[ERROR] {msg.get('error', 'Unknown error')}"
                        break
                    elif msg.get("type") == "end":
                        break

                except asyncio.TimeoutError:
                    response_text += " [TIMEOUT]"
                    break

    except Exception as e:
        response_text = f"[CONNECTION_ERROR] {str(e)}"

    end_time = time.time()
    return {
        "response": response_text.strip(),
        "latency_ms": int((end_time - start_time) * 1000),
        "ttft_ms": int((first_token_time - start_time) * 1000) if first_token_time else None,
    }


async def send_question_http(endpoint: str, question: str, timeout: int) -> dict:
    """Send a question via HTTP POST and collect the response."""
    if httpx is None:
        print("Error: httpx required for http:// endpoints. Install with: pip install httpx")
        sys.exit(1)

    start_time = time.time()

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(endpoint, json={
                "message": question
            })
            resp.raise_for_status()
            data = resp.json()
            response_text = data.get("response", data.get("content", data.get("text", str(data))))
    except Exception as e:
        response_text = f"[ERROR] {str(e)}"

    end_time = time.time()
    return {
        "response": response_text.strip(),
        "latency_ms": int((end_time - start_time) * 1000),
        "ttft_ms": None,
    }


async def send_question(endpoint: str, question: str, timeout: int) -> dict:
    """Route to the appropriate transport based on endpoint scheme."""
    if endpoint.startswith("ws://") or endpoint.startswith("wss://"):
        return await send_question_ws(endpoint, question, timeout)
    elif endpoint.startswith("http://") or endpoint.startswith("https://"):
        return await send_question_http(endpoint, question, timeout)
    else:
        print(f"Error: Unsupported endpoint scheme: {endpoint}")
        sys.exit(1)


# ---------------------------------------------------------------------------
# LLM-as-Judge scoring
# ---------------------------------------------------------------------------

def build_judge_prompt(question: dict, response: str) -> str:
    """Build the scoring prompt for the LLM judge."""
    required_facts = question.get('required_facts', [])
    anti_hallucination = question.get('anti_hallucination', [])
    category = question.get('category', '')

    prompt = f"""You are an evaluation judge for an AI assistant that answers questions about a product.

QUESTION: {question['question']}

EXPECTED ANSWER: {question['expected_answer']}

ACTUAL RESPONSE FROM THE AGENT:
{response}

REQUIRED FACTS (each must be present for full correctness):
{chr(10).join(f"- {f}" for f in required_facts)}

ANTI-HALLUCINATION CHECKS (the response must NOT contain these):
{chr(10).join(f"- {f}" for f in anti_hallucination)}

{"This is an OUT-OF-SCOPE question. The agent should have declined to answer or clearly stated this is outside its expertise." if category == "out-of-scope" else ""}

Score the response. Return ONLY valid JSON (no markdown fences) with this structure:
{{
  "correctness": <float 0.0-1.0, fraction of required_facts present>,
  "facts_present": [<list of required_facts that ARE present in the response>],
  "facts_missing": [<list of required_facts that are NOT present>],
  "hallucinations": [<list of anti_hallucination violations found, or empty>],
  "groundedness": <float 0.0-1.0, how well the response sticks to factual claims vs fabricating>,
  "refusal_correct": <bool, true if out-of-scope question was properly declined, null if not out-of-scope>,
  "notes": "<brief explanation of scoring>"
}}

Be strict but fair. A fact counts as present if the response conveys the same meaning, even if phrased differently. A hallucination violation counts if the response contains the specific wrong information described."""

    return prompt


async def judge_response(question: dict, response: str, judge_model: str, api_key: str) -> dict:
    """Use an LLM to score a response against expected answer."""
    if httpx is None:
        print("Error: httpx required for judge scoring. Install with: pip install httpx")
        sys.exit(1)

    prompt = build_judge_prompt(question, response)

    try:
        async with httpx.AsyncClient(timeout=120) as client:
            resp = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": judge_model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.0,
                }
            )
            resp.raise_for_status()
            data = resp.json()
            content = data['choices'][0]['message']['content'].strip()

            # Strip markdown fences if present
            if content.startswith("```"):
                content = content.split("\n", 1)[1] if "\n" in content else content[3:]
                if content.endswith("```"):
                    content = content[:-3]
                content = content.strip()

            scores = json.loads(content)

            # Add token usage if available
            usage = data.get('usage', {})
            scores['judge_tokens'] = {
                'input': usage.get('prompt_tokens', 0),
                'output': usage.get('completion_tokens', 0),
            }

            return scores

    except json.JSONDecodeError as e:
        return {
            "correctness": 0.0,
            "facts_present": [],
            "facts_missing": question.get('required_facts', []),
            "hallucinations": [],
            "groundedness": 0.0,
            "refusal_correct": None,
            "notes": f"Judge returned invalid JSON: {str(e)}",
            "judge_tokens": {"input": 0, "output": 0},
        }
    except Exception as e:
        return {
            "correctness": 0.0,
            "facts_present": [],
            "facts_missing": question.get('required_facts', []),
            "hallucinations": [],
            "groundedness": 0.0,
            "refusal_correct": None,
            "notes": f"Judge error: {str(e)}",
            "judge_tokens": {"input": 0, "output": 0},
        }


# ---------------------------------------------------------------------------
# Main eval loop
# ---------------------------------------------------------------------------

async def run_eval(args):
    """Execute the full eval run."""
    data = load_questions(args.questions)
    questions = data['questions']

    # Load API key for judge
    api_key = os.environ.get('OPENROUTER_API_KEY', '')
    if not api_key and not args.dry_run:
        # Try loading from .env files
        for env_path in ['/root/.openclaw/.env', os.path.expanduser('~/.openclaw/.env')]:
            if os.path.exists(env_path):
                with open(env_path) as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith('OPENROUTER_API_KEY='):
                            api_key = line.split('=', 1)[1].strip().strip('"').strip("'")
                            break
            if api_key:
                break

    if not api_key and not args.dry_run:
        print("Warning: No OPENROUTER_API_KEY found. Judge scoring will fail.")

    if args.dry_run:
        print(f"\n=== DRY RUN ===")
        print(f"Questions: {len(questions)}")
        categories = {}
        for q in questions:
            cat = q.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1
        for cat, count in sorted(categories.items()):
            print(f"  {cat}: {count}")
        print(f"Endpoint: {args.endpoint}")
        print(f"Judge model: {args.judge_model}")
        print(f"Timeout: {args.timeout}s per question")
        print("Validation passed.")
        return

    print(f"\n=== EVAL RUN: {args.label} ===")
    print(f"Endpoint: {args.endpoint}")
    print(f"Judge: {args.judge_model}")
    print(f"Questions: {len(questions)}")
    print()

    results = []
    total_judge_input = 0
    total_judge_output = 0

    for i, q in enumerate(questions):
        qid = q['id']
        print(f"[{i+1}/{len(questions)}] {qid}: {q['question'][:60]}...", end=" ", flush=True)

        # Send question to agent
        agent_result = await send_question(args.endpoint, q['question'], args.timeout)
        response = agent_result['response']

        if response.startswith("[ERROR]") or response.startswith("[CONNECTION_ERROR]"):
            print(f"ERROR: {response[:80]}")
            scores = {
                "correctness": 0.0,
                "facts_present": [],
                "facts_missing": q.get('required_facts', []),
                "hallucinations": [],
                "groundedness": 0.0,
                "refusal_correct": None,
                "notes": response,
                "judge_tokens": {"input": 0, "output": 0},
            }
        else:
            # Score with judge
            scores = await judge_response(q, response, args.judge_model, api_key)
            print(f"correctness={scores.get('correctness', '?')}", end=" ")

        total_judge_input += scores.get('judge_tokens', {}).get('input', 0)
        total_judge_output += scores.get('judge_tokens', {}).get('output', 0)

        result = {
            "id": qid,
            "category": q.get('category', ''),
            "difficulty": q.get('difficulty', ''),
            "correctness": scores.get('correctness', 0.0),
            "groundedness": scores.get('groundedness', 0.0),
            "facts_present": scores.get('facts_present', []),
            "facts_missing": scores.get('facts_missing', []),
            "hallucinations": scores.get('hallucinations', []),
            "refusal_correct": scores.get('refusal_correct'),
            "latency_ms": agent_result['latency_ms'],
            "ttft_ms": agent_result.get('ttft_ms'),
            "response_preview": response[:300],
            "notes": scores.get('notes', ''),
        }
        results.append(result)
        print(f"({agent_result['latency_ms']}ms)")

        # Delay between questions
        if args.delay > 0 and i < len(questions) - 1:
            await asyncio.sleep(args.delay)

    # -----------------------------------------------------------------------
    # Compute aggregates
    # -----------------------------------------------------------------------
    n = len(results)
    avg_correctness = sum(r['correctness'] for r in results) / n if n else 0
    avg_groundedness = sum(r['groundedness'] for r in results) / n if n else 0

    hallucination_count = sum(1 for r in results if r['hallucinations'])
    hallucination_rate = hallucination_count / n if n else 0

    oos_questions = [r for r in results if r['category'] == 'out-of-scope']
    refusal_correct = sum(1 for r in oos_questions if r.get('refusal_correct') is True)
    refusal_accuracy = refusal_correct / len(oos_questions) if oos_questions else 1.0

    avg_latency = sum(r['latency_ms'] for r in results) / n if n else 0

    # -----------------------------------------------------------------------
    # Build output
    # -----------------------------------------------------------------------
    output = {
        "run_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "label": args.label,
        "eval_set_version": data.get('version', '1.0'),
        "questions_total": len(questions),
        "questions_evaluated": n,
        "dimensions": {
            "structure": {
                "version": args.structure_version or data.get('version', 'unknown'),
                "changes": "",
            },
            "model": {
                "name": args.model or "unknown",
                "provider": "openrouter",
            },
            "agent_training": {
                "version": args.agent_training_version or "1.0",
                "changes": "",
            },
        },
        "scores": {
            "correctness": round(avg_correctness, 3),
            "groundedness": round(avg_groundedness, 3),
            "hallucination_rate": round(hallucination_rate, 3),
            "refusal_accuracy": round(refusal_accuracy, 3),
            "avg_latency_ms": int(avg_latency),
        },
        "judge": {
            "model": args.judge_model,
            "total_input_tokens": total_judge_input,
            "total_output_tokens": total_judge_output,
        },
        "details": results,
    }

    # Write output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        yaml.dump(output, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"\n=== RESULTS ===")
    print(f"Correctness:      {output['scores']['correctness']:.1%}")
    print(f"Groundedness:     {output['scores']['groundedness']:.1%}")
    print(f"Hallucination:    {output['scores']['hallucination_rate']:.1%}")
    print(f"Refusal accuracy: {output['scores']['refusal_accuracy']:.1%}")
    print(f"Avg latency:      {output['scores']['avg_latency_ms']}ms")
    print(f"Judge tokens:     {total_judge_input} in / {total_judge_output} out")
    print(f"\nResults written to: {output_path}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="ExpertPack Eval Runner — Automated quality evaluation"
    )
    parser.add_argument('--questions', required=True, help='Path to questions.yaml')
    parser.add_argument('--endpoint', required=True, help='Agent endpoint (ws:// or http://)')
    parser.add_argument('--output', required=True, help='Output results YAML path')
    parser.add_argument('--model', default=None, help='Model name for metadata')
    parser.add_argument('--label', default='eval-run', help='Label for this run')
    parser.add_argument('--judge-model', default='anthropic/claude-sonnet-4',
                        help='Model for LLM-as-judge scoring')
    parser.add_argument('--timeout', type=int, default=60, help='Per-question timeout (seconds)')
    parser.add_argument('--delay', type=float, default=2.0, help='Delay between questions (seconds)')
    parser.add_argument('--dry-run', action='store_true', help='Validate without sending')
    parser.add_argument('--structure-version', default=None, help='Pack version for dimensions')
    parser.add_argument('--agent-training-version', default=None, help='Agent training version')

    args = parser.parse_args()
    asyncio.run(run_eval(args))


if __name__ == '__main__':
    main()
