#!/usr/bin/env python3
"""
AgentShield Audit Initiation
Generates keypair, authenticates with AgentShield, runs security audit.

Now with auto-detection capabilities!
"""

import argparse
import base64
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

# AgentShield API endpoint
AGENTSHIELD_API = os.environ.get("AGENTSHIELD_API", "https://agentshield.live")

# Local storage paths
WORKSPACE = Path.home() / ".openclaw" / "workspace"
AGENTSHIELD_DIR = WORKSPACE / ".agentshield"
KEY_FILE = AGENTSHIELD_DIR / "agent.key"
CERT_FILE = AGENTSHIELD_DIR / "certificate.json"
CONFIG_FILE = AGENTSHIELD_DIR / "config.json"

# Files to check for agent name detection
IDENTITY_FILES = [
    WORKSPACE / "IDENTITY.md",
    WORKSPACE / "SOUL.md", 
    WORKSPACE / "AGENTS.md",
]


def ensure_directory():
    """Create .agentshield directory if needed."""
    AGENTSHIELD_DIR.mkdir(parents=True, exist_ok=True)


def detect_agent_name(skip_consent: bool = False):
    """
    Auto-detect agent name from identity files.
    Checks: IDENTITY.md, SOUL.md, AGENTS.md
    
    Args:
        skip_consent: Skip consent prompt (for --yes flag)
    
    Returns: (name, confidence) tuple
    """
    # First check: Do files exist?
    files_found = [f for f in IDENTITY_FILES if f.exists()]
    if not files_found:
        # No files - try environment variables
        env_name = os.environ.get('AGENT_NAME') or os.environ.get('OPENCLAW_AGENT_NAME')
        if env_name:
            return env_name, 0.7
        return None, 0.0
    
    # Files exist - ask for consent BEFORE reading
    if not skip_consent:
        print("\n" + "="*60)
        print("🔐 PRIVACY CONSENT")
        print("="*60)
        print("AgentShield needs to read workspace files to detect your")
        print("agent name:")
        for f in files_found:
            print(f"  • {f.relative_to(WORKSPACE)}")
        print("\nThese files will be read locally only - NOT sent to API.")
        print("You can also use: --name 'YourAgentName' to skip file access.")
        print("="*60)
        
        response = input("\nProceed with file access? [Y/n]: ").strip().lower()
        if response and response not in ('y', 'yes', ''):
            print("\n❌ File access declined.")
            print("   Please run with: --name 'YourAgentName' instead.")
            sys.exit(0)
        print("✓ Consent granted\n")
    
    # NOW read files after consent
    name_patterns = [
        # More strict patterns (MULTILINE flag for line start matching)
        r'^\s*\*\*\s*(?:Name|name)\s*:\*\*\s*(.+)$',  # **Name:** or **name:**
        r'^\s*-\s*\*\*\s*(?:Name|name)\s*:\*\*\s*(.+)$',  # - **Name:**
        r'^\s*#+\s*(?:I am|Name is|About)\s+(.+)$',  # ## I am ...
        # Fallback patterns (less strict)
        r'(?:^|\n)[\s]*[*_-]*\s*(?:Name|name)\s*[*_]*[\s]*[:\-]?\s*[*_]*\s*([^\n*_"\']+)',
    ]
    
    for file_path in files_found:
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            for pattern in name_patterns:
                match = re.search(pattern, content, re.MULTILINE)
                if match:
                    name = match.group(1).strip()
                    # Clean up the name (remove markdown formatting)
                    name = re.sub(r'[\*\-\#\`_:]', '', name).strip()
                    # Validate: reject if contains sentence markers
                    if '.' in name or len(name) > 50 or len(name) < 2:
                        continue
                    return name, 0.9
        except Exception:
            continue
    
    # Hermes fallback: read name from Hermes config directly (no consent needed - config only)
    hermes_detected, hermes_name = detect_hermes()
    if hermes_detected and hermes_name:
        return hermes_name, 0.8

    # Fallback: environment variables
    env_name = (
        os.environ.get('AGENT_NAME') or
        os.environ.get('OPENCLAW_AGENT_NAME') or
        os.environ.get('HERMES_AGENT_NAME')
    )
    if env_name:
        return env_name, 0.7

    return None, 0.0


