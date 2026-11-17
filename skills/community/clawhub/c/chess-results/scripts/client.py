"""A client for Chess-Results: public queries, and the team-championship result entry.

Chess-Results has no API. It is ASP.NET WebForms: pages are read with GETs
(tnr<N>.aspx?art=…), forms are POSTed back with their hidden state (__VIEWSTATE,
__EVENTVALIDATION), and links like "Ändern" are __doPostBack events.

Learned the hard way:

* The User-Agent must start with "Mozilla/5.0". ASP.NET's browser detection treats an
  unknown agent as having no JavaScript and silently ignores __doPostBack events.
* Chess-Results throttles bursts with connection resets and 503s. Requests are spaced
  (PoliteSession), retried with back-off, and public pages are cached.
* Login is only needed for the result editor. Overviews, team compositions, player
  cards and the searches are public.

The login comes from credentials.py (the system credential store), never a file.
"""
import hashlib
import json
import os
import re
import time as clock
from datetime import date, datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import requests
from bs4 import BeautifulSoup

import credentials
from report import club_words, flipped, fold, is_ours, normal_result, team_number

BASE = 'https://chess-results.com/'
SEARCH_BASE = 'https://s1.chess-results.com/'
LOGIN = BASE + 'Login.aspx?xx=0'
CHAMPIONSHIP = BASE + 'meisterschaft.aspx?lan=1&jahr={year}'
CACHE = Path(os.environ.get('CLAUDE_PLUGIN_DATA') or Path.home() / '.cache/chess-results') / 'pages'

# combo_Erg on the entry form: 0 Kein, 1 1-0, 2 Remis, 3 0-1, 4 1K-0K, 5 0K-1K,
# 6 0K-0K, 7 unbekannt.
RESULT_CODES = {'1-0': '1', '½-½': '2', '0-1': '3', '+--': '4', '--+': '5', '---': '6', '?': '7'}
# How the overview prints a saved board result, back in report notation.
RESULT_LABELS = {'1-0': '1-0', '½-½': '½-½', '0-1': '0-1', 'remis': '½-½', '1k-0k': '+--',
                 '0k-1k': '--+', '0k-0k': '---', 'unbekannt': '?', '+-': '+--', '-+': '--+',
                 '--': '---'}
NOBODY = 'nicht besetzt'


class EntryError(SystemExit):
    pass


class PoliteSession(requests.Session):
    """At most one request every PAUSE seconds: Chess-Results throttles bursts with
    connection resets and 503s, and a results run needs only a few dozen pages."""
    PAUSE = 0.6

    def request(self, *args, **kwargs):
        wait = getattr(self, '_last', 0) + self.PAUSE - clock.monotonic()
        if wait > 0:
            clock.sleep(wait)
        try:
            return super().request(*args, **kwargs)
        finally:
            self._last = clock.monotonic()


def session(cfg):
    """A session that identifies itself and retries politely: Chess-Results drops
    connections when asked too much too fast, so failed requests are retried with a
    growing pause instead of hammering it."""
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    s = PoliteSession()
    s.headers['User-Agent'] = f"Mozilla/5.0 (compatible; {cfg.get('user_agent', 'chess-results-skill/1.0')})"
    retry = Retry(total=4, connect=4, read=4, backoff_factor=1.5,
                  status_forcelist=(429, 500, 502, 503, 504), allowed_methods=frozenset({'GET'}))
    s.mount('https://', HTTPAdapter(max_retries=retry))
    return s


# ---------------------------------------------------------------- login

def hidden_state(html):
    soup = BeautifulSoup(html, 'html.parser')
    return {i['name']: i.get('value', '') for i in soup.select('input[type=hidden][name]')}


def logged_on_as(html):
    m = re.search(r'Logged on:\s*([^<\n]+)|Angemeldet:\s*([^<\n]+)', html)
    return (m.group(1) or m.group(2)).strip() if m else None


def login(s):
    page = s.get(LOGIN, timeout=30)
    page.raise_for_status()
    try:
        pno, password = credentials.load()
    except credentials.CredentialError as e:
        raise EntryError(str(e))
    form = hidden_state(page.text)
    form.update({'ctl00$P1$txt_user': pno, 'ctl00$P1$txt_kennwort': password,
                 'ctl00$P1$cb_anmelden': 'Login'})
    done = s.post(LOGIN, data=form, timeout=30)
    done.raise_for_status()
    who = logged_on_as(done.text)
    if not who or who.lower() in ('gast', 'guest'):
        raise EntryError('Login failed: Chess-Results still shows a guest session. '
                         'Check the stored login (cli.py login to replace it).')
    return who


