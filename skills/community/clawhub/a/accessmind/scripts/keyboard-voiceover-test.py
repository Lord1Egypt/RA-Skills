#!/usr/bin/env python3
"""
AccessMind Klavye ve VoiceOver Erişilebilirlik Testi
WCAG 2.2 Uyumlu Kapsamlı Test Protokolü
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Tuple

class KeyboardA11yTester:
    """Klavye erişilebilirlik test sınıfı"""
    
    def __init__(self, accessibility_tree: dict):
        self.tree = accessibility_tree
        self.findings = {
            "focus_order": [],
            "focus_visible": [],
            "focus_trap": [],
            "keyboard_accessible": [],
            "tabindex_issues": []
        }
    
    def analyze_focus_order(self) -> List[Dict]:
        """Tab sırasını analiz et"""
        issues = []
        
        # Accessibility tree'den focusable elementleri bul
        focusable_elements = self._extract_focusable_elements()
        
        # Tabindex değerlerini kontrol et
        tabindex_values = []
        for elem in focusable_elements:
            tabindex = elem.get("tabindex")
            if tabindex:
                try:
                    val = int(tabindex)
                    if val > 0:
                        tabindex_values.append((elem, val))
                except:
                    pass
        
        # Pozitif tabindex kullanımı (WCAG ihlali)
        if tabindex_values:
            issues.append({
                "type": "positive_tabindex",
                "severity": "medium",
                "wcag": "2.4.3 Focus Order",
                "count": len(tabindex_values),
                "description": f"{len(tabindex_values)} element pozitif tabindex kullanıyor. Doğal DOM sırası önerilir.",
                "elements": [e[0].get("ref", "unknown") for e in tabindex_values[:5]]
            })
        
        return issues
    
    def analyze_focus_visible(self) -> List[Dict]:
        """Focus göstergesi kontrolü"""
        issues = []
        
        # Focusable elementler
        focusable = self._extract_focusable_elements()
        
        # Interactive elementler
        buttons = [e for e in focusable if e.get("role") == "button" or e.get("tag") == "button"]
        links = [e for e in focusable if e.get("role") == "link" or e.get("tag") == "a"]
        inputs = [e for e in focusable if e.get("tag") in ["input", "select", "textarea"]]
        
        # Focus stilinin olmadığı elementler (varsayımsal - gerçek test için CSS gerekiyor)
        if not buttons and not links and not inputs:
            issues.append({
                "type": "no_focusable_elements",
                "severity": "critical",
                "wcag": "2.1.1 Keyboard",
                "description": "Sayfada focusable element bulunamadı"
            })
        
        return issues
    
    def analyze_keyboard_traps(self) -> List[Dict]:
        """Focus tuzağı kontrolü"""
        issues = []
        
        # Modal, dialog gibi elementler
        dialogs = self._extract_by_role("dialog")
        modals = self._extract_by_role("modal")
        
        for dialog in dialogs + modals:
            # Modal için escape ile çıkış var mı?
            has_close = dialog.get("has_close") or self._has_close_button(dialog)
            has_escape = dialog.get("aria_escape") or has_close
            
            if not has_escape:
                issues.append({
                    "type": "keyboard_trap",
                    "severity": "critical",
                    "wcag": "2.1.2 No Keyboard Trap",
                    "description": f"Modal/dialog'den klavye ile çıkış yok: {dialog.get('ref', 'unknown')}",
                    "solution": "ESC tuşu ile kapatma ekleyin"
                })
        
        return issues
    
    def _extract_focusable_elements(self) -> List[Dict]:
        """Focusable elementleri çıkar"""
        elements = []
        
        def traverse(node):
            if isinstance(node, dict):
                role = node.get("role", "")
                tag = node.get("tag", "").lower()
                tabindex = node.get("tabindex")
                
                # Focusable elementler
                focusable_roles = ["button", "link", "checkbox", "radio", "tab", "menuitem", "option"]
                focusable_tags = ["a", "button", "input", "select", "textarea"]
                
                is_focusable = (
                    role in focusable_roles or
                    tag in focusable_tags or
                    tabindex is not None
                )
                
                if is_focusable:
                    elements.append(node)
                
                # Children'ı gez
                for key, value in node.items():
                    if isinstance(value, list):
                        for item in value:
                            traverse(item)
                    elif isinstance(value, dict):
                        traverse(value)
        
        traverse(self.tree)
        return elements
    
    def _extract_by_role(self, role: str) -> List[Dict]:
        """Belirli roldeki elementleri çıkar"""
        elements = []
        
        def traverse(node):
            if isinstance(node, dict):
                if node.get("role") == role:
                    elements.append(node)
                
                for key, value in node.items():
                    if isinstance(value, list):
                        for item in value:
                            traverse(item)
                    elif isinstance(value, dict):
                        traverse(value)
        
        traverse(self.tree)
        return elements
    
    def _has_close_button(self, dialog: Dict) -> bool:
        """Dialog'da close butonu var mı"""
        # Basit kontrol - geliştirilebilir
        text = str(dialog).lower()
        return "close" in text or "kapat" in text or "x" in text


