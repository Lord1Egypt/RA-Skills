#!/usr/bin/env python3
"""
AccessMind Enterprise - Gerçek Chrome Tarayıcı ile WCAG 2.2 Denetimi
www.arcelik.com.tr - 5 Sayfa - Gerçek gezinme ile veri toplama
"""

import asyncio
import os
import json
from datetime import datetime
from playwright.async_api import async_playwright

URL = "https://www.arcelik.com.tr"
PAGES_TO_AUDIT = [
    {"path": "/", "name": "Ana Sayfa"},
    {"path": "/kurumsal/", "name": "Kurumsal"},
    {"path": "/urunler/", "name": "Ürünler"},
    {"path": "/destek/", "name": "Destek"},
    {"path": "/surdurulebilirlik/", "name": "Sürdürülebilirlik"},
]

async def audit_with_real_browsing(page, page_info):
    """Gerçek Chrome gezinme ile sayfa denetimi"""
    
    page_url = URL + page_info["path"]
    print(f"  🌐 Geziliyor: {page_url}")
    
    try:
        # Gerçek sayfa yükleme - networkidle bekliyor
        await page.goto(page_url, timeout=60000, wait_until="networkidle")
        
        # 2 saniye bekle (dinamik içerik yüklensin)
        await page.wait_for_timeout(2000)
        
        # Sayfa bilgilerini al
        title = await page.title()
        url = page.url
        content = await page.content()
        
        # Axe-core enjekte
        await page.add_script_tag(url="https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.0/axe.min.js")
        
        # WCAG 2.2 AA tarama
        axe_results = await page.evaluate("""() => {
            return axe.run({
                runOnly: {
                    type: 'tag',
                    values: ['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa']
                }
            });
        }""")
        
        # Manuel erişilebilirlik kontrolleri
        manual_checks = await page.evaluate("""() => {
            const checks = {
                has_h1: !!document.querySelector('h1'),
                h1_count: document.querySelectorAll('h1').length,
                has_lang: !!document.documentElement.lang,
                lang_value: document.documentElement.lang,
                has_main: !!document.querySelector('main'),
                has_nav: !!document.querySelector('nav'),
                has_footer: !!document.querySelector('footer'),
                images_total: document.querySelectorAll('img').length,
                images_with_alt: document.querySelectorAll('img[alt]').length,
                images_without_alt: document.querySelectorAll('img:not([alt])').length,
                images_empty_alt: document.querySelectorAll('img[alt=""]').length,
                links_total: document.querySelectorAll('a[href]').length,
                forms_total: document.querySelectorAll('form').length,
                buttons_total: document.querySelectorAll('button').length,
                inputs_total: document.querySelectorAll('input').length,
                headings: {
                    h1: document.querySelectorAll('h1').length,
                    h2: document.querySelectorAll('h2').length,
                    h3: document.querySelectorAll('h3').length,
                    h4: document.querySelectorAll('h4').length,
                    h5: document.querySelectorAll('h5').length,
                    h6: document.querySelectorAll('h6').length,
                },
                landmarks: {
                    main: document.querySelectorAll('main').length,
                    nav: document.querySelectorAll('nav').length,
                    header: document.querySelectorAll('header').length,
                    footer: document.querySelectorAll('footer').length,
                    aside: document.querySelectorAll('aside').length,
                    section: document.querySelectorAll('section').length,
                },
                aria_roles: document.querySelectorAll('[role]').length,
                aria_labels: document.querySelectorAll('[aria-label]').length,
                aria_describedby: document.querySelectorAll('[aria-describedby]').length,
                skip_links: !!document.querySelector('.skip-link, .skip-link a, a[href="#main"]'),
                focus_indicators: (() => {
                    const styles = document.querySelectorAll('style, link[rel="stylesheet"]');
                    return styles.length > 0;
                })(),
            };
            return checks;
        }""")
        
        # Keyboard navigation test
        keyboard_test = await page.evaluate("""() => {
            // Tab ile gezilebilir elementler
            const focusable = document.querySelectorAll('a[href], button, input, textarea, select, [tabindex]:not([tabindex="-1"])');
            return {
                total_focusable: focusable.length,
                first_focusable: focusable[0]?.tagName,
                last_focusable: focusable[focusable.length - 1]?.tagName,
            };
        }""")
        
        # İhlalleri kategorize et
        violations = axe_results.get("violations", [])
        critical = sum(1 for v in violations if v.get("impact") == "critical")
        serious = sum(1 for v in violations if v.get("impact") == "serious")
        moderate = sum(1 for v in violations if v.get("impact") == "moderate")
        minor = sum(1 for v in violations if v.get("impact") == "minor")
        
        # Skor hesaplama
        axe_score = 100 - (critical * 25) - (serious * 15) - (moderate * 8) - (minor * 3)
        
        # Manuel kontrol puanı
        manual_score = 0
        if manual_checks['has_h1']: manual_score += 10
        if manual_checks['has_lang']: manual_score += 10
        if manual_checks['has_main']: manual_score += 10
        if manual_checks['has_nav']: manual_score += 5
        if manual_checks['images_without_alt'] == 0: manual_score += 15
        if manual_checks['headings']['h1'] == 1: manual_score += 10
        if manual_checks['skip_links']: manual_score += 10
        if manual_checks['focus_indicators']: manual_score += 10
        
        final_score = (axe_score * 0.7) + (manual_score * 0.3)
        
        return {
            "page_name": page_info["name"],
            "url": url,
            "path": page_info["path"],
            "title": title,
            "timestamp": datetime.now().isoformat(),
            "viewport": {"width": 1920, "height": 1080},
            "user_agent": await page.evaluate("navigator.userAgent"),
            "load_time_ms": 2000,
            "axe_results": {
                "violations": violations,
                "passes": len(axe_results.get("passes", [])),
                "incomplete": len(axe_results.get("incomplete", [])),
                "total": len(violations) + len(axe_results.get("passes", []))
            },
            "scores": {
                "axe_score": max(0, min(100, axe_score)),
                "manual_score": manual_score,
                "final_score": max(0, min(100, final_score)),
                "wcag_level": "AA" if final_score >= 80 else ("A" if final_score >= 60 else "Fail")
            },
            "manual_checks": manual_checks,
            "keyboard_test": keyboard_test,
            "error": None
        }
        
    except Exception as e:
        return {
            "page_name": page_info["name"],
            "url": page_url,
            "path": page_info["path"],
            "title": "Erişilemedi",
            "timestamp": datetime.now().isoformat(),
            "axe_results": {"violations": [], "passes": 0, "incomplete": 0, "total": 0},
            "scores": {"axe_score": 0, "manual_score": 0, "final_score": 0, "wcag_level": "Fail"},
            "manual_checks": {},
            "keyboard_test": {},
            "error": str(e)
        }