def postback(s, url, html, **fields):
    form = hidden_state(html)
    form['ctl00$P1$G1'] = 'rb_eingabe_pnr'
    form.update(fields)
    r = s.post(url, data=form, timeout=30)
    r.raise_for_status()
    return r


# ---------------------------------------------------------------- the entry window

def deadline(day, cfg):
    """When online entry closes, from the config: the given time on the first working
    day after the match (Saturday and Sunday skipped, public holidays not). None when
    the config sets no deadline."""
    rule = cfg.get('deadline')
    if not rule:
        return None
    zone = ZoneInfo(rule.get('timezone', 'Europe/Vienna'))
    nxt = day + timedelta(days=1)
    while nxt.weekday() >= 5:
        nxt += timedelta(days=1)
    hh, mm = (int(x) for x in rule.get('time', '12:00').split(':'))
    return datetime.combine(nxt, time(hh, mm), zone)


def check_window(day, cfg, now=None):
    """None when results for that date may be entered now, else the reason not."""
    zone = ZoneInfo((cfg.get('deadline') or {}).get('timezone', 'Europe/Vienna'))
    now = now or datetime.now(zone)
    if day > now.date():
        return f'the match date {day:%d.%m.%Y} is in the future'
    due = deadline(day, cfg)
    if due and now > due:
        return (f'the deadline for {day:%d.%m.%Y} was {due:%a %d.%m. %H:%M}; '
                "a late result has to go to the league's organiser")
    return None


# ---------------------------------------------------------------- tournaments and pairings

def entry_url(tnr):
    return f'{BASE}EingabeMeisterschaft.aspx?lan=1&tnr={tnr}'


def season_of(day):
    return day.year if day.month >= 7 else day.year - 1


def tournaments(s, day, cfg):
    """(name, tnr) of the leagues to search: the configured numbers, and/or every
    league on the AUT championship overview whose name starts with the prefix."""
    spec = cfg.get('tournaments', {})
    out = [(f'tnr {n}', str(n)) for n in spec.get('numbers', [])]
    prefix = (spec.get('championship') or {}).get('prefix')
    if prefix:
        year = season_of(day)
        soup = BeautifulSoup(s.get(CHAMPIONSHIP.format(year=year), timeout=30).text, 'html.parser')
        for tr in soup.find_all('tr'):
            if tr.find('tr'):
                continue
            a = tr.find('a', href=re.compile(r'tnr\d+'))
            if a and a.get_text(strip=True).startswith(prefix):
                out.append((a.get_text(strip=True), re.search(r'tnr(\d+)', a['href']).group(1)))
    if not out:
        raise EntryError('No tournaments to search: set "tournaments" in club.json.')
    return out


def pairings(html):
    """The round an entry page offers: its date and every pairing on it."""
    soup = BeautifulSoup(html, 'html.parser')
    grid = soup.find(id='P1_GridView1')
    if not grid:
        return None, []
    m = re.search(r'(\d{2})\.(\d{2})\.(\d{4})', grid.get_text(' '))
    day = date(int(m.group(3)), int(m.group(2)), int(m.group(1))) if m else None
    rows = []
    for tr in grid.find_all('tr'):
        cells = [td.get_text(' ', strip=True) for td in tr.find_all('td')]
        link = tr.find('a', string=re.compile('ndern'))
        if len(cells) >= 5 and link:
            target = re.search(r"__doPostBack\('([^']+)'", link['href']).group(1)
            rows.append(dict(home=cells[2], away=cells[3], score=cells[4], target=target))
    return day, rows


class Pages:
    """The entry pages of the season's leagues, fetched once per run."""

    def __init__(self, s, cfg):
        self.s, self.cfg, self.leagues, self.pages = s, cfg, {}, {}

    def league_list(self, day):
        season = season_of(day)
        if season not in self.leagues:
            self.leagues[season] = tournaments(self.s, day, self.cfg)
        return self.leagues[season]

    def page(self, tnr, fresh=False):
        if fresh or tnr not in self.pages:
            r = self.s.get(entry_url(tnr), timeout=30)
            self.pages[tnr] = (r.url, r.text, *pairings(r.text))
        return self.pages[tnr]


