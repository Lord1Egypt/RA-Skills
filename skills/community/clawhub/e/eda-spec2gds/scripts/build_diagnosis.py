#!/usr/bin/env python3
"""
Diagnosis Engine v2 - 自动解析 flow.log 错误并给出建议
"""
from pathlib import Path
import json
import re
import sys


def load_text(path: Path):
    if not path.exists():
        return ''
    return path.read_text(encoding='utf-8', errors='ignore')


def parse_lint_errors(text: str):
    """解析 Lint 错误"""
    errors = []
    for line in text.splitlines():
        if 'Error-' in line or '%Error' in line:
            match = re.search(r'%?Error-(\w+):.*?:(\d+):(\d+):(.+)', line)
            if match:
                errors.append({
                    'type': match.group(1),
                    'line': int(match.group(2)),
                    'col': int(match.group(3)),
                    'msg': match.group(4).strip()
                })
    return errors


def parse_synth_errors(text: str):
    """解析综合错误"""
    errors = []
    for line in text.splitlines():
        if 'ERROR' in line or 'Error:' in line:
            errors.append(line.strip())
    return errors


def parse_openlane_errors(text: str):
    """解析 OpenLane flow 错误"""
    errors = []
    in_error = False
    error_block = []
    
    for line in text.splitlines():
        if 'ERROR' in line or 'Error:' in line:
            in_error = True
            error_block = [line.strip()]
        elif in_error:
            if line.strip() and not line.startswith('['):
                error_block.append(line.strip())
            else:
                if error_block:
                    errors.append(' '.join(error_block))
                in_error = False
                error_block = []
    
    if error_block:
        errors.append(' '.join(error_block))
    
    return errors


def detect_issue(text: str):
    """智能诊断引擎"""
    lower = text.lower()
    
    # 1. 检查 Lint 错误
    lint_errors = parse_lint_errors(text)
    if lint_errors:
        suggestions = []
        error_types = set(e['type'] for e in lint_errors)
        
        if 'BLKANDNBLK' in error_types:
            suggestions.append('混用了阻塞 (=) 和非阻塞 (<=) 赋值。建议：在时序逻辑中统一使用 <= 。')
        if 'BLKSEQ' in error_types:
            suggestions.append('在时序逻辑中使用了阻塞赋值。建议：改用非阻塞赋值 <= 。')
        if 'UNDRIVEN' in error_types:
            suggestions.append('信号未驱动。检查是否所有输出都有赋值。')
        if 'MULTIDRIVEN' in error_types:
            suggestions.append('信号多驱动。检查是否有多个 always 块驱动同一信号。')
        
        return {
            'kind': 'lint_errors',
            'summary': f'发现 {len(lint_errors)} 个 Lint 错误',
            'suggestion': ' '.join(suggestions) if suggestions else '查看具体错误信息并修复 RTL 代码。',
            'details': lint_errors[:5]  # 最多显示 5 个
        }
    
    # 2. 检查 Utilization 溢出
    if 'utilization' in lower and ('exceeds 100%' in lower or 'overflow' in lower):
        return {
            'kind': 'placement_utilization_overflow',
            'summary': 'Placement failed because utilization exceeded 100%.',
            'suggestion': 'Increase DIE_AREA before changing RTL.'
        }
    
    # 3. 检查 Docker TTY 问题
    if 'input device is not a tty' in lower:
        return {
            'kind': 'docker_tty_issue',
            'summary': 'OpenLane docker invocation required no-TTY mode.',
            'suggestion': 'Use --docker-no-tty in non-interactive environments.'
        }
    
    # 4. 检查 Config 路径问题
    if 'does not exist' in lower and 'config' in lower:
        return {
            'kind': 'config_path_issue',
            'summary': 'OpenLane config path could not be resolved.',
            'suggestion': 'Use absolute config paths in script invocation.'
        }
    
    # 5. 检查 Testbench 失败
    if 'tb_fail' in lower or 'assertion failed' in lower:
        return {
            'kind': 'testbench_failure',
            'summary': 'Simulation failed due to testbench assertions.',
            'suggestion': 'Inspect assertion timing and expected cycle alignment.'
        }
    
    # 6. 检查时序违例（要先检查"No violations"避免误判）
    if 'no setup violations found' in lower and 'no hold violations found' in lower:
        pass  # 时序没问题，跳过
    elif 'setup violation' in lower or 'hold violation' in lower:
        return {
            'kind': 'timing_violation',
            'summary': 'Timing violations detected.',
            'suggestion': 'Try relaxing clock constraints or optimizing RTL.'
        }
    
    # 7. 检查 DRC 错误（先检查成功状态）
    if 'drc errors clear' in lower or 'no drc errors' in lower or 'drc passed' in lower or 'magic drc errors clear' in lower:
        pass  # DRC 通过了
    elif 'magic drc' in lower and 'error' in lower:
        match = re.search(r'(\d+)\s*drc\s*error', lower)
        if match:
            count = int(match.group(1))
            if count > 0:
                return {
                    'kind': 'drc_errors',
                    'summary': f'{count} DRC errors found.',
                    'suggestion': 'Review layout and fix spacing/violation issues.'
                }
    
    # 8. 检查 LVS 错误（先检查成功状态）
    if 'lvs errors clear' in lower or 'lvs passed' in lower or 'lvs successful' in lower:
        pass  # LVS 通过了
    elif 'lvs error' in lower and 'clear' not in lower:
        return {
            'kind': 'lvs_errors',
            'summary': 'LVS comparison failed.',
            'suggestion': 'Check schematic vs layout connectivity.'
        }
    
    # 9. 检查综合错误
    synth_errors = parse_synth_errors(text)
    if synth_errors:
        return {
            'kind': 'synthesis_errors',
            'summary': f'发现 {len(synth_errors)} 个综合错误',
            'suggestion': '检查 RTL 语法和约束文件。',
            'details': synth_errors[:5]
        }
    
    # 10. 检查 OpenLane 通用错误
    openlane_errors = parse_openlane_errors(text)
    if openlane_errors:
        return {
            'kind': 'openlane_errors',
            'summary': f'发现 {len(openlane_errors)} 个 OpenLane 错误',
            'suggestion': '查看 flow.log 详细错误信息。',
            'details': openlane_errors[:5]
        }
    
    # 无错误
    return {
        'kind': 'none',
        'summary': 'No known failure signature detected.',
        'suggestion': 'Inspect flow.log, warning.log, and error.log manually.'
    }


def main():
    if len(sys.argv) < 3:
        print('usage: build_diagnosis.py <project-root> <output.json>', file=sys.stderr)
        sys.exit(1)
    
    project = Path(sys.argv[1])
    out = Path(sys.argv[2])
    
    # 收集所有日志
    texts = []
    
    # 最新 run 的 flow.log
    runs_root = project / 'constraints' / 'runs'
    if runs_root.exists():
        run_dirs = sorted([p for p in runs_root.iterdir() if p.is_dir()])
        if run_dirs:
            latest = run_dirs[-1]
            for log_name in ['flow.log', 'warning.log', 'error.log']:
                log_path = latest / log_name
                if log_path.exists():
                    texts.append(f'=== {log_name} ===\n{load_text(log_path)}')
    
    # 合成日志
    full_text = '\n'.join(texts)
    
    # 诊断
    diagnosis = detect_issue(full_text)
    
    # 输出
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(diagnosis, indent=2, ensure_ascii=False), encoding='utf-8')
    print(out)


if __name__ == '__main__':
    main()
