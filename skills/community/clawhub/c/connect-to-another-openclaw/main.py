#!/usr/bin/env python3
"""
Connect to Another OpenClaw - Skill Implementation
Provides SSH-based remote OpenClaw management and skill synchronization.
"""

import os
import sys
import subprocess
import argparse
import json
from pathlib import Path
from typing import Tuple, List, Optional

# Configuration defaults
DEFAULT_SSH_KEY = os.path.expanduser("~/.ssh/id_rsa")
DEFAULT_USER = "root"
DEFAULT_GATEWAY_PORT = 18790
DEFAULT_SSH_PORT = 22

class RemoteOpenClaw:
    def __init__(self, host: str, user: str = DEFAULT_USER, ssh_key: str = DEFAULT_SSH_KEY, ssh_port: int = DEFAULT_SSH_PORT):
        self.host = host
        self.user = user
        self.ssh_key = ssh_key
        self.ssh_port = str(ssh_port)
        self.ssh_base = ["ssh", "-i", self.ssh_key, "-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout=15", "-p", self.ssh_port, f"{self.user}@{self.host}"]

    def run(self, cmd: str, timeout: int = 30) -> Tuple[int, str, str]:
        """Run a remote command via SSH and return (returncode, stdout, stderr)"""
        full_cmd = self.ssh_base + [cmd]
        try:
            proc = subprocess.run(full_cmd, capture_output=True, text=True, timeout=timeout)
            return proc.returncode, proc.stdout, proc.stderr
        except subprocess.TimeoutExpired:
            return -1, "", f"SSH command timed out after {timeout}s"
        except Exception as e:
            return -1, "", str(e)

    def test_connection(self) -> bool:
        """Test basic SSH connectivity"""
        rc, out, err = self.run("echo 'OK'")
        return rc == 0 and "OK" in out

    def gateway_status(self) -> dict:
        """Get OpenClaw gateway status"""
        rc, out, err = self.run("openclaw gateway status")
        if rc != 0:
            return {"error": err}
        return {"raw": out, "status": "running" if "Runtime: running" in out else "stopped"}

    def channels_list(self) -> dict:
        """List configured channels"""
        rc, out, err = self.run("openclaw channels list 2>&1")
        if rc != 0:
            return {"error": err}
        return {"raw": out}

    def sessions_list(self, filter_qqbot: bool = False) -> dict:
        """List active sessions"""
        rc, out, err = self.run("openclaw sessions 2>&1")
        if rc != 0:
            return {"error": err}
        lines = out.strip().split("\n")
        if filter_qqbot:
            qqbot_sessions = [line for line in lines if "qqbot" in line.lower()]
            return {"sessions": qqbot_sessions, "count": len(qqbot_sessions)}
        return {"sessions": lines, "count": len(lines)}

    def check_port_conflict(self, port: int = DEFAULT_GATEWAY_PORT) -> dict:
        """Check if port is in use and return occupying processes"""
        rc, out, err = self.run(f"lsof -i :{port} 2>/dev/null || ss -tulpn | grep :{port}")
        return {"occupied": bool(out.strip()), "details": out.strip()}

    def kill_conflicts(self) -> dict:
        """Kill common conflicting processes"""
        cmds = [
            "pkill -f 'ssh -N.*18790' || true",
            "pkill -f 'voice-bridge-light' || true"
        ]
        results = []
        for cmd in cmds:
            rc, out, err = self.run(cmd)
            results.append({"cmd": cmd, "rc": rc, "output": out})
        return {"results": results}

    def restart_gateway(self) -> dict:
        """Restart OpenClaw gateway service"""
        rc, out, err = self.run("openclaw gateway restart")
        return {"rc": rc, "output": out, "error": err}

    def list_skills(self) -> dict:
        """List all installed skills on remote"""
        rc, out, err = self.run("ls -1 ~/.openclaw/workspace/skills/ 2>/dev/null | grep -v '^\\.' | sort")
        if rc != 0:
            return {"error": err}
        skills = out.strip().split("\n") if out.strip() else []
        return {"skills": skills, "count": len(skills)}

    def compare_skills(self, local_skills_file: str) -> dict:
        """Compare local skills file with remote skills"""
        remote_data = self.list_skills()
        if "error" in remote_data:
            return remote_data

        # Read local skills
        try:
            with open(local_skills_file) as f:
                local_skills = [line.strip() for line in f if line.strip()]
        except Exception as e:
            return {"error": f"Failed to read local skills: {e}"}

        remote_skills = remote_data["skills"]
        local_set = set(local_skills)
        remote_set = set(remote_skills)

        return {
            "common": sorted(local_set & remote_set),
            "local_only": sorted(local_set - remote_set),
            "remote_only": sorted(remote_set - local_set),
            "stats": {
                "local_total": len(local_skills),
                "remote_total": len(remote_skills),
                "common_count": len(local_set & remote_set),
                "local_only_count": len(local_set - remote_set),
                "remote_only_count": len(remote_set - local_set)
            }
        }

    def install_skill(self, skill_name: str) -> dict:
        """Install a skill on remote via SkillHub"""
        rc, out, err = self.run("cd ~/.openclaw/workspace && ~/.local/bin/skillhub install " + skill_name)
        return {"rc": rc, "output": out, "error": err, "skill": skill_name}

    def tail_logs(self, lines: int = 20, filter: str = "qqbot") -> dict:
        """Tail OpenClaw logs with optional filter"""
        cmd = f"tail -{lines} /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log"
        if filter:
            cmd += f" | grep -i '{filter}'"
        rc, out, err = self.run(cmd)
        return {"rc": rc, "output": out, "error": err}