def find_pairing(pages, match, day):
    """League, entry page and pairing of a report, found by date and our team.

    The round must be dated on the match day and contain our team with the report's
    number. Chess-Results decides who is at home: a sheet written the wrong way round
    is turned around (`swapped`). The opponent's name then has to share a word with
    the listed opponent — a check, not the key, since sheets abbreviate."""
    cfg = pages.cfg
    ours = 'home' if is_ours(match['home']['team'], cfg) else 'away'
    if not is_ours(match[ours]['team'], cfg):
        raise EntryError(f'Neither {match["home"]["team"]} nor {match["away"]["team"]} '
                         f'is a {cfg["club"]} team.')
    number = team_number(match[ours]['team'])
    found, offered = [], set()
    for name, tnr in pages.league_list(day):
        url, html, round_day, rows = pages.page(tnr)
        if round_day:
            offered.add(round_day)
        if round_day != day:
            continue
        for row in rows:
            for side in ('home', 'away'):
                if is_ours(row[side], cfg) and team_number(row[side]) == number:
                    found.append((name, tnr, row, side != ours))
    if not found:
        raise EntryError(f'No {match[ours]["team"]} pairing in a round dated {day}. The entry '
                         f'pages only offer the round currently open: '
                         f'{", ".join(sorted(map(str, offered))) or "none"}.')
    if len(found) > 1:
        raise EntryError(f'{match[ours]["team"]} appears in more than one pairing on {day}: '
                         + ', '.join(f'{f[2]["home"]} – {f[2]["away"]} ({f[0]})' for f in found))
    name, tnr, row, swapped = found[0]
    report = flipped(match) if swapped else match
    theirs = 'away' if (ours == 'home') != swapped else 'home'
    if not club_words(report[theirs]['team'], cfg) & club_words(row[theirs], cfg):
        raise EntryError(f'On {day} {row["home"]} – {row["away"]} is the {name} pairing, '
                         f'but the sheet names {report[theirs]["team"]} as the opponent.')
    return name, tnr, row, report, swapped


# ---------------------------------------------------------------- the editor

def open_editor(s, url, html, row):
    """Press "Ändern" on the pairing."""
    editor = postback(s, url, html, __EVENTTARGET=row['target'], __EVENTARGUMENT='')
    if 'cb_save' not in editor.text:
        raise EntryError(f'The editor for {row["home"]} – {row["away"]} did not open. '
                         'Is the login allowed to enter results for this league?')
    return editor


def parse_members(html):
    """A club's members at the round date, as "Spieler Team x anzeigen" lists them."""
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find(id='P1_GridView4')
    if not table:
        return []
    rows = table.find_all('tr')
    head = [c.get_text(strip=True) for c in rows[0].find_all(['th', 'td'])]
    out = []
    for tr in rows[1:]:
        cell = dict(zip(head, (c.get_text(' ', strip=True) for c in tr.find_all('td'))))
        if not cell.get('PNr', '').isdigit():
            continue
        elo, elo_i = cell.get('Elo', '0'), cell.get('EloI', '0')
        rating = int(elo) if elo.isdigit() and elo != '0' else (
            int(elo_i) if elo_i.isdigit() and elo_i != '0' else 0)
        out.append(dict(ident=cell['PNr'], surname=cell.get('Nachname', ''),
                        given=cell.get('Vorname', ''), rating=rating,
                        national=int(elo) if elo.isdigit() else 0,
                        fide=cell.get('FideNr') if cell.get('FideNr') not in ('', '0') else None,
                        club=cell.get('Verein', ''), kind=cell.get('Art', '')))
    return out


def members(s, url, editor_html):
    """Both clubs' member lists at the round date: (home club, guest club)."""
    lists = []
    for button, label in (('ctl00$P1$cb_team1', 'Spieler Team1 anzeigen'),
                          ('ctl00$P1$cb_team2', 'Spieler Team2 anzeigen')):
        lists.append(parse_members(postback(s, url, editor_html, **{button: label}).text))
    return tuple(lists)


def board_rows(html):
    return re.findall(r'name="(ctl00\$P1\$GridView2\$ctl\d+)\$txt_PNr1"', html)


def filled(rows, boards):
    """The editor's fields for a report: an empty number for a board nobody sat at."""
    if len(boards) > len(rows):
        raise EntryError(f'The report has {len(boards)} boards, the form {len(rows)}.')
    fields = {}
    for row, board in zip(rows, boards):
        fields[f'{row}$txt_PNr1'] = board['home'][0] if board['home'] else ''
        fields[f'{row}$txt_PNr2'] = board['away'][0] if board['away'] else ''
        fields[f'{row}$combo_Erg'] = RESULT_CODES[normal_result(board['result'])]
    return fields


