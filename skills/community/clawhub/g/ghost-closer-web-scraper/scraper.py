#!/usr/bin/env python3
"""
Ghost Closer Web Scraper — OpenClaw ClawHub Skill
Scrapes Google Maps, Facebook, and Instagram for complete business intelligence.
Connects to existing Chrome on port 9222.
"""

import asyncio
import json
import os
import re
import sys
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

# Load env
load_dotenv(Path("/Users/edwin/.openclaw/workspace/dreams-arts/.env"))

try:
    from playwright.async_api import async_playwright, TimeoutError as PWTimeout
except ImportError:
    print(json.dumps({"error": "playwright not installed. Run: pip install playwright"}), file=sys.stderr)
    sys.exit(1)


CDP_URL = "http://localhost:9222"
REQUEST_TIMEOUT = 15_000  # 15s per navigation
MAX_RETRIES = 3


class GhostCloserScraper:
    """Scrapes business data from Google Maps, Facebook, and Instagram."""

    def __init__(self):
        self.browser = None
        self.context = None

    async def _connect(self):
        """Connect to existing Chrome via CDP."""
        pw = await async_playwright().start()
        self.browser = await pw.chromium.connect_over_cdp(CDP_URL)
        self.context = self.browser.contexts[0] if self.browser.contexts else await self.browser.new_context()

    async def _new_page(self):
        page = await self.context.new_page()
        page.set_default_timeout(REQUEST_TIMEOUT)
        return page

    async def _safe_goto(self, page, url, retries=MAX_RETRIES):
        """Navigate with retries."""
        for attempt in range(retries):
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=REQUEST_TIMEOUT)
                return True
            except Exception as e:
                if attempt == retries - 1:
                    print(f"Failed to load {url}: {e}", file=sys.stderr)
                    return False
                await asyncio.sleep(1 * (attempt + 1))
        return False

    # ── Google Maps ──────────────────────────────────────────────────────

    async def scrape_google_maps(self, business_name: str, location: str) -> dict | None:
        """Scrape Google Maps for business data."""
        page = await self._new_page()
        try:
            query = urllib.parse.quote_plus(f"{business_name} {location}")
            url = f"https://www.google.com/maps/search/{query}"

            if not await self._safe_goto(page, url):
                return None

            # Wait for results to load
            await asyncio.sleep(3)

            # Click the first result if we're on a search results page
            try:
                first_result = page.locator('[role="feed"] > div').first
                await first_result.click(timeout=5000)
                await asyncio.sleep(2)
            except Exception:
                pass  # May already be on a single result page

            data = await page.evaluate(r"""() => {
                const result = {};

                // Business name
                const nameEl = document.querySelector('h1');
                if (nameEl) result.name = nameEl.textContent.trim();

                // Rating
                const ratingEl = document.querySelector('[role="img"][aria-label*="star"]');
                if (ratingEl) {
                    const match = ratingEl.getAttribute('aria-label').match(/([\d.]+)/);
                    if (match) result.rating = parseFloat(match[1]);
                }

                // Review count
                const reviewEl = document.querySelector('button[aria-label*="review"]');
                if (reviewEl) {
                    const match = reviewEl.textContent.match(/([\d,]+)/);
                    if (match) result.review_count = parseInt(match[1].replace(/,/g, ''));
                }

                // Address
                const addrBtn = document.querySelector('button[data-item-id="address"]');
                if (addrBtn) result.address = addrBtn.textContent.trim();

                // Phone
                const phoneBtn = document.querySelector('button[data-item-id*="phone"]');
                if (phoneBtn) result.phone = phoneBtn.textContent.trim();

                // Website
                const webBtn = document.querySelector('a[data-item-id="authority"]');
                if (webBtn) result.website = webBtn.getAttribute('href');

                // Hours — try the hours table
                const hoursRows = document.querySelectorAll('table[aria-label*="hour"] tr, .OqCZI tr');
                if (hoursRows.length > 0) {
                    result.hours = {};
                    hoursRows.forEach(row => {
                        const cells = row.querySelectorAll('td');
                        if (cells.length >= 2) {
                            result.hours[cells[0].textContent.trim()] = cells[1].textContent.trim();
                        }
                    });
                }

                // Categories
                const catEl = document.querySelector('button[jsaction*="category"]');
                if (catEl) result.categories = [catEl.textContent.trim()];

                // Photo URLs from the gallery
                const photos = [];
                document.querySelectorAll('button[aria-label*="Photo"] img, .p-d83-Iiigned img, div[role="img"] img').forEach(img => {
                    const src = img.src || img.getAttribute('data-src');
                    if (src && src.startsWith('http') && !src.includes('data:')) {
                        photos.push(src);
                    }
                });
                if (photos.length > 0) result.photo_urls = [...new Set(photos)].slice(0, 10);

                return result;
            }""")

            # Also try to grab hours by clicking the hours section
            if not data.get("hours"):
                try:
                    hours_btn = page.locator('[data-item-id*="oh"], [aria-label*="hour"]').first
                    await hours_btn.click(timeout=3000)
                    await asyncio.sleep(1)
                    hours_data = await page.evaluate(r"""() => {
                        const hours = {};
                        document.querySelectorAll('table tr').forEach(row => {
                            const cells = row.querySelectorAll('td');
                            if (cells.length >= 2) {
                                hours[cells[0].textContent.trim()] = cells[1].textContent.trim();
                            }
                        });
                        return Object.keys(hours).length > 0 ? hours : null;
                    }""")
                    if hours_data:
                        data["hours"] = hours_data
                except Exception:
                    pass

            return data if data.get("name") else None

        except Exception as e:
            print(f"Google Maps error: {e}", file=sys.stderr)
            return None
        finally:
            await page.close()

    # ── Facebook ─────────────────────────────────────────────────────────

    async def scrape_facebook(self, business_name: str, location: str) -> dict | None:
        """Search Facebook for the business page and scrape data."""
        page = await self._new_page()
        try:
            query = urllib.parse.quote_plus(f"{business_name} {location}")
            url = f"https://www.facebook.com/search/pages/?q={query}"

            if not await self._safe_goto(page, url):
                return None

            await asyncio.sleep(3)

            # Try to find and click the first page result
            try:
                first_link = page.locator('a[role="presentation"]').first
                page_url = await first_link.get_attribute("href", timeout=5000)
                await first_link.click(timeout=5000)
                await asyncio.sleep(3)
            except Exception:
                # Try alternative: direct search
                alt_url = f"https://www.facebook.com/search/top/?q={query}"
                if not await self._safe_goto(page, alt_url):
                    return None
                await asyncio.sleep(3)
                try:
                    first_link = page.locator('a[role="presentation"]').first
                    page_url = await first_link.get_attribute("href", timeout=5000)
                    await first_link.click(timeout=5000)
                    await asyncio.sleep(3)
                except Exception:
                    return None

            data = await page.evaluate(r"""() => {
                const result = {};

                // Page URL
                result.page_url = window.location.href.split('?')[0];

                // Followers/likes from the page intro
                const allText = document.body.innerText;

                const followersMatch = allText.match(/([\d,.]+[KMB]?)\s+follower/i);
                if (followersMatch) {
                    let val = followersMatch[1].replace(/,/g, '');
                    if (val.endsWith('K')) val = parseFloat(val) * 1000;
                    else if (val.endsWith('M')) val = parseFloat(val) * 1000000;
                    result.followers = parseInt(val);
                }

                const likesMatch = allText.match(/([\d,.]+[KMB]?)\s+like/i);
                if (likesMatch) {
                    let val = likesMatch[1].replace(/,/g, '');
                    if (val.endsWith('K')) val = parseFloat(val) * 1000;
                    else if (val.endsWith('M')) val = parseFloat(val) * 1000000;
                    result.likes = parseInt(val);
                }

                // Logo — profile image
                const profileImg = document.querySelector('image[preserveAspectRatio], svg image, [role="img"] image');
                if (profileImg) {
                    result.logo_url = profileImg.getAttribute('xlink:href') || profileImg.getAttribute('href');
                }

                // Recent posts — grab first few visible post texts
                const posts = [];
                document.querySelectorAll('[data-ad-preview="message"], [data-ad-comet-preview="message"]').forEach(el => {
                    const text = el.textContent.trim();
                    if (text.length > 10) posts.push({text: text.substring(0, 300)});
                });
                if (posts.length > 0) result.recent_posts = posts.slice(0, 5);

                return result;
            }""")

            return data if data.get("page_url") else None

        except Exception as e:
            print(f"Facebook error: {e}", file=sys.stderr)
            return None
        finally:
            await page.close()

    # ── Instagram ────────────────────────────────────────────────────────

    async def scrape_instagram(self, business_name: str) -> dict | None:
        """Search Google for the business Instagram handle."""
        page = await self._new_page()
        try:
            query = urllib.parse.quote_plus(f"{business_name} instagram.com")
            url = f"https://www.google.com/search?q={query}"

            if not await self._safe_goto(page, url):
                return None

            await asyncio.sleep(2)

            # Look for instagram.com links in Google results
            ig_data = await page.evaluate(r"""() => {
                const links = document.querySelectorAll('a[href*="instagram.com/"]');
                for (const link of links) {
                    const href = link.getAttribute('href');
                    const match = href.match(/instagram\\.com\\/([\\w.]+)/);
                    if (match && !['p', 'explore', 'reel', 'stories', 'accounts'].includes(match[1])) {
                        return {
                            handle: '@' + match[1],
                            profile_url: 'https://www.instagram.com/' + match[1]
                        };
                    }
                }
                return null;
            }""")

            return ig_data

        except Exception as e:
            print(f"Instagram error: {e}", file=sys.stderr)
            return None
        finally:
            await page.close()

    # ── Services/Menu ────────────────────────────────────────────────────

    async def scrape_services(self, website_url: str) -> list | None:
        """Try to scrape services or menu from the business website."""
        if not website_url:
            return None

        page = await self._new_page()
        try:
            if not await self._safe_goto(page, website_url):
                return None

            await asyncio.sleep(2)

            # Look for common menu/services pages
            services_data = await page.evaluate(r"""() => {
                const items = [];

                // Look for price-like patterns
                const priceRegex = /\\$\\d+/;
                const allElements = document.querySelectorAll('li, p, td, div, span');

                for (const el of allElements) {
                    const text = el.textContent.trim();
                    if (priceRegex.test(text) && text.length < 200 && text.length > 5) {
                        // Clean up and avoid duplicates
                        const clean = text.replace(/\\s+/g, ' ').trim();
                        if (!items.includes(clean)) {
                            items.push(clean);
                        }
                    }
                    if (items.length >= 20) break;
                }

                return items.length > 0 ? items : null;
            }""")

            # If no prices found, look for services/menu links and follow them
            if not services_data:
                try:
                    menu_link = page.locator('a:has-text("menu"), a:has-text("services"), a:has-text("pricing"), a:has-text("servicios")').first
                    await menu_link.click(timeout=3000)
                    await asyncio.sleep(2)

                    services_data = await page.evaluate(r"""() => {
                        const items = [];
                        const els = document.querySelectorAll('li, h3, h4, .service, .menu-item, [class*="service"], [class*="menu"]');
                        for (const el of els) {
                            const text = el.textContent.trim().replace(/\\s+/g, ' ');
                            if (text.length > 3 && text.length < 200 && !items.includes(text)) {
                                items.push(text);
                            }
                            if (items.length >= 20) break;
                        }
                        return items.length > 0 ? items : null;
                    }""")
                except Exception:
                    pass

            return services_data

        except Exception as e:
            print(f"Services scrape error: {e}", file=sys.stderr)
            return None
        finally:
            await page.close()

    # ── Main Runner ──────────────────────────────────────────────────────

    async def run(self, business_name: str, location: str) -> dict:
        """Run full scrape pipeline and return structured JSON."""
        await self._connect()

        result = {
            "business_name": business_name,
            "location_query": location,
            "google_maps": None,
            "facebook": None,
            "instagram": None,
            "services_or_menu": None,
            "scraped_at": datetime.now(timezone.utc).isoformat(),
        }

        # Run Google Maps first (we need the website URL for services)
        print(f"Scraping Google Maps for '{business_name}' in '{location}'...", file=sys.stderr)
        result["google_maps"] = await self.scrape_google_maps(business_name, location)

        # Run Facebook and Instagram in parallel
        print("Scraping Facebook and Instagram...", file=sys.stderr)
        fb_task = self.scrape_facebook(business_name, location)
        ig_task = self.scrape_instagram(business_name)
        fb_result, ig_result = await asyncio.gather(fb_task, ig_task, return_exceptions=True)

        result["facebook"] = fb_result if not isinstance(fb_result, Exception) else None
        result["instagram"] = ig_result if not isinstance(ig_result, Exception) else None

        # Scrape services from website if available
        website = None
        if result["google_maps"] and result["google_maps"].get("website"):
            website = result["google_maps"]["website"]
        if website:
            print(f"Scraping services from {website}...", file=sys.stderr)
            result["services_or_menu"] = await self.scrape_services(website)

        return result


async def main():
    if len(sys.argv) < 3:
        print("Usage: python scraper.py \"Business Name\" \"City, State\"", file=sys.stderr)
        sys.exit(1)

    business_name = sys.argv[1]
    location = sys.argv[2]

    scraper = GhostCloserScraper()
    result = await scraper.run(business_name, location)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
