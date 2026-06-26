#!/usr/bin/env python3
"""ArmorClaw CLI — manage your vault from the terminal."""
import sys, os, getpass, json
from pathlib import Path


def _get_ck():
    from armorclaw import ArmorClaw
    return ArmorClaw()


def _unlock_interactive(ck) -> bool:
    pwd = getpass.getpass("🔐 ArmorClaw master password: ")
    result = ck.unlock(pwd)
    if not result["ok"]:
        print(f"❌ {result.get('error', 'Unknown error')}")
        return False
    print("✅ Vault unlocked")
    return True


def _run_import(ck, env_path: str, bulk_action: str | None = None):
    """Shared import flow. bulk_action skips per-file prompts if set."""
    from armorclaw.importer import import_env_file, handle_env_after_import
    print(f"Importing: {env_path}")
    result = import_env_file(env_path, ck._session._password)
    if result.get("error"):
        print(f"  ❌ {result['error']}"); return

    imported = result.get("imported", [])
    skipped  = result.get("skipped", [])
    print(f"  ✅ Imported {len(imported)} keys: {', '.join(imported[:5])}{'...' if len(imported)>5 else ''}")
    if skipped:
        print(f"  ⏭️  Skipped {len(skipped)} empty keys")

    # Use bulk action if set, otherwise ask per file
    action = bulk_action
    if action is None:
        print("\n  What should we do with this .env file?")
        print("    1. Delete it  ⚠️")
        print("    2. Backup it")
        print("    3. Keep it")
        action_map = {"1": "delete", "2": "backup", "3": "keep"}
        action = action_map.get(input("  Choose [1-3]: ").strip(), "keep")

        if action == "delete":
            confirm = input("  ⚠️  Are you sure? [yes/N]: ")
            if confirm.lower() != "yes":
                action = "keep"

    cleanup = handle_env_after_import(env_path, action)
    if cleanup.get("action") == "backup":
        print(f"  💾 Backup: {cleanup['backup']}")
    elif cleanup.get("action") == "deleted":
        print("  🗑️  Deleted")
    else:
        print("  📁 Kept as-is")


