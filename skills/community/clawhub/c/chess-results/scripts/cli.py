"""The chess-results tools from a terminal.

    python3 cli.py login                 # store the Chess-Results login (asks, hidden)
    python3 cli.py login --file [path]   # in a private file instead (no credential store)
    python3 cli.py logout                # remove it
    python3 cli.py status

    python3 cli.py players --last-name Huber [--federation AUT] [--date-from 2026-01-01]
    python3 cli.py player <tnr> <snr>   # player card: tournament number, player number
    python3 cli.py tournaments --name Landesliga --country AUT
    python3 cli.py tournament <tnr> [--art 3 --rd 2] [--details]
    python3 cli.py leagues 2026 [--prefix Bgld]

    python3 cli.py check report.json [--complete filled.json]
    python3 cli.py enter report.json     # check, then save the clean matches after a typed yes
    python3 cli.py enter report.json --yes   # no prompt: only once the user has approved

Queries print JSON. Run `login` yourself: it is the one command that handles the
password, and it never shows it.
"""
import argparse
import getpass
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import client
import credentials
from report import load_config, require_club


def show(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('login', help='store the Chess-Results login in the system credential store')
    p.add_argument('--file', nargs='?', const='', default=None, metavar='PATH',
                   help='write a private credentials file instead (default ~/.config/chess-results/'
                        'credentials.json), for machines without a credential store')
    sub.add_parser('logout', help='remove the stored login')
    sub.add_parser('status', help='what is configured; tries the login')
    p = sub.add_parser('players', help='search players')
    for field in client.PLAYER_FIELDS:
        p.add_argument('--' + field.replace('_', '-'))
    p.add_argument('--limit', type=int, default=50)
    p = sub.add_parser('player', help="a player's card in one tournament")
    p.add_argument('tnr', type=int)
    p.add_argument('snr', type=int)
    p = sub.add_parser('tournaments', help='search tournaments')
    for field in client.TOURNAMENT_FIELDS:
        p.add_argument('--' + field.replace('_', '-'))
    p.add_argument('--country')
    p.add_argument('--limit', type=int, default=50)
    p = sub.add_parser('tournament', help='a page of a tournament')
    p.add_argument('tnr', type=int)
    p.add_argument('--art', type=int)
    p.add_argument('--rd', type=int)
    p.add_argument('--snr', type=int)
    p.add_argument('--details', action='store_true')
    p = sub.add_parser('leagues', help='the leagues of an AUT championship season')
    p.add_argument('year', type=int)
    p.add_argument('--prefix')
    for name in ('check', 'enter'):
        p = sub.add_parser(name, help='check a match report' + (', then save it' if name == 'enter' else ''))
        p.add_argument('report')
        p.add_argument('--complete', help='write the report with every ident filled in')
        if name == 'enter':
            p.add_argument('--yes', action='store_true',
                           help='save without asking (only once the user has approved the checked results)')
    args = ap.parse_args()

    if args.cmd == 'login':
        to_file = args.file is not None
        target = (args.file or credentials.credentials_file()) if to_file else credentials.backend()
        print(f'Stored in: {target or "nowhere — use --file, install keyring, or use environment variables"}')
        pno = input('Chess-Results personal number: ').strip()
        password = getpass.getpass('Password (not shown): ')
        if not pno or not password:
            print('Both are needed; nothing stored.')
            return 1
        where = credentials.store_file(pno, password, args.file or None) if to_file else credentials.store(pno, password)
        s = client.session(load_config())
        try:
            print(f'Saved to the {where}. Chess-Results logs you on as: {client.login(s)}')
        except client.EntryError as e:
            print(f'Saved to the {where}, but the login did not work: {e}')
            return 1
        return 0
    if args.cmd == 'logout':
        credentials.forget()
        print('Stored Chess-Results login removed.')
        return 0

    cfg = load_config()
    s = client.session(cfg)
    try:
        if args.cmd == 'status':
            info = dict(credentials=credentials.status(), settings=cfg.get('_path'), club=cfg.get('club'))
            if info['credentials']['stored']:
                info['login'] = client.login(s)
            show(info)
        elif args.cmd == 'players':
            query = {k: getattr(args, k) for k in client.PLAYER_FIELDS if getattr(args, k)}
            show(client.search_players(s, limit=args.limit, **query))
        elif args.cmd == 'player':
            show(client.player_card(s, args.tnr, args.snr))
        elif args.cmd == 'tournaments':
            query = {k: getattr(args, k) for k in client.TOURNAMENT_FIELDS if getattr(args, k)}
            show(client.search_tournaments(s, country=args.country, limit=args.limit, **query))
        elif args.cmd == 'tournament':
            show(client.tournament(s, args.tnr, art=args.art, rd=args.rd, snr=args.snr, details=args.details))
        elif args.cmd == 'leagues':
            show(client.championship_leagues(s, args.year, args.prefix))
        elif args.cmd in ('check', 'enter'):
            import match
            require_club(cfg)
            print(f'Logged on as {client.login(s)}.')
            report = json.loads(Path(args.report).read_text(encoding='utf-8'))
            # Always check first, saving nothing.
            problems, completed = match.process(s, cfg, report, save=False)
            if args.cmd == 'enter':
                if problems:
                    print(f'\n{problems} problem(s): nothing saved.')
                    return 1
                # Saved results are public to the whole league, so saving needs an explicit
                # yes: typed at a terminal, or --yes for a caller that has already asked
                # the user (the command-line counterpart of confirm=true in the MCP tool).
                if not args.yes:
                    if not sys.stdin.isatty():
                        print('\nChecked and clean; not saved. Saving is public: re-run with --yes '
                              'once the user has approved the checked results.')
                        return 1
                    if input('\nSave these results on Chess-Results, visible to the whole league? '
                             'Type yes: ').strip().lower() != 'yes':
                        print('Not saved.')
                        return 1
                problems, completed = match.process(s, cfg, completed, save=True)
            if args.complete:
                Path(args.complete).write_text(json.dumps(completed, ensure_ascii=False, indent=1) + '\n',
                                               encoding='utf-8')
                print(f'\nReport with every ident filled in: {args.complete}')
            print(f'\n{problems} problem(s).' if problems else '\nAll matches clean.')
            return 1 if problems else 0
    except (client.EntryError, client.QueryError, credentials.CredentialError, ValueError) as e:
        print(f'error: {e}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
