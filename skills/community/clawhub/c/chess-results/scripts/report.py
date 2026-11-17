"""Match reports as transcribed from the paper Spielbericht: notation, names, config.

Nothing here touches the network. client.py talks to Chess-Results, match.py checks
and enters reports, server.py and cli.py expose them.

A report file holds one or more matches, written exactly as on the sheet:

    {"date": "2026-10-04", "matches": [
      {"division": "2. Klasse Nord", "round": 2,
       "home": {"team": "Musterdorf 2"}, "away": {"team": "Beispielstadt 1"}, "total": "1:3",
       "boards": [{"home": ["900101", "HUBER K."], "result": "1-0",
                   "away": ["", "Lang Eva"]},
                  {"home": null, "result": "--+", "away": ["900204", "Wolff"]}]}]}

A player is [ident, name as written]; an empty ident means the sheet has none and it
is to be looked up. null means nobody sat at that board (a no-show). Results are from
the home side: 1-0, 0-1, ½-½; forfeits +-- (1K-0K), --+ (0K-1K), --- (0K-0K); ? for a
result not known yet ("unbekannt").
"""
import json
import re
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

CONFIG_NAME = 'chess-results.json'

RESULTS = {'1-0': (1, 0), '0-1': (0, 1), '½-½': (.5, .5), '+--': (1, 0), '--+': (0, 1),
           '---': (0, 0), '?': (0, 0)}
FLIPPED_RESULT = {'1-0': '0-1', '0-1': '1-0', '½-½': '½-½', '+--': '--+', '--+': '+--',
                  '---': '---', '?': '?'}
ROMAN = {'i': '1', 'ii': '2', 'iii': '3', 'iv': '4', 'v': '5', 'vi': '6', 'vii': '7', 'viii': '8'}
# Words that say nothing about which club a team is. Sponsors go in the config.
GENERIC_WORDS = {'spgm', 'sgm', 'sg', 'sk', 'sc', 'sv', 'asv', 'askö', 'asko', 'schach', 'schachklub',
                 'schachverein', 'chess', 'club', 'verein', 'union'}


def find_config(start=None):
    """The club settings file: $CHESS_RESULTS_CONFIG, else chess-results.json in the
    working folder or one above it (the project), else ~/.config/chess-results/."""
    import os
    if os.environ.get('CHESS_RESULTS_CONFIG'):
        return Path(os.environ['CHESS_RESULTS_CONFIG'])
    here = Path(start or Path.cwd()).resolve()
    for folder in (here, *here.parents):
        if (folder / CONFIG_NAME).exists():
            return folder / CONFIG_NAME
    home = Path.home() / '.config/chess-results' / CONFIG_NAME
    return home if home.exists() else None


def load_config(path=None):
    """The club's settings. Without a file, only the public queries work."""
    path = Path(path) if path else find_config()
    cfg = json.loads(path.read_text(encoding='utf-8')) if path else {}
    cfg['_path'] = str(path) if path else None
    cfg.setdefault('ignore_words', [])
    cfg.setdefault('board_order_tolerance', None)
    cfg.setdefault('deadline', None)
    return cfg


def require_club(cfg):
    if not cfg.get('club'):
        raise ValueError(f'No club settings: create {CONFIG_NAME} in the project folder '
                         '(see SETUP.md; examples/chess-results.example.json is a template).')


def fold(text):
    """Lower case, accents dropped, ß as ss: "Müller" and "Muller" are one word."""
    bare = ''.join(c for c in unicodedata.normalize('NFD', text or '')
                   if unicodedata.category(c) != 'Mn')
    return bare.lower().replace('ß', 'ss')


def words(text):
    return [w for w in re.split(r'[^a-z]+', fold(text)) if w]


def normal_result(result):
    return (result or '').replace(' ', '').replace('1/2', '½')


def forfeit_problem(board):
    """Why a board's players and result do not fit together, or None.

    A no-show leaves the board empty and the opponent wins by forfeit, so an empty
    home board must be --+, an empty guest board +--, both empty ---."""
    home, away = board.get('home'), board.get('away')
    result = normal_result(board['result'])
    want = {(True, True): '---', (True, False): '--+', (False, True): '+--'}.get(
        (home is None, away is None))
    if want and result != want:
        side = 'both players' if want == '---' else (
            'the home player' if home is None else 'the guest player')
        return f'{side} did not turn up, so the result must be {want}, not {board["result"]}'
    return None


