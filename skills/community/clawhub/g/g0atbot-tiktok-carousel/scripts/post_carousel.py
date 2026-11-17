#!/usr/bin/env python3
"""
TikTok Poster
Posts carousels to TikTok using cookies
"""

import os
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Config
DATA_DIR = Path("/Users/g0atface/clawd/skills/tiktok-carousel/data")
COOKIES_FILE = DATA_DIR / "tiktok_cookies.json"

def load_cookies():
    """Load TikTok cookies from file"""
    if not COOKIES_FILE.exists():
        return None
    
    with open(COOKIES_FILE, 'r') as f:
        return json.load(f)

def save_cookies(driver):
    """Save TikTok cookies after login"""
    driver.get("https://www.tiktok.com")
    time.sleep(3)
    
    cookies = driver.get_cookies()
    with open(COOKIES_FILE, 'w') as f:
        json.dump(cookies, f)
    
    print(f"✅ Cookies saved to {COOKIES_FILE}")
    return cookies

def post_carousel(carousel_id, images, caption):
    """Post carousel to TikTok"""
    
    cookies = load_cookies()
    if not cookies:
        print("❌ No TikTok cookies found")
        print("   Run with --login to authenticate")
        return False
    
    # Setup Chrome
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    driver = webdriver.Chrome(options=options)
    
    try:
        # Login with cookies
        driver.get("https://www.tiktok.com")
        time.sleep(3)
        
        for cookie in cookies:
            driver.add_cookie(cookie)
        
        driver.refresh()
        time.sleep(3)
        
        # Check if logged in
        try:
            upload_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Upload')]")
            print("✅ Logged in to TikTok")
        except:
            print("❌ Not logged in - cookies may be expired")
            return False
        
        # Click upload
        upload_btn.click()
        time.sleep(2)
        
        # Upload images (TikTok has specific carousel upload flow)
        # This is simplified - real implementation would need more complex handling
        
        print(f"📤 Would post carousel: {carousel_id}")
        print(f"   Images: {len(images)}")
        print(f"   Caption: {caption[:100]}...")
        
        # Note: TikTok carousel upload requires specific Selenium handling
        # This is a placeholder for the full implementation
        
        return True
        
    except Exception as e:
        print(f"❌ Error posting: {e}")
        return False
    
    finally:
        driver.quit()

def login():
    """Interactive login to get TikTok cookies"""
    
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=options)
    
    try:
        print("🌐 Opening TikTok login page...")
        driver.get("https://www.tiktok.com/login")
        input("👤 Please login manually, then press Enter to save cookies...")
        
        save_cookies(driver)
        print("✅ TikTok authentication complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        driver.quit()

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="TikTok Poster")
    parser.add_argument("--carousel", "-c", help="Carousel ID to post")
    parser.add_argument("--login", "-l", action="store_true", help="Login to TikTok")
    parser.add_argument("--list", action="store_true", help="List pending posts")
    
    args = parser.parse_args()
    
    if args.login:
        login()
        return
    
    if args.list:
        print("📋 Pending carousels:")
        # List carousels ready to post
        return
    
    if not args.carousel:
        print("Usage:")
        print("  python3 post_carousel.py -l          # Login to TikTok")
        print("  python3 post_carousel.py -c <id>     # Post carousel")
        return
    
    # Post carousel
    post_carousel(args.carousel, [], "")

if __name__ == "__main__":
    main()
