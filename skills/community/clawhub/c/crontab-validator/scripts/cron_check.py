#!/usr/bin/env python3
"""Crontab expression validator, explainer, and next-run calculator."""

import sys
import json
import argparse
import re
from datetime import datetime, timedelta
import calendar

FIELD_NAMES = ['minute', 'hour', 'day_of_month', 'month', 'day_of_week']
FIELD_RANGES = {
    'minute': (0, 59),
    'hour': (0, 23),
    'day_of_month': (1, 31),
    'month': (1, 12),
    'day_of_week': (0, 7),  # 0 and 7 = Sunday
}

MONTH_NAMES = {
    'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
    'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
}

DOW_NAMES = {
    'sun': 0, 'mon': 1, 'tue': 2, 'wed': 3, 'thu': 4, 'fri': 5, 'sat': 6
}

SHORTCUTS = {
    '@yearly': '0 0 1 1 *',
    '@annually': '0 0 1 1 *',
    '@monthly': '0 0 1 * *',
    '@weekly': '0 0 * * 0',
    '@daily': '0 0 * * *',
    '@midnight': '0 0 * * *',
    '@hourly': '0 * * * *',
}


class CronField:
    def __init__(self, raw, name):
        self.raw = raw
        self.name = name
        self.min_val, self.max_val = FIELD_RANGES[name]
        self.values = set()
        self.is_wildcard = (raw.strip() == '*')
        self._parse()

    def _parse(self):
        field = self.raw.lower()

        # Replace month/dow names
        if self.name == 'month':
            for name, num in MONTH_NAMES.items():
                field = field.replace(name, str(num))
        elif self.name == 'day_of_week':
            for name, num in DOW_NAMES.items():
                field = field.replace(name, str(num))

        for part in field.split(','):
            part = part.strip()
            if not part:
                raise ValueError(f'Empty part in {self.name}: {self.raw}')

            # Step: */2 or 1-10/2
            step_match = re.match(r'^(.+)/(\d+)$', part)
            step = 1
            if step_match:
                part = step_match.group(1)
                step = int(step_match.group(2))
                if step == 0:
                    raise ValueError(f'Step cannot be 0 in {self.name}: {self.raw}')

            # Wildcard
            if part == '*':
                for v in range(self.min_val, self.max_val + 1, step):
                    self.values.add(v)
                continue

            # Range: 1-5
            range_match = re.match(r'^(\d+)-(\d+)$', part)
            if range_match:
                start = int(range_match.group(1))
                end = int(range_match.group(2))
                self._validate_range(start, end)
                for v in range(start, end + 1, step):
                    self.values.add(v)
                continue

            # Single value
            if re.match(r'^\d+$', part):
                val = int(part)
                self._validate_val(val)
                if step_match:
                    for v in range(val, self.max_val + 1, step):
                        self.values.add(v)
                else:
                    self.values.add(val)
                continue

            raise ValueError(f'Invalid {self.name} field: {self.raw}')

        # Normalize day_of_week: 7 → 0 (both mean Sunday)
        if self.name == 'day_of_week' and 7 in self.values:
            self.values.discard(7)
            self.values.add(0)

    def _validate_val(self, val):
        if val < self.min_val or val > self.max_val:
            raise ValueError(
                f'{self.name} value {val} out of range [{self.min_val}-{self.max_val}]: {self.raw}'
            )

    def _validate_range(self, start, end):
        self._validate_val(start)
        self._validate_val(end)
        if start > end:
            raise ValueError(f'Invalid range {start}-{end} in {self.name}: {self.raw}')

    def matches(self, val):
        return val in self.values

    def explain(self):
        sorted_vals = sorted(self.values)
        total = self.max_val - self.min_val + 1

        if len(sorted_vals) == total:
            return f'every {self.name}'
        if len(sorted_vals) == 1:
            return self._format_single(sorted_vals[0])

        # Check if it's a step pattern
        if len(sorted_vals) > 2:
            diffs = [sorted_vals[i+1] - sorted_vals[i] for i in range(len(sorted_vals)-1)]
            if len(set(diffs)) == 1:
                step = diffs[0]
                start = sorted_vals[0]
                if start == self.min_val:
                    return f'every {step} {self.name}s'
                return f'every {step} {self.name}s from {self._format_single(start)}'

        formatted = [self._format_single(v) for v in sorted_vals]
        return f'{self.name} {", ".join(formatted)}'

    def _format_single(self, val):
        if self.name == 'minute':
            return f':{val:02d}'
        if self.name == 'hour':
            if val == 0:
                return '12 AM'
            if val < 12:
                return f'{val} AM'
            if val == 12:
                return '12 PM'
            return f'{val - 12} PM'
        if self.name == 'day_of_month':
            return f'day {val}'
        if self.name == 'month':
            months = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December']
            return months[val] if 1 <= val <= 12 else str(val)
        if self.name == 'day_of_week':
            days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
            return days[val] if 0 <= val <= 6 else str(val)
        return str(val)


