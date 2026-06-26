#!/usr/bin/env python3
"""Summarize remote GPU, CPU, memory, and disk utilization."""

from __future__ import annotations

import json
import sys
from typing import Any, Dict, List

from common import (
    ConfigArgumentParser,
    SkillError,
    build_guard_block,
    load_config,
    print_error,
    print_json,
    run_remote_script,
    validate_required_config,
)


def build_resource_script(config: Dict[str, Any]) -> str:
    return f"""
{build_guard_block(config)}
echo '__GPU_START__'
if command -v nvidia-smi >/dev/null 2>&1; then
  nvidia-smi --query-gpu=index,name,utilization.gpu,memory.used,memory.total,temperature.gpu --format=csv,noheader,nounits 2>/dev/null || true
fi
echo '__GPU_END__'
echo '__CPU_START__'
python3 - <<'PY'
import json
import os
with open('/proc/loadavg', 'r', encoding='utf-8') as handle:
    load = handle.read().split()[:3]
print(json.dumps({{
    'loadavg': [float(v) for v in load],
    'cpu_count': os.cpu_count() or 1,
}}))
PY
echo '__CPU_END__'
echo '__MEM_START__'
python3 - <<'PY'
import json

meminfo = {{}}
with open('/proc/meminfo', 'r', encoding='utf-8') as handle:
    for line in handle:
        key, value = line.split(':', 1)
        meminfo[key] = int(value.strip().split()[0])

total_kb = meminfo.get('MemTotal', 0)
available_kb = meminfo.get('MemAvailable', meminfo.get('MemFree', 0))
free_kb = meminfo.get('MemFree', 0)
buffers_kb = meminfo.get('Buffers', 0)
cached_kb = meminfo.get('Cached', 0)
shared_kb = meminfo.get('Shmem', 0)
used_kb = max(total_kb - available_kb, 0)

print(json.dumps({{
    'total_mb': round(total_kb / 1024, 2),
    'used_mb': round(used_kb / 1024, 2),
    'free_mb': round(free_kb / 1024, 2),
    'shared_mb': round(shared_kb / 1024, 2),
    'buff_cache_mb': round((buffers_kb + cached_kb) / 1024, 2),
    'available_mb': round(available_kb / 1024, 2),
}}))
PY
echo '__MEM_END__'
echo '__DISK_START__'
python3 - <<'PY'
import json
import os

project_path = os.environ['PROJECT_PATH']
stats = os.statvfs(project_path)
total = stats.f_blocks * stats.f_frsize
available = stats.f_bavail * stats.f_frsize
used = max(total - available, 0)
used_pct = round((used / total) * 100, 2) if total else 0.0

print(json.dumps({{
    'filesystem': project_path,
    'size_mb': round(total / 1024 / 1024, 2),
    'used_mb': round(used / 1024 / 1024, 2),
    'available_mb': round(available / 1024 / 1024, 2),
    'used_pct': used_pct,
    'mount': project_path,
}}))
PY
echo '__DISK_END__'
""".strip()


def split_sections(stdout: str) -> Dict[str, str]:
    sections: Dict[str, List[str]] = {"gpu": [], "cpu": [], "mem": [], "disk": []}
    active = None
    markers = {
        "__GPU_START__": "gpu",
        "__GPU_END__": None,
        "__CPU_START__": "cpu",
        "__CPU_END__": None,
        "__MEM_START__": "mem",
        "__MEM_END__": None,
        "__DISK_START__": "disk",
        "__DISK_END__": None,
    }
    for line in stdout.splitlines():
        if line in markers:
            active = markers[line]
            continue
        if active:
            sections[active].append(line)
    return {key: "\n".join(value).strip() for key, value in sections.items()}


def parse_gpu(section: str) -> List[Dict[str, Any]]:
    rows = []
    for line in section.splitlines():
        parts = [part.strip() for part in line.split(",")]
        if len(parts) != 6 or not parts[0].isdigit():
            continue
        index, name, util, mem_used, mem_total, temperature = parts
        rows.append(
            {
                "index": int(index),
                "name": name,
                "utilization_gpu_pct": float(util or 0),
                "memory_used_mb": float(mem_used or 0),
                "memory_total_mb": float(mem_total or 0),
                "temperature_c": float(temperature or 0),
            }
        )
    return rows


