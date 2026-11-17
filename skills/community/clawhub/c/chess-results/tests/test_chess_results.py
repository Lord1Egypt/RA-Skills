"""Offline tests: notation, name matching, and parsing of Chess-Results pages.

All clubs, players and numbers here are made up.

    python3 -m unittest discover -s tests
"""
import os
import sys
import unittest
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import credentials
from client import (ago_to_timestamp, check_window, deadline, iso_date, messages, number,
                    parse_compositions, parse_members, resolved, saved_pairings, tables, when)
from match import judge
from report import (best_fit, board_order_warnings, club_words, flipped, forfeit_problem,
                    name_fit, score, team_number)

CFG = {'club': 'Musterdorf', 'ignore_words': ['Sponsorbank'],
       'deadline': {'time': '12:00', 'timezone': 'Europe/Vienna'}}
VIENNA = ZoneInfo('Europe/Vienna')


def member(ident, surname, given, rating=0, fide=None, national=None):
    return dict(ident=ident, surname=surname, given=given, rating=rating, fide=fide,
                national=rating if national is None else national,
                club='SV Musterdorf', kind='Stamm')


# A father and daughter, two brothers, and others: the cases that make matching hard.
MUSTERDORF = [member('900101', 'Novak', 'Bernd', 2210), member('900102', 'Novakova', 'Bettina', 1350),
              member('900103', 'Huber', 'Karl', 1500), member('900104', 'Gruber', 'Lena', 1420),
              member('900105', 'Kovar', 'Martin', 1600), member('900106', 'Kovar', 'David')]
BEISPIELSTADT = [member('900201', 'Lang', 'Eva', 1650)]


class NotationTests(unittest.TestCase):
    def test_team_numbers_in_digits_roman_or_absent(self):
        self.assertEqual(team_number('Sponsorbank Musterdorf 3'), '3')
        self.assertEqual(team_number('Musterdorf IV'), '4')
        self.assertEqual(team_number('Musterdorf'), '1')

    def test_club_words_skip_sponsors_and_generic_words(self):
        self.assertEqual(club_words('SPGM Nordheim Südheim 1', CFG), {'nordheim', 'sudheim'})
        self.assertEqual(club_words('Sponsorbank Musterdorf 2', CFG), {'musterdorf'})

    def test_an_empty_board_needs_the_matching_forfeit(self):
        self.assertIsNone(forfeit_problem(dict(home=None, away=['1', 'A'], result='--+')))
        self.assertIsNone(forfeit_problem(dict(home=None, away=None, result='---')))
        self.assertIn('--+', forfeit_problem(dict(home=None, away=['1', 'A'], result='1-0')))

    def test_turning_a_report_around(self):
        match = dict(home=dict(team='Beispielstadt 1'), away=dict(team='Musterdorf 2'), total='3:1',
                     boards=[dict(home=['1', 'A'], away=['2', 'B'], result='0-1'),
                             dict(home=None, away=['3', 'C'], result='--+')])
        out = flipped(match)
        self.assertEqual(out['home']['team'], 'Musterdorf 2')
        self.assertEqual([b['result'] for b in out['boards']], ['1-0', '+--'])
        self.assertEqual(out['total'], '1:3')
        self.assertEqual(score(out), (2, 0))
        self.assertEqual(flipped(out), match)

    def test_board_order_by_national_rating_leaves_unrated_out(self):
        a, b, c = member('1', 'A', 'a', 1500), member('2', 'B', 'b', 1650), member('3', 'C', 'c', 0)
        self.assertEqual(len(board_order_warnings('T', [a, b], 100)), 1)
        self.assertEqual(board_order_warnings('T', [a, b], 200), [])
        self.assertEqual(board_order_warnings('T', [c, b], 100), [])
        self.assertEqual(board_order_warnings('T', [a, b], None), [])
        guest = member('4', 'D', 'd', 1900, national=0)     # FIDE only: shown, not ordered by
        self.assertEqual(board_order_warnings('T', [a, guest], 100), [])


