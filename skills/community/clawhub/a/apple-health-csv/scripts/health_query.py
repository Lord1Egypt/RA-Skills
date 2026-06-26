#!/usr/bin/env python3
"""Apple Health CSV data query tool.

Usage:
  health_query.py list                          List available health metrics
  health_query.py summary [--json]              Comprehensive daily health summary
  health_query.py query <metric> [--days N] [--json]  Query specific metric
"""

import csv
import os
import sys
import json
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path

DATA_DIR = Path(os.environ.get(
    'HEALTH_DATA_DIR',
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'health-data')
)).resolve()

METRICS = {
    'HeartRate': ('心率', 'count/min', 'rate'),
    'StepCount': ('步数', '步', 'cumulative'),
    'ActiveEnergyBurned': ('活动消耗', 'kcal', 'cumulative'),
    'BasalEnergyBurned': ('基础消耗', 'kcal', 'cumulative'),
    'DistanceWalkingRunning': ('步行跑步距离', 'km', 'cumulative'),
    'DistanceCycling': ('骑行距离', 'km', 'cumulative'),
    'DistanceSwimming': ('游泳距离', 'm', 'cumulative'),
    'FlightsClimbed': ('爬楼', '层', 'cumulative'),
    'SleepAnalysis': ('睡眠', '', 'sleep'),
    'OxygenSaturation': ('血氧', '%', 'percentage'),
    'RespiratoryRate': ('呼吸频率', '次/min', 'rate'),
    'RestingHeartRate': ('静息心率', 'count/min', 'rate'),
    'HeartRateVariabilitySDNN': ('心率变异性', 'ms', 'rate'),
    'VO2Max': ('最大摄氧量', 'mL/min·kg', 'rate'),
    'BodyMass': ('体重', 'kg', 'rate'),
    'BodyFatPercentage': ('体脂率', '%', 'percentage'),
    'BodyMassIndex': ('BMI', '', 'rate'),
    'Height': ('身高', 'cm', 'rate'),
    'LeanBodyMass': ('去脂体重', 'kg', 'rate'),
    'AppleExerciseTime': ('运动时间', 'min', 'cumulative'),
    'AppleStandTime': ('站立时间', 'min', 'cumulative'),
    'WalkingSpeed': ('步行速度', 'km/hr', 'rate'),
    'WalkingStepLength': ('步长', 'cm', 'rate'),
    'WalkingAsymmetryPercentage': ('步行不对称', '%', 'percentage'),
    'WalkingDoubleSupportPercentage': ('双脚支撑时间', '%', 'percentage'),
    'EnvironmentalAudioExposure': ('环境噪音', 'dBASPL', 'rate'),
    'HeadphoneAudioExposure': ('耳机音量', 'dBASPL', 'rate'),
    'AppleSleepingWristTemperature': ('睡眠腕温', '°C', 'rate'),
    'WalkingHeartRateAverage': ('步行平均心率', 'count/min', 'rate'),
    'DietaryWater': ('饮水', 'mL', 'cumulative'),
    'SixMinuteWalkTestDistance': ('六分钟步行距离', 'm', 'rate'),
    'AppleWalkingSteadiness': ('步行稳定性', '', 'rate'),
    'NumberOfTimesFallen': ('跌倒次数', '次', 'cumulative'),
    'StairAscentSpeed': ('上楼速度', 'ft/s', 'rate'),
    'StairDescentSpeed': ('下楼速度', 'ft/s', 'rate'),
    'SwimmingStrokeCount': ('游泳划水', '次', 'cumulative'),
}

SUMMARY_METRICS = [
    'StepCount', 'ActiveEnergyBurned', 'HeartRate', 'RestingHeartRate',
    'OxygenSaturation', 'SleepAnalysis', 'AppleExerciseTime',
    'BodyMass', 'DistanceWalkingRunning',
]


def find_csv(metric_key):
    """Find CSV file for a metric using exact HK type identifier prefix matching."""
    for prefix in ['HKQuantityTypeIdentifier', 'HKCategoryTypeIdentifier', 'HKWorkoutActivityType']:
        pattern = prefix + metric_key + '_*'
        matches = list(DATA_DIR.glob(pattern))
        if matches:
            return matches[0]
    return None


