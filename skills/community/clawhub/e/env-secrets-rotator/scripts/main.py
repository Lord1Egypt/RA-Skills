#!/usr/bin/env python3
import argparse
import json
import os
import sys
import re
import secrets
import base64
import uuid
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

class EnvFileParser:
    """Parse and manipulate .env files."""
    
    @staticmethod
    def parse_file(filepath: str) -> Tuple[Dict[str, str], List[str]]:
        """Parse .env file, return dict of key-value pairs and original lines."""
        key_values = {}
        lines = []
        
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    lines.append(line.rstrip('\n'))
                    # Remove leading/trailing whitespace
                    line = line.strip()
                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue
                    # Parse KEY=VALUE
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        # Remove quotes if present
                        if (value.startswith('"') and value.endswith('"')) or \
                           (value.startswith("'") and value.endswith("'")):
                            value = value[1:-1]
                        key_values[key] = value
        except Exception as e:
            raise ValueError(f"Error parsing .env file: {e}")
        
        return key_values, lines
    
    @staticmethod
    def write_file(filepath: str, key_values: Dict[str, str], original_lines: List[str]) -> None:
        """Write .env file with updated values while preserving comments and formatting."""
        # Create a mapping for replacement
        updated_lines = []
        for line in original_lines:
            # Check if this line contains a key we need to update
            updated = False
            for key, new_value in key_values.items():
                # Simple pattern matching: key=value (with optional spaces)
                pattern = rf'^{re.escape(key)}\s*=\s*.*'
                if re.match(pattern, line):
                    # Preserve any comment after the value
                    if '#' in line:
                        value_part, comment = line.split('#', 1)
                        # Extract just the assignment part
                        if '=' in value_part:
                            key_part, old_value = value_part.split('=', 1)
                            new_line = f"{key}={new_value} #{comment}"
                        else:
                            new_line = f"{key}={new_value} #{comment}"
                    else:
                        new_line = f"{key}={new_value}"
                    updated_lines.append(new_line)
                    updated = True
                    break
            
            if not updated:
                updated_lines.append(line)
        
        # Write back
        with open(filepath, 'w') as f:
            f.write('\n'.join(updated_lines))
    
    @staticmethod
    def validate_file(filepath: str, strict: bool = False) -> Dict[str, Any]:
        """Validate .env file format and content."""
        try:
            key_values, lines = EnvFileParser.parse_file(filepath)
            issues = []
            
            # Check for empty values in strict mode
            if strict:
                for key, value in key_values.items():
                    if not value:
                        issues.append(f"Key '{key}' has empty value")
            
            # Check for duplicate keys (simple check)
            # Note: our parser overwrites duplicates, but we can check lines
            seen_keys = set()
            for line in lines:
                if '=' in line and not line.strip().startswith('#'):
                    key = line.split('=', 1)[0].strip()
                    if key in seen_keys:
                        issues.append(f"Duplicate key: {key}")
                    seen_keys.add(key)
            
            return {
                "valid": len(issues) == 0,
                "keys": list(key_values.keys()),
                "total_keys": len(key_values),
                "issues": issues
            }
        except Exception as e:
            return {
                "valid": False,
                "error": str(e),
                "keys": [],
                "total_keys": 0,
                "issues": [f"Parse error: {e}"]
            }

class SecretGenerator:
    """Generate secure random secrets."""
    
    @staticmethod
    def generate_secret(algorithm: str = "hex", length: int = 32) -> str:
        """Generate a cryptographically secure random secret."""
        if algorithm == "hex":
            # Hex string of specified length (bytes = length/2)
            byte_length = (length + 1) // 2
            random_bytes = secrets.token_bytes(byte_length)
            secret = random_bytes.hex()
            # Truncate or pad to exact length
            secret = secret[:length]
            return secret
            
        elif algorithm == "base64":
            # Base64 string
            byte_length = (length * 3 + 3) // 4  # Approximate
            random_bytes = secrets.token_bytes(byte_length)
            secret = base64.b64encode(random_bytes).decode('ascii')
            # Remove padding and truncate
            secret = secret.replace('=', '')[:length]
            return secret
            
        elif algorithm == "uuid":
            # UUID v4
            return str(uuid.uuid4())
            
        elif algorithm == "alphanumeric":
            # Alphanumeric string
            alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            return ''.join(secrets.choice(alphabet) for _ in range(length))
            
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
    
    @staticmethod
    def generate_multiple(keys: List[str], algorithm: str = "hex", length: int = 32) -> Dict[str, str]:
        """Generate secrets for multiple keys."""
        return {key: SecretGenerator.generate_secret(algorithm, length) for key in keys}

