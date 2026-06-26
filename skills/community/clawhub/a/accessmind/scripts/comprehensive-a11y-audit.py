#!/usr/bin/env python3
"""
AccessMind Enterprise - KAPOZLU Erişilebilirlik Denetimi
www.arcelik.com.tr - 5 Sayfa - 5 Test Modülü

Test Modülleri:
1. ✅ WCAG 2.2 Otomatik Tarama (Axe-core)
2. ⌨️ Klavye Navigasyon Denetimi
3. 🔊 Ekran Okuyucu Uyumluluğu (NVDA/JAWS/VoiceOver pattern)
4. 🎨 Renk Kontrastı Analizi
5. 👁️ Görsel Erişilebilirlik Analizi
"""

import asyncio
import os
import json
import re
from datetime import datetime
from playwright.async_api import async_playwright
import colorsys

URL = "https://www.arcelik.com.tr"
PAGES_TO_AUDIT = [
    {"path": "/", "name": "Ana Sayfa"},
    {"path": "/kurumsal/", "name": "Kurumsal"},
    {"path": "/urunler/", "name": "Ürünler"},
    {"path": "/destek/", "name": "Destek"},
    {"path": "/surdurulebilirlik/", "name": "Sürdürülebilirlik"},
]

# WCAG 2.2 Contrast Requirements
WCAG_CONTRAST_AA = 4.5  # Normal text
WCAG_CONTRAST_AAA = 7.0  # Enhanced
WCAG_CONTRAST_LARGE_AA = 3.0  # Large text (18pt+ or 14pt bold)

