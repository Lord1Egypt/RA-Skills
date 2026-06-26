import yfinance as yf
import pandas as pd
import json
import os
import requests
from io import StringIO
from datetime import datetime, timedelta
from tqdm import tqdm
from typing import List, Tuple, Dict, Any

def get_sp500_tickers() -> List[str]:
    """Fetch S&P 500 constituent tickers from Wikipedia"""
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    tables = pd.read_html(StringIO(response.text))
    df = tables[0]
    
    # Clean ticker format (e.g., BRK.B to BRK-B for yfinance)
    tickers = df['Symbol'].str.replace('.', '-', regex=False).tolist()
    return tickers

def get_top_100_by_market_cap(tickers: List[str]) -> List[Dict[str, Any]]:
    """Get top 100 stocks by market capitalization and cache their info payload."""
    print("Fetching S&P 500 market cap data in batches...")
    stock_data = []
    
    # For speed, download multiple stocks at once (yfinance supports batch)
    tickers_obj = yf.Tickers(" ".join(tickers))
    
    # Add tqdm progress bar to monitor market cap retrieval
    for ticker in tqdm(tickers, desc="Filtering top 100 by market cap", unit="stocks"):
        try:
            # Save the info dictionary to avoid fetching it again later
            info = tickers_obj.tickers[ticker].info
            cap = info.get('marketCap', 0)
            if cap > 0:
                stock_data.append({
                    'Ticker': ticker, 
                    'Name': info.get('shortName', ticker), 
                    'MarketCap': cap,
                    'Info': info 
                })
        except Exception:
            continue
            
    # Sort and take top 100
    stock_data.sort(key=lambda x: x['MarketCap'], reverse=True)
    return stock_data[:100]

def check_canslim(ticker: str, info: Dict[str, Any]) -> Tuple[List[str], List[str], float, Dict[str, str]]:
    """
    Check CANSLIM criteria for a single stock using pre-fetched info.
    Returns: (met criteria list, missed criteria list, price, check details)
    """
    try:
        # We no longer call stock.info here, saving a network request!
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y")
        
        # Edge Case: Ensure the stock has been trading for roughly a full year (~250 trading days)
        if hist.empty or len(hist) < 250:
            return [], ["Insufficient trading data (needs 1 year)"], 0.0, {}
            
        met = []
        missed = []
        details = {}
        current_price = float(hist['Close'].iloc[-1])
        
        # C: Current Quarterly Earnings (quarterly EPS YoY growth > 20%)
        eps_growth = info.get('earningsQuarterlyGrowth', 0)
        details['C_EPS_Growth'] = f"{eps_growth*100:.1f}%" if eps_growth else "N/A"
        if eps_growth and eps_growth > 0.20:
            met.append('C')
        else:
            missed.append('C')
            
        # A: Annual Earnings Growth (using revenue growth as proxy)
        rev_growth = info.get('revenueGrowth', 0)
        details['A_Rev_Growth'] = f"{rev_growth*100:.1f}%" if rev_growth else "N/A"
        if rev_growth and rev_growth > 0.20:
            met.append('A')
        else:
            missed.append('A')
            
        # N: New Product / New High (price near 52-week high)
        high_52w = info.get('fiftyTwoWeekHigh', hist['High'].max())
        if high_52w and high_52w > 0:  # Prevent ZeroDivisionError
            price_to_high = current_price / high_52w
            details['N_Pct_of_High'] = f"{price_to_high*100:.1f}%"
            if price_to_high > 0.85:
                met.append('N')
            else:
                missed.append('N')
        else:
            details['N_Pct_of_High'] = "N/A"
            missed.append('N')
            
        # S: Supply and Demand (today's volume > 10-day average volume)
        vol_today = hist['Volume'].iloc[-1]
        vol_10d_avg = hist['Volume'].tail(10).mean()
        details['S_Vol_Ratio'] = f"{vol_today / vol_10d_avg:.2f}x" if vol_10d_avg else "N/A"
        if vol_10d_avg and vol_today > vol_10d_avg:
            met.append('S')
        else:
            missed.append('S')
            
        # L: Leader or Laggard (52-week total return > 20%)
        price_1y_ago = hist['Close'].iloc[0]
        if price_1y_ago and price_1y_ago > 0:  # Prevent ZeroDivisionError
            return_1y = (current_price - price_1y_ago) / price_1y_ago
            details['L_1y_Return'] = f"{return_1y*100:.1f}%"
            if return_1y > 0.20:
                met.append('L')
            else:
                missed.append('L')
        else:
            details['L_1y_Return'] = "N/A"
            missed.append('L')
            
        # I: Institutional Sponsorship (institutional ownership > 50%)
        inst_own = info.get('heldPercentInstitutions', 0)
        details['I_Inst_Own'] = f"{inst_own*100:.1f}%" if inst_own else "N/A"
        if inst_own and inst_own > 0.50:
            met.append('I')
        else:
            missed.append('I')
            
        # M: Market Direction (stock above 200-day moving average)
        ma_200 = info.get('twoHundredDayAverage', hist['Close'].tail(200).mean())
        details['M_Above_200MA'] = "Yes" if current_price > ma_200 else "No"
        if current_price > ma_200:
            met.append('M')
        else:
            missed.append('M')
            
        return met, missed, current_price, details
        
    except Exception as e:
        return [], [f"Error: {str(e)}"], 0.0, {}

def main() -> None:
    print("Starting CANSLIM S&P 500 analysis module...")
    
    # 1. Get S&P 500 list
    sp500_tickers = get_sp500_tickers()
    
    # 2. Filter top 100 by market cap
    # Now returns a list of dictionaries with cached 'Info' 
    top_100_data = get_top_100_by_market_cap(sp500_tickers)
    
    results = []
    print(f"\nPreparing to analyze CANSLIM indicators for Top {len(top_100_data)} stocks...")
    
    # 3. Analyze CANSLIM for each stock, passing the cached 'Info' to prevent double-fetching
    for row in tqdm(top_100_data, desc="Calculating CANSLIM", unit="stocks"):
        ticker = row['Ticker']
        name = row['Name']
        market_cap = row['MarketCap']
        info = row['Info']
        
        met, missed, price, details = check_canslim(ticker, info)
        
        results.append({
            "Ticker": ticker,
            "Name": name,
            "MarketCap": f"${market_cap / 1e9:.1f}B",
            "Price": f"${price:.2f}",
            "Met_Criteria": ", ".join(met) if met else "None",
            "Missed_Criteria": ", ".join(missed) if missed else "None",
            "Score": len(met),
            "Details": details
        })
        
    # 4. Sort by number of criteria met
    results_sorted = sorted(results, key=lambda x: x['Score'], reverse=True)
    
    # 5. Output to JSON file (in parent directory if running from Scripts folder)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    output_dir = parent_dir if script_dir.endswith('Scripts') else script_dir
    output_file = os.path.join(output_dir, "canslim_results.json")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results_sorted, f, ensure_ascii=False, indent=4)
        
    print(f"\nAnalysis complete! Results saved to {os.path.basename(output_file)}")

if __name__ == "__main__":
    main()