def resolved(html):
    """Per board the names Chess-Results shows after "Eingabe Prüfen", and its score.

    Read by the labels' ids — row 1 is the team header (l_erg_1 the score), rows 2…
    the boards — because an unknown number shows "nicht in Meldekartei" where the
    name would be, and positions among the names would shift."""
    soup = BeautifulSoup(html, 'html.parser')

    def label(kind, n):
        el = soup.find(id=f'P1_GridView2_l_{kind}_{n}')
        return re.sub(r'\s+', ' ', el.get_text(' ', strip=True)) if el else ''

    score = label('erg', 1).replace(' ', '').replace('-', ':') or None
    boards, n = [], 2
    while soup.find(id=f'P1_GridView2_l_Br_{n}'):
        boards.append(dict(home=label('Name1', n), away=label('Name2', n)))
        n += 1
    return boards, score


def messages(html):
    """What the site says after a check: (errors, notices). P_Error holds errors
    ("Die Personennummer … ist nicht in der Meldekartei"), P_Info and P_ImpMessage
    notices ("Der Spieler … war am … nicht Mitglied bei Verein …"), one <h5> each."""
    soup = BeautifulSoup(html, 'html.parser')

    def lines(box):
        el = soup.find(id=box)
        if not el:
            return []
        items = [h.get_text(' ', strip=True) for h in el.find_all('h5')]
        return [t for t in (items or [el.get_text(' ', strip=True)]) if t]
    return lines('P_Error'), lines('P_Info') + lines('P_ImpMessage')


# ---------------------------------------------------------------- public pages

def parse_compositions(html):
    """Team -> [{name, fide, card}] from a league's Team-Composition page (art=8):
    everyone who has played for each team so far."""
    soup = BeautifulSoup(html, 'html.parser')
    teams, team = {}, None
    for table in soup.select('table.CRs1'):
        for tr in table.find_all('tr'):
            head = tr.find('td', attrs={'colspan': True})
            if head:
                m = re.match(r'\s*\d+\.\s*(.*?)\s*\(RtgAvg', head.get_text(' ', strip=True))
                team = m.group(1) if m else None
                if team:
                    teams[team] = []
                continue
            cells = tr.find_all('td')
            if team and len(cells) >= 7 and cells[0].get_text(strip=True).isdigit():
                link = cells[2].find('a', href=True)
                fide = cells[6].get_text(strip=True)
                teams[team].append(dict(name=cells[2].get_text(' ', strip=True),
                                        fide=fide if fide not in ('', '0') else None,
                                        card=link['href'] if link else None))
    return teams


class Rosters:
    """Team compositions per league (art=8): who has played for each team so far.

    The compositions carry names and FIDE ids but no national idents; those come from
    matching each entry to the club's member list (FIDE id first, then the name),
    which the editor provides anyway. No player cards are fetched."""

    def __init__(self, s):
        self.s, self.teams = s, {}

    def league(self, tnr):
        if tnr not in self.teams:
            html = self.s.get(f'{BASE}tnr{tnr}.aspx?lan=1&art=8', timeout=30).text
            self.teams[tnr] = parse_compositions(html)
        return self.teams[tnr]

    def idents(self, tnr, team, people):
        """The idents of everyone who has played for that team, among `people`."""
        out = set()
        for entry in self.league(tnr).get(team, []):
            hit = next((m for m in people if entry['fide'] and m.get('fide') == entry['fide']), None)
            if not hit:
                surname, _, given = entry['name'].partition(',')
                first = (fold(given).split() or [''])[0]
                hit = next((m for m in people if fold(m['surname']) == fold(surname.strip())
                            and (fold(m['given']).split() or [''])[0] == first), None)
            if hit:
                out.add(hit['ident'])
        return out


def saved_pairings(html):
    """Every pairing in the overview's board list, with what has been saved:
    [{home, away, score, boards: [{home, away, result}]}], a player being
    {ident, name, title, rating} or None for an empty board."""
    soup = BeautifulSoup(html, 'html.parser')

    def label(kind, n):
        el = soup.find(id=f'P1_GridView2_l_{kind}_{n}')
        return re.sub(r'\s+', ' ', el.get_text(' ', strip=True)) if el else ''

    out, n = [], 1
    while soup.find(id=f'P1_GridView2_l_Br_{n}'):
        if label('elo1', n) == 'Elo':
            out.append(dict(home=label('Name1', n), away=label('Name2', n),
                            score=label('erg', n), boards=[]))
        elif out:
            def player(side):
                ident, name = label(f'Pnr{side}', n), label(f'Name{side}', n)
                if not ident.strip('0') or NOBODY in fold(name):
                    return None
                elo = label(f'elo{side}', n)
                return dict(ident=ident, name=name, title=label(f'Mnr{side}', n),
                            rating=int(elo) if elo.isdigit() and elo != '0' else None)
            raw = fold(label('erg', n)).replace(' ', '')
            out[-1]['boards'].append(dict(home=player(1), away=player(2),
                                          result=RESULT_LABELS.get(raw)))
        n += 1
    return out


