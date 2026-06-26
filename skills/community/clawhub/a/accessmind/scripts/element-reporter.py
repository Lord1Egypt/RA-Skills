#!/usr/bin/env python3
"""
AccessMind Element Bazlı Rapor Oluşturucu
Her element için detaylı paragraf açıklamalı rapor
"""

import json
from datetime import datetime
from typing import Dict, List, Optional


class ElementReporter:
    """Element bazlı detaylı rapor oluşturucu"""
    
    def __init__(self):
        self.elements = []
        
    def report_heading(self, element: Dict) -> Dict:
        """Başlık elementi raporu"""
        
        level = element.get("level", element.get("aria-level", 2))
        text = element.get("text", "").strip()
        ref = element.get("ref", "")
        
        # VoiceOver duyurusu
        vo_announcement = f"Başlık seviyesi {level}, {text}" if text else f"Başlık seviyesi {level}"
        
        # Durum belirleme
        if not text:
            status = "❌ İHLAL"
            score = 0
        elif level == 1:
            status = "✅ UYUMLU"
            score = 100
        elif level in [2, 3, 4]:
            status = "✅ UYUMLU"
            score = 95
        else:
            status = "✅ UYUMLU"
            score = 90
        
        # WCAG kriterleri
        wcag_criteria = [
            {
                "criterion": "1.3.1",
                "name": "Info and Relationships",
                "level": "A",
                "status": "✅" if text else "❌",
                "description": f"H{level} başlığı {'açıklayıcı' if text else 'boş'}"
            },
            {
                "criterion": "2.4.6",
                "name": "Headings and Labels",
                "level": "AA",
                "status": "✅" if text else "❌",
                "description": f"Başlık {'anlamlı' if text else 'içeriksiz'}"
            }
        ]
        
        return {
            "type": "heading",
            "element_type": "HEADING",
            "name": text[:50] if text else "(boş)",
            "basic_info": {
                "element_type": "heading",
                "level": f"H{level}",
                "location": ref,
                "content": text,
                "voiceover_announcement": vo_announcement
            },
            "accessibility_status": {
                "status": status,
                "score": score
            },
            "wcag_criteria": wcag_criteria,
            "related_elements": {
                "parent": "Ana içerik alanı",
                "children": "Yok (metin içeriği)",
                "previous_heading": "Önceki başlık bilgisi gerekli",
                "next_heading": "Sonraki başlık bilgisi gerekli"
            },
            "issues": [] if text else [{
                "issue": "Başlık metni boş",
                "wcag": "1.3.1 Info and Relationships",
                "description": "Screen Reader kullanıcıları boş başlık duyduğunda kafaları karışır.",
                "recommendation": "Başlığa açıklayıcı metin ekleyin",
                "code": f"<h{level}>[Açıklayıcı Başlık]</h{level}>"
            }],
            "voiceover_test": {
                "key": "H",
                "announcement": vo_announcement,
                "expected": f"Başlık seviyesi {level}, [içerik]" if text else f"Başlık seviyesi {level}",
                "status": "✅ Doğru" if text else "❌ Hatalı"
            },
            "paragraph": self._generate_paragraph("heading", element)
        }
    
    def report_link(self, element: Dict) -> Dict:
        """Link elementi raporu"""
        
        text = element.get("text", "").strip()
        aria_label = element.get("aria-label", "").strip()
        href = element.get("href", element.get("/url", ""))
        ref = element.get("ref", "")
        
        link_text = text or aria_label
        
        # VoiceOver duyurusu
        vo_announcement = f"{link_text}, link" if link_text else "link"
        
        # Belirsiz kelimeler
        vague_words = ["tıkla", "tıklayın", "buraya", "buradan", "devam", "devamı",
                      "daha fazla", "link", "click", "here", "more", "incele", "detay", "git"]
        
        # Durum belirleme
        if not link_text:
            status = "❌ İHLAL"
            score = 0
        elif any(word in link_text.lower() for word in vague_words) and len(link_text) < 30:
            status = "⚠️ UYARI"
            score = 70
        elif link_text.startswith("http") or link_text.startswith("www."):
            status = "⚠️ UYARI"
            score = 60
        else:
            status = "✅ UYUMLU"
            score = 100
        
        # WCAG kriterleri
        wcag_criteria = [
            {
                "criterion": "2.4.4",
                "name": "Link Purpose",
                "level": "A",
                "status": "✅" if status == "✅ UYUMLU" else "⚠️",
                "description": f"Link amacı {'belirlenebilir' if status == '✅ UYUMLU' else 'belirsiz'}"
            },
            {
                "criterion": "4.1.2",
                "name": "Name, Role, Value",
                "level": "A",
                "status": "✅",
                "description": "Role ve name doğru"
            }
        ]
        
        # Sorunlar
        issues = []
        if not link_text:
            issues.append({
                "issue": "Link metni ve aria-label boş",
                "wcag": "2.4.4 Link Purpose",
                "description": "Screen Reader kullanıcıları linkin ne işe yaradığını anlayamaz.",
                "recommendation": "Link metni ekleyin veya aria-label kullanın",
                "code": '<a href="..." aria-label="Açıklayıcı metin">Link</a>'
            })
        elif any(word in link_text.lower() for word in vague_words) and len(link_text) < 30:
            issues.append({
                "issue": f"Belirsiz link metni: '{link_text}'",
                "wcag": "2.4.4 Link Purpose",
                "description": f"VoiceOver kullanıcısı '{link_text}' duyduğunda linkin amacını tam olarak anlayamayabilir.",
                "recommendation": "Link metnini daha açıklayıcı yapın",
                "code": f'<!-- Mevcut -->\n<a href="...">{link_text}</a>\n\n<!-- Önerilen -->\n<a href="...">Ürünü İncele</a>'
            })
        
        return {
            "type": "link",
            "element_type": "LINK",
            "name": link_text[:50] if link_text else "(boş)",
            "basic_info": {
                "element_type": "link",
                "role": "link",
                "location": ref,
                "content": link_text,
                "href": href,
                "aria_label": aria_label,
                "voiceover_announcement": vo_announcement
            },
            "accessibility_status": {
                "status": status,
                "score": score
            },
            "wcag_criteria": wcag_criteria,
            "related_elements": {
                "parent": "Ana içerik alanı",
                "children": "Yok",
                "target": href[:50] if href else "Yok"
            },
            "issues": issues,
            "voiceover_test": {
                "key": "U",
                "announcement": vo_announcement,
                "expected": f"[Açıklayıcı metin], link",
                "status": "✅ Doğru" if status == "✅ UYUMLU" else "⚠️ Kısmen" if status == "⚠️ UYARI" else "❌ Hatalı"
            },
            "paragraph": self._generate_paragraph("link", element)
        }
    
    def report_button(self, element: Dict) -> Dict:
        """Buton elementi raporu"""
        
        text = element.get("text", "").strip()
        aria_label = element.get("aria-label", "").strip()
        disabled = element.get("disabled", False)
        ref = element.get("ref", "")
        
        btn_text = text or aria_label
        
        # VoiceOver duyurusu
        if disabled:
            vo_announcement = f"{btn_text}, dimmed button" if btn_text else "dimmed button"
        else:
            vo_announcement = f"{btn_text}, button" if btn_text else "button"
        
        # Durum belirleme
        if not btn_text:
            status = "❌ İHLAL"
            score = 0
        elif len(btn_text) <= 2 and not btn_text.isalpha():
            status = "⚠️ UYARI"
            score = 50
        elif disabled:
            status = "⚠️ BILGI"
            score = 80
        else:
            status = "✅ UYUMLU"
            score = 100
        
        # WCAG kriterleri
        wcag_criteria = [
            {
                "criterion": "4.1.2",
                "name": "Name, Role, Value",
                "level": "A",
                "status": "✅" if btn_text else "❌",
                "description": f"Buton {'isimli' if btn_text else 'isimsiz'}"
            },
            {
                "criterion": "2.1.1",
                "name": "Keyboard",
                "level": "A",
                "status": "✅",
                "description": "Klavye ile erişilebilir"
            }
        ]
        
        # Sorunlar
        issues = []
        if not btn_text:
            issues.append({
                "issue": "Buton metni ve aria-label boş",
                "wcag": "4.1.2 Name, Role, Value",
                "description": "Screen Reader kullanıcıları butonun ne işe yaradığını anlayamaz.",
                "recommendation": "Buton metni ekleyin veya aria-label kullanın",
                "code": '<button aria-label="Ara">\n  <svg>...</svg>\n</button>'
            })
        elif len(btn_text) <= 2 and not btn_text.isalpha():
            issues.append({
                "issue": f"Sadece ikon buton: '{btn_text}'",
                "wcag": "4.1.2 Name, Role, Value",
                "description": "Sembol butonlar için aria-label şart.",
                "recommendation": "aria-label ekleyin",
                "code": f'<button aria-label="{btn_text} butonu">{btn_text}</button>'
            })
        
        return {
            "type": "button",
            "element_type": "BUTTON",
            "name": btn_text[:50] if btn_text else "(boş)",
            "basic_info": {
                "element_type": "button",
                "role": "button",
                "location": ref,
                "content": btn_text,
                "disabled": disabled,
                "voiceover_announcement": vo_announcement
            },
            "accessibility_status": {
                "status": status,
                "score": score
            },
            "wcag_criteria": wcag_criteria,
            "related_elements": {
                "parent": "Ana içerik alanı",
                "children": "Yok",
                "action": "Buton tıklama aksiyonu"
            },
            "issues": issues,
            "voiceover_test": {
                "key": "B",
                "announcement": vo_announcement,
                "expected": f"[Açıklayıcı metin], button",
                "status": "✅ Doğru" if status == "✅ UYUMLU" else "⚠️ İyileştirilebilir"
            },
            "paragraph": self._generate_paragraph("button", element)
        }
    
    def report_form(self, element: Dict) -> Dict:
        """Form elementi raporu"""
        
        form_type = element.get("type", element.get("role", "text"))
        label = element.get("label", "").strip()
        aria_label = element.get("aria-label", "").strip()
        placeholder = element.get("placeholder", "").strip()
        autocomplete = element.get("autocomplete", "")
        ref = element.get("ref", "")
        
        form_label = label or aria_label
        
        # VoiceOver duyurusu
        type_names = {
            "text": "metin alanı",
            "email": "e-posta alanı",
            "password": "güvenli metin alanı",
            "tel": "telefon alanı",
            "search": "arama alanı",
            "combobox": "açılır menü",
            "listbox": "liste kutusu",
            "checkbox": "onay kutusu",
            "radio": "radyo düğmesi"
        }
        
        type_name = type_names.get(form_type, form_type)
        vo_announcement = f"{form_label}, {type_name}" if form_label else f"{type_name}"
        
        # Durum belirleme
        if not form_label and not placeholder:
            status = "❌ İHLAL"
            score = 0
        elif not form_label and placeholder:
            status = "⚠️ UYARI"
            score = 70
        else:
            status = "✅ UYUMLU"
            score = 100
        
        # WCAG kriterleri
        wcag_criteria = [
            {
                "criterion": "1.3.1",
                "name": "Info and Relationships",
                "level": "A",
                "status": "✅" if form_label else "⚠️",
                "description": f"Form alanı {'etiketli' if form_label else 'etiketsiz'}"
            },
            {
                "criterion": "3.3.2",
                "name": "Labels or Instructions",
                "level": "A",
                "status": "✅" if form_label else "⚠️",
                "description": f"Kullanıcıya ne girmesi gerektiği {'açık' if form_label else 'belirsiz'}"
            }
        ]
        
        # Sorunlar
        issues = []
        if not form_label:
            if placeholder:
                issues.append({
                    "issue": f"Placeholder label olarak kullanılıyor: '{placeholder}'",
                    "wcag": "1.3.1 Info and Relationships",
                    "description": "Placeholder geçici metindir, label olarak kullanılmamalıdır.",
                    "recommendation": "label elementi veya aria-label kullanın",
                    "code": f'<!-- Mevcut -->\n<input placeholder="{placeholder}">\n\n<!-- Önerilen -->\n<label for="input-id">{placeholder}</label>\n<input id="input-id" placeholder="{placeholder}">'
                })
            else:
                issues.append({
                    "issue": "Form alanının label'ı yok",
                    "wcag": "1.3.1 Info and Relationships",
                    "description": "Screen Reader kullanıcıları form alanının amacını anlayamaz.",
                    "recommendation": "label ekleyin",
                    "code": '<label for="input-id">Etiket</label>\n<input id="input-id">'
                })
        
        return {
            "type": "form",
            "element_type": "FORM",
            "name": form_label[:50] if form_label else f"({type_name})",
            "basic_info": {
                "element_type": form_type,
                "role": element.get("role", form_type),
                "location": ref,
                "content": form_label or placeholder,
                "placeholder": placeholder,
                "autocomplete": autocomplete,
                "voiceover_announcement": vo_announcement
            },
            "accessibility_status": {
                "status": status,
                "score": score
            },
            "wcag_criteria": wcag_criteria,
            "related_elements": {
                "parent": "Form alanı",
                "label": label if label else "Yok",
                "sibling": "Diğer form alanları"
            },
            "issues": issues,
            "voiceover_test": {
                "key": "F",
                "announcement": vo_announcement,
                "expected": f"[Etiket], {type_name}",
                "status": "✅ Doğru" if status == "✅ UYUMLU" else "⚠️ İyileştirilebilir"
            },
            "paragraph": self._generate_paragraph("form", element)
        }
    
    def report_image(self, element: Dict) -> Dict:
        """Görsel elementi raporu"""
        
        alt = element.get("alt", "").strip()
        src = element.get("src", "").strip()
        role = element.get("role", "")
        aria_hidden = element.get("aria-hidden", "")
        ref = element.get("ref", "")
        
        # VoiceOver duyurusu
        if aria_hidden == "true" or role == "presentation":
            vo_announcement = "(görmezden gelindi)"
        elif alt:
            vo_announcement = f"{alt}, grafik"
        else:
            vo_announcement = "grafik"
        
        # Durum belirleme
        if aria_hidden == "true" or role == "presentation":
            status = "✅ UYUMLU"
            score = 100
        elif not alt:
            status = "❌ İHLAL"
            score = 0
        elif alt.endswith((".jpg", ".png", ".gif", ".webp")) or "_" in alt and len(alt) < 30:
            status = "⚠️ UYARI"
            score = 50
        else:
            status = "✅ UYUMLU"
            score = 100
        
        # WCAG kriterleri
        wcag_criteria = [
            {
                "criterion": "1.1.1",
                "name": "Non-text Content",
                "level": "A",
                "status": "✅" if alt else "❌",
                "description": f"Görsel {'açıklayıcı alt metinli' if alt else 'alt metinsiz'}"
            }
        ]
        
        # Sorunlar
        issues = []
        if not alt and aria_hidden != "true" and role != "presentation":
            issues.append({
                "issue": "Alt metin yok",
                "wcag": "1.1.1 Non-text Content",
                "description": "Screen Reader kullanıcıları görselin ne olduğunu anlayamaz.",
                "recommendation": "Alt metin ekleyin",
                "code": '<img alt="Açıklayıcı metin" src="...">'
            })
        elif alt and (alt.endswith((".jpg", ".png", ".gif")) or (len(alt) < 30 and "_" in alt)):
            issues.append({
                "issue": f"Anlamsız alt metin: '{alt}'",
                "wcag": "1.1.1 Non-text Content",
                "description": "Alt metin dosya adı formatında veya anlamsız.",
                "recommendation": "Görselin içeriğini açıklayan alt metin kullanın",
                "code": f'<!-- Mevcut -->\n<img alt="{alt}" src="...">\n\n<!-- Önerilen -->\n<img alt="[Görselin içeriğini açıklayan metin]" src="...">'
            })
        
        return {
            "type": "image",
            "element_type": "IMAGE",
            "name": alt[:50] if alt else "(alt yok)",
            "basic_info": {
                "element_type": "img",
                "role": role or "img",
                "location": ref,
                "content": alt,
                "src": src[:50] if src else "Yok",
                "aria_hidden": aria_hidden,
                "voiceover_announcement": vo_announcement
            },
            "accessibility_status": {
                "status": status,
                "score": score
            },
            "wcag_criteria": wcag_criteria,
            "related_elements": {
                "parent": "Ana içerik alanı",
                "context": "Görselin kullanım amacı"
            },
            "issues": issues,
            "voiceover_test": {
                "key": "VoiceOver görsel modu",
                "announcement": vo_announcement,
                "expected": "[Açıklayıcı alt metin], grafik",
                "status": "✅ Doğru" if status == "✅ UYUMLU" else "❌ Hatalı"
            },
            "paragraph": self._generate_paragraph("image", element)
        }
    
    def _generate_paragraph(self, element_type: str, element: Dict) -> str:
        """Element için paragraf açıklaması oluştur"""
        
        paragraphs = {
            "heading": self._paragraph_heading(element),
            "link": self._paragraph_link(element),
            "button": self._paragraph_button(element),
            "form": self._paragraph_form(element),
            "image": self._paragraph_image(element)
        }
        
        return paragraphs.get(element_type, "Bu element erişilebilirlik açısından değerlendirilmiştir.")
    
    def _paragraph_heading(self, element: Dict) -> str:
        """Başlık için paragraf"""
        level = element.get("level", element.get("aria-level", 2))
        text = element.get("text", "").strip()
        
        if not text:
            return f"H{level} başlığı boş olarak tanımlanmış. Bu, ekran okuyucu kullanıcıları için kafa karıştırıcı olabilir çünkü başlığın ne hakkında olduğunu bilemezler. Her başlık açıklayıcı bir metin içermelidir."
        
        return f"H{level} başlığı \"{text}\" olarak tanımlanmış. Bu başlık, sayfanın içerik yapısını organize eder ve ekran okuyucu kullanıcılarının H tuşu ile hızlı navigasyon yapmasını sağlar. Başlık seviyesi {level}, içeriğin hiyerarşik önemini gösterir."
    
    def _paragraph_link(self, element: Dict) -> str:
        """Link için paragraf"""
        text = element.get("text", "").strip()
        aria_label = element.get("aria-label", "").strip()
        link_text = text or aria_label
        
        if not link_text:
            return "Bu link herhangi bir metin içermiyor ve aria-label da tanımlanmamış. Ekran okuyucu kullanıcıları bu linki duyduğunda ne işe yaradığını anlayamaz. Link metni ekleyerek veya aria-label kullanarak erişilebilirliği sağlayın."
        
        vague_words = ["tıkla", "tıklayın", "buraya", "devam", "daha fazla", "click", "here", "more"]
        if any(word in link_text.lower() for word in vague_words) and len(link_text) < 30:
            return f"Link metni \"{link_text}\" bağlamdan ayrıldığında belirsiz görünüyor. Ekran okuyucu kullanıcıları link listesinde gezinirken bu linkin amacını tam olarak anlayamayabilir. \"Ürünü İncele\", \"Sepete Git\" gibi açıklayıcı link metinleri kullanın."
        
        return f"Link metni \"{link_text}\" olarak tanımlanmış. Bu metin, linkin amacını açıkça belirtiyor ve ekran okuyucu kullanıcılarının U tuşu ile navigasyon yaparken neyle karşılaşacaklarını anlamalarını sağlıyor."
    
    def _paragraph_button(self, element: Dict) -> str:
        """Buton için paragraf"""
        text = element.get("text", "").strip()
        aria_label = element.get("aria-label", "").strip()
        btn_text = text or aria_label
        
        if not btn_text:
            return "Bu buton herhangi bir metin içermiyor ve aria-label da tanımlanmamış. Ekran okuyucu kullanıcıları B tuşu ile butonlarda gezinirken bu butonun ne işe yaradığını anlayamaz. aria-label ekleyerek veya görünür metin kullanarak erişilebilirliği sağlayın."
        
        if len(btn_text) <= 2 and not btn_text.isalpha():
            return f"Buton metni \"{btn_text}\" sadece bir sembol içeriyor. Bu tür butonlar genellikle ikon butonlarıdır ve aria-label ile açıklanmalıdır. Örnek: aria-label=\"Ara\" veya aria-label=\"Menüyü aç\"."
        
        return f"Buton metni \"{btn_text}\" olarak tanımlanmış. Bu metin, butonun eylemini açıkça belirtiyor ve ekran okuyucu kullanıcılarının ne yapacaklarını anlamalarını sağlıyor."
    
    def _paragraph_form(self, element: Dict) -> str:
        """Form için paragraf"""
        label = element.get("label", "").strip()
        aria_label = element.get("aria-label", "").strip()
        placeholder = element.get("placeholder", "").strip()
        form_type = element.get("type", "text")
        form_label = label or aria_label
        
        if not form_label and not placeholder:
            return f"Bu {form_type} form alanı herhangi bir etiket içermiyor. Ekran okuyucu kullanıcıları F tuşu ile form alanlarında gezinirken bu alanın ne için kullanıldığını anlayamaz. label elementi veya aria-label kullanarak form alanının amacını belirtin."
        
        if not form_label and placeholder:
            return f"Bu form alanı placeholder olarak \"{placeholder}\" kullanıyor. Placeholder geçici metindir ve kullanıcı yazmaya başladığında kaybolur. Form alanının amacını kalıcı olarak belirtmek için label elementi veya aria-label kullanın."
        
        return f"Form alanı etiketi \"{form_label}\" olarak tanımlanmış. Bu etiket, ekran okuyucu kullanıcılarına form alanının amacını açıkça belirtiyor ve doğru veriyi girmelerini sağlıyor."
    
    def _paragraph_image(self, element: Dict) -> str:
        """Görsel için paragraf"""
        alt = element.get("alt", "").strip()
        aria_hidden = element.get("aria-hidden", "")
        role = element.get("role", "")
        
        if aria_hidden == "true" or role == "presentation":
            return "Bu görsel dekoratif olarak işaretlenmiş (aria-hidden='true' veya role='presentation'). Dekoratif görseller screen reader tarafından atlanır ve alt metin gerektirmez."
        
        if not alt:
            return "Bu görsel alt metin içermiyor. Ekran okuyucu kullanıcıları görselin ne olduğunu anlayamaz. Alt metin ekleyerek görselin içeriğini açıklayın. Dekoratif görseller için alt=\"\" kullanın."
        
        if alt.endswith((".jpg", ".png", ".gif", ".webp")) or (len(alt) < 30 and "_" in alt):
            return f"Alt metin \"{alt}\" dosya adı formatında görünüyor. Bu, ekran okuyucu kullanıcıları için yararlı değildir. Alt metni görselin içeriğini açıklayacak şekilde değiştirin. Örnek: \"Ürün görseli - Buzdolabı 283616 EI\"."
        
        return f"Görselin alt metini \"{alt}\" olarak tanımlanmış. Bu metin, ekran okuyucu kullanıcılarına görselin içeriğini açıkça anlatıyor."


