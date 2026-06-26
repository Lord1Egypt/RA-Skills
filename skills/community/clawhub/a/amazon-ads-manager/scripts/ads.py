#!/usr/bin/env python3
# /// script
# dependencies = ["requests"]
# ///
"""
Amazon Advertising API CLI — Sponsored Products (v3)

Env vars (set in .env alongside this script):
  AMAZON_ADS_CLIENT_ID
  AMAZON_ADS_CLIENT_SECRET
  AMAZON_ADS_REFRESH_TOKEN
  AMAZON_ADS_PROFILE_ID      (run `profiles` command to discover)
  AMAZON_ADS_REGION          NA | EU | FE  (default: NA)

Commands:
  profiles
  campaigns [--state ENABLED|PAUSED|ARCHIVED|ALL]
  adgroups  --campaign <id>
  keywords  --campaign <id> | --adgroup <id>
  negatives --campaign <id>
  set-bid   <keyword_id> <bid>
  set-state <keyword_id> ENABLED|PAUSED|ARCHIVED
  add-negative --campaign <id> --keyword <text> [--match EXACT|PHRASE]
  report campaigns   --days 30
  report adgroups    --days 30
  report keywords    --days 30  [--campaign <id>]
  report searchterms --days 30  [--campaign <id>]
"""
from __future__ import annotations

import argparse
import gzip
import json
import os
import sys
import time
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import requests

# ── Env loading ───────────────────────────────────────────────────────────────

def _load_env(path: Path):
    if not path.exists():
        return
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k, _, v = line.partition('=')
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if k and k not in os.environ:
                os.environ[k] = v

# Load skill .env (place credentials here after installing)
_load_env(Path(__file__).parent.parent / '.env')

CLIENT_ID     = os.environ.get('AMAZON_ADS_CLIENT_ID', '')
CLIENT_SECRET = os.environ.get('AMAZON_ADS_CLIENT_SECRET', '')
REFRESH_TOKEN = os.environ.get('AMAZON_ADS_REFRESH_TOKEN', '')
PROFILE_ID    = os.environ.get('AMAZON_ADS_PROFILE_ID', '')
REGION        = os.environ.get('AMAZON_ADS_REGION', 'NA').upper()

ENDPOINTS = {
    'NA': 'https://advertising-api.amazon.com',
    'EU': 'https://advertising-api-eu.amazon.com',
    'FE': 'https://advertising-api-fe.amazon.com',
}
BASE = ENDPOINTS.get(REGION, ENDPOINTS['NA'])
TOKEN_URL = 'https://api.amazon.com/auth/o2/token'


# ── AdsClient ─────────────────────────────────────────────────────────────────

