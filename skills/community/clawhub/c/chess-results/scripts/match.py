"""Check a transcribed team match report against Chess-Results, and enter it.

For each match: find the pairing by date and our team (a sheet written the wrong way
round is turned around), open the result editor, read both clubs' member lists on
the round date ("Spieler Team x anzeigen") and the team compositions so far.

Every written name is matched, the team's own players first and the rest of the club
second: the ident must belong to a member of that side's club, the written name must
fit that member and must not fit another player of the team clearly better (on a team
where Bernd Novak plays, "Novak B." is Bernd, not his daughter Bettina Novakova). A side written without
an ident ("") is looked up the same way and accepted only when one player clearly
fits. Results, no-shows, the total and the board order (national rating, configured
tolerance) are checked.

Then the boards go into the editor and "Eingabe Prüfen" is pressed: Chess-Results
resolves each number against the federation's register, and any error or notice, a
name that does not fit, or a different score stops the match. Saving happens only
when asked, for a clean match inside the entry window, and is confirmed on the
overview afterwards.
"""
import json
from datetime import date
from pathlib import Path

import requests

from client import (EntryError, Pages, Rosters, board_rows, check_window, filled, find_pairing,
                    members, messages, open_editor, postback, resolved)
from report import (best_fit, board_order_warnings, forfeit_problem, is_ours, load_config,
                    name_fit, normal_result, score, score_text)


def full(p):
    return f"{p['surname']}, {p['given']}" if p else '?'


def judge(written, ident, side_members, team_idents, other_members, other_club):
    """(person, verdict, stop) for one player of one side."""
    team = [m for m in side_members if m['ident'] in team_idents]
    looked_up = None
    if not str(ident or '').strip():
        for source, pool in (('team', team), ('club', side_members)):
            p, _, unique = best_fit(written, pool)
            if p and unique:
                ident, looked_up = p['ident'], source
                break
            if p:
                return None, 'STOP: no ident on the sheet, and several players fit the name', True
        if not looked_up:
            return None, 'STOP: no ident on the sheet, and no member fits the name', True
    person = next((m for m in side_members if m['ident'] == str(ident)), None)
    if not person:
        other = next((m for m in other_members if m['ident'] == str(ident)), None)
        if other:
            return other, f'STOP: {ident} is {full(other)} of {other_club}, the other side', True
        return None, f'STOP: {ident} is not a member of this club on the round date', True
    fit, ratio = name_fit(written, person['surname'], person['given'])
    if fit == 'mismatch':
        likely = best_fit(written, team)[0] or best_fit(written, side_members)[0]
        hint = f'; the name fits {full(likely)} {likely["ident"]}' if likely else ''
        return person, f'STOP: the written name does not fit {full(person)}{hint}', True
    for scope, pool in (('of this team', team), ('of this club', side_members)):
        rival, r_ratio, _ = best_fit(written, [m for m in pool if m['ident'] != person['ident']])
        if rival and r_ratio > ratio + 0.05:
            return person, (f'STOP: the written name fits {full(rival)} {rival["ident"]} {scope} '
                            f'better than {full(person)}'), True
    verdict = 'ok' if fit == 'ok' else 'ok (spelling differs)'
    if looked_up:
        verdict += f' (ident looked up in the {looked_up})'
    return person, verdict, False


