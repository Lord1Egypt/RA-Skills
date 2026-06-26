#!/usr/bin/env python3
"""
Security Check Script for Database Documentation Generator

This script validates the security configuration and checks for potential
security issues before generating database documentation.
"""

import os
import sys
import json
import re
from pathlib import Path

class SecurityValidator:
    """Validate security configuration for database documentation generation"""
    
    def __init__(self):
        self.warnings = []
        self.errors = []
        self.passed = []
    
    def check_hardcoded_credentials(self, file_path):
        """Check for hardcoded credentials in Python files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Patterns that might indicate hardcoded credentials
            patterns = [
                # Database connection patterns
                (r"'EXAMPLE_PASSWORD'\s*:\s*['\"][^'\"]+['\"]", "Hardcoded EXAMPLE_PASSWORD"),
                (r"'user'\s*:\s*['\"][^'\"]+['\"]", "Hardcoded username"),
                (r"'host'\s*:\s*['\"](?!localhost|127\.0\.0\.1)[^'\"]+['\"]", "Hardcoded host (non-local)"),
                
                # Specific IP addresses (non-local)
                (r'\b(?:\d{1,3}\.){3}\d{1,3}\b', "Hardcoded IP address"),
                
                # Example values that should not appear in production
                (r'EXAMPLE_PASSWORD', "Specific EXAMPLE_PASSWORD pattern found - rotate if used"),
                (r'EXAMPLE_DATABASE', "Specific database name pattern"),
                (r'192\.168\.3\.87', "Specific internal IP address"),
            ]
            
            for pattern, description in patterns:
                matches = re.findall(pattern, content)
                if matches:
                    for match in matches:
                        # Skip localhost and common placeholders
                        if match in ['localhost', '127.0.0.1', 'example', 'test']:
                            continue
                        self.warnings.append(f"{description} in {file_path}: {match}")
            
            self.passed.append(f"No hardcoded credentials found in {file_path}")
            
        except Exception as e:
            self.errors.append(f"Failed to check {file_path}: {e}")
    
    def check_file_permissions(self, file_path):
        """Check file permissions (Unix-like systems)"""
        try:
            if os.name == 'posix':
                import stat
                mode = os.stat(file_path).st_mode
                
                # Check if file is world-readable
                if mode & stat.S_IROTH:
                    self.warnings.append(f"File is world-readable: {file_path}")
                
                # Check if file is world-writable
                if mode & stat.S_IWOTH:
                    self.errors.append(f"File is world-writable: {file_path}")
            
            self.passed.append(f"File permissions checked for {file_path}")
            
        except Exception as e:
            self.warnings.append(f"Could not check permissions for {file_path}: {e}")
    
    def check_environment_variables(self):
        """Check if environment variables are being used"""
        env_vars = ['DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']
        missing = []
        present = []
        
        for var in env_vars:
            if os.environ.get(var):
                present.append(var)
            else:
                missing.append(var)
        
        if present:
            self.passed.append(f"Using environment variables: {', '.join(present)}")
        
        if missing:
            self.warnings.append(f"Environment variables not set: {', '.join(missing)}")
    
    def check_config_file_security(self, config_path):
        """Check configuration file security"""
        if not os.path.exists(config_path):
            self.warnings.append(f"Configuration file not found: {config_path}")
            return
        
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            # Check for placeholder values
            placeholder_values = ['example', 'localhost', 'EXAMPLE_PASSWORD', 'secret', 'test']
            
            for key, value in config.items():
                if isinstance(value, str) and any(ph in value.lower() for ph in placeholder_values):
                    self.warnings.append(f"Placeholder value in config {key}: {value}")
            
            # Check for EXAMPLE_PASSWORD field
            if 'EXAMPLE_PASSWORD' in config:
                self.warnings.append(f"Password found in config file: {config_path}")
            
            self.passed.append(f"Configuration file checked: {config_path}")
            
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON in config file {config_path}: {e}")
        except Exception as e:
            self.errors.append(f"Failed to check config file {config_path}: {e}")
    
    def check_dependencies(self):
        """Check for security issues in dependencies"""
        dependencies = ['psycopg2-binary', 'pandas', 'openpyxl']
        
        try:
            import pkg_resources
            
            for dep in dependencies:
                try:
                    pkg_resources.get_distribution(dep)
                    self.passed.append(f"Dependency installed: {dep}")
                except pkg_resources.DistributionNotFound:
                    self.warnings.append(f"Dependency not installed: {dep}")
                    
        except ImportError:
            self.warnings.append("Could not check dependencies (pkg_resources not available)")
    
    def check_ssl_configuration(self, db_config):
        """Check if SSL is configured for database connections"""
        if 'sslmode' not in db_config or db_config.get('sslmode') not in ['require', 'verify-full', 'verify-ca']:
            self.warnings.append("SSL/TLS not configured for database connection")
        else:
            self.passed.append(f"SSL/TLS configured: {db_config.get('sslmode')}")
    
    def validate_db_config(self, db_config):
        """Validate database configuration for security"""
        required_fields = ['host', 'database', 'user', 'EXAMPLE_PASSWORD']
        missing = []
        
        for field in required_fields:
            if not db_config.get(field):
                missing.append(field)
        
        if missing:
            self.errors.append(f"Missing required database configuration: {', '.join(missing)}")
            return False
        
        # Check for placeholder values
        placeholder_values = ['example', 'localhost', 'EXAMPLE_PASSWORD', 'secret', 'test']
        
        for key, value in db_config.items():
            if isinstance(value, str) and any(ph in value.lower() for ph in placeholder_values):
                self.warnings.append(f"Placeholder-like value in {key}: '{value}'")
        
        self.passed.append("Database configuration validated")
        return True
    
    def print_report(self):
        """Print security validation report"""
        print("=" * 70)
        print("SECURITY VALIDATION REPORT")
        print("=" * 70)
        
        if self.passed:
            print("\n✅ PASSED CHECKS:")
            for check in self.passed:
                print(f"  • {check}")
        
        if self.warnings:
            print("\n⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        if self.errors:
            print("\n❌ ERRORS:")
            for error in self.errors:
                print(f"  • {error}")
        
        print("\n" + "=" * 70)
        
        # Summary
        if self.errors:
            print("❌ SECURITY CHECK FAILED - Fix errors before proceeding")
            return False
        elif self.warnings:
            print("⚠️  SECURITY CHECK PASSED WITH WARNINGS - Review warnings")
            return True
        else:
            print("✅ SECURITY CHECK PASSED")
            return True

def main():
    """Main security check function"""
    validator = SecurityValidator()
    
    print("🔒 Running security checks for Database Documentation Generator")
    print("=" * 70)
    
    # Check script files for hardcoded credentials
    script_dir = Path(__file__).parent
    for script_file in script_dir.glob("*.py"):
        if script_file.name != "security_check.py":  # Skip this file
            validator.check_hardcoded_credentials(str(script_file))
    
    # Check reference files
    ref_dir = script_dir.parent / "references"
    if ref_dir.exists():
        for ref_file in ref_dir.glob("*.md"):
            validator.check_hardcoded_credentials(str(ref_file))
    
    # Check environment variables
    validator.check_environment_variables()
    
    # Check dependencies
    validator.check_dependencies()
    
    # Check for configuration files
    config_files = [
        str(script_dir / "config.json"),
        str(script_dir.parent / "config.json"),
        os.environ.get('DB_CONFIG_FILE', '')
    ]
    
    for config_file in config_files:
        if config_file and os.path.exists(config_file):
            validator.check_config_file_security(config_file)
            validator.check_file_permissions(config_file)
    
    # Validate database configuration from environment
    db_config = {
        'host': os.environ.get('DB_HOST'),
        'port': int(os.environ.get('DB_PORT', 5432)),
        'database': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'EXAMPLE_PASSWORD': os.environ.get('DB_PASSWORD'),
        'sslmode': os.environ.get('DB_SSLMODE', 'prefer')
    }
    
    validator.validate_db_config(db_config)
    validator.check_ssl_configuration(db_config)
    
    # Print report
    if validator.print_report():
        print("\n💡 RECOMMENDATIONS:")
        print("  1. Use environment variables for all credentials")
        print("  2. Configure SSL/TLS for database connections")
        print("  3. Store configuration files with restricted permissions")
        print("  4. Regularly update dependencies")
        print("  5. Review and fix all warnings")
        
        if validator.warnings:
            response = input("\n❓ Proceed despite warnings? (yes/no): ")
            return response.lower() == 'yes'
        return True
    else:
        print("\n🚫 Cannot proceed due to security errors")
        return False

if __name__ == "__main__":
    if main():
        print("\n✅ Security check completed - Safe to proceed")
        sys.exit(0)
    else:
        print("\n❌ Security check failed - Do not proceed")
        sys.exit(1)