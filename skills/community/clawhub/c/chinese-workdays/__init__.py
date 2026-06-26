# Chinese Workdays Calculator
# Skill entry point for OpenClaw

from .chinese_workdays import ChineseWorkdays, count_workdays

__all__ = ['ChineseWorkdays', 'count_workdays']
__name__ = 'chinese_workdays'
__version__ = '1.0.0'

def main():
    """CLI interface for the skill"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python -m chinese_workdays <start_date> <end_date>")
        print("Example: python -m chinese_workdays 2026-01-01 2026-12-31")
        sys.exit(1)
    
    start = sys.argv[1]
    end = sys.argv[2] if len(sys.argv) > 2 else start
    
    workdays = count_workdays(start, end)
    print(f"Working days between {start} and {end}: {workdays}")

if __name__ == "__main__":
    main()