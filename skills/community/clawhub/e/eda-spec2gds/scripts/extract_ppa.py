#!/usr/bin/env python3
from pathlib import Path
import json
import sys


def pick(d, key, default=None):
    return d.get(key, default)


def collect_prefix(metrics, prefix):
    return {k: v for k, v in metrics.items() if k.startswith(prefix)}


def main():
    if len(sys.argv) < 3:
        print('usage: extract_ppa.py <metrics.json> <output.json>', file=sys.stderr)
        sys.exit(1)

    metrics_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])
    metrics = json.loads(metrics_path.read_text(encoding='utf-8'))

    ppa = {
        'summary': {
            'area': {
                'die_area': pick(metrics, 'design__die__area'),
                'core_area': pick(metrics, 'design__core__area'),
                'instance_area': pick(metrics, 'design__instance__area'),
                'stdcell_area': pick(metrics, 'design__instance__area__stdcell'),
                'utilization': pick(metrics, 'design__instance__utilization'),
            },
            'timing': {
                'setup_wns': pick(metrics, 'timing__setup__wns'),
                'setup_tns': pick(metrics, 'timing__setup__tns'),
                'hold_wns': pick(metrics, 'timing__hold__wns'),
                'hold_tns': pick(metrics, 'timing__hold__tns'),
            },
            'power': {
                'total': pick(metrics, 'power__total'),
                'internal': pick(metrics, 'power__internal__total'),
                'switching': pick(metrics, 'power__switching__total'),
                'leakage': pick(metrics, 'power__leakage__total'),
            },
            'route': {
                'wirelength': pick(metrics, 'route__wirelength'),
                'wirelength_estimated': pick(metrics, 'route__wirelength__estimated'),
                'drc_errors': pick(metrics, 'route__drc_errors'),
            },
            'checks': {
                'magic_drc_errors': pick(metrics, 'magic__drc_error__count'),
                'lvs_errors': pick(metrics, 'design__lvs_error__count'),
                'max_slew_violations': pick(metrics, 'design__max_slew_violation__count'),
                'max_cap_violations': pick(metrics, 'design__max_cap_violation__count'),
                'power_grid_violations': pick(metrics, 'design__power_grid_violation__count'),
            }
        },
        'details': {
            'timing_setup_corners': collect_prefix(metrics, 'timing__setup__wns__corner:'),
            'timing_hold_corners': collect_prefix(metrics, 'timing__hold__wns__corner:'),
            'timing_setup_tns_corners': collect_prefix(metrics, 'timing__setup__tns__corner:'),
            'timing_hold_tns_corners': collect_prefix(metrics, 'timing__hold__tns__corner:'),
            'max_slew_corners': collect_prefix(metrics, 'design__max_slew_violation__count__corner:'),
            'max_cap_corners': collect_prefix(metrics, 'design__max_cap_violation__count__corner:'),
            'route_iterations': collect_prefix(metrics, 'route__drc_errors__iter:'),
            'wirelength_iterations': collect_prefix(metrics, 'route__wirelength__iter:'),
            'power_grid': {k: v for k, v in metrics.items() if k.startswith('design_powergrid__')},
            'lvs_breakdown': {k: v for k, v in metrics.items() if k.startswith('design__lvs_')},
        },
        'raw_metric_count': len(metrics)
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(ppa, indent=2, ensure_ascii=False), encoding='utf-8')
    print(out_path)


if __name__ == '__main__':
    main()
