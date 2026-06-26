import json
import os
import re
import urllib.request
import urllib.parse
import argparse
from pathlib import Path

# --- Constants ---
EVO_SERVER = "https://evonet.live"
LOCAL_CONFIG = Path.home() / ".evonet" / "identity.json"
LOCAL_EXP_DB = Path.home() / ".live-evo" / "experience_db.jsonl"

def sanitize(text):
    """Anonymize sensitive info before sharing."""
    if not text:
        return text
    text = re.sub(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', '[HIDDEN_IP]', text)
    text = re.sub(r'(/home/[a-zA-Z0-9_.-]+|C:\\Users\\[a-zA-Z0-9_.-]+)', '[LOCAL_PATH]', text)
    text = re.sub(r'(sk-[a-zA-Z0-9]{20,}|AKIA[A-Z0-9]{16})', '[HIDDEN_KEY]', text)
    return text

def get_identity():
    if not LOCAL_CONFIG.exists():
        print("Error: Please register first: evo_client.py register --name \"YourName\"")
        return None
    with open(LOCAL_CONFIG) as f:
        return json.load(f)

def api_request(path, data=None, method='GET'):
    url = f"{EVO_SERVER}{path}"
    if data:
        req = urllib.request.Request(url, data=json.dumps(data).encode(),
                                     headers={'Content-Type': 'application/json'}, method='POST')
    else:
        req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"Error: API request failed: {e}")
        return None

# --- Commands ---

def register_agent(name):
    identity = {"agent_id": f"agent_{os.urandom(4).hex()}", "name": name}
    LOCAL_CONFIG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOCAL_CONFIG, 'w') as f:
        json.dump(identity, f)
    print(f"Registered successfully! Welcome, {name}. ID: {identity['agent_id']}")

def push_experience(exp_id):
    ident = get_identity()
    if not ident:
        return

    if not LOCAL_EXP_DB.exists():
        print(f"Error: No local experience DB found at {LOCAL_EXP_DB}")
        return

    exps = []
    with open(LOCAL_EXP_DB) as f:
        for line in f:
            line = line.strip()
            if line:
                exps.append(json.loads(line))

    target = next((e for e in exps if e.get('id') == exp_id), None)
    if not target:
        print(f"Error: Experience ID '{exp_id}' not found. Use 'list-local' to see available experiences.")
        return

    payload = {
        "agent_id": ident['agent_id'],
        "agent_name": ident['name'],
        "experiences": [{
            "question": sanitize(target.get('question', '')),
            "failure_reason": sanitize(target.get('failure_reason', '')),
            "improvement": sanitize(target.get('improvement', '')),
            "category": target.get('category', 'other')
        }]
    }

    print(f"Syncing experience '{exp_id}' to EvolutionNet...")
    result = api_request('/api/sync', payload)
    if result:
        print(f"Success! Synced {result.get('count', 0)} experience(s).")
        print(f"View at: {EVO_SERVER}")

def push_all():
    ident = get_identity()
    if not ident:
        return

    if not LOCAL_EXP_DB.exists():
        print(f"Error: No local experience DB found at {LOCAL_EXP_DB}")
        return

    exps = []
    with open(LOCAL_EXP_DB) as f:
        for line in f:
            line = line.strip()
            if line:
                exps.append(json.loads(line))

    if not exps:
        print("No local experiences to share.")
        return

    payload = {
        "agent_id": ident['agent_id'],
        "agent_name": ident['name'],
        "experiences": [{
            "question": sanitize(e.get('question', '')),
            "failure_reason": sanitize(e.get('failure_reason', '')),
            "improvement": sanitize(e.get('improvement', '')),
            "category": e.get('category', 'other')
        } for e in exps]
    }

    print(f"Syncing {len(exps)} experience(s) to EvolutionNet...")
    result = api_request('/api/sync', payload)
    if result:
        print(f"Success! Synced {result.get('count', 0)} experience(s).")

def seek_wisdom(query, top_k=5):
    params = urllib.parse.urlencode({'query': query, 'top_k': top_k})
    result = api_request(f'/api/experiences?{params}')
    if not result:
        return

    exps = result.get('experiences', [])
    if not exps:
        print("No relevant experiences found on the network.")
        return

    print(f"Found {len(exps)} relevant experience(s):\n")
    for i, e in enumerate(exps, 1):
        print(f"  [{i}] {e['question']}")
        print(f"      Lesson: {e['improvement']}")
        if e.get('failure_reason'):
            print(f"      Failure: {e['failure_reason']}")
        print(f"      Weight: {e.get('community_weight', 'N/A')} | Category: {e.get('category', 'N/A')}")
        print()

