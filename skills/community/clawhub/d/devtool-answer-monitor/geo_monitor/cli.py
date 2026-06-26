import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def call(script_name, args):
    script = ROOT / 'scripts' / script_name
    cmd = [sys.executable, str(script), *args]
    return subprocess.check_call(cmd)


def cmd_run(ns):
    return call('run_monitor.py', ['--query-pool', ns.query_pool, '--model-config', ns.model_config, '--out-dir', ns.out_dir, *(['--manual-responses', ns.manual_responses] if ns.manual_responses else []), *(['--limit', str(ns.limit)] if ns.limit is not None else [])])


def cmd_report(ns):
    call('score_run.py', ['--input', ns.input, '--output-dir', ns.output_dir])
    summary_path = str(Path(ns.output_dir) / 'summary.json')
    output_path = ns.output or str(Path(ns.output_dir) / 'weekly_report.md')
    return call('generate_weekly_report.py', ['--summary', summary_path, '--output', output_path])


def cmd_validate(ns):
    return call('validate_data.py', ['--repo-root', ns.repo_root])


def cmd_leaderboard(ns):
    return call('build_leaderboard.py', ['--runs-root', ns.runs_root, '--output-dir', ns.output_dir, '--image-output', ns.image_output])


def main(argv=None):
    parser = argparse.ArgumentParser(prog='python -m devtool_answer_monitor')
    sub = parser.add_subparsers(dest='command', required=True)

    run_p = sub.add_parser('run', help='Run query pool collection')
    run_p.add_argument('--query-pool', required=True)
    run_p.add_argument('--model-config', required=True)
    run_p.add_argument('--out-dir', required=True)
    run_p.add_argument('--manual-responses')
    run_p.add_argument('--limit', type=int)
    run_p.set_defaults(func=cmd_run)

    report_p = sub.add_parser('report', help='Build summary and weekly report from annotation input')
    report_p.add_argument('--input', required=True)
    report_p.add_argument('--output-dir', required=True)
    report_p.add_argument('--output')
    report_p.set_defaults(func=cmd_report)

    validate_p = sub.add_parser('validate', help='Validate schemas and sample data')
    validate_p.add_argument('--repo-root', default=str(ROOT))
    validate_p.set_defaults(func=cmd_validate)

    lb_p = sub.add_parser('leaderboard', help='Generate leaderboard outputs')
    lb_p.add_argument('--runs-root', default='data/runs')
    lb_p.add_argument('--output-dir', default='data/leaderboards')
    lb_p.add_argument('--image-output', default='assets/leaderboard-sample.png')
    lb_p.set_defaults(func=cmd_leaderboard)

    ns = parser.parse_args(argv)
    return ns.func(ns)
