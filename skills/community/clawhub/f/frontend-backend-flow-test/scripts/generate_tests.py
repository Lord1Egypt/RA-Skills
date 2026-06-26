#!/usr/bin/env python3
"""
Experimental live helper for Frontend-Backend Flow Test.

This script is intentionally not the primary entrypoint of the skill and is not a
real API regression framework. Use `audit_contracts.py` first for static contract
analysis, then use this helper only for narrow dev/staging follow-up checks when
runtime confirmation is needed.
"""

import json
import argparse
from pathlib import Path
from datetime import datetime

TEST_TEMPLATE = '''#!/usr/bin/env python3
"""
Auto-generated Flow Test: {feature_name}
Generated: {timestamp}
Service: {service_name}
"""

import requests
import json
from datetime import datetime

# Configuration
API_BASE = "{api_base}"
AUTH_METHOD = "{auth_method}"

class {class_name}Test:
    def __init__(self):
        self.token = None
        self.user_id = None
        self.resource_id = None
    
    def login(self):
        """Login and get authentication token"""
        print("🔐 Logging in...")
        
        login_payload = {{
            'email': '{email}',
            'password': '{password}'
        }}

        if "{login_request_encoding}" == "json":
            r = requests.post(
                f"{{API_BASE}}{login_endpoint}",
                json=login_payload,
                timeout=10
            )
        elif "{login_request_encoding}" == "params":
            r = requests.post(
                f"{{API_BASE}}{login_endpoint}",
                params=login_payload,
                timeout=10
            )
        else:
            r = requests.post(
                f"{{API_BASE}}{login_endpoint}",
                data=login_payload,
                timeout=10
            )
        
        if r.status_code == 200:
            data = r.json()
            {token_extraction}
            {user_id_extraction}
            print(f"  ✅ Login successful")
            return True
        else:
            print(f"  ❌ Login failed: {{r.status_code}}")
            return False
    
    def get_auth_headers(self):
        """Get authentication headers"""
        {auth_headers}
    
    def test_create(self):
        """Test CREATE operation"""
        print("\n[CREATE] Creating {feature_name}...")
        
        try:
            data = {create_data}
            {create_user_binding}

            if "{create_request_encoding}" == "json":
                r = requests.{http_create_method}(
                    f"{{API_BASE}}{create_endpoint}",
                    json=data,
                    headers=self.get_auth_headers(),
                    timeout=10
                )
            elif "{create_request_encoding}" == "params":
                r = requests.{http_create_method}(
                    f"{{API_BASE}}{create_endpoint}",
                    params=data,
                    headers=self.get_auth_headers(),
                    timeout=10
                )
            else:
                r = requests.{http_create_method}(
                    f"{{API_BASE}}{create_endpoint}",
                    data=data,
                    headers=self.get_auth_headers(),
                    timeout=10
                )
            
            if r.status_code in [200, 201]:
                result = r.json()
                self.resource_id = {id_extraction}
                print(f"  ✅ CREATE success (ID: {{self.resource_id}})")
                return True
            else:
                print(f"  ❌ CREATE failed: {{r.status_code}}")
                return False
        except Exception as e:
            print(f"  ❌ CREATE error: {{e}}")
            return False
    
    {read_method}
    {update_method}
    
    def test_delete(self):
        """Test DELETE operation (rollback)"""
        if not self.resource_id:
            print("\n[DELETE] No resource to delete")
            return True
        
        print("\n[DELETE] Deleting {feature_name} (rollback)...")
        
        try:
            endpoint = "{delete_endpoint}".format(id=self.resource_id)
            payload = {delete_payload_base}
            {delete_user_binding}
            {delete_resource_id_binding}

            if "{delete_request_encoding}" == "json":
                r = requests.{http_delete_method}(
                    f"{{API_BASE}}{{endpoint}}",
                    json=payload,
                    headers=self.get_auth_headers(),
                    timeout=10
                )
            elif "{delete_request_encoding}" == "params":
                r = requests.{http_delete_method}(
                    f"{{API_BASE}}{{endpoint}}",
                    params=payload,
                    headers=self.get_auth_headers(),
                    timeout=10
                )
            else:
                r = requests.{http_delete_method}(
                    f"{{API_BASE}}{{endpoint}}",
                    data=payload,
                    headers=self.get_auth_headers(),
                    timeout=10
                )
            
            if r.status_code in [200, 204]:
                print(f"  ✅ DELETE success (rollback complete)")
                self.resource_id = None
                return True
            else:
                print(f"  ⚠️  DELETE failed: {{r.status_code}}")
                return False
        except Exception as e:
            print(f"  ❌ DELETE error: {{e}}")
            return False
    
    def run(self):
        """Run full test suite"""
        print("="*70)
        print("🧪 Flow Test: {feature_name}")
        print("="*70)
        print(f"Time: {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}")
        print()
        
        if not self.login():
            return
        
        passed = 0
        total = 0
        
        try:
            # CREATE
            total += 1
            if self.test_create():
                passed += 1
            
            {test_sequence}
            
        finally:
            # Always try to delete (rollback)
            self.test_delete()
        
        print()
        print("="*70)
        print(f"🎉 Test Complete: {{passed}}/{{total}} passed ({{passed*100//total if total > 0 else 0}}%)")
        print("="*70)

if __name__ == '__main__':
    tester = {class_name}Test()
    tester.run()
'''