def read_csv(filepath, days=7):
    """Read CSV file and return rows within the specified day range."""
    cutoff = datetime.now() - timedelta(days=days)
    rows = []
    with open(filepath, 'r', encoding='utf-8') as f:
        first_line = f.readline()
        if not first_line.startswith('sep='):
            f.seek(0)
        reader = csv.DictReader(f)
        for row in reader:
            start = row.get('startDate', '')
            try:
                dt = datetime.strptime(start[:19], '%Y-%m-%d %H:%M:%S')
                if dt >= cutoff:
                    rows.append({**row, '_datetime': dt})
            except (ValueError, TypeError):
                continue
    return sorted(rows, key=lambda x: x['_datetime'])


def extract_value(row):
    """Extract numeric value from a row, trying multiple column names."""
    for col in ['value', 'qty', 'quantity']:
        val = row.get(col)
        if val is not None:
            try:
                return float(val)
            except (ValueError, TypeError):
                continue
    return None


def group_by_day(rows):
    """Group rows by date and extract numeric values."""
    by_day = defaultdict(list)
    for r in rows:
        day = r['_datetime'].strftime('%Y-%m-%d')
        val = extract_value(r)
        if val is not None:
            by_day[day].append(val)
    return dict(sorted(by_day.items()))


def analyze_sleep(rows):
    """Analyze sleep data, grouped by night (cross-midnight aware)."""
    by_night = defaultdict(list)
    for r in rows:
        night = (r['_datetime'] - timedelta(hours=12)).strftime('%Y-%m-%d')
        by_night[night].append(r)

    results = {}
    for night, sleep_rows in sorted(by_night.items()):
        total_min = 0
        stages = defaultdict(float)
        for r in sleep_rows:
            val = r.get('value', '')
            if 'Asleep' not in val and 'InBed' not in val:
                continue
            try:
                start = r['_datetime']
                end = datetime.strptime(r['endDate'][:19], '%Y-%m-%d %H:%M:%S')
                dur = (end - start).total_seconds() / 60
                if 'Asleep' in val:
                    total_min += dur
                    stage = val.replace('HKCategoryValueSleepAnalysis', '')
                    stages[stage] += dur
            except (ValueError, KeyError):
                pass
        if total_min > 0:
            results[night] = {
                'total_hours': round(total_min / 60, 1),
                'total_minutes': round(total_min),
                'stages': {s: round(m) for s, m in sorted(stages.items())},
            }
    return results


def format_value(val, metric_type):
    """Format a value based on metric type."""
    if metric_type == 'percentage':
        return val * 100 if val <= 1 else val
    return val


def cmd_list(as_json=False):
    """List available health metrics with data counts."""
    available = []
    for key, (name, unit, mtype) in sorted(METRICS.items()):
        f = find_csv(key)
        if not f:
            continue
        with open(f, encoding='utf-8') as fh:
            lines = sum(1 for _ in fh) - 2
        if lines > 0:
            available.append({
                'metric': key, 'name': name, 'unit': unit, 'type': mtype, 'rows': lines,
            })

    if as_json:
        print(json.dumps(available, ensure_ascii=False, indent=2))
        return

    print('Available health metrics:')
    print('%-30s %-15s %-15s %s' % ('Metric', 'Name', 'Unit', 'Rows'))
    print('-' * 75)
    for m in available:
        print('%-30s %-15s %-15s %d' % (m['metric'], m['name'], m['unit'], m['rows']))


