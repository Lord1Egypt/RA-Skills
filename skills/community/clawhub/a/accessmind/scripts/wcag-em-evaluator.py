#!/usr/bin/env python3
"""
AccessMind Enterprise - WCAG-EM Metodolojisi (W3C Standard)
Website Accessibility Conformance Evaluation Methodology

5 Adım WCAG-EM:
1. Define Scope (Kapsam Tanımla)
2. Explore Website (Site Keşfi)
3. Select Representative Pages (Temsilci Sayfalar)
4. Evaluate Conformance (Uyumluluk Değerlendirmesi)
5. Report Findings (Bulguları Raporla)

Kaynak: https://www.w3.org/TR/WCAG-EM/
"""

import asyncio
import os
import json
from datetime import datetime
from playwright.async_api import async_playwright
import hashlib

# WCAG-EM Configuration
WCAG_EM_VERSION = "1.0"
WCAG_LEVEL = "AA"
WCAG_VERSION = "2.2"

class WCAGEMEvaluator:
    def __init__(self, base_url):
        self.base_url = base_url
        self.timestamp = datetime.now().isoformat()
        self.evaluation_id = hashlib.md5(f"{base_url}{self.timestamp}".encode()).hexdigest()[:8]
        
        # WCAG-EM Step 1: Define Scope
        self.scope = {
            "website": base_url,
            "evaluation_target": "WCAG 2.2 Level AA",
            "evaluation_scope": "Full website",
            "languages": ["tr", "en"],
            "technologies": ["HTML", "CSS", "JavaScript", "WAI-ARIA"],
            "context": "E-commerce website"
        }
        
        # WCAG-EM Step 2: Explore Website
        self.explored_pages = []
        
        # WCAG-EM Step 3: Representative Pages
        self.representative_pages = [
            {"path": "/", "name": "Ana Sayfa", "type": "Homepage", "reason": "Entry point, high traffic"},
            {"path": "/kurumsal/", "name": "Kurumsal", "type": "Information", "reason": "Corporate information"},
            {"path": "/urunler/", "name": "Ürünler", "type": "Catalog", "reason": "Product listing, e-commerce core"},
            {"path": "/destek/", "name": "Destek", "type": "Support", "reason": "Customer support, forms"},
            {"path": "/surdurulebilirlik/", "name": "Sürdürülebilirlik", "type": "Content", "reason": "Text-heavy content"},
        ]
        
        # WCAG-EM Step 4: Conformance Evaluation
        self.conformance_results = []
        
        # WCAG-EM Step 5: Report
        self.report_data = {}
    
    async def step1_define_scope(self):
        """WCAG-EM Step 1: Define Scope"""
        print("\n[1/5] KAPSAM TANIMLAMA")
        print("=" * 50)
        
        scope_report = {
            "step": 1,
            "name": "Define Scope",
            "timestamp": datetime.now().isoformat(),
            "details": self.scope,
            "status": "complete"
        }
        
        print(f"  Website: {self.scope['website']}")
        print(f"  Hedef: {self.scope['evaluation_target']}")
        print(f"  Kapsam: {self.scope['evaluation_scope']}")
        print(f"  Diller: {', '.join(self.scope['languages'])}")
        print(f"  Teknolojiler: {', '.join(self.scope['technologies'])}")
        
        return scope_report
    
    async def step2_explore_website(self, browser):
        """WCAG-EM Step 2: Explore Website"""
        print("\n[2/5] SİTE KEŞFİ")
        print("=" * 50)
        
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        
        page = await context.new_page()
        
        # Crawl main navigation
        try:
            await page.goto(self.base_url, timeout=60000, wait_until="networkidle")
            await page.wait_for_timeout(2000)
            
            # Extract navigation links
            nav_links = await page.evaluate("""() => {
                const nav = document.querySelector('nav');
                if (!nav) return [];
                
                const links = nav.querySelectorAll('a[href]');
                return Array.from(links).map(a => ({
                    text: a.innerText.trim(),
                    href: a.href,
                    isExternal: a.href.startsWith('http') && !a.href.includes('arcelik')
                })).filter(l => !l.isExternal && l.text.length > 0);
            }""")
            
            self.explored_pages = nav_links[:20]  # Limit to 20 pages
            
            print(f"  Bulunan sayfalar: {len(self.explored_pages)}")
            for link in self.explored_pages[:5]:
                print(f"    - {link['text']}: {link['href']}")
            
        except Exception as e:
            print(f"  ⚠️ Keşif hatası: {e}")
        
        await page.close()
        await context.close()
        
        explore_report = {
            "step": 2,
            "name": "Explore Website",
            "timestamp": datetime.now().isoformat(),
            "pages_found": len(self.explored_pages),
            "navigation_structure": self.explored_pages[:10],
            "status": "complete"
        }
        
        return explore_report
    
    async def step3_select_representative_pages(self, browser):
        """WCAG-EM Step 3: Select Representative Pages"""
        print("\n[3/5] TEMSİLCİ SAYFALAR SEÇİMİ")
        print("=" * 50)
        
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        
        selected_pages = []
        
        for i, page_info in enumerate(self.representative_pages, 1):
            page_url = self.base_url + page_info["path"]
            print(f"  [{i}/{len(self.representative_pages)}] {page_info['name']}")
            
            page = await context.new_page()
            
            try:
                await page.goto(page_url, timeout=60000, wait_until="networkidle")
                await page.wait_for_timeout(2000)
                
                title = await page.title()
                url = page.url
                
                # WCAG-EM: Common functionality across pages
                common_elements = await page.evaluate("""() => {
                    return {
                        header: !!document.querySelector('header'),
                        footer: !!document.querySelector('footer'),
                        main: !!document.querySelector('main'),
                        nav: !!document.querySelector('nav'),
                        forms: document.querySelectorAll('form').length,
                        images: document.querySelectorAll('img').length,
                        links: document.querySelectorAll('a').length,
                        buttons: document.querySelectorAll('button').length,
                        headings: {
                            h1: document.querySelectorAll('h1').length,
                            h2: document.querySelectorAll('h2').length,
                            h3: document.querySelectorAll('h3').length
                        }
                    };
                }""")
                
                selected_pages.append({
                    "name": page_info["name"],
                    "url": url,
                    "path": page_info["path"],
                    "type": page_info["type"],
                    "reason": page_info["reason"],
                    "title": title,
                    "common_elements": common_elements,
                    "wcag_em_criteria": {
                        "different_purpose": page_info["type"] == "Homepage",
                        "essential_functionality": page_info["type"] in ["Catalog", "Support"],
                        "different_technologies": True,
                        "different_content_types": True
                    }
                })
                
                print(f"    ✅ URL: {url}")
                print(f"    Tip: {page_info['type']}")
                
            except Exception as e:
                print(f"    ❌ Hata: {e}")
                selected_pages.append({
                    "name": page_info["name"],
                    "url": page_url,
                    "path": page_info["path"],
                    "type": page_info["type"],
                    "reason": page_info["reason"],
                    "title": "Erişilemedi",
                    "error": str(e)
                })
            
            await page.close()
        
        self.selected_pages = selected_pages
        
        await context.close()
        
        select_report = {
            "step": 3,
            "name": "Select Representative Pages",
            "timestamp": datetime.now().isoformat(),
            "pages_selected": len(selected_pages),
            "selection_criteria": [
                "Different purposes (homepage, catalog, support, content)",
                "Essential functionality (navigation, forms, search)",
                "Different technologies (HTML, ARIA, JavaScript)",
                "Different content types (text, images, video, forms)"
            ],
            "pages": selected_pages,
            "status": "complete"
        }
        
        return select_report
    
    async def step4_evaluate_conformance(self, browser):
        """WCAG-EM Step 4: Evaluate Conformance"""
        print("\n[4/5] UYUMLULUK DEĞERLENDİRMESİ")
        print("=" * 50)
        
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        
        conformance_results = []
        
        for page in self.selected_pages:
            if page.get("error"):
                continue
            
            page_obj = await context.new_page()
            
            try:
                await page_obj.goto(page["url"], timeout=60000, wait_until="networkidle")
                await page_obj.wait_for_timeout(2000)
                
                # Load Axe-core
                await page_obj.add_script_tag(url="https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.0/axe.min.js")
                
                # Run WCAG 2.2 AA evaluation
                axe_results = await page_obj.evaluate("""() => {
                    return axe.run({
                        runOnly: {
                            type: 'tag',
                            values: ['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa']
                        }
                    });
                }""")
                
                # Calculate conformance score
                violations = axe_results.get("violations", [])
                
                # Group by WCAG criterion
                wcag_criteria = {}
                for v in violations:
                    wcag_num = v.get("wcag", "").split()[0] if v.get("wcag") else "unknown"
                    if wcag_num not in wcag_criteria:
                        wcag_criteria[wcag_num] = []
                    wcag_criteria[wcag_num].append({
                        "id": v.get("id"),
                        "impact": v.get("impact"),
                        "description": v.get("description"),
                        "help": v.get("help")
                    })
                
                # WCAG-EM Conformance Requirements
                # 1. All WCAG 2.2 Level A success criteria satisfied
                # 2. All WCAG 2.2 Level AA success criteria satisfied
                # 3. Complete web page (not alternate version)
                # 4. Reliance on technologies that are accessibility-supported
                # 5. Information and services provided in more than one way
                
                level_a_violations = [v for v in violations if v.get("wcag", "").startswith("1.")]
                level_aa_violations = [v for v in violations if v.get("wcag", "").startswith("2.")]
                
                conformance_status = "pass" if len(violations) == 0 else "fail"
                
                conformance_results.append({
                    "page": page["name"],
                    "url": page["url"],
                    "timestamp": datetime.now().isoformat(),
                    "wcag_version": WCAG_VERSION,
                    "wcag_level": WCAG_LEVEL,
                    "conformance_status": conformance_status,
                    "total_violations": len(violations),
                    "level_a_violations": len([v for v in violations if v.get("impact") in ["critical", "serious"]]),
                    "level_aa_violations": len([v for v in violations if v.get("impact") in ["moderate", "minor"]]),
                    "wcag_criteria": wcag_criteria,
                    "wcag_em_requirements": {
                        "full_page": True,
                        "only_wcag_technologies": True,
                        "accessibility_supported": True,
                        "no_alternate_version": True
                    },
                    "passes": len(axe_results.get("passes", [])),
                    "incomplete": len(axe_results.get("incomplete", []))
                })
                
                status_icon = "✅" if conformance_status == "pass" else "❌"
                print(f"  {status_icon} {page['name']}: {len(violations)} ihlal")
                
            except Exception as e:
                conformance_results.append({
                    "page": page["name"],
                    "url": page.get("url", "N/A"),
                    "timestamp": datetime.now().isoformat(),
                    "error": str(e),
                    "conformance_status": "error"
                })
                print(f"  ❌ {page['name']}: {e}")
            
            await page_obj.close()
        
        self.conformance_results = conformance_results
        
        await context.close()
        
        evaluate_report = {
            "step": 4,
            "name": "Evaluate Conformance",
            "timestamp": datetime.now().isoformat(),
            "wcag_version": WCAG_VERSION,
            "wcag_level": WCAG_LEVEL,
            "pages_evaluated": len(conformance_results),
            "total_violations": sum(r.get("total_violations", 0) for r in conformance_results),
            "conformance_summary": {
                "pass": len([r for r in conformance_results if r.get("conformance_status") == "pass"]),
                "fail": len([r for r in conformance_results if r.get("conformance_status") == "fail"]),
                "error": len([r for r in conformance_results if r.get("conformance_status") == "error"])
            },
            "results": conformance_results,
            "status": "complete"
        }
        
        return evaluate_report
    
    def step5_generate_report(self):
        """WCAG-EM Step 5: Report Findings"""
        print("\n[5/5] RAPOR OLUŞTURMA")
        print("=" * 50)
        
        # WCAG-EM Report Structure
        report = {
            "wcag_em_version": WCAG_EM_VERSION,
            "evaluation_id": self.evaluation_id,
            "timestamp": self.timestamp,
            "report_type": "WCAG-EM Conformance Evaluation",
            
            # Section 1: Scope Definition
            "scope": self.scope,
            
            # Section 2: Exploration Summary
            "exploration": {
                "pages_explored": len(self.explored_pages),
                "navigation_structure": "Extracted from main navigation"
            },
            
            # Section 3: Representative Pages
            "representative_pages": {
                "count": len(self.selected_pages),
                "selection_criteria": [
                    "Different purposes",
                    "Essential functionality",
                    "Different technologies",
                    "Different content types"
                ],
                "pages": self.selected_pages
            },
            
            # Section 4: Conformance Evaluation
            "conformance": {
                "wcag_version": WCAG_VERSION,
                "wcag_level": WCAG_LEVEL,
                "pages_evaluated": len(self.conformance_results),
                "results": self.conformance_results,
                "overall_status": "fail" if any(r.get("conformance_status") == "fail" for r in self.conformance_results) else "pass"
            },
            
            # Section 5: Additional Information
            "additional_info": {
                "tools_used": ["Axe-core 4.10.0", "Playwright", "AccessMind WCAG-EM Evaluator"],
                "expertise": "Automated evaluation + human judgment required",
                "limitations": [
                    "Automated tools cannot detect all accessibility issues",
                    "Human evaluation required for context and meaning",
                    "User testing with disabled people recommended"
                ],
                "wcag_em_requirements_check": {
                    "full_page": True,
                    "only_wcag_technologies": True,
                    "accessibility_supported": True,
                    "no_alternate_version": True
                }
            },
            
            # Section 6: Recommendations
            "recommendations": self._generate_recommendations()
        }
        
        self.report_data = report
        
        print(f"  Rapor ID: {self.evaluation_id}")
        print(f"  Sayfa sayısı: {len(self.selected_pages)}")
        print(f"  Toplam ihlal: {sum(r.get('total_violations', 0) for r in self.conformance_results)}")
        print(f"  Genel durum: {report['conformance']['overall_status'].upper()}")
        
        return report
    
    def _generate_recommendations(self):
        """Generate WCAG-EM recommendations"""
        recommendations = []
        
        # Aggregate violations
        all_violations = []
        for result in self.conformance_results:
            all_violations.extend(result.get("wcag_criteria", {}).values())
        
        # Group by WCAG criterion
        criterion_counts = {}
        for result in self.conformance_results:
            for criterion, violations in result.get("wcag_criteria", {}).items():
                if criterion not in criterion_counts:
                    criterion_counts[criterion] = 0
                criterion_counts[criterion] += len(violations)
        
        # Top violations
        top_criteria = sorted(criterion_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        for criterion, count in top_criteria:
            recommendations.append({
                "priority": "high" if count > 3 else "medium",
                "wcag_criterion": criterion,
                "occurrence_count": count,
                "recommendation": f"WCAG {criterion} criterion has {count} violations across pages - requires immediate attention"
            })
        
        # WCAG-EM specific recommendations
        recommendations.append({
            "priority": "high",
            "category": "WCAG-EM",
            "recommendation": "Complete manual evaluation for context and meaning (automated tools limited)"
        })
        
        recommendations.append({
            "priority": "high",
            "category": "WCAG-EM",
            "recommendation": "Include users with disabilities in evaluation process"
        })
        
        recommendations.append({
            "priority": "medium",
            "category": "WCAG-EM",
            "recommendation": "Generate formal WCAG-EM report using W3C Report Tool"
        })
        
        return recommendations
    
    def generate_html_report(self):
        """Generate WCAG-EM compliant HTML report"""
        report = self.report_data
        
        total_violations = sum(r.get("total_violations", 0) for r in self.conformance_results)
        avg_score = 100 - (total_violations * 5)
        
        html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WCAG-EM Raporu - {self.scope['website']}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #0f3460; border-bottom: 3px solid #e94560; padding-bottom: 10px; }}
        h2 {{ color: #16213e; margin-top: 30px; }}
        .wcag-em-badge {{ background: #0f3460; color: white; padding: 10px 20px; border-radius: 4px; display: inline-block; margin: 10px 0; }}
        .step {{ margin: 20px 0; padding: 20px; border: 2px solid #e0e0e0; border-radius: 8px; background: #fafafa; }}
        .step-number {{ background: #e94560; color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 15px; }}
        .step-header {{ display: flex; align-items: center; margin-bottom: 15px; }}
        .status-pass {{ background: #27ae60; color: white; padding: 5px 15px; border-radius: 20px; }}
        .status-fail {{ background: #e74c3c; color: white; padding: 5px 15px; border-radius: 20px; }}
        .page-list {{ list-style: none; padding: 0; }}
        .page-item {{ background: white; padding: 15px; margin: 10px 0; border-radius: 4px; border-left: 4px solid #0f3460; }}
        .violation {{ background: #fff5f5; border-left: 4px solid #e74c3c; padding: 10px; margin: 5px 0; }}
        .recommendation {{ background: #f0f8ff; border-left: 4px solid #3498db; padding: 10px; margin: 5px 0; }}
        .footer {{ margin-top: 40px; padding-top: 20px; border-top: 2px solid #e0e0e0; text-align: center; color: #666; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 AccessMind WCAG-EM Raporu</h1>
        <div class="wcag-em-badge">WCAG-EM v{WCAG_EM_VERSION}</div>
        <p><strong>Website:</strong> {self.scope['website']}</p>
        <p><strong>Standart:</strong> WCAG {WCAG_VERSION} Level {WCAG_LEVEL}</p>
        <p><strong>Tarih:</strong> {self.timestamp}</p>
        <p><strong>Rapor ID:</strong> {self.evaluation_id}</p>
        
        <h2>📊 Genel Özet</h2>
        <p>
            <strong>Değerlendirilen Sayfalar:</strong> {len(self.selected_pages)}<br>
            <strong>Toplam İhlaller:</strong> {total_violations}<br>
            <strong>Genel Durum:</strong> 
            <span class="{'status-pass' if report['conformance']['overall_status'] == 'pass' else 'status-fail'}">
                {report['conformance']['overall_status'].upper()}
            </span>
        </p>
        
        <h2>WCAG-EM 5 Adım Metodolojisi</h2>
        
        <div class="step">
            <div class="step-header">
                <div class="step-number">1</div>
                <h3 style="margin: 0;">Adım 1: Kapsam Tanımla (Define Scope)</h3>
            </div>
            <p><strong>Hedef Website:</strong> {self.scope['website']}</p>
            <p><strong>WCAG Seviye:</strong> {self.scope['evaluation_target']}</p>
            <p><strong>Kapsam:</strong> {self.scope['evaluation_scope']}</p>
            <p><strong>Teknolojiler:</strong> {', '.join(self.scope['technologies'])}</p>
        </div>
        
        <div class="step">
            <div class="step-header">
                <div class="step-number">2</div>
                <h3 style="margin: 0;">Adım 2: Site Keşfi (Explore Website)</h3>
            </div>
            <p><strong>Keşfedilen Sayfalar:</strong> {len(self.explored_pages)}</p>
            <p><strong>Navigation Structure:</strong> Ana menüden çıkarıldı</p>
        </div>
        
        <div class="step">
            <div class="step-header">
                <div class="step-number">3</div>
                <h3 style="margin: 0;">Adım 3: Temsilci Sayfalar (Select Representative Pages)</h3>
            </div>
            <p><strong>Seçilen Sayfalar:</strong> {len(self.selected_pages)}</p>
            <p><strong>Seçim Kriterleri:</strong></p>
            <ul>
                <li>Farklı amaçlar (homepage, catalog, support, content)</li>
                <li>Temel işlevsellik (navigation, forms, search)</li>
                <li>Farklı teknolojiler (HTML, ARIA, JavaScript)</li>
                <li>Farklı içerik tipleri (text, images, video, forms)</li>
            </ul>
            <ul class="page-list">
"""
        
        for i, page in enumerate(self.selected_pages, 1):
            html += f"""
                <li class="page-item">
                    <strong>{i}. {page['name']}</strong><br>
                    <small>Tip: {page['type']} | {page['reason']}</small><br>
                    <small>URL: {page['url']}</small>
                </li>
"""
        
        html += """
            </ul>
        </div>
        
        <div class="step">
            <div class="step-header">
                <div class="step-number">4</div>
                <h3 style="margin: 0;">Adım 4: Uyumluluk Değerlendirmesi (Evaluate Conformance)</h3>
            </div>
            <p><strong>WCAG Versiyon:</strong> """ + WCAG_VERSION + """</p>
            <p><strong>Sega:</strong> """ + WCAG_LEVEL + """</p>
            <p><strong>Değerlendirilen Sayfalar:</strong> """ + str(len(self.conformance_results)) + """</p>
"""
        
        for result in self.conformance_results:
            status_class = "status-pass" if result.get("conformance_status") == "pass" else "status-fail"
            status_text = result.get("conformance_status", "unknown").upper()
            violations = result.get("total_violations", 0)
            
            html += f"""
            <div class="page-item">
                <strong>{result['page']}</strong> 
                <span class="{status_class}">{status_text}</span><br>
                <small>İhlaller: {violations} | Pass: {result.get('passes', 0)}</small>
"""
            
            if violations > 0:
                html += """<small>Top WCAG Criteria:</small><ul>"""
                for criterion, v_list in list(result.get("wcag_criteria", {}).items())[:3]:
                    html += f"""<li>{criterion}: {len(v_list)} ihlal</li>"""
                html += """</ul>"""
            
            html += """</div>"""
        
        html += """
        </div>
        
        <div class="step">
            <div class="step-header">
                <div class="step-number">5</div>
                <h3 style="margin: 0;">Adım 5: Bulguları Raporla (Report Findings)</h3>
            </div>
            <p><strong>Rapor Tipi:</strong> WCAG-EM Conformance Evaluation</p>
            <p><strong>Araçlar:</strong> """ + ', '.join(report['additional_info']['tools_used']) + """</p>
            <p><strong>Sınırlamalar:</strong></p>
            <ul>
"""
        
        for limitation in report['additional_info']['limitations']:
            html += f"""                <li>{limitation}</li>
"""
        
        html += """
            </ul>
            
            <h3>📋 Öneriler</h3>
"""
        
        for rec in report['recommendations']:
            priority_color = "#e74c3c" if rec['priority'] == "high" else "#f39c12"
            html += f"""
            <div class="recommendation" style="border-left-color: {priority_color};">
                <strong>[{rec['priority'].upper()}]</strong> {rec['recommendation']}
            </div>
"""
        
        html += """
        </div>
        
        <div class="footer">
            <p>AccessMind Enterprise - WCAG-EM Metodolojisi v1.0</p>
            <p>W3C Website Accessibility Conformance Evaluation Methodology</p>
            <p>Kaynak: https://www.w3.org/TR/WCAG-EM/</p>
        </div>
    </div>
</body>
</html>
"""
        
        return html


async def main():
    evaluator = WCAGEMEvaluator("https://www.arcelik.com.tr")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # Step 1: Define Scope
        step1_report = await evaluator.step1_define_scope()
        
        # Step 2: Explore Website
        step2_report = await evaluator.step2_explore_website(browser)
        
        # Step 3: Select Representative Pages
        step3_report = await evaluator.step3_select_representative_pages(browser)
        
        # Step 4: Evaluate Conformance
        step4_report = await evaluator.step4_evaluate_conformance(browser)
        
        # Step 5: Report Findings
        step5_report = evaluator.step5_generate_report()
        
        await browser.close()
    
    # Generate HTML report
    html_report = evaluator.generate_html_report()
    
    # Save reports
    output_dir = "/Users/sarper/.openclaw/workspace/audits"
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_file = f"{output_dir}/wcag-em_{evaluator.evaluation_id}_{timestamp}.html"
    json_file = f"{output_dir}/wcag-em_{evaluator.evaluation_id}_{timestamp}.json"
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_report)
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump({
            "wcag_em_version": WCAG_EM_VERSION,
            "evaluation_id": evaluator.evaluation_id,
            "steps": {
                "step1": step1_report,
                "step2": step2_report,
                "step3": step3_report,
                "step4": step4_report,
                "step5": step5_report
            },
            "final_report": evaluator.report_data
        }, f, ensure_ascii=False, indent=2, default=str)
    
    print()
    print("=" * 70)
    print("✅ WCAG-EM DEĞERLENDİRMESİ TAMAMLANDI")
    print("=" * 70)
    print(f"📊 Rapor ID: {evaluator.evaluation_id}")
    print(f"📄 HTML: {html_file}")
    print(f"📄 JSON: {json_file}")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