class CodeGenerator:
    """Erişilebilir kod çıktı ve iyileştirme oluşturucu"""
    
    def __init__(self):
        self.indent = "  "
    
    def generate_html(self, element: Dict, original: bool = True) -> str:
        """HTML kod çıktısı oluştur"""
        
        element_type = element.get("type", element.get("role", "div"))
        
        if element_type == "heading":
            return self._generate_heading_html(element, original)
        elif element_type == "link":
            return self._generate_link_html(element, original)
        elif element_type == "button":
            return self._generate_button_html(element, original)
        elif element_type in ["textbox", "combobox", "listbox", "checkbox", "radio"]:
            return self._generate_form_html(element, original)
        elif element_type == "img" or element_type == "image":
            return self._generate_image_html(element, original)
        else:
            return self._generate_generic_html(element, original)
    
    def _generate_heading_html(self, element: Dict, original: bool) -> str:
        """Başlık HTML kodu"""
        level = element.get("level", element.get("aria-level", 2))
        text = element.get("text", "")
        ref = element.get("ref", "")
        
        if original:
            # Mevcut (boş başlık varsa)
            if not text:
                return f"""<!-- MEVCUT KOD (İHLAL) -->
<h{level} ref="{ref}"></h{level}>

<!-- SORUN: Başlık metni boş -->
<!-- WCAG: 1.3.1 Info and Relationships -->
<!-- AÇIKLAMA: Ekran okuyucu kullanıcıları boş başlık duyduğunda ne hakkında olduğunu anlayamaz -->
"""
            else:
                return f"""<!-- MEVCUT KOD (UYUMLU) -->
<h{level} ref="{ref}">{text}</h{level}>

<!-- DURUM: ✅ UYUMLU -->
<!-- AÇIKLAMA: Başlık açıklayıcı metin içeriyor -->
"""
        else:
            # İyileştirilmiş
            return f"""<!-- İYİLEŞTİRİLMİŞ KOD -->
<h{level} id="main-heading">{text}</h{level}>

<!-- İYİLEŞTİRMELER:
  1. id eklendi (anchor için)
  2. Anlamsal HTML5 kullanımı
  3. ARIA gereksiz (doğal heading yeterli)
-->"""
    
    def _generate_link_html(self, element: Dict, original: bool) -> str:
        """Link HTML kodu"""
        text = element.get("text", "")
        aria_label = element.get("aria-label", "")
        href = element.get("href", "#")
        ref = element.get("ref", "")
        link_text = text or aria_label
        
        if original:
            # Mevcut
            if not link_text:
                return f"""<!-- MEVCUT KOD (İHLAL) -->
<a href="{href}" ref="{ref}"></a>

<!-- SORUN: Link metni ve aria-label boş -->
<!-- WCAG: 2.4.4 Link Purpose -->
<!-- AÇIKLAMA: Ekran okuyucu kullanıcıları linkin ne işe yaradığını anlayamaz -->
"""
            elif any(word in link_text.lower() for word in ["tıkla", "tıklayın", "buraya", "devam", "click", "here"]) and len(link_text) < 30:
                return f"""<!-- MEVCUT KOD (UYARI) -->
<a href="{href}" ref="{ref}">{link_text}</a>

<!-- SORUN: Belirsiz link metni: '{link_text}' -->
<!-- WCAG: 2.4.4 Link Purpose -->
<!-- AÇIKLAMA: Link amacı bağlamdan ayrıldığında belirsiz -->
"""
            else:
                return f"""<!-- MEVCUT KOD (UYUMLU) -->
<a href="{href}" ref="{ref}">{link_text}</a>

<!-- DURUM: ✅ UYUMLU -->
<!-- AÇIKLAMA: Link metni açıklayıcı -->
"""
        else:
            # İyileştirilmiş
            improved_text = link_text if link_text and link_text not in ["tıkla", "tıklayın", "buraya", "click", "here"] else "Ürünü İncele"
            return f"""<!-- İYİLEŞTİRİLMİŞ KOD -->
<a href="{href}" 
   ref="{ref}"
   aria-label="{improved_text}"
   class="link-interactive">
  {improved_text}
</a>

<!-- İYİLEŞTİRMELER:
  1. Açıklayıcı link metni: '{improved_text}'
  2. aria-label eklendi (context için)
  3. Etkileşim sınıfı (CSS için)
-->"""
    
    def _generate_button_html(self, element: Dict, original: bool) -> str:
        """Buton HTML kodu"""
        text = element.get("text", "")
        aria_label = element.get("aria-label", "")
        disabled = element.get("disabled", False)
        ref = element.get("ref", "")
        btn_text = text or aria_label
        
        if original:
            # Mevcut
            disabled_attr = " disabled" if disabled else ""
            
            if not btn_text:
                return f"""<!-- MEVCUT KOD (İHLAL) -->
<button ref="{ref}"{disabled_attr}></button>

<!-- SORUN: Buton metni ve aria-label boş -->
<!-- WCAG: 4.1.2 Name, Role, Value -->
<!-- AÇIKLAMA: Ekran okuyucu kullanıcıları butonun ne işe yaradığını anlayamaz -->
"""
            elif len(btn_text) <= 2 and not btn_text.isalpha():
                return f"""<!-- MEVCUT KOD (UYARI) -->
<button ref="{ref}"{disabled_attr}>{btn_text}</button>

<!-- SORUN: Sadece ikon buton: '{btn_text}' -->
<!-- WCAG: 4.1.2 Name, Role, Value -->
<!-- AÇIKLAMA: İkon butonlar aria-label gerektirir -->
"""
            elif "Seç Seç" in btn_text or "Evet Evet" in btn_text:
                return f"""<!-- MEVCUT KOD (UYARI) -->
<button ref="{ref}"{disabled_attr}>{btn_text}</button>

<!-- SORUN: Tekrarlayan buton metni: '{btn_text}' -->
<!-- WCAG: 4.1.2 Name, Role, Value -->
<!-- AÇIKLAMA: VoiceOver kullanıcıları aynı kelimeyi iki kez duyar -->
"""
            else:
                return f"""<!-- MEVCUT KOD (UYUMLU) -->
<button ref="{ref}"{disabled_attr}>{btn_text}</button>

<!-- DURUM: ✅ UYUMLU -->
<!-- AÇIKLAMA: Buton metni açıklayıcı ve eylem odaklı -->
"""
        else:
            # İyileştirilmiş
            improved_text = btn_text.split()[0] if " " in btn_text and btn_text.split()[0] == btn_text.split()[1] else btn_text
            if len(btn_text) <= 2:
                improved_text = "Ara"  # Default
            
            return f"""<!-- İYİLEŞTİRİLMİŞ KOD -->
<button ref="{ref}"
        type="button"
        aria-label="{improved_text}"
        class="btn-primary">
  <span class="btn-text">{improved_text}</span>
</button>

<!-- İYİLEŞTİRMELER:
  1. Açıklayıcı buton metni: '{improved_text}'
  2. aria-label eklendi (ikon butonlar için)
  3. type="button" belirtildi
  4. Anlamsal sınıf eklendi
-->"""
    
    def _generate_form_html(self, element: Dict, original: bool) -> str:
        """Form HTML kodu"""
        form_type = element.get("type", "text")
        label = element.get("label", "")
        aria_label = element.get("aria-label", "")
        placeholder = element.get("placeholder", "")
        name = element.get("name", "field")
        autocomplete = element.get("autocomplete", "")
        ref = element.get("ref", "")
        form_label = label or aria_label
        
        input_types = {
            "textbox": "text",
            "combobox": "select",
            "listbox": "select",
            "checkbox": "checkbox",
            "radio": "radio"
        }
        
        html_type = input_types.get(form_type, "text")
        
        if original:
            # Mevcut
            autocomplete_attr = f' autocomplete="{autocomplete}"' if autocomplete else ""
            
            if not form_label and not placeholder:
                return f"""<!-- MEVCUT KOD (İHLAL) -->
<input type="{html_type}" 
       name="{name}"
       ref="{ref}"{autocomplete_attr}>

<!-- SORUN: Form alanının label'ı yok -->
<!-- WCAG: 1.3.1 Info and Relationships, 3.3.2 Labels or Instructions -->
<!-- AÇIKLAMA: Ekran okuyucu kullanıcıları form alanının amacını anlayamaz -->
"""
            elif not form_label and placeholder:
                return f"""<!-- MEVCUT KOD (UYARI) -->
<input type="{html_type}" 
       name="{name}"
       placeholder="{placeholder}"
       ref="{ref}"{autocomplete_attr}>

<!-- SORUN: Placeholder label olarak kullanılıyor -->
<!-- WCAG: 1.3.1 Info and Relationships -->
<!-- AÇIKLAMA: Placeholder kullanıcı yazmaya başladığında kaybolur -->
"""
            else:
                return f"""<!-- MEVCUT KOD (UYUMLU) -->
<label for="{name}">{form_label}</label>
<input type="{html_type}" 
       id="{name}"
       name="{name}"
       aria-label="{form_label}"
       ref="{ref}"{autocomplete_attr}>

<!-- DURUM: ✅ UYUMLU -->
<!-- AÇIKLAMA: Form alanı etiketli -->
"""
        else:
            # İyileştirilmiş
            improved_label = form_label or placeholder or "Alan"
            autocomplete_suggestion = autocomplete or self._suggest_autocomplete(form_type)
            
            return f"""<!-- İYİLEŞTİRİLMİŞ KOD -->
<div class="form-group">
  <label for="{name}" class="form-label">
    {improved_label}
    <span class="required" aria-hidden="true">*</span>
  </label>
  
  <input type="{html_type}"
         id="{name}"
         name="{name}"
         aria-label="{improved_label}"
         aria-describedby="{name}-hint"
         aria-required="true"
         autocomplete="{autocomplete_suggestion}"
         placeholder="{placeholder}"
         class="form-input"
         ref="{ref}">
  
  <span id="{name}-hint" class="form-hint">
    Lütfen geçerli bir {improved_label.lower()} girin.
  </span>
</div>

<!-- İYİLEŞTİRMELER:
  1. <label> elementi eklendi
  2. aria-describedby ile hint bağlandı
  3. aria-required ile zorunlu alan belirtildi
  4. autocomplete önerisi: '{autocomplete_suggestion}'
  5. Anlamsal CSS sınıfları
-->"""
    
    def _generate_image_html(self, element: Dict, original: bool) -> str:
        """Görsel HTML kodu"""
        alt = element.get("alt", "")
        src = element.get("src", "image.jpg")
        aria_hidden = element.get("aria-hidden", "")
        role = element.get("role", "")
        ref = element.get("ref", "")
        
        if original:
            # Mevcut
            if aria_hidden == "true" or role == "presentation":
                return f"""<!-- MEVCUT KOD (DEKORATİF) -->
<img src="{src}" 
     alt=""
     role="presentation"
     aria-hidden="true"
     ref="{ref}">

<!-- DURUM: ✅ UYUMLU (Dekoratif) -->
<!-- AÇIKLAMA: Dekoratif görsel, screen reader atlar -->
"""
            elif not alt:
                return f"""<!-- MEVCUT KOD (İHLAL) -->
<img src="{src}" ref="{ref}">

<!-- SORUN: Alt metin yok -->
<!-- WCAG: 1.1.1 Non-text Content -->
<!-- AÇIKLAMA: Ekran okuyucu kullanıcıları görselin ne olduğunu anlayamaz -->
"""
            elif alt.endswith((".jpg", ".png", ".gif")) or (len(alt) < 30 and "_" in alt):
                return f"""<!-- MEVCUT KOD (UYARI) -->
<img src="{src}" 
     alt="{alt}"
     ref="{ref}">

<!-- SORUN: Anlamsız alt metin: '{alt}' -->
<!-- WCAG: 1.1.1 Non-text Content -->
<!-- AÇIKLAMA: Dosya adı formatı anlamsız -->
"""
            else:
                return f"""<!-- MEVCUT KOD (UYUMLU) -->
<img src="{src}" 
     alt="{alt}"
     ref="{ref}">

<!-- DURUM: ✅ UYUMLU -->
<!-- AÇIKLAMA: Alt metin açıklayıcı -->
"""
        else:
            # İyileştirilmiş
            if aria_hidden == "true" or role == "presentation":
                return f"""<!-- İYİLEŞTİRİLMİŞ KOD (Dekoratif) -->
<img src="{src}" 
     alt=""
     role="presentation"
     aria-hidden="true"
     class="img-decorative"
     ref="{ref}">

<!-- İYİLEŞTİRMELER:
  1. alt="" (dekoratif için)
  2. role="presentation" belirtildi
  3. aria-hidden="true" eklendi
  4. Dekoratif için CSS sınıfı
-->"""
            else:
                improved_alt = alt if alt and not alt.endswith((".jpg", ".png")) else "Görselin içeriğini açıklayan metin"
                
                return f"""<!-- İYİLEŞTİRİLMİŞ KOD -->
<figure class="img-container">
  <img src="{src}" 
       alt="{improved_alt}"
       loading="lazy"
       decoding="async"
       class="img-responsive"
       ref="{ref}">
  
  <figcaption class="img-caption">
    {improved_alt}
  </figcaption>
</figure>

<!-- İYİLEŞTİRMELER:
  1. Anlamlı alt metin: '{improved_alt}'
  2. <figure> ve <figcaption> ile anlamsal yapı
  3. loading="lazy" performans için
  4. decoding="async" render optimizasyonu
  5. Responsive CSS sınıfı
-->"""
    
    def _generate_generic_html(self, element: Dict, original: bool) -> str:
        """Genel HTML kodu"""
        return f"""<!-- MEVCUT KOD -->
<div ref="{element.get('ref', '')}">
  {element.get('text', '')}
</div>
"""
    
    def _suggest_autocomplete(self, form_type: str) -> str:
        """Autocomplete önerisi"""
        suggestions = {
            "email": "email",
            "tel": "tel",
            "password": "current-password",
            "text": "on",
            "search": "search",
            "url": "url"
        }
        return suggestions.get(form_type, "on")
    
    def generate_css(self, element: Dict) -> str:
        """CSS çıktısı oluştur"""
        
        element_type = element.get("type", element.get("role", "div"))
        
        base_css = """/* Erişilebilirlik için Temel CSS */

/* Focus göstergesi - KRİTİK */
*:focus {
  outline: 2px solid #005fcc;
  outline-offset: 2px;
}

*:focus:not(:focus-visible) {
  outline: none;
}

*:focus-visible {
  outline: 2px solid #005fcc;
  outline-offset: 2px;
}

/* Skip Link - KRİTİK */
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: #005fcc;
  color: white;
  padding: 8px 16px;
  z-index: 10000;
  transition: top 0.3s;
}

.skip-link:focus {
  top: 0;
}

/* Başlıklar */
h1 { font-size: 2rem; margin: 1rem 0; }
h2 { font-size: 1.5rem; margin: 0.875rem 0; }
h3 { font-size: 1.25rem; margin: 0.75rem 0; }
h4 { font-size: 1rem; margin: 0.625rem 0; }

/* Linkler */
a {
  color: #005fcc;
  text-decoration: underline;
  text-underline-offset: 3px;
}

a:hover,
a:focus {
  color: #003d7a;
  text-decoration-thickness: 2px;
}

/* Butonlar */
button {
  min-height: 44px;
  min-width: 44px;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.btn-primary {
  background: #005fcc;
  color: white;
  border: none;
}

.btn-primary:hover,
.btn-primary:focus {
  background: #003d7a;
}

/* Form alanları */
.form-group {
  margin-bottom: 1rem;
}

.form-label {
  display: block;
  margin-bottom: 0.25rem;
  font-weight: 600;
}

.form-input {
  width: 100%;
  padding: 0.5rem;
  border: 2px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
}

.form-input:focus {
  border-color: #005fcc;
  outline: none;
  box-shadow: 0 0 0 3px rgba(0, 95, 204, 0.2);
}

.form-hint {
  display: block;
  margin-top: 0.25rem;
  font-size: 0.875rem;
  color: #666;
}

.required {
  color: #dc3545;
  margin-left: 0.25rem;
}

/* Görseller */
.img-container {
  margin: 1rem 0;
}

.img-responsive {
  max-width: 100%;
  height: auto;
}

.img-caption {
  margin-top: 0.5rem;
  font-size: 0.875rem;
  color: #666;
}

/* Ekran okuyucu için gizli içerik */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* Yüksek kontrast modu */
@media (prefers-contrast: high) {
  * {
    border-color: currentColor;
  }
  
  a:focus,
  button:focus,
  input:focus {
    outline: 3px solid currentColor;
  }
}

/* Hareket azaltma */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
"""
        
        return base_css
    
    def generate_js(self, element: Dict) -> str:
        """JavaScript çıktısı oluştur"""
        
        element_type = element.get("type", element.get("role", "div"))
        
        base_js = """// Erişilebilirlik için JavaScript

// Skip Link Functionality
document.addEventListener('DOMContentLoaded', function() {
  const skipLinks = document.querySelectorAll('.skip-link');
  
  skipLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.setAttribute('tabindex', '-1');
        target.focus();
      }
    });
  });
});

// Focus Trap for Modals
function trapFocus(element) {
  const focusableElements = element.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  
  const firstFocusable = focusableElements[0];
  const lastFocusable = focusableElements[focusableElements.length - 1];
  
  element.addEventListener('keydown', function(e) {
    if (e.key === 'Tab') {
      if (e.shiftKey) {
        if (document.activeElement === firstFocusable) {
          lastFocusable.focus();
          e.preventDefault();
        }
      } else {
        if (document.activeElement === lastFocusable) {
          firstFocusable.focus();
          e.preventDefault();
        }
      }
    }
    
    if (e.key === 'Escape') {
      closeModal();
    }
  });
}

// ARIA State Toggle
function toggleAriaExpanded(button) {
  const isExpanded = button.getAttribute('aria-expanded') === 'true';
  button.setAttribute('aria-expanded', !isExpanded);
  
  const controlsId = button.getAttribute('aria-controls');
  if (controlsId) {
    const controlledElement = document.getElementById(controlsId);
    if (controlledElement) {
      controlledElement.hidden = isExpanded;
    }
  }
}

// Form Validation
function validateForm(input) {
  const isValid = input.checkValidity();
  const errorId = input.getAttribute('aria-describedby');
  
  if (errorId) {
    const errorElement = document.getElementById(errorId);
    if (errorElement) {
      if (!isValid) {
        input.setAttribute('aria-invalid', 'true');
        errorElement.textContent = input.validationMessage;
        errorElement.hidden = false;
      } else {
        input.setAttribute('aria-invalid', 'false');
        errorElement.textContent = '';
        errorElement.hidden = true;
      }
    }
  }
  
  return isValid;
}

// Live Region Announcements
function announce(message, priority = 'polite') {
  const liveRegion = document.createElement('div');
  liveRegion.setAttribute('role', 'status');
  liveRegion.setAttribute('aria-live', priority);
  liveRegion.setAttribute('aria-atomic', 'true');
  liveRegion.className = 'sr-only';
  liveRegion.textContent = message;
  
  document.body.appendChild(liveRegion);
  
  setTimeout(() => {
    document.body.removeChild(liveRegion);
  }, 1000);
}

// Keyboard Navigation
document.addEventListener('keydown', function(e) {
  // Escape tuşu ile modal kapatma
  if (e.key === 'Escape') {
    const openModal = document.querySelector('[role="dialog"]:not([hidden])');
    if (openModal) {
      closeModal(openModal);
    }
  }
  
  // Enter/Space ile buton aktivasyonu
  if (e.key === 'Enter' || e.key === ' ') {
    const activeElement = document.activeElement;
    if (activeElement.getAttribute('role') === 'button') {
      e.preventDefault();
      activeElement.click();
    }
  }
});

// Intersection Observer for Lazy Loading
if ('IntersectionObserver' in window) {
  const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const image = entry.target;
        image.src = image.dataset.src;
        image.classList.remove('lazy');
        observer.unobserve(image);
      }
    });
  });
  
  document.querySelectorAll('img.lazy').forEach(img => {
    imageObserver.observe(img);
  });
}

// Focus Visible Polyfill
try {
  document.querySelector(':focus-visible');
} catch (e) {
  document.addEventListener('keydown', function() {
    document.body.classList.add('using-keyboard');
  });
  
  document.addEventListener('mousedown', function() {
    document.body.classList.remove('using-keyboard');
  });
}
"""
        
        return base_js