def cmd_init():
    ck = _get_ck()
    if ck.is_setup:
        print("Vault already initialized at ~/.armorclaw/vault.db")
        return

    print("\n🔐 ArmorClaw Setup\n" + "─"*40)
    print("Create your master password.")
    print("Requirements: 12+ chars, uppercase, number, special char\n")

    from armorclaw.auth import validate_password
    while True:
        pwd = getpass.getpass("Master password: ")
        errors = validate_password(pwd)
        if errors:
            for e in errors: print(f"  ❌ {e}")
            continue
        confirm = getpass.getpass("Confirm password: ")
        if pwd != confirm:
            print("  ❌ Passwords don't match")
            continue
        break

    print("\nLock mode:")
    print("  1. Password only        — type master password each time")
    print("  2. Machine lock         — only unlocks on this machine (MAC address)")
    print("  3. Machine + Static IP  — machine AND your external static IP (strongest)")
    print("  4. Bot auto-unlock      — bot uses stored password (convenient)")
    print()
    choice = input("Choose [1-4]: ").strip()

    mode_map = {"1": "password", "2": "machine", "3": "machine+static-ip", "4": "bot"}
    mode = mode_map.get(choice, "password")
    reg_machine = "machine" in mode
    reg_ip      = "static-ip" in mode
    ip_type     = "external" if reg_ip else "local"

    if reg_ip:
        print()
        print("  ⚠️  STATIC IP WARNING")
        print("  ─────────────────────────────────────────────────────")
        print("  IP restriction should ONLY be used with a STATIC")
        print("  external IP address. Dynamic/rotating IPs will lock")
        print("  you out of your own vault when your IP changes.")
        print()
        print("  ✅ Good for: business fiber, VPS, dedicated server")
        print("  ❌ Risky for: home cable/DSL (IP changes periodically)")
        print()
        has_static = input("  Do you have a static external IP? [yes/no]: ").strip().lower()
        if has_static != "yes":
            print()
            print("  Switching to machine-only lock (safer for dynamic IPs)")
            mode    = "machine"
            reg_ip  = False
            ip_type = "local"
        else:
            print("\n  Fetching your current external IP...")
            from armorclaw.auth import get_external_ip
            ext_ip = get_external_ip()
            if ext_ip:
                print(f"  Detected: {ext_ip}")
                confirm = input(f"  Register this IP? [Y/n]: ").strip().lower()
                if confirm in ("", "y", "yes"):
                    print(f"  ✅ External IP {ext_ip} will be registered")
                else:
                    manual = input("  Enter your static external IP: ").strip()
                    ext_ip = manual
            else:
                print("  Could not auto-detect. Please enter manually.")
                ext_ip = input("  Your static external IP: ").strip()

    result = ck.setup(password=pwd, mode=mode,
                      register_machine=reg_machine,
                      register_ip=reg_ip,
                      ip_type=ip_type)
    if not result["ok"]:
        print(f"❌ Setup failed: {result}"); return

    print(f"\n✅ Step 1 complete — Vault initialized (mode: {mode})")
    print(f"   Location: ~/.armorclaw/vault.db")

    from armorclaw import ArmorClaw
    ck_session = ArmorClaw()
    ck_session.unlock(pwd)

    # ── Step 3: Bot access ────────────────────────────────────────────
    print()
    print("─"*50)
    print("Step 3 — Give your bot access to the vault")
    print("─"*50)
    print("Stores your master password in OpenClaw's protected")
    print("config so the bot auto-unlocks the vault at startup.")
    print()
    give_access = input("Configure bot auto-unlock? [Y/n]: ").strip().lower()
    if give_access in ("", "y", "yes"):
        import subprocess, json as _json

        # Use getpass so password is never visible on screen
        print("Enter your master password to store for bot access.")
        print("(Input is hidden — nothing will appear as you type)")
        bot_pwd = getpass.getpass("🔐 Master password (hidden): ")

        # Encrypt password with machine binding before writing to config
        config_path = Path.home() / ".openclaw" / "openclaw.json"
        try:
            from armorclaw.machine_crypto import encrypt_for_machine
            encrypted = encrypt_for_machine(bot_pwd)

            with open(config_path) as f:
                cfg = _json.load(f)
            cfg.setdefault("env", {})["ARMORCLAW_PASSWORD"] = encrypted
            with open(config_path, "w") as f:
                _json.dump(cfg, f, indent=2)
            print("✅ Bot access configured — vault auto-unlocks on startup")
            print("   Password stored machine-encrypted (enc:v1:...)")
            print("   Even if openclaw.json is stolen, password cannot be read")
            print("   on any other machine.")
        except Exception as e:
            print(f"⚠️  Could not write to openclaw.json: {e}")
            print("   Add manually: open ~/.openclaw/openclaw.json")
            print('   Set: "ARMORCLAW_PASSWORD": "your-password"  under "env":')
    else:
        print("⏭️  Skipped — you can configure bot access later")

    # ── Steps 4 & 5: Scan and import ─────────────────────────────────
    print()
    print("─"*50)
    print("Steps 4 & 5 — Scan and import .env files")
    print("─"*50)
    do_import = input("Scan for .env files to import now? [Y/n]: ").strip().lower()
    if do_import in ("", "y", "yes"):
        print("\nScanning...")
        found = ck_session.scan_envs()
        if not found:
            print("No .env files found — run 'armorclaw import' later")
        else:
            print(f"\nFound {len(found)} file(s):")
            for i, f in enumerate(found, 1):
                print(f"  {i}. {f}")
            print()
            print("Enter numbers to import (comma-separated), 'all', or Enter to skip:")
            choice = input("→ ").strip()
            if choice:
                paths_to_import = []
                if choice.lower() == "all":
                    paths_to_import = found
                elif "," in choice or choice.isdigit():
                    for part in choice.split(","):
                        part = part.strip()
                        try:
                            paths_to_import.append(found[int(part) - 1])
                        except (ValueError, IndexError):
                            print(f"  ⚠️  Skipping: {part}")
                else:
                    paths_to_import = [choice]

                if paths_to_import:
                    bulk_action = None
                    if len(paths_to_import) > 1:
                        print()
                        print("What to do with ALL original .env files?")
                        print("  1. Delete all ⚠️   2. Backup all   3. Keep all   4. Ask each time")
                        bulk_action = {"1":"delete","2":"backup","3":"keep","4":None}.get(
                            input("Choose [1-4]: ").strip(), "keep")
                        if bulk_action == "delete":
                            confirm = input("⚠️  Are you sure? [yes/N]: ")
                            if confirm.lower() != "yes":
                                bulk_action = "keep"
                    print()
                    for path in paths_to_import:
                        _run_import(ck_session, path, bulk_action=bulk_action)
                        print()
    else:
        print("⏭️  Skipped — run 'armorclaw import' anytime to add keys")

    print()
    print("─"*50)
    print("✅ ArmorClaw setup complete!")
    print("   armorclaw list     — view stored secrets")
    print("   armorclaw import   — add more .env files")
    print("   armorclaw --help   — all commands")
    print("─"*50)
    print()