class NameTests(unittest.TestCase):
    def test_slips_of_the_pen_still_fit(self):
        self.assertEqual(name_fit('Grubar L', 'Gruber', 'Lena')[0], 'spelling')
        self.assertEqual(name_fit('Eva Lang', 'Lang-Berger', 'Eva')[0], 'ok')
        self.assertEqual(name_fit('HUBER K.', 'Huber', 'Karl')[0], 'ok')

    def test_another_person_or_initial_does_not(self):
        self.assertEqual(name_fit('GRUBER L.', 'Huber', 'Karl')[0], 'mismatch')
        self.assertEqual(name_fit('KOVAR M.', 'Kovar', 'David')[0], 'mismatch')

    def test_best_fit_says_when_two_fit_alike(self):
        _, _, unique = best_fit('Kovar', MUSTERDORF)
        self.assertFalse(unique)
        p, _, unique = best_fit('KOVAR D.', MUSTERDORF)
        self.assertEqual((p['ident'], unique), ('900106', True))


class JudgeTests(unittest.TestCase):
    def verdict(self, written, ident, team=()):
        return judge(written, ident, MUSTERDORF, set(team), BEISPIELSTADT, 'SV Beispielstadt')

    def test_a_right_ident_passes(self):
        person, _, stop = self.verdict('NOVAK B.', '900101', team=['900101'])
        self.assertFalse(stop)
        self.assertEqual(person['given'], 'Bernd')

    def test_a_relatives_ident_stops_when_a_team_player_fits_better(self):
        _, text, stop = self.verdict('NOVAK B.', '900102', team=['900101'])
        self.assertTrue(stop)
        self.assertIn('Novak, Bernd 900101 of this team', text)

    def test_a_missing_ident_is_looked_up_team_first(self):
        person, text, stop = self.verdict('Novak B.', '', team=['900101'])
        self.assertFalse(stop)
        self.assertEqual(person['ident'], '900101')
        self.assertIn('looked up in the team', text)

    def test_a_missing_ident_with_two_candidates_stops(self):
        _, text, stop = self.verdict('Kovar', '')
        self.assertTrue(stop)
        self.assertIn('several', text)

    def test_the_other_clubs_ident_and_an_unknown_one_stop(self):
        _, text, stop = self.verdict('Lang', '900201')
        self.assertTrue(stop)
        self.assertIn('SV Beispielstadt', text)
        _, text, stop = self.verdict('Nobody', '999999')
        self.assertTrue(stop)
        self.assertIn('not a member', text)

    def test_a_name_that_fits_nobody_names_the_likely_player(self):
        _, text, stop = self.verdict('GRUBER L.', '900103')
        self.assertTrue(stop)
        self.assertIn('Gruber, Lena 900104', text)


class WindowTests(unittest.TestCase):
    def at(self, *args):
        return datetime(*args, tzinfo=VIENNA)

    def test_a_weekend_match_is_due_monday_noon(self):
        self.assertEqual(deadline(date(2026, 10, 4), CFG), self.at(2026, 10, 5, 12))
        self.assertEqual(deadline(date(2026, 10, 3), CFG), self.at(2026, 10, 5, 12))

    def test_open_on_the_day_and_until_the_deadline_only(self):
        self.assertIsNone(check_window(date(2026, 10, 4), CFG, self.at(2026, 10, 5, 11, 59)))
        self.assertIn('deadline', check_window(date(2026, 10, 4), CFG, self.at(2026, 10, 5, 12, 1)))
        self.assertIn('future', check_window(date(2026, 10, 11), CFG, self.at(2026, 10, 4, 18)))

    def test_no_deadline_configured(self):
        self.assertIsNone(check_window(date(2026, 1, 1), dict(CFG, deadline=None), self.at(2026, 10, 4, 18)))


