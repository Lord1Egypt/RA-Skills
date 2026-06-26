import sys
import time
from playwright.sync_api import sync_playwright

def analyze_token(token_address):
    url = f"https://dexscreener.com/solana/{token_address}"
    print(f"Analyzing token: {token_address}")
    print(f"URL: {url}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            page.goto(url, wait_until="networkidle")
            time.sleep(5)  # Wait for dynamic content
            
            # Basic info extraction
            title = page.title()
            print(f"Page Title: {title}")
            
            # Look for security indicators (placeholders for real selectors)
            # DexScreener often shows 'Liquidity', 'FDV', 'Mkt Cap'
            # We can also look for 'Mint Revoked', 'Freeze Authority Disabled' if available in the UI
            
            content = page.content()
            
            indicators = {
                "liquidity": "Not found",
                "fdv": "Not found",
                "security_checks": []
            }
            
            # This is a simplified analysis logic
            if "Liquidity" in content:
                indicators["liquidity"] = "Present (Check value on UI)"
            
            # Example of what to look for in a rug-pull context:
            # 1. Liquidity Locked/Burnt
            # 2. Top holders concentration
            # 3. Mint/Freeze authority status
            
            print("\n--- Potential Risk Indicators ---")
            print(f"Liquidity Status: {indicators['liquidity']}")
            
            # Suggesting manual verification for critical data
            print("\nManual verification recommended for:")
            print("- Liquidity Lock status")
            print("- Top 10 holders percentage")
            print("- Mint/Freeze authority status")
            
        except Exception as e:
            print(f"Error during analysis: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 analyze_token.py <token_address>")
    else:
        analyze_token(sys.argv[1])
