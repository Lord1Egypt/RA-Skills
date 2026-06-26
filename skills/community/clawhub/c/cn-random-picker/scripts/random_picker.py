#!/usr/bin/env python3
import sys, json, random

def pick(items, count=1):
    items = items.split('\n') if '\n' in items else items.split(',')
    items = [i.strip() for i in items if i.strip()]
    if count >= len(items):
        random.shuffle(items)
        return {'picked': items, 'all': True}
    return {'picked': random.sample(items, count), 'all': False}

if __name__ == '__main__':
    items = sys.argv[1] if len(sys.argv)>1 else 'a,b,c,d,e'
    count = int(sys.argv[2]) if len(sys.argv)>2 else 1
    print(json.dumps(pick(items, count), ensure_ascii=False))
