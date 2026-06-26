"""
dnd-engine CLI

Usage:
    dnd-engine init [--workspace PATH]
    dnd-engine verify [--workspace PATH]
    dnd-engine server [--port auto] [--daemon]
"""

import os
import sys
import argparse

_OK = '+'
_WARN = '!'


def cmd_init(workspace):
    """Initialize workspace directory"""
    base = workspace or os.getcwd()
    results = []
    status = True

    def _mkdir(d, desc):
        nonlocal status
        try:
            os.makedirs(os.path.join(base, d), exist_ok=True)
            results.append(f'{_OK} {d}/  {desc}')
        except Exception as e:
            results.append(f'{_WARN} {d}/  failed: {e}')
            status = False

    # saves/
    _mkdir('saves', 'created')

    # modules/ + README
    try:
        os.makedirs(os.path.join(base, 'modules'), exist_ok=True)
        with open(os.path.join(base, 'modules', 'README.txt'), 'w', encoding='utf-8') as f:
            f.write('-- D&D modules --\nPlace your module files (.md / .json) here.\n')
        results.append(f'{_OK} modules/  created with README.txt')
    except Exception as e:
        results.append(f'{_WARN} modules/  failed: {e}')
        status = False

    # rules/ + README
    try:
        os.makedirs(os.path.join(base, 'rules'), exist_ok=True)
        with open(os.path.join(base, 'rules', 'README.txt'), 'w', encoding='utf-8') as f:
            f.write('-- D&D rulebooks --\nPlace your 2024 rulebooks (.md / .pdf) here.\n')
        results.append(f'{_OK} rules/  created with README.txt')
    except Exception as e:
        results.append(f'{_WARN} rules/  failed: {e}')
        status = False

    # live_party.json
    lpj = os.path.join(base, 'live_party.json')
    if not os.path.exists(lpj):
        try:
            with open(lpj, 'w', encoding='utf-8') as f:
                f.write('{"party":[],"version":1,"timestamp":"init"}')
            results.append(f'{_OK} live_party.json  template created')
        except Exception as e:
            results.append(f'{_WARN} live_party.json  failed: {e}')
            status = False

    # Check references/
    core_files = [
        'DM_RULES.md', 'DM_RULES_INDEX.md', 'DM_TEMPLATES.md',
        'DM_MAP_SYS.md', 'DM_DEV_GUIDE.md', 'CHAR_CREATION.md',
        'MODULE_ARC.md', 'MODULE_INDEX.md', 'ECHO_ARC.md',
        'SOUL.md', 'IDENTITY.md', 'AGENTS.md', 'TOOLS.md'
    ]
    ref_dir = os.path.join(base, 'references')
    if os.path.exists(ref_dir):
        found = sum(1 for f in core_files if os.path.exists(os.path.join(ref_dir, f)))
        if found == len(core_files):
            results.append(f'{_OK} references/  {found}/{len(core_files)} all present')
        else:
            results.append(f'{_WARN} references/  {found}/{len(core_files)} present, {len(core_files)-found} missing')
            status = False
    else:
        results.append(f'{_WARN} references/  directory not found (should be in zip)')

    # Check dnd-engine
    try:
        import dnd_engine
        v = getattr(dnd_engine, '__version__', '?')
        results.append(f'{_OK} dnd-engine {v}  installed')
    except ImportError:
        results.append(f'{_WARN} dnd-engine  not installed. Run: pip install dnd-engine')

    # Summary
    results.append(f'\nStatus: {"OK" if status else "INCOMPLETE"}')
    print('\n'.join(results))
    return status


def cmd_verify(workspace):
    """Run environment verification (direct engine call, no HTTP)"""
    from dnd_engine.verify import verify_environment
    data = verify_environment(workspace)
    
    print(f'Status:  {data["status"]}')
    print(f'Engine:  {data["engine"]["status"]} v{data["engine"]["version"]}')
    print(f'Refs:    {data["references"]["found"]}/{data["references"]["total"]} ({data["references"]["status"]})')
    print(f'Rules:   {_OK if data["rules"]["directory_exists"] else _WARN} ({data["rules"]["files_found"]} files)')
    print(f'Modules: {_OK if data["modules"]["directory_exists"] else _WARN} ({data["modules"]["files_found"]} files)')
    print(f'Writes:  {_OK if data["saves_writable"] else _WARN}')
    if data['actions']:
        print(f'\nPending:')
        for a in data['actions']:
            print(f'  - {a}')


def main():
    parser = argparse.ArgumentParser(description='dnd-engine - D&D 5e engine CLI')
    sub = parser.add_subparsers(dest='command')

    p = sub.add_parser('init', help='Initialize workspace (creates saves/ rules/ modules/)')
    p.add_argument('--workspace', '-w', default=None, help='Workspace path (default: cwd)')

    p = sub.add_parser('verify', help='Verify environment (requires API running)')
    p.add_argument('--workspace', '-w', default=None, help='Workspace path (default: cwd)')

    p = sub.add_parser('server', help='Start API server')
    p.add_argument('--port', default='8080', help='Port (auto=try 8080 then 8010-8020)')
    p.add_argument('--daemon', action='store_true', help='Run in background')
    p.add_argument('--host', default='127.0.0.1', help='Bind address')

    args = parser.parse_args()

    if args.command == 'init':
        sys.exit(0 if cmd_init(args.workspace) else 1)
    elif args.command == 'verify':
        cmd_verify(args.workspace)
    elif args.command == 'server':
        # Run server.py directly
        server_py = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'api', 'server.py')
        if os.path.exists(server_py):
            cmd = [sys.executable, server_py]
            cmd += ['--host', args.host]
            cmd += ['--port', args.port]
            if args.daemon:
                cmd.append('--daemon')
            os.execvp(sys.executable, cmd)
        else:
            print(f'Server not found at: {server_py}')
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
