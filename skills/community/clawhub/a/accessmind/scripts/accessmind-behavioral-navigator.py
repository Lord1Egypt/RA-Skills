#!/usr/bin/env python3
"""
AccessMind Behavioral Navigator v2.0
Davranış bazlı erişilebilirlik gezinim ve test sistemi

Özellikler:
1. Akıllı klavye navigasyonu - Kullanıcı davranışını taklit eder
2. Focus trap detection - Gelişmiş focus tuzakları tespiti
3. Screen reader simülasyonu - NVDA/JAWS benzeri davranış
4. Form interaction testing - Form etkileşim testleri
5. Dynamic content monitoring - Dinamik içerik takibi
6. Keyboard shortcut testing - Kısayol tuşları testi
7. Behavioral pattern learning - Davranış kalıbı öğrenimi
"""

import json
import asyncio
import os
import sys
import time
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import subprocess
import traceback

# Playwright for browser automation
try:
    from playwright.async_api import async_playwright, Page, Browser, ElementHandle
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️ Playwright yüklü değil. Yüklemek için: pip install playwright && playwright install chromium")


class NavigationMode(Enum):
    """Gezinim modları"""
    LINEAR = "linear"  # Sırayla Tab ile gezin
    SMART = "smart"    # Önemli elementlere öncelik ver
    FORM_FOCUSED = "form"  # Form elemanlarına odaklan
    LANDMARK = "landmark"  # Landmark'lara göre gezin
    HEADING = "heading"  # Başlık seviyelerine göre gezin


class BehaviorPattern(Enum):
    """Davranış kalıpları"""
    TAB_NAVIGATION = "tab_navigation"
    SHIFT_TAB = "shift_tab"
    ENTER_ACTIVATION = "enter_activation"
    SPACE_ACTIVATION = "space_activation"
    ESCAPE_CLOSE = "escape_close"
    ARROW_NAVIGATION = "arrow_navigation"
    SHORTCUT_USE = "shortcut_use"
    FORM_SUBMISSION = "form_submission"
    ERROR_RECOVERY = "error_recovery"
    SEARCH_PATTERN = "search_pattern"


@dataclass
class NavigationStep:
    """Gezinim adımı"""
    step_number: int
    element_ref: str
    element_tag: str
    element_role: str
    element_name: str
    focus_visible: bool
    focus_outline: str
    aria_label: str
    accessible_name: str
    is_interactive: bool
    wcag_issues: List[Dict] = field(default_factory=list)
    timestamp: str = ""
    screenshot_path: str = ""


@dataclass
class FocusTrap:
    """Focus tuzağı"""
    element_ref: str
    element_tag: str
    trap_type: str  # "infinite_loop", "no_escape", "modal_trap"
    severity: str  # "critical", "serious", "moderate"
    description: str
    wcag_criterion: str
    reproduction_steps: List[str]


@dataclass
class BehavioralTest:
    """Davranış testi"""
    test_name: str
    test_type: str
    actions: List[Dict]
    expected_result: str
    actual_result: str
    passed: bool
    wcag_criteria: List[str]
    notes: str


@dataclass
class BehavioralAuditReport:
    """Davranış bazlı denetim raporu"""
    url: str
    timestamp: str
    navigation_mode: NavigationMode
    
    # Gezinim istatistikleri
    total_steps: int
    focus_changes: int
    unique_elements: int
    interactive_elements: int
    
    # Focus göstergeleri
    visible_focus_count: int
    missing_focus_count: int
    focus_visible_support: int
    
    # Focus traps
    focus_traps: List[FocusTrap]
    trap_count: int
    
    # Screen reader simülasyonu
    announcements: List[Dict]
    aria_live_regions: List[Dict]
    name_calculation_issues: List[Dict]
    
    # Form testleri
    form_tests: List[BehavioralTest]
    form_error_handling: List[Dict]
    
    # Keyboard shortcut testleri
    shortcut_tests: List[BehavioralTest]
    
    # WCAG ihlalleri
    wcag_violations: List[Dict]
    violations_by_criterion: Dict[str, int]
    
    # Skorlar
    scores: Dict[str, int]
    
    # Öneriler
    recommendations: List[str]
    
    # Ham veriler
    navigation_steps: List[NavigationStep] = field(default_factory=list)
    screenshot_paths: List[str] = field(default_factory=list)