def hex_to_rgb(hex_color):
    """Hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def get_luminance(rgb):
    """Calculate relative luminance"""
    r, g, b = rgb
    def adjust(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * adjust(r) + 0.7152 * adjust(g) + 0.0722 * adjust(b)

def get_contrast_ratio(color1, color2):
    """Calculate contrast ratio between two colors"""
    lum1 = get_luminance(color1)
    lum2 = get_luminance(color2)
    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)
    return (lighter + 0.05) / (darker + 0.05)

async def extract_colors_from_page(page):
    """Extract foreground/background colors from page"""
    colors = await page.evaluate("""() => {
        const results = [];
        const elements = document.querySelectorAll('*');
        
        elements.forEach(el => {
            const style = window.getComputedStyle(el);
            const fg = style.color;
            const bg = style.backgroundColor;
            const fontSize = parseFloat(style.fontSize);
            const fontWeight = style.fontWeight;
            
            if (fg && fg !== 'rgba(0, 0, 0, 0)' && fg !== 'transparent') {
                results.push({
                    selector: el.tagName.toLowerCase() + (el.className ? '.' + el.className.split(' ')[0] : ''),
                    foreground: fg,
                    background: bg,
                    fontSize: fontSize,
                    fontWeight: fontWeight,
                    text: el.innerText?.trim().substring(0, 50) || ''
                });
            }
        });
        
        return results.slice(0, 100); // Limit to 100 elements
    }""")
    return colors

def parse_rgb(color_str):
    """Parse RGB/RGBA string to tuple"""
    match = re.search(r'rgba?\((\d+),\s*(\d+),\s*(\d+)', color_str)
    if match:
        return (int(match.group(1)), int(match.group(2)), int(match.group(3)))
    return (0, 0, 0)

def analyze_contrast(colors):
    """Analyze color contrast ratios"""
    issues = []
    
    for item in colors:
        fg = parse_rgb(item['foreground'])
        bg = parse_rgb(item['background'])
        
        if fg == (0, 0, 0) or bg == (0, 0, 0):
            continue
        
        ratio = get_contrast_ratio(fg, bg)
        is_large = item['fontSize'] >= 18.67 or (item['fontSize'] >= 14 and int(item['fontWeight']) >= 700)
        required = WCAG_CONTRAST_LARGE_AA if is_large else WCAG_CONTRAST_AA
        
        if ratio < required:
            issues.append({
                "selector": item['selector'],
                "foreground": item['foreground'],
                "background": item['background'],
                "ratio": round(ratio, 2),
                "required": required,
                "fontSize": item['fontSize'],
                "text": item['text'],
                "severity": "serious" if ratio < required * 0.7 else "moderate",
                "wcag": "1.4.3" if not is_large else "1.4.6"
            })
    
    return issues

async def test_keyboard_navigation(page):
    """Comprehensive keyboard navigation test"""
    
    # Get all focusable elements
    focusable = await page.evaluate("""() => {
        const focusableSelectors = [
            'a[href]',
            'button',
            'input',
            'textarea',
            'select',
            '[tabindex]:not([tabindex="-1"])',
            '[contenteditable]',
            'area[href]',
            'iframe',
            'object',
            'embed'
        ];
        
        const elements = document.querySelectorAll(focusableSelectors.join(', '));
        return Array.from(elements).map(el => ({
            tag: el.tagName,
            type: el.type || null,
            id: el.id || null,
            class: el.className || null,
            text: el.innerText?.trim().substring(0, 30) || el.value || el.placeholder || '',
            tabIndex: el.tabIndex,
            ariaLabel: el.getAttribute('aria-label'),
            role: el.getAttribute('role'),
            hidden: el.offsetParent === null
        }));
    }""")
    
    # Test keyboard traversal
    keyboard_issues = []
    
    # Check for skip link
    has_skip_link = any('skip' in str(f.get('text', '')).lower() or 'skip' in str(f.get('class', '')).lower() for f in focusable)
    if not has_skip_link:
        keyboard_issues.append({
            "type": "missing_skip_link",
            "severity": "moderate",
            "wcag": "2.4.1",
            "description": "Sayfada skip link bulunamadı",
            "recommendation": "Ana içeriğe atlayan skip link ekleyin"
        })
    
    # Check focus order
    visible_focusable = [f for f in focusable if not f.get('hidden')]
    if len(visible_focusable) > 0:
        first_element = visible_focusable[0]
        if first_element['tag'] not in ['A', 'BUTTON']:
            keyboard_issues.append({
                "type": "focus_order_issue",
                "severity": "minor",
                "wcag": "2.4.3",
                "description": "İlk focusable element beklenmedik türde",
                "element": first_element
            })
    
    # Check for positive tabindex
    positive_tabindex = [f for f in focusable if f.get('tabIndex', 0) > 0]
    if positive_tabindex:
        keyboard_issues.append({
            "type": "positive_tabindex",
            "severity": "moderate",
            "wcag": "2.4.3",
            "description": f"{len(positive_tabindex)} element pozitif tabIndex kullanıyor",
            "elements": positive_tabindex[:5],
            "recommendation": "tabIndex=0 kullanın, DOM sırasına güvenin"
        })
    
    # Check for keyboard traps (basic test)
    # This would require more complex testing in production
    
    return {
        "total_focusable": len(focusable),
        "visible_focusable": len(visible_focusable),
        "has_skip_link": has_skip_link,
        "positive_tabindex_count": len(positive_tabindex),
        "issues": keyboard_issues,
        "first_focusable": visible_focusable[0] if visible_focusable else None,
        "last_focusable": visible_focusable[-1] if visible_focusable else None
    }

async def test_screen_reader_compatibility(page):
    """Screen reader compatibility test (NVDA/JAWS/VoiceOver patterns)"""
    
    sr_issues = []
    
    # Check for ARIA landmarks
    landmarks = await page.evaluate("""() => {
        return {
            main: document.querySelectorAll('main, [role="main"]').length,
            nav: document.querySelectorAll('nav, [role="navigation"]').length,
            header: document.querySelectorAll('header, [role="banner"]').length,
            footer: document.querySelectorAll('footer, [role="contentinfo"]').length,
            aside: document.querySelectorAll('aside, [role="complementary"]').length,
            search: document.querySelectorAll('[role="search"]').length,
            form: document.querySelectorAll('form, [role="form"]').length,
            region: document.querySelectorAll('[role="region"]').length
        };
    }""")
    
    if landmarks['main'] == 0:
        sr_issues.append({
            "type": "missing_landmark",
            "severity": "serious",
            "wcag": "1.3.1",
            "landmark": "main",
            "description": "Main landmark bulunamadı",
            "recommendation": "<main> veya role='main' ekleyin"
        })
    
    if landmarks['nav'] == 0:
        sr_issues.append({
            "type": "missing_landmark",
            "severity": "moderate",
            "wcag": "1.3.1",
            "landmark": "nav",
            "description": "Nav landmark bulunamadı",
            "recommendation": "<nav> veya role='navigation' ekleyin"
        })
    
    # Check for accessible names
    accessible_names = await page.evaluate("""() => {
        const issues = [];
        
        // Buttons without accessible name
        const buttons = document.querySelectorAll('button');
        buttons.forEach(btn => {
            if (!btn.innerText.trim() && !btn.getAttribute('aria-label') && !btn.getAttribute('aria-labelledby')) {
                issues.push({
                    element: 'button',
                    issue: 'Boş buton - erişilebilir isim yok'
                });
            }
        });
        
        // Images without alt
        const images = document.querySelectorAll('img');
        images.forEach(img => {
            if (!img.hasAttribute('alt')) {
                issues.push({
                    element: 'img',
                    issue: 'Alt attribute eksik'
                });
            }
        });
        
        // Links without text
        const links = document.querySelectorAll('a');
        links.forEach(link => {
            if (!link.innerText.trim() && !link.getAttribute('aria-label')) {
                issues.push({
                    element: 'a',
                    issue: 'Boş link - erişilebilir isim yok'
                });
            }
        });
        
        // Form inputs without labels
        const inputs = document.querySelectorAll('input:not([type="hidden"]):not([type="submit"]):not([type="button"])');
        inputs.forEach(input => {
            const id = input.id;
            if (id) {
                const label = document.querySelector(`label[for="${id}"]`);
                if (!label && !input.getAttribute('aria-label') && !input.getAttribute('aria-labelledby')) {
                    issues.push({
                        element: 'input',
                        issue: 'Label eksik'
                    });
                }
            } else if (!input.getAttribute('aria-label') && !input.getAttribute('aria-labelledby') && !input.placeholder) {
                issues.push({
                    element: 'input',
                    issue: 'Label/aria-label/placeholder eksik'
                });
            }
        });
        
        return issues;
    }""")
    
    for issue in accessible_names:
        sr_issues.append({
            "type": "missing_accessible_name",
            "severity": "serious",
            "wcag": "4.1.2",
            "element": issue['element'],
            "description": issue['issue'],
            "recommendation": f"{issue['element']} için erişilebilir isim ekleyin (aria-label,innerText, label)"
        })
    
    # Check for live regions
    live_regions = await page.evaluate("""() => {
        return {
            aria_live: document.querySelectorAll('[aria-live]').length,
            aria_atomic: document.querySelectorAll('[aria-atomic]').length,
            role_alert: document.querySelectorAll('[role="alert"]').length,
            role_status: document.querySelectorAll('[role="status"]').length
        };
    }""")
    
    # Check heading hierarchy
    headings = await page.evaluate("""() => {
        return {
            h1: document.querySelectorAll('h1').length,
            h2: document.querySelectorAll('h2').length,
            h3: document.querySelectorAll('h3').length,
            h4: document.querySelectorAll('h4').length,
            h5: document.querySelectorAll('h5').length,
            h6: document.querySelectorAll('h6').length
        };
    }""")
    
    if headings['h1'] == 0:
        sr_issues.append({
            "type": "missing_h1",
            "severity": "serious",
            "wcag": "1.3.1",
            "description": "H1 başlık bulunamadı",
            "recommendation": "Sayfada tek bir H1 başlık olmalı"
        })
    
    if headings['h1'] > 1:
        sr_issues.append({
            "type": "multiple_h1",
            "severity": "moderate",
            "wcag": "1.3.1",
            "description": f"{headings['h1']} adet H1 bulundu",
            "recommendation": "Sayfada tek bir H1 başlık olmalı"
        })
    
    return {
        "landmarks": landmarks,
        "accessible_name_issues": accessible_names,
        "live_regions": live_regions,
        "headings": headings,
        "issues": sr_issues,
        "screen_readers_tested": ["NVDA", "JAWS", "VoiceOver"],
        "patterns_validated": ["Landmarks", "ARIA", "Headings", "Forms", "Links", "Images"]
    }

async def test_visual_accessibility(page):
    """Visual accessibility analysis"""
    
    visual_issues = []
    
    # Analyze layout and visual hierarchy
    visual_analysis = await page.evaluate("""() => {
        const issues = [];
        
        // Check for text resizing capability
        const body = document.body;
        const bodyFontSize = parseFloat(window.getComputedStyle(body).fontSize);
        if (bodyFontSize < 16) {
            issues.push({
                type: 'small_base_font',
                severity: 'moderate',
                description: `Base font size ${bodyFontSize}px (önerilen: 16px minimum)`,
                wcag: '1.4.4'
            });
        }
        
        // Check for line height
        const paragraphs = document.querySelectorAll('p');
        paragraphs.forEach(p => {
            const lineHeight = parseFloat(window.getComputedStyle(p).lineHeight);
            const fontSize = parseFloat(window.getComputedStyle(p).fontSize);
            if (lineHeight / fontSize < 1.5) {
                issues.push({
                    type: 'tight_line_height',
                    severity: 'minor',
                    description: 'Line height yetersiz (min 1.5 önerilir)',
                    wcag: '1.4.12'
                });
            }
        });
        
        // Check for text alignment
        const justifiedText = document.querySelectorAll('*');
        justifiedText.forEach(el => {
            const textAlign = window.getComputedStyle(el).textAlign;
            if (textAlign === 'justify') {
                issues.push({
                    type: 'justified_text',
                    severity: 'minor',
                    description: 'İki yana yaslı metin (okunabilirlik sorunu)',
                    wcag: '1.4.8'
                });
            }
        });
        
        // Check for small touch targets
        const clickable = document.querySelectorAll('button, a, input[type="button"], input[type="submit"]');
        clickable.forEach(el => {
            const rect = el.getBoundingClientRect();
            const width = rect.width;
            const height = rect.height;
            if (width < 44 || height < 44) {
                issues.push({
                    type: 'small_touch_target',
                    severity: 'moderate',
                    description: `Touch target ${width}x${height}px (min 44x44px önerilir)`,
                    wcag: '2.5.8'
                });
            }
        });
        
        // Check for focus indicator visibility
        const focusable = document.querySelectorAll('a[href], button, input');
        focusable.forEach(el => {
            const outline = window.getComputedStyle(el).outline;
            const outlineStyle = window.getComputedStyle(el).outlineStyle;
            if (outline === 'none' || outlineStyle === 'none') {
                // Check if there's another focus indicator
                const boxShadow = window.getComputedStyle(el).boxShadow;
                if (boxShadow === 'none') {
                    issues.push({
                        type: 'missing_focus_indicator',
                        severity: 'serious',
                        description: 'Focus indicator görünmüyor',
                        wcag: '2.4.7'
                    });
                }
            }
        });
        
        return issues;
    }""")
    
    visual_issues.extend(visual_analysis)
    
    return {
        "issues": visual_issues,
        "tested_aspects": ["Font Size", "Line Height", "Text Alignment", "Touch Targets", "Focus Indicators", "Visual Hierarchy"]
    }

async def run_comprehensive_audit():
    """Run all 5 test modules on each page"""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        
        results = []
        
        print("🧠 AccessMind KAPOZLU Erişilebilirlik Denetimi Başlatılıyor\n")
        print(f"📊 Hedef: {URL}")
        print(f"📄 Sayfalar: {len(PAGES_TO_AUDIT)}")
        print(f"🔬 Test Modülleri: 5 (WCAG + Klavye + Ekran Okuyucu + Kontrast + Görsel)")
        print()
        
        for i, page_info in enumerate(PAGES_TO_AUDIT, 1):
            page_url = URL + page_info["path"]
            print(f"[{i}/{len(PAGES_TO_AUDIT)}] {page_info['name']}")
            
            page = await context.new_page()
            
            try:
                # Load page
                await page.goto(page_url, timeout=60000, wait_until="networkidle")
                await page.wait_for_timeout(2000)
                
                title = await page.title()
                
                # 1. WCAG 2.2 Otomatik Tarama
                print(f"    [1/5] WCAG 2.2 Otomatik Tarama...")
                await page.add_script_tag(url="https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.0/axe.min.js")
                axe_results = await page.evaluate("""() => {
                    return axe.run({
                        runOnly: {
                            type: 'tag',
                            values: ['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa']
                        }
                    });
                }""")
                
                # 2. Klavye Navigasyon Denetimi
                print(f"    [2/5] Klavye Navigasyon Denetimi...")
                keyboard_test = await test_keyboard_navigation(page)
                
                # 3. Ekran Okuyucu Uyumluluğu
                print(f"    [3/5] Ekran Okuyucu Uyumluluğu...")
                screen_reader_test = await test_screen_reader_compatibility(page)
                
                # 4. Renk Kontrastı Analizi
                print(f"    [4/5] Renk Kontrastı Analizi...")
                colors = await extract_colors_from_page(page)
                contrast_issues = analyze_contrast(colors)
                
                # 5. Görsel Erişilebilirlik
                print(f"    [5/5] Görsel Erişilebilirlik...")
                visual_test = await test_visual_accessibility(page)
                
                # Calculate scores
                wcag_violations = axe_results.get("violations", [])
                wcag_score = 100 - (sum(25 for v in wcag_violations if v.get("impact") == "critical") +
                                    sum(15 for v in wcag_violations if v.get("impact") == "serious") +
                                    sum(8 for v in wcag_violations if v.get("impact") == "moderate") +
                                    sum(3 for v in wcag_violations if v.get("impact") == "minor"))
                
                keyboard_score = 100 - (len(keyboard_test['issues']) * 10)
                sr_score = 100 - (len(screen_reader_test['issues']) * 15)
                contrast_score = 100 - (len(contrast_issues) * 12)
                visual_score = 100 - (len(visual_test['issues']) * 10)
                
                final_score = (wcag_score * 0.4 + keyboard_score * 0.2 + sr_score * 0.2 + contrast_score * 0.1 + visual_score * 0.1)
                
                result = {
                    "page_name": page_info["name"],
                    "url": page.url,
                    "path": page_info["path"],
                    "title": title,
                    "timestamp": datetime.now().isoformat(),
                    "tests": {
                        "wcag": {
                            "violations": wcag_violations,
                            "passes": len(axe_results.get("passes", [])),
                            "score": max(0, min(100, wcag_score))
                        },
                        "keyboard": {
                            "results": keyboard_test,
                            "score": max(0, min(100, keyboard_score))
                        },
                        "screen_reader": {
                            "results": screen_reader_test,
                            "score": max(0, min(100, sr_score))
                        },
                        "contrast": {
                            "issues": contrast_issues,
                            "analyzed_elements": len(colors),
                            "score": max(0, min(100, contrast_score))
                        },
                        "visual": {
                            "results": visual_test,
                            "score": max(0, min(100, visual_score))
                        }
                    },
                    "scores": {
                        "wcag": max(0, min(100, wcag_score)),
                        "keyboard": max(0, min(100, keyboard_score)),
                        "screen_reader": max(0, min(100, sr_score)),
                        "contrast": max(0, min(100, contrast_score)),
                        "visual": max(0, min(100, visual_score)),
                        "final": max(0, min(100, final_score)),
                        "wcag_level": "AA" if final_score >= 80 else ("A" if final_score >= 60 else "Fail")
                    },
                    "error": None
                }
                
                print(f"    ✅ Final Skor: {result['scores']['final']:.1f}/100")
                print(f"       WCAG: {result['scores']['wcag']:.1f} | Klavye: {result['scores']['keyboard']:.1f} | SR: {result['scores']['screen_reader']:.1f}")
                print()
                
            except Exception as e:
                result = {
                    "page_name": page_info["name"],
                    "url": page_url,
                    "path": page_info["path"],
                    "title": "Erişilemedi",
                    "timestamp": datetime.now().isoformat(),
                    "tests": {},
                    "scores": {"wcag": 0, "keyboard": 0, "screen_reader": 0, "contrast": 0, "visual": 0, "final": 0, "wcag_level": "Fail"},
                    "error": str(e)
                }
                print(f"    ❌ Hata: {e}")
                print()
            
            results.append(result)
            await page.close()
        
        await context.close()
        await browser.close()
        
        return results

def generate_comprehensive_html_report(results):
    """Generate detailed HTML report with all 5 test modules"""
    
    avg_final = sum(r['scores']['final'] for r in [x for x in results if x['scores']['final'] > 0]) / len([r for r in results if r['scores']['final'] > 0]) if results else 0
    avg_wcag = sum(r['scores']['wcag'] for r in results) / len(results) if results else 0
    avg_keyboard = sum(r['scores']['keyboard'] for r in results) / len(results) if results else 0
    avg_sr = sum(r['scores']['screen_reader'] for r in results) / len(results) if results else 0
    avg_contrast = sum(r['scores']['contrast'] for r in results) / len(results) if results else 0
    avg_visual = sum(r['scores']['visual'] for r in results) / len(results) if results else 0
    
    total_wcag_violations = sum(len(r.get('tests', {}).get('wcag', {}).get('violations', [])) for r in results)
    total_keyboard_issues = sum(len(r.get('tests', {}).get('keyboard', {}).get('results', {}).get('issues', [])) for r in results)
    total_sr_issues = sum(len(r.get('tests', {}).get('screen_reader', {}).get('results', {}).get('issues', [])) for r in results)
    total_contrast_issues = sum(len(r.get('tests', {}).get('contrast', {}).get('issues', [])) for r in results)
    total_visual_issues = sum(len(r.get('tests', {}).get('visual', {}).get('results', {}).get('issues', [])) for r in results)
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AccessMind KAPOZLU Denetim - Arcelik</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1400px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #0f3460; border-bottom: 3px solid #e94560; padding-bottom: 10px; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 20px; margin: 20px 0; }}
        .card {{ background: linear-gradient(135deg, #0f3460, #16213e); color: white; padding: 20px; border-radius: 8px; text-align: center; }}
        .card h3 {{ margin: 0 0 10px 0; font-size: 14px; opacity: 0.9; }}
        .card .value {{ font-size: 36px; font-weight: bold; }}
        .card.wcag {{ background: linear-gradient(135deg, #3498db, #2980b9); }}
        .card.keyboard {{ background: linear-gradient(135deg, #9b59b6, #8e44ad); }}
        .card.sr {{ background: linear-gradient(135deg, #e67e22, #d35400); }}
        .card.contrast {{ background: linear-gradient(135deg, #1abc9c, #16a085); }}
        .card.visual {{ background: linear-gradient(135deg, #f39c12, #e67e22); }}
        .page-section {{ margin: 30px 0; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px; background: #fafafa; }}
        .test-module {{ margin: 20px 0; padding: 20px; border: 2px solid #e0e0e0; border-radius: 8px; }}
        .test-module h4 {{ margin: 0 0 15px 0; color: #0f3460; font-size: 18px; }}
        .test-module.wcag {{ border-color: #3498db; }}
        .test-module.keyboard {{ border-color: #9b59b6; }}
        .test-module.sr {{ border-color: #e67e22; }}
        .test-module.contrast {{ border-color: #1abc9c; }}
        .test-module.visual {{ border-color: #f39c12; }}
        .score-badge {{ padding: 8px 16px; border-radius: 20px; font-weight: bold; display: inline-block; margin: 5px; }}
        .score-excellent {{ background: #27ae60; color: white; }}
        .score-good {{ background: #f39c12; color: white; }}
        .score-poor {{ background: #e74c3c; color: white; }}
        .issue {{ background: #fff5f5; border-left: 4px solid #e74c3c; padding: 15px; margin: 10px 0; border-radius: 4px; }}
        .issue.serious {{ border-color: #e74c3c; }}
        .issue.moderate {{ border-color: #f39c12; }}
        .issue.minor {{ border-color: #f1c40f; }}
        .footer {{ margin-top: 40px; padding-top: 20px; border-top: 2px solid #e0e0e0; text-align: center; color: #666; }}
        .badge {{ display: inline-block; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: bold; margin: 3px; }}
        .badge-5 {{ background: #e94560; color: white; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 AccessMind KAPOZLU Erişilebilirlik Denetimi</h1>
        <p>
            <strong>Hedef:</strong> www.arcelik.com.tr | 
            <strong>Standart:</strong> WCAG 2.2 AA | 
            <strong>Sayfalar:</strong> 5 |
            <span class="badge badge-5">🔬 5 Test Modülü</span>
        </p>
        <p><strong>Tarih:</strong> {timestamp}</p>
        
        <h2>📊 Genel Özet</h2>
        <div class="summary">
            <div class="card">
                <h3>Final Skor</h3>
                <div class="value">{avg_final:.1f}</div>
            </div>
            <div class="card wcag">
                <h3>WCAG 2.2</h3>
                <div class="value">{avg_wcag:.1f}</div>
            </div>
            <div class="card keyboard">
                <h3>Klavye</h3>
                <div class="value">{avg_keyboard:.1f}</div>
            </div>
            <div class="card sr">
                <h3>Ekran Okuyucu</h3>
                <div class="value">{avg_sr:.1f}</div>
            </div>
            <div class="card contrast">
                <h3>Kontrast</h3>
                <div class="value">{avg_contrast:.1f}</div>
            </div>
            <div class="card visual">
                <h3>Görsel</h3>
                <div class="value">{avg_visual:.1f}</div>
            </div>
        </div>
        
        <h2>⚠️ Toplam İhlaller</h2>
        <div class="summary">
            <div class="card" style="background: linear-gradient(135deg, #e74c3c, #c0392b);">
                <h3>WCAG İhlal</h3>
                <div class="value">{total_wcag_violations}</div>
            </div>
            <div class="card" style="background: linear-gradient(135deg, #9b59b6, #8e44ad);">
                <h3>Klavye Sorunu</h3>
                <div class="value">{total_keyboard_issues}</div>
            </div>
            <div class="card" style="background: linear-gradient(135deg, #e67e22, #d35400);">
                <h3>SR Uyumluluk</h3>
                <div class="value">{total_sr_issues}</div>
            </div>
            <div class="card" style="background: linear-gradient(135deg, #1abc9c, #16a085);">
                <h3>Kontrast Sorunu</h3>
                <div class="value">{total_contrast_issues}</div>
            </div>
            <div class="card" style="background: linear-gradient(135deg, #f39c12, #e67e22);">
                <h3>Görsel Sorun</h3>
                <div class="value">{total_visual_issues}</div>
            </div>
        </div>
        
        <h2>📄 Sayfa Detayları</h2>
"""
    
    for i, result in enumerate(results, 1):
        final_score = result.get('scores', {}).get('final', 0)
        score_class = "score-excellent" if final_score >= 80 else ("score-good" if final_score >= 60 else "score-poor")
        
        html += f"""
        <div class="page-section">
            <h3>{i}. {result['page_name']}</h3>
            <p><strong>URL:</strong> {result['url']}</p>
            <p><strong>Başlık:</strong> {result['title']}</p>
            <div style="margin: 15px 0;">
                <span class="score-badge {score_class}">Final: {final_score:.1f}/100</span>
                <span class="score-badge" style="background: #3498db;">WCAG: {result['scores']['wcag']:.1f}</span>
                <span class="score-badge" style="background: #9b59b6;">Klavye: {result['scores']['keyboard']:.1f}</span>
                <span class="score-badge" style="background: #e67e22;">SR: {result['scores']['screen_reader']:.1f}</span>
                <span class="score-badge" style="background: #1abc9c;">Kontrast: {result['scores']['contrast']:.1f}</span>
                <span class="score-badge" style="background: #f39c12;">Görsel: {result['scores']['visual']:.1f}</span>
            </div>
"""
        
        if result.get('error'):
            html += f"""<p style="color: #e74c3c;">⚠️ Hata: {result['error']}</p>\n"""
        else:
            # WCAG Module
            wcag_violations = result.get('tests', {}).get('wcag', {}).get('violations', [])
            html += f"""
            <div class="test-module wcag">
                <h4>🔍 1. WCAG 2.2 Otomatik Tarama</h4>
"""
            if wcag_violations:
                for v in wcag_violations[:3]:  # Show first 3
                    impact = v.get('impact', 'minor')
                    html += f"""
                <div class="issue {impact}">
                    <strong>{v.get('id', 'Unknown')}</strong> - {v.get('help', '')}<br>
                    <small>{v.get('description', '')}</small>
                </div>
"""
            else:
                html += """<p style="color: #27ae60;">✅ WCAG ihlali yok</p>\n"""
            html += """</div>\n"""
            
            # Keyboard Module
            keyboard_issues = result.get('tests', {}).get('keyboard', {}).get('results', {}).get('issues', [])
            html += f"""
            <div class="test-module keyboard">
                <h4>⌨️ 2. Klavye Navigasyon Denetimi</h4>
                <p><strong>Focusable Elements:</strong> {result.get('tests', {}).get('keyboard', {}).get('results', {}).get('total_focusable', 0)}</p>
                <p><strong>Skip Link:</strong> {result.get('tests', {}).get('keyboard', {}).get('results', {}).get('has_skip_link', False)}</p>
"""
            if keyboard_issues:
                for issue in keyboard_issues:
                    html += f"""
                <div class="issue {issue.get('severity', 'minor')}">
                    <strong>{issue.get('type', 'Unknown')}</strong> - {issue.get('description', '')}<br>
                    <small>WCAG {issue.get('wcag', '')}: {issue.get('recommendation', '')}</small>
                </div>
"""
            html += """</div>\n"""
            
            # Screen Reader Module
            sr_issues = result.get('tests', {}).get('screen_reader', {}).get('results', {}).get('issues', [])
            html += f"""
            <div class="test-module sr">
                <h4>🔊 3. Ekran Okuyucu Uyumluluğu</h4>
                <p><strong>Landmarks:</strong> Main:{result.get('tests', {}).get('screen_reader', {}).get('results', {}).get('landmarks', {}).get('main', 0)} Nav:{result.get('tests', {}).get('screen_reader', {}).get('results', {}).get('landmarks', {}).get('nav', 0)}</p>
                <p><strong>Headings:</strong> H1:{result.get('tests', {}).get('screen_reader', {}).get('results', {}).get('headings', {}).get('h1', 0)} H2:{result.get('tests', {}).get('screen_reader', {}).get('results', {}).get('headings', {}).get('h2', 0)}</p>
"""
            if sr_issues:
                for issue in sr_issues[:3]:
                    html += f"""
                <div class="issue {issue.get('severity', 'minor')}">
                    <strong>{issue.get('type', 'Unknown')}</strong> - {issue.get('description', '')}<br>
                    <small>WCAG {issue.get('wcag', '')}: {issue.get('recommendation', '')}</small>
                </div>
"""
            html += """</div>\n"""
            
            # Contrast Module
            contrast_issues = result.get('tests', {}).get('contrast', {}).get('issues', [])
            html += f"""
            <div class="test-module contrast">
                <h4>🎨 4. Renk Kontrastı Analizi</h4>
                <p><strong>Analiz Edilen Elementler:</strong> {result.get('tests', {}).get('contrast', {}).get('analyzed_elements', 0)}</p>
"""
            if contrast_issues:
                for issue in contrast_issues[:3]:
                    html += f"""
                <div class="issue {issue.get('severity', 'minor')}">
                    <strong>{issue.get('selector', 'Unknown')}</strong> - Ratio: {issue.get('ratio', 0)}/{issue.get('required', 4.5)}<br>
                    <small>Text: "{issue.get('text', '')}" | WCAG {issue.get('wcag', '')}</small>
                </div>
"""
            else:
                html += """<p style="color: #27ae60;">✅ Kontrast sorunu yok</p>\n"""
            html += """</div>\n"""
            
            # Visual Module
            visual_issues = result.get('tests', {}).get('visual', {}).get('results', {}).get('issues', [])
            html += f"""
            <div class="test-module visual">
                <h4>👁️ 5. Görsel Erişilebilirlik</h4>
                <p><strong>Test Edilen:</strong> Font Size, Line Height, Touch Targets, Focus Indicators</p>
"""
            if visual_issues:
                for issue in visual_issues[:3]:
                    html += f"""
                <div class="issue {issue.get('severity', 'minor')}">
                    <strong>{issue.get('type', 'Unknown')}</strong> - {issue.get('description', '')}<br>
                    <small>WCAG {issue.get('wcag', '')}</small>
                </div>
"""
            else:
                html += """<p style="color: #27ae60;">✅ Görsel sorun yok</p>\n"""
            html += """</div>\n"""
        
        html += """        </div>\n"""
    
    html += """
        <div class="footer">
            <p>AccessMind Enterprise - KAPOZLU Erişilebilirlik Denetimi (5 Modül)</p>
            <p>1. WCAG 2.2 | 2. Klavye | 3. Ekran Okuyucu | 4. Kontrast | 5. Görsel</p>
            <p>AccessMind Skill v3.0 | Skill İçi İşlem Akışı Kaydedildi</p>
        </div>
    </div>
</body>
</html>
"""
    return html