class PageTests(unittest.TestCase):
    MEMBERS = '''<table id="P1_GridView4">
      <tr><th>PNr</th><th>Nachname</th><th>Vorname</th><th>Titel</th><th>Elo</th><th>EloI</th>
          <th>FideNr</th><th>Land</th><th>VNr</th><th>Verein</th><th>Art</th></tr>
      <tr><td>900107</td><td>Gast</td><td>Tomas</td><td></td><td>0</td><td>2100</td><td>99000001</td>
          <td>CZE</td><td>9999</td><td>SV Musterdorf</td><td>Gast</td></tr>
      <tr><td>900103</td><td>Huber</td><td>Karl</td><td></td><td>1500</td><td>1520</td><td>99000002</td>
          <td>AUT</td><td>9999</td><td>SV Musterdorf</td><td>Stamm</td></tr></table>'''

    CHECKED = '''<div id="P_Info" class="info"><h5>Hinweis: Der Spieler Lang, Eva (Pnr=900201) war am
      04.10.2026 nicht Miglied bei Verein SV Musterdorf</h5></div>
      <div id="P_Error" class="error"><h5>Die Personennummer 999999 ist nicht in der Meldekartei vorhanden</h5></div>
      <table id="P1_GridView2">
       <tr><td><span id="P1_GridView2_l_Br_1">Br.</span><span id="P1_GridView2_l_erg_1">4 - 0</span></td></tr>
       <tr><td><span id="P1_GridView2_l_Br_2">1</span><span id="P1_GridView2_l_Name1_2">nicht in Meldekartei</span>
           <span id="P1_GridView2_l_Name2_2">Wolff,  Ida</span></td></tr>
       <tr><td><span id="P1_GridView2_l_Br_3">2</span><span id="P1_GridView2_l_Name1_3">Lang,  Eva</span>
           <span id="P1_GridView2_l_Name2_3">Wolff,  Jan</span></td></tr></table>'''

    OVERVIEW = '''<table id="P1_GridView2">
      <tr><td><span id="P1_GridView2_l_Br_0">2. Runde am 04.10.2026 um 09:00</span></td></tr>
      <tr><td><span id="P1_GridView2_l_Br_1">Br.</span><span id="P1_GridView2_l_Name1_1">Sponsorbank Musterdorf 1</span>
          <span id="P1_GridView2_l_elo1_1">Elo</span><span id="P1_GridView2_l_Name2_1">SPGM Nordheim Südheim 1</span>
          <span id="P1_GridView2_l_elo2_1">Elo</span><span id="P1_GridView2_l_erg_1">2 : 4</span></td></tr>
      <tr><td><span id="P1_GridView2_l_Br_2">1</span><span id="P1_GridView2_l_Pnr1_2">900101</span>
          <span id="P1_GridView2_l_Name1_2">Novak, Bernd</span><span id="P1_GridView2_l_elo1_2">2210</span>
          <span id="P1_GridView2_l_Mnr2_2">FM</span><span id="P1_GridView2_l_Pnr2_2">900301</span>
          <span id="P1_GridView2_l_Name2_2">Berger, Anna</span><span id="P1_GridView2_l_elo2_2">2250</span>
          <span id="P1_GridView2_l_erg_2">0 - 1</span></td></tr>
      <tr><td><span id="P1_GridView2_l_Br_3">2</span><span id="P1_GridView2_l_Pnr1_3">0</span>
          <span id="P1_GridView2_l_Name1_3">Brett nicht besetzt</span><span id="P1_GridView2_l_elo1_3">0</span>
          <span id="P1_GridView2_l_Pnr2_3">900302</span><span id="P1_GridView2_l_Name2_3">Fuchs, Max</span>
          <span id="P1_GridView2_l_elo2_3">2190</span><span id="P1_GridView2_l_erg_3">0K - 1K</span></td></tr>
      <tr><td><span id="P1_GridView2_l_Br_4">Br.</span><span id="P1_GridView2_l_Name1_4">Westdorf 1</span>
          <span id="P1_GridView2_l_elo1_4">Elo</span><span id="P1_GridView2_l_Name2_4">Ostdorf 1</span>
          <span id="P1_GridView2_l_elo2_4">Elo</span><span id="P1_GridView2_l_erg_4">0 : 0</span></td></tr>
      <tr><td><span id="P1_GridView2_l_Br_5">1</span><span id="P1_GridView2_l_Pnr1_5">900401</span>
          <span id="P1_GridView2_l_Name1_5">Roth, Paul</span><span id="P1_GridView2_l_elo1_5">2200</span>
          <span id="P1_GridView2_l_Pnr2_5">900501</span><span id="P1_GridView2_l_Name2_5">Weiss, Ute</span>
          <span id="P1_GridView2_l_elo2_5">1980</span><span id="P1_GridView2_l_erg_5">HP-HP</span></td></tr></table>'''

    def test_member_lists_with_the_fide_rating_standing_in(self):
        people = parse_members(self.MEMBERS)
        self.assertEqual([(p['ident'], p['rating'], p['national']) for p in people],
                         [('900107', 2100, 0), ('900103', 1500, 1500)])
        self.assertEqual(people[0]['fide'], '99000001')

    def test_the_check_page_keeps_every_name_on_its_own_board(self):
        boards, site_score = resolved(self.CHECKED)
        self.assertEqual(site_score, '4:0')
        self.assertEqual(boards[0], dict(home='nicht in Meldekartei', away='Wolff, Ida'))
        errors, notices = messages(self.CHECKED)
        self.assertIn('999999', errors[0])
        self.assertIn('nicht Miglied', notices[0])

    def test_saved_pairings_with_titles_ratings_forfeits_and_unentered_ones(self):
        pairs = saved_pairings(self.OVERVIEW)
        self.assertEqual([p['home'] for p in pairs], ['Sponsorbank Musterdorf 1', 'Westdorf 1'])
        first = pairs[0]['boards']
        self.assertEqual(first[0]['away'], dict(ident='900301', name='Berger, Anna', title='FM', rating=2250))
        self.assertEqual((first[1]['home'], first[1]['result']), (None, '--+'))
        self.assertIsNone(pairs[1]['boards'][0]['result'])

    def test_team_compositions(self):
        html = '''<table class="CRs1">
          <tr><td colspan="9">&nbsp;1. Sponsorbank Musterdorf 3 (RtgAvg:1410 / TB1: 3)</td></tr>
          <tr><th>Bo.</th><th></th><th>Name</th><th>Rtg</th><th>FED</th><td>Art</td><th>FideID</th></tr>
          <tr><td>1</td><td></td><td><a href="x?snr=7">Huber, Karl</a></td><td>1500</td><td>AUT</td>
              <td>Stamm</td><td><a href="#">99000002</a></td><td>1</td><td>1</td></tr></table>'''
        teams = parse_compositions(html)
        self.assertEqual(teams['Sponsorbank Musterdorf 3'][0]['fide'], '99000002')

    def test_tables_keep_headers_sections_and_links(self):
        html = """<table class="CRs1"><tr class="CRg1b"><th>No.</th><th>Tournament</th><th>dbkey</th></tr>
          <tr><td>1</td><td><a href="tnr100001.aspx?lan=1">Example League</a></td><td>100001</td></tr>
          <tr><td colspan="3">Round 2</td></tr></table>"""
        t = tables(html)[0]
        self.assertEqual(t['header'], ['No.', 'Tournament', 'dbkey'])
        self.assertEqual(t['rows'][0]['_link'], 'tnr100001.aspx?lan=1')
        self.assertEqual(t['rows'][1], {'section': 'Round 2'})

    def test_a_plain_first_row_is_the_header_but_key_value_rows_are_not(self):
        html = '''<table class="CRs2"><tr><td>Name</td><td>ID</td><td>FED</td></tr>
          <tr><td>Huber, Karl</td><td>900103</td><td>AUT</td></tr></table>
          <table class="CRs1"><tr><td>Name</td><td>Huber, Karl</td></tr>
          <tr><td>Ident-Number</td><td>900103</td></tr></table>'''
        search, card = tables(html)
        self.assertEqual(search['rows'][0]['ID'], '900103')
        self.assertIsNone(card['header'])
        self.assertEqual(card['rows'][1]['cells'], ['Ident-Number', '900103'])