class AdsClient:
    def __init__(self):
        self._token: str | None = None
        self._expiry: float = 0.0

    def _refresh(self):
        if self._token and time.time() < self._expiry:
            return
        r = requests.post(TOKEN_URL, data={
            'grant_type':    'refresh_token',
            'client_id':     CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'refresh_token': REFRESH_TOKEN,
        }, timeout=15)
        r.raise_for_status()
        d = r.json()
        self._token = d['access_token']
        self._expiry = time.time() + d.get('expires_in', 3600) - 60

    def _headers(self, extra: dict | None = None) -> dict:
        self._refresh()
        h = {
            'Authorization':                   f'Bearer {self._token}',
            'Amazon-Advertising-API-ClientId': CLIENT_ID,
            'Amazon-Advertising-API-Scope':    PROFILE_ID,
            'Accept':                          'application/json',
            'Content-Type':                    'application/json',
        }
        if extra:
            h.update(extra)
        return h

    def _vnd(self, resource: str, v: int = 3) -> dict:
        mt = f'application/vnd.{resource}.v{v}+json'
        return {'Content-Type': mt, 'Accept': mt}

    def req(self, method: str, path: str, body: Any = None,
            extra_headers: dict | None = None, retries: int = 3) -> Any:
        url = BASE + path
        headers = self._headers(extra_headers)
        exc = None
        for attempt in range(retries):
            try:
                r = requests.request(
                    method, url, headers=headers,
                    json=body if method in ('POST', 'PUT', 'PATCH') else None,
                    params=body if method == 'GET' else None,
                    timeout=60,
                )
                if r.status_code == 401:
                    self._token = None
                    self._refresh()
                    headers['Authorization'] = f'Bearer {self._token}'
                    continue
                if r.status_code == 429:
                    wait = float(r.headers.get('Retry-After', 2 ** attempt))
                    time.sleep(wait)
                    continue
                if r.status_code >= 500 and attempt < retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                if not r.ok:
                    raise RuntimeError(f'API {r.status_code}: {r.text[:400]}')
                r.raise_for_status()
                return r.json() if r.text.strip() else {}
            except requests.HTTPError:
                raise
            except Exception as e:
                exc = e
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)
        raise RuntimeError(f'Request failed: {exc}')

    # Profiles (no scope header needed)
    def list_profiles(self) -> list:
        self._refresh()
        r = requests.get(f'{BASE}/v2/profiles', headers={
            'Authorization':                   f'Bearer {self._token}',
            'Amazon-Advertising-API-ClientId': CLIENT_ID,
        }, timeout=30)
        r.raise_for_status()
        return r.json()

    # Campaigns
    def list_campaigns(self, states: list[str] | None = None) -> dict:
        return self.req('POST', '/sp/campaigns/list', {
            'stateFilter': {'include': states or ['ENABLED', 'PAUSED']},
            'maxResults': 100,
        }, self._vnd('spCampaign'))

    def update_campaigns(self, campaigns: list[dict]) -> dict:
        return self.req('PUT', '/sp/campaigns', {'campaigns': campaigns},
                        self._vnd('spCampaign'))

    # Ad groups
    def list_ad_groups(self, campaign_id: str | None = None) -> dict:
        body: dict = {'stateFilter': {'include': ['ENABLED', 'PAUSED']}, 'maxResults': 100}
        if campaign_id:
            body['campaignIdFilter'] = {'include': [campaign_id]}
        return self.req('POST', '/sp/adGroups/list', body, self._vnd('spAdGroup'))

    # Keywords
    def list_keywords(self, campaign_id: str | None = None,
                      adgroup_id: str | None = None) -> dict:
        body: dict = {'stateFilter': {'include': ['ENABLED', 'PAUSED']}}
        if campaign_id:
            body['campaignIdFilter'] = {'include': [campaign_id]}
        if adgroup_id:
            body['adGroupIdFilter'] = {'include': [adgroup_id]}
        return self.req('POST', '/sp/keywords/list', body, self._vnd('spKeyword'))

    def update_keywords(self, keywords: list[dict]) -> dict:
        return self.req('PUT', '/sp/keywords', {'keywords': keywords},
                        self._vnd('spKeyword'))

    # Campaign-level negatives
    def list_campaign_negatives(self, campaign_id: str | None = None) -> dict:
        body: dict = {'stateFilter': {'include': ['ENABLED']}, 'maxResults': 200}
        if campaign_id:
            body['campaignIdFilter'] = {'include': [campaign_id]}
        return self.req('POST', '/sp/campaignNegativeKeywords/list', body,
                        self._vnd('spCampaignNegativeKeyword'))

    def create_campaign_negatives(self, keywords: list[dict]) -> dict:
        return self.req('POST', '/sp/campaignNegativeKeywords',
                        {'campaignNegativeKeywords': keywords},
                        self._vnd('spCampaignNegativeKeyword'))

    # Reporting (v3 async)
    REPORT_COLS = {
        'campaigns':   (['campaign'], 'spCampaigns',
                        ['impressions','clicks','cost','purchases7d','sales7d',
                         'campaignName','campaignId','campaignStatus']),
        'adgroups':    (['adGroup'],  'spAdGroups',
                        ['impressions','clicks','cost','purchases7d','sales7d',
                         'campaignName','adGroupName','adGroupId']),
        'keywords':    (['keyword'],  'spKeywords',
                        ['impressions','clicks','cost','purchases7d','sales7d',
                         'campaignName','adGroupName','keyword','matchType','keywordId','bid']),
        'searchterms': (['searchTerm'], 'spSearchTerms',
                        ['impressions','clicks','cost','purchases7d','sales7d',
                         'campaignName','adGroupName','keyword','matchType','searchTerm']),
    }

    def request_report(self, report_type: str, start: str, end: str,
                       campaign_id: str | None = None) -> str:
        group_by, type_id, columns = self.REPORT_COLS[report_type]
        body: dict = {
            'name': f'{report_type} {start}→{end}',
            'startDate': start,
            'endDate': end,
            'configuration': {
                'adProduct': 'SPONSORED_PRODUCTS',
                'groupBy': group_by,
                'columns': columns,
                'reportTypeId': type_id,
                'timeUnit': 'SUMMARY',
                'format': 'GZIP_JSON',
            },
        }
        if campaign_id:
            body['configuration']['filters'] = [
                {'field': 'campaignId', 'values': [campaign_id]}
            ]
        try:
            resp = self.req('POST', '/reporting/reports', body)
            return resp['reportId']
        except RuntimeError as e:
            msg = str(e)
            # 425 = duplicate: reuse the existing report ID
            if '425' in msg and 'duplicate' in msg.lower():
                import re as _re
                m = _re.search(r'[0-9a-f-]{36}', msg)
                if m:
                    dup_id = m.group(0)
                    print(f'Duplicate report — reusing: {dup_id}', file=sys.stderr)
                    return dup_id
            raise

    def wait_report(self, report_id: str, timeout_s: int = 360) -> list[dict]:
        deadline = time.time() + timeout_s
        attempt = 0
        while time.time() < deadline:
            attempt += 1
            time.sleep(10)
            info = self.req('GET', f'/reporting/reports/{report_id}')
            status = info.get('status', '')
            elapsed = int(time.time() - (deadline - timeout_s))
            print(f'  [{attempt}] {status} ({elapsed}s)', file=sys.stderr)
            if status == 'COMPLETED':
                raw = requests.get(info['url'], timeout=60).content
                try:
                    return json.loads(gzip.decompress(raw))
                except Exception:
                    return json.loads(raw)
            if status == 'FAILED':
                raise RuntimeError(f'Report failed: {info}')
        # Timeout — return report ID so caller can poll later
        print(f'\nReport still processing. Poll manually:', file=sys.stderr)
        print(f'  ads.py poll-report {report_id}', file=sys.stderr)
        sys.exit(2)  # exit code 2 = timeout (not error)

    def fetch_report(self, report_id: str) -> list[dict]:
        """Download a report that has already completed."""
        info = self.req('GET', f'/reporting/reports/{report_id}')
        status = info.get('status', '')
        if status != 'COMPLETED':
            print(f'Report status: {status}', file=sys.stderr)
            sys.exit(2)
        raw = requests.get(info['url'], timeout=60).content
        try:
            return json.loads(gzip.decompress(raw))
        except Exception:
            return json.loads(raw)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _enrich(rows: list[dict]) -> list[dict]:
    for row in rows:
        spend  = float(row.get('cost', 0) or 0)
        sales  = float(row.get('sales7d', 0) or 0)
        clicks = int(row.get('clicks', 0) or 0)
        imps   = int(row.get('impressions', 0) or 0)
        orders = int(row.get('purchases7d', 0) or 0)
        row['acos_pct'] = round(spend / sales * 100, 1) if sales > 0 else None
        row['roas']     = round(sales / spend, 2)        if spend > 0 else None
        row['ctr_pct']  = round(clicks / imps * 100, 2)  if imps > 0  else None
        row['cpc']      = round(spend / clicks, 2)        if clicks > 0 else None
        row['cvr_pct']  = round(orders / clicks * 100, 1) if clicks > 0 else None
    rows.sort(key=lambda x: float(x.get('cost', 0) or 0), reverse=True)
    return rows