class ElementStructureAnalyzer:
    """Element yapısı ve DOM analizi"""
    
    def analyze_structure(self, element: Dict) -> Dict:
        """Element yapısını analiz et"""
        
        return {
            "dom_tree": self._get_dom_tree(element),
            "attributes": self._get_attributes(element),
            "computed_styles": self._get_computed_styles(element),
            "event_listeners": self._get_event_listeners(element),
            "parent_context": self._get_parent_context(element),
            "children": self._get_children(element),
            "siblings": self._get_siblings(element)
        }
    
    def _get_dom_tree(self, element: Dict) -> str:
        """DOM ağacı çıktısı"""
        ref = element.get("ref", "unknown")
        role = element.get("role", element.get("type", "div"))
        text = element.get("text", "")[:30]
        
        return f"""
DOM Ağacı:
└── <{role} ref="{ref}">
    └── Text: "{text}..."
"""
    
    def _get_attributes(self, element: Dict) -> Dict:
        """Element öznitelikleri"""
        return {
            "role": element.get("role", ""),
            "aria-label": element.get("aria-label", ""),
            "aria-labelledby": element.get("aria-labelledby", ""),
            "aria-describedby": element.get("aria-describedby", ""),
            "aria-expanded": element.get("aria-expanded", ""),
            "aria-pressed": element.get("aria-pressed", ""),
            "aria-hidden": element.get("aria-hidden", ""),
            "aria-invalid": element.get("aria-invalid", ""),
            "tabindex": element.get("tabindex", ""),
            "disabled": element.get("disabled", False),
            "href": element.get("href", ""),
            "alt": element.get("alt", ""),
            "title": element.get("title", ""),
            "placeholder": element.get("placeholder", ""),
            "autocomplete": element.get("autocomplete", ""),
            "required": element.get("required", False)
        }
    
    def _get_computed_styles(self, element: Dict) -> Dict:
        """Hesaplanan stiller (tahmini)"""
        return {
            "display": "block",
            "visibility": "visible",
            "color": "#000000",
            "background-color": "#ffffff",
            "font-size": "16px",
            "line-height": "1.5"
        }
    
    def _get_event_listeners(self, element: Dict) -> List[str]:
        """Olay dinleyicileri (tahmini)"""
        listeners = []
        
        role = element.get("role", "")
        if role == "button":
            listeners.extend(["click", "keydown"])
        elif role == "link":
            listeners.append("click")
        elif role in ["textbox", "combobox"]:
            listeners.extend(["input", "change", "focus", "blur"])
        
        return listeners
    
    def _get_parent_context(self, element: Dict) -> str:
        """Üst element bağlamı"""
        return "Ana içerik alanı (main) veya form grubu"
    
    def _get_children(self, element: Dict) -> List[str]:
        """Alt elementler"""
        return []
    
    def _get_siblings(self, element: Dict) -> List[str]:
        """Kardeş elementler"""
        return []