def detect_hermes():
    """
    Detect if running inside a Hermes Agent environment.
    Checks for ~/.hermes/ directory and common Hermes config files.
    Returns: (detected: bool, agent_name: str or None)
    """
    hermes_dir = Path.home() / ".hermes"

    # Check 1: ~/.hermes/ directory exists
    if not hermes_dir.exists():
        return False, None

    agent_name = None

    # Check 2: ~/.hermes/config.json or ~/.hermes/config.yaml
    for config_name in ["config.json", "config.yaml", "config.yml"]:
        config_file = hermes_dir / config_name
        if config_file.exists():
            try:
                with open(config_file) as f:
                    content = f.read()
                # Try JSON first
                try:
                    config = json.loads(content)
                    agent_name = (
                        config.get('agent_name') or
                        config.get('name') or
                        config.get('agentName')
                    )
                except json.JSONDecodeError:
                    # YAML: look for name: or agent_name: line
                    for line in content.splitlines():
                        line = line.strip()
                        if line.startswith('agent_name:') or line.startswith('name:'):
                            parts = line.split(':', 1)
                            if len(parts) == 2:
                                agent_name = parts[1].strip().strip('"\'')
                                break
            except Exception:
                pass
            break

    # Check 3: ~/.hermes/workspace/ or ~/.hermes/memory/ confirms active install
    workspace_dir = hermes_dir / "workspace"
    memory_dir = hermes_dir / "memory"
    if workspace_dir.exists() or memory_dir.exists():
        return True, agent_name

    # ~/.hermes/ alone is enough
    return True, agent_name


def detect_n8n():
    """
    Detect if running inside an n8n environment.
    Checks for ~/.n8n/ directory and common n8n config files.
    Returns: (detected: bool, agent_name: str or None)
    """
    n8n_dir = Path.home() / ".n8n"
    
    # Check 1: ~/.n8n/ directory exists
    if not n8n_dir.exists():
        return False, None
    
    agent_name = None
    
    # Check 2: ~/.n8n/config file (JSON or plain)
    config_file = n8n_dir / "config"
    if config_file.exists():
        try:
            with open(config_file) as f:
                config = json.load(f)
            # Try to extract a meaningful name
            agent_name = (
                config.get('instanceName') or
                config.get('name') or
                config.get('N8N_INSTANCE_NAME')
            )
        except Exception:
            pass
    
    # Check 3: ~/.n8n/database.sqlite or .n8n/nodes/ (confirms active install)
    db_file = n8n_dir / "database.sqlite"
    nodes_dir = n8n_dir / "nodes"
    if db_file.exists() or nodes_dir.exists():
        return True, agent_name
    
    # ~/.n8n/ exists alone is enough
    return True, agent_name


def detect_platform():
    """
    Auto-detect platform/channel from config files only.
    Does NOT scan environment variables (privacy-first design).
    Returns: (platform, confidence) tuple
    """
    # NOTE: Previously checked environment variables like TELEGRAM_TOKEN,
    # DISCORD_TOKEN, etc. This has been removed for privacy reasons.
    # We only check config files now.

    # Check Hermes first (more specific than generic openclaw fallback)
    hermes_detected, _ = detect_hermes()
    if hermes_detected:
        return "hermes", 0.85

    # Check n8n
    n8n_detected, _ = detect_n8n()
    if n8n_detected:
        return "n8n", 0.85
    
    # Check OpenClaw channel config file
    channel_file = WORKSPACE / ".channel" / "config.json"
    if channel_file.exists():
        try:
            with open(channel_file) as f:
                config = json.load(f)
            channel = config.get('channel', '').lower()
            if channel:
                return channel, 0.9
        except Exception:
            pass
    
    # Default - no env var scanning for privacy
    return "openclaw", 0.5