# ---------------------------------------------------------------- public queries

class QueryError(Exception):
    pass


def text_of(el):
    return ' '.join(el.get_text(' ', strip=True).split())


DATE = re.compile(r'(\d{4})/(\d{2})/(\d{2})')


def iso_date(text):
    """'2026/09/20' as Chess-Results prints it -> '2026-09-20'; anything else unchanged."""
    m = DATE.fullmatch((text or '').strip())
    return f'{m.group(1)}-{m.group(2)}-{m.group(3)}' if m else text


def number(text):
    """'10' -> 10; '-', '' and anything not a whole number -> None."""
    text = (text or '').strip()
    return int(text) if text.isdigit() else None


AGO = re.compile(r'(\d+)\s*(Year|Month|Week|Day|Hour|Min|Sec)', re.I)
AGO_UNITS = dict(year=365 * 86400, month=30 * 86400, week=7 * 86400, day=86400, hour=3600, min=60, sec=1)


def ago_to_timestamp(text, now=None):
    """'19 Hours 24 Min.' (Chess-Results' "last update") -> the ISO time it stands for,
    counted back from `now`, to the minute. None if the text is not a duration."""
    parts = AGO.findall(text or '')
    if not parts:
        return None
    seconds = sum(int(n) * AGO_UNITS[unit.lower()] for n, unit in parts)
    now = now or datetime.now(ZoneInfo('UTC'))
    return (now - timedelta(seconds=seconds)).replace(second=0, microsecond=0).isoformat().replace('+00:00', 'Z')


def when(text):
    """'Round 2 on 2026/10/04 at 09:00' -> '2026-10-04T09:00' (or just the date)."""
    m = re.search(r'(\d{4})/(\d{2})/(\d{2})(?:\s+at\s+(\d{1,2}:\d{2}))?', text or '')
    if not m:
        return None
    day = f'{m.group(1)}-{m.group(2)}-{m.group(3)}'
    return f'{day}T{int(m.group(4).split(":")[0]):02d}:{m.group(4).split(":")[1]}' if m.group(4) else day


def cached_get(s, url, ttl):
    """A public page, from the local cache when younger than `ttl` seconds."""
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / (hashlib.sha256(url.encode()).hexdigest() + '.html')
    if ttl and path.exists() and clock.time() - path.stat().st_mtime < ttl:
        return path.read_text(encoding='utf-8')
    r = s.get(url, timeout=30)
    r.raise_for_status()
    path.write_text(r.text, encoding='utf-8')
    return r.text


def form_of(html):
    """A WebForms form's current values: hidden state, text fields, selected options."""
    soup = BeautifulSoup(html, 'html.parser')
    form = soup.select_one('form')
    if form is None:
        raise QueryError('No form on the page; the site may have changed.')
    data = {el['name']: el.get('value', '') for el in form.select('input[name]')
            if el.get('type', 'text') not in ('submit', 'checkbox', 'radio')}
    for el in form.select('select[name]'):
        choice = el.select_one('option[selected]') or el.select_one('option')
        if choice:
            data[el['name']] = choice.get('value', '')
    return data


BOARD_HEADER = ['Bo.', 'Title', 'Name', 'Rtg', '-', 'Title 2', 'Name 2', 'Rtg 2', 'Res.']
SCORE = re.compile(r'\d(?:[,.]5|½)?\s*:\s*\d|½\s*:')


def unique_names(names):
    """Column names made unique: a schedule has "Team, Team, Res., :, Res." — the second
    of each becomes "Team 2", "Res. 2", so no column overwrites another."""
    seen, out = {}, []
    for name in names:
        seen[name] = seen.get(name, 0) + 1
        out.append(name if seen[name] == 1 or not name else f'{name} {seen[name]}')
    return out