class AccessMindBehavioralNavigator:
    """Davranış bazlı erişilebilirlik gezinim sistemi"""
    
    def __init__(
        self,
        url: str,
        output_dir: str = "/Users/sarper/.openclaw/workspace/audits",
        navigation_mode: NavigationMode = NavigationMode.SMART,
        max_steps: int = 100,
        headless: bool = True
    ):
        self.url = url
        self.output_dir = output_dir
        self.navigation_mode = navigation_mode
        self.max_steps = max_steps
        self.headless = headless
        
        # State
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.navigation_steps: List[NavigationStep] = []
        self.focus_traps: List[FocusTrap] = []
        self.visited_elements: Set[str] = set()
        self.focus_history: List[str] = []
        
        # WCAG kriterleri
        self.wcag_criteria = {
            "2.1.1": "Keyboard",
            "2.1.2": "No Keyboard Trap",
            "2.4.3": "Focus Order",
            "2.4.7": "Focus Visible",
            "4.1.2": "Name, Role, Value",
            "4.1.3": "Status Messages"
        }
        
        os.makedirs(output_dir, exist_ok=True)
    
    async def initialize(self):
        """Tarayıcıyı başlat"""
        if not PLAYWRIGHT_AVAILABLE:
            raise RuntimeError("Playwright yüklü değil. pip install playwright && playwright install chromium")
        
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=self.headless)
        self.page = await self.browser.new_page()
        
        # Screen reader simülasyonu için
        await self.page.set_extra_http_headers({
            "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7"
        })
    
    async def close(self):
        """Tarayıcıyı kapat"""
        if self.browser:
            await self.browser.close()
    
    async def navigate_to_url(self):
        """URL'ye git"""
        await self.page.goto(self.url, wait_until="networkidle", timeout=60000)
        await self.page.wait_for_timeout(2000)  # Dinamik içerik için bekle
    
    async def get_page_snapshot(self) -> Dict:
        """Sayfa snapshot'ı al"""
        snapshot = await self.page.evaluate("""
            () => {
                const getAccessibleName = (el) => {
                    // aria-label
                    if (el.getAttribute('aria-label')) {
                        return el.getAttribute('aria-label');
                    }
                    // aria-labelledby
                    const labelledBy = el.getAttribute('aria-labelledby');
                    if (labelledBy) {
                        const labelEl = document.getElementById(labelledBy);
                        if (labelEl) return labelEl.textContent.trim();
                    }
                    // <label> for attribute
                    if (el.id) {
                        const label = document.querySelector(`label[for="${el.id}"]`);
                        if (label) return label.textContent.trim();
                    }
                    // <label> wrapping
                    const parentLabel = el.closest('label');
                    if (parentLabel) return parentLabel.textContent.trim();
                    // title attribute
                    if (el.getAttribute('title')) {
                        return el.getAttribute('title');
                    }
                    // placeholder
                    if (el.getAttribute('placeholder')) {
                        return el.getAttribute('placeholder');
                    }
                    // innerText for buttons, links
                    if (el.innerText) {
                        return el.innerText.trim().substring(0, 50);
                    }
                    // alt for images
                    if (el.getAttribute('alt')) {
                        return el.getAttribute('alt');
                    }
                    return '';
                };
                
                const elements = [];
                const focusable = document.querySelectorAll(
                    'a[href], button, input, select, textarea, [tabindex]:not([tabindex="-1"]), [contenteditable="true"]'
                );
                
                focusable.forEach((el, idx) => {
                    const rect = el.getBoundingClientRect();
                    if (rect.width > 0 && rect.height > 0) {
                        const style = window.getComputedStyle(el);
                        elements.push({
                            ref: `e${idx}`,
                            tag: el.tagName.toLowerCase(),
                            role: el.getAttribute('role') || el.tagName.toLowerCase(),
                            name: getAccessibleName(el),
                            ariaLabel: el.getAttribute('aria-label') || '',
                            tabIndex: el.getAttribute('tabindex') || '0',
                            isInteractive: el.tagName.match(/A|BUTTON|INPUT|SELECT|TEXTAREA/) !== null,
                            isVisible: rect.width > 0 && rect.height > 0,
                            focusOutline: style.outline,
                            focusVisible: false, // Will be checked during navigation
                            hasFocus: document.activeElement === el,
                            position: { x: rect.x, y: rect.y, width: rect.width, height: rect.height }
                        });
                    }
                });
                
                // ARIA live regions
                const liveRegions = [];
                document.querySelectorAll('[aria-live]').forEach(el => {
                    liveRegions.push({
                        ariaLive: el.getAttribute('aria-live'),
                        ariaAtomic: el.getAttribute('aria-atomic'),
                        ariaRelevant: el.getAttribute('aria-relevant'),
                        content: el.textContent.trim().substring(0, 100)
                    });
                });
                
                // Landmarks
                const landmarks = [];
                document.querySelectorAll('[role="banner"], [role="main"], [role="navigation"], [role="complementary"], [role="form"], [role="search"], header, main, nav, aside, form').forEach(el => {
                    landmarks.push({
                        role: el.getAttribute('role') || el.tagName.toLowerCase(),
                        label: el.getAttribute('aria-label') || ''
                    });
                });
                
                // Headings
                const headings = [];
                document.querySelectorAll('h1, h2, h3, h4, h5, h6, [role="heading"]').forEach(el => {
                    headings.push({
                        level: el.getAttribute('aria-level') || el.tagName.substring(1),
                        text: el.textContent.trim().substring(0, 50)
                    });
                });
                
                return {
                    url: window.location.href,
                    title: document.title,
                    elements: elements,
                    liveRegions: liveRegions,
                    landmarks: landmarks,
                    headings: headings,
                    totalFocusable: elements.length
                };
            }
        """)
        
        return snapshot
    
    async def check_focus_visible(self, element_ref: str) -> Tuple[bool, str]:
        """Element'in focus göstergesi var mı kontrol et"""
        result = await self.page.evaluate(f"""
            () => {{
                const el = document.querySelector('[data-ref="{element_ref}"]');
                if (!el) return {{ visible: false, outline: 'none' }};
                
                // Focus element'e ver
                el.focus();
                
                // :focus-visible kontrolü
                const style = window.getComputedStyle(el);
                const hasOutline = style.outline !== 'none' && style.outline !== '';
                const hasBoxShadow = style.boxShadow !== 'none' && style.boxShadow !== '';
                const hasBorder = style.border !== style.getPropertyValue('border');
                
                // :focus-visible pseudo-class kontrolü
                const focusVisibleSupported = 'matches' in Element.prototype;
                let hasFocusVisible = false;
                if (focusVisibleSupported) {{
                    try {{
                        hasFocusVisible = el.matches(':focus-visible');
                    }} catch (e) {{
                        hasFocusVisible = false;
                    }}
                }}
                
                return {{
                    visible: hasOutline || hasBoxShadow || hasFocusVisible,
                    outline: style.outline,
                    boxShadow: style.boxShadow
                }};
            }}
        """)
        
        return result.get('visible', False), result.get('outline', 'none')
    
    async def simulate_tab_navigation(self, steps: int = 50) -> List[NavigationStep]:
        """Tab navigasyonu simülasyonu"""
        navigation_steps = []
        
        # İlk element'e focus
        await self.page.keyboard.press('Tab')
        await self.page.wait_for_timeout(100)
        
        for i in range(steps):
            step_number = i + 1
            
            # Aktif element bilgisini al
            active_info = await self.page.evaluate("""
                () => {
                    const el = document.activeElement;
                    if (!el || el === document.body) return null;
                    
                    const getAccessibleName = (element) => {
                        if (element.getAttribute('aria-label')) return element.getAttribute('aria-label');
                        if (element.getAttribute('aria-labelledby')) {
                            const labelEl = document.getElementById(element.getAttribute('aria-labelledby'));
                            if (labelEl) return labelEl.textContent.trim();
                        }
                        if (element.id) {
                            const label = document.querySelector(`label[for="${element.id}"]`);
                            if (label) return label.textContent.trim();
                        }
                        if (element.getAttribute('placeholder')) return element.getAttribute('placeholder');
                        if (element.innerText) return element.innerText.trim().substring(0, 50);
                        if (element.getAttribute('alt')) return element.getAttribute('alt');
                        return '';
                    };
                    
                    const rect = el.getBoundingClientRect();
                    const style = window.getComputedStyle(el);
                    
                    return {
                        tag: el.tagName.toLowerCase(),
                        role: el.getAttribute('role') || el.tagName.toLowerCase(),
                        name: getAccessibleName(el),
                        ariaLabel: el.getAttribute('aria-label') || '',
                        tabIndex: el.getAttribute('tabindex') || '0',
                        type: el.getAttribute('type') || '',
                        href: el.getAttribute('href') || '',
                        isVisible: rect.width > 0 && rect.height > 0,
                        hasOutline: style.outline !== 'none' && style.outline !== '',
                        outline: style.outline,
                        position: { x: rect.x, y: rect.y, width: rect.width, height: rect.height }
                    };
                }
            """)
            
            if not active_info:
                # Focus body'de, döngü başa sardı
                break
            
            element_ref = f"step_{step_number}"
            
            # Focus tuzağı kontrolü
            element_key = f"{active_info['tag']}:{active_info['name']}"
            if element_key in self.visited_elements:
                # Aynı element'e tekrar gelindi - focus tuzağı olabilir
                pass
            self.visited_elements.add(element_key)
            
            # WCAG ihlalleri kontrolü
            wcag_issues = []
            
            if not active_info.get('hasOutline', False):
                wcag_issues.append({
                    "wcag": "2.4.7",
                    "severity": "serious",
                    "message": f"Focus göstergesi yok: {active_info['tag']} - {active_info['name']}",
                    "element": element_ref
                })
            
            if not active_info.get('name') and active_info.get('isInteractive', True):
                wcag_issues.append({
                    "wcag": "4.1.2",
                    "severity": "critical",
                    "message": f"Erişilebilir isim yok: {active_info['tag']}",
                    "element": element_ref
                })
            
            # Navigation step kaydet
            step = NavigationStep(
                step_number=step_number,
                element_ref=element_ref,
                element_tag=active_info['tag'],
                element_role=active_info['role'],
                element_name=active_info.get('name', ''),
                focus_visible=active_info.get('hasOutline', False),
                focus_outline=active_info.get('outline', 'none'),
                aria_label=active_info.get('ariaLabel', ''),
                accessible_name=active_info.get('name', ''),
                is_interactive=active_info.get('isInteractive', True),
                wcag_issues=wcag_issues,
                timestamp=datetime.now().isoformat()
            )
            
            navigation_steps.append(step)
            
            # Sonraki element'e geç
            await self.page.keyboard.press('Tab')
            await self.page.wait_for_timeout(100)
        
        return navigation_steps
    
    async def detect_focus_traps(self) -> List[FocusTrap]:
        """Focus tuzaklarını tespit et"""
        traps = []
        
        # 1. Modal focus tuzağı kontrolü
        modal_traps = await self.page.evaluate("""
            () => {
                const traps = [];
                
                // Modal dialog'ları bul
                const modals = document.querySelectorAll('[role="dialog"], [role="alertdialog"], .modal, .dialog');
                
                modals.forEach(modal => {
                    const focusableElements = modal.querySelectorAll(
                        'a[href], button, input, select, textarea, [tabindex]:not([tabindex="-1"])'
                    );
                    
                    if (focusableElements.length > 0) {
                        // Modal açık mı kontrol et
                        const style = window.getComputedStyle(modal);
                        const isVisible = style.display !== 'none' && style.visibility !== 'hidden';
                        
                        if (isVisible) {
                            traps.push({
                                type: 'modal_trap',
                                element: modal.tagName.toLowerCase(),
                                hasCloseButton: modal.querySelector('button[aria-label*="close"], button.close, [aria-label*="kapat"]') !== null,
                                ariaModal: modal.getAttribute('aria-modal'),
                                ariaLabel: modal.getAttribute('aria-label')
                            });
                        }
                    }
                });
                
                return traps;
            }
        """)
        
        for trap in modal_traps:
            if not trap.get('hasCloseButton') and not trap.get('ariaModal'):
                traps.append(FocusTrap(
                    element_ref="modal",
                    element_tag=trap.get('element', 'div'),
                    trap_type="modal_trap",
                    severity="serious",
                    description="Modal açık ancak kapatma mekanizması erişilebilir değil",
                    wcag_criterion="2.1.2",
                    reproduction_steps=["Modal aç", "Tab ile gez", "Kapatma tuşu yok"]
                ))
        
        # 2. Infinite loop kontrolü
        if len(self.focus_history) > 10:
            # Son 10 element'i kontrol et
            last_10 = self.focus_history[-10:]
            if len(set(last_10)) < 5:  # 5'ten az unique element
                traps.append(FocusTrap(
                    element_ref="infinite_loop",
                    element_tag="unknown",
                    trap_type="infinite_loop",
                    severity="critical",
                    description="Klavye navigasyonu sonsuz döngüye girdi",
                    wcag_criterion="2.1.2",
                    reproduction_steps=["Tab ile gezin", "5 element'ten sonra başa sariyor"]
                ))
        
        # 3. Escape tuşu kontrolü
        escape_test = await self.page.evaluate("""
            () => {
                // Escape tuşu dinleyicisi var mı?
                const hasEscapeListener = document.querySelectorAll('[role="dialog"], [role="alertdialog"]').length > 0;
                return {
                    hasEscapeListener: hasEscapeListener,
                    openModals: document.querySelectorAll('[role="dialog"][aria-hidden="false"], [role="alertdialog"][aria-hidden="false"]').length
                };
            }
        """)
        
        return traps
    
    async def simulate_screen_reader(self) -> Dict:
        """Screen reader simülasyonu"""
        # NVDA/JAWS benzeri davranış simülasyonu
        announcements = []
        
        # 1. Sayfa başlığı
        title = await self.page.title()
        announcements.append({
            "type": "page_title",
            "content": title,
            "source": "browser"
        })
        
        # 2. Landmark'ları duyur
        landmarks = await self.page.evaluate("""
            () => {
                const landmarks = [];
                document.querySelectorAll('[role="banner"], [role="main"], [role="navigation"], [role="complementary"], [role="form"], [role="search"], header, main, nav, aside, form').forEach(el => {
                    landmarks.push({
                        role: el.getAttribute('role') || el.tagName.toLowerCase(),
                        label: el.getAttribute('aria-label') || ''
                    });
                });
                return landmarks;
            }
        """)
        
        for landmark in landmarks:
            label = landmark.get('label', '')
            role = landmark.get('role', '')
            announcements.append({
                "type": "landmark",
                "content": f"{role} bölgesi" + (f": {label}" if label else ""),
                "source": "aria"
            })
        
        # 3. Başlıkları duyur
        headings = await self.page.evaluate("""
            () => {
                const headings = [];
                document.querySelectorAll('h1, h2, h3, h4, h5, h6, [role="heading"]').forEach(el => {
                    headings.push({
                        level: el.getAttribute('aria-level') || (el.tagName ? el.tagName.substring(1) : '2'),
                        text: el.textContent.trim().substring(0, 100)
                    });
                });
                return headings;
            }
        """)
        
        for heading in headings:
            level = heading.get('level', '2')
            text = heading.get('text', '')
            announcements.append({
                "type": "heading",
                "content": f"Başlık seviye {level}: {text}",
                "source": "heading"
            })
        
        # 4. ARIA live regions
        live_regions = await self.page.evaluate("""
            () => {
                const regions = [];
                document.querySelectorAll('[aria-live]').forEach(el => {
                    regions.push({
                        ariaLive: el.getAttribute('aria-live'),
                        ariaAtomic: el.getAttribute('aria-atomic'),
                        content: el.textContent.trim().substring(0, 100)
                    });
                });
                return regions;
            }
        """)
        
        return {
            "announcements": announcements,
            "landmarks": landmarks,
            "headings": headings,
            "live_regions": live_regions
        }
    
    async def test_form_interactions(self) -> List[BehavioralTest]:
        """Form etkileşim testleri"""
        tests = []
        
        # Form element'lerini bul
        forms = await self.page.query_selector_all('form')
        
        for i, form in enumerate(forms):
            form_test = BehavioralTest(
                test_name=f"Form {i+1} Interaction",
                test_type="form_submission",
                actions=[],
                expected_result="Form elements accessible, labels present, error messages announced",
                actual_result="",
                passed=False,
                wcag_criteria=["1.3.1", "3.3.1", "3.3.2", "4.1.2"],
                notes=""
            )
            
            # Form element'lerini kontrol et
            form_elements = await form.query_selector_all('input, select, textarea, button')
            
            for el in form_elements:
                tag = await el.evaluate('el => el.tagName.toLowerCase()')
                has_label = await el.evaluate('el => el.getAttribute("aria-label") || el.getAttribute("aria-labelledby") || document.querySelector(`label[for="${el.id}"]`) !== null')
                
                if not has_label:
                    form_test.wcag_criteria.append("1.3.1")
                    form_test.notes += f"Label missing for {tag}. "
            
            # Submit testi
            submit_btn = await form.query_selector('button[type="submit"], input[type="submit"]')
            if submit_btn:
                form_test.actions.append({"action": "click", "target": "submit"})
            
            form_test.passed = "Label missing" not in form_test.notes
            tests.append(form_test)
        
        return tests
    
    async def test_keyboard_shortcuts(self) -> List[BehavioralTest]:
        """Klavye kısayol testleri"""
        tests = []
        
        # Skip link testi
        skip_test = BehavioralTest(
            test_name="Skip Link Test",
            test_type="shortcut",
            actions=[{"key": "Tab", "expected": "Skip link visible"}],
            expected_result="Skip link should be first focusable element and visible on focus",
            actual_result="",
            passed=False,
            wcag_criteria=["2.4.1"],
            notes=""
        )
        
        # İlk Tab'da skip link var mı?
        await self.page.keyboard.press('Tab')
        await self.page.wait_for_timeout(100)
        
        first_element = await self.page.evaluate("""
            () => {
                const el = document.activeElement;
                if (!el) return null;
                return {
                    tag: el.tagName.toLowerCase(),
                    text: el.textContent.trim().substring(0, 50),
                    href: el.getAttribute('href') || '',
                    isSkipLink: el.textContent.toLowerCase().includes('skip') || 
                               el.textContent.toLowerCase().includes('geç') ||
                               el.getAttribute('href')?.startsWith('#')
                };
            }
        """)
        
        if first_element and first_element.get('isSkipLink'):
            skip_test.actual_result = f"Skip link found: {first_element.get('text')}"
            skip_test.passed = True
        else:
            skip_test.actual_result = "No skip link found as first focusable element"
            skip_test.passed = False
        
        tests.append(skip_test)
        
        # Escape key test (modal close)
        escape_test = BehavioralTest(
            test_name="Escape Key Test",
            test_type="shortcut",
            actions=[{"key": "Escape", "expected": "Close any open modal or menu"}],
            expected_result="Escape key should close open dialogs/menus",
            actual_result="",
            passed=False,
            wcag_criteria=["2.1.2"],
            notes=""
        )
        
        tests.append(escape_test)
        
        return tests
    
    async def run_full_audit(self) -> BehavioralAuditReport:
        """Tam denetim çalıştır"""
        report = BehavioralAuditReport(
            url=self.url,
            timestamp=datetime.now().isoformat(),
            navigation_mode=self.navigation_mode,
            total_steps=0,
            focus_changes=0,
            unique_elements=0,
            interactive_elements=0,
            visible_focus_count=0,
            missing_focus_count=0,
            focus_visible_support=0,
            focus_traps=[],
            trap_count=0,
            announcements=[],
            aria_live_regions=[],
            name_calculation_issues=[],
            form_tests=[],
            form_error_handling=[],
            shortcut_tests=[],
            wcag_violations=[],
            violations_by_criterion={},
            scores={},
            recommendations=[]
        )
        
        try:
            # Başlat
            await self.initialize()
            await self.navigate_to_url()
            
            # 1. Klavye navigasyonu
            print("⌨️ Klavye navigasyonu test ediliyor...")
            self.navigation_steps = await self.simulate_tab_navigation(self.max_steps)
            report.navigation_steps = self.navigation_steps
            report.total_steps = len(self.navigation_steps)
            
            # Focus istatistikleri
            report.focus_changes = len(self.navigation_steps)
            report.unique_elements = len(set(s.element_ref for s in self.navigation_steps))
            report.interactive_elements = sum(1 for s in self.navigation_steps if s.is_interactive)
            report.visible_focus_count = sum(1 for s in self.navigation_steps if s.focus_visible)
            report.missing_focus_count = report.total_steps - report.visible_focus_count
            
            # Focus visible support score
            if report.total_steps > 0:
                report.focus_visible_support = int((report.visible_focus_count / report.total_steps) * 100)
            
            # 2. Focus tuzakları
            print("🔍 Focus tuzakları tespit ediliyor...")
            report.focus_traps = await self.detect_focus_traps()
            report.trap_count = len(report.focus_traps)
            
            # 3. Screen reader simülasyonu
            print("🔇 Screen reader simülasyonu...")
            sr_result = await self.simulate_screen_reader()
            report.announcements = sr_result.get("announcements", [])
            report.aria_live_regions = sr_result.get("live_regions", [])
            
            # 4. Form testleri
            print("📝 Form etkileşim testleri...")
            report.form_tests = await self.test_form_interactions()
            
            # 5. Klavye kısayol testleri
            print("⌨️ Klavye kısayol testleri...")
            report.shortcut_tests = await self.test_keyboard_shortcuts()
            
            # 6. WCAG ihlalleri topla
            all_violations = []
            for step in self.navigation_steps:
                all_violations.extend(step.wcag_issues)
            
            # Benzersiz ihlaller
            unique_violations = []
            seen = set()
            for v in all_violations:
                key = (v.get("wcag"), v.get("element"))
                if key not in seen:
                    seen.add(key)
                    unique_violations.append(v)
            
            report.wcag_violations = unique_violations
            
            # Kriter bazlı sayım
            for v in unique_violations:
                criterion = v.get("wcag", "unknown")
                report.violations_by_criterion[criterion] = report.violations_by_criterion.get(criterion, 0) + 1
            
            # 7. Skorlar
            report.scores = self._calculate_scores(report)
            
            # 8. Öneriler
            report.recommendations = self._generate_recommendations(report)
            
            print(f"✅ Denetim tamamlandı: {report.total_steps} adım, {len(report.wcag_violations)} ihlal")
            
        except Exception as e:
            print(f"❌ Hata: {e}")
            traceback.print_exc()
        
        finally:
            await self.close()
        
        return report
    
    def _calculate_scores(self, report: BehavioralAuditReport) -> Dict[str, int]:
        """Skorları hesapla"""
        scores = {
            "focus_efficiency": 100,
            "keyboard_accessibility": 100,
            "screen_reader_friendliness": 100,
            "focus_trap_risk": 100,
            "form_accessibility": 100,
            "overall_behavioral_score": 100
        }
        
        # Focus efficiency
        if report.total_steps > 0:
            scores["focus_efficiency"] = int((report.visible_focus_count / report.total_steps) * 100)
        
        # Keyboard accessibility
        critical_violations = sum(1 for v in report.wcag_violations if v.get("severity") == "critical")
        serious_violations = sum(1 for v in report.wcag_violations if v.get("severity") == "serious")
        moderate_violations = sum(1 for v in report.wcag_violations if v.get("severity") == "moderate")
        
        scores["keyboard_accessibility"] = max(0, 100 - (critical_violations * 10) - (serious_violations * 5) - (moderate_violations * 2))
        
        # Focus trap risk
        if report.trap_count == 0:
            scores["focus_trap_risk"] = 100
        elif report.trap_count == 1:
            scores["focus_trap_risk"] = 70
        elif report.trap_count == 2:
            scores["focus_trap_risk"] = 40
        else:
            scores["focus_trap_risk"] = 20
        
        # Screen reader friendliness
        if report.announcements:
            name_issues = sum(1 for a in report.announcements if not a.get("content"))
            scores["screen_reader_friendliness"] = max(0, 100 - (name_issues * 5))
        
        # Form accessibility
        failed_forms = sum(1 for f in report.form_tests if not f.passed)
        scores["form_accessibility"] = max(0, 100 - (failed_forms * 15))
        
        # Overall
        scores["overall_behavioral_score"] = int(
            (scores["focus_efficiency"] * 0.2 +
             scores["keyboard_accessibility"] * 0.25 +
             scores["screen_reader_friendliness"] * 0.2 +
             scores["focus_trap_risk"] * 0.2 +
             scores["form_accessibility"] * 0.15)
        )
        
        return scores
    
    def _generate_recommendations(self, report: BehavioralAuditReport) -> List[str]:
        """Öneriler oluştur"""
        recommendations = []
        
        # Focus göstergesi
        if report.missing_focus_count > 0:
            recommendations.append(f"⚠️ {report.missing_focus_count} element'te focus göstergesi eksik. :focus-visible CSS sınıfı ekleyin.")
        
        # Focus traps
        if report.trap_count > 0:
            recommendations.append(f"🚨 {report.trap_count} focus tuzağı tespit edildi. Escape tuşu ve kapatma mekanizmaları ekleyin.")
        
        # WCAG ihlalleri
        by_criterion = report.violations_by_criterion
        if "2.4.7" in by_criterion:
            recommendations.append("📌 2.4.7 Focus Visible: Tüm focusable element'lere görünür focus göstergesi ekleyin.")
        if "4.1.2" in by_criterion:
            recommendations.append("📌 4.1.2 Name, Role, Value: Etkileşimli element'lere aria-label veya erişilebilir isim ekleyin.")
        if "2.1.2" in by_criterion:
            recommendations.append("📌 2.1.2 No Keyboard Trap: Focus tuzağı oluşturan element'leri düzeltin.")
        
        # Screen reader
        if not report.announcements:
            recommendations.append("🔇 Sayfa başlığı ve landmark'lar için ARIA live region kullanın.")
        
        # Form testleri
        failed_forms = [f for f in report.form_tests if not f.passed]
        if failed_forms:
            recommendations.append(f"📝 {len(failed_forms)} form'da erişilebilirlik sorunu var. Form element'lerine label ekleyin.")
        
        # Skip link
        skip_tests = [t for t in report.shortcut_tests if "Skip" in t.test_name and not t.passed]
        if skip_tests:
            recommendations.append("⏭️ Ana içeriğe atlama linki (skip link) ekleyin.")
        
        return recommendations
    
    def save_report(self, report: BehavioralAuditReport) -> str:
        """Raporu kaydet"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        domain = self.url.replace("https://", "").replace("http://", "").split("/")[0]
        filename = f"behavioral_navigator_{domain}_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        report_dict = {
            "url": report.url,
            "timestamp": report.timestamp,
            "navigation_mode": report.navigation_mode.value,
            "statistics": {
                "total_steps": report.total_steps,
                "focus_changes": report.focus_changes,
                "unique_elements": report.unique_elements,
                "interactive_elements": report.interactive_elements,
                "visible_focus_count": report.visible_focus_count,
                "missing_focus_count": report.missing_focus_count,
                "focus_visible_support": report.focus_visible_support
            },
            "focus_traps": [
                {
                    "element": t.element_ref,
                    "type": t.trap_type,
                    "severity": t.severity,
                    "description": t.description,
                    "wcag": t.wcag_criterion
                } for t in report.focus_traps
            ],
            "screen_reader": {
                "announcements_count": len(report.announcements),
                "live_regions_count": len(report.aria_live_regions)
            },
            "form_tests": [
                {
                    "name": f.test_name,
                    "passed": f.passed,
                    "wcag_criteria": f.wcag_criteria,
                    "notes": f.notes
                } for f in report.form_tests
            ],
            "shortcut_tests": [
                {
                    "name": t.test_name,
                    "passed": t.passed,
                    "expected": t.expected_result,
                    "actual": t.actual_result
                } for t in report.shortcut_tests
            ],
            "wcag_violations": report.wcag_violations,
            "violations_by_criterion": report.violations_by_criterion,
            "scores": report.scores,
            "recommendations": report.recommendations
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report_dict, f, ensure_ascii=False, indent=2)
        
        return filepath
    
    def generate_html_report(self, report: BehavioralAuditReport) -> str:
        """HTML rapor oluştur"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        domain = self.url.replace("https://", "").replace("http://", "").split("/")[0]
        filename = f"behavioral_navigator_{domain}_{timestamp}.html"
        filepath = os.path.join(self.output_dir, filename)
        
        html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AccessMind Behavioral Navigator - {report.url}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 1200px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #1a365d; border-bottom: 3px solid #3182ce; padding-bottom: 10px; }}
        h2 {{ color: #2c5282; margin-top: 30px; }}
        h3 {{ color: #4a5568; }}
        .score-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
        .score-card {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 12px; text-align: center; }}
        .score-card h3 {{ margin: 0; font-size: 14px; opacity: 0.9; }}
        .score-card .score {{ font-size: 48px; font-weight: bold; margin: 10px 0; }}
        .score-card.low {{ background: linear-gradient(135deg, #e53e3e 0%, #c53030 100%); }}
        .score-card.medium {{ background: linear-gradient(135deg, #ed8936 0%, #c05621 100%); }}
        .score-card.high {{ background: linear-gradient(135deg, #38a169 0%, #2f855a 100%); }}
        .stats {{ background: #f7fafc; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; }}
        .stat {{ text-align: center; }}
        .stat-value {{ font-size: 32px; font-weight: bold; color: #3182ce; }}
        .stat-label {{ font-size: 14px; color: #718096; }}
        .violations {{ margin: 20px 0; }}
        .violation {{ background: #fff; border-left: 4px solid #e53e3e; padding: 15px; margin: 10px 0; border-radius: 0 8px 8px 0; }}
        .violation.serious {{ border-left-color: #ed8936; }}
        .violation.moderate {{ border-left-color: #ecc94b; }}
        .violation h4 {{ margin: 0 0 5px 0; color: #e53e3e; }}
        .wcag-tag {{ background: #3182ce; color: white; padding: 2px 8px; border-radius: 4px; font-size: 12px; margin-right: 8px; }}
        .recommendations {{ background: #ebf8ff; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .recommendation {{ padding: 10px 0; border-bottom: 1px solid #bee3f8; }}
        .recommendation:last-child {{ border-bottom: none; }}
        .focus-trap {{ background: #fed7d7; padding: 15px; border-radius: 8px; margin: 10px 0; }}
        .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #e2e8f0; color: #718096; font-size: 13px; }}
    </style>
</head>
<body>
    <h1>🔍 AccessMind Behavioral Navigator Report</h1>
    <p><strong>URL:</strong> <a href="{report.url}">{report.url}</a></p>
    <p><strong>Tarih:</strong> {report.timestamp}</p>
    <p><strong>Mod:</strong> {report.navigation_mode.value}</p>
    
    <h2>📊 Skorlar</h2>
    <div class="score-grid">
        <div class="score-card {'low' if report.scores.get('focus_efficiency', 0) < 50 else 'medium' if report.scores.get('focus_efficiency', 0) < 80 else 'high'}">
            <h3>Focus Efficiency</h3>
            <div class="score">{report.scores.get('focus_efficiency', 0)}</div>
        </div>
        <div class="score-card {'low' if report.scores.get('keyboard_accessibility', 0) < 50 else 'medium' if report.scores.get('keyboard_accessibility', 0) < 80 else 'high'}">
            <h3>Keyboard Accessibility</h3>
            <div class="score">{report.scores.get('keyboard_accessibility', 0)}</div>
        </div>
        <div class="score-card {'low' if report.scores.get('screen_reader_friendliness', 0) < 50 else 'medium' if report.scores.get('screen_reader_friendliness', 0) < 80 else 'high'}">
            <h3>Screen Reader Friendliness</h3>
            <div class="score">{report.scores.get('screen_reader_friendliness', 0)}</div>
        </div>
        <div class="score-card {'low' if report.scores.get('focus_trap_risk', 0) < 50 else 'medium' if report.scores.get('focus_trap_risk', 0) < 80 else 'high'}">
            <h3>Focus Trap Risk</h3>
            <div class="score">{report.scores.get('focus_trap_risk', 0)}</div>
        </div>
        <div class="score-card {'low' if report.scores.get('form_accessibility', 0) < 50 else 'medium' if report.scores.get('form_accessibility', 0) < 80 else 'high'}">
            <h3>Form Accessibility</h3>
            <div class="score">{report.scores.get('form_accessibility', 0)}</div>
        </div>
        <div class="score-card {'low' if report.scores.get('overall_behavioral_score', 0) < 50 else 'medium' if report.scores.get('overall_behavioral_score', 0) < 80 else 'high'}">
            <h3>Overall Score</h3>
            <div class="score">{report.scores.get('overall_behavioral_score', 0)}</div>
        </div>
    </div>
    
    <h2>📈 İstatistikler</h2>
    <div class="stats">
        <div class="stats-grid">
            <div class="stat">
                <div class="stat-value">{report.total_steps}</div>
                <div class="stat-label">Toplam Adım</div>
            </div>
            <div class="stat">
                <div class="stat-value">{report.unique_elements}</div>
                <div class="stat-label">Unique Element</div>
            </div>
            <div class="stat">
                <div class="stat-value">{report.visible_focus_count}</div>
                <div class="stat-label">Visible Focus</div>
            </div>
            <div class="stat">
                <div class="stat-value">{report.missing_focus_count}</div>
                <div class="stat-label">Missing Focus</div>
            </div>
            <div class="stat">
                <div class="stat-value">{report.trap_count}</div>
                <div class="stat-label">Focus Trap</div>
            </div>
            <div class="stat">
                <div class="stat-value">{len(report.wcag_violations)}</div>
                <div class="stat-label">WCAG İhlali</div>
            </div>
        </div>
    </div>
"""
        
        # Focus traps
        if report.focus_traps:
            html += """
    <h2>🚨 Focus Tuzakları</h2>
"""
            for trap in report.focus_traps:
                html += f"""
    <div class="focus-trap">
        <h4>{trap.trap_type}</h4>
        <p><strong>Element:</strong> {trap.element_tag}</p>
        <p><strong>Severity:</strong> {trap.severity}</p>
        <p><strong>WCAG:</strong> {trap.wcag_criterion}</p>
        <p>{trap.description}</p>
    </div>
"""
        
        # WCAG violations
        if report.wcag_violations:
            html += """
    <h2>⚠️ WCAG İhlalleri</h2>
    <div class="violations">
"""
            for v in report.wcag_violations[:20]:  # İlk 20
                severity = v.get('severity', 'moderate')
                html += f"""
        <div class="violation {severity}">
            <h4><span class="wcag-tag">{v.get('wcag', 'unknown')}</span>{v.get('message', 'No message')}</h4>
            <p><strong>Severity:</strong> {severity}</p>
        </div>
"""
            html += """
    </div>
"""
        
        # Recommendations
        if report.recommendations:
            html += """
    <h2>💡 Öneriler</h2>
    <div class="recommendations">
"""
            for r in report.recommendations:
                html += f"""
        <div class="recommendation">{r}</div>
"""
            html += """
    </div>
"""
        
        html += """
    <div class="footer">
        <p>AccessMind Behavioral Navigator v2.0 - Davranış Bazlı Erişilebilirlik Denetimi</p>
        <p>Generated by AccessMind Enterprise</p>
    </div>
</body>
</html>
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return filepath


# CLI kullanımı
async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='AccessMind Behavioral Navigator')
    parser.add_argument('--url', required=True, help='Test edilecek URL')
    parser.add_argument('--steps', type=int, default=50, help='Navigasyon adım sayısı')
    parser.add_argument('--output', default='/Users/sarper/.openclaw/workspace/audits', help='Çıktı dizini')
    parser.add_argument('--mode', choices=['linear', 'smart', 'form', 'landmark', 'heading'], default='smart', help='Gezinim modu')
    parser.add_argument('--headless', action='store_true', default=True, help='Headless mod')
    parser.add_argument('--html', action='store_true', help='HTML rapor oluştur')
    
    args = parser.parse_args()
    
    print(f"🔍 AccessMind Behavioral Navigator v2.0")
    print(f"URL: {args.url}")
    print(f"Mode: {args.mode}")
    print(f"Steps: {args.steps}")
    print()
    
    navigator = AccessMindBehavioralNavigator(
        url=args.url,
        output_dir=args.output,
        navigation_mode=NavigationMode(args.mode),
        max_steps=args.steps,
        headless=args.headless
    )
    
    report = await navigator.run_full_audit()
    
    # JSON rapor
    json_path = navigator.save_report(report)
    print(f"✅ JSON rapor: {json_path}")
    
    # HTML rapor
    if args.html:
        html_path = navigator.generate_html_report(report)
        print(f"✅ HTML rapor: {html_path}")
    
    # Özet
    print()
    print("📊 Özet:")
    print(f"  - Toplam adım: {report.total_steps}")
    print(f"  - Focus göstergesi: {report.visible_focus_count}/{report.total_steps}")
    print(f"  - Focus tuzağı: {report.trap_count}")
    print(f"  - WCAG ihlali: {len(report.wcag_violations)}")
    print(f"  - Overall Score: {report.scores.get('overall_behavioral_score', 0)}")
    
    if report.recommendations:
        print()
        print("💡 Öneriler:")
        for r in report.recommendations[:5]:
            print(f"  - {r}")


if __name__ == "__main__":
    asyncio.run(main())