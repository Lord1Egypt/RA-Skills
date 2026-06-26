#!/usr/bin/env python3
"""
AgentShield Bundle Verification Script

Verifies that the ClawHub bundle is correctly structured and ready for distribution.
"""

import json
import sys
from pathlib import Path

# Colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def check_file_exists(file_path: Path, description: str) -> bool:
    """Check if a required file exists."""
    if file_path.exists():
        print(f"{GREEN}✅{RESET} {description}: {file_path.name}")
        return True
    else:
        print(f"{RED}❌{RESET} {description}: {file_path.name} NOT FOUND")
        return False

def check_clawhub_json(file_path: Path) -> bool:
    """Validate clawhub.json structure."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Required fields
        required = [
            "name", "version", "description", "author", "license",
            "installation", "privacy", "security"
        ]
        
        missing = [field for field in required if field not in data]
        
        if missing:
            print(f"{RED}❌{RESET} clawhub.json missing fields: {', '.join(missing)}")
            return False
        
        # Check installation method
        if data.get("installation", {}).get("method") != "bundle":
            print(f"{YELLOW}⚠️{RESET}  clawhub.json: installation method should be 'bundle'")
        
        # Check privacy section
        privacy = data.get("privacy", {})
        if "private_keys" not in privacy:
            print(f"{YELLOW}⚠️{RESET}  clawhub.json: missing 'private_keys' in privacy section")
        
        print(f"{GREEN}✅{RESET} clawhub.json: Valid structure")
        print(f"   {BLUE}→{RESET} Name: {data['name']}")
        print(f"   {BLUE}→{RESET} Version: {data['version']}")
        print(f"   {BLUE}→{RESET} Author: {data['author']}")
        print(f"   {BLUE}→{RESET} Method: {data['installation']['method']}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"{RED}❌{RESET} clawhub.json: Invalid JSON - {e}")
        return False
    except Exception as e:
        print(f"{RED}❌{RESET} clawhub.json: Error - {e}")
        return False

def check_python_imports() -> bool:
    """Test that Python modules can be imported."""
    try:
        # Add src to path
        import sys
        src_path = Path(__file__).parent / "src"
        sys.path.insert(0, str(src_path))
        
        # Try importing
        from agentshield_security import (
            InputSanitizer, OutputDLP, ToolSandbox, 
            EchoLeakTester, SecretScanner
        )
        
        print(f"{GREEN}✅{RESET} Python modules: All imports successful")
        return True
        
    except ImportError as e:
        print(f"{RED}❌{RESET} Python modules: Import failed - {e}")
        return False

def main():
    """Run all verification checks."""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}AgentShield Bundle Verification{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    bundle_dir = Path(__file__).parent
    results = []
    
    # 1. Required files
    print(f"\n{YELLOW}[1/5]{RESET} Checking required files...")
    required_files = [
        (bundle_dir / "clawhub.json", "ClawHub manifest"),
        (bundle_dir / "README.md", "README"),
        (bundle_dir / "SKILL.md", "Skill documentation"),
        (bundle_dir / "LICENSE", "License file"),
        (bundle_dir / "setup.py", "Setup script"),
        (bundle_dir / "MANIFEST.in", "Manifest"),
        (bundle_dir / "CHANGELOG.md", "Changelog"),
    ]
    
    results.append(all(check_file_exists(path, desc) for path, desc in required_files))
    
    # 2. Scripts
    print(f"\n{YELLOW}[2/5]{RESET} Checking scripts...")
    scripts = [
        (bundle_dir / "scripts" / "__init__.py", "Scripts package init"),
        (bundle_dir / "scripts" / "initiate_audit.py", "Audit initiator"),
        (bundle_dir / "scripts" / "verify_peer.py", "Peer verifier"),
        (bundle_dir / "scripts" / "show_certificate.py", "Certificate viewer"),
        (bundle_dir / "scripts" / "requirements.txt", "Dependencies"),
    ]
    
    results.append(all(check_file_exists(path, desc) for path, desc in scripts))
    
    # 3. Source modules
    print(f"\n{YELLOW}[3/5]{RESET} Checking source modules...")
    src_modules = [
        (bundle_dir / "src" / "agentshield_security" / "__init__.py", "Security package init"),
        (bundle_dir / "src" / "agentshield_security" / "input_sanitizer.py", "Input sanitizer"),
        (bundle_dir / "src" / "agentshield_security" / "output_dlp.py", "Output DLP"),
        (bundle_dir / "src" / "agentshield_security" / "secret_scanner.py", "Secret scanner"),
    ]
    
    results.append(all(check_file_exists(path, desc) for path, desc in src_modules))
    
    # 4. Validate clawhub.json
    print(f"\n{YELLOW}[4/5]{RESET} Validating clawhub.json...")
    results.append(check_clawhub_json(bundle_dir / "clawhub.json"))
    
    # 5. Test Python imports
    print(f"\n{YELLOW}[5/5]{RESET} Testing Python imports...")
    results.append(check_python_imports())
    
    # Summary
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}Summary{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"{GREEN}✅ ALL CHECKS PASSED ({passed}/{total}){RESET}")
        print(f"\n{GREEN}Bundle is ready for distribution!{RESET}\n")
        return 0
    else:
        print(f"{RED}❌ SOME CHECKS FAILED ({passed}/{total}){RESET}")
        print(f"\n{RED}Please fix the issues above before distributing.{RESET}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