def tables(html):
    """Every result table on a page (class CRs1/CRs2) as {header, rows}.

    A row spanning the table ("Round 2 on 2026/10/04 at 09:00", "1. Musterdorf 2
    (RtgAvg …)") is kept as {'section': text}, with `date` when it names one. The
    header is the first row marked <th>/CRg1b, or the first row at all after any
    section headings (the player search marks nothing). A two-cell row is a key/value
    pair (the player card), never a header. Columns without a name (flags) are
    dropped, dates become ISO, and a row's tournament link is kept as "_link"."""
    soup = BeautifulSoup(html, 'html.parser')
    out = []
    for t in soup.select('table.CRs1, table.CRs2'):
        header, raw_header, rows = None, None, []
        for tr in t.find_all('tr', recursive=False) or t.find_all('tr'):
            cells = tr.find_all(['td', 'th'], recursive=False)
            if len(cells) == 1 and cells[0].get('colspan'):
                section = {'section': text_of(cells[0])}
                if when(section['section']):
                    section['date'] = when(section['section'])
                rows.append(section)
                continue
            values = [iso_date(text_of(c)) for c in cells]
            # A team round page (art=3) heads each match with its own row: "Bo. | 6 |
            # Westdorf 1 | Rtg | - | 4 | Ostdorf 1 | Rtg | 1 : 5". That is a heading, not
            # the column header; the boards under it get neutral column names.
            if len(values) == len(BOARD_HEADER) and values[0] == 'Bo.' and SCORE.search(values[-1]):
                rows.append({'section': f'{values[2]} – {values[6]} {values[-1]}',
                             'home': values[2], 'away': values[6], 'score': values[-1]})
                header, raw_header = BOARD_HEADER, None
                continue
            only_sections = all('section' in r for r in rows)
            if header is None and only_sections and (tr.find('th') or 'CRg1b' in (tr.get('class') or [])
                                                     or len(values) > 2):
                raw_header, header = values, unique_names(values)
                continue
            if header and values == raw_header:
                continue        # the header again, under the next round's heading
            link = next((a['href'] for a in tr.find_all('a', href=True) if 'tnr' in a['href']), None)
            if header and len(header) == len(values):
                row = {k: v for k, v in zip(header, values) if k}
            else:
                row = {'cells': values}
            if link:
                row['_link'] = link
            rows.append(row)
        if rows:
            out.append(dict(header=[h for h in header if h] if header else None, rows=rows))
    return out


def title_of(html):
    soup = BeautifulSoup(html, 'html.parser')
    h = soup.find('h2') or soup.find('title')
    return text_of(h) if h else None


# Player search (SpielerSuche): the form's own field names.
PLAYER_FIELDS = dict(last_name='txt_nachname', first_name='txt_vorname', club='txt_verein',
                     ident='txt_ident', fide_id='txt_fideID', federation='txt_FED',
                     birth_year='txt_GJahr', min_rating='txt_min_elo',
                     tournament_federation='txt_Fed_tur', date_from='txt_von_tag', date_to='txt_bis_tag')


def search_players(s, limit=50, **query):
    """Tournament appearances of players matching the query, grouped per player.

    Chess-Results needs a surname, ident, FIDE id or federation. The search shows
    appearances in tournaments, not a membership register; a group is one FIDE id,
    else one federation ident, else (unverified) one name."""
    unknown = set(query) - set(PLAYER_FIELDS)
    if unknown:
        raise QueryError(f'Unknown search field: {sorted(unknown)[0]}')
    query = {k: str(v).strip() for k, v in query.items() if v not in (None, '')}
    if not any(query.get(k) for k in ('last_name', 'ident', 'fide_id', 'federation')):
        raise QueryError('Give a last_name, ident, fide_id or federation.')
    # The site ignores a date range with only one end, so the other is filled in.
    if query.get('date_from') or query.get('date_to'):
        query.setdefault('date_from', '1990-01-01')
        query.setdefault('date_to', f'{date.today().year + 1}-12-31')
    url = SEARCH_BASE + 'SpielerSuche.aspx?lan=1'
    data = form_of(s.get(url, timeout=30).text)
    for key, field in PLAYER_FIELDS.items():
        data['ctl00$P1$' + field] = query.get(key, '')
    data.update({'ctl00$P1$combo_anzahl_zeilen': '1', 'ctl00$P1$cb_suchen': 'Search'})
    html = s.post(url, data=data, timeout=30).text
    found = next((t for t in tables(html) if t['header'] and t['header'][:2] == ['Name', 'ID']), None)
    groups = {}
    for row in (found or {}).get('rows', []):
        if 'Name' not in row:
            continue
        fide, ident, fed = row.get('FideID', '').strip('0') and row['FideID'], row.get('ID', ''), row.get('FED', '')
        key = f'fide:{fide}' if fide else (f'ident:{fed}:{ident}' if ident.strip('0') else f'name:{fold(row["Name"])}:{fed}')
        g = groups.setdefault(key, dict(name=row['Name'], fideId=fide or None,
                                        ident=ident if ident.strip('0') else None, federation=fed or None,
                                        clubs=[], appearances=[], grouping=key.split(':')[0]))
        if row.get('Club/City') and row['Club/City'] not in g['clubs']:
            g['clubs'].append(row['Club/City'])
        m = re.search(r'tnr(\d+)\.aspx.*snr=(\d+)', row.get('_link', ''))
        g['appearances'].append(dict(tournament=row.get('Tournament'), end=iso_date(row.get('End-Date')),
                                     rank=number(row.get('Rk.')), rounds=number(row.get('Rd.')),
                                     players=number(row.get('n')),
                                     tnr=m and m.group(1), snr=m and m.group(2)))
    players = sorted(groups.values(), key=lambda g: -len(g['appearances']))[:limit]
    full_tournament_names(s, [a for g in players for a in g['appearances']])
    return dict(query=query, players=players, playerCount=len(groups),
                truncated=len(groups) > limit or len((found or {}).get('rows', [])) >= 250)


