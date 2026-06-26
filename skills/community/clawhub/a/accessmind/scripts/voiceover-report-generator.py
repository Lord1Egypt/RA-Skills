#!/usr/bin/env python3
"""
AccessMind VoiceOver ve Klavye Test Raporu Oluşturucu
WCAG 2.2 Uyumlu HTML Rapor
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

# Klavye ve VoiceOver test modülünü import et
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from keyboard_voiceover_test import (
    VoiceOverSimulator, 
    KeyboardA11yTester,
    calculate_a11y_score
)


def generate_voiceover_section(vo_results: dict) -> str:
    """VoiceOver bulguları için HTML bölümü oluştur"""
    
    # Başlık navigasyonu
    headings = vo_results.get("headings", {})
    heading_html = f"""
    <div class="vo-section">
        <h3>🔊 Başlık Navigasyonu (H Tuşu)</h3>
        <div class="vo-stats">
            <span class="stat">Toplam: {headings.get('total', 0)}</span>
            <span class="stat">H1: {headings.get('h1_count', 0)}</span>
            <span class="stat">H2: {headings.get('h2_count', 0)}</span>
            <span class="stat">H3: {headings.get('h3_count', 0)}</span>
        </div>
    """
    
    # VoiceOver duyuruları
    vo_announcements = headings.get("voiceover_announcements", [])
    for ann in vo_announcements[:10]:  # İlk 10
        status_class = "ok" if "OK" in ann.get("status", "") else "error"
        heading_html += f"""
        <div class="vo-announcement {status_class}">
            <span class="vo-level">H{ann.get('level', 2)}</span>
            <span class="vo-text">{ann.get('text', '')[:50]}</span>
            <span class="vo-duyuru">{ann.get('voiceover', '')}</span>
            <span class="vo-status">{ann.get('status', '')}</span>
        </div>
        """
    
    # Boş başlıklar
    empty_headings = headings.get("empty_headings", [])
    if empty_headings:
        heading_html += "<h4>❌ Boş/eksik başlıklar:</h4><ul>"
        for eh in empty_headings:
            heading_html += f"<li>H{eh.get('level')}: {eh.get('issue')}</li>"
        heading_html += "</ul>"
    
    # Hiyerarşi sorunları
    hierarchy_issues = headings.get("hierarchy_issues", [])
    if hierarchy_issues:
        heading_html += "<h4>⚠️ Hiyerarşi sorunları:</h4><ul>"
        for hi in hierarchy_issues:
            heading_html += f"<li>{hi.get('from')} → {hi.get('to')}: {hi.get('issue')}</li>"
        heading_html += "</ul>"
    
    heading_html += "</div>"
    
    # Link navigasyonu
    links = vo_results.get("links", {})
    link_html = f"""
    <div class="vo-section">
        <h3>🔊 Link Navigasyonu (U Tuşu)</h3>
        <div class="vo-stats">
            <span class="stat">Toplam: {links.get('total', 0)}</span>
            <span class="stat error">Boş: {len(links.get('empty_links', []))}</span>
            <span class="stat warning">Belirsiz: {len(links.get('vague_links', []))}</span>
            <span class="stat ok">Geçerli: {len(links.get('valid_links', []))}</span>
        </div>
    """
    
    # Boş linkler
    empty_links = links.get("empty_links", [])
    if empty_links:
        link_html += "<h4>❌ Boş linkler:</h4><ul>"
        for el in empty_links[:5]:
            link_html += f"<li>{el.get('ref')}: {el.get('issue')}</li>"
        link_html += "</ul>"
    
    # Belirsiz linkler
    vague_links = links.get("vague_links", [])
    if vague_links:
        link_html += "<h4>⚠️ Belirsiz linkler:</h4><ul>"
        for vl in vague_links[:5]:
            link_html += f"<li>'{vl.get('text', '')[:30]}': {vl.get('issue')}</li>"
        link_html += "</ul>"
    
    link_html += "</div>"
    
    # Buton navigasyonu
    buttons = vo_results.get("buttons", {})
    button_html = f"""
    <div class="vo-section">
        <h3>🔊 Buton Navigasyonu (B Tuşu)</h3>
        <div class="vo-stats">
            <span class="stat">Toplam: {buttons.get('total', 0)}</span>
            <span class="stat error">Boş: {len(buttons.get('empty_buttons', []))}</span>
            <span class="stat warning">İkon: {len(buttons.get('icon_only_buttons', []))}</span>
            <span class="stat ok">Geçerli: {len(buttons.get('valid_buttons', []))}</span>
        </div>
    """
    
    # Boş butonlar
    empty_buttons = buttons.get("empty_buttons", [])
    if empty_buttons:
        button_html += "<h4>❌ İsimsiz butonlar:</h4><ul>"
        for eb in empty_buttons[:5]:
            button_html += f"<li>{eb.get('ref')}: {eb.get('issue')}</li>"
        button_html += "</ul>"
    
    button_html += "</div>"
    
    # Form navigasyonu
    forms = vo_results.get("forms", {})
    form_html = f"""
    <div class="vo-section">
        <h3>🔊 Form Navigasyonu (F Tuşu)</h3>
        <div class="vo-stats">
            <span class="stat">Toplam: {forms.get('total', 0)}</span>
            <span class="stat error">Labelsız: {len(forms.get('unlabeled_inputs', []))}</span>
            <span class="stat ok">Geçerli: {len(forms.get('valid_inputs', []))}</span>
        </div>
    """
    
    # Labelsız inputlar
    unlabeled = forms.get("unlabeled_inputs", [])
    if unlabeled:
        form_html += "<h4>❌ Labelsız form alanları:</h4><ul>"
        for u in unlabeled[:5]:
            form_html += f"<li>{u.get('type')}: {u.get('issue')}</li>"
        form_html += "</ul>"
    
    form_html += "</div>"
    
    # Landmark navigasyonu
    landmarks = vo_results.get("landmarks", {})
    landmark_html = f"""
    <div class="vo-section">
        <h3>🔊 Landmark Navigasyonu (D Tuşu)</h3>
        <div class="vo-stats">
            <span class="stat">Toplam: {landmarks.get('total', 0)}</span>
        </div>
    """
    
    # Bulunan landmark'lar
    found = landmarks.get("found_landmarks", [])
    if found:
        landmark_html += "<h4>✅ Bulunan landmark'lar:</h4><ul>"
        for f in found:
            landmark_html += f"<li>{f.get('type')}</li>"
        landmark_html += "</ul>"
    
    # Eksik landmark'lar
    missing = landmarks.get("missing_landmarks", [])
    if missing:
        landmark_html += "<h4>❌ Eksik landmark'lar:</h4><ul>"
        for m in missing:
            landmark_html += f"<li>{m.get('type')}: {m.get('issue')}</li>"
        landmark_html += "</ul>"
    
    landmark_html += "</div>"
    
    return heading_html + link_html + button_html + form_html + landmark_html


def generate_keyboard_section(kb_results: dict) -> str:
    """Klavye bulguları için HTML bölümü oluştur"""
    
    html = "<div class='keyboard-section'><h3>⌨️ Klavye Erişilebilirlik Testi</h3>"
    
    # Focus order
    focus_order = kb_results.get("focus_order", [])
    if focus_order:
        html += "<h4>Focus Sırası Sorunları:</h4><ul>"
        for fo in focus_order:
            severity = fo.get("severity", "medium")
            severity_class = "error" if severity == "critical" else "warning"
            html += f"""
            <li class="{severity_class}">
                <strong>{fo.get('type')}</strong>: {fo.get('description')}
                <br><small>WCAG {fo.get('wcag')}</small>
            </li>
            """
        html += "</ul>"
    else:
        html += "<p class='ok'>✅ Focus sırasında sorun bulunamadı</p>"
    
    # Focus visible
    focus_visible = kb_results.get("focus_visible", [])
    if focus_visible:
        html += "<h4>Focus Görünürlük Sorunları:</h4><ul>"
        for fv in focus_visible:
            severity = fv.get("severity", "medium")
            severity_class = "error" if severity == "critical" else "warning"
            html += f"""
            <li class="{severity_class}">
                <strong>{fv.get('type')}</strong>: {fv.get('description')}
                <br><small>WCAG {fv.get('wcag')}</small>
            </li>
            """
        html += "</ul>"
    else:
        html += "<p class='ok'>✅ Focus göstergesi mevcut</p>"
    
    # Keyboard traps
    traps = kb_results.get("keyboard_traps", [])
    if traps:
        html += "<h4>❌ Klavye Tuzakları:</h4><ul>"
        for trap in traps:
            html += f"""
            <li class="error">
                <strong>{trap.get('type')}</strong>: {trap.get('description')}
                <br><small>WCAG {trap.get('wcag')} - {trap.get('solution')}</small>
            </li>
            """
        html += "</ul>"
    else:
        html += "<p class='ok'>✅ Klavye tuzağı bulunamadı</p>"
    
    html += "</div>"
    return html


def generate_full_report(accessibility_tree: dict, page_name: str, page_url: str) -> str:
    """Tam HTML rapor oluştur"""
    
    # Test sınıflarını başlat
    keyboard_tester = KeyboardA11yTester(accessibility_tree)
    vo_simulator = VoiceOverSimulator(accessibility_tree)
    
    # Testleri çalıştır
    kb_results = {
        "focus_order": keyboard_tester.analyze_focus_order(),
        "focus_visible": keyboard_tester.analyze_focus_visible(),
        "keyboard_traps": keyboard_tester.analyze_keyboard_traps()
    }
    
    vo_results = {
        "headings": vo_simulator.simulate_heading_navigation(),
        "links": vo_simulator.simulate_link_navigation(),
        "buttons": vo_simulator.simulate_button_navigation(),
        "forms": vo_simulator.simulate_form_navigation(),
        "landmarks": vo_simulator.simulate_landmark_navigation()
    }
    
    # Skor hesapla
    score = calculate_a11y_score({
        "keyboard": kb_results,
        "voiceover": vo_results
    })
    
    # Skor rengi
    if score >= 90:
        score_color = "#28a745"
        score_label = "🟢 Mükemmel"
    elif score >= 75:
        score_color = "#20c997"
        score_label = "🟢 İyi"
    elif score >= 60:
        score_color = "#ffc107"
        score_label = "🟡 Orta"
    elif score >= 40:
        score_color = "#fd7e14"
        score_label = "🟠 Zayıf"
    else:
        score_color = "#dc3545"
        score_label = "🔴 Kritik"
    
    # VoiceOver bölümü
    vo_html = generate_voiceover_section(vo_results)
    
    # Klavye bölümü
    kb_html = generate_keyboard_section(kb_results)
    
    # Tam HTML
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_name} - VoiceOver ve Klavye Test Raporu</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; color: #333; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; border-radius: 15px; margin-bottom: 30px; }}
        h1 {{ margin-bottom: 10px; }}
        .subtitle {{ opacity: 0.9; }}
        .score-card {{ background: white; border-radius: 15px; padding: 30px; text-align: center; margin-bottom: 30px; box-shadow: 0 5px 20px rgba(0,0,0,0.1); }}
        .score-big {{ font-size: 5em; font-weight: bold; color: {score_color}; }}
        .score-label {{ font-size: 1.5em; margin-top: 10px; color: #666; }}
        .vo-section {{ background: white; border-radius: 10px; padding: 25px; margin-bottom: 20px; box-shadow: 0 3px 10px rgba(0,0,0,0.08); }}
        .vo-section h3 {{ color: #667eea; margin-bottom: 15px; border-bottom: 2px solid #667eea; padding-bottom: 10px; }}
        .vo-stats {{ display: flex; gap: 15px; margin-bottom: 15px; flex-wrap: wrap; }}
        .stat {{ background: #f8f9fa; padding: 8px 15px; border-radius: 20px; font-size: 0.9em; }}
        .stat.ok {{ background: #d4edda; color: #28a745; }}
        .stat.warning {{ background: #fff3cd; color: #856404; }}
        .stat.error {{ background: #f8d7da; color: #dc3545; }}
        .vo-announcement {{ display: flex; align-items: center; gap: 10px; padding: 10px; margin-bottom: 5px; border-radius: 5px; font-size: 0.9em; }}
        .vo-announcement.ok {{ background: #d4edda; }}
        .vo-announcement.error {{ background: #f8d7da; }}
        .vo-level {{ font-weight: bold; color: #667eea; min-width: 40px; }}
        .vo-text {{ flex: 1; }}
        .vo-duyuru {{ font-style: italic; color: #666; }}
        .vo-status {{ font-weight: bold; }}
        h4 {{ color: #0f3460; margin: 15px 0 10px; }}
        ul {{ margin-left: 20px; }}
        li {{ margin-bottom: 5px; }}
        li.error {{ color: #dc3545; }}
        li.warning {{ color: #856404; }}
        .keyboard-section {{ background: white; border-radius: 10px; padding: 25px; margin-bottom: 20px; box-shadow: 0 3px 10px rgba(0,0,0,0.08); }}
        .keyboard-section h3 {{ color: #e94560; margin-bottom: 15px; border-bottom: 2px solid #e94560; padding-bottom: 10px; }}
        p.ok {{ background: #d4edda; padding: 10px; border-radius: 5px; color: #28a745; }}
        footer {{ text-align: center; padding: 30px; color: #666; }}
        .summary-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .summary-card {{ background: white; border-radius: 10px; padding: 20px; text-align: center; box-shadow: 0 3px 10px rgba(0,0,0,0.08); }}
        .summary-card h4 {{ color: #667eea; margin-bottom: 10px; }}
        .summary-card .value {{ font-size: 2em; font-weight: bold; }}
        .summary-card.success .value {{ color: #28a745; }}
        .summary-card.warning .value {{ color: #ffc107; }}
        .summary-card.error .value {{ color: #dc3545; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔊 VoiceOver & ⌨️ Klavye Test Raporu</h1>
            <p class="subtitle">{page_name}</p>
            <p style="margin-top: 10px; opacity: 0.8;">{page_url}</p>
            <p style="margin-top: 5px; opacity: 0.7;">Tarih: {now}</p>
        </header>
        
        <div class="score-card">
            <div class="score-big">{score}</div>
            <div class="score-label">{score_label}</div>
            <p style="margin-top: 10px; color: #666;">Erişilebilirlik Skoru</p>
        </div>
        
        <div class="summary-grid">
            <div class="summary-card {'success' if vo_results['headings']['h1_count'] > 0 else 'error'}">
                <h4>H1 Başlık</h4>
                <div class="value">{vo_results['headings']['h1_count']}</div>
            </div>
            <div class="summary-card {'success' if len(vo_results['links']['empty_links']) == 0 else 'error'}">
                <h4>Boş Link</h4>
                <div class="value">{len(vo_results['links']['empty_links'])}</div>
            </div>
            <div class="summary-card {'success' if len(vo_results['buttons']['empty_buttons']) == 0 else 'error'}">
                <h4>İsimsiz Buton</h4>
                <div class="value">{len(vo_results['buttons']['empty_buttons'])}</div>
            </div>
            <div class="summary-card {'success' if len(vo_results['forms']['unlabeled_inputs']) == 0 else 'error'}">
                <h4>Labelsız Form</h4>
                <div class="value">{len(vo_results['forms']['unlabeled_inputs'])}</div>
            </div>
            <div class="summary-card {'success' if len(vo_results['landmarks']['missing_landmarks']) == 0 else 'warning'}">
                <h4>Eksik Landmark</h4>
                <div class="value">{len(vo_results['landmarks']['missing_landmarks'])}</div>
            </div>
            <div class="summary-card {'success' if len(kb_results['keyboard_traps']) == 0 else 'error'}">
                <h4>Klavye Tuzağı</h4>
                <div class="value">{len(kb_results['keyboard_traps'])}</div>
            </div>
        </div>
        
        {vo_html}
        
        {kb_html}
        
        <footer>
            <p>Bu rapor WCAG 2.2 kriterlerine göre VoiceOver simülasyonu ve klavye erişilebilirlik testi ile oluşturulmuştur.</p>
            <p style="margin-top: 10px;"><strong>AccessMind</strong> Erişilebilirlik Denetim Sistemi © 2026</p>
        </footer>
    </div>
</body>
</html>"""
    
    return html


if __name__ == "__main__":
    # Örnek accessibility tree ile test
    sample_tree = {
        "role": "document",
        "children": [
            {"role": "heading", "aria-level": 1, "text": "Ana Başlık", "ref": "h1-1"},
            {"role": "heading", "aria-level": 2, "text": "Bölüm 1", "ref": "h2-1"},
            {"role": "link", "text": "Tıklayın", "href": "#", "ref": "link-1"},
            {"role": "link", "text": "Ürün Detayı", "href": "/urun", "ref": "link-2"},
            {"role": "button", "text": "", "aria-label": "Ara", "ref": "btn-1"},
            {"role": "button", "text": "Sepete Ekle", "ref": "btn-2"},
            {"role": "textbox", "type": "text", "aria-label": "E-posta", "ref": "input-1"},
            {"role": "textbox", "type": "text", "placeholder": "Ara...", "ref": "input-2"},
        ]
    }
    
    html = generate_full_report(sample_tree, "Test Sayfası", "https://example.com")
    
    # Raporu kaydet
    output_path = "/Users/sarper/.openclaw/workspace/audits/voiceover-test-raporu.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Rapor oluşturuldu: {output_path}")