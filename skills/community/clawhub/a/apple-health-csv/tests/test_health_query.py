#!/usr/bin/env python3
"""Unit tests for health_query.py"""

import csv
import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from io import StringIO
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
import health_query


class TestFindCsv(unittest.TestCase):
    """Tests for find_csv metric file matching."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.orig_data_dir = health_query.DATA_DIR
        health_query.DATA_DIR = Path(self.tmpdir)

    def tearDown(self):
        health_query.DATA_DIR = self.orig_data_dir
        import shutil
        shutil.rmtree(self.tmpdir)

    def _create_csv(self, name):
        path = Path(self.tmpdir) / name
        path.write_text('sep=,\ntype,value\n')
        return path

    def test_find_quantity_type(self):
        self._create_csv('HKQuantityTypeIdentifierHeartRate_2026-03-01.csv')
        result = health_query.find_csv('HeartRate')
        self.assertIsNotNone(result)
        self.assertIn('HeartRate', result.name)

    def test_find_category_type(self):
        self._create_csv('HKCategoryTypeIdentifierSleepAnalysis_2026-03-01.csv')
        result = health_query.find_csv('SleepAnalysis')
        self.assertIsNotNone(result)

    def test_find_workout_type(self):
        self._create_csv('HKWorkoutActivityTypeCycling_2026-03-01.csv')
        result = health_query.find_csv('Cycling')
        self.assertIsNotNone(result)

    def test_exact_match_heart_rate_not_resting(self):
        """HeartRate should not match RestingHeartRate or HeartRateVariabilitySDNN."""
        self._create_csv('HKQuantityTypeIdentifierHeartRate_2026-03-01.csv')
        self._create_csv('HKQuantityTypeIdentifierRestingHeartRate_2026-03-01.csv')
        self._create_csv('HKQuantityTypeIdentifierHeartRateVariabilitySDNN_2026-03-01.csv')

        hr = health_query.find_csv('HeartRate')
        rhr = health_query.find_csv('RestingHeartRate')
        hrv = health_query.find_csv('HeartRateVariabilitySDNN')

        self.assertIn('IdentifierHeartRate_', hr.name)
        self.assertIn('RestingHeartRate', rhr.name)
        self.assertIn('HeartRateVariabilitySDNN', hrv.name)

    def test_not_found(self):
        result = health_query.find_csv('NonExistentMetric')
        self.assertIsNone(result)


class TestReadCsv(unittest.TestCase):
    """Tests for CSV reading and time filtering."""

    def _write_csv(self, rows, header='sep=,\ntype,sourceName,startDate,endDate,value'):
        fd, path = tempfile.mkstemp(suffix='.csv')
        with os.fdopen(fd, 'w', newline='') as f:
            f.write(header + '\n')
            for row in rows:
                f.write(row + '\n')
        return path

    def test_read_within_range(self):
        now = datetime.now()
        yesterday = (now - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
        rows = ['HK,src,%s +0000,%s +0000,72.0' % (yesterday, yesterday)]
        path = self._write_csv(rows)
        result = health_query.read_csv(path, days=7)
        self.assertEqual(len(result), 1)
        os.unlink(path)

    def test_read_outside_range(self):
        old_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
        rows = ['HK,src,%s +0000,%s +0000,72.0' % (old_date, old_date)]
        path = self._write_csv(rows)
        result = health_query.read_csv(path, days=7)
        self.assertEqual(len(result), 0)
        os.unlink(path)

    def test_read_sorts_by_time(self):
        now = datetime.now()
        t1 = (now - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
        t2 = (now - timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
        rows = [
            'HK,src,%s +0000,%s +0000,80.0' % (t2, t2),
            'HK,src,%s +0000,%s +0000,60.0' % (t1, t1),
        ]
        path = self._write_csv(rows)
        result = health_query.read_csv(path, days=1)
        self.assertEqual(len(result), 2)
        self.assertLess(result[0]['_datetime'], result[1]['_datetime'])
        os.unlink(path)

    def test_read_handles_sep_line(self):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        rows = ['HK,src,%s +0000,%s +0000,99.0' % (now, now)]
        path = self._write_csv(rows)
        result = health_query.read_csv(path, days=1)
        self.assertEqual(len(result), 1)
        os.unlink(path)

    def test_read_handles_no_sep_line(self):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        fd, path = tempfile.mkstemp(suffix='.csv')
        with os.fdopen(fd, 'w', newline='') as f:
            f.write('type,sourceName,startDate,endDate,value\n')
            f.write('HK,src,%s +0000,%s +0000,42.0\n' % (now, now))
        result = health_query.read_csv(path, days=1)
        self.assertEqual(len(result), 1)
        os.unlink(path)

    def test_read_skips_invalid_dates(self):
        rows = ['HK,src,not-a-date,not-a-date,72.0']
        path = self._write_csv(rows)
        result = health_query.read_csv(path, days=365)
        self.assertEqual(len(result), 0)
        os.unlink(path)


class TestExtractValue(unittest.TestCase):
    """Tests for value extraction from CSV rows."""

    def test_value_column(self):
        self.assertEqual(health_query.extract_value({'value': '72.5'}), 72.5)

    def test_qty_column(self):
        self.assertEqual(health_query.extract_value({'qty': '100'}), 100.0)

    def test_quantity_column(self):
        self.assertEqual(health_query.extract_value({'quantity': '3.14'}), 3.14)

    def test_non_numeric(self):
        self.assertIsNone(health_query.extract_value({'value': 'stood'}))

    def test_empty_row(self):
        self.assertIsNone(health_query.extract_value({}))

    def test_none_value(self):
        self.assertIsNone(health_query.extract_value({'value': None}))


class TestGroupByDay(unittest.TestCase):
    """Tests for daily grouping."""

    def test_groups_correctly(self):
        now = datetime.now()
        rows = [
            {'_datetime': now.replace(hour=10), 'value': '60'},
            {'_datetime': now.replace(hour=14), 'value': '75'},
        ]
        result = health_query.group_by_day(rows)
        today = now.strftime('%Y-%m-%d')
        self.assertIn(today, result)
        self.assertEqual(len(result[today]), 2)

    def test_multiple_days(self):
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        rows = [
            {'_datetime': yesterday, 'value': '50'},
            {'_datetime': now, 'value': '60'},
        ]
        result = health_query.group_by_day(rows)
        self.assertEqual(len(result), 2)

    def test_skips_non_numeric(self):
        rows = [{'_datetime': datetime.now(), 'value': 'stood'}]
        result = health_query.group_by_day(rows)
        self.assertEqual(len(result), 0)

    def test_sorted_output(self):
        now = datetime.now()
        rows = [
            {'_datetime': now, 'value': '60'},
            {'_datetime': now - timedelta(days=2), 'value': '50'},
            {'_datetime': now - timedelta(days=1), 'value': '55'},
        ]
        result = health_query.group_by_day(rows)
        keys = list(result.keys())
        self.assertEqual(keys, sorted(keys))


class TestAnalyzeSleep(unittest.TestCase):
    """Tests for sleep analysis."""

    def _make_sleep_row(self, start_dt, end_dt, value):
        return {
            '_datetime': start_dt,
            'startDate': start_dt.strftime('%Y-%m-%d %H:%M:%S +0000'),
            'endDate': end_dt.strftime('%Y-%m-%d %H:%M:%S +0000'),
            'value': value,
        }

    def test_basic_sleep(self):
        start = datetime(2026, 3, 4, 23, 0)
        end = datetime(2026, 3, 5, 7, 0)
        rows = [self._make_sleep_row(start, end, 'HKCategoryValueSleepAnalysisAsleepCore')]
        result = health_query.analyze_sleep(rows)
        self.assertEqual(len(result), 1)
        night_data = list(result.values())[0]
        self.assertEqual(night_data['total_hours'], 8.0)

    def test_multiple_stages(self):
        base = datetime(2026, 3, 4, 23, 0)
        rows = [
            self._make_sleep_row(base, base + timedelta(hours=2), 'HKCategoryValueSleepAnalysisAsleepCore'),
            self._make_sleep_row(base + timedelta(hours=2), base + timedelta(hours=3), 'HKCategoryValueSleepAnalysisAsleepREM'),
            self._make_sleep_row(base + timedelta(hours=3), base + timedelta(hours=5), 'HKCategoryValueSleepAnalysisAsleepDeep'),
        ]
        result = health_query.analyze_sleep(rows)
        night_data = list(result.values())[0]
        self.assertEqual(night_data['total_hours'], 5.0)
        self.assertIn('AsleepCore', night_data['stages'])
        self.assertIn('AsleepREM', night_data['stages'])
        self.assertIn('AsleepDeep', night_data['stages'])

    def test_cross_midnight_grouping(self):
        """Sleep starting before midnight and ending after should be grouped as one night."""
        pre_midnight = datetime(2026, 3, 4, 23, 30)
        post_midnight = datetime(2026, 3, 5, 6, 30)
        rows = [self._make_sleep_row(pre_midnight, post_midnight, 'HKCategoryValueSleepAnalysisAsleepCore')]
        result = health_query.analyze_sleep(rows)
        self.assertEqual(len(result), 1)
        self.assertEqual(list(result.values())[0]['total_hours'], 7.0)

    def test_ignores_non_asleep(self):
        start = datetime(2026, 3, 4, 23, 0)
        end = datetime(2026, 3, 5, 7, 0)
        rows = [self._make_sleep_row(start, end, 'HKCategoryValueSleepAnalysisAwake')]
        result = health_query.analyze_sleep(rows)
        self.assertEqual(len(result), 0)

    def test_inbed_not_counted_as_asleep(self):
        """InBed should be parsed but not added to total sleep time."""
        start = datetime(2026, 3, 4, 22, 0)
        end = datetime(2026, 3, 5, 7, 0)
        rows = [self._make_sleep_row(start, end, 'HKCategoryValueSleepAnalysisInBed')]
        result = health_query.analyze_sleep(rows)
        self.assertEqual(len(result), 0)

    def test_empty_rows(self):
        result = health_query.analyze_sleep([])
        self.assertEqual(len(result), 0)


class TestFormatValue(unittest.TestCase):
    """Tests for value formatting."""

    def test_percentage_conversion(self):
        self.assertEqual(health_query.format_value(0.95, 'percentage'), 95.0)

    def test_percentage_already_converted(self):
        self.assertEqual(health_query.format_value(95.0, 'percentage'), 95.0)

    def test_rate_passthrough(self):
        self.assertEqual(health_query.format_value(72.0, 'rate'), 72.0)

    def test_cumulative_passthrough(self):
        self.assertEqual(health_query.format_value(1000, 'cumulative'), 1000)


class TestCmdListJson(unittest.TestCase):
    """Tests for list command JSON output."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.orig_data_dir = health_query.DATA_DIR
        health_query.DATA_DIR = Path(self.tmpdir)
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(os.path.join(self.tmpdir, 'HKQuantityTypeIdentifierHeartRate_2026.csv'), 'w') as f:
            f.write('sep=,\ntype,sourceName,startDate,endDate,value\n')
            f.write('HK,src,%s +0000,%s +0000,72\n' % (now, now))

    def tearDown(self):
        health_query.DATA_DIR = self.orig_data_dir
        import shutil
        shutil.rmtree(self.tmpdir)

    def test_list_json(self):
        captured = StringIO()
        with patch('sys.stdout', captured):
            health_query.cmd_list(as_json=True)
        data = json.loads(captured.getvalue())
        self.assertIsInstance(data, list)
        self.assertTrue(any(m['metric'] == 'HeartRate' for m in data))

    def test_list_text(self):
        captured = StringIO()
        with patch('sys.stdout', captured):
            health_query.cmd_list(as_json=False)
        output = captured.getvalue()
        self.assertIn('HeartRate', output)
        self.assertIn('Available', output)


