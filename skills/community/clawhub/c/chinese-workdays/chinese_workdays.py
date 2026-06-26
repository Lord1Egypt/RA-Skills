#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chinese Workdays Calculator
Calculate legal working days between two dates based on Chinese government holiday schedules
"""

import yaml
import os
from datetime import datetime, date, timedelta
from typing import List, Dict, Tuple
from pathlib import Path

class ChineseWorkdays:
    """Calculate working days according to Chinese holiday schedules"""
    
    def __init__(self, data_dir: str = None):
        self.data_dir = data_dir or os.path.join(
            os.path.dirname(__file__), 
            "data"
        )
        self.holiday_schedules: Dict[int, Dict] = {}
        self._load_schedules()
    
    def _load_schedules(self):
        """Load all holiday schedule YAML files from data directory"""
        data_path = Path(self.data_dir)
        if not data_path.exists():
            os.makedirs(data_path, exist_ok=True)
            # Create example 2026 schedule
            self._create_example_schedule(2026)
        
        for yaml_file in data_path.glob("*.yaml"):
            with open(yaml_file, 'r', encoding='utf-8') as f:
                try:
                    schedule = yaml.safe_load(f)
                    if 'year' in schedule:
                        self.holiday_schedules[schedule['year']] = schedule
                except Exception as e:
                    print(f"Failed to load {yaml_file}: {e}")
    
    def _create_example_schedule(self, year: int):
        """Create an example holiday schedule for given year"""
        example = {
            'year': year,
            'holidays': [
                {
                    'name': '元旦',
                    'start': f'{year}-01-01',
                    'end': f'{year}-01-03',
                    'days_off': [f'{year}-01-01', f'{year}-01-02'],
                    'makeup_workdays': [f'{year}-12-28', f'{year}-01-04']  # previous year
                },
                {
                    'name': '春节',
                    'start': f'{year}-01-28',
                    'end': f'{year}-02-03',
                    'days_off': [
                        f'{year}-01-28', f'{year}-01-29', f'{year}-01-30',
                        f'{year}-01-31', f'{year}-02-01', f'{year}-02-02'
                    ],
                    'makeup_workdays': [f'{year}-01-25', f'{year}-02-04']
                },
                {
                    'name': '清明节',
                    'start': f'{year}-04-04',
                    'end': f'{year}-04-06',
                    'days_off': [f'{year}-04-04', f'{year}-04-05'],
                    'makeup_workdays': []
                },
                {
                    'name': '劳动节',
                    'start': f'{year}-05-01',
                    'end': f'{year}-05-05',
                    'days_off': [f'{year}-05-01', f'{year}-05-02'],
                    'makeup_workdays': [f'{year}-04-25', f'{year}-05-08']
                },
                {
                    'name': '端午节',
                    'start': f'{year}-05-31',
                    'end': f'{year}-06-02',
                    'days_off': [f'{year}-05-31', f'{year}-06-01'],
                    'makeup_workdays': []
                },
                {
                    'name': '中秋节',
                    'start': f'{year}-09-15',
                    'end': f'{year}-09-17',
                    'days_off': [f'{year}-09-15', f'{year}-09-16'],
                    'makeup_workdays': []
                },
                {
                    'name': '国庆节',
                    'start': f'{year}-10-01',
                    'end': f'{year}-10-07',
                    'days_off': [
                        f'{year}-10-01', f'{year}-10-02', f'{year}-10-03',
                        f'{year}-10-04', f'{year}-10-05', f'{year}-10-06', f'{year}-10-07'
                    ],
                    'makeup_workdays': [f'{year}-09-27', f'{year}-10-10']
                }
            ]
        }
        
        file_path = os.path.join(self.data_dir, f"{year}.yaml")
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(example, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        self.holiday_schedules[year] = example
    
    def _parse_date(self, d: str) -> date:
        """Parse date string to date object"""
        if isinstance(d, date):
            return d
        for fmt in ('%Y-%m-%d', '%Y年%m月%d日', '%Y/%m/%d'):
            try:
                return datetime.strptime(d, fmt).date()
            except ValueError:
                continue
        raise ValueError(f"Invalid date format: {d}")
    
    def _is_weekend(self, d: date) -> bool:
        """Check if date is weekend (Saturday=5, Sunday=6)"""
        return d.weekday() >= 5
    
    def _get_holiday_schedule(self, year: int) -> Dict:
        """Get holiday schedule for a specific year"""
        if year not in self.holiday_schedules:
            # Try to create example schedule
            self._create_example_schedule(year)
        return self.holiday_schedules.get(year, {})
    
    def _is_holiday_off(self, d: date, schedule: Dict) -> bool:
        """Check if date is a holiday day off"""
        for holiday in schedule.get('holidays', []):
            for day_off in holiday.get('days_off', []):
                if d == self._parse_date(day_off):
                    return True
        return False
    
    def _is_makeup_workday(self, d: date, schedule: Dict) -> bool:
        """Check if date is a makeup workday (调休补班)"""
        for holiday in schedule.get('holidays', []):
            for makeup in holiday.get('makeup_workdays', []):
                if d == self._parse_date(makeup):
                    return True
        return False
    
    def count_workdays(self, start_date, end_date) -> int:
        """
        Count working days between two dates (inclusive)
        
        Args:
            start_date: start date (string or date)
            end_date: end date (string or date)
        
        Returns:
            Number of working days
        """
        start = self._parse_date(start_date)
        end = self._parse_date(end_date)
        
        if start > end:
            start, end = end, start
        
        # Get schedules for all relevant years
        years = range(start.year, end.year + 1)
        schedules = {y: self._get_holiday_schedule(y) for y in years}
        
        workdays = 0
        current = start
        
        while current <= end:
            # Check if current day is a makeup workday first
            is_makeup = self._is_makeup_workday(current, schedules.get(current.year, {}))
            
            # Default: not a working day if weekend
            is_workday = not self._is_weekend(current)
            
            # If it's a holiday off, it's not a working day (unless makeup overrides)
            if self._is_holiday_off(current, schedules.get(current.year, {})):
                is_workday = False
            
            # Makeup workdays override everything
            if is_makeup:
                is_workday = True
            
            if is_workday:
                workdays += 1
            
            current += timedelta(days=1)
        
        return workdays
    
    def get_workdays_in_month(self, year: int, month: int) -> int:
        """Count working days in a specific month"""
        import calendar
        _, last_day = calendar.monthrange(year, month)
        start = date(year, month, 1)
        end = date(year, month, last_day)
        return self.count_workdays(start, end)
    
    def get_workdays_in_year(self, year: int) -> int:
        """Count working days in a whole year"""
        start = date(year, 1, 1)
        end = date(year, 12, 31)
        return self.count_workdays(start, end)
    
    def list_holidays(self, year: int = None) -> List[Dict]:
        """List all holidays for a year"""
        if year is None:
            year = datetime.now().year
        schedule = self._get_holiday_schedule(year)
        return schedule.get('holidays', [])

# Convenience function
def count_workdays(start_date, end_date) -> int:
    """
    Quick function to count workdays without creating instance
    
    Example:
        count_workdays("2026-01-01", "2026-12-31")
    """
    calculator = ChineseWorkdays()
    return calculator.count_workdays(start_date, end_date)

if __name__ == "__main__":
    # Quick test
    calc = ChineseWorkdays()
    
    # Example: Calculate Q1 2026 workdays
    q1_start = "2026-01-01"
    q1_end = "2026-03-31"
    workdays = calc.count_workdays(q1_start, q1_end)
    
    print(f"Working days in Q1 2026 ({q1_start} to {q1_end}): {workdays}")
    
    # Show all 2026 holidays
    print("\n2026 Holidays:")
    for h in calc.list_holidays(2026):
        print(f"  {h['name']}: {h['start']} to {h['end']}")