#!/usr/bin/env python3
import json
import random
import string
from urllib import request

API = "https://api.mail.tm"

WORDS = [
    "amber", "apple", "aqua", "bamboo", "berry", "blue", "brisk", "cedar", "cherry", "cloud",
    "coral", "cosmic", "dawn", "delta", "ember", "forest", "frost", "gold", "harbor", "hazel",
    "indigo", "ivory", "jade", "jolly", "lemon", "lotus", "lunar", "maple", "mist", "moss",
    "nova", "ocean", "olive", "opal", "pearl", "pine", "plum", "polar", "raven", "river",
    "rose", "ruby", "sable", "sage", "sky", "solar", "stone", "sunny", "violet", "willow",
]


def http_json(url, method="GET", data=None, headers=None):
    req = request.Request(url=url, method=method)
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    body = None
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        req.add_header("Content-Type", "application/json")
    with request.urlopen(req, body, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def random_local_part():
    word1 = random.choice(WORDS)
    word2 = random.choice(WORDS)
    digits = "".join(random.choices(string.digits, k=4))
    return f"{word1}.{word2}.{digits}"


def main():
    domains = http_json(f"{API}/domains").get("hydra:member", [])
    if not domains:
        raise SystemExit("No Mail.tm domains available")

    domain = domains[0]["domain"]
    local = random_local_part()
    requested_address = f"{local}@{domain}"
    password = "Tmp!" + "".join(random.choices(string.ascii_letters + string.digits, k=12))

    account = http_json(f"{API}/accounts", method="POST", data={"address": requested_address, "password": password})
    canonical_address = account.get("address") or requested_address
    token_resp = http_json(f"{API}/token", method="POST", data={"address": canonical_address, "password": password})

    print(json.dumps({
        "address": canonical_address,
        "requestedAddress": requested_address,
        "password": password,
        "token": token_resp.get("token"),
        "accountId": account.get("id"),
        "domain": domain,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