def generate_complete_element_report(element: Dict) -> Dict:
    """Tek element için tam rapor"""
    
    reporter = ElementReporter()
    code_gen = CodeGenerator()
    structure_analyzer = ElementStructureAnalyzer()
    
    # Element tipine göre rapor
    element_type = element.get("type", element.get("role", ""))
    
    if element_type == "heading":
        report = reporter.report_heading(element)
    elif element_type == "link":
        report = reporter.report_link(element)
    elif element_type == "button":
        report = reporter.report_button(element)
    elif element_type in ["textbox", "combobox", "listbox", "checkbox", "radio"]:
        report = reporter.report_form(element)
    elif element_type in ["img", "image"]:
        report = reporter.report_image(element)
    else:
        report = reporter.report_heading(element)  # Default
    
    # Kod çıktıları
    report["code"] = {
        "html_original": code_gen.generate_html(element, original=True),
        "html_improved": code_gen.generate_html(element, original=False),
        "css": code_gen.generate_css(element),
        "js": code_gen.generate_js(element)
    }
    
    # Element yapısı
    report["structure"] = structure_analyzer.analyze_structure(element)
    
    return report


def generate_full_report(accessibility_tree: dict, page_name: str, page_url: str) -> dict:
    """Kapsamlı element bazlı rapor oluştur"""
    
    reporter = ElementReporter()
    
    # Elementleri çıkar
    elements = []
    
    def traverse(node):
        if isinstance(node, dict):
            role = node.get("role", "")
            
            if role == "heading":
                elements.append(reporter.report_heading(node))
            elif role == "link":
                elements.append(reporter.report_link(node))
            elif role == "button":
                elements.append(reporter.report_button(node))
            elif role in ["textbox", "combobox", "listbox", "checkbox", "radio"]:
                elements.append(reporter.report_form(node))
            elif "img" in str(node).lower() or role == "img":
                elements.append(reporter.report_image(node))
            
            for key, value in node.items():
                if isinstance(value, list):
                    for item in value:
                        traverse(item)
                elif isinstance(value, dict):
                    traverse(value)
    
    traverse(accessibility_tree)
    
    return {
        "page": page_name,
        "url": page_url,
        "timestamp": datetime.now().isoformat(),
        "elements": elements,
        "total_elements": len(elements)
    }


