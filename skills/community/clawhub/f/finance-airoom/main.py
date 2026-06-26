#!/usr/bin/env python3
"""
AiroomLtd Global Finance Data Platform - WordPress Data Downloader

This tool is part of the airoom-ltd-global-finance-data-platform package.
It is designed to download financial data files from the airoom.ltd WordPress site.

The WordPress file downloader is a means to obtain financial data files for the platform.
"""
import sys
import json
import os
import time
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse

# Configuration paths
CONF_DIR = Path.home() / ".config" / "airoom-ltd-global-finance-data-platform"
CONF_FILE = CONF_DIR / "config.json"
DEFAULT_OUTPUT_DIR = "./downloads"

# Security: Blocked file extensions (potentially dangerous - will NOT be downloaded)
BLOCKED_EXTENSIONS = [
    '.exe', '.apk', '.bat', '.cmd', '.sh', '.bash', '.ps1',
    '.scr', '.pif', '.application', '.gadget', '.msi',
    '.msp', '.com', '.hta', '.vbs', '.vbe', '.js', '.jse',
    '.wsf', '.wsh', '.jar'
]

# Security: Allowed file extensions (safe financial data file types)
ALLOWED_EXTENSIONS = [
    '.csv', '.txt', '.xlsx', '.xls', '.doc', '.docx', '.pdf',
    '.zip', '.rar', '.7z', '.json', '.xml', '.png', '.jpg',
    '.jpeg', '.gif', '.bmp', '.svg', '.webp', '.ico',
    '.mp3', '.wav', '.ogg', '.flac',
    '.mp4', '.avi', '.mkv', '.mov', '.webm',
    '.html', '.htm', '.css'
]


def get_config():
    """Read configuration file, environment variables take priority"""
    config = {}

    # Environment variables have highest priority
    if os.getenv("WP_URL"):
        config["wordpress"] = {
            "url": os.getenv("WP_URL"),
            "username": os.getenv("WP_USERNAME", ""),
            "password": os.getenv("WP_PASSWORD", "")
        }
    if os.getenv("WP_TARGET_URL"):
        config["target"] = {
            "page_url": os.getenv("WP_TARGET_URL")
        }
    if os.getenv("WP_OUTPUT_DIR"):
        config["download"] = {
            "output_dir": os.getenv("WP_OUTPUT_DIR")
        }
    if os.getenv("WP_MAX_FILES"):
        config["download"] = config.get("download", {})
        config["download"]["max_files"] = int(os.getenv("WP_MAX_FILES", "0"))

    # Read configuration file
    if CONF_FILE.exists():
        try:
            file_config = json.loads(CONF_FILE.read_text(encoding="utf-8"))
            # Merge config, file config has lower priority than environment variables
            if "wordpress" in file_config and "wordpress" not in config:
                config["wordpress"] = file_config["wordpress"]
            if "target" in file_config and "target" not in config:
                config["target"] = file_config["target"]
            if "download" in file_config and "download" not in config:
                config["download"] = file_config["download"]
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Failed to read config file: {e}")

    # Set default values for airoom.ltd financial data platform
    if "wordpress" not in config:
        config["wordpress"] = {"url": "http://airoom.ltd", "username": "", "password": ""}
    if "target" not in config:
        # Default target for financial data
        config["target"] = {"page_url": "http://airoom.ltd/index.php/airoom/"}
    if "download" not in config:
        config["download"] = {"output_dir": DEFAULT_OUTPUT_DIR}

    return config


def print_config(config):
    """Display configuration information (hide sensitive data)"""
    print("=" * 60)
    print("AiroomLtd Global Finance Data Platform - Configuration")
    print("=" * 60)

    wp = config.get("wordpress", {})
    print(f"WordPress URL: {wp.get('url', 'Not set')}")
    print(f"Username: {wp.get('username', 'Not set (may not be required)')}")
    print(f"Password: {'*' * len(wp.get('password', '')) if wp.get('password') else 'Not set (may not be required)'}")

    target = config.get("target", {})
    print(f"Target Page: {target.get('page_url', 'Not set')}")

    download = config.get("download", {})
    print(f"Output Directory: {download.get('output_dir', 'Not set')}")

    max_files = download.get("max_files")
    if max_files and max_files > 0:
        print(f"Max Files: {max_files}")
    else:
        print(f"Max Files: Unlimited")

    # Security notice
    print("\n" + "=" * 60)
    print("SECURITY NOTICE:")
    print("- Executable files (.exe, .apk, .bat, .js, etc.) are BLOCKED")
    print("- Only safe financial data file types will be downloaded")
    print("- For http://airoom.ltd/index.php/airoom/: No login required")
    print("=" * 60)


