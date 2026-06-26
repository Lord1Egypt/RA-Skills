#!/usr/bin/env python3
"""
AccessMind Behavioral Bridge - Extension-Skill Köprüsü
Davranış bazlı erişilebilirlik denetim sistemi

Bu modül:
1. Extension'dan gelen verileri alır
2. OpenClaw browser tool ile derinlemesine analiz yapar
3. Sonuçları geri gönderir
4. Davranış kalıplarını öğrenir
"""

import json
import asyncio
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import subprocess

# OpenClaw browser tool entegrasyonu
sys.path.append('/Users/sarper/.openclaw/workspace/scripts')


class BehaviorType(Enum):
    KEYBOARD_NAVIGATION = "keyboard_navigation"
    FOCUS_CHANGE = "focus_change"
    ELEMENT_INTERACTION = "element_interaction"
    FORM_SUBMISSION = "form_submission"
    ERROR_ENCOUNTER = "error_encounter"
    SCREEN_READER_SIMULATION = "screen_reader_simulation"


@dataclass
class BehavioralEvent:
    """Kullanıcı davranış olayı"""
    type: BehaviorType
    element_ref: str
    element_tag: str
    element_role: str
    timestamp: str
    success: bool
    context: Dict[str, Any] = field(default_factory=dict)
    
    # Erişilebilirlik analizi
    wcag_issues: List[Dict] = field(default_factory=list)
    focus_visible: bool = False
    aria_label: str = ""
    accessible_name: str = ""


@dataclass
class BehavioralAuditResult:
    """Davranış bazlı denetim sonucu"""
    url: str
    timestamp: str
    total_events: int
    success_rate: float
    wcag_violations: List[Dict]
    behavioral_patterns: Dict[str, Any]
    recommendations: List[str]
    scores: Dict[str, int]