class CronExpr:
    def __init__(self, expression):
        self.raw = expression.strip()
        expr = SHORTCUTS.get(self.raw.lower(), self.raw)
        parts = expr.split()
        if len(parts) != 5:
            raise ValueError(
                f'Expected 5 fields (minute hour day month weekday), got {len(parts)}: {self.raw}'
            )
        self.fields = {}
        for i, name in enumerate(FIELD_NAMES):
            self.fields[name] = CronField(parts[i], name)

    def explain(self):
        parts = [self.fields[name].explain() for name in FIELD_NAMES]
        # Build human-readable sentence
        minute = self.fields['minute']
        hour = self.fields['hour']
        dom = self.fields['day_of_month']
        month = self.fields['month']
        dow = self.fields['day_of_week']

        time_part = ''
        if len(minute.values) == 1 and len(hour.values) == 1:
            m = sorted(minute.values)[0]
            h = sorted(hour.values)[0]
            time_part = f'At {h:02d}:{m:02d}'
        elif len(minute.values) == 1:
            m = sorted(minute.values)[0]
            time_part = f'At minute {m} of {hour.explain()}'
        elif len(hour.values) == 1:
            time_part = f'At {minute.explain()} past {hour.explain()}'
        else:
            time_part = f'{minute.explain()}, {hour.explain()}'

        when_parts = []
        dom_all = len(dom.values) == 31
        dow_all = len(dow.values) == 7
        month_all = len(month.values) == 12

        if not dom_all:
            when_parts.append(f'on {dom.explain()}')
        if not dow_all:
            when_parts.append(f'on {dow.explain()}')
        if not month_all:
            when_parts.append(f'in {month.explain()}')

        result = time_part
        if when_parts:
            result += ', ' + ', '.join(when_parts)
        return result

    def next_runs(self, count=5, from_time=None):
        """Calculate next N run times."""
        if from_time is None:
            from_time = datetime.now()

        runs = []
        current = from_time.replace(second=0, microsecond=0) + timedelta(minutes=1)

        max_iterations = 525960  # 1 year of minutes
        iterations = 0

        while len(runs) < count and iterations < max_iterations:
            iterations += 1
            if self._matches(current):
                runs.append(current)
                current += timedelta(minutes=1)
            else:
                # Skip ahead intelligently
                if not self.fields['month'].matches(current.month):
                    # Skip to next matching month
                    current = self._next_month(current)
                elif not self._day_matches(current):
                    current = current.replace(hour=0, minute=0) + timedelta(days=1)
                elif not self.fields['hour'].matches(current.hour):
                    current = current.replace(minute=0) + timedelta(hours=1)
                else:
                    current += timedelta(minutes=1)

        return runs

    def _matches(self, dt):
        if not self.fields['minute'].matches(dt.minute):
            return False
        if not self.fields['hour'].matches(dt.hour):
            return False
        if not self.fields['month'].matches(dt.month):
            return False
        return self._day_matches(dt)

    def _day_matches(self, dt):
        dom_field = self.fields['day_of_month']
        dow_field = self.fields['day_of_week']
        dom_all = len(dom_field.values) == 31
        dow_all = len(dow_field.values) == 7

        # Standard cron: if both restricted, match either (OR logic)
        if not dom_all and not dow_all:
            return dom_field.matches(dt.day) or dow_field.matches(dt.weekday() if dt.weekday() != 6 else 0)

        dow_val = (dt.isoweekday() % 7)  # 0=Sun, 1=Mon, ...
        if not dom_all:
            return dom_field.matches(dt.day)
        if not dow_all:
            return dow_field.matches(dow_val)
        return True

    def _next_month(self, dt):
        month = dt.month
        year = dt.year
        for _ in range(12):
            month += 1
            if month > 12:
                month = 1
                year += 1
            if self.fields['month'].matches(month):
                return dt.replace(year=year, month=month, day=1, hour=0, minute=0)
        return dt + timedelta(days=366)

    def lint(self):
        """Run lint checks on the expression."""
        findings = []

        # Check for every-minute pattern
        if (len(self.fields['minute'].values) == 60 and
                len(self.fields['hour'].values) == 24):
            findings.append({
                'level': 'warning',
                'message': 'Runs every minute — is this intentional?'
            })

        # Check for conflicting day-of-month and day-of-week
        dom_all = len(self.fields['day_of_month'].values) == 31
        dow_all = len(self.fields['day_of_week'].values) == 7
        if not dom_all and not dow_all:
            findings.append({
                'level': 'info',
                'message': 'Both day-of-month and day-of-week specified — uses OR logic (matches either)'
            })

        # Check for day 31 in months without 31 days (only if day explicitly specified)
        if not self.fields['day_of_month'].is_wildcard and 31 in self.fields['day_of_month'].values:
            restricted_months = self.fields['month'].values
            short_months = {2, 4, 6, 9, 11}
            overlap = restricted_months & short_months
            if overlap:
                month_names = {2: 'Feb', 4: 'Apr', 6: 'Jun', 9: 'Sep', 11: 'Nov'}
                names = [month_names[m] for m in sorted(overlap)]
                findings.append({
                    'level': 'warning',
                    'message': f'Day 31 specified but {", ".join(names)} have fewer days — job will skip those months'
                })

        # Check for February 29/30/31 (only if day explicitly specified)
        if not self.fields['day_of_month'].is_wildcard and self.fields['month'].matches(2):
            high_days = {d for d in self.fields['day_of_month'].values if d > 28}
            if high_days:
                findings.append({
                    'level': 'warning',
                    'message': f'Day(s) {sorted(high_days)} in February — will only run in leap years (29) or never (30-31)'
                })

        # Very frequent schedules
        runs_per_hour = len(self.fields['minute'].values)
        runs_per_day = runs_per_hour * len(self.fields['hour'].values)
        if runs_per_day > 288:  # more than every 5 min
            findings.append({
                'level': 'info',
                'message': f'High frequency: ~{runs_per_day} runs per day'
            })

        return findings