class VoiceOverSimulator:
    """VoiceOver simülasyon sınıfı"""
    
    def __init__(self, accessibility_tree: dict):
        self.tree = accessibility_tree
        self.findings = {
            "headings": {"valid": [], "invalid": []},
            "links": {"valid": [], "invalid": []},
            "buttons": {"valid": [], "invalid": []},
            "forms": {"valid": [], "invalid": []},
            "landmarks": {"valid": [], "missing": []}
        }
    
    def simulate_heading_navigation(self) -> Dict:
        """H tuşu simülasyonu - Başlık navigasyonu"""
        headings = self._extract_headings()
        
        results = {
            "total": len(headings),
            "h1_count": 0,
            "h2_count": 0,
            "h3_count": 0,
            "h4_count": 0,
            "h5_count": 0,
            "h6_count": 0,
            "empty_headings": [],
            "hierarchy_issues": [],
            "voiceover_announcements": []
        }
        
        prev_level = 0
        for h in headings:
            level = h.get("level", 0)
            text = h.get("text", "").strip()
            
            # Seviye sayaçları
            if level == 1:
                results["h1_count"] += 1
            elif level == 2:
                results["h2_count"] += 1
            elif level == 3:
                results["h3_count"] += 1
            elif level == 4:
                results["h4_count"] += 1
            elif level == 5:
                results["h5_count"] += 1
            elif level == 6:
                results["h6_count"] += 1
            
            # Boş başlık kontrolü
            if not text:
                results["empty_headings"].append({
                    "level": level,
                    "ref": h.get("ref", "unknown"),
                    "issue": "Başlık metni boş"
                })
            
            # Hiyerarşi kontrolü
            if level > prev_level + 1 and prev_level > 0:
                results["hierarchy_issues"].append({
                    "from": f"H{prev_level}",
                    "to": f"H{level}",
                    "text": text[:50] if text else "(boş)",
                    "issue": f"H{prev_level}'den H{level}'e atlama"
                })
            
            prev_level = level
            
            # VoiceOver duyurusu
            vo_text = f"Başlık seviyesi {level}, {text}" if text else f"Başlık seviyesi {level}"
            results["voiceover_announcements"].append({
                "level": level,
                "text": text,
                "voiceover": vo_text,
                "status": "✅ OK" if text else "❌ BOŞ"
            })
        
        # H1 kontrolü
        if results["h1_count"] == 0:
            results["empty_headings"].append({
                "level": 1,
                "ref": "page",
                "issue": "H1 başlığı bulunamadı"
            })
        elif results["h1_count"] > 1:
            results["hierarchy_issues"].append({
                "from": "H1",
                "to": "H1",
                "text": f"{results['h1_count']} adet H1",
                "issue": f"Sayfada {results['h1_count']} adet H1 var, 1 olmalı"
            })
        
        return results
    
    def simulate_link_navigation(self) -> Dict:
        """U tuşu simülasyonu - Link navigasyonu"""
        links = self._extract_links()
        
        results = {
            "total": len(links),
            "empty_links": [],
            "vague_links": [],
            "url_as_text": [],
            "valid_links": [],
            "voiceover_announcements": []
        }
        
        vague_words = ["tıkla", "tıklayın", "buraya", "buradan", "devam", "devamı", 
                       "daha fazla", "link", "click", "here", "more", "read more",
                       "incele", "detay", "git"]
        
        for link in links:
            text = link.get("text", "").strip()
            aria_label = link.get("aria_label", "").strip()
            href = link.get("href", "")
            ref = link.get("ref", "unknown")
            
            # Boş link kontrolü
            if not text and not aria_label:
                results["empty_links"].append({
                    "ref": ref,
                    "href": href,
                    "issue": "Link metni ve aria-label boş"
                })
                results["voiceover_announcements"].append({
                    "text": text or "(boş)",
                    "voiceover": "link",
                    "status": "❌ BOŞ"
                })
                continue
            
            # Belirsiz link kontrolü
            link_text = text.lower() if text else aria_label.lower()
            is_vague = any(word in link_text for word in vague_words)
            
            if is_vague and len(link_text) < 20:
                results["vague_links"].append({
                    "ref": ref,
                    "text": text or aria_label,
                    "href": href,
                    "issue": f"Belirsiz link metni: '{text or aria_label}'"
                })
                results["voiceover_announcements"].append({
                    "text": text or aria_label,
                    "voiceover": f"{text or aria_label}, link",
                    "status": "⚠️ BELİRSİZ"
                })
                continue
            
            # URL metin kontrolü
            if text.startswith("http") or text.startswith("www."):
                results["url_as_text"].append({
                    "ref": ref,
                    "text": text,
                    "issue": "URL link metni olarak kullanılıyor"
                })
                results["voiceover_announcements"].append({
                    "text": text,
                    "voiceover": f"{text}, link",
                    "status": "⚠️ URL"
                })
                continue
            
            # Geçerli link
            results["valid_links"].append(link)
            results["voiceover_announcements"].append({
                "text": text or aria_label,
                "voiceover": f"{text or aria_label}, link",
                "status": "✅ OK"
            })
        
        return results
    
    def simulate_button_navigation(self) -> Dict:
        """B tuşu simülasyonu - Buton navigasyonu"""
        buttons = self._extract_buttons()
        
        results = {
            "total": len(buttons),
            "empty_buttons": [],
            "icon_only_buttons": [],
            "disabled_buttons": [],
            "valid_buttons": [],
            "voiceover_announcements": []
        }
        
        for btn in buttons:
            text = btn.get("text", "").strip()
            aria_label = btn.get("aria_label", "").strip()
            disabled = btn.get("disabled", False)
            ref = btn.get("ref", "unknown")
            
            # Boş buton kontrolü
            if not text and not aria_label:
                results["empty_buttons"].append({
                    "ref": ref,
                    "issue": "Buton metni ve aria-label boş"
                })
                results["voiceover_announcements"].append({
                    "text": "(boş)",
                    "voiceover": "button",
                    "status": "❌ BOŞ"
                })
                continue
            
            # Sadece ikon kontrolü (tek karakter veya kısa)
            btn_text = text or aria_label
            if len(btn_text) <= 2 and not btn_text.isalpha():
                results["icon_only_buttons"].append({
                    "ref": ref,
                    "text": btn_text,
                    "issue": "Sadece ikon buton, aria-label ekleyin"
                })
                results["voiceover_announcements"].append({
                    "text": btn_text,
                    "voiceover": f"{btn_text}, button",
                    "status": "⚠️ İKON"
                })
                continue
            
            # Disabled buton kontrolü
            if disabled:
                results["disabled_buttons"].append(btn)
                results["voiceover_announcements"].append({
                    "text": btn_text,
                    "voiceover": f"{btn_text}, dimmed button",
                    "status": "⚠️ DISABLED"
                })
                continue
            
            # Geçerli buton
            results["valid_buttons"].append(btn)
            results["voiceover_announcements"].append({
                "text": btn_text,
                "voiceover": f"{btn_text}, button",
                "status": "✅ OK"
            })
        
        return results
    
    def simulate_form_navigation(self) -> Dict:
        """F tuşu simülasyonu - Form alanı navigasyonu"""
        forms = self._extract_form_elements()
        
        results = {
            "total": len(forms),
            "unlabeled_inputs": [],
            "missing_autocomplete": [],
            "valid_inputs": [],
            "voiceover_announcements": []
        }
        
        for form in forms:
            input_type = form.get("type", "text")
            label = form.get("label", "").strip()
            aria_label = form.get("aria_label", "").strip()
            placeholder = form.get("placeholder", "").strip()
            name = form.get("name", "")
            ref = form.get("ref", "unknown")
            
            # Label kontrolü
            if not label and not aria_label:
                # Placeholder'ı label sanıyor olabilir
                if placeholder:
                    results["unlabeled_inputs"].append({
                        "ref": ref,
                        "type": input_type,
                        "placeholder": placeholder,
                        "issue": f"Placeholder label olarak kullanılıyor: '{placeholder}'"
                    })
                    results["voiceover_announcements"].append({
                        "text": placeholder,
                        "voiceover": f"{placeholder}, {input_type} alanı",
                        "status": "⚠️ PLACEHOLDER"
                    })
                else:
                    results["unlabeled_inputs"].append({
                        "ref": ref,
                        "type": input_type,
                        "issue": "Form alanının label'ı yok"
                    })
                    results["voiceover_announcements"].append({
                        "text": "(boş)",
                        "voiceover": f"{input_type} alanı",
                        "status": "❌ LABELSIZ"
                    })
                continue
            
            # Autocomplete kontrolü
            autocomplete_sensitive = ["email", "password", "tel", "name", "address"]
            if input_type in autocomplete_sensitive or name in autocomplete_sensitive:
                if not form.get("autocomplete"):
                    results["missing_autocomplete"].append(form)
            
            # Geçerli input
            results["valid_inputs"].append(form)
            results["voiceover_announcements"].append({
                "text": label or aria_label,
                "voiceover": f"{label or aria_label}, {input_type} alanı",
                "status": "✅ OK"
            })
        
        return results
    
    def simulate_landmark_navigation(self) -> Dict:
        """D tuşu simülasyonu - Landmark navigasyonu"""
        landmarks = self._extract_landmarks()
        
        results = {
            "total": len(landmarks),
            "found_landmarks": [],
            "missing_landmarks": [],
            "voiceover_announcements": []
        }
        
        # Beklenen landmark'lar
        expected = ["banner", "main", "navigation", "contentinfo"]
        found_types = []
        
        for lm in landmarks:
            lm_type = lm.get("type", lm.get("role", ""))
            found_types.append(lm_type)
            
            results["found_landmarks"].append(lm)
            results["voiceover_announcements"].append({
                "type": lm_type,
                "voiceover": f"{lm_type}, landmark",
                "status": "✅ OK"
            })
        
        # Eksik landmark'lar
        for exp in expected:
            if exp not in found_types:
                results["missing_landmarks"].append({
                    "type": exp,
                    "issue": f"{exp} landmark bulunamadı"
                })
                results["voiceover_announcements"].append({
                    "type": exp,
                    "voiceover": f"{exp} landmark yok",
                    "status": "❌ EKSİK"
                })
        
        return results
    
    def _extract_headings(self) -> List[Dict]:
        """Başlık elementlerini çıkar"""
        headings = []
        
        def traverse(node, path=""):
            if isinstance(node, dict):
                if node.get("role") == "heading":
                    level = node.get("aria-level", 2)
                    text = node.get("text", "")
                    headings.append({
                        "level": int(level),
                        "text": text,
                        "ref": node.get("ref", "unknown")
                    })
                
                for key, value in node.items():
                    if isinstance(value, list):
                        for i, item in enumerate(value):
                            traverse(item, f"{path}.{key}[{i}]")
                    elif isinstance(value, dict):
                        traverse(value, f"{path}.{key}")
        
        traverse(self.tree)
        return headings
    
    def _extract_links(self) -> List[Dict]:
        """Link elementlerini çıkar"""
        links = []
        
        def traverse(node):
            if isinstance(node, dict):
                if node.get("role") == "link" or "link" in str(node.get("ref", "")).lower():
                    links.append({
                        "text": node.get("text", ""),
                        "aria_label": node.get("aria-label", ""),
                        "href": node.get("href", ""),
                        "ref": node.get("ref", "unknown")
                    })
                
                for key, value in node.items():
                    if isinstance(value, list):
                        for item in value:
                            traverse(item)
                    elif isinstance(value, dict):
                        traverse(value)
        
        traverse(self.tree)
        return links
    
    def _extract_buttons(self) -> List[Dict]:
        """Buton elementlerini çıkar"""
        buttons = []
        
        def traverse(node):
            if isinstance(node, dict):
                if node.get("role") == "button" or "button" in str(node).lower():
                    buttons.append({
                        "text": node.get("text", ""),
                        "aria_label": node.get("aria-label", ""),
                        "disabled": node.get("disabled", False),
                        "ref": node.get("ref", "unknown")
                    })
                
                for key, value in node.items():
                    if isinstance(value, list):
                        for item in value:
                            traverse(item)
                    elif isinstance(value, dict):
                        traverse(value)
        
        traverse(self.tree)
        return buttons
    
    def _extract_form_elements(self) -> List[Dict]:
        """Form elementlerini çıkar"""
        forms = []
        
        def traverse(node):
            if isinstance(node, dict):
                node_type = node.get("type", "")
                if node_type in ["text", "email", "password", "tel", "search", "url", "number"] or \
                   node.get("role") == "textbox" or \
                   node.get("role") == "combobox" or \
                   node.get("role") == "listbox":
                    forms.append({
                        "type": node_type,
                        "label": node.get("label", ""),
                        "aria_label": node.get("aria-label", ""),
                        "placeholder": node.get("placeholder", ""),
                        "name": node.get("name", ""),
                        "autocomplete": node.get("autocomplete", ""),
                        "ref": node.get("ref", "unknown")
                    })
                
                for key, value in node.items():
                    if isinstance(value, list):
                        for item in value:
                            traverse(item)
                    elif isinstance(value, dict):
                        traverse(value)
        
        traverse(self.tree)
        return forms
    
    def _extract_landmarks(self) -> List[Dict]:
        """Landmark elementlerini çıkar"""
        landmarks = []
        
        landmark_roles = ["banner", "main", "navigation", "contentinfo", 
                         "complementary", "region", "search", "form"]
        
        def traverse(node):
            if isinstance(node, dict):
                role = node.get("role", "")
                tag = node.get("tag", "").lower()
                
                # HTML5 semantic elements
                if tag in ["header", "main", "nav", "footer", "aside", "section", "article"]:
                    landmarks.append({
                        "type": tag,
                        "ref": node.get("ref", "unknown")
                    })
                # ARIA roles
                elif role in landmark_roles:
                    landmarks.append({
                        "type": role,
                        "ref": node.get("ref", "unknown")
                    })
                
                for key, value in node.items():
                    if isinstance(value, list):
                        for item in value:
                            traverse(item)
                    elif isinstance(value, dict):
                        traverse(value)
        
        traverse(self.tree)
        return landmarks


