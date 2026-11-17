#!/usr/bin/env python3
"""Estimate AI short-drama production workload and generation volume."""
from __future__ import annotations

import argparse
import json
import math


COMPLEXITY = {"low": 0.80, "medium": 1.00, "high": 1.35}


def estimate(args: argparse.Namespace) -> dict:
    cm = COMPLEXITY[args.complexity]
    shots_per_episode = args.shots_per_episode or math.ceil(args.duration / args.avg_shot)
    total_shots = args.episodes * shots_per_episode
    raw_generations = math.ceil(total_shots * args.variants * (1 + args.rework))
    keyframes = math.ceil(total_shots * 1.2)

    hours = {
        "prompt_and_shot_design": total_shots * 0.12 * cm,
        "character_scene_consistency": total_shots * 0.06 * cm,
        "generation_operations": raw_generations * 0.05 * cm,
        "visual_qc_and_regeneration": total_shots * 0.08 * cm,
        "asset_preparation": 8 + 2 * args.characters + 0.4 * args.scenes,
        "editing_and_finishing": args.episodes * (args.duration / 60) * 2.2 * cm,
        "voice_and_tts": args.episodes * (args.duration / 60) * 1.2 * cm,
        "subtitles": args.episodes * 0.5,
        "lipsync": total_shots * 0.35 * 0.12 * cm,
    }
    subtotal = sum(hours.values())
    hours["production_management"] = subtotal * 0.12
    hours["qa_and_release_buffer"] = (subtotal + hours["production_management"]) * 0.10
    total_hours = sum(hours.values())

    person_days = total_hours / 8
    generation_wall_hours = (
        raw_generations * args.avg_generation_minutes / max(args.parallel, 1) / 60
    )
    wall_days = person_days / max(args.team_size, 1) * 1.15 + generation_wall_hours / 24
    storage_gb = raw_generations * 0.04 + keyframes * 0.002 + total_shots * 0.02 + 5

    return {
        "assumptions": {
            "episodes": args.episodes,
            "duration_sec": args.duration,
            "avg_shot_sec": args.avg_shot,
            "shots_per_episode": shots_per_episode,
            "variants_per_shot": args.variants,
            "rework_rate": args.rework,
            "characters": args.characters,
            "scenes": args.scenes,
            "complexity": args.complexity,
            "complexity_multiplier": cm,
            "parallel_generation_tasks": args.parallel,
            "avg_generation_minutes": args.avg_generation_minutes,
            "team_size": args.team_size,
        },
        "volume": {
            "accepted_shots": total_shots,
            "keyframes": keyframes,
            "raw_generations": raw_generations,
            "estimated_storage_gb": round(storage_gb, 1),
        },
        "person_hours": {k: round(v, 1) for k, v in hours.items()},
        "total_person_hours": round(total_hours, 1),
        "person_days": round(person_days, 1),
        "generation_wall_hours": round(generation_wall_hours, 1),
        "estimated_wall_days": round(wall_days, 1),
        "release_gate": (
            "Do not submit paid generation until scope, character references, canvas, "
            "shot manifest, task count, resolution, duration, and expected wait are approved."
        ),
    }


def print_markdown(result: dict) -> None:
    a = result["assumptions"]
    v = result["volume"]
    print("# AI短剧工作量估算\n")
    print("## 假设\n")
    for key, value in a.items():
        print(f"- `{key}`: {value}")
    print("\n## 生成量\n")
    for key, value in v.items():
        print(f"- `{key}`: {value}")
    print("\n## 人时拆分\n")
    for key, value in result["person_hours"].items():
        print(f"- `{key}`: {value} 小时")
    print("\n## 汇总\n")
    print(f"- 总人时：{result['total_person_hours']} 小时")
    print(f"- 人日：{result['person_days']} 人日")
    print(f"- 生成队列墙钟时间：{result['generation_wall_hours']} 小时")
    print(f"- 预计日历周期：{result['estimated_wall_days']} 天")
    print(f"- 预计存储：{v['estimated_storage_gb']} GB")
    print(f"\n**付费生成闸门：** {result['release_gate']}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--episodes", type=int, default=20)
    parser.add_argument("--duration", type=float, default=120, help="Seconds per episode")
    parser.add_argument("--avg-shot", type=float, default=8, help="Average accepted shot seconds")
    parser.add_argument("--variants", type=float, default=2.5, help="Generated takes per accepted shot")
    parser.add_argument("--rework", type=float, default=0.15, help="Extra retry ratio")
    parser.add_argument("--characters", type=int, default=1)
    parser.add_argument("--scenes", type=int, default=12)
    parser.add_argument("--complexity", choices=COMPLEXITY, default="medium")
    parser.add_argument("--parallel", type=int, default=4)
    parser.add_argument("--avg-generation-minutes", type=float, default=8)
    parser.add_argument("--team-size", type=int, default=4)
    parser.add_argument("--shots-per-episode", type=int, default=0)
    parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown")
    args = parser.parse_args()
    result = estimate(args)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_markdown(result)


if __name__ == "__main__":
    main()