def cmd_summary(as_json=False):
    """Generate comprehensive daily health summary."""
    now = datetime.now()
    today_str = now.strftime('%Y-%m-%d')
    results = {}

    for key in SUMMARY_METRICS:
        f = find_csv(key)
        if not f:
            continue
        name, unit, mtype = METRICS[key]

        if key == 'SleepAnalysis':
            sleep = analyze_sleep(read_csv(f, days=2))
            if sleep:
                latest = list(sleep.values())[-1]
                results[key] = {
                    'name': name, 'value': latest['total_hours'],
                    'unit': 'hours', 'detail': latest,
                }
            continue

        rows_today = read_csv(f, days=1)
        rows_week = read_csv(f, days=7) if not rows_today else []

        source_rows = rows_today or rows_week
        period = 'today' if rows_today else '7d'
        values = [v for v in (extract_value(r) for r in source_rows) if v is not None]

        if not values:
            continue

        if mtype == 'cumulative':
            results[key] = {
                'name': name, 'value': round(sum(values)),
                'unit': unit, 'period': period,
            }
        elif mtype == 'percentage':
            vals = [v * 100 if v <= 1 else v for v in values]
            results[key] = {
                'name': name, 'value': round(sum(vals) / len(vals), 1),
                'unit': '%', 'min': round(min(vals), 1),
                'max': round(max(vals), 1), 'count': len(vals), 'period': period,
            }
        else:
            results[key] = {
                'name': name, 'value': round(sum(values) / len(values), 1),
                'unit': unit, 'min': round(min(values), 1),
                'max': round(max(values), 1), 'count': len(values), 'period': period,
            }

    if as_json:
        print(json.dumps({'date': today_str, 'metrics': results}, ensure_ascii=False, indent=2))
        return

    print('=== Health Summary (%s) ===\n' % today_str)
    for key in SUMMARY_METRICS:
        if key not in results:
            continue
        r = results[key]
        period_label = '今日' if r.get('period') == 'today' else '近7天'
        if key == 'SleepAnalysis':
            detail = r.get('detail', {})
            stages = detail.get('stages', {})
            stage_str = ' | '.join('%s: %dmin' % (s, m) for s, m in stages.items())
            print('  %s: %.1f 小时 [%s]' % (r['name'], r['value'], stage_str))
        elif METRICS[key][2] == 'cumulative':
            print('  %s: %d %s（%s）' % (r['name'], r['value'], r['unit'], period_label))
        else:
            if 'min' in r:
                print('  %s: %.1f %s（%s, 范围 %.1f-%.1f, %d条）' % (
                    r['name'], r['value'], r['unit'], period_label,
                    r['min'], r['max'], r['count']))
            else:
                print('  %s: %.1f %s（%s）' % (r['name'], r['value'], r['unit'], period_label))


def cmd_query(metric, days=7, as_json=False):
    """Query a specific health metric."""
    f = find_csv(metric)
    if not f:
        print('Metric not found: %s' % metric, file=sys.stderr)
        print('Available: %s' % ', '.join(sorted(METRICS.keys())), file=sys.stderr)
        sys.exit(1)

    name, unit, mtype = METRICS.get(metric, (metric, '', 'rate'))
    rows = read_csv(f, days=days)

    if mtype == 'sleep':
        sleep = analyze_sleep(rows)
        if as_json:
            print(json.dumps({
                'metric': metric, 'name': name, 'days': days, 'data': sleep,
            }, ensure_ascii=False, indent=2))
            return
        print('=== %s (%s) last %d days ===\n' % (name, metric, days))
        for night, data in sleep.items():
            stages = data.get('stages', {})
            stage_str = ' | '.join('%s: %dmin' % (s, m) for s, m in stages.items())
            print('  %s: %.1fh [%s]' % (night, data['total_hours'], stage_str))
        return

    by_day = group_by_day(rows)

    if as_json:
        json_data = {}
        for day, values in by_day.items():
            if mtype == 'percentage':
                values = [v * 100 if v <= 1 else v for v in values]
            if mtype == 'cumulative':
                json_data[day] = {'total': round(sum(values)), 'count': len(values)}
            else:
                json_data[day] = {
                    'avg': round(sum(values) / len(values), 1),
                    'min': round(min(values), 1),
                    'max': round(max(values), 1),
                    'count': len(values),
                }
        print(json.dumps({
            'metric': metric, 'name': name, 'unit': unit,
            'days': days, 'data': json_data,
        }, ensure_ascii=False, indent=2))
        return

    print('=== %s (%s) last %d days ===\n' % (name, metric, days))
    for day, values in by_day.items():
        if mtype == 'percentage':
            values = [v * 100 if v <= 1 else v for v in values]
        if mtype == 'cumulative':
            print('  %s: %d %s' % (day, sum(values), unit))
        else:
            avg = sum(values) / len(values)
            print('  %s: avg %.1f %s (%.1f-%.1f, %d records)' % (
                day, avg, unit, min(values), max(values), len(values)))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1]
    as_json = '--json' in sys.argv

    if cmd == 'list':
        cmd_list(as_json)
    elif cmd == 'summary':
        cmd_summary(as_json)
    elif cmd == 'query':
        if len(sys.argv) < 3:
            print('Usage: health_query.py query <metric> [--days N] [--json]', file=sys.stderr)
            sys.exit(1)
        metric = sys.argv[2]
        days = 7
        if '--days' in sys.argv:
            idx = sys.argv.index('--days')
            if idx + 1 < len(sys.argv):
                days = int(sys.argv[idx + 1])
        cmd_query(metric, days, as_json)
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == '__main__':
    main()