class NormalisationTests(unittest.TestCase):
    """Chess-Results prints dates with slashes, the last update as time ago, and numbers
    as text; the tools return ISO dates, timestamps and integers."""

    def test_dates_numbers_and_round_times(self):
        self.assertEqual(iso_date('2026/09/20'), '2026-09-20')
        self.assertEqual(iso_date('Kittsee'), 'Kittsee')
        self.assertEqual((number('10'), number('-'), number('')), (10, None, None))
        self.assertEqual(when('Round 2 on 2026/10/04 at 09:00'), '2026-10-04T09:00')
        self.assertEqual(when('Round 1 on 2026/09/20'), '2026-09-20')

    def test_time_ago_becomes_a_timestamp(self):
        now = datetime(2026, 10, 5, 16, 30, 45, tzinfo=ZoneInfo('UTC'))
        self.assertEqual(ago_to_timestamp('19 Hours 24 Min.', now), '2026-10-04T21:06:00Z')
        self.assertEqual(ago_to_timestamp('2 Days 3 Hours', now), '2026-10-03T13:30:00Z')
        self.assertEqual(ago_to_timestamp('6 Days', now), '2026-09-29T16:30:00Z')
        self.assertIsNone(ago_to_timestamp('yesterday', now))

    def test_a_schedule_keeps_both_teams_and_skips_repeated_headers(self):
        html = """<table class="CRs1">
          <tr><td colspan="6">Round 1 on 2026/09/20 at 09:00</td></tr>
          <tr><td>No.</td><td>Team</td><td>Team</td><td>Res.</td><td>:</td><td>Res.</td></tr>
          <tr><td>1</td><td>Westdorf 1</td><td>Ostdorf 1</td><td>4½</td><td>:</td><td>1½</td></tr>
          <tr><td colspan="6">Round 2 on 2026/10/04 at 09:00</td></tr>
          <tr><td>No.</td><td>Team</td><td>Team</td><td>Res.</td><td>:</td><td>Res.</td></tr>
          <tr><td>1</td><td>Ostdorf 1</td><td>Nordheim 1</td><td>3</td><td>:</td><td>3</td></tr></table>"""
        t = tables(html)[0]
        self.assertEqual(t['header'], ['No.', 'Team', 'Team 2', 'Res.', ':', 'Res. 2'])
        rows = t['rows']
        self.assertEqual(rows[0], {'section': 'Round 1 on 2026/09/20 at 09:00', 'date': '2026-09-20T09:00'})
        self.assertEqual((rows[1]['Team'], rows[1]['Team 2'], rows[1]['Res.'], rows[1]['Res. 2']),
                         ('Westdorf 1', 'Ostdorf 1', '4½', '1½'))
        self.assertEqual([r.get('section', r.get('Team')) for r in rows],
                         ['Round 1 on 2026/09/20 at 09:00', 'Westdorf 1', 'Round 2 on 2026/10/04 at 09:00', 'Ostdorf 1'])


    def test_a_round_page_heads_each_match_and_names_the_board_columns(self):
        html = """<table class="CRs1">
          <tr><td colspan="9">Round 2 on 2026/10/04 at 09:00</td></tr>
          <tr><td>Bo.</td><td>6</td><td>Westdorf 1</td><td>Rtg</td><td>-</td><td>4</td><td>Ostdorf 1</td><td>Rtg</td><td>1 : 5</td></tr>
          <tr><td>1.1</td><td>FM</td><td>Roth, Paul</td><td>2066</td><td>-</td><td></td><td>Weiss, Ute</td><td>2369</td><td>½ - ½</td></tr>
          <tr><td>Bo.</td><td>5</td><td>Nordheim 1</td><td>Rtg</td><td>-</td><td>3</td><td>Südheim 1</td><td>Rtg</td><td>3 : 3</td></tr>
          <tr><td>2.1</td><td></td><td>Lang, Eva</td><td>1900</td><td>-</td><td></td><td>Fuchs, Max</td><td>1850</td><td>1 - 0</td></tr></table>"""
        rows = tables(html)[0]['rows']
        self.assertEqual(rows[1], {'section': 'Westdorf 1 – Ostdorf 1 1 : 5', 'home': 'Westdorf 1',
                                   'away': 'Ostdorf 1', 'score': '1 : 5'})
        self.assertEqual((rows[2]['Name'], rows[2]['Name 2'], rows[2]['Res.']), ('Roth, Paul', 'Weiss, Ute', '½ - ½'))
        self.assertEqual(rows[3]['home'], 'Nordheim 1')
        self.assertEqual(rows[4]['Name'], 'Lang, Eva')


