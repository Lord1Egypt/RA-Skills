#!/usr/bin/env python3
"""
AccessMind VoiceOver Gerçek Dolaşım ve Chrome Yönetim Sistemi
WCAG 2.2 Uyumlu Kapsamlı Erişilebilirlik Analizi
"""

import json
import subprocess
import time
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class ChromeManager:
    """Chrome tarayıcı yönetim sınıfı"""
    
    def __init__(self):
        self.browser_process = None
        
    async def close_all_browsers(self):
        """Tüm Chrome süreçlerini kapat"""
        # MacOS
        subprocess.run(["pkill", "-9", "Google Chrome"], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # Chrome Driver
        subprocess.run(["pkill", "-9", "chromedriver"], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2)  # Kapanmasını bekle
    
    async def clear_browser_data(self):
        """Browser verilerini temizle"""
        # Cache, cookies, localStorage temizle
        subprocess.run(["rm", "-rf", 
                       os.path.expanduser("~/Library/Caches/Google/Chrome")],
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
    async def prepare_for_audit(self, url: str) -> Dict:
        """Tarama öncesi hazırlık"""
        await self.close_all_browsers()
        await self.clear_browser_data()
        
        return {
            "status": "ready",
            "url": url,
            "timestamp": datetime.now().isoformat()
        }


class VoiceOverNavigator:
    """VoiceOver gerçek dolaşım simülatörü"""
    
    def __init__(self):
        self.current_element = None
        self.navigation_history = []
        
    def simulate_heading_navigation(self, tree: Dict) -> Dict:
        """H tuşu ile başlık navigasyonu simülasyonu"""
        headings = self._extract_headings(tree)
        
        results = {
            "total": len(headings),
            "h1_count": 0,
            "h2_count": 0,
            "h3_count": 0,
            "h4_count": 0,
            "h5_count": 0,
            "h6_count": 0,
            "hierarchy": [],
            "issues": [],
            "voiceover_announcements": []
        }
        
        prev_level = 0
        for h in headings:
            level = h.get("level", h.get("aria-level", 2))
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
            
            # Hiyerarşi kontrolü
            if level > prev_level + 1 and prev_level > 0:
                results["issues"].append({
                    "type": "hierarchy_skip",
                    "severity": "medium",
                    "wcag": "1.3.1 Info and Relationships",
                    "description": f"H{prev_level}'den H{level}'e atlama (H{prev_level + 1} eksik)",
                    "from_heading": f"H{prev_level}",
                    "to_heading": f"H{level}",
                    "text": text[:50]
                })
            
            # Boş başlık kontrolü
            if not text:
                results["issues"].append({
                    "type": "empty_heading",
                    "severity": "high",
                    "wcag": "2.4.6 Headings and Labels",
                    "description": f"H{level} başlığı boş"
                })
            
            # VoiceOver duyurusu
            vo_text = f"Başlık seviyesi {level}, {text}" if text else f"Başlık seviyesi {level}"
            results["voiceover_announcements"].append({
                "level": level,
                "text": text,
                "voiceover": vo_text,
                "status": "OK" if text else "EMPTY"
            })
            
            results["hierarchy"].append({
                "level": level,
                "text": text,
                "ref": h.get("ref", "")
            })
            
            prev_level = level
        
        # H1 kontrolü
        if results["h1_count"] == 0:
            results["issues"].insert(0, {
                "type": "missing_h1",
                "severity": "critical",
                "wcag": "1.3.1 Info and Relationships",
                "description": "Sayfada H1 başlığı yok"
            })
        elif results["h1_count"] > 1:
            results["issues"].insert(0, {
                "type": "multiple_h1",
                "severity": "medium",
                "wcag": "1.3.1 Info and Relationships",
                "description": f"Sayfada {results['h1_count']} adet H1 var (1 olmalı)"
            })
        
        return results
    
    def simulate_link_navigation(self, tree: Dict) -> Dict:
        """U tuşu ile link navigasyonu simülasyonu"""
        links = self._extract_links(tree)
        
        results = {
            "total": len(links),
            "valid": [],
            "empty": [],
            "vague": [],
            "url_as_text": [],
            "voiceover_announcements": []
        }
        
        vague_words = ["tıkla", "tıklayın", "buraya", "buradan", "devam", "devamı",
                      "daha fazla", "link", "click", "here", "more", "read more",
                      "incele", "detay", "git", "seç"]
        
        for link in links:
            text = link.get("text", "").strip()
            aria_label = link.get("aria-label", "").strip()
            href = link.get("href", "")
            
            link_text = text or aria_label
            
            # Boş link kontrolü
            if not link_text:
                results["empty"].append({
                    "ref": link.get("ref", ""),
                    "href": href,
                    "issue": "Link metni ve aria-label boş",
                    "wcag": "2.4.4 Link Purpose"
                })
                results["voiceover_announcements"].append({
                    "text": "(boş)",
                    "voiceover": "link",
                    "status": "EMPTY"
                })
                continue
            
            # Belirsiz link kontrolü
            text_lower = link_text.lower()
            is_vague = any(word in text_lower for word in vague_words)
            
            if is_vague and len(link_text) < 30:
                results["vague"].append({
                    "ref": link.get("ref", ""),
                    "text": link_text,
                    "href": href,
                    "issue": f"Belirsiz link metni: '{link_text}'",
                    "wcag": "2.4.4 Link Purpose"
                })
                results["voiceover_announcements"].append({
                    "text": link_text,
                    "voiceover": f"{link_text}, link",
                    "status": "VAGUE"
                })
                continue
            
            # URL as text kontrolü
            if link_text.startswith("http") or link_text.startswith("www."):
                results["url_as_text"].append({
                    "ref": link.get("ref", ""),
                    "text": link_text,
                    "issue": "URL link metni olarak kullanılıyor",
                    "wcag": "2.4.4 Link Purpose"
                })
                results["voiceover_announcements"].append({
                    "text": link_text,
                    "voiceover": f"{link_text}, link",
                    "status": "URL"
                })
                continue
            
            # Geçerli link
            results["valid"].append(link)
            results["voiceover_announcements"].append({
                "text": link_text,
                "voiceover": f"{link_text}, link",
                "status": "OK"
            })
        
        return results
    
    def simulate_button_navigation(self, tree: Dict) -> Dict:
        """B tuşu ile buton navigasyonu simülasyonu"""
        buttons = self._extract_buttons(tree)
        
        results = {
            "total": len(buttons),
            "valid": [],
            "empty": [],
            "icon_only": [],
            "disabled": [],
            "voiceover_announcements": []
        }
        
        for btn in buttons:
            text = btn.get("text", "").strip()
            aria_label = btn.get("aria-label", "").strip()
            disabled = btn.get("disabled", False)
            
            btn_text = text or aria_label
            
            # Boş buton kontrolü
            if not btn_text:
                results["empty"].append({
                    "ref": btn.get("ref", ""),
                    "issue": "Buton metni ve aria-label boş",
                    "wcag": "4.1.2 Name Role Value"
                })
                results["voiceover_announcements"].append({
                    "text": "(boş)",
                    "voiceover": "button",
                    "status": "EMPTY"
                })
                continue
            
            # Sadece ikon kontrolü
            if len(btn_text) <= 2 and not btn_text.isalpha():
                results["icon_only"].append({
                    "ref": btn.get("ref", ""),
                    "text": btn_text,
                    "issue": "Sadece ikon buton, aria-label ekleyin",
                    "wcag": "4.1.2 Name Role Value"
                })
                results["voiceover_announcements"].append({
                    "text": btn_text,
                    "voiceover": f"{btn_text}, button",
                    "status": "ICON"
                })
                continue
            
            # Disabled kontrolü
            if disabled:
                results["disabled"].append(btn)
                results["voiceover_announcements"].append({
                    "text": btn_text,
                    "voiceover": f"{btn_text}, dimmed button",
                    "status": "DISABLED"
                })
                continue
            
            # Geçerli buton
            results["valid"].append(btn)
            results["voiceover_announcements"].append({
                "text": btn_text,
                "voiceover": f"{btn_text}, button",
                "status": "OK"
            })
        
        return results
    
    def simulate_form_navigation(self, tree: Dict) -> Dict:
        """F tuşu ile form navigasyonu simülasyonu"""
        forms = self._extract_forms(tree)
        
        results = {
            "total": len(forms),
            "valid": [],
            "unlabeled": [],
            "missing_autocomplete": [],
            "voiceover_announcements": []
        }
        
        autocomplete_sensitive = ["email", "password", "tel", "name", 
                                   "given-name", "family-name", "street-address",
                                   "postal-code", "bday"]
        
        for form in forms:
            form_type = form.get("type", "text")
            label = form.get("label", "").strip()
            aria_label = form.get("aria-label", "").strip()
            placeholder = form.get("placeholder", "").strip()
            autocomplete = form.get("autocomplete", "")
            name = form.get("name", "")
            
            # Label kontrolü
            if not label and not aria_label:
                # Placeholder'ı label sanıyor olabilir
                if placeholder:
                    results["unlabeled"].append({
                        "ref": form.get("ref", ""),
                        "type": form_type,
                        "placeholder": placeholder,
                        "issue": f"Placeholder label olarak kullanılıyor: '{placeholder}'",
                        "wcag": "1.3.1 Info and Relationships"
                    })
                    results["voiceover_announcements"].append({
                        "text": placeholder,
                        "voiceover": f"{placeholder}, {form_type} alanı",
                        "status": "PLACEHOLDER"
                    })
                else:
                    results["unlabeled"].append({
                        "ref": form.get("ref", ""),
                        "type": form_type,
                        "issue": "Form alanının label'ı yok",
                        "wcag": "1.3.1 Info and Relationships"
                    })
                    results["voiceover_announcements"].append({
                        "text": "(boş)",
                        "voiceover": f"{form_type} alanı",
                        "status": "UNLABELED"
                    })
                continue
            
            # Autocomplete kontrolü
            if form_type in autocomplete_sensitive or name in autocomplete_sensitive:
                if not autocomplete:
                    results["missing_autocomplete"].append(form)
            
            # Geçerli form
            results["valid"].append(form)
            results["voiceover_announcements"].append({
                "text": label or aria_label,
                "voiceover": f"{label or aria_label}, {form_type} alanı",
                "status": "OK"
            })
        
        return results
    
    def simulate_landmark_navigation(self, tree: Dict) -> Dict:
        """D tuşu ile landmark navigasyonu simülasyonu"""
        landmarks = self._extract_landmarks(tree)
        
        results = {
            "total": len(landmarks),
            "found": [],
            "missing": [],
            "voiceover_announcements": []
        }
        
        expected_landmarks = ["banner", "main", "navigation", "contentinfo"]
        found_types = []
        
        for lm in landmarks:
            lm_type = lm.get("type", lm.get("role", ""))
            found_types.append(lm_type)
            
            results["found"].append(lm)
            results["voiceover_announcements"].append({
                "type": lm_type,
                "voiceover": f"{lm_type}, landmark",
                "status": "OK"
            })
        
        # Eksik landmark'lar
        for expected in expected_landmarks:
            if expected not in found_types:
                results["missing"].append({
                    "type": expected,
                    "issue": f"{expected} landmark bulunamadı",
                    "wcag": "1.3.1 Info and Relationships"
                })
                results["voiceover_announcements"].append({
                    "type": expected,
                    "voiceover": f"{expected} landmark yok",
                    "status": "MISSING"
                })
        
        return results
    
    def _extract_headings(self, tree: Dict) -> List[Dict]:
        """Başlık elementlerini çıkar"""
        headings = []
        
        def traverse(node):
            if isinstance(node, dict):
                if node.get("role") == "heading":
                    level = node.get("level", node.get("aria-level", 2))
                    text = node.get("text", "")
                    headings.append({
                        "level": int(level) if str(level).isdigit() else 2,
                        "text": text,
                        "ref": node.get("ref", "")
                    })
                
                for key, value in node.items():
                    if isinstance(value, list):
                        for item in value:
                            traverse(item)
                    elif isinstance(value, dict):
                        traverse(value)
        
        traverse(tree)
        return headings
    
    def _extract_links(self, tree: Dict) -> List[Dict]:
        """Link elementlerini çıkar"""
        links = []
        
        def traverse(node):
            if isinstance(node, dict):
                if node.get("role") == "link" or "link" in str(node.get("ref", "")).lower():
                    links.append({
                        "text": node.get("text", ""),
                        "aria-label": node.get("aria-label", ""),
                        "href": node.get("href", node.get("/url", "")),
                        "ref": node.get("ref", "")
                    })
                
                for key, value in node.items():
                    if isinstance(value, list):
                        for item in value:
                            traverse(item)
                    elif isinstance(value, dict):
                        traverse(value)
        
        traverse(tree)
        return links
    
    def _extract_buttons(self, tree: Dict) -> List[Dict]:
        """Buton elementlerini çıkar"""
        buttons = []
        
        def traverse(node):
            if isinstance(node, dict):
                if node.get("role") == "button":
                    buttons.append({
                        "text": node.get("text", ""),
                        "aria-label": node.get("aria-label", ""),
                        "disabled": node.get("disabled", False),
                        "ref": node.get("ref", "")
                    })
                
                for key, value in node.items():
                    if isinstance(value, list):
                        for item in value:
                            traverse(item)
                    elif isinstance(value, dict):
                        traverse(value)
        
        traverse(tree)
        return buttons
    
    def _extract_forms(self, tree: Dict) -> List[Dict]:
        """Form elementlerini çıkar"""
        forms = []
        
        def traverse(node):
            if isinstance(node, dict):
                form_type = node.get("type", "")
                if form_type in ["text", "email", "password", "tel", "search", 
                                  "url", "number", "date"] or \
                   node.get("role") in ["textbox", "combobox", "listbox", 
                                        "checkbox", "radio", "slider"]:
                    forms.append({
                        "type": form_type or node.get("role", "text"),
                        "label": node.get("label", ""),
                        "aria-label": node.get("aria-label", ""),
                        "placeholder": node.get("placeholder", ""),
                        "name": node.get("name", ""),
                        "autocomplete": node.get("autocomplete", ""),
                        "ref": node.get("ref", "")
                    })
                
                for key, value in node.items():
                    if isinstance(value, list):
                        for item in value:
                            traverse(item)
                    elif isinstance(value, dict):
                        traverse(value)
        
        traverse(tree)
        return forms
    
    def _extract_landmarks(self, tree: Dict) -> List[Dict]:
        """Landmark elementlerini çıkar"""
        landmarks = []
        landmark_roles = ["banner", "main", "navigation", "contentinfo",
                         "complementary", "region", "search", "form"]
        
        def traverse(node):
            if isinstance(node, dict):
                role = node.get("role", "")
                tag = node.get("tag", "").lower() if node.get("tag") else ""
                
                # HTML5 semantic elements
                if tag in ["header", "main", "nav", "footer", "aside", "section", "article"]:
                    landmarks.append({
                        "type": tag,
                        "ref": node.get("ref", "")
                    })
                # ARIA roles
                elif role in landmark_roles:
                    landmarks.append({
                        "type": role,
                        "ref": node.get("ref", "")
                    })
                
                for key, value in node.items():
                    if isinstance(value, list):
                        for item in value:
                            traverse(item)
                    elif isinstance(value, dict):
                        traverse(value)
        
        traverse(tree)
        return landmarks


class InteractionAnalyzer:
    """Element etkileşim ve anlamsal ilişki analiz sınıfı"""
    
    def __init__(self, tree: Dict):
        self.tree = tree
        
    def analyze_label_control_relations(self) -> Dict:
        """Label-control ilişkisi analizi"""
        return VoiceOverNavigator()._extract_forms(self.tree)
    
    def analyze_heading_hierarchy(self) -> Dict:
        """Başlık hiyerarşisi analizi"""
        return VoiceOverNavigator().simulate_heading_navigation(self.tree)
    
    def analyze_landmark_content(self) -> Dict:
        """Landmark-content ilişkisi analizi"""
        return VoiceOverNavigator().simulate_landmark_navigation(self.tree)
    
    def analyze_state_changes(self) -> Dict:
        """Durum değişikliği analizi"""
        findings = {
            "toggles": [],      # aria-pressed
            "expands": [],       # aria-expanded
            "invalids": [],      # aria-invalid
            "loadings": []       # aria-busy
        }
        
        def traverse(node):
            if isinstance(node, dict):
                # aria-pressed
                if "aria-pressed" in str(node):
                    findings["toggles"].append({
                        "ref": node.get("ref", ""),
                        "pressed": node.get("aria-pressed", "")
                    })
                
                # aria-expanded
                if "aria-expanded" in str(node):
                    findings["expands"].append({
                        "ref": node.get("ref", ""),
                        "expanded": node.get("aria-expanded", ""),
                        "controls": node.get("aria-controls", "")
                    })
                
                # aria-invalid
                if "aria-invalid" in str(node):
                    findings["invalids"].append({
                        "ref": node.get("ref", ""),
                        "invalid": node.get("aria-invalid", "")
                    })
                
                # aria-busy
                if "aria-busy" in str(node):
                    findings["loadings"].append({
                        "ref": node.get("ref", ""),
                        "busy": node.get("aria-busy", "")
                    })
                
                for key, value in node.items():
                    if isinstance(value, list):
                        for item in value:
                            traverse(item)
                    elif isinstance(value, dict):
                        traverse(value)
        
        traverse(self.tree)
        return findings
    
    def calculate_relation_score(self, results: Dict) -> int:
        """Anlamsal ilişki skoru hesapla"""
        score = 100
        
        # Form label eksikliği
        if "unlabeled" in results:
            score -= len(results["unlabeled"]) * 10
        
        # Başlık hiyerarşi sorunları
        if "issues" in results.get("headings", {}):
            score -= len(results["headings"]["issues"]) * 5
        
        # Landmark eksikliği
        if "missing" in results.get("landmarks", {}):
            score -= len(results["landmarks"]["missing"]) * 5
        
        # State change bonus
        if results.get("state_changes", {}).get("toggles") or \
           results.get("state_changes", {}).get("expands"):
            score += 5
        
        return max(0, min(100, score))


def generate_full_report(tree: Dict, page_name: str, page_url: str) -> Dict:
    """Kapsamlı erişilebilirlik raporu oluştur"""
    
    # VoiceOver navigasyonu
    vo = VoiceOverNavigator()
    
    headings = vo.simulate_heading_navigation(tree)
    links = vo.simulate_link_navigation(tree)
    buttons = vo.simulate_button_navigation(tree)
    forms = vo.simulate_form_navigation(tree)
    landmarks = vo.simulate_landmark_navigation(tree)
    
    # Etkileşim analizi
    interaction = InteractionAnalyzer(tree)
    state_changes = interaction.analyze_state_changes()
    
    # Skorlar
    heading_score = 100 - len(headings["issues"]) * 5
    link_score = 100 - len(links["empty"]) * 10 - len(links["vague"]) * 3
    button_score = 100 - len(buttons["empty"]) * 10 - len(buttons["icon_only"]) * 5
    form_score = 100 - len(forms["unlabeled"]) * 10
    landmark_score = 100 - len(landmarks["missing"]) * 5
    
    # Genel skor
    total_score = (heading_score + link_score + button_score + form_score + landmark_score) / 5
    
    return {
        "page": page_name,
        "url": page_url,
        "timestamp": datetime.now().isoformat(),
        "scores": {
            "total": round(total_score, 1),
            "headings": heading_score,
            "links": link_score,
            "buttons": button_score,
            "forms": form_score,
            "landmarks": landmark_score
        },
        "voiceover": {
            "headings": headings,
            "links": links,
            "buttons": buttons,
            "forms": forms,
            "landmarks": landmarks
        },
        "interaction": {
            "state_changes": state_changes
        }
    }


if __name__ == "__main__":
    # Test
    test_tree = {
        "role": "document",
        "children": [
            {"role": "heading", "level": 1, "text": "Ana Başlık"},
            {"role": "link", "text": "Tıklayın", "href": "#"},
            {"role": "button", "text": "", "aria-label": "Ara"},
            {"role": "textbox", "type": "text", "aria-label": "E-posta"}
        ]
    }
    
    report = generate_full_report(test_tree, "Test Sayfası", "https://example.com")
    print(json.dumps(report, indent=2, ensure_ascii=False))