class TestCmdQueryJson(unittest.TestCase):
    """Tests for query command JSON output."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.orig_data_dir = health_query.DATA_DIR
        health_query.DATA_DIR = Path(self.tmpdir)
        now = datetime.now()
        with open(os.path.join(self.tmpdir, 'HKQuantityTypeIdentifierHeartRate_2026.csv'), 'w') as f:
            f.write('sep=,\ntype,sourceName,startDate,endDate,unit,value\n')
            for h in range(5):
                t = (now - timedelta(hours=h)).strftime('%Y-%m-%d %H:%M:%S')
                f.write('HK,src,%s +0000,%s +0000,count/min,%d\n' % (t, t, 60 + h * 5))

    def tearDown(self):
        health_query.DATA_DIR = self.orig_data_dir
        import shutil
        shutil.rmtree(self.tmpdir)

    def test_query_json(self):
        captured = StringIO()
        with patch('sys.stdout', captured):
            health_query.cmd_query('HeartRate', days=7, as_json=True)
        data = json.loads(captured.getvalue())
        self.assertEqual(data['metric'], 'HeartRate')
        self.assertIn('data', data)

    def test_query_text(self):
        captured = StringIO()
        with patch('sys.stdout', captured):
            health_query.cmd_query('HeartRate', days=7, as_json=False)
        output = captured.getvalue()
        self.assertIn('HeartRate', output)

    def test_query_not_found(self):
        with self.assertRaises(SystemExit):
            health_query.cmd_query('NonExistent', days=7)


class TestCmdSummary(unittest.TestCase):
    """Tests for summary command."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.orig_data_dir = health_query.DATA_DIR
        health_query.DATA_DIR = Path(self.tmpdir)
        now = datetime.now()
        t = now.strftime('%Y-%m-%d %H:%M:%S')
        with open(os.path.join(self.tmpdir, 'HKQuantityTypeIdentifierStepCount_2026.csv'), 'w') as f:
            f.write('sep=,\ntype,sourceName,startDate,endDate,value\n')
            f.write('HK,src,%s +0000,%s +0000,500\n' % (t, t))
            f.write('HK,src,%s +0000,%s +0000,300\n' % (t, t))
        with open(os.path.join(self.tmpdir, 'HKQuantityTypeIdentifierOxygenSaturation_2026.csv'), 'w') as f:
            f.write('sep=,\ntype,sourceName,startDate,endDate,unit,value\n')
            f.write('HK,src,%s +0000,%s +0000,%%,0.97\n' % (t, t))

    def tearDown(self):
        health_query.DATA_DIR = self.orig_data_dir
        import shutil
        shutil.rmtree(self.tmpdir)

    def test_summary_json(self):
        captured = StringIO()
        with patch('sys.stdout', captured):
            health_query.cmd_summary(as_json=True)
        data = json.loads(captured.getvalue())
        self.assertIn('date', data)
        self.assertIn('StepCount', data['metrics'])
        self.assertEqual(data['metrics']['StepCount']['value'], 800)

    def test_summary_spo2_percentage(self):
        captured = StringIO()
        with patch('sys.stdout', captured):
            health_query.cmd_summary(as_json=True)
        data = json.loads(captured.getvalue())
        spo2 = data['metrics'].get('OxygenSaturation', {})
        self.assertGreater(spo2.get('value', 0), 90)

    def test_summary_text(self):
        captured = StringIO()
        with patch('sys.stdout', captured):
            health_query.cmd_summary(as_json=False)
        output = captured.getvalue()
        self.assertIn('Summary', output)
        self.assertIn('800', output)


