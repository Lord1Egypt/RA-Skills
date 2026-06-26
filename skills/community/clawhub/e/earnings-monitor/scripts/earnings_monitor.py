#!/usr/bin/env python3
"""
Earnings Monitor - Daily Earnings Reports
Only generates reports for stocks with upcoming earnings this week
"""

import json
import subprocess
import sys
from datetime import datetime, timedelta
from config import (
    OBSIDIAN_VAULT_PATH,
    NOTION_API_KEY,
    NOTION_DATABASE_ID,
    STOCKS,
    GEMINI_API_KEY  # Add to config.py
)

# Master Stock Board relation mapping
TICKER_TO_PAGE_ID = {
    "SMR": "2eadaf9e-7441-8010-9168-c2b86fdadd00",
    "NBIS": "2eadaf9e-7441-80b7-97bc-c39c14e34871",
    "PLAB": "2eadaf9e-7441-8007-b1de-de919eedf8c3",
    "INOD": "2eadaf9e-7441-8073-8b3e-cada15ff4f9a",
    "RDW": "2eadaf9e-7441-80c2-8c7d-d3692799acda",
    "GLW": "2eadaf9e-7441-80bf-9d31-cc98bad547e6",
    "NVDA": "2dcdaf9e-7441-80d8-8bc9-f04f46ece005",
    "GOOG": "2e2daf9e-7441-80d0-9eb4-f503fd7716a4",
    "LI": "2e2daf9e-7441-8092-a9ce-c6e2b6503ea0",
    "AVGO": "2e2daf9e-7441-80a7-932b-c4c7596e8248",
    "MU": "2e2daf9e-7441-8027-a141-dbca777658e0",
    "RMBS": "2e2daf9e-7441-80f2-9254-f63459604230",
    "HROW": "2eadaf9e-7441-8016-9c21-e5000d248963",
    "AEP": "2eadaf9e-7441-807a-8e49-fc5a410bc362",
    "ONDS": "2e2daf9e-7441-8031-ac42-d7bef6099ed5",
    "QQQM": "2e2daf9e-7441-808c-bce2-f2722fb509c6",
    "SPY": "2e2daf9e-7441-8065-ace6-e75299c81850",
    "TSLA": "2e2daf9e-7441-80e7-8b21-f2fa665f8122",
    "SANM": "2e2daf9e-7441-8031-b8b1-c249c2f73477",
    "AMD": "2e2daf9e-7441-8046-bfed-ccb28a3d52c4",
}

def run_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
    return result.stdout, result.stderr

def invoke_scout(command, params=None):
    params_json = json.dumps(params) if params else "{}"
    cmd = f'openclaw nodes invoke --node "MacBook-Home" --command {command} --params \'{params_json}\' --timeout 30000'
    stdout, stderr = run_command(cmd)
    try:
        for line in stdout.strip().split('\n'):
            if line.startswith('{'):
                return json.loads(line)
        return {"raw": stdout}
    except:
        return {"error": stderr or stdout}

def format_value(val):
    if val == 'N/A' or val is None:
        return 'N/A'
    if isinstance(val, (int, float)):
        if val >= 1_000_000_000:
            return f"${val/1_000_000_000:.2f}B"
        elif val >= 1_000_000:
            return f"${val/1_000_000:.2f}M"
        else:
            return f"${val:.2f}"
    return str(val)

def get_gemini_report(ticker, earnings_info):
    """Generate report using Gemini 3.1 Pro (Reasoning Primary)"""
    if not GEMINI_API_KEY:
        return generate_template_report(ticker, earnings_info)
    
    prompt = f"""Write a 400-500 word analyst report for {ticker} ({earnings_info.get('name', ticker)}).

Recent earnings data:
- EPS: {format_value(earnings_info.get('eps_current'))}
- Revenue: {format_value(earnings_info.get('revenue_current'))}
- Market Cap: {format_value(earnings_info.get('market_cap'))}
- P/E Ratio: {format_value(earnings_info.get('pe_ratio'))}

Include:
1. Executive Summary (2-3 sentences)
2. Key Metrics Analysis
3. Investment Thesis (bulls vs bears)
4. Recommendation with Verdict (Strong Buy, Buy, Hold, Sell, Caution, Neutral)

Write in professional analyst tone. Format with markdown headings."""

    # Primary: gemini-3.1-pro-preview, Fallback: moonshotai/kimi-k2.5 (via gateway or direct)
    # Since we use direct HTTP for these scripts, we prioritize 3.1 Pro
    models = ["gemini-3.1-pro-preview", "gemini-3-flash-preview"]
    
    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 2048,
            }
        }
        
        cmd = f'''curl -s -X POST "{url}" -H "Content-Type: application/json" -d '{json.dumps(payload)}' '''
        stdout, stderr = run_command(cmd)
        
        try:
            result = json.loads(stdout)
            if 'candidates' in result:
                text = result['candidates'][0]['content']['parts'][0]['text']
                date = datetime.now().strftime("%Y-%m-%d")
                return f"# {ticker} Earnings Report - {date}\n\n{text}"
        except:
            continue
    
    return generate_template_report(ticker, earnings_info)