def validate_config(config):
    """Validate configuration completeness"""
    target = config.get("target", {})
    if not target.get("page_url"):
        print("Error: Missing target page URL (WP_TARGET_URL)")
        return False

    wp = config.get("wordpress", {})
    base_url = wp.get("url", "")
    if not base_url:
        print("Error: Missing WordPress URL (WP_URL)")
        return False

    return True


def test_connection(config):
    """Test WordPress connection"""
    print("Testing WordPress connection...")

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Error: Playwright not installed")
        print("Please run: pip install playwright && playwright install chromium")
        return False

    wp = config.get("wordpress", {})
    base_url = wp.get("url", "")

    if not base_url:
        print("Error: WordPress URL not configured")
        return False

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Try to access target page directly (may not require login)
            target = config.get("target", {})
            page_url = target.get("page_url", base_url)
            print(f"Accessing target page: {page_url}")

            response = page.goto(page_url, wait_until="domcontentloaded", timeout=30000)

            if response and response.status < 400:
                print(f"Connection successful (Status: {response.status})")

                # Check if login is required
                if page.query_selector("#user_login"):
                    print("Note: This page requires WordPress login")
                    print("Configure WP_USERNAME and WP_PASSWORD if needed")
                else:
                    print("Page accessible - no login required")

                browser.close()
                return True
            else:
                print(f"Connection failed (Status: {response.status if response else 'N/A'})")
                browser.close()
                return False

    except ImportError:
        print("Error: Playwright not installed")
        print("Please run: pip install playwright && playwright install chromium")
        return False
    except Exception as e:
        print(f"Connection failed: {str(e)}")
        return False


def detect_file_type(url, text):
    """Detect file type from URL and text"""
    url_lower = url.lower()

    # Common financial data file extensions
    extensions = {
        '.csv': 'csv', '.txt': 'txt', '.xlsx': 'xlsx', '.xls': 'xls',
        '.doc': 'doc', '.docx': 'docx', '.pdf': 'pdf', '.zip': 'zip',
        '.rar': 'rar', '.7z': '7z', '.json': 'json', '.xml': 'xml',
        '.png': 'image', '.jpg': 'image', '.jpeg': 'image', '.gif': 'image',
        '.mp3': 'audio', '.mp4': 'video', '.html': 'html'
    }

    # Check extension in URL first
    for ext, file_type in extensions.items():
        if ext in url_lower:
            return file_type

    return 'unknown'


def is_file_extension_blocked(filename):
    """Check if file extension is blocked for security"""
    filename_lower = filename.lower()

    # Check blocked extensions (dangerous file types)
    for ext in BLOCKED_EXTENSIONS:
        if filename_lower.endswith(ext):
            return True

    return False


def is_downloadable_link(href, text):
    """Determine if a link is a downloadable financial data file"""
    if not href:
        return False

    # Exclude non-download links
    exclude_patterns = ['#', 'javascript:', 'mailto:', 'tel:', '/wp-admin/', '/wp-login.php']
    for pattern in exclude_patterns:
        if pattern in href.lower():
            return False

    # Exclude anchor links
    if href.startswith('#'):
        return False

    href_lower = href.lower()

    # Check for file extensions (both allowed and blocked for initial detection)
    all_extensions = ALLOWED_EXTENSIONS + BLOCKED_EXTENSIONS

    # Check if URL ends with any known extension
    for ext in all_extensions:
        if href_lower.endswith(ext):
            return True

    # Check for WordPress media library links (financial data storage)
    wp_patterns = ['/wp-content/uploads/', '/wp-content/attachments/', 'attachment_id=']
    if any(pattern in href_lower for pattern in wp_patterns):
        return True

    # Check text for download keywords
    text_lower = text.lower()
    download_keywords = ['download', '下载', 'file', '文件', 'attachment', '附件', '数据', 'data']
    if any(keyword in text_lower for keyword in download_keywords):
        return True

    return False