def score(match):
    """(home, away) points from the boards."""
    total = [0, 0]
    for b in match['boards']:
        h, a = RESULTS[normal_result(b['result'])]
        total[0] += h
        total[1] += a
    return tuple(total)


def score_text(points):
    return f'{points[0]:g}:{points[1]:g}'


def flipped(match):
    """The report with home and guest exchanged: teams, players, each result, total."""
    out = dict(match, home=match['away'], away=match['home'], boards=[])
    for b in match['boards']:
        out['boards'].append(dict(b, home=b['away'], away=b['home'],
                                  result=FLIPPED_RESULT[normal_result(b['result'])]))
    if match.get('total'):
        out['total'] = ':'.join(reversed(match['total'].replace(' ', '').split(':')))
    return out


def team_number(name):
    """The team's number, whether written 3, III or not at all (= 1)."""
    for w in reversed(re.findall(r'[a-z0-9]+', fold(name))):
        if w.isdigit():
            return w
        if w in ROMAN:
            return ROMAN[w]
    return '1'


def club_words(name, cfg=None):
    """The words of a team name that identify the club."""
    ignore = GENERIC_WORDS | {fold(w) for w in (cfg or {}).get('ignore_words', [])}
    return {w for w in re.findall(r'[a-z0-9]+', fold(name))
            if not w.isdigit() and w not in ROMAN and w not in ignore and len(w) > 2}


def is_ours(team, cfg):
    return fold(cfg['club']) in fold(team)


def name_fit(written, surname, given):
    """How well a handwritten name fits a register entry: ('ok' | 'spelling' |
    'mismatch', score).

    The surname carries the identification. Captains write it first or last, in
    capitals or not, with or without a first name or initial, and shorten double
    names to one part, so the best-matching written word is compared with each part.
    A written first name or initial must agree with the registered one."""
    tokens = [w for w in words(written) if len(w) > 1]
    parts = words(surname)
    if not tokens or not parts:
        return 'mismatch', 0.0
    ratio = max(SequenceMatcher(None, t, p).ratio() for t in tokens for p in parts)
    rest = [w for w in words(written)
            if max(SequenceMatcher(None, w, p).ratio() for p in parts) < 0.75]
    given_words = words(given)
    if rest and given_words and rest[0][0] != given_words[0][0]:
        return 'mismatch', ratio
    if ratio >= 0.95:
        return 'ok', ratio
    if ratio >= 0.75:
        return 'spelling', ratio
    return 'mismatch', ratio


def best_fit(written, people):
    """(person, ratio, unique): who the written name fits best among register entries
    ({'surname', 'given', …}). unique is False when a second fits nearly as well."""
    scored = sorted(((name_fit(written, p['surname'], p['given']), p) for p in people),
                    key=lambda x: -x[0][1])
    scored = [(f, p) for f, p in scored if f[0] != 'mismatch']
    if not scored:
        return None, 0.0, False
    (_, ratio), person = scored[0]
    unique = len(scored) == 1 or scored[1][0][1] < ratio - 0.05
    return person, ratio, unique


def board_order_warnings(team, players, tolerance):
    """Boards where a higher board is rated more than `tolerance` below a lower one.

    players: per board the member entry or None. The order is judged on the national
    rating; players without one are left out (a guest's FIDE rating is shown on the
    card but is not what the board order goes by)."""
    if tolerance is None:
        return []
    out = []
    for upper in range(len(players)):
        for lower in range(upper + 1, len(players)):
            a, b = players[upper], players[lower]
            if not a or not b or not a.get('national') or not b.get('national'):
                continue
            gap = b['national'] - a['national']
            if gap > tolerance:
                out.append(f'{team}: board {upper + 1} {a["surname"]} ({a["national"]}) plays above '
                           f'board {lower + 1} {b["surname"]} ({b["national"]}), {gap} points apart '
                           f'(more than the {tolerance} allowed)')
    return out
