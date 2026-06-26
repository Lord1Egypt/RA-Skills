#!/usr/bin/env python3
import sys, json, re

def test_regex(pattern, text, mode='match'):
    try:
        if mode == 'match':
            matches = re.findall(pattern, text)
            return {'matches': matches, 'count': len(matches)}
        elif mode == 'replace':
            result = re.sub(pattern, '', text)
            return {'result': result}
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    p = sys.argv[1] if len(sys.argv)>1 else ''
    t = sys.argv[2] if len(sys.argv)>2 else ''
    print(json.dumps(test_regex(p, t), ensure_ascii=False))