READ_METHOD_TEMPLATE = '''
    def test_read(self):
        """Test READ operation"""
        print("\n[READ] Reading {feature_name}...")
        
        try:
            {read_code}
            
            if r.status_code == 200:
                result = r.json()
                print(f"  ✅ READ success")
                return True
            else:
                print(f"  ❌ READ failed: {{r.status_code}}")
                return False
        except Exception as e:
            print(f"  ❌ READ error: {{e}}")
            return False
'''

UPDATE_METHOD_TEMPLATE = '''
    def test_update(self):
        """Test UPDATE operation"""
        if not self.resource_id:
            print("\n[UPDATE] No resource to update")
            return False
        
        print("\n[UPDATE] Updating {feature_name}...")
        
        try:
            endpoint = "{update_endpoint}".format(id=self.resource_id)
            data = {update_data}
            {update_user_binding}
            {update_resource_id_binding}

            if "{update_request_encoding}" == "json":
                r = requests.{http_method}(
                    f"{{API_BASE}}{{endpoint}}",
                    json=data,
                    headers=self.get_auth_headers(),
                    timeout=10
                )
            elif "{update_request_encoding}" == "params":
                r = requests.{http_method}(
                    f"{{API_BASE}}{{endpoint}}",
                    params=data,
                    headers=self.get_auth_headers(),
                    timeout=10
                )
            else:
                r = requests.{http_method}(
                    f"{{API_BASE}}{{endpoint}}",
                    data=data,
                    headers=self.get_auth_headers(),
                    timeout=10
                )
            
            if r.status_code in [200, 201]:
                print(f"  ✅ UPDATE success")
                return True
            else:
                print(f"  ❌ UPDATE failed: {{r.status_code}}")
                return False
        except Exception as e:
            print(f"  ❌ UPDATE error: {{e}}")
            return False
'''

def extract_json_path(path):
    """Convert JSON path to Python code"""
    if '.' in path:
        parts = path.split('.')
        code = "data"
        for part in parts:
            code += f".get('{part}')"
        return code
    else:
        return f"data.get('{path}')"

def generate_auth_headers(auth_config):
    """Generate authentication headers code"""
    method = auth_config.get('method', 'header')
    
    if method == 'header':
        token_key = auth_config.get('token_key', 'Authorization')
        token_prefix = auth_config.get('token_prefix', 'Bearer')
        return f'''return {{
            '{token_key}': '{token_prefix} {{self.token}}'
        }}'''
    
    elif method == 'custom':
        headers = auth_config.get('headers', {})
        lines = ["return {"]
        for key, value in headers.items():
            value = value.replace('{token}', '{self.token}')
            value = value.replace('{user_id}', '{self.user_id}')
            lines.append(f"            '{key}': '{value}',")
        lines.append("        }")
        return '\n'.join(lines)
    
    else:
        return "return {}"

def build_user_binding(include_user_id, field_name='userId', target='data'):
    if include_user_id:
        return f"{target}['{field_name}'] = self.user_id"
    return ""


def build_resource_id_binding(include_resource_id, field_name, target='data'):
    if include_resource_id:
        return f"{target}['{field_name}'] = self.resource_id"
    return ""


