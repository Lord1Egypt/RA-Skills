#!/usr/bin/env python3
import sys, json

CRON_HELP = {
    'minute': '0-59',
    'hour': '0-23', 
    'day': '1-31',
    'month': '1-12',
    'weekday': '0-6'
}

def describe(cron):
    parts = cron.split()
    if len(parts) != 5:
        return {'error': '需要5个字段'}
    m, h, d, mo, w = parts
    return {'cron': cron, 'desc': f'每{m}分 {h}时 {d}日 {mo}月 周{w}'}

if __name__ == '__main__':
    print(json.dumps(describe(sys.argv[1] if len(sys.argv)>1 else '* * * * *'), ensure_ascii=False))