def generate_keyboard_voiceover_report(accessibility_tree: dict, page_name: str) -> dict:
    """Kapsamlı klavye ve VoiceOver raporu oluştur"""
    
    # Test sınıflarını başlat
    keyboard_tester = KeyboardA11yTester(accessibility_tree)
    vo_simulator = VoiceOverSimulator(accessibility_tree)
    
    # Testleri çalıştır
    report = {
        "page": page_name,
        "timestamp": datetime.now().isoformat(),
        "keyboard": {
            "focus_order": keyboard_tester.analyze_focus_order(),
            "focus_visible": keyboard_tester.analyze_focus_visible(),
            "keyboard_traps": keyboard_tester.analyze_keyboard_traps()
        },
        "voiceover": {
            "headings": vo_simulator.simulate_heading_navigation(),
            "links": vo_simulator.simulate_link_navigation(),
            "buttons": vo_simulator.simulate_button_navigation(),
            "forms": vo_simulator.simulate_form_navigation(),
            "landmarks": vo_simulator.simulate_landmark_navigation()
        }
    }
    
    # Skor hesapla
    report["score"] = calculate_a11y_score(report)
    
    return report


def calculate_a11y_score(report: dict) -> int:
    """Erişilebilirlik skoru hesapla"""
    score = 100
    
    # Klavye bulguları
    keyboard = report.get("keyboard", {})
    
    # Focus order sorunları
    for issue in keyboard.get("focus_order", []):
        if issue.get("severity") == "medium":
            score -= 5
    
    # Focus visible
    for issue in keyboard.get("focus_visible", []):
        if issue.get("severity") == "critical":
            score -= 15
    
    # Keyboard traps
    for trap in keyboard.get("keyboard_traps", []):
        if trap.get("severity") == "critical":
            score -= 20
    
    # VoiceOver bulguları
    vo = report.get("voiceover", {})
    
    # Başlık sorunları
    headings = vo.get("headings", {})
    if headings.get("h1_count") == 0:
        score -= 15
    elif headings.get("h1_count") > 1:
        score -= 5
    score -= len(headings.get("empty_headings", [])) * 5
    score -= len(headings.get("hierarchy_issues", [])) * 3
    
    # Link sorunları
    links = vo.get("links", {})
    score -= len(links.get("empty_links", [])) * 10
    score -= len(links.get("vague_links", [])) * 3
    score -= len(links.get("url_as_text", [])) * 2
    
    # Buton sorunları
    buttons = vo.get("buttons", {})
    score -= len(buttons.get("empty_buttons", [])) * 10
    score -= len(buttons.get("icon_only_buttons", [])) * 5
    
    # Form sorunları
    forms = vo.get("forms", {})
    score -= len(forms.get("unlabeled_inputs", [])) * 10
    
    # Landmark sorunları
    landmarks = vo.get("landmarks", {})
    score -= len(landmarks.get("missing_landmarks", [])) * 5
    
    return max(0, min(100, score))


if __name__ == "__main__":
    # Test için örnek accessibility tree
    sample_tree = {
        "role": "document",
        "children": [
            {"role": "heading", "aria-level": 1, "text": "Ana Başlık"},
            {"role": "heading", "aria-level": 2, "text": "Bölüm 1"},
            {"role": "link", "text": "Tıklayın", "href": "#"},
            {"role": "button", "text": "", "aria-label": "Ara"},
            {"role": "textbox", "type": "text", "aria-label": "E-posta"}
        ]
    }
    
    report = generate_keyboard_voiceover_report(sample_tree, "Test Sayfası")
    print(json.dumps(report, indent=2, ensure_ascii=False))