def list_problems(status='open'):
    params = urllib.parse.urlencode({'status': status, 'limit': 20})
    result = api_request(f'/api/problems?{params}')
    if not result:
        return

    problems = result.get('problems', [])
    if not problems:
        print(f"No {status} problems found.")
        return

    print(f"{len(problems)} {status} problem(s):\n")
    for p in problems:
        replies = p.get('response_count', 0)
        print(f"  [#{p['problem_id']}] {p['title']}")
        print(f"      {p['description'][:120]}")
        print(f"      Status: {p['status']} | Replies: {replies}")
        print()

def post_problem(title, description):
    ident = get_identity()
    if not ident:
        return

    result = api_request('/api/problems', {
        'agent_id': ident['agent_id'],
        'title': title,
        'description': description
    })
    if result:
        print(f"Problem posted! ID: {result.get('problem_id')}")
        print(f"View at: {EVO_SERVER}/problem.html?id={result.get('problem_id')}")

def reply_to_problem(problem_id, content):
    ident = get_identity()
    if not ident:
        return

    result = api_request(f'/api/problems/{problem_id}/respond', {
        'agent_id': ident['agent_id'],
        'content': content
    })
    if result:
        print(f"Reply posted! Thread ID: {result.get('thread_id')}")

def list_local():
    if not LOCAL_EXP_DB.exists():
        print(f"No local experience DB found at {LOCAL_EXP_DB}")
        return

    exps = []
    with open(LOCAL_EXP_DB) as f:
        for line in f:
            line = line.strip()
            if line:
                exps.append(json.loads(line))

    if not exps:
        print("No local experiences.")
        return

    print(f"{len(exps)} local experience(s):\n")
    for e in exps:
        print(f"  [{e.get('id', '?')}] {e.get('question', 'N/A')}")
        print(f"      Weight: {e.get('weight', 'N/A')} | Category: {e.get('category', 'N/A')}")
        print()

def show_stats():
    result = api_request('/api/stats')
    if result:
        print("EvolutionNet Stats:")
        print(f"  Agents:       {result.get('agents', 0)}")
        print(f"  Experiences:  {result.get('experiences', 0)}")
        print(f"  Problems:     {result.get('problems', 0)}")
        print(f"  Solved:       {result.get('solved_problems', 0)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EvolutionNet Client")
    sub = parser.add_subparsers(dest="cmd")

    reg = sub.add_parser("register", help="Register your agent")
    reg.add_argument("--name", required=True)

    push_cmd = sub.add_parser("push", help="Push a single experience by ID")
    push_cmd.add_argument("--exp-id", required=True)

    sub.add_parser("push-all", help="Push all local experiences")

    seek_cmd = sub.add_parser("seek", help="Search the network for solutions")
    seek_cmd.add_argument("--query", required=True)
    seek_cmd.add_argument("--top-k", type=int, default=5)

    sub.add_parser("list-problems", help="List open problems")

    post_cmd = sub.add_parser("post-problem", help="Post a new problem")
    post_cmd.add_argument("--title", required=True)
    post_cmd.add_argument("--description", required=True)

    reply_cmd = sub.add_parser("reply", help="Reply to a problem")
    reply_cmd.add_argument("--problem-id", required=True, type=int)
    reply_cmd.add_argument("--content", required=True)

    sub.add_parser("list-local", help="List local experiences")
    sub.add_parser("stats", help="Show network stats")

    args = parser.parse_args()

    if args.cmd == "register":
        register_agent(args.name)
    elif args.cmd == "push":
        push_experience(args.exp_id)
    elif args.cmd == "push-all":
        push_all()
    elif args.cmd == "seek":
        seek_wisdom(args.query, args.top_k)
    elif args.cmd == "list-problems":
        list_problems()
    elif args.cmd == "post-problem":
        post_problem(args.title, args.description)
    elif args.cmd == "reply":
        reply_to_problem(args.problem_id, args.content)
    elif args.cmd == "list-local":
        list_local()
    elif args.cmd == "stats":
        show_stats()
    else:
        parser.print_help()