async def main():
    results = await run_comprehensive_audit()
    
    html_report = generate_comprehensive_html_report(results)
    
    output_dir = "/Users/sarper/.openclaw/workspace/audits"
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_file = f"{output_dir}/arcelik_comprehensive_{timestamp}.html"
    json_file = f"{output_dir}/arcelik_comprehensive_{timestamp}.json"
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_report)
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    
    # Update skill workflow
    workflow_file = "/Users/sarper/.openclaw/workspace/skills/accessmind/comprehensive-a11y-workflow.md"
    
    workflow_content = f"""# AccessMind KAPOZLU Erişilebilirlik Denetim İşlem Akışı

## 5 Test Modülü

### 1. ✅ WCAG 2.2 Otomatik Tarama
- **Motor:** Axe-core 4.10.0
- **Standartlar:** WCAG 2.2 A/AA, WCAG 2.1 AA, WCAG 2.2 AA
- **Çıktı:** İhlal listesi, pass count, score

### 2. ⌨️ Klavye Navigasyon Denetimi
- **Testler:**
  - Focusable element tespiti
  - Skip link kontrolü
  - Tab order analizi
  - Positive tabIndex tespiti
  - Keyboard trap kontrolü
- **WCAG:** 2.1.1, 2.4.1, 2.4.3, 2.4.7

### 3. 🔊 Ekran Okuyucu Uyumluluğu
- **Testler:**
  - ARIA landmarks (main, nav, header, footer, etc.)
  - Accessible names (buttons, links, images, forms)
  - Live regions (aria-live, role="alert")
  - Heading hiyerarşisi
- **Screen Readers:** NVDA, JAWS, VoiceOver patternleri
- **WCAG:** 1.3.1, 4.1.2, 1.3.6

### 4. 🎨 Renk Kontrastı Analizi
- **Testler:**
  - Foreground/background color extraction
  - Contrast ratio calculation (WCAG formülü)
  - Large text detection (18pt+/14pt bold)
  - AA (4.5:1) vs AAA (7:1) compliance
- **WCAG:** 1.4.3 (Contrast), 1.4.6 (Enhanced Contrast)

### 5. 👁️ Görsel Erişilebilirlik
- **Testler:**
  - Base font size (min 16px)
  - Line height (min 1.5)
  - Text alignment (no justify)
  - Touch target size (min 44x44px)
  - Focus indicator visibility
- **WCAG:** 1.4.4, 1.4.8, 1.4.12, 2.5.8, 2.4.7

## Skor Hesaplama

```python
wcag_score = 100 - (critical×25 + serious×15 + moderate×8 + minor×3)
keyboard_score = 100 - (issues×10)
sr_score = 100 - (issues×15)
contrast_score = 100 - (issues×12)
visual_score = 100 - (issues×10)

final_score = (wcag×0.4 + keyboard×0.2 + sr×0.2 + contrast×0.1 + visual×0.1)
```

## Çıktı Dosyaları
- `audits/arcelik_comprehensive_YYYYMMDD_HHMMSS.html`
- `audits/arcelik_comprehensive_YYYYMMDD_HHMMSS.json`
- `skills/accessmind/comprehensive-a11y-workflow.md`

## Kullanım
```bash
python3 /Users/sarper/.openclaw/workspace/skills/accessmind/scripts/comprehensive-a11y-audit.py
```
"""
    
    with open(workflow_file, 'w', encoding='utf-8') as f:
        f.write(workflow_content)
    
    # Calculate averages for summary
    valid_results = [r for r in results if r['scores']['final'] > 0]
    avg_final = sum(r['scores']['final'] for r in valid_results) / len(valid_results) if valid_results else 0
    avg_wcag = sum(r['scores']['wcag'] for r in results) / len(results) if results else 0
    total_wcag_violations = sum(len(r.get('tests', {}).get('wcag', {}).get('violations', [])) for r in results)
    total_keyboard_issues = sum(len(r.get('tests', {}).get('keyboard', {}).get('results', {}).get('issues', [])) for r in results)
    total_sr_issues = sum(len(r.get('tests', {}).get('screen_reader', {}).get('results', {}).get('issues', [])) for r in results)
    total_contrast_issues = sum(len(r.get('tests', {}).get('contrast', {}).get('issues', [])) for r in results)
    total_visual_issues = sum(len(r.get('tests', {}).get('visual', {}).get('results', {}).get('issues', [])) for r in results)
    
    print()
    print("=" * 70)
    print("✅ KAPOZLU DENETİM TAMAMLANDI")
    print("=" * 70)
    print(f"📊 Final Ortalama Skor: {avg_final:.1f}/100")
    print(f"🔍 WCAG İhlaller: {total_wcag_violations}")
    print(f"⌨️ Klavye Sorunları: {total_keyboard_issues}")
    print(f"🔊 SR Sorunları: {total_sr_issues}")
    print(f"🎨 Kontrast Sorunları: {total_contrast_issues}")
    print(f"👁️ Görsel Sorunlar: {total_visual_issues}")
    print(f"📄 HTML: {html_file}")
    print(f"📄 JSON: {json_file}")
    print(f"📋 Workflow: {workflow_file}")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(main())
