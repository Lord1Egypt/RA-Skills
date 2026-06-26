#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
WORKSPACE = SKILL_DIR.parent.parent
MEMORY_PATH = WORKSPACE / 'MEMORY.md'
SINGLE_SCRIPT = SKILL_DIR.parent / 'docker-container-rerun' / 'scripts' / 'update_docker_run_container.py'

def list_container_names():
    try:
        out = subprocess.check_output(['docker', 'ps', '-a', '--format', '{{.Names}}'], text=True)
        return [line.strip() for line in out.splitlines() if line.strip()]
    except Exception:
        return []

def parse_memory_safe(memory_text, container_names):
    # 1. 尝试定位章节（允许部分匹配）
    start_pattern = re.compile(r'^##\s+已记住的\s+Docker\s+容器固定重建命令', re.M)
    end_pattern = re.compile(r'^##\s+Nginx\s+Proxy\s+Manager\s+托管', re.M)
    
    m_start = start_pattern.search(memory_text)
    m_end = end_pattern.search(memory_text)
    
    if m_start:
        start_idx = m_start.end()
        if m_end and m_end.start() > start_idx:
            target_text = memory_text[start_idx:m_end.start()]
        else:
            target_text = memory_text[start_idx:]
    else:
        target_text = memory_text

    # 2. 提取所有代码块（更宽松的匹配）
    blocks = re.findall(r'```(?:bash|sh)?\s*\n(.*?)\n\s*```', target_text, re.DOTALL)
    
    matched = []
    missing = []
    
    for name in container_names:
        found_cmd = None
        # 针对该容器名的正则
        name_pattern = re.compile(rf'--name\s+[\'"]?{re.escape(name)}[\'"]?(?:\s|\\|$)', re.I)
        
        for block in reversed(blocks):
            flat = block.replace('\\\n', ' ').replace('\n', ' ')
            if 'docker run' in flat and name_pattern.search(flat):
                # 寻找真正的 docker run 起始行
                lines = block.splitlines()
                cleaned = []
                started = False
                for l in lines:
                    s = l.strip()
                    if not started:
                        if s.startswith('docker run'):
                            cleaned.append(s)
                            started = True
                    else:
                        cleaned.append(s)
                if cleaned:
                    found_cmd = "\n".join(cleaned)
                    break
        
        if found_cmd:
            matched.append({'container_name': name, 'recreate_command': found_cmd})
        else:
            missing.append(name)
            
    return matched, missing

def run_one(container_name: str, recreate_command: str, apply: bool):
    cmd = ['python3', str(SINGLE_SCRIPT), '--container-name', container_name, '--recreate-command', recreate_command]
    if apply: cmd.append('--apply')
    proc = subprocess.run(cmd, text=True, capture_output=True)
    if proc.returncode != 0:
        return {'container_name': container_name, 'ok': False, 'error': (proc.stderr or proc.stdout).strip()}
    stdout = (proc.stdout or '').strip()
    start = stdout.find('{')
    if start == -1: return {'container_name': container_name, 'ok': False, 'error': 'No JSON returned'}
    try:
        data = json.loads(stdout[start:])
        data['ok'] = True
        return data
    except Exception as e:
        return {'container_name': container_name, 'ok': False, 'error': str(e)}

def build_report(results, total_count, matched, missing):
    updated = [r for r in results if r.get('ok') and r.get('needs_update')]
    up_to_date = [r for r in results if r.get('ok') and not r.get('needs_update')]
    failed = [r for r in results if not r.get('ok')]
    
    lines = [
        'Docker 容器批量检查结果（智能版 v3）',
        f'系统总数：{total_count} | 匹配成功：{len(matched)} | 未匹配：{len(missing)}',
        f'更新：{len(updated)} | 最新：{len(up_to_date)} | 失败：{len(failed)}',
        ''
    ]
    if updated:
        lines.append('【已更新】')
        for r in updated: lines.append(f"- {r['container_name']}")
    if failed:
        lines.append('【失败项】')
        for r in failed: lines.append(f"- {r['container_name']}: {r.get('error')}")
    if missing:
        lines.append('【未匹配记忆】')
        lines.append(", ".join(missing))
        
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--memory-path', default=str(MEMORY_PATH))
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()

    memory_text = Path(args.memory_path).read_text(encoding='utf-8')
    all_names = list_container_names()
    matched, missing = parse_memory_safe(memory_text, all_names)

    results = [run_one(m['container_name'], m['recreate_command'], args.apply) for m in matched]
    
    report = build_report(results, len(all_names), matched, missing)
    print(json.dumps({'report_zh': report}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
