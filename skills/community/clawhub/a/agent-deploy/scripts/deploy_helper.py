#!/usr/bin/env python3
"""agent-deploy helper: pre-flight checks + config generation"""
import json, sys, os

def main():
    action = sys.argv[1]
    config_path = os.environ.get("OPENCLAW_CONFIG_PATH",
                                 os.path.expanduser("~/.openclaw/openclaw.json"))

    with open(config_path) as f:
        config = json.load(f)

    if action == "preflight":
        agent_id = sys.argv[2]
        bot_token = sys.argv[3]
        errors = []
        for a in config.get("agents", {}).get("list", []):
            if a.get("id") == agent_id:
                errors.append(f"Agent '{agent_id}' already in agents.list")
        for b in config.get("bindings", []):
            if b.get("agentId") == agent_id:
                errors.append(f"Binding for '{agent_id}' already exists")
            m = b.get("match", {})
            if m.get("channel") == "telegram" and m.get("accountId") == agent_id and b.get("agentId") != agent_id:
                errors.append(f"AccountId '{agent_id}' bound to '{b['agentId']}'")
        accts = config.get("channels", {}).get("telegram", {}).get("accounts", {})
        if agent_id in accts:
            errors.append(f"Telegram account '{agent_id}' already exists")
        for k, v in accts.items():
            if v.get("botToken") == bot_token:
                errors.append(f"Token already used by account '{k}'")
        # Check if still in single-bot mode
        tg = config.get("channels", {}).get("telegram", {})
        if "botToken" in tg and "accounts" not in tg:
            print("MIGRATE_SINGLE_BOT")
        if errors:
            for e in errors:
                print(f"CONFLICT: {e}", file=sys.stderr)
            sys.exit(1)
        print("OK")

    elif action == "gen-agents-list":
        agent_id = sys.argv[2]
        workspace = sys.argv[3]
        lst = config.get("agents", {}).get("list", [])
        lst.append({
            "id": agent_id,
            "workspace": workspace,
            "tools": {"deny": ["gateway"]},
            "sandbox": {
                "mode": "non-main",
                "scope": "agent",
                "workspaceAccess": "none"
            }
        })
        print(json.dumps(lst))

    elif action == "gen-bindings":
        agent_id = sys.argv[2]
        lst = config.get("bindings", [])
        lst.append({
            "agentId": agent_id,
            "match": {"channel": "telegram", "accountId": agent_id}
        })
        print(json.dumps(lst))

    elif action == "migrate-single-bot":
        tg = config.get("channels", {}).get("telegram", {})
        old_token = tg.get("botToken", "")
        old_dm = tg.get("dmPolicy", "pairing")
        if old_token:
            acct = json.dumps({"botToken": old_token, "dmPolicy": old_dm})
            print(acct)
        else:
            print("{}")

    elif action == "list":
        agents = config.get("agents", {}).get("list", [])
        bindings = config.get("bindings", [])
        accounts = config.get("channels", {}).get("telegram", {}).get("accounts", {})
        fmt = "{:<12} {:<3} {:<36} {:<15} {:<12} {}"
        print("Configured Agents")
        print()
        print(fmt.format("ID", "", "Workspace", "Tools Deny", "TG Account", "Bot Token"))
        print("-" * 100)
        for a in agents:
            aid = a.get("id", "?")
            ws = a.get("workspace", "?")
            deny = ",".join(a.get("tools", {}).get("deny", [])) or "none"
            sb_mode = a.get("sandbox", {}).get("mode", "off")
            tg_acct = "none"
            for b in bindings:
                if b.get("agentId") == aid:
                    m = b.get("match", {})
                    if m.get("channel") == "telegram":
                        tg_acct = m.get("accountId", "?")
            token = accounts.get(tg_acct, {}).get("botToken", "N/A")
            t_short = token[:10] + "..." if len(token) > 10 else token
            ws_ok = "OK" if os.path.isdir(ws) else "NO"
            print(fmt.format(aid, ws_ok, ws, deny, tg_acct, t_short))
            print(fmt.format("", "", "", "sandbox=" + sb_mode, "", ""))
        print()
        print(f"Total: {len(agents)} agents | Config: {config_path}")

    elif action == "gen-remove-agents":
        agent_id = sys.argv[2]
        lst = config.get("agents", {}).get("list", [])
        lst = [a for a in lst if a.get("id") != agent_id]
        print(json.dumps(lst))


    elif action == "merge-auth":
        agent_id = sys.argv[2]
        agent_auth_path = os.path.expanduser(
            f"~/.openclaw/agents/{agent_id}/agent/auth-profiles.json"
        )
        main_auth_path = os.path.expanduser(
            "~/.openclaw/agents/main/agent/auth-profiles.json"
        )

        # Start with empty auth
        merged = {"version": 1, "profiles": {}, "lastGood": {}, "usageStats": {}}

        # Source 1: Global auth from openclaw.json
        global_profiles = config.get("auth", {}).get("profiles", {})
        for pid, pdata in global_profiles.items():
            merged["profiles"][pid] = pdata
            provider = pdata.get("provider", pid.split(":")[0])
            merged["lastGood"][provider] = pid
            merged["usageStats"][pid] = {"lastUsed": 0, "errorCount": 0}
            print(f"  [global] {pid}")

        # Source 2: Main agent per-agent auth
        if os.path.isfile(main_auth_path):
            with open(main_auth_path) as f2:
                main_auth = json.load(f2)
            for pid, pdata in main_auth.get("profiles", {}).items():
                if pid not in merged["profiles"]:
                    merged["profiles"][pid] = pdata
                    provider = pdata.get("provider", pid.split(":")[0])
                    merged["lastGood"][provider] = pid
                    merged["usageStats"][pid] = {"lastUsed": 0, "errorCount": 0}
                    print(f"  [main]   {pid}")

        # Write to agent auth dir
        os.makedirs(os.path.dirname(agent_auth_path), exist_ok=True)
        with open(agent_auth_path, "w") as f2:
            json.dump(merged, f2, indent=2)

        print(f"  Total: {len(merged['profiles'])} profiles -> {agent_auth_path}")

    elif action == "gen-remove-bindings":
        agent_id = sys.argv[2]
        lst = config.get("bindings", [])
        lst = [b for b in lst if b.get("agentId") != agent_id]
        print(json.dumps(lst))

if __name__ == "__main__":
    main()
