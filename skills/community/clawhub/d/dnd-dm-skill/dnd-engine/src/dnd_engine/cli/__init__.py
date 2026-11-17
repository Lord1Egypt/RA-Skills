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


def _load_party(workspace):
    """读实时角色状态（优先工作区根的 live_party.json，再退 .dnd/）。"""
    import json
    for rel in ('live_party.json', os.path.join('.dnd', 'live_party.json')):
        path = os.path.join(workspace, rel)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f), path
    return None, None


def _find_actor(party, who):
    """按名字找人：先完全相等，再包含匹配。返回 (角色, 错误信息)。"""
    members = (party or {}).get('party') or []
    if not members:
        return None, 'live_party.json 里没有队伍成员'
    exact = [c for c in members if str(c.get('name')) == who]
    if exact:
        return exact[0], ''
    loose = [c for c in members if who and who in str(c.get('name'))]
    if len(loose) == 1:
        return loose[0], ''
    names = '、'.join(str(c.get('name')) for c in members)
    if len(loose) > 1:
        return None, f'「{who}」匹配到多人：{"、".join(str(c.get("name")) for c in loose)}'
    return None, f'队里找不到「{who}」。现有：{names}'


def cmd_check(args):
    """一次搞定一次检定：读角色卡 → 定技能/DC → 结算 → 直接输出可贴给玩家的明细。

    设计目标：把「LLM 写临时脚本调引擎」降成**一条命令**。
    """
    import json
    from dnd_engine.judge import DecisionPacket, render, resolve_packet
    from dnd_engine.judge import check_rules

    workspace = args.workspace or os.getcwd()
    party, party_path = _load_party(workspace)
    if party is None:
        print(f'{_WARN} 找不到 live_party.json（工作区：{workspace}）')
        return False

    sheet, err = _find_actor(party, args.actor) if args.actor else (None, '')
    if err:
        print(f'{_WARN} {err}')
        return False

    skill = args.skill or ''
    dc = args.dc
    band_source = 'cli'
    if args.action:
        looked = check_rules.lookup(args.action, skill)
        if not skill:
            skill = looked.get('skill') or ''
        if dc is None:
            dc = looked.get('dc')
        band_source = looked.get('source') or band_source

    if not skill and args.ac is None:
        print(f'{_WARN} 既没给 --skill 也没给 --action（或动作未命中规则表），无法定技能项')
        return False

    if skill:
        skill = check_rules.canonical_skill(skill)

    if dc is None and args.ac is None:
        dc = check_rules.band_dc('normal') or 15
        band_source = 'default'

    packet = DecisionPacket(
        requires_check=True,
        skill=skill,
        dc=int(dc or 0),
        dc_source=band_source,
        advantage=args.advantage or "普通",
        acting_character=str((sheet or {}).get('name') or args.actor or '冒险者'),
        intent=args.action or '',
    )

    extra = {}
    for item in (args.extra or []):
        if '=' in item:
            key, value = item.split('=', 1)
            try:
                extra[key.strip()] = int(value)
            except ValueError:
                print(f'{_WARN} 忽略无法解析的加值：{item}')
                return False

    if args.bonus is not None and sheet is not None:
        sheet = dict(sheet)
        bonuses = dict(sheet.get('skill_bonuses') or {})
        bonuses[skill] = int(args.bonus)
        sheet['skill_bonuses'] = bonuses

    outcome = resolve_packet(packet, sheet=sheet, d20=args.d20,
                             extra_components=extra or None,
                             target_ac=args.ac,
                             display_name=args.label or args.skill or "")
    packet.skill = skill

    if args.json:
        print(json.dumps({
            'actor': packet.acting_character,
            'skill': skill,
            'dc': packet.dc if args.ac is None else None,
            'ac': args.ac,
            'advantage': outcome.advantage,
            'd20': outcome.d20,
            'components': outcome.components,
            'hit': outcome.hit,
            'detail_lines': outcome.detail_lines,
            'summary_line': outcome.summary_line,
            'dc_source': band_source,
        }, ensure_ascii=False, indent=2))
    else:
        print(render(outcome))
        if args.debug:
            print(f'\n[debug] 角色：{packet.acting_character}（来自 {os.path.relpath(party_path, workspace)}）')
            print(f'[debug] 技能：{skill}  目标：{"AC " + str(args.ac) if args.ac is not None else "DC " + str(packet.dc)}  来源：{band_source}')
            print(f'[debug] 加值明细：{outcome.components}')
    return outcome.ran


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

    p = sub.add_parser('check', help='一次搞定一次检定：读 live_party.json → 结算 → 输出明细')
    p.add_argument('--actor', '-a', required=True, help='角色名（如 老白）')
    p.add_argument('--skill', '-s', default='', help='技能名（如 潜行；中文名/别名均可）')
    p.add_argument('--dc', type=int, default=None, help='DC（不给则查规则表/默认档）')
    p.add_argument('--ac', type=int, default=None, help='目标 AC（给了就走攻击检定）')
    p.add_argument('--advantage', default=None, choices=['优势', '劣势', '普通'], help='优/劣势')
    p.add_argument('--d20', type=int, default=None, help='固定 d20 骰面（不投骰，用于复现）')
    p.add_argument('--bonus', type=int, default=None, help='该技能的总加值（覆盖推导）')
    p.add_argument('--label', default='', help='展示用的技能名（默认用你输入的写法）')
    p.add_argument('--extra', action='append', default=[], help='额外加值，可重复：--extra 掩体=2')
    p.add_argument('--action', '-m', default='', help='行动原文（用于从规则表推断技能/DC）')
    p.add_argument('--workspace', '-w', default=None, help='工作区路径（默认 cwd）')
    p.add_argument('--json', action='store_true', help='输出 JSON')
    p.add_argument('--debug', action='store_true', help='加打角色/加值/来源')

    args = parser.parse_args()

    if args.command == 'init':
        sys.exit(0 if cmd_init(args.workspace) else 1)
    elif args.command == 'verify':
        cmd_verify(args.workspace)
    elif args.command == 'check':
        sys.exit(0 if cmd_check(args) else 1)
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
