#!/usr/bin/env python3
"""
API Key Auditor — 扫描 workspace/skills 目录下硬编码的 API Key / Token，
并提供集成到 openclaw.json env.vars 的迁移方案。

用法：
    python3 audit.py [--skills-dir PATH] [--openclaw-json PATH] [--fix]

    --skills-dir    skills 根目录，默认 ~/.openclaw/workspace/skills
    --openclaw-json openclaw.json 路径，默认 ~/.openclaw/openclaw.json
    --fix           自动将发现的 key 写入 openclaw.json 并提示需要手动替换的位置
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

# ── 敏感模式匹配规则 ──────────────────────────────────────────────────────────
# 每条规则：(正则, 变量名建议, 描述)
PATTERNS = [
    # OpenAI / DashScope / 通义 style  sk-xxxxx
    (r'(?<![A-Za-z0-9_])(sk-[A-Za-z0-9]{20,})', 'OPENAI_API_KEY', 'OpenAI/DashScope style key (sk-...)'),
    # Bearer token / API key 赋值
    (r'''(?:api[_-]?key|apikey|token|secret|bearer)\s*[=:]\s*["']([A-Za-z0-9\-_\.]{16,})["']''',
     'API_KEY', 'Generic API key/token assignment'),
    # URL 里的 ?key= 参数（排除 localhost）
    (r'https?://(?!localhost)[^\s"\']+[?&]key=([A-Za-z0-9]{16,})',
     'MCP_KEY', 'Key embedded in URL query string'),
    # bce-v3/ALTAK style (百度云)
    (r'(bce-v3/ALTAK[A-Za-z0-9\-_/]{10,})', 'BAIDU_API_KEY', 'Baidu Cloud BCE key'),
    # PRIVATE-TOKEN (GitLab / dingword)
    (r'PRIVATE-TOKEN["\s]*[:=]["\s]*([A-Za-z0-9\-_]{8,})', 'PRIVATE_TOKEN', 'GitLab/DingWord private token'),
    # Authorization: Bearer <token>
    (r'Authorization["\s]*[:=]["\s]*[Bb]earer\s+([A-Za-z0-9\-_\.]{16,})', 'BEARER_TOKEN', 'Bearer token in Authorization header'),
]

# 已知安全的误报（占位符、示例值）
ALLOWLIST = {
    'your_api_key_here', 'your-api-key-here', 'your-api-key', 'YOUR_API_KEY', 'YOUR_TOKEN',
    'xxxxxxxx', 'sk-xxxxxxxxxxxxxxxxxxxx', 'sk-...', '<your-key>', 'example', 'placeholder',
    'REPLACE_ME', 'INSERT_YOUR_KEY', 'your_key', 'your-key', 'api-key-here',
}

# 文件扩展名白名单
SCAN_EXTENSIONS = {'.py', '.sh', '.js', '.ts', '.json', '.yaml', '.yml', '.md', '.env'}
SKIP_DIRS = {'__pycache__', '.git', 'node_modules', '.venv', 'venv', 'dist', 'build'}


def is_allowlisted(value: str) -> bool:
    v = value.strip('"\'').lower()
    return any(a.lower() in v for a in ALLOWLIST) or len(v) < 12


def scan_file(filepath: Path) -> list[dict]:
    findings = []
    try:
        text = filepath.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return findings

    for pattern, suggested_var, desc in PATTERNS:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            value = m.group(1)
            if is_allowlisted(value):
                continue
            line_no = text[:m.start()].count('\n') + 1
            findings.append({
                'file': str(filepath),
                'line': line_no,
                'value_prefix': value[:8] + '...' if len(value) > 8 else value,
                'full_value': value,
                'suggested_var': suggested_var,
                'description': desc,
                'match': m.group(0)[:80],
            })
    return findings


def load_mcporter_keys(mcporter_json: Path) -> set[str]:
    """从 ~/.mcporter/mcporter.json 提取所有 MCP server URL 中的 key，
    这类 key 由 mcporter 统一管理，不需要抽取到 openclaw.json。"""
    keys = set()
    if not mcporter_json.exists():
        return keys
    try:
        data = json.loads(mcporter_json.read_text())
        for cfg in data.get('mcpServers', {}).values():
            url = cfg.get('url') or cfg.get('baseUrl', '')
            for m in re.finditer(r'[?&]key=([A-Za-z0-9]{16,})', url):
                keys.add(m.group(1))
    except Exception:
        pass
    return keys


def scan_skills_dir(skills_dir: Path, mcporter_keys: set[str] = None) -> list[dict]:
    all_findings = []
    mcporter_keys = mcporter_keys or set()
    for root, dirs, files in os.walk(skills_dir):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in files:
            fp = Path(root) / fname
            if fp.suffix in SCAN_EXTENSIONS:
                for f in scan_file(fp):
                    # 跳过 mcporter 管理的 MCP key
                    if f['full_value'] in mcporter_keys:
                        f['mcporter_managed'] = True
                    all_findings.append(f)
    return all_findings


def load_openclaw_json(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text())
    return {}


def get_existing_env_vars(oc: dict) -> dict:
    return oc.get('env', {}).get('vars', {})


def suggest_var_name(finding: dict, existing_vars: dict) -> str:
    """根据文件路径和模式建议一个环境变量名。"""
    file_path = Path(finding['file'])
    skill_name = file_path.parts[file_path.parts.index('skills') + 1] if 'skills' in file_path.parts else 'UNKNOWN'
    prefix = skill_name.upper().replace('-', '_').replace(' ', '_')
    base = finding['suggested_var']
    candidate = f"{prefix}_{base}" if not base.startswith(prefix) else base
    # 如果已存在同值，找到对应 key
    for k, v in existing_vars.items():
        if v == finding['full_value']:
            return k  # 已集成，返回已有名称
    return candidate


def apply_fix(findings: list[dict], oc_path: Path):
    oc = load_openclaw_json(oc_path)
    oc.setdefault('env', {}).setdefault('vars', {})
    existing = oc['env']['vars']

    added = {}
    already = {}

    for f in findings:
        val = f['full_value']
        # 检查是否已存在
        existing_key = next((k for k, v in existing.items() if v == val), None)
        if existing_key:
            already[existing_key] = f
        else:
            var_name = suggest_var_name(f, existing)
            if var_name not in existing:
                existing[var_name] = val
                added[var_name] = f

    oc_path.write_text(json.dumps(oc, indent=2, ensure_ascii=False))
    return added, already


def print_report(findings: list[dict], existing_vars: dict, fix_mode: bool,
                 added: dict = None, already: dict = None):
    if not findings:
        print("✅ 未发现硬编码的 API Key / Token，所有凭证管理规范！")
        return

    print(f"\n{'='*60}")
    print(f"  🔍 API Key 审计报告")
    print(f"{'='*60}")
    print(f"  发现 {len(findings)} 处疑似硬编码凭证\n")

    for i, f in enumerate(findings, 1):
        val = f['full_value']
        existing_key = next((k for k, v in existing_vars.items() if v == val), None)
        is_mcporter = f.get('mcporter_managed', False)

        if is_mcporter:
            status = "🔧 mcporter 管理（无需迁移）"
        elif existing_key:
            status = "✅ 已集成到 openclaw.json"
        else:
            status = "⚠️  未集成"

        print(f"  [{i}] {status}")
        print(f"      文件: {f['file']}")
        print(f"      行号: {f['line']}")
        print(f"      类型: {f['description']}")
        print(f"      值  : {f['value_prefix']}")
        if existing_key:
            print(f"      → 已注册为 ${existing_key}")
        if is_mcporter:
            print(f"      → 由 ~/.mcporter/mcporter.json 统一管理")
        print()

    print(f"{'='*60}")

    if fix_mode and added is not None:
        print("\n  📦 本次迁移结果：")
        if added:
            print(f"\n  新增写入 openclaw.json env.vars ({len(added)} 个)：")
            for var, f in added.items():
                print(f"    ${var}  ←  {Path(f['file']).name}:{f['line']}")
            print("\n  ⚠️  请手动将对应文件中的硬编码值替换为环境变量引用：")
            for var, f in added.items():
                print(f"    {f['file']}:{f['line']}")
                print(f"      将硬编码值替换为 os.environ.get('{var}') 或 ${{var:{var}}}")
        if already:
            print(f"\n  已存在于 openclaw.json，无需重复写入 ({len(already)} 个)：")
            for var, f in already.items():
                print(f"    ${var}  ✓")
    else:
        unintegrated = [f for f in findings
                        if not f.get('mcporter_managed')
                        and not any(v == f['full_value'] for v in existing_vars.values())]
        if unintegrated:
            print(f"\n  💡 建议：运行 --fix 参数自动将以上 {len(unintegrated)} 个未集成的凭证")
            print(f"     写入 openclaw.json env.vars，再手动替换文件中的硬编码值。\n")

    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(description='Scan skills dir for hardcoded API keys/tokens')
    parser.add_argument('--skills-dir', default=str(Path.home() / '.openclaw/workspace/skills'))
    parser.add_argument('--openclaw-json', default=str(Path.home() / '.openclaw/openclaw.json'))
    parser.add_argument('--fix', action='store_true', help='Auto-write found keys to openclaw.json')
    args = parser.parse_args()

    skills_dir = Path(args.skills_dir)
    oc_path = Path(args.openclaw_json)

    if not skills_dir.exists():
        print(f"❌ skills 目录不存在: {skills_dir}", file=sys.stderr)
        sys.exit(1)

    mcporter_json = Path.home() / '.mcporter/mcporter.json'
    mcporter_keys = load_mcporter_keys(mcporter_json)
    if mcporter_keys:
        print(f"ℹ️  已识别 {len(mcporter_keys)} 个 mcporter 管理的 MCP key（将标注为受管理，不建议迁移）")

    print(f"🔍 扫描目录: {skills_dir}")
    findings = scan_skills_dir(skills_dir, mcporter_keys)

    oc = load_openclaw_json(oc_path)
    existing_vars = get_existing_env_vars(oc)

    added, already = {}, {}
    if args.fix and findings:
        added, already = apply_fix(findings, oc_path)
        # 重新加载以反映最新状态
        oc = load_openclaw_json(oc_path)
        existing_vars = get_existing_env_vars(oc)

    print_report(findings, existing_vars, args.fix, added, already)


if __name__ == '__main__':
    main()