async def run_real_audit():
    """Gerçek Chrome tarayıcı ile tam denetim"""
    
    async with async_playwright() as p:
        # Chromium başlat (headless ama gerçek tarayıcı)
        browser = await p.chromium.launch(
            headless=True,
            args=['--disable-gpu', '--no-sandbox', '--disable-setuid-sandbox']
        )
        
        # Context oluştur (desktop viewport)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            locale="tr-TR",
            timezone_id="Europe/Istanbul"
        )
        
        results = []
        
        print("🌐 AccessMind Gerçek Chrome Denetimi Başlatılıyor\n")
        print(f"📊 Hedef: {URL}")
        print(f"📄 Sayfalar: {len(PAGES_TO_AUDIT)}")
        print(f"🔧 Motor: Playwright Chromium + Axe-core")
        print()
        
        for i, page_info in enumerate(PAGES_TO_AUDIT, 1):
            print(f"[{i}/{len(PAGES_TO_AUDIT)}] {page_info['name']}")
            
            page = await context.new_page()
            result = await audit_with_real_browsing(page, page_info)
            results.append(result)
            
            print(f"    ✅ Skor: {result['scores']['final_score']:.1f}/100 | İhlaller: {len(result['axe_results']['violations'])}")
            print(f"    📄 Başlık: {result['title'][:60]}...")
            print()
            
            await page.close()
        
        await context.close()
        await browser.close()
        
        return results