class SecretsRotator:
    def __init__(self):
        self.history_file = Path.home() / ".env-rotation-history.json"
    
    def rotate(self, filepath: str, keys: List[str], algorithm: str = "hex", 
               length: int = 32, backup: bool = True, dry_run: bool = False,
               output_file: Optional[str] = None) -> Dict[str, Any]:
        """Rotate secrets in .env file."""
        try:
            # Validate file exists
            if not os.path.exists(filepath):
                return {"status": "error", "message": f"File not found: {filepath}"}
            
            # Parse current file
            current_values, original_lines = EnvFileParser.parse_file(filepath)
            
            # Determine which keys to rotate
            if keys == ["*"]:
                keys_to_rotate = list(current_values.keys())
            else:
                keys_to_rotate = [k for k in keys if k in current_values]
                missing_keys = [k for k in keys if k not in current_values]
                if missing_keys:
                    return {
                        "status": "error",
                        "message": f"Keys not found in file: {missing_keys}",
                        "found_keys": keys_to_rotate
                    }
            
            if not keys_to_rotate:
                return {"status": "error", "message": "No valid keys to rotate"}
            
            # Generate new secrets
            new_values = SecretGenerator.generate_multiple(keys_to_rotate, algorithm, length)
            
            # Create backup if requested
            backup_path = None
            if backup and not dry_run:
                timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
                backup_path = f"{filepath}.backup.{timestamp}"
                shutil.copy2(filepath, backup_path)
            
            # Update file if not dry run
            target_file = output_file if output_file else filepath
            if not dry_run:
                # Create updated key-values dict
                updated_values = current_values.copy()
                updated_values.update(new_values)
                EnvFileParser.write_file(target_file, new_values, original_lines)
            
            # Generate Vault commands
            vault_commands = self._generate_vault_commands(keys_to_rotate, new_values)
            
            # Record history
            if not dry_run:
                self._record_history(filepath, keys_to_rotate, new_values)
            
            result = {
                "status": "success",
                "file": filepath,
                "rotated_keys": keys_to_rotate,
                "new_values": new_values,
                "backup": backup_path,
                "vault_commands": vault_commands,
                "dry_run": dry_run,
                "target_file": target_file if output_file else filepath
            }
            
            if dry_run:
                result["message"] = "Dry run completed - no changes made"
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Rotation failed: {str(e)}"}
    
    def _generate_vault_commands(self, keys: List[str], values: Dict[str, str], 
                                path: str = "secret/data/myapp", engine: str = "kv",
                                method: str = "patch") -> List[str]:
        """Generate HashiCorp Vault CLI commands."""
        commands = []
        base_cmd = f"vault kv {method} {engine}/{path}"
        
        for key in keys:
            value = values.get(key)
            if value:
                # Escape value if needed
                if ' ' in value or '"' in value:
                    value_escaped = f'"{value}"'
                else:
                    value_escaped = value
                commands.append(f"{base_cmd} {key}={value_escaped}")
        
        return commands
    
    def _record_history(self, filepath: str, keys: List[str], new_values: Dict[str, str]):
        """Record rotation history (optional)."""
        try:
            history = []
            if self.history_file.exists():
                with open(self.history_file) as f:
                    history = json.load(f)
            
            entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "file": filepath,
                "keys": keys,
                "new_values": new_values
            }
            
            history.append(entry)
            # Keep only last 100 entries
            if len(history) > 100:
                history = history[-100:]
            
            with open(self.history_file, 'w') as f:
                json.dump(history, f, indent=2)
                
        except Exception:
            # History recording is optional, don't fail on error
            pass
    
    def get_history(self, filepath: Optional[str] = None, key: Optional[str] = None) -> Dict[str, Any]:
        """Get rotation history."""
        try:
            if not self.history_file.exists():
                return {"status": "success", "history": [], "count": 0}
            
            with open(self.history_file) as f:
                history = json.load(f)
            
            # Filter by file and/or key
            filtered = []
            for entry in history:
                if filepath and entry.get("file") != filepath:
                    continue
                if key and key not in entry.get("keys", []):
                    continue
                filtered.append(entry)
            
            return {
                "status": "success",
                "history": filtered,
                "count": len(filtered),
                "total": len(history)
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Error reading history: {str(e)}"}
    
    def generate_vault_commands(self, keys: List[str], path: str = "secret/data/myapp",
                               engine: str = "kv", method: str = "patch") -> Dict[str, Any]:
        """Generate Vault commands for keys (without rotating)."""
        try:
            # Generate dummy values for command generation
            dummy_values = {key: f"NEW_{key.upper()}_VALUE" for key in keys}
            commands = self._generate_vault_commands(keys, dummy_values, path, engine, method)
            
            return {
                "status": "success",
                "keys": keys,
                "path": path,
                "engine": engine,
                "method": method,
                "commands": commands,
                "note": "Replace dummy values with actual secrets"
            }
        except Exception as e:
            return {"status": "error", "message": f"Error generating commands: {str(e)}"}

def run_rotate(args):
    """Handle rotate command."""
    rotator = SecretsRotator()
    
    # Parse keys
    if args.keys == "*":
        keys = ["*"]
    else:
        keys = [k.strip() for k in args.keys.split(",")]
    
    result = rotator.rotate(
        filepath=args.file,
        keys=keys,
        algorithm=args.algorithm,
        length=args.length,
        backup=args.backup,
        dry_run=args.dry_run,
        output_file=args.output
    )
    
    return result

def run_vault(args):
    """Handle vault command."""
    rotator = SecretsRotator()
    
    # Parse keys
    keys = [k.strip() for k in args.keys.split(",")]
    
    result = rotator.generate_vault_commands(
        keys=keys,
        path=args.path,
        engine=args.engine,
        method=args.method
    )
    
    return result

def run_validate(args):
    """Handle validate command."""
    result = EnvFileParser.validate_file(args.file, args.strict)
    result["status"] = "success" if result["valid"] else "error"
    return result

def run_history(args):
    """Handle history command."""
    rotator = SecretsRotator()
    result = rotator.get_history(filepath=args.file, key=args.key)
    return result

def main():
    parser = argparse.ArgumentParser(description='Environment Secrets Rotator')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Rotate command
    rotate_parser = subparsers.add_parser('rotate', help='Rotate secrets in .env file')
    rotate_parser.add_argument('--file', required=True, help='Path to .env file')
    rotate_parser.add_argument('--keys', default='*', help='Comma-separated keys or "*" for all')
    rotate_parser.add_argument('--algorithm', default='hex', 
                              choices=['hex', 'base64', 'uuid', 'alphanumeric'],
                              help='Random generation algorithm')
    rotate_parser.add_argument('--length', type=int, default=32, help='Length of generated secret')
    rotate_parser.add_argument('--backup', type=bool, default=True, help='Create backup')
    rotate_parser.add_argument('--dry-run', action='store_true', help='Preview changes')
    rotate_parser.add_argument('--output', help='Write to new file instead of modifying')
    
    # Vault command
    vault_parser = subparsers.add_parser('vault', help='Generate Vault commands')
    vault_parser.add_argument('--keys', required=True, help='Comma-separated keys')
    vault_parser.add_argument('--path', default='secret/data/myapp', help='Vault secret path')
    vault_parser.add_argument('--engine', default='kv', help='Vault secrets engine')
    vault_parser.add_argument('--method', default='patch', choices=['patch', 'put'],
                             help='Vault method')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate .env file')
    validate_parser.add_argument('--file', required=True, help='Path to .env file')
    validate_parser.add_argument('--strict', action='store_true', help='Require non-empty values')
    
    # History command
    history_parser = subparsers.add_parser('history', help='Show rotation history')
    history_parser.add_argument('--file', help='Filter by file')
    history_parser.add_argument('--key', help='Filter by key')
    
    # Help command
    subparsers.add_parser('help', help='Show help')
    
    args = parser.parse_args()
    
    if args.command == 'rotate':
        result = run_rotate(args)
    elif args.command == 'vault':
        result = run_vault(args)
    elif args.command == 'validate':
        result = run_validate(args)
    elif args.command == 'history':
        result = run_history(args)
    elif args.command == 'help' or args.command is None:
        parser.print_help()
        return
    else:
        result = {"status": "error", "message": f"Unknown command: {args.command}"}
    
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()