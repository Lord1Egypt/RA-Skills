#!/usr/bin/env python3
"""
Generate all missing API endpoints for 1Panel Skill
"""

import json
import re
import os
from collections import defaultdict

def generate_method_name(path, method):
    """Generate camelCase method name from API path"""
    # Remove /api/v2/ prefix
    path = path.replace('/api/v2/', '').replace('/api/v1/', '')
    
    # Split by / and filter
    parts = path.split('/')
    parts = [p for p in parts if p and not p.startswith(':') and not p.startswith('{')]
    
    if not parts:
        return method.lower()
    
    # Build camelCase name
    name = parts[0].lower()
    for part in parts[1:]:
        # Clean special chars
        clean = re.sub(r'[^a-zA-Z0-9]', '', part)
        if clean:
            name += clean.capitalize()
    
    # Add action prefix based on HTTP method and path
    if method == 'GET':
        if 'list' in path.lower() or 'search' in path.lower():
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
    """Extract path parameters like :id or {id}"""
    params = re.findall(r'[:{](\w+)[}]?', path)
    return params

def generate_ts_method(name, method, path, summary):
    """Generate TypeScript method"""
    params = extract_path_params(path)
    
    # Build parameter list
    param_list = []
    for p in params:
        param_list.append(f"{p}: string | number")
    
    # Check if needs body
    needs_body = method == 'POST' and not any(x in path.lower() for x in ['del', 'delete', 'get', 'search', 'list'])
    if needs_body:
        param_list.append("data?: any")
    
    param_str = ", ".join(param_list) if param_list else ""
    
    # Build path with template literals
    ts_path = path
    for p in params:
        ts_path = ts_path.replace(f':{p}', f'${{{p}}}').replace(f'{{{p}}}', f'${{{p}}}')
    
    # Generate method
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

def generate_api_file(tag, apis):
    """Generate complete API file for a tag"""
    lines = []
    lines.append(f'import {{ BaseAPI }} from "./base.js";')
    lines.append("")
    lines.append(f"export class {tag.replace(' ', '')}API extends BaseAPI {{")
    
    for api in sorted(apis, key=lambda x: x['path']):
        name = generate_method_name(api['path'], api['method'])
        method_code = generate_ts_method(name, api['method'], api['path'], api['summary'])
        lines.append("")
        lines.append(method_code)
    
    lines.append("")
    lines.append("}")
    
    return "\n".join(lines)

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
    
    print(f"已实现的端点数: {len(implemented)}")
    
    # Group missing by tag
    missing_by_tag = defaultdict(list)
    for path, methods in docs.get('paths', {}).items():
        for method, details in methods.items():
            key = f"{method.upper()} {path}"
            if key not in implemented:
                tag = details.get('tags', ['Unknown'])[0] if details.get('tags') else 'Unknown'
                # Clean tag name for filename
                tag_clean = tag.replace(' ', '-').replace('/', '-')
                missing_by_tag[tag_clean].append({
                    'method': method.upper(),
                    'path': path,
                    'summary': details.get('summary', 'No description'),
                    'key': key
                })
    
    # Generate files for each tag
    output_dir = '/home/EaveLuo/1panel-skill/src/api'
    total_generated = 0
    
    print(f"\n生成 API 文件...")
    print(f"缺失的模块数: {len(missing_by_tag)}")
    
    for tag, apis in sorted(missing_by_tag.items()):
        if len(apis) == 0:
            continue
        
        # Skip if file already exists (we'll append instead)
        filename = f"{tag.lower()}.ts"
        filepath = os.path.join(output_dir, filename)
        
        print(f"\n【{tag}】{len(apis)} 个端点")
        
        if os.path.exists(filepath):
            print(f"  文件已存在，跳过生成: {filename}")
            continue
        
        # Generate new file
        content = generate_api_file(tag, apis)
        with open(filepath, 'w') as f:
            f.write(content)
        
        print(f"  已生成: {filename}")
        total_generated += len(apis)
    
    print(f"\n总计生成: {total_generated} 个端点")

if __name__ == '__main__':
    main()