def cmd_set(name: str, value: str | None = None):
    ck = _get_ck()
    if not ck.is_setup:
        print("❌ Run: armorclaw init"); return
    if not _unlock_interactive(ck): return
    if not value:
        value = getpass.getpass(f"Value for {name}: ")
    ck.set(name, value)
    print(f"✅ {name} stored in vault")


def cmd_get(name: str):
    ck = _get_ck()
    if not ck.is_setup:
        print("❌ Run: armorclaw init"); return
    if not _unlock_interactive(ck): return
    val = ck.get(name)
    if val is None:
        print(f"❌ Key not found: {name}")
    else:
        print(val)


def cmd_list():
    ck = _get_ck()
    if not ck.is_setup:
        print("❌ Run: armorclaw init"); return
    if not _unlock_interactive(ck): return
    secrets = ck.list()
    if not secrets:
        print("Vault is empty")
        return
    print(f"\n🔐 ArmorClaw — {len(secrets)} secrets\n" + "─"*40)
    for s in secrets:
        tags = f"  [{', '.join(s['tags'])}]" if s.get("tags") else ""
        print(f"  {s['name']:<30}{tags}")
    print()


def cmd_delete(name: str):
    ck = _get_ck()
    if not ck.is_setup:
        print("❌ Run: armorclaw init"); return
    if not _unlock_interactive(ck): return
    confirm = input(f"Delete '{name}'? This cannot be undone. [yes/N]: ")
    if confirm.lower() != "yes":
        print("Cancelled"); return
    if ck.delete(name):
        print(f"✅ {name} deleted")
    else:
        print(f"❌ Not found: {name}")


def cmd_import(env_path: str | None = None):
    ck = _get_ck()
    if not ck.is_setup:
        print("❌ Run: armorclaw init"); return

    if not _unlock_interactive(ck): return

    if env_path:
        _run_import(ck, env_path)
        return

    print("\nScanning for .env files...")
    found = ck.scan_envs()
    if not found:
        print("No .env files found")
        return

    print("\nFound:")
    for i, f in enumerate(found, 1):
        print(f"  {i}. {f}")

    print()
    print("Enter numbers to import (comma-separated), 'all' for everything, or a path:")
    print("Examples:  1,3,5   or   all   or   /path/to/.env")
    choice = input("→ ").strip()

    if not choice:
        print("Cancelled"); return

    paths_to_import = []

    if choice.lower() == "all":
        paths_to_import = found
    elif "," in choice or choice.isdigit():
        for part in choice.split(","):
            part = part.strip()
            try:
                paths_to_import.append(found[int(part) - 1])
            except (ValueError, IndexError):
                print(f"  ⚠️  Skipping invalid selection: {part}")
    else:
        paths_to_import = [choice]

    if not paths_to_import:
        print("Nothing to import"); return

    print(f"\nImporting {len(paths_to_import)} file(s)...")

    # If multiple files, ask once what to do with ALL originals
    bulk_action = None
    if len(paths_to_import) > 1:
        print()
        print("What should we do with ALL original .env files after import?")
        print("  1. Delete all   ⚠️  (keys only in vault from now on)")
        print("  2. Backup all   (copies saved, originals deleted)")
        print("  3. Keep all     (leave them as-is — safe for now)")
        print("  4. Ask me each time")
        action_map = {"1": "delete", "2": "backup", "3": "keep", "4": None}
        bulk_action = action_map.get(input("Choose [1-4]: ").strip(), "keep")

        if bulk_action == "delete":
            confirm = input("⚠️  Are you sure? Any tool still using these .env files will break. [yes/N]: ")
            if confirm.lower() != "yes":
                bulk_action = "keep"
                print("Switching to keep — originals will be left as-is")
    print()

    for path in paths_to_import:
        _run_import(ck, path, bulk_action=bulk_action)
        print()


def cmd_log(name: str | None = None):
    ck = _get_ck()
    if not ck.is_setup:
        print("❌ Run: armorclaw init"); return
    if not _unlock_interactive(ck): return
    log = ck.access_log(name, limit=20)
    if not log:
        print("No access log entries"); return
    print(f"\n📋 Access Log\n" + "─"*50)
    for entry in log:
        print(f"  [{entry['accessed_at'][:16]}] {entry['action']:<8} {entry['secret_name']:<20} skill={entry['skill'] or 'manual'}")
    print()


def cmd_report():
    ck = _get_ck()
    if not ck.is_setup:
        print("❌ Run: armorclaw init"); return
    if not _unlock_interactive(ck): return
    report = ck.skill_report()
    if not report:
        print("No skill usage yet"); return
    print(f"\n📊 Skill Usage Report\n" + "─"*50)
    for skill, keys in report.items():
        print(f"\n  {skill}:")
        for key, count in keys.items():
            print(f"    {key:<30} {count} reads")
    print()