def cmd_validate(args):
    results = []
    exit_code = 0
    for expr in args.expressions:
        try:
            cron = CronExpr(expr)
            entry = {
                'expression': expr, 'valid': True,
                'explanation': cron.explain()
            }
            if args.lint:
                findings = cron.lint()
                entry['findings'] = findings
            results.append(entry)
        except ValueError as e:
            results.append({'expression': expr, 'valid': False, 'error': str(e)})
            exit_code = 1
    _output(results, args.format)
    return exit_code


def cmd_explain(args):
    try:
        cron = CronExpr(args.expression)
        result = {
            'expression': args.expression,
            'explanation': cron.explain(),
            'fields': {}
        }
        for name in FIELD_NAMES:
            field = cron.fields[name]
            result['fields'][name] = {
                'raw': field.raw,
                'values': sorted(field.values),
                'description': field.explain()
            }
        _output(result, args.format)
    except ValueError as e:
        _output({'expression': args.expression, 'error': str(e)}, args.format)
        return 1
    return 0


def cmd_next(args):
    try:
        cron = CronExpr(args.expression)
        from_time = datetime.now()
        if args.from_time:
            from_time = datetime.fromisoformat(args.from_time)
        runs = cron.next_runs(count=args.count, from_time=from_time)
        result = {
            'expression': args.expression,
            'from': from_time.isoformat(),
            'next_runs': [r.strftime('%Y-%m-%d %H:%M') for r in runs]
        }
        _output(result, args.format)
    except ValueError as e:
        _output({'expression': args.expression, 'error': str(e)}, args.format)
        return 1
    return 0


def cmd_lint(args):
    results = []
    exit_code = 0
    for expr in args.expressions:
        try:
            cron = CronExpr(expr)
            findings = cron.lint()
            entry = {
                'expression': expr,
                'explanation': cron.explain(),
                'findings': findings
            }
            warnings = sum(1 for f in findings if f['level'] == 'warning')
            if warnings > 0:
                entry['warnings'] = warnings
                if args.strict:
                    exit_code = 1
            results.append(entry)
        except ValueError as e:
            results.append({'expression': expr, 'error': str(e)})
            exit_code = 1
    _output(results, args.format)
    return exit_code


