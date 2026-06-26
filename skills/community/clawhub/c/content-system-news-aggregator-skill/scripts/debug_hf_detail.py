
import sys
from playwright.sync_api import sync_playwright

def inspect():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://huggingface.co/papers/2602.07026", timeout=30000)
        
        # Print Abstract
        # Look for abstract in common structures
        print("--- PAGE TEXT ---")
        # Find potential abstract
        
        # Try generic selector for paragraphs
        for p in page.query_selector_all("p"):
            txt = p.inner_text()
            if len(txt) > 200:
                print(f"POTENTIAL ABSTRACT (p) Found (len {len(txt)})")
        
        # Look for GitHub link
        # Usually a button with text "GitHub" or href containing github.com
        print("--- LINKS ---")
        for a in page.query_selector_all("a[href*='github.com']"):
            href = a.get_attribute('href')
            text = a.inner_text()
            print(f"GITHUB LINK: {text} -> {href}")
            
        print("--- BUTTONS ---")
        for btn in page.query_selector_all("button"):
            txt = btn.inner_text()
            print(f"BUTTON: {txt}")

        # Look for upvotes (usually near title or top right)
        # Often has an icon (heart or like) and a number
        print("--- NUMBERS ---")
        # Try finding elements with numbers
        # This is tricky without specific class, but let's dump text of top elements
        
        # Try specific heat selector if known (often div.rounded-xl containing number?)
        
        browser.close()
                
        # Try finding elements with class 'abstract'
        for el in page.query_selector_all(".abstract, [class*='abstract']"):
            print(f"ABSTRACT CLASS: {el.inner_text()}")

        # Try specific HF structure often used
        # Often it is a div covering the abstract
        
        browser.close()

if __name__ == "__main__":
    inspect()