def cmd_config():
    """Change lock mode, add/remove IP or machine binding."""
    ck = _get_ck()
    if not ck.is_setup:
        print("❌ Run: armorclaw init"); return
    if not _unlock_interactive(ck): return

    from armorclaw.store import get_lock_config
    from armorclaw.config_mgr import (add_static_ip, remove_ip_restriction,
                                      add_machine_binding, remove_machine_binding)

    cfg = get_lock_config()
    print(f"\n🔐 Current lock config")
    print(f"  Mode:       {cfg.mode}")
    print(f"  Machine:    {'registered' if cfg.registered_fingerprint else 'none'}")
    print(f"  IP:         {cfg.registered_ip or 'none'} ({cfg.ip_type})")
    print()
    print("What would you like to change?")
    print("  1. Add static external IP restriction")
    print("  2. Remove IP restriction")
    print("  3. Add machine binding (lock to this machine)")
    print("  4. Remove machine binding")
    print("  5. Cancel")
    choice = input("Choose [1-5]: ").strip()

    if choice == "1":
        print()
        print("  ⚠️  STATIC IP WARNING")
        print("  Only use this if you have a static external IP.")
        print("  Dynamic IPs will lock you out when they change.")
        confirm = input("  Do you have a static external IP? [yes/no]: ").strip().lower()
        if confirm != "yes":
            print("  Cancelled — IP restriction not added"); return
        ok, msg = add_static_ip(use_external=True)
        print(f"  {'✅' if ok else '❌'} {msg}")

    elif choice == "2":
        ok, msg = remove_ip_restriction()
        print(f"  {'✅' if ok else '❌'} {msg}")

    elif choice == "3":
        ok, msg = add_machine_binding()
        print(f"  {'✅' if ok else '❌'} {msg}")

    elif choice == "4":
        confirm = input("  ⚠️  Remove machine binding? Vault will open on any machine. [yes/N]: ")
        if confirm.lower() == "yes":
            ok, msg = remove_machine_binding()
            print(f"  {'✅' if ok else '❌'} {msg}")
        else:
            print("  Cancelled")
    else:
        print("  Cancelled")
    print()


def cmd_export(output_path: str | None = None):
    """Export vault secrets back to a .env file. Requires master password."""
    ck = _get_ck()
    if not ck.is_setup:
        print("❌ Run: armorclaw init"); return

    print("\n⚠️  EXPORT WARNING")
    print("   This writes your secrets to a plain text .env file.")
    print("   Make sure you store it securely and delete when done.")
    print()
    confirm = input("Continue? [yes/N]: ").strip().lower()
    if confirm != "yes":
        print("Cancelled"); return

    if not _unlock_interactive(ck): return

    if not output_path:
        output_path = input("Output path [./exported.env]: ").strip() or "./exported.env"

    from armorclaw.config_mgr import export_to_env
    result = export_to_env(ck._session._password, output_path)

    if result.get("error"):
        print(f"❌ {result['error']}"); return

    exported = result.get("exported", [])
    skipped  = result.get("skipped", [])
    print(f"\n✅ Exported {len(exported)} keys to: {result['path']}")
    print(f"   File permissions set to 600 (owner read-only)")
    if skipped:
        print(f"   Skipped: {', '.join(skipped[:5])}")
    print()
    print("⚠️  Remember: delete this file when you're done with it!")
    print()


COMMANDS = {
    "init":    (cmd_init,   "Initialize vault"),
    "set":     (cmd_set,    "Store a secret: armorclaw set KEY_NAME [value]"),
    "get":     (cmd_get,    "Get a secret:   armorclaw get KEY_NAME"),
    "list":    (cmd_list,   "List all secrets"),
    "delete":  (cmd_delete, "Delete a secret: armorclaw delete KEY_NAME"),
    "import":  (cmd_import, "Import .env file: armorclaw import [path]"),
    "export":  (cmd_export, "Export secrets to .env: armorclaw export [path]"),
    "config":  (cmd_config, "Change lock mode, IP, or machine binding"),
    "log":     (cmd_log,    "View access log: armorclaw log [KEY_NAME]"),
    "report":  (cmd_report, "Skill usage report"),
}


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print("\n🔐 ArmorClaw — Encrypted secrets manager for OpenClaw")
        print("─"*50)
        for cmd, (_, desc) in COMMANDS.items():
            print(f"  armorclaw {cmd:<10} {desc}")
        print()
        return

    cmd = args[0].lower()
    if cmd not in COMMANDS:
        print(f"❌ Unknown command: {cmd}")
        return

    fn, _ = COMMANDS[cmd]
    extra = args[1:]
    try:
        fn(*extra)
    except TypeError:
        fn()
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