def download_files(config):
    """Main file download process for financial data"""
    print("=" * 60)
    print("AiroomLtd Global Finance Data Platform")
    print("Starting Financial Data Download...")
    print("=" * 60)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Error: Playwright not installed")
        print("Please run: pip install playwright && playwright install chromium")
        return False

    wp = config.get("wordpress", {})
    target = config.get("target", {})
    download = config.get("download", {})

    base_url = wp.get("url", "")
    username = wp.get("username", "")
    password = wp.get("password", "")
    page_url = target.get("page_url", "")
    output_dir = Path(download.get("output_dir", DEFAULT_OUTPUT_DIR))
    max_files = download.get("max_files", 0)

    # Validate URL is from expected domain for security
    if base_url and page_url:
        parsed_base = urlparse(base_url)
        parsed_page = urlparse(page_url)

        # Ensure target URL is on the same domain as base URL
        if parsed_base.netloc and parsed_page.netloc:
            if parsed_base.netloc != parsed_page.netloc:
                print("Security Error: Target URL must be on the same domain as the WordPress URL")
                return False

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output Directory: {output_dir.absolute()}")

    if max_files > 0:
        print(f"Max Files to Download: {max_files}")
    else:
        print("Max Files: Unlimited")

    # Show blocked file types
    print(f"\nSecurity: Blocking dangerous file types: {', '.join(BLOCKED_EXTENSIONS[:5])}...")

    # File name deduplication counter
    file_counter = {}

    try:
        with sync_playwright() as p:
            # Launch browser
            print("\nLaunching browser...")
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(accept_downloads=True)
            page = context.new_page()

            # Step 1: Try to access page directly (no login may be required)
            print("\n[Step 1] Accessing target page...")
            print(f"URL: {page_url}")

            try:
                page.goto(page_url, wait_until="domcontentloaded", timeout=30000)
                print("Page loaded")

                # Check if login is required
                requires_login = page.query_selector("#user_login") is not None

                if requires_login and username and password:
                    # Login required and credentials provided
                    print("\n[Step 2] Logging into WordPress...")
                    login_url = f"{base_url}/wp-login.php"

                    try:
                        page.goto(login_url, wait_until="domcontentloaded", timeout=30000)
                        print("Entering login credentials...")
                        page.fill("#user_login", username)
                        page.fill("#user_pass", password)
                        page.click("#wp-submit")

                        try:
                            page.wait_for_url("**/wp-admin/**", timeout=15000)
                            print("Login successful")
                        except:
                            error_msg = page.query_selector("#login_error")
                            if error_msg:
                                print("Login failed: Invalid username or password")
                                browser.close()
                                return False
                            print("Login completed")

                        # Navigate back to target page
                        page.goto(page_url, wait_until="domcontentloaded", timeout=30000)
                        print("Returned to target page")

                    except Exception as e:
                        print(f"Login failed: {str(e)}")
                        browser.close()
                        return False
                elif requires_login:
                    print("Note: Page requires login, but no credentials provided")
                    print("Some content may still be accessible")
                else:
                    print("Note: No login required for this page")

                # Wait for page content to fully load
                time.sleep(2)

            except Exception as e:
                print(f"Page access failed: {str(e)}")
                browser.close()
                return False

            # Step 3: Find all downloadable financial data file links
            print("\n[Step 3] Searching for downloadable financial data files...")

            file_links = []

            # Method 1: Find all links with file extensions
            all_extensions = ALLOWED_EXTENSIONS + BLOCKED_EXTENSIONS

            for ext in all_extensions:
                selectors = [
                    f"a[href$='{ext}']",
                    f"a[href$='{ext.upper()}']"
                ]
                for selector in selectors:
                    try:
                        links = page.query_selector_all(selector)
                        for link in links:
                            href = link.get_attribute("href")
                            if href and not any(l["href"] == href for l in file_links):
                                text = link.inner_text().strip() or link.get_attribute("title") or ""
                                file_type = detect_file_type(href, text)
                                file_links.append({
                                    "href": href,
                                    "text": text,
                                    "type": file_type
                                })
                    except:
                        pass

            # Method 2: Find WordPress media library attachment links
            attachment_selectors = [
                "a[href*='/wp-content/uploads/']",
                "a[href*='/wp-content/attachments/']"
            ]

            for selector in attachment_selectors:
                try:
                    links = page.query_selector_all(selector)
                    for link in links:
                        href = link.get_attribute("href")
                        if href and is_downloadable_link(href, link.inner_text()) and not any(l["href"] == href for l in file_links):
                            text = link.inner_text().strip() or link.get_attribute("title") or ""
                            file_type = detect_file_type(href, text)
                            file_links.append({
                                "href": href,
                                "text": text,
                                "type": file_type
                            })
                except:
                    pass

            # Method 3: Find links with download-related text
            download_texts = ['download', 'download', 'file', '文件', 'attachment', '附件', '数据', 'data']
            for text in download_texts:
                try:
                    links = page.query_selector_all(f"a:has-text('{text}')")
                    for link in links:
                        href = link.get_attribute("href")
                        if href and is_downloadable_link(href, link.inner_text()) and not any(l["href"] == href for l in file_links):
                            link_text = link.inner_text().strip()
                            file_type = detect_file_type(href, link_text)
                            file_links.append({
                                "href": href,
                                "text": link_text,
                                "type": file_type
                            })
                except:
                    pass

            print(f"Found {len(file_links)} potential download links")

            # Filter out blocked file types (keep only safe financial data)
            safe_file_links = []
            blocked_count = 0

            for file_info in file_links:
                filename = file_info["href"].split('/')[-1]
                if is_file_extension_blocked(filename):
                    blocked_count += 1
                    print(f"  [BLOCKED] {filename} - dangerous file type")
                else:
                    safe_file_links.append(file_info)

            if blocked_count > 0:
                print(f"\nSecurity: Blocked {blocked_count} dangerous file(s)")

            file_links = safe_file_links

            if not file_links:
                print("No downloadable financial data files found")
                print("\nPage content preview:")
                content = page.content()
                print(content[:2000])
                browser.close()
                return False

            # Display found files
            print("\nFinancial data files to download:")
            for i, file_info in enumerate(file_links):
                print(f"  {i+1}. [{file_info['type']}] {file_info['text'] or file_info['href']}")

            # Step 4: Download files
            print("\n[Step 4] Downloading financial data files...")

            downloaded_files = []
            failed_files = []

            # Determine number of files to download
            files_to_download = file_links
            if max_files > 0:
                files_to_download = file_links[:max_files]
                print(f"Will download first {len(files_to_download)} file(s) (found {len(file_links)} total)")
            else:
                print(f"Will download all {len(files_to_download)} file(s)")

            for i, file_info in enumerate(files_to_download):
                href = file_info["href"]
                file_type = file_info["type"]
                display_name = file_info["text"] or href

                # Final security check
                filename = href.split('/')[-1]
                if is_file_extension_blocked(filename):
                    print(f"\nSkipping {i+1}: {filename} - blocked for security")
                    continue

                print(f"\nDownloading {i+1}/{len(files_to_download)}: {display_name}")

                try:
                    # Create download task
                    with page.expect_download(timeout=60000) as download_info:
                        page.goto(href, wait_until="domcontentloaded", timeout=30000)

                    # Get download info
                    download = download_info.value

                    # Generate unique filename
                    original_name = download.suggested_filename
                    if not original_name or original_name == "unknown":
                        original_name = href.split('/')[-1]
                        if '?' in original_name:
                            original_name = original_name.split('?')[0]
                        if not original_name or '.' not in original_name:
                            original_name = f"download_{i+1}.{file_type}" if file_type != 'unknown' else f"download_{i+1}.bin"

                    # Handle filename conflicts
                    if original_name in file_counter:
                        file_counter[original_name] += 1
                        name, ext = os.path.splitext(original_name)
                        original_name = f"{name}_{file_counter[original_name]}{ext}"
                    else:
                        file_counter[original_name] = 0

                    # Save file
                    save_path = output_dir / original_name
                    download.save_as(str(save_path))

                    # Verify file
                    if save_path.exists() and save_path.stat().st_size > 0:
                        file_size = save_path.stat().st_size
                        print(f"Downloaded: {original_name} ({file_size} bytes)")
                        downloaded_files.append({
                            "name": original_name,
                            "path": str(save_path),
                            "size": file_size
                        })
                    else:
                        print(f"File save failed or file is empty")
                        failed_files.append(href)

                except Exception as e:
                    print(f"Download failed: {str(e)}")
                    failed_files.append(href)

            # Close browser
            browser.close()

            # Output results
            print("\n" + "=" * 60)
            print("Download Summary - AiroomLtd Global Finance Data Platform")
            print("=" * 60)
            print(f"Successfully downloaded: {len(downloaded_files)} file(s)")
            print(f"Failed: {len(failed_files)} file(s)")

            if downloaded_files:
                print("\nDownloaded financial data files:")
                for f in downloaded_files:
                    print(f"  - {f['name']} ({f['size']} bytes)")
                    print(f"    Path: {f['path']}")

            if failed_files:
                print("\nFailed file links:")
                for href in failed_files:
                    print(f"  - {href}")

            print("=" * 60)

            return len(downloaded_files) > 0

    except Exception as e:
        print(f"Execution failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main program entry"""
    # Read configuration
    config = get_config()

    # Parse command line arguments
    if len(sys.argv) < 2:
        # Default: show configuration
        print_config(config)
        print("\nUsage:")
        print("  python3 main.py download  - Download financial data")
        print("  python3 main.py test      - Test connection")
        print("  python3 main.py config    - Show configuration")
        return

    command = sys.argv[1]

    if command == "config":
        print_config(config)

    elif command == "test":
        if not validate_config(config):
            return
        test_connection(config)

    elif command == "download":
        if not validate_config(config):
            return
        success = download_files(config)
        if success:
            print("\nFinancial data download completed successfully")
            sys.exit(0)
        else:
            print("\nDownload task failed")
            sys.exit(1)

    else:
        print(f"Unknown command: {command}")
        print("Available commands: download, test, config")


if __name__ == "__main__":
    main()
