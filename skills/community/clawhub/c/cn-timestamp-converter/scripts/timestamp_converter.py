#!/usr/bin/env python3
import sys, json, time
from datetime import datetime, timezone, timedelta

def convert(ts, is_millis=False):
    try:
        ts = int(ts)
        if is_millis or ts > 1e11:
            ts //= 1000
        dt = datetime.fromtimestamp(ts, timezone.utc)
        local = dt.astimezone()
        return {'unix': ts, 'utc': dt.isoformat(), 'local': local.strftime('%Y-%m-%d %H:%M:%S'), 'readable': local.strftime('%Y年%m月%d日 %H:%M:%S')}
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    print(json.dumps(convert(sys.argv[1] if len(sys.argv)>1 else str(int(time.time()))), ensure_ascii=False))
