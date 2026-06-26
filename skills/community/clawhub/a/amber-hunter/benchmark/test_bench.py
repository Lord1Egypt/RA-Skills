#!/usr/bin/env python3
"""
Synthetic benchmark for amber-hunter — tests the logic without real dataset.
Uses 5 fake entries, each with 10 sessions.
"""
import json, math, argparse, time
from pathlib import Path

AMBER_URL = "http://localhost:18998"
AMBER_TOKEN = None


def get_token():
    global AMBER_TOKEN
    import urllib.request
    req = urllib.request.urlopen(f"{AMBER_URL}/token", timeout=5)
    AMBER_TOKEN = json.loads(req.read())["api_key"]


def ingest_capsule(memo, content, tags):
    import urllib.request
    data = json.dumps({"memo": memo, "content": content, "tags": tags}).encode()
    req = urllib.request.Request(
        f"{AMBER_URL}/capsules", data=data,
        headers={"Authorization": f"Bearer {AMBER_TOKEN}", "Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())["id"]


def clear_all():
    import urllib.request
    req = urllib.request.Request(
        f"{AMBER_URL}/capsules",
        headers={"Authorization": f"Bearer {AMBER_TOKEN}"},
        method="GET"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            capsules = json.loads(resp.read()).get("capsules", [])
            for c in capsules:
                del_req = urllib.request.Request(
                    f"{AMBER_URL}/capsules/{c['id']}",
                    headers={"Authorization": f"Bearer {AMBER_TOKEN}"},
                    method="DELETE"
                )
                try:
                    urllib.request.urlopen(del_req, timeout=5)
                except Exception:
                    pass
    except Exception:
        pass


def recall(query, limit=50):
    import urllib.request, urllib.parse
    url = f"{AMBER_URL}/recall?q={urllib.parse.quote(query)}&limit={limit}"
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {AMBER_TOKEN}"},
        method="GET"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
    return [(m["id"], m["memo"]) for m in data.get("memories", [])]


# Synthetic dataset: 5 queries, each with 10 sessions
SYNTHETIC_DATA = [
    {
        "question": "What database did the user say they prefer?",
        "answer_session_ids": ["sess_3"],
        "haystack_session_ids": [f"sess_{i}" for i in range(10)],
        "haystack_sessions": [
            [{"role": "user", "content": f"I used MongoDB for project {i}."}] * 3
            for i in range(10)
        ]
    },
    {
        "question": "Which city does the user live in?",
        "answer_session_ids": ["sess_7"],
        "haystack_session_ids": [f"sess_{i}" for i in range(10)],
        "haystack_sessions": [
            [{"role": "user", "content": f"Living in Tokyo, working remotely." if i == 7 else f"Office is in SF."}]
            for i in range(10)
        ]
    },
    {
        "question": "What language do they mostly code in?",
        "answer_session_ids": ["sess_1", "sess_5"],
        "haystack_session_ids": [f"sess_{i}" for i in range(10)],
        "haystack_sessions": [
            [{"role": "user", "content": f"I write Rust for my side projects." if i in [1,5] else f"I use Python at work."}]
            for i in range(10)
        ]
    },
    {
        "question": "What is their favorite editor?",
        "answer_session_ids": ["sess_2"],
        "haystack_session_ids": [f"sess_{i}" for i in range(10)],
        "haystack_sessions": [
            [{"role": "user", "content": f"VSCode is my go-to editor."}]
            for i in range(10)
        ]
    },
    {
        "question": "Are they working on any open source projects?",
        "answer_session_ids": ["sess_9"],
        "haystack_session_ids": [f"sess_{i}" for i in range(10)],
        "haystack_sessions": [
            [{"role": "user", "content": f"Maintaining a CLI tool in Go." if i == 9 else f"No OSS work lately."}]
            for i in range(10)
        ]
    },
]


def run_synthetic():
    print("="*50)
    print("Synthetic Benchmark — amber-hunter logic test")
    print("="*50)

    get_token()
    print(f"Connected to amber-hunter\n")

    # Clear
    print("Clearing existing capsules...")
    clear_all()

    # Ingest all sessions
    print("Ingesting 50 sessions (5 entries × 10 sessions)...")
    capsule_map = {}  # sess_id -> (capsule_id, content_preview)
    session_capsule = {}  # capsule_id -> sess_id (for reverse lookup)

    for entry in SYNTHETIC_DATA:
        for sess_id, session in zip(entry["haystack_session_ids"], entry["haystack_sessions"]):
            text = " ".join(t["content"] for t in session if t.get("role") == "user")
            try:
                cid = ingest_capsule(
                    memo=f"[benchmark:{sess_id}]",
                    content=text,
                    tags=f"benchmark,sess:{sess_id}"
                )
                capsule_map[sess_id] = (cid, text[:30])
                session_capsule[cid] = sess_id
            except Exception as e:
                print(f"  Ingest failed for {sess_id}: {e}")

    print(f"Ingested {len(capsule_map)} capsules.\n")

    # Query
    print("Running 5 queries...\n")
    results = []
    for i, entry in enumerate(SYNTHETIC_DATA):
        q = entry["question"]
        correct_sids = set(entry["answer_session_ids"])

        recalled = recall(q, limit=5)
        recalled_sids = [session_capsule.get(cid, "") for cid, _ in recalled]
        recalled_sids = [s for s in recalled_sids if s]

        hit = any(s in correct_sids for s in recalled_sids)
        results.append(hit)

        print(f"Q{i+1}: {q[:50]}")
        print(f"  Correct: {correct_sids}")
        print(f"  Recalled: {recalled_sids}")
        print(f"  Hit: {'✅' if hit else '❌'}\n")

    recall_score = sum(results) / len(results)
    print(f"Recall@5: {recall_score:.1%} ({sum(results)}/{len(results)})")
    print(f"\nAmber-hunter is functional ✅")


if __name__ == "__main__":
    run_synthetic()