class CredentialTests(unittest.TestCase):
    def test_the_environment_wins_and_the_password_is_never_reported(self):
        old = {k: os.environ.get(k) for k in ('CHESS_RESULTS_PNO', 'CHESS_RESULTS_PASSWORD')}
        os.environ.update(CHESS_RESULTS_PNO='900999', CHESS_RESULTS_PASSWORD='test-only-value')
        try:
            self.assertEqual(credentials.load(), ('900999', 'test-only-value'))
            info = credentials.status()
            self.assertEqual((info['source'], info['account']), ('environment', '900999'))
            self.assertNotIn('test-only-value', repr(info))
        finally:
            for k, v in old.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v


class CredentialFileTests(unittest.TestCase):
    """The file route, with the system store switched off so a real entry is untouched."""

    def setUp(self):
        import tempfile
        self.dir = tempfile.TemporaryDirectory()
        self.path = Path(self.dir.name) / 'credentials.json'
        self.saved = (credentials._security, credentials._keyring,
                      {k: os.environ.get(k) for k in ('CHESS_RESULTS_PNO', 'CHESS_RESULTS_PASSWORD',
                                                      'CHESS_RESULTS_CREDENTIALS')})
        credentials._security = lambda: None
        credentials._keyring = lambda: None
        for k in ('CHESS_RESULTS_PNO', 'CHESS_RESULTS_PASSWORD'):
            os.environ.pop(k, None)
        os.environ['CHESS_RESULTS_CREDENTIALS'] = str(self.path)

    def tearDown(self):
        credentials._security, credentials._keyring, env = self.saved
        for k, v in env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        self.dir.cleanup()

    def test_a_private_file_is_used_and_written_private(self):
        credentials.store_file('900999', 'file-only-value')
        self.assertEqual(oct(self.path.stat().st_mode & 0o777), '0o600')
        self.assertEqual(credentials.load(), ('900999', 'file-only-value'))
        info = credentials.status()
        self.assertTrue(info['source'].startswith('file '))
        self.assertNotIn('file-only-value', repr(info))

    def test_a_file_others_can_read_is_refused(self):
        credentials.store_file('900999', 'file-only-value')
        os.chmod(self.path, 0o644)
        with self.assertRaises(credentials.CredentialError):
            credentials.load()

    def test_the_environment_still_wins_over_the_file(self):
        credentials.store_file('900999', 'file-only-value')
        os.environ.update(CHESS_RESULTS_PNO='900888', CHESS_RESULTS_PASSWORD='env-value')
        self.assertEqual(credentials.load(), ('900888', 'env-value'))

    def test_without_any_login_the_hint_says_how(self):
        with self.assertRaises(credentials.CredentialError) as e:
            credentials.load()
        self.assertIn('--file', str(e.exception))


class PackagingTests(unittest.TestCase):
    """The same folder is a skill (OpenClaw, ClawHub), a Claude Code plugin and an
    OpenClaw Claude bundle; these keep the pieces in step."""
    ROOT = Path(__file__).resolve().parents[1]

    def test_the_plugin_skill_is_the_same_as_the_root_skill(self):
        self.assertEqual((self.ROOT / 'SKILL.md').read_text(),
                         (self.ROOT / 'skills/chess-results/SKILL.md').read_text(),
                         'copy SKILL.md to skills/chess-results/SKILL.md')

    def test_the_mcp_server_is_declared_in_mcp_json(self):
        import json
        servers = json.loads((self.ROOT / '.mcp.json').read_text())['mcpServers']
        self.assertIn('scripts/server.py', servers['chess-results']['args'][0])
        manifest = json.loads((self.ROOT / '.claude-plugin/plugin.json').read_text())
        # OpenClaw reads a Claude bundle's servers from .mcp.json only.
        self.assertNotIn('mcpServers', manifest)


if __name__ == '__main__':
    unittest.main()
