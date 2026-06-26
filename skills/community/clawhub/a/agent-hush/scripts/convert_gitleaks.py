#!/usr/bin/env python3
"""Convert Gitleaks TOML rules to Agent Hush Python format.
Handles Go regex → Python regex translation."""
import re
import sys
import json

def parse_gitleaks_toml(filepath):
    """Parse gitleaks.toml without external dependencies."""
    rules = []
    current_rule = None
    in_multiline = False
    multiline_key = None
    multiline_val = ""
    
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        stripped = line.strip()
        
        # Handle multi-line strings
        if in_multiline:
            if stripped.endswith("'''"):
                multiline_val += stripped[:-3]
                if current_rule is not None:
                    current_rule[multiline_key] = multiline_val
                in_multiline = False
            else:
                multiline_val += line
            continue
        
        if stripped == '[[rules]]':
            if current_rule and 'regex' in current_rule:
                rules.append(current_rule)
            current_rule = {}
            continue
        
        if current_rule is None:
            continue
            
        if stripped.startswith('#') or stripped.startswith('[') or '=' not in stripped:
            continue
            
        key, _, val = stripped.partition('=')
        key = key.strip()
        val = val.strip()
        
        if val.startswith("'''"):
            content = val[3:]
            if content.endswith("'''"):
                current_rule[key] = content[:-3]
            else:
                in_multiline = True
                multiline_key = key
                multiline_val = content + '\n'
        elif val.startswith('"'):
            # Handle escaped quotes inside
            current_rule[key] = val.strip('"')
        elif val.startswith("'"):
            current_rule[key] = val.strip("'")
        else:
            current_rule[key] = val
    
    if current_rule and 'regex' in current_rule:
        rules.append(current_rule)
    
    return rules


def go_regex_to_python(pattern):
    """Convert Go regex to Python-compatible regex."""
    p = pattern
    # POSIX character classes → Python equivalents
    p = p.replace('[[:alnum:]]', '[a-zA-Z0-9]')
    p = p.replace('[[:alpha:]]', '[a-zA-Z]')
    p = p.replace('[[:digit:]]', '[0-9]')
    p = p.replace('[[:lower:]]', '[a-z]')
    p = p.replace('[[:upper:]]', '[A-Z]')
    p = p.replace('[[:space:]]', r'\s')
    p = p.replace('[[:print:]]', r'[\x20-\x7e]')
    p = p.replace('[[:xdigit:]]', '[0-9a-fA-F]')
    # Fix HTML entities that might leak through
    p = p.replace('\u003e', '>')
    p = p.replace('\u003c', '<')
    return p


def test_regex(pattern):
    """Test if a regex compiles in Python."""
    try:
        re.compile(pattern)
        return True
    except re.error:
        return False


def shorten_description(desc):
    """Shorten verbose Gitleaks descriptions."""
    # Remove common verbose prefixes
    prefixes = [
        r'Uncovered a possible ',
        r'Identified a potential ',
        r'Detected a pattern that resembles (?:a |an )',
        r'Discovered a potential ',
        r'Found a ',
        r'Identified (?:a |an )',
        r'Detected (?:a |an )',
    ]
    result = desc
    for prefix in prefixes:
        result = re.sub(f'^{prefix}', '', result, flags=re.IGNORECASE)
    
    # Remove trailing explanations after comma
    if ', ' in result:
        parts = result.split(', ')
        if len(parts[0]) > 15:
            result = parts[0]
    
    # Capitalize first letter
    if result:
        result = result[0].upper() + result[1:]
    
    # Truncate if still too long
    if len(result) > 60:
        result = result[:57] + '...'
    
    return result


def convert(rules):
    """Convert parsed rules to Python code."""
    output_rules = []
    skipped = 0
    
    for rule in rules:
        rule_id = rule.get('id', 'unknown')
        desc = rule.get('description', rule_id)
        regex = rule.get('regex', '')
        
        if not regex:
            skipped += 1
            continue
        
        # Convert Go regex to Python
        py_regex = go_regex_to_python(regex)
        
        # Test compilation
        if not test_regex(py_regex):
            skipped += 1
            print(f"  SKIP (bad regex): {rule_id}", file=sys.stderr)
            continue
        
        name = shorten_description(desc)
        placeholder = f"[REDACTED_{rule_id.upper().replace('-', '_').replace(' ', '_')}]"
        
        output_rules.append({
            'name': name,
            'id': rule_id,
            'regex': py_regex,
            'placeholder': placeholder,
        })
    
    print(f"  Converted: {len(output_rules)}, Skipped: {skipped}", file=sys.stderr)
    
    # Generate Python code
    lines = []
    lines.append("    # ═══════════════════════════════════════════════")
    lines.append("    # Gitleaks Rules (auto-converted)")
    lines.append("    # Source: https://github.com/gitleaks/gitleaks")
    lines.append("    # License: MIT | 222+ community-maintained rules")
    lines.append("    # ═══════════════════════════════════════════════")
    lines.append("")
    
    for r in output_rules:
        name_escaped = r['name'].replace('"', '\\"')
        lines.append(f'    ("{name_escaped}", CRITICAL, HIGH_CONF,')
        lines.append(f"     r'''{r['regex']}''',")
        lines.append(f'     "{r["placeholder"]}"),')
        lines.append("")
    
    return '\n'.join(lines)


if __name__ == '__main__':
    filepath = sys.argv[1] if len(sys.argv) > 1 else '/tmp/gitleaks.toml'
    print(f"Parsing {filepath}...", file=sys.stderr)
    rules = parse_gitleaks_toml(filepath)
    print(f"  Found {len(rules)} rules", file=sys.stderr)
    print(convert(rules))