def generate_test(config, feature_key, feature_config, output_dir, read_only=False):
    """Generate test file for a feature"""
    
    service_name = config['service']['name']
    api_base = config['service']['api_base']
    feature_name = feature_config.get('name', feature_key)
    class_name = ''.join(word.capitalize() for word in feature_key.split('_'))
    
    # Authentication
    auth_config = config.get('auth', {'method': 'header'})
    test_account = config.get('test_account', {})
    
    token_path = test_account.get('token_path', 'token')
    user_id_path = test_account.get('user_id_path', 'user_id')
    login_request_encoding = test_account.get('request_encoding', 'data')

    token_extraction = f"self.token = str({extract_json_path(token_path)})"
    user_id_extraction = f"self.user_id = {extract_json_path(user_id_path)}"
    
    # CREATE
    create_config = feature_config.get('create', {})
    create_endpoint = create_config.get('endpoint', f'/{feature_key}')
    create_method = create_config.get('method', 'POST')
    create_request_encoding = create_config.get('request_encoding', 'data')
    create_include_user_id = create_config.get('include_user_id', False)
    create_user_id_field = create_config.get('user_id_field', 'userId')
    id_field = create_config.get('id_field', 'id')
    test_data = create_config.get('test_data', {})
    
    if not test_data:
        test_data = {
            'content': f'[AutoTest] Test {feature_name}',
            'name': f'Test {feature_name}'
        }
    
    id_extraction = extract_json_path(id_field) if '.' in id_field else f"result.get('{id_field}')"
    
    # READ
    read_method_code = ""
    read_test = ""
    if 'read' in feature_config:
        read_config = feature_config['read']
        read_endpoint = read_config.get('endpoint', f'/{feature_key}')
        
        if 'detail_endpoint' in read_config:
            detail_endpoint = read_config['detail_endpoint']
            read_code = f'''endpoint = "{detail_endpoint}".format(id=self.resource_id)
            r = requests.get(
                f"{{API_BASE}}{{endpoint}}",
                headers=self.get_auth_headers(),
                timeout=10
            )'''
        else:
            read_code = f'''r = requests.get(
                f"{{API_BASE}}{read_endpoint}",
                headers=self.get_auth_headers(),
                timeout=10
            )'''
        
        read_method_code = READ_METHOD_TEMPLATE.format(
            feature_name=feature_name,
            read_code=read_code
        )
        read_test = '''
            # READ
            total += 1
            if self.test_read():
                passed += 1
'''
    
    # UPDATE
    update_method_code = ""
    update_test = ""
    if 'update' in feature_config and not read_only:
        update_config = feature_config['update']
        update_endpoint = update_config.get('endpoint', f'/{feature_key}/{{id}}')
        update_method = update_config.get('method', 'PUT')
        update_request_encoding = update_config.get('request_encoding', 'data')
        update_include_user_id = update_config.get('include_user_id', False)
        update_user_id_field = update_config.get('user_id_field', 'userId')
        update_include_resource_id = update_config.get('include_resource_id', False)
        update_resource_id_field = update_config.get('resource_id_field', f'{feature_key}_id')
        update_data = update_config.get('test_data', test_data.copy())
        if 'content' in update_data:
            update_data['content'] = f'[AutoTest] Updated {feature_name}'

        update_method_code = UPDATE_METHOD_TEMPLATE.format(
            feature_name=feature_name,
            update_endpoint=update_endpoint,
            update_request_encoding=update_request_encoding,
            update_user_binding=build_user_binding(update_include_user_id, update_user_id_field),
            update_resource_id_binding=build_resource_id_binding(update_include_resource_id, update_resource_id_field),
            http_method=update_method.lower(),
            update_data=json.dumps(update_data)
        )
        update_test = '''
            # UPDATE
            total += 1
            if self.test_update():
                passed += 1
'''
    
    # DELETE
    delete_config = feature_config.get('delete', {})
    delete_endpoint = delete_config.get('endpoint', f'/{feature_key}/{{id}}')
    delete_method = delete_config.get('method', 'DELETE')
    delete_request_encoding = delete_config.get('request_encoding', 'data')
    delete_include_user_id = delete_config.get('include_user_id', False)
    delete_user_id_field = delete_config.get('user_id_field', 'userId')
    delete_include_resource_id = delete_config.get('include_resource_id', False)
    delete_resource_id_field = delete_config.get('resource_id_field', f'{feature_key}_id')
    
    test_sequence = read_test + update_test

    if read_only:
        create_method = 'GET'
        create_endpoint = feature_config.get('read', {}).get('detail_endpoint') or feature_config.get('read', {}).get('endpoint', create_endpoint)
        test_sequence = ''
    
    # Generate final code
    code = TEST_TEMPLATE.format(
        feature_name=feature_name,
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        service_name=service_name,
        api_base=api_base,
        auth_method=auth_config.get('method', 'header'),
        class_name=class_name,
        login_endpoint=test_account.get('login_endpoint', '/login'),
        login_request_encoding=login_request_encoding,
        email=test_account.get('email', 'test@example.com'),
        password=test_account.get('password', 'password'),
        token_extraction=token_extraction,
        user_id_extraction=user_id_extraction,
        auth_headers=generate_auth_headers(auth_config),
        http_create_method=create_method.lower(),
        create_endpoint=create_endpoint,
        create_request_encoding=create_request_encoding,
        create_user_binding=build_user_binding(create_include_user_id and not read_only, create_user_id_field),
        create_data=json.dumps(test_data if not read_only else {}),
        id_extraction=id_extraction,
        read_method=read_method_code,
        update_method=update_method_code,
        delete_endpoint=delete_endpoint,
        delete_request_encoding=delete_request_encoding,
        delete_payload_base='{}',
        delete_user_binding=build_user_binding(delete_include_user_id and not read_only, delete_user_id_field, 'payload'),
        delete_resource_id_binding=build_resource_id_binding(delete_include_resource_id and not read_only, delete_resource_id_field, 'payload'),
        http_delete_method=delete_method.lower(),
        test_sequence=test_sequence
    )
    
    # Write file
    output_file = output_dir / f"test_{feature_key}_crud.py"
    output_file.write_text(code)
    output_file.chmod(0o755)
    
    print(f"✅ Generated: {output_file}")
    return output_file