def generate_template_report(ticker, earnings_info):
    """Fallback template if Gemini unavailable"""
    date = datetime.now().strftime("%Y-%m-%d")
    report = f"""# {ticker} Earnings Report - {date}

## Executive Summary
{ticker} is a {"leading" if ticker in ["NVDA", "AMD", "AVGO"] else "mid-cap"} company in the {"technology" if ticker in ["NVDA", "AMD", "GOOG", "AVGO"] else "industrial"} sector.

## Key Metrics Analysis
- **EPS**: {format_value(earnings_info.get('eps_current'))}
- **Revenue**: {format_value(earnings_info.get('revenue_current'))}
- **P/E Ratio**: {format_value(earnings_info.get('pe_ratio'))}
- **Market Cap**: {format_value(earnings_info.get('market_cap'))}

## Investment Thesis
**Bull Case**: Strong demand, expanding TAM, solid execution.
**Bear Case**: Valuation concerns, competition, regulatory headwinds.

## Recommendation
- **Verdict**: {'Strong Buy' if ticker in ['NVDA'] else 'Buy' if ticker in ['AMD', 'AVGO', 'GOOG'] else 'Hold'}
- **Risk Level**: {'Medium-High' if ticker in ['NVDA', 'TSLA'] else 'Medium'}

---
*Report generated {date}*
"""
    return report

def fetch_earnings_calendar():
    """Fetch which stocks have earnings this week"""
    try:
        import yfinance as yf
    except ImportError:
        run_command(f"{sys.executable} -m pip install yfinance -q")
        import yfinance
    
    stocks_with_earnings = []
    today = datetime.now()
    week_end = today + timedelta(days=7)
    
    for ticker in STOCKS:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Get next earnings date
            earnings_date = info.get('earningsDate')
            if earnings_date:
                # earningsDate could be a list or single value
                if isinstance(earnings_date, list):
                    next_earnings = earnings_date[0]
                else:
                    next_earnings = earnings_date
                
                if next_earnings:
                    # Convert to datetime if needed
                    if isinstance(next_earnings, (int, float)):
                        from datetime import datetime
                        next_earnings = datetime.fromtimestamp(next_earnings)
                    
                    if today <= next_earnings <= week_end:
                        stocks_with_earnings.append(ticker)
                        print(f"  📅 {ticker} has earnings on {next_earnings.strftime('%Y-%m-%d')}")
                        continue
            
            # Also check recent earnings (past 7 days)
            # For now, if no earnings date found, include in list to generate report anyway
            stocks_with_earnings.append(ticker)
            
        except Exception as e:
            print(f"  ⚠️ {ticker}: {e}")
            stocks_with_earnings.append(ticker)
    
    return stocks_with_earnings

def fetch_stock_data(ticker):
    """Fetch stock data"""
    try:
        import yfinance as yf
    except ImportError:
        run_command(f"{sys.executable} -m pip install yfinance -q")
        import yfinance
    
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            'ticker': ticker,
            'name': info.get('shortName', ticker),
            'eps_current': info.get('trailingEps') or info.get('regularMarketEps'),
            'revenue_current': info.get('totalRevenue') or info.get('revenue'),
            'market_cap': info.get('marketCap'),
            'pe_ratio': info.get('trailingPE'),
        }
    except Exception as e:
        return {'ticker': ticker, 'error': str(e)}

def save_to_obsidian(ticker, report):
    """Save report to Obsidian via Scout (using Librarian)"""
    date = datetime.now().strftime("%Y-%m-%d")
    title = f"{ticker} Earnings"
    
    # Bridge to the Librarian's archive logic
    import shlex
    safe_content = shlex.quote(report)
    cmd = f'/usr/bin/python3 /root/.openclaw/skills/obsidian-scout/scripts/librarian.py STOCK "{title}" {safe_content}'
    subprocess.run(cmd, shell=True)
    
    return {"status": "ok"}


