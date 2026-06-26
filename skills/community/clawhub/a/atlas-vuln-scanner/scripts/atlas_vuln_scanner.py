#!/usr/bin/env python3
"""Atlas Smart Contract Vulnerability Pattern Scanner v0.1.

Heuristic Solidity scanner. Produces markdown + JSON reports.
No network calls. No secrets. No exploit generation.
"""
from __future__ import annotations
import argparse, json, re
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime

@dataclass
class Pattern:
    id: str
    title: str
    severity: str
    confidence: str
    description: str
    regexes: list[str]
    advice: str

PATTERNS = [
    Pattern('T1.1','Reentrancy / external call review','High','Medium','External value/token calls that may require checks-effects-interactions or reentrancy protection.',[r'\.call\s*\{\s*value\s*:', r'\.call\s*\(', r'\.send\s*\(', r'\.transfer\s*\('],'Ensure state updates happen before external calls and affected functions use nonReentrant where needed.'),
    Pattern('T1.2','Access control review','High','Medium','Public/external admin-like functions or role logic that may need authorization review.',[r'function\s+(set|update|configure|pause|unpause|mint|burn|sweep|upgrade|setFee|setOracle|setAdmin)\w*\s*\([^)]*\)\s*(public|external)(?![^\{;]*(onlyOwner|onlyRole|auth|requiresAuth|adminOnly|governance|manager))', r'require\s*\([^;]*(msg\.sender|owner\(\))\s*!='],'Confirm privileged operations have correct access control and no inverse/threshold logic bug.'),
    Pattern('T1.3','Oracle manipulation / spot-price risk','Critical','Medium','Potential use of spot AMM reserves/slot0 or missing staleness/TWAP protections.',[r'(?<!function )getReserves\s*\(', r'\.slot0\s*\(', r'latestRoundData\s*\(', r'answer\s*=|price\s*='],'Confirm TWAP/staleness/liquidity bounds; spot prices are unsafe for lending/liquidation decisions.'),
    Pattern('T1.4','Unchecked low-level or token call','High','Medium','Low-level/token transfer calls may ignore success or non-standard ERC20 returns.',[r'\.call\s*\(', r'\.delegatecall\s*\(', r'\.staticcall\s*\(', r'\.transferFrom\s*\(', r'\.transfer\s*\('],'Check return values or use SafeERC20 / explicit require(success).'),
    Pattern('T1.5','Accounting/share math review','High','Low','Share, index, exchange-rate, or rounding math that may cause accounting drift.',[r'share|shares|exchangeRate|index|accumulator|totalAssets|totalSupply', r'\*\s*1e(18|27)|/\s*1e(18|27)', r'Math\.mulDiv|mulDiv'],'Manually validate rounding direction, empty-market edge cases, and share-price manipulation.'),
    Pattern('T2.1','Unchecked arithmetic / unsafe casts','Medium','Medium','Unchecked blocks or narrowing casts require bounds review.',[r'unchecked\s*\{', r'uint(8|16|32|64|96|128)\s*\(', r'int(8|16|32|64|96|128)\s*\('],'Verify explicit bounds before narrowing casts and unchecked arithmetic.'),
    Pattern('T2.2','Delegatecall / arbitrary execution','High','Medium','delegatecall/executor patterns can create upgrade or function-injection risk.',[r'delegatecall\s*\(', r'execute\s*\([^)]*bytes', r'functionCall\s*\('],'Validate target allowlists, selector filtering, and authorization.'),
    Pattern('T2.3','Pause/emergency coverage gap','Medium','Low','Pause mechanisms may not cover every value-moving path.',[r'Pausable|whenNotPaused|paused\s*\(', r'pause\s*\(|unpause\s*\('],'Map all deposit/withdraw/borrow/liquidate paths and confirm pause coverage.'),
    Pattern('T2.4','Initialization / upgradeability review','High','Medium','Upgradeable contracts need initialization guards and safe upgrade authorization.',[r'initialize\s*\(', r'reinitializer\s*\(', r'_disableInitializers\s*\(', r'UUPSUpgradeable|TransparentUpgradeableProxy'],'Confirm initializer cannot be replayed and implementation is locked.'),
    Pattern('T3.1','Timestamp / block-number dependency','Low','Low','Time/block assumptions can create manipulation or boundary bugs.',[r'block\.timestamp', r'block\.number'],'Review tolerances, boundary conditions, and miner/validator influence.'),
    Pattern('T3.2','Large loop / gas griefing','Medium','Low','Unbounded loops over dynamic arrays can become DoS vectors.',[r'for\s*\([^;]+;[^;]+\.length', r'while\s*\('],'Check max collection size and whether anyone can grow the looped array.'),
]

EXCLUDE_PARTS = {'node_modules', 'lib', 'out', 'cache', '.git'}

def iter_sol_files(target: Path, include_tests: bool):
    for p in target.rglob('*.sol'):
        parts=set(p.parts)
        if parts & EXCLUDE_PARTS:
            continue
        low=str(p).lower()
        if not include_tests and any(x in low for x in ['/test/', '/tests/', '/mock', 'mock/', '.t.sol']):
            continue
        yield p