SEARCH_NAME_LENGTH = 30   # the player search cuts tournament names to this many characters
FULL_NAME_LOOKUPS = 25    # at most this many tournament pages per search


def full_tournament_names(s, appearances):
    """Replace tournament names the player search cut short with the full name from the
    tournament's own page (cached for a week; names don't change). At most
    FULL_NAME_LOOKUPS distinct tournaments per call; the rest keep the short name and
    are marked `nameShortened`."""
    cut = {a['tnr'] for a in appearances
           if a.get('tnr') and len(a.get('tournament') or '') >= SEARCH_NAME_LENGTH}
    names = {}
    for tnr in sorted(cut, reverse=True)[:FULL_NAME_LOOKUPS]:
        title = title_of(cached_get(s, f'{SEARCH_BASE}tnr{int(tnr)}.aspx?lan=1', 7 * 86400))
        if title:
            names[tnr] = ' '.join(title.split())
    for a in appearances:
        if a.get('tnr') in names:
            a['tournament'] = names[a['tnr']]
        elif a.get('tnr') in cut:
            a['nameShortened'] = True


def player_card(s, tnr, snr):
    """A player's card in one tournament (art=9): ident, FIDE id, birth year, ratings,
    and their games there."""
    html = cached_get(s, f'{SEARCH_BASE}tnr{int(tnr)}.aspx?lan=1&art=9&snr={int(snr)}', 3600)
    fields, games = {}, []
    for t in tables(html):
        rows = t['rows']
        if all('cells' in r and len(r['cells']) == 2 for r in rows[:3]) and not t['header']:
            fields.update({r['cells'][0]: r['cells'][1] for r in rows if 'cells' in r and len(r['cells']) == 2})
        elif t['header']:
            games = rows
    if not fields:
        soup = BeautifulSoup(html, 'html.parser')
        for tr in soup.select('table tr'):
            cells = tr.find_all('td', recursive=False)
            if len(cells) == 2:
                fields[text_of(cells[0])] = text_of(cells[1])
    def rating(key):
        value = number(fields.get(key))
        return value or None
    player = dict(name=fields.get('Name'), ident=fields.get('Ident-Number') or None,
                  fideId=(fields.get('Fide-ID') or fields.get('FIDE-ID') or '').strip('0') and
                  (fields.get('Fide-ID') or fields.get('FIDE-ID')) or None,
                  federation=fields.get('Federation'), title=fields.get('Title') or None,
                  club=fields.get('Club/City') or None, birthYear=number(fields.get('Year of birth')),
                  rating=rating('Rating'), ratingNational=rating('Rating national'),
                  ratingInternational=rating('Rating international'),
                  performance=rating('Performance rating'), startingRank=number(fields.get('Starting rank')),
                  rank=number(fields.get('Rank')),
                  points=float(fields['Points'].replace(',', '.').replace('½', '.5'))
                  if re.fullmatch(r'\d+(?:[.,]5|½)?|½', fields.get('Points') or '') else None)
    return dict(tournament=title_of(html), player=player, fields=fields, games=games,
                source=f'{SEARCH_BASE}tnr{tnr}.aspx?lan=1&art=9&snr={snr}')


# Tournament search (TurnierSuche): the form's own field names.
TOURNAMENT_FIELDS = dict(name='txt_bez', tnr='txt_tnr', director='txt_leiter', organizer='txt_veranstalter',
                         chief_arbiter='txt_Hauptschiedsrichter', arbiter='txt_Schiedsrichter',
                         location='txt_ort', ended_from='txt_von_tag', ended_to='txt_bis_tag')