class TestMetricsDefinition(unittest.TestCase):
    """Tests for METRICS dictionary completeness."""

    def test_all_metrics_have_three_fields(self):
        for key, val in health_query.METRICS.items():
            self.assertEqual(len(val), 3, f'{key} should have (name, unit, type)')

    def test_valid_metric_types(self):
        valid_types = {'rate', 'cumulative', 'percentage', 'sleep'}
        for key, (_, _, mtype) in health_query.METRICS.items():
            self.assertIn(mtype, valid_types, f'{key} has invalid type: {mtype}')

    def test_summary_metrics_exist(self):
        for key in health_query.SUMMARY_METRICS:
            self.assertIn(key, health_query.METRICS, f'{key} in SUMMARY_METRICS but not in METRICS')


class TestSleepQueryJson(unittest.TestCase):
    """Tests for sleep query with JSON output."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.orig_data_dir = health_query.DATA_DIR
        health_query.DATA_DIR = Path(self.tmpdir)
        start = datetime(2026, 3, 4, 23, 0)
        end = datetime(2026, 3, 5, 7, 0)
        with open(os.path.join(self.tmpdir, 'HKCategoryTypeIdentifierSleepAnalysis_2026.csv'), 'w') as f:
            f.write('sep=,\ntype,sourceName,startDate,endDate,value\n')
            f.write('HK,src,%s +0000,%s +0000,HKCategoryValueSleepAnalysisAsleepCore\n' % (
                start.strftime('%Y-%m-%d %H:%M:%S'), end.strftime('%Y-%m-%d %H:%M:%S')))

    def tearDown(self):
        health_query.DATA_DIR = self.orig_data_dir
        import shutil
        shutil.rmtree(self.tmpdir)

    def test_sleep_json(self):
        captured = StringIO()
        with patch('sys.stdout', captured):
            health_query.cmd_query('SleepAnalysis', days=30, as_json=True)
        data = json.loads(captured.getvalue())
        self.assertEqual(data['metric'], 'SleepAnalysis')
        self.assertIn('data', data)
        nights = data['data']
        self.assertTrue(len(nights) > 0)
        night_data = list(nights.values())[0]
        self.assertEqual(night_data['total_hours'], 8.0)


if __name__ == '__main__':
    unittest.main()