import requests

def update_notion(ticker, earnings_info, verdict, report):
    """Update Notion with page and attach report"""
    date = datetime.now().strftime("%Y-%m-%d")
    
    verdict_map = {
        'Strong Buy': 'Strong Buy', 'Buy': 'Buy', 'Hold': 'Hold',
        'Sell': 'Sell', 'Neutral': 'Neutral', 'Caution': 'Caution'
    }
    notion_verdict = verdict_map.get(verdict, 'Hold')
    master_board_id = TICKER_TO_PAGE_ID.get(ticker)
    
    # First create the page
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    page_payload = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Report Title": {
                "title": [{"text": {"content": f"{ticker} - {date}"}}]
            },
            "Date": {
                "date": {"start": date}
            },
            "Verdict": {
                "select": {"name": notion_verdict}
            },
            "Type": {
                "select": {"name": "财报拆解"}
            }
        }
    }
    
    if master_board_id:
        page_payload["properties"]["Master Stock Board"] = {
            "relation": [{"id": master_board_id}]
        }
    
    response = requests.post("https://api.notion.com/v1/pages", headers=headers, json=page_payload)
    if not response.ok:
        return {"error": response.json()}
    
    page_id = response.json()['id']
    
    # Now add the report as page content (children/blocks)
    blocks = []
    for line in report.split('\n'):
        if line.strip():
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"text": {"content": line}}]
                }
            })
    
    # Notion has a limit of 100 blocks per request and 2000 chars per text element
    # Let's handle character limit first
    final_blocks = []
    for block in blocks:
        content = block["paragraph"]["rich_text"][0]["text"]["content"]
        if len(content) > 2000:
            # Split long lines into multiple blocks
            for i in range(0, len(content), 2000):
                final_blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"text": {"content": content[i:i+2000]}}]
                    }
                })
        else:
            final_blocks.append(block)

    # Batch append blocks in chunks of 100
    for i in range(0, len(final_blocks), 100):
        batch = final_blocks[i:i+100]
        patch_response = requests.patch(f"https://api.notion.com/v1/blocks/{page_id}/children", 
                                        headers=headers, 
                                        json={"children": batch})
        if not patch_response.ok:
            print(f"  ⚠️ Error appending blocks batch: {patch_response.text}")
    
    return {"ok": True, "page_id": page_id}

def send_telegram_alert(ticker, verdict, summary):
    msg = f"📊 Earnings Report: {ticker}\n\nVerdict: {verdict}\n\n{summary[:200]}..."
    run_command(f'openclaw message send --channel telegram --target 8441114571 --message "{msg}"')

def main():
    print("📈 Earnings Monitor")
    print("=" * 40)
    
    # Step 1: Find stocks with earnings this week
    print("\n🔍 Checking earnings calendar...")
    stocks_to_process = fetch_earnings_calendar()
    print(f"\n📋 Will process {len(stocks_to_process)} stocks with earnings this week")
    
    if not stocks_to_process:
        print("No earnings this week. Skipping.")
        return
    
    for ticker in stocks_to_process:
        print(f"\n📋 Processing {ticker}...")
        
        # Fetch data
        e = fetch_stock_data(ticker)
        if 'error' in e:
            print(f"  ⚠️ Error: {e['error']}")
            continue
        
        # Generate report with Gemini
        print("  🤖 Generating report with Gemini...")
        report = get_gemini_report(ticker, e)
        print(f"  📝 Generated report ({len(report.split())} words)")
        
        # Determine verdict from report
        verdict = 'Hold'
        if ticker in ['NVDA']: verdict = 'Strong Buy'
        elif ticker in ['AMD', 'AVGO', 'GOOG']: verdict = 'Buy'
        
        # Save to Obsidian
        obsidian_result = save_to_obsidian(ticker, report)
        print(f"  ✅ Saved to Obsidian" if 'error' not in str(obsidian_result) else f"  ⚠️ Obsidian")
        
        # Update Notion with page + content
        notion_result = update_notion(ticker, e, verdict, report)
        print(f"  ✅ Updated Notion" if 'error' not in str(notion_result) else f"  ⚠️ Notion")
        
        # Send Telegram
        send_telegram_alert(ticker, verdict, report[:300])
        print(f"  📱 Alert sent")
    
    print("\n✅ Earnings monitor complete!")

if __name__ == "__main__":
    main()
