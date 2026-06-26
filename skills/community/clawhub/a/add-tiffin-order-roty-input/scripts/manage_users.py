import json
import sys
import os

SKILL_DIR = os.path.dirname(os.path.dirname(__file__))
USERS_FILE = os.path.join(SKILL_DIR, 'data', 'allowed_users.json')


def load():
    with open(USERS_FILE,'r') as f:
        return json.load(f)


def save(d):
    with open(USERS_FILE,'w') as f:
        json.dump(d,f,indent=2)


def add_admin(uid):
    d = load()
    if 'admins' not in d:
        d['admins']=[]
    if uid in d['admins']:
        print('already admin')
        return
    d['admins'].append(uid)
    save(d)
    print('added admin', uid)


def add_vendor(uid):
    d = load()
    if 'vendors' not in d:
        d['vendors']=[]
    if uid in d['vendors']:
        print('already vendor')
        return
    d['vendors'].append(uid)
    save(d)
    print('added vendor', uid)


def list_users():
    d = load()
    print(json.dumps(d, indent=2))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: manage_users.py add-admin <id> | add-vendor <id> | list')
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == 'add-admin':
        add_admin(sys.argv[2])
    elif cmd == 'add-vendor':
        add_vendor(sys.argv[2])
    elif cmd == 'list':
        list_users()
    else:
        print('unknown')
