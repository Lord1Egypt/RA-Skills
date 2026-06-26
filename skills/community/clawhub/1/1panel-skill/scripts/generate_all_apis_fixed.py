#!/usr/bin/env python3
"""
Generate all missing API endpoints for 1Panel Skill (Fixed version)
"""

import json
import re
import os
from collections import defaultdict

def clean_class_name(tag):
    """Clean tag name for valid TypeScript class name"""
    # Remove special chars and convert to PascalCase
    name = re.sub(r'[^a-zA-Z0-9]', '', tag)
    return name + "API"

def generate_method_name(path, method):
    """Generate camelCase method name from API path"""
    path = path.replace('/api/v2/', '').replace('/api/v1/', '')
    parts = path.split('/')
    parts = [p for p in parts if p and not p.startswith(':') and not p.startswith('{')]
    
    if not parts:
        return "execute"
    
    name = parts[0].lower()
    for part in parts[1:]:
        clean = re.sub(r'[^a-zA-Z0-9]', '', part)
        if clean:
            name += clean.capitalize()
    
    # Add action prefix
    if method == 'GET':
        if any(x in path.lower() for x in ['list', 'search', 'page']):
            name = 'list' + name.capitalize()
        else:
            name = 'get' + name.capitalize()
    elif method == 'POST':
        if any(x in path.lower() for x in ['del', 'delete', 'remove']):
            name = 'delete' + name.capitalize()
        elif any(x in path.lower() for x in ['update', 'change', 'modify']):
            name = 'update' + name.capitalize()
        elif any(x in path.lower() for x in ['create', 'add', 'new']):
            name = 'create' + name.capitalize()
        elif any(x in path.lower() for x in ['search', 'list', 'page']):
            name = 'list' + name.capitalize()
    
    return name

def extract_path_params(path):
    """Extract path parameters"""
    return re.findall(r'[:{](\w+)[}]?', path)

def generate_ts_method(name, method, path, summary):
    """Generate TypeScript method"""
    params = extract_path_params(path)
    
    param_list = []
    for p in params:
        param_list.append(f"{p}: string | number")
    
    needs_body = method == 'POST' and not any(x in path.lower() for x in ['del', 'delete', 'get', 'search', 'list'])
    if needs_body:
        param_list.append("data?: any")
    
    param_str = ", ".join(param_list) if param_list else ""
    
    ts_path = path
    for p in params:
        ts_path = ts_path.replace(f':{p}', f'${{{p}}}').replace(f'{{{p}}}', f'${{{p}}}')
    
    lines = []
    lines.append(f"  /** {summary} */")
    lines.append(f"  async {name}({param_str}): Promise<any> {{")
    
    if method == 'GET':
        lines.append(f"    return this.get(`{ts_path}`);")
    else:
        if needs_body:
            lines.append(f"    return this.post(`{ts_path}`, data);")
        elif params:
            args = ", ".join([f'{p}' for p in params])
            lines.append(f"    return this.post(`{ts_path}`, {{ {args} }});")
        else:
            lines.append(f"    return this.post(`{ts_path}`, {{}});")
    
    lines.append("  }")
    
    return "\n".join(lines)

def main():
    with open('/home/EaveLuo/.openclaw/workspace-xiaolong/tmp/1panel_api_docs.json') as f:
        docs = json.load(f)
    
    skill_dir = '/home/EaveLuo/1panel-skill/src/api'
    
    # Read existing files to avoid overwriting
    existing_files = set()
    for filename in os.listdir(skill_dir):
        if filename.endswith('.ts') and filename != 'index.ts':
            existing_files.add(filename.replace('.ts', ''))
    
    print(f"Existing API files: {len(existing_files)}")
    
    # Group by tag
    by_tag = defaultdict(list)
    for path, methods in docs.get('paths', {}).items():
        for method, details in methods.items():
            tag = details.get('tags', ['Unknown'])[0] if details.get('tags') else 'Unknown'
            tag_clean = re.sub(r'[^a-zA-Z0-9]', '', tag).lower()
            by_tag[tag_clean].append({
                'method': method.upper(),
                'path': path,
                'summary': details.get('summary', 'No description'),
            })
    
    print(f"Total tags: {len(by_tag)}")
    
    # Generate missing files
    generated = 0
    for tag, apis in sorted(by_tag.items()):
        if tag in existing_files:
            print(f"Skipping existing: {tag}")
            continue
        
        if len(apis) == 0:
            continue
        
        class_name = clean_class_name(tag)
        filename = f"{tag}.ts"
        filepath = os.path.join(skill_dir, filename)
        
        lines = []
        lines.append('import { BaseAPI } from "./base.js";')
        lines.append("")
        lines.append(f"export class {class_name} extends BaseAPI {{")
        
        for api in sorted(apis, key=lambda x: x['path']):
            name = generate_method_name(api['path'], api['method'])
            method_code = generate_ts_method(name, api['method'], api['path'], api['summary'])
            lines.append("")
            lines.append(method_code)
        
        lines.append("")
        lines.append("}")
        
        with open(filepath, 'w') as f:
            f.write("\n".join(lines))
        
        print(f"Generated: {filename} ({len(apis)} endpoints)")
        generated += len(apis)
    
    print(f"\nTotal generated: {generated} endpoints")

if __name__ == '__main__':
    main()