class AccessMindBehavioralBridge:
    """Extension-Skill köprüsü - Davranış bazlı denetim"""
    
    def __init__(self, output_dir: str = "/Users/sarper/.openclaw/workspace/audits"):
        self.output_dir = output_dir
        self.events: List[BehavioralEvent] = []
        self.learned_patterns: Dict[str, List[Dict]] = {}
        
        os.makedirs(output_dir, exist_ok=True)
    
    async def analyze_keyboard_navigation(self, url: str, steps: int = 50) -> Dict:
        """
        Klavye navigasyonu analizi - Browser tool ile
        """
        results = {
            "url": url,
            "timestamp": datetime.now().isoformat(),
            "steps": [],
            "focus_traps": [],
            "focus_order_issues": [],
            "missing_focus_indicators": [],
            "skip_links": [],
            "scores": {}
        }
        
        # Browser tool kullanarak Tab simülasyonu
        # Bu, OpenClaw browser tool ile yapılır
        
        return results
    
    def process_extension_event(self, event_data: Dict) -> BehavioralEvent:
        """
        Extension'dan gelen olayı işle
        """
        event = BehavioralEvent(
            type=BehaviorType(event_data.get("type", "element_interaction")),
            element_ref=event_data.get("element_ref", ""),
            element_tag=event_data.get("element_tag", ""),
            element_role=event_data.get("element_role", ""),
            timestamp=event_data.get("timestamp", datetime.now().isoformat()),
            success=event_data.get("success", True),
            context=event_data.get("context", {}),
        )
        
        # Olayı analiz et
        self._analyze_event(event)
        
        # Kaydet
        self.events.append(event)
        
        return event
    
    def _analyze_event(self, event: BehavioralEvent):
        """
        Olayı erişilebilirlik açısından analiz et
        """
        issues = []
        
        # Klavye navigasyonu analizi
        if event.type == BehaviorType.KEYBOARD_NAVIGATION:
            if not event.context.get("focus_visible", False):
                issues.append({
                    "wcag": "2.4.7",
                    "severity": "serious",
                    "message": f"Focus göstergesi görünmüyor: {event.element_tag}",
                    "element_ref": event.element_ref
                })
                event.focus_visible = False
            else:
                event.focus_visible = True
        
        # Form etkileşimi analizi
        if event.type == BehaviorType.FORM_SUBMISSION:
            if not event.context.get("has_label", False):
                issues.append({
                    "wcag": "1.3.1",
                    "severity": "critical",
                    "message": f"Form elemanının etiketi yok: {event.element_tag}",
                    "element_ref": event.element_ref
                })
        
        # Hata analizi
        if event.type == BehaviorType.ERROR_ENCOUNTER:
            if not event.context.get("error_announced", False):
                issues.append({
                    "wcag": "4.1.3",
                    "severity": "serious",
                    "message": "Hata mesajı ekran okuyucuya duyurulmadı",
                    "element_ref": event.element_ref
                })
        
        event.wcag_issues = issues
    
    def generate_behavioral_report(self, url: str) -> BehavioralAuditResult:
        """
        Davranış bazlı denetim raporu oluştur
        """
        # Toplam olay sayısı
        total_events = len(self.events)
        
        # Başarı oranı
        successful_events = sum(1 for e in self.events if e.success)
        success_rate = successful_events / total_events if total_events > 0 else 0
        
        # WCAG ihlalleri
        all_violations = []
        for event in self.events:
            all_violations.extend(event.wcag_issues)
        
        # Benzersiz ihlaller
        unique_violations = []
        seen = set()
        for v in all_violations:
            key = (v.get("wcag"), v.get("element_ref"))
            if key not in seen:
                seen.add(key)
                unique_violations.append(v)
        
        # Davranış kalıpları
        patterns = self._detect_patterns()
        
        # Öneriler
        recommendations = self._generate_recommendations(unique_violations, patterns)
        
        # Skorlar
        scores = self._calculate_scores(unique_violations, patterns)
        
        return BehavioralAuditResult(
            url=url,
            timestamp=datetime.now().isoformat(),
            total_events=total_events,
            success_rate=success_rate,
            wcag_violations=unique_violations,
            behavioral_patterns=patterns,
            recommendations=recommendations,
            scores=scores
        )
    
    def _detect_patterns(self) -> Dict[str, Any]:
        """
        Davranış kalıplarını tespit et
        """
        patterns = {
            "common_errors": {},
            "navigation_flow": [],
            "problematic_elements": [],
            "successful_patterns": []
        }
        
        # En sık hata alan elementler
        error_counts = {}
        for event in self.events:
            if not event.success:
                key = f"{event.element_tag}:{event.element_role}"
                error_counts[key] = error_counts.get(key, 0) + 1
        
        patterns["common_errors"] = dict(sorted(error_counts.items(), key=lambda x: -x[1])[:5])
        
        # Navigasyon akışı
        nav_events = [e for e in self.events if e.type == BehaviorType.KEYBOARD_NAVIGATION]
        patterns["navigation_flow"] = [
            {"ref": e.element_ref, "tag": e.element_tag, "focus_visible": e.focus_visible}
            for e in nav_events[:20]
        ]
        
        # Problematic elements
        patterns["problematic_elements"] = [
            {"ref": e.element_ref, "tag": e.element_tag, "issues": len(e.wcag_issues)}
            for e in self.events if e.wcag_issues
        ][:10]
        
        return patterns
    
    def _generate_recommendations(self, violations: List[Dict], patterns: Dict) -> List[str]:
        """
        Öneriler oluştur
        """
        recommendations = []
        
        # WCAG bazlı öneriler
        wcag_issues = {}
        for v in violations:
            wcag = v.get("wcag", "unknown")
            if wcag not in wcag_issues:
                wcag_issues[wcag] = 0
            wcag_issues[wcag] += 1
        
        if "2.4.7" in wcag_issues:
            recommendations.append("Focus göstergeleri için :focus-visible CSS sınıfı ekleyin")
        
        if "1.3.1" in wcag_issues:
            recommendations.append("Form elemanlarına aria-label veya <label> ekleyin")
        
        if "4.1.3" in wcag_issues:
            recommendations.append("Dinamik içerik için aria-live region kullanın")
        
        # Davranış bazlı öneriler
        if patterns.get("common_errors"):
            most_common = list(patterns["common_errors"].keys())[0]
            recommendations.append(f"En sık hata: {most_common} - Bu element türüne öncelik verin")
        
        return recommendations
    
    def _calculate_scores(self, violations: List[Dict], patterns: Dict) -> Dict[str, int]:
        """
        Skorları hesapla
        """
        scores = {
            "focus_efficiency": 100,
            "keyboard_accessibility": 100,
            "screen_reader_friendliness": 100,
            "behavioral_score": 100
        }
        
        # İhlallerden düş
        for v in violations:
            severity = v.get("severity", "moderate")
            penalty = {"critical": 10, "serious": 5, "moderate": 2, "minor": 1}.get(severity, 2)
            
            wcag = v.get("wcag", "")
            if wcag.startswith("2.4"):
                scores["keyboard_accessibility"] -= penalty
            if wcag.startswith("4.1"):
                scores["screen_reader_friendliness"] -= penalty
        
        # Minimum 0
        for key in scores:
            scores[key] = max(0, scores[key])
        
        return scores
    
    def save_report(self, result: BehavioralAuditResult) -> str:
        """
        Raporu kaydet
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"behavioral_audit_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                "url": result.url,
                "timestamp": result.timestamp,
                "total_events": result.total_events,
                "success_rate": result.success_rate,
                "wcag_violations": result.wcag_violations,
                "behavioral_patterns": result.behavioral_patterns,
                "recommendations": result.recommendations,
                "scores": result.scores
            }, f, ensure_ascii=False, indent=2)
        
        return filepath
    
    def reset(self):
        """
        Olayları sıfırla
        """
        self.events = []


# CLI kullanımı
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='AccessMind Behavioral Bridge')
    parser.add_argument('--url', help='Test edilecek URL')
    parser.add_argument('--output', default='/Users/sarper/.openclaw/workspace/audits', help='Çıktı dizini')
    parser.add_argument('--events', help='Olay dosyası (JSON)')
    
    args = parser.parse_args()
    
    bridge = AccessMindBehavioralBridge(output_dir=args.output)
    
    if args.events:
        # Olay dosyasından yükle
        with open(args.events, 'r') as f:
            events_data = json.load(f)
        
        for event_data in events_data:
            bridge.process_extension_event(event_data)
        
        result = bridge.generate_behavioral_report(args.url or "unknown")
        filepath = bridge.save_report(result)
        print(f"✅ Rapor kaydedildi: {filepath}")
    
    else:
        print("Kullanım:")
        print("  python3 accessmind-behavioral-bridge.py --events events.json --url https://example.com")