def _output(data, fmt):
    if fmt == 'json':
        print(json.dumps(data, indent=2, default=str))
    elif fmt == 'markdown':
        _output_md(data)
    else:
        _output_text(data)


def _output_text(data):
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                valid = item.get('valid')
                if valid is not None:
                    status = '✅' if valid else '❌'
                    print(f'{status} {item["expression"]}')
                    if valid:
                        print(f'   → {item.get("explanation", "")}')
                    else:
                        print(f'   Error: {item.get("error", "")}')
                elif 'explanation' in item:
                    print(f'  {item["expression"]}')
                    print(f'   → {item["explanation"]}')
                for f in item.get('findings', []):
                    icon = '⚠️' if f['level'] == 'warning' else 'ℹ️'
                    print(f'   {icon} {f["message"]}')
    elif isinstance(data, dict):
        if 'error' in data:
            print(f'❌ {data.get("expression", "?")}  Error: {data["error"]}')
        elif 'next_runs' in data:
            print(f'Expression: {data["expression"]}')
            print(f'Next {len(data["next_runs"])} runs:')
            for r in data['next_runs']:
                print(f'  {r}')
        elif 'fields' in data:
            print(f'Expression: {data["expression"]}')
            print(f'Summary: {data["explanation"]}')
            print()
            for name, info in data['fields'].items():
                print(f'  {name}: {info["raw"]} → {info["description"]}')
                print(f'    Values: {info["values"]}')
        else:
            for k, v in data.items():
                print(f'{k}: {v}')


def _output_md(data):
    if isinstance(data, list):
        print('| Expression | Status | Description |')
        print('|-----------|--------|-------------|')
        for item in data:
            if isinstance(item, dict):
                valid = item.get('valid', True)
                status = '✅' if valid and 'error' not in item else '❌'
                desc = item.get('explanation', item.get('error', ''))
                print(f'| `{item.get("expression", "")}` | {status} | {desc} |')
        # Findings
        for item in data:
            findings = item.get('findings', [])
            if findings:
                print(f'\n**Lint: `{item.get("expression", "")}`**')
                for f in findings:
                    icon = '⚠️' if f['level'] == 'warning' else 'ℹ️'
                    print(f'- {icon} {f["message"]}')
    elif isinstance(data, dict):
        if 'next_runs' in data:
            print(f'## Next runs for `{data["expression"]}`')
            for i, r in enumerate(data['next_runs'], 1):
                print(f'{i}. {r}')
        elif 'fields' in data:
            print(f'## `{data["expression"]}`')
            print(f'**{data["explanation"]}**')
            print()
            print('| Field | Raw | Description | Values |')
            print('|-------|-----|-------------|--------|')
            for name, info in data['fields'].items():
                vals = str(info["values"][:10])
                if len(info["values"]) > 10:
                    vals += '...'
                print(f'| {name} | `{info["raw"]}` | {info["description"]} | {vals} |')


def main():
    p = argparse.ArgumentParser(description='Crontab validator, explainer, and scheduler')
    p.add_argument('--format', '-f', choices=['text', 'json', 'markdown'], default='text')
    sub = p.add_subparsers(dest='command', required=True)

    # validate
    sv = sub.add_parser('validate', help='Validate cron expressions')
    sv.add_argument('expressions', nargs='+')
    sv.add_argument('--lint', '-l', action='store_true', help='Run lint checks')

    # explain
    se = sub.add_parser('explain', help='Explain a cron expression in detail')
    se.add_argument('expression')

    # next
    sn = sub.add_parser('next', help='Show next N run times')
    sn.add_argument('expression')
    sn.add_argument('--count', '-n', type=int, default=5, help='Number of runs (default: 5)')
    sn.add_argument('--from-time', help='Start time (ISO format, default: now)')

    # lint
    sl = sub.add_parser('lint', help='Lint cron expressions for common mistakes')
    sl.add_argument('expressions', nargs='+')
    sl.add_argument('--strict', '-s', action='store_true', help='Exit 1 on warnings')

    args = p.parse_args()
    commands = {
        'validate': cmd_validate,
        'explain': cmd_explain,
        'next': cmd_next,
        'lint': cmd_lint,
    }
    sys.exit(commands[args.command](args))


if __name__ == '__main__':
    main()