def pp(obj):
    print(json.dumps(obj, indent=2, ensure_ascii=False))


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    missing = [k for k, v in [
        ('AMAZON_ADS_CLIENT_ID', CLIENT_ID),
        ('AMAZON_ADS_CLIENT_SECRET', CLIENT_SECRET),
        ('AMAZON_ADS_REFRESH_TOKEN', REFRESH_TOKEN),
    ] if not v]
    if missing:
        env_path = Path(__file__).parent.parent / '.env'
        print(
            f"Missing credentials: {', '.join(missing)}\n"
            "Please ask the skill owner to provide the Amazon Ads API credentials\n"
            f"and add them to: {env_path}\n"
            "Required vars:\n"
            "  AMAZON_ADS_CLIENT_ID=amzn1.application-oa2-client.xxx\n"
            "  AMAZON_ADS_CLIENT_SECRET=amzn1.oa2-cs.v1.xxx\n"
            "  AMAZON_ADS_REFRESH_TOKEN=Atzr|xxx\n"
            "  AMAZON_ADS_PROFILE_ID=<numeric-profile-id>   # run `ads.py profiles` to find\n"
            "  AMAZON_ADS_REGION=NA                          # NA | EU | FE\n"
            "\nSee SKILL.md Setup section for how to get credentials.",
            file=sys.stderr,
        )
        sys.exit(1)

    p = argparse.ArgumentParser(prog='ads.py')
    sp = p.add_subparsers(dest='cmd', required=True)

    sp.add_parser('profiles')

    pc = sp.add_parser('campaigns')
    pc.add_argument('--state', default='ENABLED,PAUSED',
                    help='ENABLED|PAUSED|ARCHIVED|ALL  (default: ENABLED,PAUSED)')

    pag = sp.add_parser('adgroups')
    pag.add_argument('--campaign', required=True, metavar='ID')

    pkw = sp.add_parser('keywords')
    pkw.add_argument('--campaign', metavar='ID')
    pkw.add_argument('--adgroup',  metavar='ID')

    pneg = sp.add_parser('negatives')
    pneg.add_argument('--campaign', metavar='ID')

    pb = sp.add_parser('set-bid')
    pb.add_argument('keyword_id')
    pb.add_argument('bid', type=float)

    ps = sp.add_parser('set-state')
    ps.add_argument('keyword_id')
    ps.add_argument('state', choices=['ENABLED', 'PAUSED', 'ARCHIVED'])

    pan = sp.add_parser('add-negative')
    pan.add_argument('--campaign', required=True, metavar='ID')
    pan.add_argument('--keyword',  required=True)
    pan.add_argument('--match',    default='EXACT', choices=['EXACT', 'PHRASE'])

    pr = sp.add_parser('report')
    pr.add_argument('type', choices=['campaigns', 'adgroups', 'keywords', 'searchterms'])
    pr.add_argument('--days',     type=int, default=30)
    pr.add_argument('--campaign', metavar='ID')

    pp2 = sp.add_parser('poll-report',
                        help='Download a previously requested report by ID')
    pp2.add_argument('report_id')

    args = p.parse_args()
    c = AdsClient()

    if args.cmd == 'profiles':
        pp([{
            'profileId': p['profileId'],
            'name':      p.get('accountInfo', {}).get('name'),
            'type':      p.get('accountInfo', {}).get('type'),
            'market':    p.get('countryCode'),
            'currency':  p.get('currencyCode'),
        } for p in c.list_profiles()])

    elif args.cmd == 'campaigns':
        states = (['ENABLED', 'PAUSED', 'ARCHIVED'] if args.state.upper() == 'ALL'
                  else [s.strip().upper() for s in args.state.split(',')])
        pp(c.list_campaigns(states).get('campaigns', []))

    elif args.cmd == 'adgroups':
        pp(c.list_ad_groups(args.campaign).get('adGroups', []))

    elif args.cmd == 'keywords':
        if not (args.campaign or args.adgroup):
            p.error('provide --campaign or --adgroup')
        pp(c.list_keywords(args.campaign, args.adgroup).get('keywords', []))

    elif args.cmd == 'negatives':
        pp(c.list_campaign_negatives(args.campaign).get('campaignNegativeKeywords', []))

    elif args.cmd == 'set-bid':
        pp(c.update_keywords([{'keywordId': args.keyword_id,
                                'bid': round(args.bid, 2)}]))

    elif args.cmd == 'set-state':
        pp(c.update_keywords([{'keywordId': args.keyword_id,
                                'state': args.state}]))

    elif args.cmd == 'add-negative':
        pp(c.create_campaign_negatives([{
            'campaignId':  args.campaign,
            'keywordText': args.keyword,
            'matchType':   args.match,
            'state':       'ENABLED',
        }]))

    elif args.cmd == 'report':
        end   = (date.today() - timedelta(days=1)).isoformat()
        start = (date.today() - timedelta(days=args.days)).isoformat()
        print(f'Requesting {args.type} report {start}→{end}…', file=sys.stderr)
        rid = c.request_report(args.type, start, end, args.campaign)
        print(f'Report ID: {rid}', file=sys.stderr)
        rows = c.wait_report(rid)
        pp(_enrich(rows))

    elif args.cmd == 'poll-report':
        rows = c.fetch_report(args.report_id)
        pp(_enrich(rows))


if __name__ == '__main__':
    main()