if __name__ == "__main__":
    # Test
    test_tree = {
        "role": "document",
        "children": [
            {"role": "heading", "level": 1, "text": "Ana Başlık", "ref": "h1-1"},
            {"role": "link", "text": "Tıklayın", "href": "#", "ref": "link-1"},
            {"role": "button", "text": "", "aria-label": "Ara", "ref": "btn-1"},
            {"role": "button", "text": "Sepete Ekle", "ref": "btn-2"},
            {"role": "textbox", "aria-label": "E-posta", "ref": "input-1"},
            {"role": "img", "alt": "Ürün görseli", "src": "product.jpg", "ref": "img-1"}
        ]
    }
    
    report = generate_full_report(test_tree, "Test Sayfası", "https://example.com")
    
    # Element bazlı çıktı
    for element in report["elements"]:
        print(f"\n{'='*60}")
        print(f"Element Detayı: {element['element_type']} - {element['name']}")
        print(f"{'='*60}")
        print(f"\nTemel Bilgiler:")
        for key, value in element["basic_info"].items():
            print(f"  {key}: {value}")
        print(f"\nDurum: {element['accessibility_status']['status']} (Skor: {element['accessibility_status']['score']})")
        print(f"\nParagraf:\n{element['paragraph']}")
        print(f"\nVoiceOver Duyurusu: {element['voiceover_test']['announcement']}")
        
        if element["issues"]:
            print(f"\nSorunlar:")
            for issue in element["issues"]:
                print(f"  - {issue['issue']}")
                print(f"    WCAG: {issue['wcag']}")
                print(f"    Öneri: {issue['recommendation']}")