def process(s, cfg, report, save):
    """Check (and with `save`, enter) every match of a report, printing a table per
    match. Returns (problems, the report with every ident filled in, as Chess-Results
    pairs it)."""
    pages, rosters = Pages(s, cfg), Rosters(s)
    problems = 0
    out_matches = []
    for match in report['matches']:
        day = date.fromisoformat(match.get('date') or report['date'])
        late = check_window(day, cfg)
        try:
            league, tnr, row, match, swapped = find_pairing(pages, match, day)
        except EntryError as e:
            print(f"\n== {match['home']['team']} – {match['away']['team']}: {e}")
            problems += 1
            out_matches.append(match)
            continue
        url, html, _, _ = pages.page(tnr, fresh=True)
        row = next(r for r in pages.page(tnr)[3] if r['home'] == row['home'] and r['away'] == row['away'])
        print(f"\n== {row['home']} – {row['away']}: {league}, {day:%d.%m.%Y} (tnr {tnr}), now {row['score']}")
        if swapped:
            print(f"  NOTE: the sheet has home and guest the wrong way round; {row['home']} is at home "
                  'on Chess-Results. Teams, players and results are taken turned around.')
        editor = open_editor(s, url, html, row)
        lists = dict(zip(('home', 'away'), members(s, url, editor.text)))
        clubs = {side: (lists[side][0]['club'] if lists[side] else row[side]) for side in lists}
        team_idents = {side: rosters.idents(tnr, row[side], lists[side]) for side in ('home', 'away')}
        # Regulars of our club's other teams, in the leagues where it has one this
        # round. Only a notice, so a page that will not load does not stop the match.
        ours = 'home' if is_ours(row['home'], cfg) else 'away'
        elsewhere = {}
        for _, other_tnr in pages.league_list(day):
            if not any(is_ours(r['home'], cfg) or is_ours(r['away'], cfg) for r in pages.page(other_tnr)[3]):
                continue
            try:
                teams = rosters.league(other_tnr)
            except requests.RequestException as e:
                print(f'  note: team compositions of tnr {other_tnr} unavailable ({type(e).__name__})')
                continue
            for team in teams:
                if is_ours(team, cfg) and not (other_tnr == tnr and team == row[ours]):
                    for i in rosters.idents(other_tnr, team, lists[ours]):
                        elsewhere.setdefault(i, team)

        bad = 0
        people = {'home': [], 'away': []}
        for no, board in enumerate(match['boards'], 1):
            problem = forfeit_problem(board)
            if problem:
                print(f'  STOP: board {no}: {problem}')
                bad += 1
            if normal_result(board['result']) == '?':
                print(f'  note: board {no} goes in as "unbekannt"; enter the result once it is known')
            for side in ('home', 'away'):
                other = 'away' if side == 'home' else 'home'
                if board[side] is None:
                    people[side].append(None)
                    print(f'  {no} {side:<4} {"–":>7}  {"(nicht angetreten)":<24} → {"board empty":<30}')
                    continue
                ident, written = board[side]
                person, verdict, stop = judge(written, ident, lists[side], team_idents[side],
                                              lists[other], clubs[other])
                if person and not stop:
                    board[side] = [person['ident'], written]
                    if person['ident'] in team_idents[side]:
                        verdict += ', team regular'
                    elif side == ours and person['ident'] in elsewhere:
                        verdict += f', NOTICE: regular of {elsewhere[person["ident"]]}'
                    else:
                        verdict += ', first game for this team'
                bad += stop
                people[side].append(person if not stop else None)
                rating = (person or {}).get('rating') or ''
                print(f'  {no} {side:<4} {board[side][0] or "?":>7}  {written:<24} → '
                      f'{full(person):<30} {rating:>5}  {verdict}')
        expected = score_text(score(match))
        if match.get('total') and match['total'].replace(' ', '') != expected:
            print(f'  STOP: the boards add up to {expected}, the sheet says {match["total"]}')
            bad += 1
        for side in ('home', 'away'):
            for warning in board_order_warnings(row[side], people[side], cfg.get('board_order_tolerance')):
                print(f'  warn: {warning}')
        out_matches.append(match)
        if bad:
            print('  not checked on Chess-Results: fix the report first.')
            problems += bad
            continue

        fields = filled(board_rows(editor.text), match['boards'])
        checked = postback(s, url, editor.text, **fields, **{'ctl00$P1$cb_test': 'Eingabe Prüfen'})
        boards, site_score = resolved(checked.text)
        errors, notices = messages(checked.text)
        for text in errors:
            print(f'  CHESS-RESULTS ERROR: {text}')
        for text in notices:
            print(f'  CHESS-RESULTS NOTICE: {text}')
        bad += len(errors) + len(notices)
        for no, (board, got) in enumerate(zip(match['boards'], boards), 1):
            for side in ('home', 'away'):
                listed = got[side]
                if board[side] is None:
                    if listed:
                        print(f'  MISMATCH: board {no} {side} should be empty, Chess-Results shows {listed}')
                        bad += 1
                    continue
                surname, _, given = listed.partition(',')
                if ',' not in listed or name_fit(board[side][1], surname, given.strip())[0] == 'mismatch':
                    print(f'  MISMATCH: board {no} {side}: Chess-Results shows {listed or "nothing"} '
                          f'for {board[side][0]}, the sheet says {board[side][1]}')
                    bad += 1
        if site_score and site_score.replace(',', '.') != expected:
            print(f'  MISMATCH: Chess-Results computes {site_score}, the report says {expected}')
            bad += 1
        print(f'  Eingabe Prüfen: score {site_score or "?"} (report {expected}), '
              f'{len(errors)} error(s), {len(notices)} notice(s)')
        if bad:
            print('  not saved.')
            problems += bad
            continue
        if not save:
            print('  checked; not saved (use "enter" to save).')
            continue
        if late:
            print(f'  not saved: {late}.')
            problems += 1
            continue
        postback(s, url, checked.text, **fields, **{'ctl00$P1$cb_save': 'Eingabe Speichern'})
        after = next((r['score'] for r in pages.page(tnr, fresh=True)[3]
                      if r['home'] == row['home'] and r['away'] == row['away']), None)
        ok = after and after.replace(' ', '').replace(',', '.') == expected
        print(f'  saved: the overview now shows {after}' + ('' if ok else '  <- CHECK THIS BY HAND'))
        problems += not ok
    return problems, dict(report, matches=out_matches)