def main():
    parser = argparse.ArgumentParser(description="Connect to and manage another OpenClaw server")
    parser.add_argument("--host", required=True, help="Remote host IP or domain")
    parser.add_argument("--user", default=DEFAULT_USER, help="SSH username")
    parser.add_argument("--key", default=DEFAULT_SSH_KEY, help="SSH private key path")
    parser.add_argument("--ssh-port", type=int, default=DEFAULT_SSH_PORT, help="SSH port")
    parser.add_argument("--action", required=True,
                        choices=["test-connection", "status", "fix-port", "list-skills", "diff", "sync-to-local", "sync-to-remote", "list-sessions", "tail-logs"],
                        help="Action to perform")
    parser.add_argument("--local-skills-file", default="/root/.openclaw/workspace/local_skills.txt",
                        help="Local skills list file for diff action")
    parser.add_argument("--skill", help="Specific skill to install (used with sync-to-remote)")
    parser.add_argument("--yes", action="store_true", help="Auto-confirm prompts")

    args = parser.parse_args()

    # Initialize client
    client = RemoteOpenClaw(args.host, user=args.user, ssh_key=args.key, ssh_port=args.ssh_port)

    # Execute action
    if args.action == "test-connection":
        ok = client.test_connection()
        print("✅ Connected" if ok else "❌ Connection failed")
        sys.exit(0 if ok else 1)

    elif args.action == "status":
        gw = client.gateway_status()
        ch = client.channels_list()
        sess = client.sessions_list()
        print(f"=== Gateway Status ===\n{gw.get('raw', gw)}\n")
        print(f"=== Channels ===\n{ch.get('raw', '')}\n")
        print(f"=== Sessions (total: {sess.get('count',0)}) ===")
        for line in sess.get('sessions', [])[:10]:
            print(line)

    elif args.action == "fix-port":
        print("Checking port conflicts...")
        conflict = client.check_port_conflict()
        if conflict["occupied"]:
            print("Port 18790 is occupied:\n" + conflict["details"])
            print("Killing conflicting processes...")
            kill_res = client.kill_conflicts()
            print("Conflicts cleared. Restarting gateway...")
            restart = client.restart_gateway()
            print(f"Restart result: {restart.get('output', restart)}")
            # Verify
            import time; time.sleep(3)
            gw = client.gateway_status()
            print("Gateway status after restart:\n" + gw.get("raw", ""))
        else:
            print("✅ Port 18790 is free. No action needed.")

    elif args.action == "list-skills":
        skills = client.list_skills()
        if "error" in skills:
            print(f"Error: {skills['error']}")
            sys.exit(1)
        print(f"Remote skills ({skills['count']}):")
        for s in skills["skills"]:
            print(f"  - {s}")

    elif args.action == "diff":
        diff = client.compare_skills(args.local_skills_file)
        if "error" in diff:
            print(f"Error: {diff['error']}")
            sys.exit(1)
        stats = diff["stats"]
        print(f"=== Skill Comparison ===")
        print(f"Local total: {stats['local_total']}")
        print(f"Remote total: {stats['remote_total']}")
        print(f"Common: {stats['common_count']}")
        print(f"Local only: {stats['local_only_count']}")
        print(f"Remote only: {stats['remote_only_count']}")
        if diff["remote_only"]:
            print("\nSkills on remote but not local (top 20):")
            for s in diff["remote_only"][:20]:
                print(f"  - {s}")
        if diff["local_only"]:
            print("\nSkills on local but not remote:")
            for s in diff["local_only"]:
                print(f"  + {s}")

    elif args.action == "sync-to-local":
        diff = client.compare_skills(args.local_skills_file)
        if "error" in diff:
            print(f"Error: {diff['error']}")
            sys.exit(1)
        to_install = diff["remote_only"]
        if not to_install:
            print("✅ No new skills to install.")
            sys.exit(0)
        print(f"Will install {len(to_install)} skills from remote to local:")
        for s in to_install[:10]:
            print(f"  - {s}")
        if len(to_install) > 10:
            print(f"  ... and {len(to_install)-10} more")
        if args.yes or input("Continue? (y/N): ").lower() == 'y':
            for s in to_install:
                print(f"Installing {s}...")
                result = os.system(f"skillhub install {s} 2>&1 | tail -3")
                if result != 0:
                    print(f"  ⚠️  Installation may have failed")
            print("Done. Re-run with 'diff' to verify.")
        else:
            print("Cancelled.")

    elif args.action == "sync-to-remote":
        # Get remote's remote-only skills relative to local
        diff = client.compare_skills(args.local_skills_file)
        if "error" in diff:
            print(f"Error: {diff['error']}")
            sys.exit(1)
        to_install = diff["local_only"]
        if not to_install:
            print("✅ Remote already has all local skills.")
            sys.exit(0)
        print(f"Will install {len(to_install)} skills from local to remote:")
        for s in to_install[:10]:
            print(f"  - {s}")
        if len(to_install) > 10:
            print(f"  ... and {len(to_install)-10} more")
        if args.yes or input("Continue? (y/N): ").lower() == 'y':
            for s in to_install:
                print(f"Remote installing: {s}")
                result = client.install_skill(s)
                if result["rc"] != 0:
                    print(f"  ❌ Failed: {result.get('error','')}")
                else:
                    print(f"  ✅ Installed")
            print("Done.")
        else:
            print("Cancelled.")

    elif args.action == "list-sessions":
        sess = client.sessions_list(filter_qqbot=True)
        print(f"QQBot sessions: {sess.get('count',0)}")
        for line in sess.get("sessions", [])[:15]:
            print(line)

    elif args.action == "tail-logs":
        lines = 20
        filt = "qqbot"
        result = client.tail_logs(lines, filt)
        print(result.get("output", ""))

    else:
        parser.error(f"Unknown action: {args.action}")

if __name__ == "__main__":
    main()