def main():
    parser = argparse.ArgumentParser(description='Generate experimental live helper files from configuration (not a full API regression runner)')
    parser.add_argument('--config', required=True, help='Configuration file path')
    parser.add_argument('--output', default='.', help='Output directory')
    parser.add_argument('--dry-run', action='store_true', help='Generate files only. This flag does not sandbox the generated scripts; it only avoids extra confirmation during generation.')
    parser.add_argument('--read-only', action='store_true', help='Generate read-focused helpers without update/delete write flow')
    parser.add_argument('--allow-writes', action='store_true', help='Acknowledge that generated helpers may perform write requests in dev/staging')
    
    args = parser.parse_args()
    
    if not args.read_only and not args.allow_writes:
        print("❌ Refusing to generate write-capable helpers without --allow-writes")
        print("   Use --read-only for safer follow-up checks, or add --allow-writes only in dev/staging.")
        return

    # Load configuration
    config_path = Path(args.config)
    if not config_path.exists():
        print(f"❌ Config file not found: {config_path}")
        return
    
    with open(config_path) as f:
        config = json.load(f)
    
    # Safety check: environment validation
    api_base = config['service']['api_base']
    environment = config['service'].get('environment', 'unknown')
    
    # Warn on production-like URLs
    if any(prod_pattern in api_base.lower() for prod_pattern in ['production', 'prod.', 'api.myservice.com', 'live']):
        print("="*70)
        print("⚠️  WARNING: Production-like API detected!")
        print(f"   API: {api_base}")
        print(f"   Environment: {environment}")
        print()
        print("   This helper is intended for dev/staging follow-up only.")
        print("   Running tests against production may:")
        print("   - Create real data")
        print("   - Trigger real notifications")
        print("   - Consume quotas/credits")
        print("   - Leave orphaned resources")
        print()
        if not args.dry_run and not args.read_only:
            response = input("   Type 'YES' to continue anyway: ")
            if response != 'YES':
                print("   Aborted.")
                return
        print("="*70)
        print()
    
    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate tests for each feature
    print("="*70)
    print("🔧 Generating Experimental Live Helpers")
    print("="*70)
    print(f"Config: {config_path}")
    print(f"Service: {config['service']['name']}")
    print(f"Features: {len(config['features'])}")
    print()
    
    generated_files = []
    for feature_key, feature_config in config['features'].items():
        test_file = generate_test(config, feature_key, feature_config, output_dir, read_only=args.read_only)
        generated_files.append(test_file)
    
    print()
    print("="*70)
    print(f"🎉 Generated {len(generated_files)} live helper files")
    print("="*70)
    print()
    print("Next steps:")
    for f in generated_files:
        print(f"  python3 {f}")
    print()
    print("Reminder:")
    print("  - These are experimental helper files, not a real regression suite.")
    print("  - Prefer workspace-qa/tests/ for repeatable API verification.")

if __name__ == '__main__':
    main()
