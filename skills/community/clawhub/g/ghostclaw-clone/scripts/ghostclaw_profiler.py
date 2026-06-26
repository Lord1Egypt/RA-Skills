#!/usr/bin/env python3
"""
Ghostclaw profiling tool to identify timeout bottlenecks.
Uses cProfile for function-level profiling and simple timers for high-level phases.
"""

import asyncio
import sys
import time
import cProfile
import pstats
from io import StringIO
from datetime import datetime
from pathlib import Path

# Add ghostclaw src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "ghostclaw-clone" / "src"))

from ghostclaw.cli.services.analyzer_service import AnalyzerService

class SimpleTimer:
    """Track high-level phase timings."""
    def __init__(self):
        self.timings = {}
        self._starts = {}

    def start(self, name):
        self._starts[name] = time.perf_counter()

    def end(self, name):
        if name in self._starts:
            self.timings[name] = time.perf_counter() - self._starts[name]
            del self._starts[name]

    def get_total(self):
        return sum(self.timings.values())

    def print_report(self):
        print("\n" + "="*60)
        print("⏱️  PHASE TIMING")
        print("="*60)
        print(f"{'Phase':<30} {'Time (s)':>12} {'%':>6}")
        print("-"*60)
        total = self.get_total()
        for phase, secs in sorted(self.timings.items(), key=lambda x: x[1], reverse=True):
            pct = (secs / total * 100) if total > 0 else 0
            bar = "▇" * int(pct / 2)
            print(f"{phase:<30} {secs:>12.4f} {pct:>5.1f}% {bar}")
        print("-"*60)
        print(f"{'TOTAL':<30} {total:>12.4f} 100%")
        print("="*60)

def print_profile_stats(pr, top_n=30):
    """Print formatted cProfile statistics."""
    s = StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats(top_n)
    print("\n" + "="*60)
    print("📊 TOP FUNCTIONS (cumulative time)")
    print("="*60)
    print(s.getvalue())
    print("="*60)

def print_func_timings(pr):
    """Print functions that took > 0.5s for deeper investigation."""
    s = StringIO()
    pstats.Stats(pr, stream=s).sort_stats('cumulative').print_stats(0.5)
    lines = s.getvalue().split('\n')
    if len(lines) > 5:
        print("\n🔎 Functions > 0.5s:")
        print('\n'.join(lines[:50]))

async def run_with_profiling(repo_path, config_overrides, use_profile=True, save_profile=None):
    timer = SimpleTimer()

    timer.start("service_setup")
    service = AnalyzerService(
        repo_path=repo_path,
        config_overrides=config_overrides,
        use_cache=not config_overrides.get('no_cache', False),
        benchmark=True,
        json_output=True
    )
    timer.end("service_setup")

    if use_profile:
        pr = cProfile.Profile()
        timer.start("analysis")
        pr.enable()
        report = await service.run()
        pr.disable()
        timer.end("analysis")

        # Print profiling data
        print_profile_stats(pr, top_n=40)
        print_func_timings(pr)

        if save_profile:
            from pathlib import Path
            out_path = Path(save_profile)
            ps = pstats.Stats(pr)
            ps.dump_stats(str(out_path))
            print(f"\n💾 Raw profile saved to: {out_path}")
            print(f"   View with: snakeviz {out_path} or: python -m pstats {out_path}")
    else:
        timer.start("analysis")
        report = await service.run()
        timer.end("analysis")

    timer.print_report()

    # Show agent timings if available
    if hasattr(service, 'timings') and service.timings:
        print("\n🔬 Agent internal timings:")
        for key, val in sorted(service.timings.items()):
            print(f"  {key:25} {val:>8.3f}s")

    return report

async def main():
    import argparse
    parser = argparse.ArgumentParser(description="Profile ghostclaw analysis")
    parser.add_argument("repo_path", nargs="?", default=".", help="Path to repository")
    parser.add_argument("--use-ai", action="store_true", help="Enable AI synthesis")
    parser.add_argument("--no-cache", action="store_true", help="Disable cache")
    parser.add_argument("--no-parallel", action="store_true", help="Disable parallel scanning")
    parser.add_argument("--concurrency-limit", type=int, help="Max concurrent file operations")
    parser.add_argument("--no-profile", action="store_true", help="Disable cProfile, use only phase timers")
    parser.add_argument("--save-profile", help="Save cProfile data to binary file")
    args = parser.parse_args()

    repo_path = Path(args.repo_path).resolve()
    if not repo_path.exists():
        print(f"Error: Repository path does not exist: {repo_path}")
        sys.exit(1)

    overrides = {}
    if args.use_ai:
        overrides['use_ai'] = True
    else:
        # Explicitly disable AI to avoid using global default (which might be True)
        overrides['use_ai'] = False
    if args.no_cache:
        overrides['use_cache'] = False
    if args.no_parallel:
        overrides['parallel_enabled'] = False
    if args.concurrency_limit is not None:
        overrides['concurrency_limit'] = args.concurrency_limit

    print(f"🔬 Ghostclaw Profiler")
    print(f"   Repository: {repo_path}")
    print(f"   Config Overrides: {overrides}")
    print(f"   cProfile: {not args.no_profile}")
    print()

    try:
        await run_with_profiling(
            repo_path=str(repo_path),
            config_overrides=overrides,
            use_profile=not args.no_profile,
            save_profile=args.save_profile
        )
    except Exception as e:
        print(f"\n❌ Profiling failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
