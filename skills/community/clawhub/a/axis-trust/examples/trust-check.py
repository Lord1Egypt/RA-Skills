#!/usr/bin/env python3
"""
trust-check.py — Verify an agent's trustworthiness using the AXIS API.

Usage:
    python3 trust-check.py <AUID>
    python3 trust-check.py "axis:autonomous.registry:enterprise:f1a9x9deck2ed7m9261n:f1a99dec2ed79261"

No authentication required. Public endpoint.
Requires: requests (pip install requests)
"""

import sys
import json
import urllib.parse

try:
    import requests
except ImportError:
    print("Install the requests library: pip install requests")
    sys.exit(1)

BASE_URL = "https://www.axistrust.io/api/trpc"


def check_trust(auid: str) -> dict:
    """Look up an agent's public trust profile by AUID."""
    input_param = urllib.parse.quote(json.dumps({"json": {"auid": auid}}))
    url = f"{BASE_URL}/agents.getByAuid?input={input_param}"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()
    return data["result"]["data"]["json"]


def get_trust_verdict(t_score: int) -> str:
    if t_score >= 750:
        return "TRUSTED — Safe to delegate tasks and share data."
    elif t_score >= 500:
        return "VERIFIED — Safe for standard tasks. Verify before sensitive operations."
    elif t_score >= 250:
        return "PROVISIONAL — Low-risk tasks only. Monitor closely."
    else:
        return "UNVERIFIED — Do not delegate. Request manual verification."


def get_credit_verdict(c_score: int) -> str:
    if c_score >= 800:
        return "SAFE — High-value transactions permitted."
    elif c_score >= 600:
        return "STANDARD — Standard transactions permitted."
    elif c_score >= 500:
        return "CAUTION — Require escrow or human approval."
    else:
        return "HIGH RISK — Do not transact."


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <AUID>")
        sys.exit(1)

    auid = sys.argv[1]
    print(f"Looking up agent: {auid}\n")

    try:
        agent = check_trust(auid)
    except requests.HTTPError as e:
        print(f"API error: {e}")
        sys.exit(1)
    except KeyError:
        print("Unexpected response format from AXIS API.")
        sys.exit(1)

    trust = agent.get("trustScore", {})
    credit = agent.get("creditScore", {})
    t_score = trust.get("tScore", 0)
    c_score = credit.get("cScore", 0)

    print("=" * 40)
    print("AXIS Trust Profile")
    print("=" * 40)
    print(f"Name:        {agent.get('name', 'Unknown')}")
    print(f"AUID:        {agent.get('auid', 'Unknown')}")
    print(f"Class:       {agent.get('agentClass', 'Unknown')}")
    print(f"Model:       {agent.get('foundationModel', 'Unknown')}")
    print()
    print(f"T-Score:     {t_score} / 1000  (Tier T{trust.get('trustTier', '?')})")
    print(f"C-Score:     {c_score} / 1000  (Grade {credit.get('creditTier', 'N/A')})")
    print()
    print(f"Trust:   {get_trust_verdict(t_score)}")
    print(f"Credit:  {get_credit_verdict(c_score)}")
    print("=" * 40)


if __name__ == "__main__":
    main()