def assess_bottlenecks(config: Dict[str, Any], gpus: List[Dict[str, Any]], cpu: Dict[str, Any], mem: Dict[str, Any], disk: Dict[str, Any]) -> List[str]:
    notes: List[str] = []
    low_gpu_util_pct = float(config.get("resource_low_gpu_util_pct", 30))
    gpu_mem_warn_pct = float(config.get("resource_warn_gpu_memory_pct", 90))
    mem_warn_pct = float(config.get("resource_warn_memory_pct", 90))
    disk_warn_pct = float(config.get("resource_warn_disk_pct", 85))

    for gpu in gpus:
        mem_pct = 100.0 * gpu["memory_used_mb"] / max(gpu["memory_total_mb"], 1.0)
        if gpu["utilization_gpu_pct"] < low_gpu_util_pct and gpu["memory_used_mb"] > 500:
            notes.append(f"GPU {gpu['index']} 利用率只有 {gpu['utilization_gpu_pct']:.0f}%，可能存在数据加载或 CPU 瓶颈。")
        if mem_pct >= gpu_mem_warn_pct:
            notes.append(f"GPU {gpu['index']} 显存占用 {mem_pct:.1f}%，已接近上限。")

    loadavg = cpu.get("loadavg", [0.0, 0.0, 0.0])
    cpu_count = max(int(cpu.get("cpu_count", 1)), 1)
    if loadavg and loadavg[0] / cpu_count >= 0.9:
        notes.append(f"1 分钟平均负载为 {loadavg[0]:.2f}，接近或超过 CPU 核数 {cpu_count}，CPU 可能成为瓶颈。")

    total_mem = max(float(mem.get("total_mb", 1)), 1.0)
    used_mem_pct = 100.0 * float(mem.get("used_mb", 0)) / total_mem
    if used_mem_pct >= mem_warn_pct:
        notes.append(f"系统内存使用率约 {used_mem_pct:.1f}%，需要警惕数据加载或缓存占用过高。")

    if float(disk.get("used_pct", 0)) >= disk_warn_pct:
        notes.append(f"项目所在磁盘使用率约 {disk['used_pct']}%，建议尽快检查 checkpoint 和日志空间。")

    if not notes:
        notes.append("当前未观察到明显资源瓶颈，训练更像是正常运行中的资源占用。")
    return notes


def main() -> int:
    parser = ConfigArgumentParser("Monitor remote AutoDL training resources.")
    args = parser.parse_args()

    try:
        config = load_config(args)
        validate_required_config(config, require_train_command=False)
        result = run_remote_script(config, build_resource_script(config))
        sections = split_sections(result.stdout)
        gpus = parse_gpu(sections["gpu"])
        cpu = json.loads(sections["cpu"] or "{}")
        mem = json.loads(sections["mem"] or "{}")
        disk = json.loads(sections["disk"] or "{}")
        notes = assess_bottlenecks(config, gpus, cpu, mem, disk)

        payload = {
            "gpu": gpus,
            "cpu": cpu,
            "memory": mem,
            "disk": disk,
            "assessment": notes,
        }

        if args.json:
            print_json(payload)
        else:
            print("Resource summary")
            if gpus:
                for gpu in gpus:
                    mem_pct = 100.0 * gpu["memory_used_mb"] / max(gpu["memory_total_mb"], 1.0)
                    print(
                        f"- gpu{gpu['index']}: util={gpu['utilization_gpu_pct']:.0f}% mem={gpu['memory_used_mb']:.0f}/{gpu['memory_total_mb']:.0f}MB ({mem_pct:.1f}%) temp={gpu['temperature_c']:.0f}C"
                    )
            else:
                print("- gpu: nvidia-smi unavailable or no GPU detected")
            if cpu:
                print(f"- cpu: loadavg={cpu.get('loadavg')} cores={cpu.get('cpu_count')}")
            if mem:
                used_pct = 100.0 * float(mem.get("used_mb", 0)) / max(float(mem.get("total_mb", 1)), 1.0)
                print(f"- memory: used={mem.get('used_mb')}MB / total={mem.get('total_mb')}MB ({used_pct:.1f}%)")
            if disk:
                print(f"- disk: mount={disk.get('mount')} used={disk.get('used_pct')}% available={disk.get('available_mb')}MB")
            print("- assessment:")
            for item in notes:
                print(f"  - {item}")
        return 0
    except SkillError as exc:
        print_error(str(exc), json_mode=args.json)
        return 1


if __name__ == "__main__":
    sys.exit(main())