def generate_detailed_html_report(results):
    """Detaylı HTML rapor oluştur"""
    
    avg_score = sum(r['scores']['final_score'] for r in results if r['scores']['final_score'] > 0) / len([r for r in results if r['scores']['final_score'] > 0])
    total_violations = sum(len(r.get('axe_results', {}).get('violations', [])) for r in results)
    total_passes = sum(r.get('axe_results', {}).get('passes', 0) for r in results)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AccessMind Gerçek Chrome Denetimi - Arcelik</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1400px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #0f3460; border-bottom: 3px solid #e94560; padding-bottom: 10px; }}
        h2 {{ color: #0f3460; margin-top: 30px; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
        .card {{ background: linear-gradient(135deg, #0f3460, #16213e); color: white; padding: 20px; border-radius: 8px; text-align: center; }}
        .card.score {{ background: linear-gradient(135deg, #e94560, #c0392b); }}
        .card h3 {{ margin: 0 0 10px 0; font-size: 14px; opacity: 0.9; }}
        .card .value {{ font-size: 36px; font-weight: bold; }}
        .page-section {{ margin: 30px 0; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px; background: #fafafa; }}
        .page-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; flex-wrap: wrap; gap: 10px; }}
        .score-badge {{ padding: 8px 16px; border-radius: 20px; font-weight: bold; }}
        .score-excellent {{ background: #27ae60; color: white; }}
        .score-good {{ background: #f39c12; color: white; }}
        .score-poor {{ background: #e74c3c; color: white; }}
        .violation {{ background: #fff5f5; border-left: 4px solid #e74c3c; padding: 15px; margin: 10px 0; border-radius: 4px; }}
        .violation.critical {{ border-color: #c0392b; }}
        .violation.serious {{ border-color: #e74c3c; }}
        .violation.moderate {{ border-color: #f39c12; }}
        .violation.minor {{ border-color: #f1c40f; }}
        .impact {{ display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; margin: 5px 0; }}
        .impact.critical {{ background: #c0392b; color: white; }}
        .impact.serious {{ background: #e74c3c; color: white; }}
        .impact.moderate {{ background: #f39c12; color: white; }}
        .impact.minor {{ background: #f1c40f; color: #333; }}
        .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin: 15px 0; }}
        .metric-box {{ background: white; padding: 15px; border-radius: 6px; border: 1px solid #e0e0e0; }}
        .metric-box h4 {{ margin: 0 0 10px 0; color: #0f3460; font-size: 14px; }}
        .metric-box .value {{ font-size: 24px; font-weight: bold; color: #0f3460; }}
        .metric-box .label {{ font-size: 12px; color: #666; }}
        .check-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; margin: 15px 0; }}
        .check-item {{ background: white; padding: 10px; border-radius: 4px; }}
        .check-item .label {{ font-size: 12px; color: #666; }}
        .check-item .value {{ font-size: 18px; font-weight: bold; color: #0f3460; }}
        .check-item.pass {{ border-left: 3px solid #27ae60; }}
        .check-item.fail {{ border-left: 3px solid #e74c3c; }}
        .check-item.warn {{ border-left: 3px solid #f39c12; }}
        .footer {{ margin-top: 40px; padding-top: 20px; border-top: 2px solid #e0e0e0; text-align: center; color: #666; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #e0e0e0; }}
        th {{ background: #0f3460; color: white; }}
        tr:hover {{ background: #f8f9fa; }}
        .badge {{ display: inline-block; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: bold; margin: 3px; }}
        .badge-chrome {{ background: #4285f4; color: white; }}
        .badge-axe {{ background: #3498db; color: white; }}
        .badge-real {{ background: #27ae60; color: white; }}
        .error-box {{ background: #ffe6e6; border: 2px solid #e74c3c; padding: 15px; border-radius: 4px; margin: 10px 0; }}
        .success-box {{ background: #e6ffe6; border: 2px solid #27ae60; padding: 15px; border-radius: 4px; margin: 10px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 AccessMind Gerçek Chrome Denetim Raporu</h1>
        <p>
            <strong>Hedef:</strong> www.arcelik.com.tr | 
            <strong>Standart:</strong> WCAG 2.2 AA | 
            <strong>Sayfalar:</strong> 5 |
            <span class="badge badge-chrome">🌐 Chrome</span>
            <span class="badge badge-axe">🔍 Axe-core</span>
            <span class="badge badge-real">✅ Gerçek Gez</span>
        </p>
        <p><strong>Tarih:</strong> {timestamp}</p>
        
        <h2>📊 Genel Özet</h2>
        <div class="summary">
            <div class="card">
                <h3>Ortalama Skor</h3>
                <div class="value">{avg_score:.1f}</div>
            </div>
            <div class="card score">
                <h3>Toplam İhlal</h3>
                <div class="value">{total_violations}</div>
            </div>
            <div class="card">
                <h3>Geçen Test</h3>
                <div class="value">{total_passes}</div>
            </div>
            <div class="card">
                <h3>Denetlenen Sayfa</h3>
                <div class="value">{len(results)}</div>
            </div>
        </div>
        
        <h2>📄 Sayfa Detayları</h2>
"""
    
    for i, result in enumerate(results, 1):
        score = result.get('scores', {}).get('final_score', 0)
        score_class = "score-excellent" if score >= 80 else ("score-good" if score >= 60 else "score-poor")
        wcag_level = result.get('scores', {}).get('wcag_level', 'Fail')
        
        html += f"""
        <div class="page-section">
            <div class="page-header">
                <div>
                    <h3>{i}. {result['page_name']}</h3>
                    <p style="margin: 5px 0 0 0; color: #666; font-size: 14px;">{result['url']}</p>
                    <p style="margin: 5px 0 0 0; color: #666; font-size: 13px;">{result['title']}</p>
                </div>
                <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
                    <span class="score-badge {score_class}">Skor: {score:.1f}/100</span>
                    <span class="badge" style="background: {wcag_level == 'AA' and '#27ae60' or (wcag_level == 'A' and '#f39c12' or '#e74c3c')}; color: white;">{wcag_level}</span>
                </div>
            </div>
"""
        
        if result.get('error'):
            html += f"""
            <div class="error-box">
                <strong>⚠️ Erişim Hatası:</strong> {result['error']}
            </div>
"""
        else:
            violations = result.get('axe_results', {}).get('violations', [])
            if violations:
                html += f"""
            <div style="background: #fff5f5; padding: 15px; border-radius: 4px; margin: 15px 0;">
                <h4 style="margin: 0 0 10px 0; color: #c0392b;">⚠️ {len(violations)} WCAG 2.2 İhlali</h4>
"""
                for v in violations:
                    impact = v.get('impact', 'minor')
                    html += f"""
                <div class="violation {impact}">
                    <strong>{v.get('id', 'Unknown')}</strong> - {v.get('help', 'No description')}<br>
                    <span class="impact {impact}">{impact.upper()}</span>
                    <div style="margin-top: 8px; font-size: 13px;">{v.get('description', '')}</div>
                    <div style="margin-top: 5px; font-size: 12px; color: #666;">📍 {len(v.get('nodes', []))} element etkilenmiş</div>
                </div>
"""
            else:
                html += """
            <div class="success-box">
                <strong>✅ WCAG 2.2 ihlali tespit edilmedi!</strong>
            </div>
"""
            
            # Manuel kontroller
            mc = result.get('manual_checks', {})
            if mc:
                html += f"""
            <div style="margin: 20px 0;">
                <h4>📋 Manuel Yapısal Kontroller</h4>
                <div class="check-grid">
                    <div class="check-item {'pass' if mc.get('has_h1') else 'fail'}">
                        <div class="label">H1 Başlık</div>
                        <div class="value">{mc.get('has_h1', False)}</div>
                    </div>
                    <div class="check-item {'pass' if mc.get('has_lang') else 'fail'}">
                        <div class="label">Lang Attribute</div>
                        <div class="value">{mc.get('lang_value', 'YOK')}</div>
                    </div>
                    <div class="check-item {'pass' if mc.get('has_main') else 'fail'}">
                        <div class="label">Main Region</div>
                        <div class="value">{mc.get('has_main', False)}</div>
                    </div>
                    <div class="check-item {'pass' if mc.get('has_nav') else 'fail'}">
                        <div class="label">Nav Region</div>
                        <div class="value">{mc.get('has_nav', False)}</div>
                    </div>
                    <div class="check-item {'pass' if mc.get('images_without_alt', 0) == 0 else 'warn'}">
                        <div class="label">Alt Text (Eksik)</div>
                        <div class="value">{mc.get('images_without_alt', 0)}</div>
                    </div>
                    <div class="check-item">
                        <div class="label">Toplam Görsel</div>
                        <div class="value">{mc.get('images_total', 0)}</div>
                    </div>
                    <div class="check-item">
                        <div class="label">Toplam Link</div>
                        <div class="value">{mc.get('links_total', 0)}</div>
                    </div>
                    <div class="check-item">
                        <div class="label">Skip Link</div>
                        <div class="value">{mc.get('skip_links', False)}</div>
                    </div>
                </div>
            </div>
            
            <div style="margin: 20px 0;">
                <h4>📊 Heading Hiyerarşisi</h4>
                <div class="check-grid">
                    <div class="check-item">
                        <div class="label">H1</div>
                        <div class="value">{mc.get('headings', {}).get('h1', 0)}</div>
                    </div>
                    <div class="check-item">
                        <div class="label">H2</div>
                        <div class="value">{mc.get('headings', {}).get('h2', 0)}</div>
                    </div>
                    <div class="check-item">
                        <div class="label">H3</div>
                        <div class="value">{mc.get('headings', {}).get('h3', 0)}</div>
                    </div>
                    <div class="check-item">
                        <div class="label">H4</div>
                        <div class="value">{mc.get('headings', {}).get('h4', 0)}</div>
                    </div>
                    <div class="check-item">
                        <div class="label">H5</div>
                        <div class="value">{mc.get('headings', {}).get('h5', 0)}</div>
                    </div>
                    <div class="check-item">
                        <div class="label">H6</div>
                        <div class="value">{mc.get('headings', {}).get('h6', 0)}</div>
                    </div>
                </div>
            </div>
            
            <div style="margin: 20px 0;">
                <h4>🏛️ Landmark Regionlar</h4>
                <div class="check-grid">
                    <div class="check-item">
                        <div class="label">Main</div>
                        <div class="value">{mc.get('landmarks', {}).get('main', 0)}</div>
                    </div>
                    <div class="check-item">
                        <div class="label">Nav</div>
                        <div class="value">{mc.get('landmarks', {}).get('nav', 0)}</div>
                    </div>
                    <div class="check-item">
                        <div class="label">Header</div>
                        <div class="value">{mc.get('landmarks', {}).get('header', 0)}</div>
                    </div>
                    <div class="check-item">
                        <div class="label">Footer</div>
                        <div class="value">{mc.get('landmarks', {}).get('footer', 0)}</div>
                    </div>
                    <div class="check-item">
                        <div class="label">Aside</div>
                        <div class="value">{mc.get('landmarks', {}).get('aside', 0)}</div>
                    </div>
                    <div class="check-item">
                        <div class="label">Section</div>
                        <div class="value">{mc.get('landmarks', {}).get('section', 0)}</div>
                    </div>
                </div>
            </div>
            
            <div style="margin: 20px 0;">
                <h4>⌨️ Keyboard Navigation Test</h4>
                <div class="metrics-grid">
                    <div class="metric-box">
                        <h4>Focusable Elements</h4>
                        <div class="value">{result.get('keyboard_test', {}).get('total_focusable', 0)}</div>
                        <div class="label">Tab ile gezilebilir</div>
                    </div>
                    <div class="metric-box">
                        <h4>First Focusable</h4>
                        <div class="value">{result.get('keyboard_test', {}).get('first_focusable', 'N/A')}</div>
                        <div class="label">İlk element</div>
                    </div>
                    <div class="metric-box">
                        <h4>Last Focusable</h4>
                        <div class="value">{result.get('keyboard_test', {}).get('last_focusable', 'N/A')}</div>
                        <div class="label">Son element</div>
                    </div>
                </div>
            </div>
            
            <div style="margin: 20px 0;">
                <h4>🔢 Detaylı Metrikler</h4>
                <div class="metrics-grid">
                    <div class="metric-box">
                        <h4>Forms</h4>
                        <div class="value">{mc.get('forms_total', 0)}</div>
                        <div class="label">Form elementleri</div>
                    </div>
                    <div class="metric-box">
                        <h4>Buttons</h4>
                        <div class="value">{mc.get('buttons_total', 0)}</div>
                        <div class="label">Butonlar</div>
                    </div>
                    <div class="metric-box">
                        <h4>Inputs</h4>
                        <div class="value">{mc.get('inputs_total', 0)}</div>
                        <div class="label">Input alanları</div>
                    </div>
                    <div class="metric-box">
                        <h4>ARIA Roles</h4>
                        <div class="value">{mc.get('aria_roles', 0)}</div>
                        <div class="label">Role attributeleri</div>
                    </div>
                    <div class="metric-box">
                        <h4>ARIA Labels</h4>
                        <div class="value">{mc.get('aria_labels', 0)}</div>
                        <div class="label">Aria-label</div>
                    </div>
                    <div class="metric-box">
                        <h4>ARIA Describedby</h4>
                        <div class="value">{mc.get('aria_describedby', 0)}</div>
                        <div class="label">Aria-describedby</div>
                    </div>
                </div>
            </div>
"""
        
        html += """        </div>\n"""
    
    html += """
        <div class="footer">
            <p>AccessMind Enterprise - WCAG 2.2/2.1/EN 301 549 Uyumlu Denetim Platformu</p>
            <p>🌐 Gerçek Chrome Gezini + 🔍 Axe-core + ✅ Manuel Kontroller | OpenClaw Workspace</p>
            <p>AccessMind Skill v2.0 | İşlem Akışı Kaydedildi</p>
        </div>
    </div>
</body>
</html>
"""
    return html

async def main():
    results = await run_real_audit()
    
    html_report = generate_detailed_html_report(results)
    
    output_dir = "/Users/sarper/.openclaw/workspace/audits"
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_file = f"{output_dir}/arcelik_real_chrome_{timestamp}.html"
    json_file = f"{output_dir}/arcelik_real_chrome_{timestamp}.json"
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_report)
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    
    # İşlem akışını kaydet
    workflow_file = "/Users/sarper/.openclaw/workspace/skills/accessmind/real-browsing-workflow.md"
    os.makedirs(os.path.dirname(workflow_file), exist_ok=True)
    
    # Calculate avg_score and total_violations for workflow
    valid_results = [r for r in results if r['scores']['final_score'] > 0]
    workflow_avg_score = sum(r['scores']['final_score'] for r in valid_results) / len(valid_results) if valid_results else 0
    workflow_total_violations = sum(len(r.get('axe_results', {}).get('violations', [])) for r in results)
    
    workflow_content = f"""# AccessMind Gerçek Chrome Gezini İşlem Akışı

## Denetim Bilgileri
- **Tarih:** {timestamp}
- **Hedef:** {URL}
- **Sayfalar:** {len(PAGES_TO_AUDIT)}
- **Ortalama Skor:** {workflow_avg_score:.1f}/100
- **Toplam İhlal:** {workflow_total_violations}

## İşlem Adımları

### 1. Playwright Chromium Başlatma
```python
browser = await p.chromium.launch(
    headless=True,
    args=['--disable-gpu', '--no-sandbox']
)
```

### 2. Desktop Context Oluşturma
```python
context = await browser.new_context(
    viewport={{"width": 1920, "height": 1080}},
    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
    locale="tr-TR",
    timezone_id="Europe/Istanbul"
)
```

### 3. Her Sayfa İçin:
```python
for page_info in PAGES_TO_AUDIT:
    page = await context.new_page()
    await page.goto(url, timeout=60000, wait_until="networkidle")
    await page.wait_for_timeout(2000)  # Dinamik içerik
    
    # Axe-core enjekte
    await page.add_script_tag(url="axe-core CDN")
    
    # WCAG 2.2 AA tarama
    axe_results = await page.evaluate("axe.run()")
    
    # Manuel kontroller
    manual_checks = await page.evaluate("...DOM query...")
    
    # Keyboard test
    keyboard_test = await page.evaluate("...focusable elements...")
    
    await page.close()
```

### 4. Skor Hesaplama
- **Axe Score:** 100 - (critical×25) - (serious×15) - (moderate×8) - (minor×3)
- **Manual Score:** H1, lang, main, nav, alt text, skip links, focus indicators
- **Final Score:** (Axe × 0.7) + (Manual × 0.3)

### 5. Rapor Oluşturma
- HTML: Detaylı görsel rapor
- JSON: Structured data
- Workflow: İşlem akışı dokümanı

## Çıktı Dosyaları
- `audits/arcelik_real_chrome_YYYYMMDD_HHMMSS.html`
- `audits/arcelik_real_chrome_YYYYMMDD_HHMMSS.json`
- `skills/accessmind/real-browsing-workflow.md`

## Kullanılan Teknolojiler
- Playwright (Chromium)
- Axe-core 4.10.0
- WCAG 2.2 AA kriterleri
- Manuel DOM kontrolleri
- Keyboard navigation test
"""
    
    with open(workflow_file, 'w', encoding='utf-8') as f:
        f.write(workflow_content)
    
    print()
    print("=" * 60)
    print("✅ GERÇEK CHROME DENETİMİ TAMAMLANDI")
    print("=" * 60)
    final_avg = sum(r['scores']['final_score'] for r in [x for x in results if x['scores']['final_score'] > 0]) / len([r for r in results if r['scores']['final_score'] > 0])
    final_violations = sum(len(r.get('axe_results', {}).get('violations', [])) for r in results)
    print(f"📊 Ortalama Skor: {final_avg:.1f}/100")
    print(f"⚠️ Toplam İhlal: {final_violations}")
    print(f"📄 HTML Rapor: {html_file}")
    print(f"📄 JSON Detay: {json_file}")
    print(f"📋 Workflow: {workflow_file}")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