def search_tournaments(s, country=None, limit=50, **query):
    """Tournaments matching the query, newest update first. `country` is a
    three-letter federation code (AUT, GER, …); dates are YYYY-MM-DD."""
    unknown = set(query) - set(TOURNAMENT_FIELDS)
    if unknown:
        raise QueryError(f'Unknown search field: {sorted(unknown)[0]}')
    url = SEARCH_BASE + 'TurnierSuche.aspx?lan=1'
    data = form_of(s.get(url, timeout=30).text)
    for key, field in TOURNAMENT_FIELDS.items():
        data['ctl00$P1$' + field] = str(query.get(key) or '')
    if country:
        data['ctl00$P1$combo_land'] = country.upper()
    data['ctl00$P1$cb_suchen'] = 'Search'
    html = s.post(url, data=data, timeout=30).text
    fetched = datetime.now(ZoneInfo('UTC'))
    found = next((t for t in tables(html) if t['header'] and 'Tournament' in t['header']), None)
    out = []
    for row in (found or {}).get('rows', []):
        if 'Tournament' not in row:
            continue
        out.append(dict(tnr=row.get('dbkey') or (re.search(r'tnr(\d+)', row.get('_link', '')) or [None, None])[1],
                        name=row.get('Tournament'), country=row.get('FED'), start=iso_date(row.get('from')),
                        end=iso_date(row.get('to')), location=row.get('Location') or None,
                        organizer=row.get('Organizer(s)') or None, director=row.get('Tournament director') or None,
                        rounds=number(row.get('Rd.')), players=number(row.get('n')),
                        # The site prints how long ago, e.g. "19 Hours 24 Min."; this is the time.
                        updatedAt=ago_to_timestamp(row.get('Last update'), fetched)))
    return dict(query=dict(query, country=country), tournaments=out[:limit], count=len(out))


def tournament(s, tnr, art=None, rd=None, snr=None, details=False, ttl=900):
    """Any page of a tournament: its title, the page's tables, and the menu of other
    views (label -> parameters) as the page links them. Without `art` it is the
    tournament's start page; `details` adds the organiser/venue/arbiter block."""
    params = ['lan=1']
    if art is not None:
        params.append(f'art={int(art)}')
    if rd is not None:
        params.append(f'rd={int(rd)}')
    if snr is not None:
        params.append(f'snr={int(snr)}')
    if details:
        params.append('turdet=YES')
    url = f'{SEARCH_BASE}tnr{int(tnr)}.aspx?' + '&'.join(params)
    html = cached_get(s, url, ttl)
    soup = BeautifulSoup(html, 'html.parser')
    views = {}
    for a in soup.select(f'a[href*="tnr{int(tnr)}.aspx"]'):
        label = text_of(a)
        q = dict(re.findall(r'(art|rd|snr)=(\d+)', a['href']))
        if label and 'art' in q and label not in views and len(label) < 60:
            views[label] = q
    info = {}
    for tr in soup.select('table tr'):
        cells = tr.find_all('td', recursive=False)
        if len(cells) == 2 and 2 < len(text_of(cells[0])) < 40 and not text_of(cells[0])[0].isdigit():
            info.setdefault(text_of(cells[0]), text_of(cells[1]))
    # The details block also lists the page's menus; those are `views`, not facts.
    for menu in ('Links', 'Lists', 'Board Pairings', 'Excel and Print', 'Show tournament details'):
        info.pop(menu, None)
    if info.get('Parameters') == 'No tournament details':
        info.pop('Parameters')
    dates = DATE.findall(info.get('Date', ''))
    return dict(tnr=str(tnr), title=title_of(html), url=url, info=info if details else None,
                start=f'{dates[0][0]}-{dates[0][1]}-{dates[0][2]}' if dates else None,
                end=f'{dates[-1][0]}-{dates[-1][1]}-{dates[-1][2]}' if dates else None,
                tables=tables(html), views=views)


def championship_leagues(s, year, prefix=None):
    """The leagues of an AUT championship season (meisterschaft.aspx), optionally only
    those whose name starts with `prefix` (e.g. "Bgld")."""
    html = cached_get(s, CHAMPIONSHIP.format(year=int(year)), 3600)
    soup = BeautifulSoup(html, 'html.parser')
    out = []
    for tr in soup.find_all('tr'):
        if tr.find('tr'):
            continue
        a = tr.find('a', href=re.compile(r'tnr\d+'))
        if a and (not prefix or a.get_text(strip=True).startswith(prefix)):
            out.append(dict(name=a.get_text(strip=True), tnr=re.search(r'tnr(\d+)', a['href']).group(1)))
    return out
