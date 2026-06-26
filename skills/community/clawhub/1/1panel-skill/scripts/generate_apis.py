#!/usr/bin/env python3
"""
Generate missing API endpoints for 1Panel Skill
"""

import json
import re
import os
from collections import defaultdict

def main():
    # Read API docs
    with open('/home/EaveLuo/.openclaw/workspace-xiaolong/tmp/1panel_api_docs.json') as f:
        docs = json.load(f)
    
    # Read implemented APIs
    skill_dir = '/home/EaveLuo/1panel-skill/src/api'
    implemented = set()
    for filename in os.listdir(skill_dir):
        if filename.endswith('.ts') and filename != 'index.ts':
            with open(os.path.join(skill_dir, filename)) as f:
                content = f.read()
                for match in re.finditer(r'this\.(get|post)\(["\']([^"\']+)["\']', content):
                    method = match.group(1).upper()
                    path = match.group(2)
                    implemented.add(f"{method} {path}")
    
    # Group missing by tag
    missing_by_tag = defaultdict(list)
    for path, methods in docs.get('paths', {}).items():
        for method, details in methods.items():
            key = f"{method.upper()} {path}"
            if key not in implemented:
                tag = details.get('tags', ['Unknown'])[0] if details.get('tags') else 'Unknown'
                summary = details.get('summary', 'No description')
                missing_by_tag[tag].append({
                    'method': method.upper(),
                    'path': path,
                    'summary': summary,
                    'key': key
                })
    
    # Generate report
    print("=== Missing API Endpoints Report ===\n")
    total_missing = sum(len(v) for v in missing_by_tag.values())
    print(f"Total missing: {total_missing}\n")
    
    # Generate TypeScript code for each tag
    for tag in sorted(missing_by_tag.keys()):
        apis = missing_by_tag[tag]
        print(f"\n// ==================== {tag} ({len(apis)} endpoints) ====================")
        for api in sorted(apis, key=lambda x: x['path']):
            path = api['path']
            method = api['method'].lower()
            summary = api['summary']
            
            # Convert path to method name
            method_name = generate_method_name(path, method)
            
            # Generate TypeScript method
            ts_code = generate_ts_method(method_name, method, path, summary)
            print(ts_code)

def generate_method_name(path, method):
    """Generate method name from API path"""
    # Remove /api/v2 prefix
    path = path.replace('/api/v2/', '').replace('/api/v1/', '')
    
    # Split by / and convert to camelCase
    parts = path.split('/')
    parts = [p for p in parts if p and not p.startswith(':')]
    
    if not parts:
        return method
    
    # First part lowercase, rest capitalized
    name = parts[0]
    for part in parts[1:]:
        # Remove special chars
        clean = re.sub(r'[^a-zA-Z0-9]', '', part)
        if clean:
            name += clean.capitalize()
    
    # Add action prefix based on HTTP method
    if method == 'get':
        name = 'get' + name.capitalize()
    elif method == 'post':
        if 'del' in path.lower() or 'delete' in path.lower():
            name = 'delete' + name.capitalize()
        elif 'update' in path.lower():
            name = 'update' + name.capitalize()
        elif 'create' in path.lower() or 'add' in path.lower():
            name = 'create' + name.capitalize()
        else:
            name = name
    
    return name

def generate_ts_method(name, method, path, summary):
    """Generate TypeScript method code"""
    # Extract path parameters
    params = re.findall(r':(\w+)', path)
    
    # Build parameter list
    param_list = []
    for p in params:
        param_list.append(f"{p}: string | number")
    
    # Check if needs body
    needs_body = method == 'post' and not any(x in path.lower() for x in ['del', 'get', 'search'])
    if needs_body:
        param_list.append("data?: any")
    
    param_str = ", ".join(param_list) if param_list else ""
    
    # Build path with template literals
    ts_path = path
    for p in params:
        ts_path = ts_path.replace(f':{p}', f'${{{p}}}')
    
    # Generate method
    code = f"\n  /** {summary} */"
    code += f"\n  async {name}({param_str}): Promise<any> {{"
    
    if method == 'get':
        code += f"\n    return this.get(`{ts_path}`);"
    else:
        if needs_body:
            code += f"\n    return this.post(`{ts_path}`, data);"
        elif params:
            code += f"\n    return this.post(`{ts_path}`, {{ {', '.join(params)} }});"
        else:
            code += f"\n    return this.post(`{ts_path}`, {{}});"
    
    code += "\n  }"
    
    return code

if __name__ == '__main__':
    main()