def detect_platform_from_args(args_platform: str = None) -> tuple:
    """
    Get platform from explicit arguments only.
    Fallback to config file. Never scans environment variables.
    """
    if args_platform and args_platform != "openclaw":
        return args_platform, 1.0
    
    # Try config file
    channel_file = WORKSPACE / ".channel" / "config.json"
    if channel_file.exists():
        try:
            with open(channel_file) as f:
                config = json.load(f)
            channel = config.get('channel', '').lower()
            if channel:
                return channel, 0.9
        except Exception:
            pass
    
    return "openclaw", 0.5


def detect_openclaw_version():
    """
    Detect OpenClaw version.
    Returns: version string or None
    """
    # Try running openclaw command
    try:
        result = subprocess.run(
            ['openclaw', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            if version:
                return version
    except Exception:
        pass
    
    # Check config file
    config_file = Path.home() / ".openclaw" / "openclaw.json"
    if config_file.exists():
        try:
            with open(config_file) as f:
                config = json.load(f)
            version = config.get('version')
            if version:
                return f"openclaw-{version}"
        except Exception:
            pass
    
    return None


def auto_detect_all(skip_consent: bool = False):
    """
    Auto-detect all agent information.
    
    Args:
        skip_consent: Skip consent prompts (for --yes flag)
    
    Returns: dict with name, platform, version and confidence scores
    """
    name, name_conf = detect_agent_name(skip_consent=skip_consent)
    platform, platform_conf = detect_platform()
    version = detect_openclaw_version()

    # n8n: if name not found via IDENTITY.md, try n8n instance name
    if not name and platform == "n8n":
        _, n8n_name = detect_n8n()
        if n8n_name:
            name = n8n_name
            name_conf = 0.75
    
    overall_confidence = (name_conf + platform_conf) / 2
    
    return {
        'name': name,
        'name_confidence': name_conf,
        'platform': platform,
        'platform_confidence': platform_conf,
        'version': version,
        'overall_confidence': overall_confidence
    }


def generate_keypair():
    """Generate Ed25519 keypair for agent identity."""
    try:
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
        
        private_key = Ed25519PrivateKey.generate()
        public_key = private_key.public_key()
        
        # Serialize keys
        private_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        )
        public_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        
        return {
            'private_key': base64.b64encode(private_bytes).decode('utf-8'),
            'public_key': base64.b64encode(public_bytes).decode('utf-8')
        }
    except ImportError:
        print("Error: cryptography library required. Install: pip install cryptography")
        sys.exit(1)


def load_or_create_keys():
    """Load existing keys or generate new ones."""
    ensure_directory()
    
    if KEY_FILE.exists():
        with open(KEY_FILE, 'r') as f:
            return json.load(f)
    
    # Generate new keys
    keys = generate_keypair()
    with open(KEY_FILE, 'w') as f:
        json.dump(keys, f, indent=2)
    # Restrict permissions
    os.chmod(KEY_FILE, 0o600)
    print(f"✓ Generated new agent identity")
    return keys


def sign_challenge(private_key_b64: str, challenge: str) -> str:
    """Sign challenge with private key."""
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    
    private_bytes = base64.b64decode(private_key_b64)
    private_key = Ed25519PrivateKey.from_private_bytes(private_bytes)
    
    signature = private_key.sign(challenge.encode('utf-8'))
    return base64.b64encode(signature).decode('utf-8')


def initiate_audit(agent_name: str, platform: str, agent_version: str = None) -> dict:
    """
    Initiate audit with AgentShield API.
    Returns audit session info.
    """
    import requests
    
    keys = load_or_create_keys()
    
    # Build request payload
    payload = {
        "agent_name": agent_name,
        "platform": platform,
        "public_key": keys['public_key'],
    }
    
    if agent_version:
        payload["agent_version"] = agent_version
    
    try:
        response = requests.post(
            f"{AGENTSHIELD_API}/api/agent-audit/initiate",
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        print(f"Error: Cannot connect to AgentShield API at {AGENTSHIELD_API}")
        print("Please check your internet connection and try again.")
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"Error: API returned error: {e}")
        try:
            error_data = response.json()
            print(f"Details: {error_data.get('error', 'Unknown error')}")
        except:
            pass
        sys.exit(1)


def complete_challenge(audit_id: str, challenge: str, private_key: str) -> dict:
    """Complete challenge-response authentication."""
    import requests
    
    signature = sign_challenge(private_key, challenge)
    
    payload = {
        "audit_id": audit_id,
        "challenge_response": signature
    }
    
    response = requests.post(
        f"{AGENTSHIELD_API}/api/agent-audit/challenge",
        json=payload,
        timeout=30
    )
    response.raise_for_status()
    return response.json()


def run_security_tests(audit_id: str, system_prompt: str = "") -> dict:
    """
    Run 77 security tests using AgentShieldSecurityTester.
    Returns test_results dict.
    """
    print("Running 77 security tests...")
    
    # Import the full test suite
    try:
        from agentshield_tester import AgentShieldSecurityTester
    except ImportError:
        # If agentshield_tester is in same directory
        import sys
        sys.path.insert(0, str(Path(__file__).parent))
        from agentshield_tester import AgentShieldSecurityTester
    
    # Load agent config (minimal for local tests)
    agent_config = {
        "name": "LocalTest",
        "platform": "OpenClaw",
        "audit_id": audit_id
    }
    
    # Initialize tester
    tester = AgentShieldSecurityTester(
        agent_config=agent_config,
        system_prompt=system_prompt,  # Optional: passed via --system-prompt flag
        tools_config=[]
    )
    
    # Run all 77 tests
    results = tester.run_all_tests()
    
    # Print summary
    total = results.get('total_tests', 0)
    passed = results.get('tests_passed', 0)
    score = results.get('overall_score', 0)
    print(f"✓ Tests completed: {passed}/{total} passed")
    print(f"  Security Score: {score}/100")
    
    return results


def complete_audit(audit_id: str, test_results: dict, client) -> dict:
    """Submit test results and receive certificate using client's session."""
    
    # Convert new format (77 tests) to server-compatible summary format
    summary = {
        "security_score": test_results.get('security_score', 0),
        "tests_passed": test_results.get('tests_passed', 0),
        "tests_total": test_results.get('tests_total', 0),
        "tier": test_results.get('tier', 'UNKNOWN'),
        "critical_failures": test_results.get('critical_failures', 0),
        "high_failures": test_results.get('high_failures', 0),
        "medium_failures": test_results.get('medium_failures', 0)
    }
    
    # ✅ v1.0.32 FIX: Sanitize detailed results (whitelist approach)
    # Only send test_id, passed, category - NOT payloads/responses/evidence
    payload = {
        "audit_id": audit_id,
        "test_results": summary,
        "detailed_results": client._sanitize_test_details(
            test_results.get('test_results', [])
        )
    }
    
    # ✅ v1.0.32 FIX: Use client's session (maintains auth state from challenge)
    response = client.session.post(
        f"{client.api_url}/api/agent-audit/complete",
        json=payload,
        timeout=30
    )
    response.raise_for_status()
    return response.json()


def save_certificate(certificate: dict):
    """Save certificate to local storage."""
    ensure_directory()
    with open(CERT_FILE, 'w') as f:
        json.dump(certificate, f, indent=2)
    os.chmod(CERT_FILE, 0o644)


def main():
    parser = argparse.ArgumentParser(
        description="Initiate AgentShield security audit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Auto-detect everything from files (recommended)
  python initiate_audit.py --auto
  
  # Manual specification (no file access needed)
  python initiate_audit.py --name "MyAgent" --platform telegram
  
  # Privacy-first: No environment variable scanning
  python initiate_audit.py --auto
        """
    )
    
    parser.add_argument("--name", help="Agent name/identifier")
    parser.add_argument("--platform", default="openclaw", help="Platform (telegram, discord, n8n, langchain, etc.)")
    parser.add_argument("--version", help="Agent/OpenClaw version")
    parser.add_argument("--auto", action="store_true", help="Auto-detect agent info from files only (no env scanning)")
    parser.add_argument("--yes", "-y", action="store_true", help="⚠️ AUTOMATION ONLY: Skip all prompts (use only in pre-audited/sandboxed environments)")
    parser.add_argument("--dry-run", action="store_true", help="Run tests and show what WOULD be submitted (no API call)")
    parser.add_argument("--system-prompt", dest="system_prompt", default="", help="Optional: your agent's system prompt for deeper analysis (stays local, never sent to API)")
    
    args = parser.parse_args()
    
    # Warning for --yes flag
    if args.yes and not args.dry_run:
        print("\n" + "="*70)
        print("⚠️  AUTOMATION MODE (--yes flag)")
        print("="*70)
        print("This flag bypasses ALL consent prompts and confirmations.")
        print("")
        print("✅ Safe for:")
        print("   • Sandboxed test agents (no real secrets)")
        print("   • CI/CD pipelines (after manual code review)")
        print("   • Agents you've already audited manually")
        print("")
        print("❌ NOT recommended for:")
        print("   • Production agents with real secrets")
        print("   • First-time audits (use manual mode first!)")
        print("   • Agents handling sensitive user data")
        print("")
        print("📋 Code transparency: See audit_client.py line 108+ for")
        print("   submission sanitization (whitelist approach).")
        print("="*70)
        print()
        if not os.environ.get('AGENTSHIELD_YES_ACKNOWLEDGED'):
            print("Set AGENTSHIELD_YES_ACKNOWLEDGED=1 to skip this warning.")
            import time
            time.sleep(3)  # Brief pause for user to read
    
    # Determine mode: auto or manual
    if args.auto:
        print("🔍 Auto-detecting agent information...")
        detected = auto_detect_all(skip_consent=args.yes)
        
        print(f"\n  Detected name: {detected['name'] or 'UNKNOWN'} (confidence: {detected['name_confidence']:.0%})")
        print(f"  Detected platform: {detected['platform']} (confidence: {detected['platform_confidence']:.0%})")
        if detected['version']:
            print(f"  Detected version: {detected['version']}")
        
        # Use detected values
        agent_name = detected['name'] or "UnknownAgent"
        platform = detected['platform']
        version = detected['version']
        
        # Confirm in auto mode if low confidence
        if detected['overall_confidence'] < 0.8 and not args.yes:
            print(f"\n⚠️  Low confidence in auto-detection ({detected['overall_confidence']:.0%})")
            response = input(f"Use detected values? [Y/n] ").strip().lower()
            if response and response not in ('y', 'yes', ''):
                print("Please run with --name and --platform flags instead.")
                sys.exit(0)
        
    else:
        # Manual mode - require name
        if not args.name:
            print("Error: --name is required (or use --auto for auto-detection)")
            print("\nRun with --help for usage information.")
            sys.exit(1)
        
        agent_name = args.name
        platform = args.platform
        version = args.version
    
    print(f"\n🔐 AgentShield Security Audit")
    print(f"   Agent: {agent_name}")
    print(f"   Platform: {platform}")
    if version:
        print(f"   Version: {version}")
    print()
    
    # Step 1: Load or create keys
    keys = load_or_create_keys()
    public_key_short = keys['public_key'][:16] + "..."
    print(f"✓ Identity loaded: {public_key_short}")
    
    # ✅ v1.0.32 FIX: Create client instance (maintains session throughout)
    from audit_client import AgentShieldClient
    client = AgentShieldClient()
    
    # Step 2: Initiate audit (using client)
    print(f"\n📡 Contacting AgentShield API...")
    try:
        session = client.initiate_audit(
            agent_name=agent_name,
            platform=platform,
            public_key=keys['public_key'],
            agent_version=version
        )
    except SystemExit:
        raise
    except Exception as e:
        print(f"✗ Failed to initiate audit: {e}")
        sys.exit(1)
    
    audit_id = session.get('audit_id')
    challenge = session.get('challenge')
    
    print(f"✓ Audit initiated: {audit_id}")
    
    # Step 3: Complete challenge (using client)
    print(f"\n🔑 Authenticating...")
    try:
        # Sign challenge locally
        signature = sign_challenge(keys['private_key'], challenge)
        # Submit via client (maintains session)
        auth_result = client.complete_challenge(audit_id, signature)
        print(f"✓ Authentication successful")
    except Exception as e:
        print(f"✗ Authentication failed: {e}")
        sys.exit(1)
    
    # Step 4: Run security tests
    print(f"\n🧪 Running security tests...")
    test_results = run_security_tests(audit_id, system_prompt=args.system_prompt)
    overall_score = test_results.get('security_score', 0)
    tests_passed = test_results.get('tests_passed', 0)
    tests_total = test_results.get('tests_total', 0)
    print(f"✓ Tests completed: {tests_passed}/{tests_total} passed")
    print(f"   Security Score: {overall_score}/100")
    
    # DRY-RUN MODE: Show what would be submitted, then exit
    if args.dry_run:
        print("\n" + "="*70)
        print("🔍 DRY RUN MODE - NO DATA WILL BE SUBMITTED")
        print("="*70)
        print("\nThis shows exactly what WOULD be sent to the API.")
        print("Use this to verify sanitization before real submission.\n")
        
        # Use same client instance (already created above)
        # Show sanitized summary
        summary = {
            "security_score": int(test_results.get('security_score', 0)),
            "tests_passed": int(test_results.get('tests_passed', 0)),
            "tests_total": int(test_results.get('tests_total', 0)),
            "tier": str(test_results.get('tier', 'UNKNOWN')),
            "critical_failures": int(test_results.get('critical_failures', 0)),
            "high_failures": int(test_results.get('high_failures', 0)),
            "medium_failures": int(test_results.get('medium_failures', 0))
        }
        
        # Show sanitized detailed results (first 5 tests)
        detailed = client._sanitize_test_details(
            test_results.get('test_results', [])
        )
        
        print("📤 WOULD SUBMIT TO API:")
        print("─" * 70)
        print(f"\n1. Summary Scores:")
        print(json.dumps(summary, indent=2))
        
        print(f"\n2. Detailed Results (showing first 5 of {len(detailed)}):")
        for i, test in enumerate(detailed[:5]):
            print(f"   {i+1}. {test}")
        
        if len(detailed) > 5:
            print(f"   ... and {len(detailed)-5} more test results")
        
        print("\n─" * 70)
        print("✅ Dry run complete. No data sent to API.")
        print("\n💡 To submit for real: Remove --dry-run flag")
        print("─" * 70)
        sys.exit(0)
    
    # Step 5: Complete and get certificate
    print(f"\n📜 Requesting certificate...")
    try:
        # ✅ v1.0.32 FIX: Pass client instance (for session + sanitization)
        result = complete_audit(audit_id, test_results, client)
        certificate = result.get('certificate')
        agent_id = result.get('agent_id')
        
        if certificate:
            save_certificate(certificate)
            payload = certificate.get('payload', {})
            tier = payload.get('tier', result.get('tier', 'UNKNOWN'))
            score = payload.get('score', result.get('security_score', 0))
            expires = result.get('expires_at')
            
            print(f"\n{'='*50}")
            print(f"✅ AUDIT COMPLETE")
            print(f"{'='*50}")
            print(f"Security Score: {score}/100")
            print(f"Tier: {tier}")
            print(f"Valid until: {expires}")
            print(f"Agent ID: {agent_id}")
            print(f"{'='*50}")
            print(f"\nCertificate saved to: {CERT_FILE}")
            print(f"Other agents can verify you at: {AGENTSHIELD_API}/api/verify/{agent_id}")
        else:
            print("✗ No certificate received")
            sys.exit(1)
            
    except Exception as e:
        print(f"✗ Failed to complete audit: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