def line_matches(text: str, pattern: Pattern):
    flags=[]
    lines=text.splitlines()
    for idx,line in enumerate(lines, start=1):
        for rgx in pattern.regexes:
            if re.search(rgx, line, flags=re.IGNORECASE):
                context='\n'.join(lines[max(0,idx-2):min(len(lines),idx+1)])
                flags.append({'line': idx, 'match': line.strip()[:220], 'regex': rgx, 'context': context})
                break
    return flags

def scan(target: Path, include_tests=False):
    findings=[]
    files=list(iter_sol_files(target, include_tests))
    for f in files:
        try: text=f.read_text(errors='ignore')
        except Exception: continue
        rel=str(f.relative_to(target)) if f.is_relative_to(target) else str(f)
        for pat in PATTERNS:
            ms=line_matches(text, pat)
            for m in ms:
                findings.append({'file':rel, **m, **asdict(pat)})
    return files, findings

def md_escape(s): return s.replace('|','\\|')

def write_reports(target: Path, out: Path, files, findings):
    out.mkdir(parents=True, exist_ok=True)
    now=datetime.now().strftime('%Y-%m-%d %H:%M')
    bysev={}
    for f in findings: bysev[f['severity']]=bysev.get(f['severity'],0)+1
    summary=f"""# Atlas Vulnerability Scan Report

**Target:** `{target}`  
**Scanned:** {now}  
**Scanner:** Atlas Vuln Scanner v0.1  
**Files scanned:** {len(files)}  
**Flags:** {len(findings)}

## Read this first

This is a heuristic first-pass scan, not a full audit. Every flag below requires manual validation before disclosure, bounty submission, or severity claims.

## Summary by severity

- Critical: {bysev.get('Critical',0)}
- High: {bysev.get('High',0)}
- Medium: {bysev.get('Medium',0)}
- Low: {bysev.get('Low',0)}

## Prioritized flags

"""
    rows=[]
    order={'Critical':0,'High':1,'Medium':2,'Low':3}
    for i,f in enumerate(sorted(findings,key=lambda x:(order.get(x['severity'],9), x['file'], x['line'])),1):
        rows.append(f"### {i}. {f['title']} — {f['severity']} / {f['confidence']} confidence\n\n- **Location:** `{f['file']}:{f['line']}`\n- **Evidence:** `{md_escape(f['match'])}`\n- **Why flagged:** {f['description']}\n- **Manual validation:** {f['advice']}\n")
    (out/'scan-report.md').write_text(summary + ('\n'.join(rows) if rows else 'No heuristic flags found.\n'))

    top=sorted(findings,key=lambda x:(order.get(x['severity'],9), x['confidence']!='Medium', x['file']))[:8]
    fc="# Atlas Finding Candidates\n\nThese are candidates for manual review, not verified findings.\n\n"
    for i,f in enumerate(top,1):
        fc+=f"## Candidate {i}: {f['title']}\n\n**Pattern:** {f['id']}  \n**Severity hypothesis:** {f['severity']}  \n**Confidence:** {f['confidence']}  \n**Source:** `{f['file']}:{f['line']}`  \n**Flag type:** static heuristic\n\n### Summary\n{f['description']}\n\n### Evidence\n```solidity\n{f['context']}\n```\n\n### Validation needed\n{f['advice']}\n\n### Disclosure guardrail\nDo not submit externally until exploitability and impact are manually verified.\n\n"
    (out/'finding-candidates.md').write_text(fc)

    exec_md=f"""# Executive Security Summary

**Target:** `{target}`  
**Date:** {now}  
**Scope:** {len(files)} Solidity files  

## Top risks to review

"""
    for f in top[:3]:
        exec_md+=f"- **{f['title']} ({f['severity']})** — `{f['file']}:{f['line']}`. {f['description']}\n"
    exec_md+="""
## What this means

The scanner found areas worth human review before launch, audit, or bounty submission. These are not confirmed vulnerabilities yet. The next step is to validate exploitability and business impact for the highest-severity candidates.

## Recommended next step

Have Atlas or a qualified auditor manually review the top candidates, remove false positives, and convert any confirmed issue into a responsible disclosure or remediation ticket.
"""
    (out/'exec-summary.md').write_text(exec_md)
    (out/'scanner-log.json').write_text(json.dumps({'target':str(target),'scanned_at':now,'files_scanned':len(files),'findings':findings}, indent=2))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--target', required=True)
    ap.add_argument('--output', required=True)
    ap.add_argument('--include-tests', action='store_true')
    args=ap.parse_args()
    target=Path(args.target).expanduser().resolve()
    out=Path(args.output).expanduser().resolve()
    if not target.exists(): raise SystemExit(f'target not found: {target}')
    files, findings=scan(target, args.include_tests)
    write_reports(target,out,files,findings)
    print(json.dumps({'status':'ok','files_scanned':len(files),'flags':len(findings),'output':str(out)}, indent=2))
if __name__=='__main__': main()
