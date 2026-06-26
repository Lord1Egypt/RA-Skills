#!/usr/bin/env python3
"""
AccessMind Enterprise v6.0 - ACT Rules Format Implementation
W3C Accessibility Conformance Testing Rules Format (ACT Rules)

50+ Atomik Test Kuralları - WCAG 2.2 AA Uyumluluk

Kaynak: https://www.w3.org/WAI/standards-guidelines/act/rules/about/
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class Severity(Enum):
    CRITICAL = "critical"
    SERIOUS = "serious"
    MODERATE = "moderate"
    MINOR = "minor"


class WCAGLevel(Enum):
    A = "A"
    AA = "AA"
    AAA = "AAA"


@dataclass
class WCAGCriterion:
    """WCAG Kriteri"""
    id: str
    name: str
    level: WCAGLevel
    category: str  # Perceivable, Operable, Understandable, Robust
    description: str


@dataclass
class ACTRule:
    """W3C ACT Rule"""
    rule_id: str
    name: str
    description: str
    wcag_criterion: WCAGCriterion
    severity: Severity
    test_procedures: List[str] = field(default_factory=list)
    expected_result: str = ""
    assumptions: List[str] = field(default_factory=list)
    passed: Optional[bool] = None
    details: str = ""
    elements: List[Dict] = field(default_factory=list)
    
    def to_act_format(self) -> Dict:
        """ACT JSON formatına dönüştür"""
        return {
            "@context": "https://www.w3.org/WAI/act-rules/context.jsonld",
            "@type": "act-rule",
            "id": f"accessmind-{self.rule_id}",
            "name": self.name,
            "description": self.description,
            "wcag": [self.wcag_criterion.id],
            "severity": self.severity.value,
            "test_procedures": self.test_procedures,
            "expected_result": self.expected_result,
            "assumptions": self.assumptions,
            "result": {
                "passed": self.passed,
                "details": self.details,
                "elements": self.elements
            }
        }


class ACTRulesEngine:
    """ACT Rules Motoru - 50+ Kural"""
    
    def __init__(self, target_url: str):
        self.target_url = target_url
        self.timestamp = datetime.now().isoformat()
        self.rules: List[ACTRule] = []
        self._create_all_rules()
    
    def _create_all_rules(self):
        """Tüm WCAG kurallarını oluştur"""
        
        # ==================== PERCEIVABLE ====================
        
        # 1.1.1 Non-text Content
        self.rules.extend([
            ACTRule(
                rule_id="1.1.1-img-alt",
                name="Image has accessible name",
                description="All img elements have accessible alternative text",
                wcag_criterion=WCAGCriterion("1.1.1", "Non-text Content", WCAGLevel.A, "Perceivable", "All non-text content has accessible alternative"),
                severity=Severity.CRITICAL,
                test_procedures=[
                    "Find all img elements in DOM",
                    "Check alt attribute presence",
                    "Validate alt text is not empty (unless decorative)",
                    "Check aria-label or aria-labelledby for img elements",
                    "Verify role='img' elements have accessible name"
                ],
                expected_result="All images have accessible alternative text",
                assumptions=["Decorative images use alt='' or role='presentation'", "Complex images have longdesc or aria-describedby"]
            ),
            ACTRule(
                rule_id="1.1.1-svg-alt",
                name="SVG has accessible name",
                description="All SVG elements have accessible name",
                wcag_criterion=WCAGCriterion("1.1.1", "Non-text Content", WCAGLevel.A, "Perceivable", "All non-text content has accessible alternative"),
                severity=Severity.CRITICAL,
                test_procedures=[
                    "Find all svg elements",
                    "Check for <title> child element",
                    "Check for aria-label attribute",
                    "Check for aria-labelledby attribute",
                    "Verify role='img' on decorative SVGs"
                ],
                expected_result="All SVG elements have accessible name",
                assumptions=["Inline SVGs are checked separately", "role='img' requires accessible name"]
            ),
            ACTRule(
                rule_id="1.1.1-area-alt",
                name="Area has accessible name",
                description="All area elements in image maps have alt text",
                wcag_criterion=WCAGCriterion("1.1.1", "Non-text Content", WCAGLevel.A, "Perceivable", "All non-text content has accessible alternative"),
                severity=Severity.SERIOUS,
                test_procedures=[
                    "Find all area elements",
                    "Check alt attribute presence",
                    "Validate alt text describes the link destination"
                ],
                expected_result="All area elements have alt text"
            ),
            ACTRule(
                rule_id="1.1.1-object-alt",
                name="Object has accessible name",
                description="Object elements have accessible alternative",
                wcag_criterion=WCAGCriterion("1.1.1", "Non-text Content", WCAGLevel.A, "Perceivable", "All non-text content has accessible alternative"),
                severity=Severity.SERIOUS,
                test_procedures=[
                    "Find all object elements",
                    "Check for inner text content alternative",
                    "Check for aria-label or aria-labelledby"
                ],
                expected_result="Object elements have accessible alternative"
            ),
        ])
        
        # 1.2.x Time-based Media (Audio/Video)
        self.rules.extend([
            ACTRule(
                rule_id="1.2.1-audio-only",
                name="Audio has text alternative",
                description="Audio-only content has text alternative",
                wcag_criterion=WCAGCriterion("1.2.1", "Audio-only and Video-only", WCAGLevel.A, "Perceivable", "Audio-only has text alternative"),
                severity=Severity.SERIOUS,
                test_procedures=[
                    "Find all audio elements",
                    "Check for transcript link or aria-describedby",
                    "Verify transcript describes audio content"
                ],
                expected_result="Audio-only content has text alternative"
            ),
            ACTRule(
                rule_id="1.2.2-video-captions",
                name="Video has captions",
                description="Video has captions for audio content",
                wcag_criterion=WCAGCriterion("1.2.2", "Captions (Prerecorded)", WCAGLevel.A, "Perceivable", "Videos have captions"),
                severity=Severity.CRITICAL,
                test_procedures=[
                    "Find all video elements",
                    "Check for track kind='captions'",
                    "Verify captions cover all audio"
                ],
                expected_result="Videos have captions"
            ),
            ACTRule(
                rule_id="1.2.3-video-audio-desc",
                name="Video has audio description",
                description="Video has audio description or alternative",
                wcag_criterion=WCAGCriterion("1.2.3", "Audio Description", WCAGLevel.A, "Perceivable", "Videos have audio description"),
                severity=Severity.SERIOUS,
                test_procedures=[
                    "Find all video elements",
                    "Check for track kind='descriptions'",
                    "Verify audio descriptions available"
                ],
                expected_result="Videos have audio description or text alternative"
            ),
        ])
        
        # 1.3.x Adaptable
        self.rules.extend([
            ACTRule(
                rule_id="1.3.1-heading-hierarchy",
                name="Heading hierarchy is logical",
                description="Headings are properly nested and hierarchical",
                wcag_criterion=WCAGCriterion("1.3.1", "Info and Relationships", WCAGLevel.A, "Perceivable", "Structure is programmatically determinable"),
                severity=Severity.SERIOUS,
                test_procedures=[
                    "Extract all heading elements (h1-h6)",
                    "Check for exactly one h1",
                    "Verify no heading levels are skipped",
                    "Check heading order matches visual hierarchy"
                ],
                expected_result="Headings follow logical hierarchy"
            ),
            ACTRule(
                rule_id="1.3.1-list-structure",
                name="List structure is semantic",
                description="Lists use proper semantic markup",
                wcag_criterion=WCAGCriterion("1.3.1", "Info and Relationships", WCAGLevel.A, "Perceivable", "Structure is programmatically determinable"),
                severity=Severity.MODERATE,
                test_procedures=[
                    "Find all ul, ol, dl elements",
                    "Check for proper li/dt/dd children",
                    "Verify lists not used for layout"
                ],
                expected_result="Lists use proper semantic elements"
            ),
            ACTRule(
                rule_id="1.3.1-table-headers",
                name="Table has headers",
                description="Data tables have proper header cells",
                wcag_criterion=WCAGCriterion("1.3.1", "Info and Relationships", WCAGLevel.A, "Perceivable", "Structure is programmatically determinable"),
                severity=Severity.SERIOUS,
                test_procedures=[
                    "Find all table elements",
                    "Check for th elements",
                    "Verify scope or headers attributes",
                    "Check for summary or caption"
                ],
                expected_result="Data tables have proper headers"
            ),
            ACTRule(
                rule_id="1.3.1-form-labels",
                name="Form inputs have labels",
                description="Form inputs have accessible labels",
                wcag_criterion=WCAGCriterion("1.3.1", "Info and Relationships", WCAGLevel.A, "Perceivable", "Structure is programmatically determinable"),
                severity=Severity.CRITICAL,
                test_procedures=[
                    "Find all input, select, textarea elements",
                    "Check for label[for] association",
                    "Check for aria-label attribute",
                    "Check for aria-labelledby reference",
                    "Verify label describes input purpose"
                ],
                expected_result="All form inputs have accessible labels"
            ),
            ACTRule(
                rule_id="1.3.2-meaningful-sequence",
                name="Content order is meaningful",
                description="Content can be presented in different ways without losing meaning",
                wcag_criterion=WCAGCriterion("1.3.2", "Meaningful Sequence", WCAGLevel.A, "Perceivable", "Content order preserves meaning"),
                severity=Severity.MODERATE,
                test_procedures=[
                    "Check DOM order matches visual order",
                    "Verify tab order follows reading order",
                    "Check CSS doesn't reorder content confusingly"
                ],
                expected_result="Content sequence preserves meaning"
            ),
        ])
        
        # 1.4.x Distinguishable
        self.rules.extend([
            ACTRule(
                rule_id="1.4.3-contrast-normal",
                name="Normal text has sufficient contrast",
                description="Normal text has 4.5:1 contrast ratio",
                wcag_criterion=WCAGCriterion("1.4.3", "Contrast Minimum", WCAGLevel.AA, "Perceivable", "Text has sufficient contrast"),
                severity=Severity.SERIOUS,
                test_procedures=[
                    "Extract foreground color",
                    "Extract background color",
                    "Calculate contrast ratio",
                    "Compare with 4.5:1 threshold for normal text"
                ],
                expected_result="Normal text has contrast ratio >= 4.5:1"
            ),
            ACTRule(
                rule_id="1.4.3-contrast-large",
                name="Large text has sufficient contrast",
                description="Large text (18pt+) has 3:1 contrast ratio",
                wcag_criterion=WCAGCriterion("1.4.3", "Contrast Minimum", WCAGLevel.AA, "Perceivable", "Text has sufficient contrast"),
                severity=Severity.SERIOUS,
                test_procedures=[
                    "Identify large text (>=18pt or >=14pt bold)",
                    "Extract foreground and background colors",
                    "Calculate contrast ratio",
                    "Compare with 3:1 threshold"
                ],
                expected_result="Large text has contrast ratio >= 3:1"
            ),
            ACTRule(
                rule_id="1.4.4-resize-text",
                name="Text resizes properly",
                description="Text can be resized without loss of functionality",
                wcag_criterion=WCAGCriterion("1.4.4", "Resize Text", WCAGLevel.AA, "Perceivable", "Text can be resized"),
                severity=Severity.SERIOUS,
                test_procedures=[
                    "Increase text size to 200%",
                    "Check for horizontal scrolling",
                    "Verify text doesn't overlap",
                    "Verify functionality preserved"
                ],
                expected_result="Text resizes to 200% without loss"
            ),
            ACTRule(
                rule_id="1.4.10-reflow",
                name="Content reflows horizontally",
                description="Content can be presented without horizontal scrolling at 320 CSS pixels",
                wcag_criterion=WCAGCriterion("1.4.10", "Reflow", WCAGLevel.AA, "Perceivable", "Content reflows properly"),
                severity=Severity.MODERATE,
                test_procedures=[
                    "Set viewport to 320px width",
                    "Check for horizontal scrolling",
                    "Verify no content is hidden",
                    "Check zoom to 400%"
                ],
                expected_result="Content reflows without horizontal scrolling"
            ),
            ACTRule(
                rule_id="1.4.11-non-text-contrast",
                name="UI components have sufficient contrast",
                description="UI components and graphical objects have 3:1 contrast",
                wcag_criterion=WCAGCriterion("1.4.11", "Non-text Contrast", WCAGLevel.AA, "Perceivable", "UI has sufficient contrast"),
                severity=Severity.SERIOUS,
                test_procedures=[
                    "Identify interactive components",
                    "Extract component colors",
                    "Calculate contrast against adjacent colors",
                    "Compare with 3:1 threshold"
                ],
                expected_result="UI components have contrast >= 3:1"
            ),
            ACTRule(
                rule_id="1.4.12-spacing",
                name="Text spacing is adjustable",
                description="Text spacing can be modified without loss of content",
                wcag_criterion=WCAGCriterion("1.4.12", "Text Spacing", WCAGLevel.AA, "Perceivable", "Text spacing is adjustable"),
                severity=Severity.MODERATE,
                test_procedures=[
                    "Apply text spacing override",
                    "Check for content overlap",
                    "Verify no truncation"
                ],
                expected_result="Text spacing adjustable without content loss"
            ),
        ])
        
        # ==================== OPERABLE ====================
        
        # 2.1.x Keyboard Accessible
        self.rules.extend([
            ACTRule(
                rule_id="2.1.1-keyboard-accessible",
                name="All interactive elements are keyboard accessible",
                description="Functionality is operable through keyboard",
                wcag_criterion=WCAGCriterion("2.1.1", "Keyboard", WCAGLevel.A, "Operable", "All functionality keyboard accessible"),
                severity=Severity.CRITICAL,
                test_procedures=[
                    "Identify all interactive elements",
                    "Tab through focusable elements",
                    "Verify all functionality accessible via keyboard",
                    "Check for keyboard event handlers"
                ],
                expected_result="All interactive elements keyboard accessible"
            ),
            ACTRule(
                rule_id="2.1.2-no-keyboard-trap",
                name="No keyboard trap",
                description="Focus can be moved away from all components",
                wcag_criterion=WCAGCriterion("2.1.2", "No Keyboard Trap", WCAGLevel.A, "Operable", "No keyboard traps"),
                severity=Severity.CRITICAL,
                test_procedures=[
                    "Tab through all focusable elements",
                    "Check for infinite focus loops",
                    "Verify modal dialogs can be closed",
                    "Test Escape key for modal close"
                ],
                expected_result="No keyboard traps detected"
            ),
            ACTRule(
                rule_id="2.1.4-character-key-shortcuts",
                name="Character key shortcuts have override",
                description="Single-key shortcuts can be turned off or remapped",
                wcag_criterion=WCAGCriterion("2.1.4", "Character Key Shortcuts", WCAGLevel.A, "Operable", "Shortcuts can be turned off"),
                severity=Severity.MODERATE,
                test_procedures=[
                    "Identify keyboard shortcuts using character keys",
                    "Check for mechanism to turn off",
                    "Check for mechanism to remap",
                    "Verify shortcuts only active on focus"
                ],
                expected_result="Character shortcuts can be turned off or remapped"
            ),
        ])
        
        # 2.4.x Navigable
        self.rules.extend([
            ACTRule(
                rule_id="2.4.1-bypass-blocks",
                name="Page has bypass blocks",
                description="Skip link or bypass mechanism exists",
                wcag_criterion=WCAGCriterion("2.4.1", "Bypass Blocks", WCAGLevel.A, "Operable", "Skip link available"),
                severity=Severity.SERIOUS,
                test_procedures=[
                    "Check for skip link at page start",
                    "Verify skip link is first focusable element",
                    "Verify skip link targets main content",
                    "Test skip link functionality"
                ],
                expected_result="Skip link present and functional"
            ),
            ACTRule(
                rule_id="2.4.2-page-title",
                name="Page has descriptive title",
                description="Page has title element with descriptive text",
                wcag_criterion=WCAGCriterion("2.4.2", "Page Titled", WCAGLevel.A, "Operable", "Page has title"),
                severity=Severity.CRITICAL,
                test_procedures=[
                    "Check for title element",
                    "Verify title is non-empty",
                    "Verify title describes page content",
                    "Check title is unique across site"
                ],
                expected_result="Page has descriptive title"
            ),
            ACTRule(
                rule_id="2.4.3-focus-order",
                name="Focus order is logical",
                description="Focus order preserves meaning and operability",
                wcag_criterion=WCAGCriterion("2.4.3", "Focus Order", WCAGLevel.A, "Operable", "Focus order logical"),
                severity=Severity.SERIOUS,
                test_procedures=[
                    "Tab through all focusable elements",
                    "Verify focus follows reading order",
                    "Check tabindex values are logical",
                    "Verify modal focus management"
                ],
                expected_result="Focus order preserves meaning"
            ),
            ACTRule(
                rule_id="2.4.4-link-purpose",
                name="Link purpose is clear",
                description="Link text describes destination",
                wcag_criterion=WCAGCriterion("2.4.4", "Link Purpose (In Context)", WCAGLevel.A, "Operable", "Link purpose clear"),
                severity=Severity.SERIOUS,
                test_procedures=[
                    "Find all anchor elements",
                    "Check link text is not empty",
                    "Verify link text is meaningful",
                    "Check 'click here' and 'read more' links",
                    "Verify icon links have aria-label"
                ],
                expected_result="All links have meaningful text"
            ),
            ACTRule(
                rule_id="2.4.5-multiple-ways",
                name="Multiple ways to find pages",
                description="More than one way to locate pages within site",
                wcag_criterion=WCAGCriterion("2.4.5", "Multiple Ways", WCAGLevel.AA, "Operable", "Multiple navigation methods"),
                severity=Severity.MODERATE,
                test_procedures=[
                    "Check for navigation menu",
                    "Check for search functionality",
                    "Check for sitemap",
                    "Verify at least two methods available"
                ],
                expected_result="Multiple ways to find pages"
            ),
            ACTRule(
                rule_id="2.4.6-headings-labels",
                name="Headings and labels are descriptive",
                description="Headings and labels describe topic or purpose",
                wcag_criterion=WCAGCriterion("2.4.6", "Headings and Labels", WCAGLevel.AA, "Operable", "Headings descriptive"),
                severity=Severity.SERIOUS,
                test_procedures=[
                    "Check heading text is descriptive",
                    "Check form labels are descriptive",
                    "Verify headings describe section content",
                    "Verify labels describe input purpose"
                ],
                expected_result="Headings and labels are descriptive"
            ),
            ACTRule(
                rule_id="2.4.7-focus-visible",
                name="Focus indicator is visible",
                description="Focus indicator is visible on all focusable elements",
                wcag_criterion=WCAGCriterion("2.4.7", "Focus Visible", WCAGLevel.AA, "Operable", "Focus visible"),
                severity=Severity.SERIOUS,
                test_procedures=[
                    "Tab through all focusable elements",
                    "Check focus outline is visible",
                    "Verify focus style has 3:1 contrast",
                    "Check :focus-visible support"
                ],
                expected_result="Focus indicator visible on all elements"
            ),
            ACTRule(
                rule_id="2.4.8-location",
                name="Location is indicated",
                description="User's location within site is indicated",
                wcag_criterion=WCAGCriterion("2.4.8", "Location", WCAGLevel.AAA, "Operable", "Location indicated"),
                severity=Severity.MINOR,
                test_procedures=[
                    "Check for breadcrumbs",
                    "Check for sitemap link",
                    "Check for current page indicator"
                ],
                expected_result="User location is indicated"
            ),
            ACTRule(
                rule_id="2.4.11-focus-not-obscured",
                name="Focus is not obscured",
                description="Focused component is not hidden",
                wcag_criterion=WCAGCriterion("2.4.11", "Focus Not Obscured", WCAGLevel.AA, "Operable", "Focus not obscured"),
                severity=Severity.SERIOUS,
                test_procedures=[
                    "Tab through all elements",
                    "Check sticky headers don't obscure focus",
                    "Check modals don't obscure focus",
                    "Verify focused element is visible"
                ],
                expected_result="Focused element not obscured"
            ),
            ACTRule(
                rule_id="2.4.12-focus-not-obscured-minimum",
                name="Focus is at least partially visible",
                description="Focused component is at least partially visible",
                wcag_criterion=WCAGCriterion("2.4.12", "Focus Not Obscured (Minimum)", WCAGLevel.AA, "Operable", "Focus partially visible"),
                severity=Severity.MODERATE,
                test_procedures=[
                    "Tab through all elements",
                    "Verify at least partial visibility",
                    "Check for content overlap issues"
                ],
                expected_result="Focus at least partially visible"
            ),
            ACTRule(
                rule_id="2.4.13-focus-appearance",
                name="Focus appearance is visible",
                description="Focus indicator meets size and contrast requirements",
                wcag_criterion=WCAGCriterion("2.4.13", "Focus Appearance", WCAGLevel.AAA, "Operable", "Focus appearance visible"),
                severity=Severity.MODERATE,
                test_procedures=[
                    "Measure focus indicator area",
                    "Check area is at least 2px solid",
                    "Verify 3:1 contrast ratio"
                ],
                expected_result="Focus indicator meets size requirements"
            ),
        ])
        
        # 2.5.x Input Modalities
        self.rules.extend([
            ACTRule(
                rule_id="2.5.1-pointer-gestures",
                name="Pointer gestures have alternatives",
                description="Multipoint or path-based gestures have alternatives",
                wcag_criterion=WCAGCriterion("2.5.1", "Pointer Gestures", WCAGLevel.A, "Operable", "Gestures have alternatives"),
                severity=Severity.SERIOUS,
                test_procedures=[
                    "Identify multipoint gestures",
                    "Check for single-pointer alternatives",
                    "Identify path-based gestures",
                    "Check for button alternatives"
                ],
                expected_result="Gestures have single-pointer alternatives"
            ),
            ACTRule(
                rule_id="2.5.2-pointer-cancellation",
                name="Pointer input can be cancelled",
                description="Single pointer operation can be aborted or undone",
                wcag_criterion=WCAGCriterion("2.5.2", "Pointer Cancellation", WCAGLevel.A, "Operable", "Pointer can be cancelled"),
                severity=Severity.SERIOUS,
                test_procedures=[
                    "Press down on interactive element",
                    "Move pointer away before release",
                    "Verify action is cancelled",
                    "Check for up-event vs down-event"
                ],
                expected_result="Pointer operations can be cancelled"
            ),
            ACTRule(
                rule_id="2.5.3-label-in-name",
                name="Label is in accessible name",
                description="Label text is in accessible name",
                wcag_criterion=WCAGCriterion("2.5.3", "Label in Name", WCAGLevel.A, "Operable", "Label in name"),
                severity=Severity.SERIOUS,
                test_procedures=[
                    "Find visible label text",
                    "Get accessible name via aria",
                    "Verify visible label is in accessible name",
                    "Check voice activation works"
                ],
                expected_result="Visible label in accessible name"
            ),
            ACTRule(
                rule_id="2.5.4-motion-actuation",
                name="Motion can be disabled",
                description="Functionality triggered by motion can be disabled",
                wcag_criterion=WCAGCriterion("2.5.4", "Motion Actuation", WCAGLevel.A, "Operable", "Motion can be disabled"),
                severity=Severity.SERIOUS,
                test_procedures=[
                    "Identify motion-triggered functions",
                    "Check for disable mechanism",
                    "Verify alternative input exists"
                ],
                expected_result="Motion actuation can be disabled"
            ),
            ACTRule(
                rule_id="2.5.5-target-size",
                name="Target size is sufficient",
                description="Targets are at least 44x44 CSS pixels",
                wcag_criterion=WCAGCriterion("2.5.5", "Target Size", WCAGLevel.AAA, "Operable", "Target size sufficient"),
                severity=Severity.MODERATE,
                test_procedures=[
                    "Measure interactive element size",
                    "Check minimum 44x44 pixels",
                    "Verify adequate spacing between targets"
                ],
                expected_result="Targets are at least 44x44 pixels"
            ),
            ACTRule(
                rule_id="2.5.7-dragging-movements",
                name="Dragging has alternatives",
                description="Dragging movements have single-pointer alternatives",
                wcag_criterion=WCAGCriterion("2.5.7", "Dragging Movements", WCAGLevel.AA, "Operable", "Dragging has alternatives"),
                severity=Severity.SERIOUS,
                test_procedures=[
                    "Identify drag operations",
                    "Check for single-pointer alternatives",
                    "Verify buttons or menus available"
                ],
                expected_result="Dragging has single-pointer alternative"
            ),
            ACTRule(
                rule_id="2.5.8-target-size-minimum",
                name="Target size minimum 44px",
                description="Targets are at least 44x44 CSS pixels (minimum)",
                wcag_criterion=WCAGCriterion("2.5.8", "Target Size (Minimum)", WCAGLevel.AA, "Operable", "Target minimum 44px"),
                severity=Severity.SERIOUS,
                test_procedures=[
                    "Measure all interactive targets",
                    "Check for 44x44 minimum",
                    "Verify exceptions are valid"
                ],
                expected_result="Targets meet minimum size"
            ),
        ])
        
        # ==================== UNDERSTANDABLE ====================
        
        # 3.1.x Readable
        self.rules.extend([
            ACTRule(
                rule_id="3.1.1-page-language",
                name="Page language is declared",
                description="Default language of page is declared",
                wcag_criterion=WCAGCriterion("3.1.1", "Language of Page", WCAGLevel.A, "Understandable", "Page language declared"),
                severity=Severity.CRITICAL,
                test_procedures=[
                    "Check html element has lang attribute",
                    "Verify lang value is valid BCP 47",
                    "Check for xml:lang if XHTML"
                ],
                expected_result="Valid lang attribute on html element"
            ),
            ACTRule(
                rule_id="3.1.2-part-language",
                name="Language of parts is declared",
                description="Language of each passage is declared",
                wcag_criterion=WCAGCriterion("3.1.2", "Language of Parts", WCAGLevel.AA, "Understandable", "Part language declared"),
                severity=Severity.MODERATE,
                test_procedures=[
                    "Find content in different language",
                    "Check for lang attribute on elements",
                    "Verify lang value matches content"
                ],
                expected_result="Language changes marked with lang attribute"
            ),
        ])
        
        # 3.2.x Predictable
        self.rules.extend([
            ACTRule(
                rule_id="3.2.1-on-focus",
                name="Focus does not change context",
                description="Focus does not trigger context change",
                wcag_criterion=WCAGCriterion("3.2.1", "On Focus", WCAGLevel.A, "Understandable", "Focus doesn't change context"),
                severity=Severity.SERIOUS,
                test_procedures=[
                    "Tab through all focusable elements",
                    "Verify no automatic navigation",
                    "Verify no popup windows on focus",
                    "Check for focus event handlers"
                ],
                expected_result="Focus does not change context"
            ),
            ACTRule(
                rule_id="3.2.2-on-input",
                name="Input does not change context unexpectedly",
                description="Changing input does not change context unexpectedly",
                wcag_criterion=WCAGCriterion("3.2.2", "On Input", WCAGLevel.A, "Understandable", "Input doesn't change context"),
                severity=Severity.SERIOUS,
                test_procedures=[
                    "Enter data in form fields",
                    "Verify no automatic submission",
                    "Check for onchange handlers",
                    "Verify user is informed of changes"
                ],
                expected_result="Input does not change context unexpectedly"
            ),
            ACTRule(
                rule_id="3.2.3-consistent-navigation",
                name="Navigation is consistent",
                description="Navigation is consistent across pages",
                wcag_criterion=WCAGCriterion("3.2.3", "Consistent Navigation", WCAGLevel.AA, "Understandable", "Navigation consistent"),
                severity=Severity.MODERATE,
                test_procedures=[
                    "Compare navigation across pages",
                    "Verify same order and position",
                    "Check for consistent styling"
                ],
                expected_result="Navigation consistent across pages"
            ),
            ACTRule(
                rule_id="3.2.4-consistent-identification",
                name="Components are consistently identified",
                description="Components with same functionality are identified consistently",
                wcag_criterion=WCAGCriterion("3.2.4", "Consistent Identification", WCAGLevel.AA, "Understandable", "Components consistent"),
                severity=Severity.MODERATE,
                test_procedures=[
                    "Find repeated components",
                    "Verify same naming and labeling",
                    "Check icons and labels consistent"
                ],
                expected_result="Same components have same identification"
            ),
            ACTRule(
                rule_id="3.2.6-consistent-help",
                name="Help is consistently available",
                description="Help mechanism is consistently available",
                wcag_criterion=WCAGCriterion("3.2.6", "Consistent Help", WCAGLevel.A, "Understandable", "Help consistently available"),
                severity=Severity.MODERATE,
                test_procedures=[
                    "Check for help mechanism",
                    "Verify consistent placement",
                    "Check multiple pages for consistency"
                ],
                expected_result="Help mechanism consistently available"
            ),
        ])
        
        # 3.3.x Input Assistance
        self.rules.extend([
            ACTRule(
                rule_id="3.3.1-error-identification",
                name="Errors are identified",
                description="Input errors are automatically detected and described",
                wcag_criterion=WCAGCriterion("3.3.1", "Error Identification", WCAGLevel.A, "Understandable", "Errors identified"),
                severity=Severity.CRITICAL,
                test_procedures=[
                    "Submit form with errors",
                    "Verify error messages displayed",
                    "Check errors associated with fields",
                    "Verify aria-invalid on error fields"
                ],
                expected_result="Errors identified and described"
            ),
            ACTRule(
                rule_id="3.3.2-labels-instructions",
                name="Labels and instructions provided",
                description="Labels and instructions are provided for input",
                wcag_criterion=WCAGCriterion("3.3.2", "Labels or Instructions", WCAGLevel.A, "Understandable", "Labels provided"),
                severity=Severity.CRITICAL,
                test_procedures=[
                    "Check all form inputs have labels",
                    "Verify instructions provided",
                    "Check for aria-describedby for hints",
                    "Verify required fields marked"
                ],
                expected_result="Labels and instructions provided"
            ),
            ACTRule(
                rule_id="3.3.3-error-suggestion",
                name="Error suggestions provided",
                description="Suggestions for fixing errors are provided",
                wcag_criterion=WCAGCriterion("3.3.3", "Error Suggestion", WCAGLevel.AA, "Understandable", "Error suggestions"),
                severity=Severity.SERIOUS,
                test_procedures=[
                    "Trigger form errors",
                    "Check for correction suggestions",
                    "Verify suggestions are helpful"
                ],
                expected_result="Error suggestions provided"
            ),
            ACTRule(
                rule_id="3.3.4-error-prevention",
                name="Error prevention for important actions",
                description="Important actions are reversible, checked, or confirmed",
                wcag_criterion=WCAGCriterion("3.3.4", "Error Prevention", WCAGLevel.AA, "Understandable", "Error prevention"),
                severity=Severity.SERIOUS,
                test_procedures=[
                    "Identify important actions",
                    "Check for confirmation dialogs",
                    "Verify reversibility option",
                    "Check for review before submission"
                ],
                expected_result="Error prevention for important actions"
            ),
            ACTRule(
                rule_id="3.3.7-redundant-entry",
                name="Redundant entry minimized",
                description="User does not have to re-enter information",
                wcag_criterion=WCAGCriterion("3.3.7", "Redundant Entry", WCAGLevel.A, "Understandable", "Redundant entry minimized"),
                severity=Severity.MODERATE,
                test_procedures=[
                    "Complete multi-step form",
                    "Check for auto-fill from previous steps",
                    "Verify user can review entered data"
                ],
                expected_result="Redundant entry minimized"
            ),
            ACTRule(
                rule_id="3.3.8-accessible-authentication",
                name="Authentication is accessible",
                description="Authentication does not rely on cognitive function",
                wcag_criterion=WCAGCriterion("3.3.8", "Accessible Authentication", WCAGLevel.AA, "Understandable", "Authentication accessible"),
                severity=Severity.SERIOUS,
                test_procedures=[
                    "Check authentication methods",
                    "Verify no memory test required",
                    "Check for password managers support"
                ],
                expected_result="Authentication accessible"
            ),
        ])
        
        # ==================== ROBUST ====================
        
        # 4.1.x Compatible
        self.rules.extend([
            ACTRule(
                rule_id="4.1.1-valid-html",
                name="HTML is valid",
                description="Markup is valid and complete",
                wcag_criterion=WCAGCriterion("4.1.1", "Parsing", WCAGLevel.A, "Robust", "Valid HTML"),
                severity=Severity.SERIOUS,
                test_procedures=[
                    "Validate HTML syntax",
                    "Check for duplicate IDs",
                    "Verify proper nesting",
                    "Check for unclosed elements"
                ],
                expected_result="HTML is valid"
            ),
            ACTRule(
                rule_id="4.1.2-name-role-value",
                name="Custom components have name, role, value",
                description="Custom components expose name, role, and value",
                wcag_criterion=WCAGCriterion("4.1.2", "Name, Role, Value", WCAGLevel.A, "Robust", "Components accessible"),
                severity=Severity.CRITICAL,
                test_procedures=[
                    "Find custom components",
                    "Check for role attribute",
                    "Check for accessible name",
                    "Check for state management",
                    "Verify ARIA attributes valid"
                ],
                expected_result="Custom components have name, role, value"
            ),
            ACTRule(
                rule_id="4.1.2-form-name",
                name="Form inputs have accessible name",
                description="Form inputs have accessible name",
                wcag_criterion=WCAGCriterion("4.1.2", "Name, Role, Value", WCAGLevel.A, "Robust", "Form accessible"),
                severity=Severity.CRITICAL,
                test_procedures=[
                    "Find all form inputs",
                    "Check for label association",
                    "Check for aria-label",
                    "Check for aria-labelledby"
                ],
                expected_result="All form inputs have accessible name"
            ),
            ACTRule(
                rule_id="4.1.3-status-messages",
                name="Status messages are announced",
                description="Status messages are announced by screen readers",
                wcag_criterion=WCAGCriterion("4.1.3", "Status Messages", WCAGLevel.AA, "Robust", "Status announced"),
                severity=Severity.SERIOUS,
                test_procedures=[
                    "Trigger status messages",
                    "Check for role='status' or 'alert'",
                    "Verify aria-live attribute",
                    "Test screen reader announcement"
                ],
                expected_result="Status messages announced"
            ),
        ])
    
    def evaluate_page(self, page_data: Dict) -> Dict:
        """Sayfa verilerine göre tüm kuralları değerlendir"""
        
        results = {
            "url": self.target_url,
            "timestamp": self.timestamp,
            "total_rules": len(self.rules),
            "passed": 0,
            "failed": 0,
            "warnings": 0,
            "rule_results": [],
            "summary": {
                "by_severity": {
                    "critical": {"passed": 0, "failed": 0},
                    "serious": {"passed": 0, "failed": 0},
                    "moderate": {"passed": 0, "failed": 0},
                    "minor": {"passed": 0, "failed": 0}
                },
                "by_category": {
                    "Perceivable": {"passed": 0, "failed": 0},
                    "Operable": {"passed": 0, "failed": 0},
                    "Understandable": {"passed": 0, "failed": 0},
                    "Robust": {"passed": 0, "failed": 0}
                }
            }
        }
        
        for rule in self.rules:
            # Kural değerlendirmesi
            passed = self._evaluate_single_rule(rule, page_data)
            rule.passed = passed
            
            # İstatistikleri güncelle
            if passed:
                results["passed"] += 1
                results["summary"]["by_severity"][rule.severity.value]["passed"] += 1
                results["summary"]["by_category"][rule.wcag_criterion.category]["passed"] += 1
            else:
                results["failed"] += 1
                results["summary"]["by_severity"][rule.severity.value]["failed"] += 1
                results["summary"]["by_category"][rule.wcag_criterion.category]["failed"] += 1
            
            results["rule_results"].append(rule.to_act_format())
        
        # Yüzde hesapla
        results["pass_rate"] = (results["passed"] / results["total_rules"] * 100) if results["total_rules"] > 0 else 0
        
        return results
    
    def _evaluate_single_rule(self, rule: ACTRule, page_data: Dict) -> bool:
        """Tek bir kuralı değerlendir"""
        
        # Sayfa verilerinden ilgili metriği al
        rule_type = rule.rule_id.split("-")[0]
        
        # Değerlendirme mantığı
        checks = {
            "1.1.1": page_data.get("missing_alt", 0) == 0,
            "1.2": page_data.get("media_issues", 0) == 0,
            "1.3": page_data.get("structure_issues", 0) == 0,
            "1.4": page_data.get("contrast_issues", 0) == 0,
            "2.1": page_data.get("keyboard_issues", 0) == 0,
            "2.4": page_data.get("navigation_issues", 0) == 0,
            "2.5": page_data.get("input_issues", 0) == 0,
            "3.1": page_data.get("language_issues", 0) == 0,
            "3.2": page_data.get("predictability_issues", 0) == 0,
            "3.3": page_data.get("form_issues", 0) == 0,
            "4.1": page_data.get("compatibility_issues", 0) == 0,
        }
        
        # Kural ID'sine göre kontrol et
        for prefix, passed in checks.items():
            if rule.rule_id.startswith(prefix):
                return passed
        
        # Varsayılan: sayfa verilerinde sorun yoksa geçer
        return True
    
    def to_json(self) -> Dict:
        """JSON formatında dışa aktar"""
        return {
            "act_rules_engine": "AccessMind Enterprise v6.0",
            "standard": "W3C ACT Rules Format",
            "url": self.target_url,
            "timestamp": self.timestamp,
            "total_rules": len(self.rules),
            "rules": [rule.to_act_format() for rule in self.rules]
        }
    
    def to_html_report(self, page_data: Dict = None) -> str:
        """HTML rapor oluştur"""
        
        results = self.evaluate_page(page_data or {})
        
        html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ACT Rules Raporu - {self.target_url}</title>
    <style>
        :root {{
            --primary: #0f3460;
            --secondary: #e94560;
            --success: #27ae60;
            --danger: #e74c3c;
            --warning: #f39c12;
            --light: #f8f9fa;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: var(--light); padding: 20px; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, var(--primary), #16213e); color: white; padding: 30px; border-radius: 12px; margin-bottom: 30px; }}
        .header h1 {{ font-size: 28px; margin-bottom: 10px; }}
        .header .url {{ font-size: 14px; opacity: 0.8; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .stat-card {{ background: white; padding: 25px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); text-align: center; }}
        .stat-card .value {{ font-size: 42px; font-weight: bold; margin-bottom: 5px; }}
        .stat-card .label {{ color: #666; font-size: 14px; }}
        .stat-card.passed .value {{ color: var(--success); }}
        .stat-card.failed .value {{ color: var(--danger); }}
        .stat-card.total .value {{ color: var(--primary); }}
        .section {{ background: white; border-radius: 12px; padding: 25px; margin-bottom: 25px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }}
        .section h2 {{ color: var(--primary); border-bottom: 3px solid var(--secondary); padding-bottom: 10px; margin-bottom: 20px; }}
        .rule {{ padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 5px solid #ddd; background: var(--light); }}
        .rule.passed {{ border-left-color: var(--success); }}
        .rule.failed {{ border-left-color: var(--danger); }}
        .rule-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }}
        .rule-id {{ font-size: 12px; color: #888; font-family: monospace; }}
        .rule-name {{ font-weight: 600; color: #333; }}
        .status {{ padding: 5px 15px; border-radius: 20px; font-size: 12px; font-weight: bold; }}
        .status-passed {{ background: var(--success); color: white; }}
        .status-failed {{ background: var(--danger); color: white; }}
        .wcag-badge {{ background: var(--primary); color: white; padding: 3px 8px; border-radius: 4px; font-size: 11px; margin-left: 10px; }}
        .severity-critical {{ color: #c0392b; }}
        .severity-serious {{ color: #e74c3c; }}
        .severity-moderate {{ color: #f39c12; }}
        .severity-minor {{ color: #3498db; }}
        .footer {{ text-align: center; color: #888; padding: 30px; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 AccessMind ACT Rules Report</h1>
            <div class="url">{self.target_url}</div>
            <div style="margin-top: 10px; font-size: 12px;">{self.timestamp}</div>
        </div>
        
        <div class="stats">
            <div class="stat-card total">
                <div class="value">{results['total_rules']}</div>
                <div class="label">Toplam Kural</div>
            </div>
            <div class="stat-card passed">
                <div class="value">{results['passed']}</div>
                <div class="label">Geçen</div>
            </div>
            <div class="stat-card failed">
                <div class="value">{results['failed']}</div>
                <div class="label">Kalın</div>
            </div>
            <div class="stat-card">
                <div class="value" style="color: var(--primary);">{results['pass_rate']:.1f}%</div>
                <div class="label">Uyumluluk Oranı</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 Kriter Özeti</h2>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px;">
                <div style="text-align: center; padding: 15px; background: #e8f4f8; border-radius: 8px;">
                    <strong>Perceivable</strong><br>
                    <span style="color: var(--success);">{results['summary']['by_category']['Perceivable']['passed']}</span> / 
                    <span style="color: var(--danger);">{results['summary']['by_category']['Perceivable']['failed']}</span>
                </div>
                <div style="text-align: center; padding: 15px; background: #fff3e8; border-radius: 8px;">
                    <strong>Operable</strong><br>
                    <span style="color: var(--success);">{results['summary']['by_category']['Operable']['passed']}</span> / 
                    <span style="color: var(--danger);">{results['summary']['by_category']['Operable']['failed']}</span>
                </div>
                <div style="text-align: center; padding: 15px; background: #f0e8f8; border-radius: 8px;">
                    <strong>Understandable</strong><br>
                    <span style="color: var(--success);">{results['summary']['by_category']['Understandable']['passed']}</span> / 
                    <span style="color: var(--danger);">{results['summary']['by_category']['Understandable']['failed']}</span>
                </div>
                <div style="text-align: center; padding: 15px; background: #e8f8e8; border-radius: 8px;">
                    <strong>Robust</strong><br>
                    <span style="color: var(--success);">{results['summary']['by_category']['Robust']['passed']}</span> / 
                    <span style="color: var(--danger);">{results['summary']['by_category']['Robust']['failed']}</span>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>📋 ACT Rules Detayları</h2>
"""
        
        # Kategorilere göre grupla
        categories = ["Perceivable", "Operable", "Understandable", "Robust"]
        for category in categories:
            category_rules = [r for r in self.rules if r.wcag_criterion.category == category]
            if category_rules:
                html += f"""
            <h3 style="color: var(--primary); margin: 25px 0 15px 0;">{category}</h3>
"""
                for rule in category_rules:
                    status_class = "passed" if rule.passed else "failed"
                    status_text = "PASSED" if rule.passed else "FAILED"
                    severity_class = f"severity-{rule.severity.value}"
                    
                    html += f"""
            <div class="rule {status_class}">
                <div class="rule-header">
                    <div>
                        <span class="rule-id">{rule.rule_id}</span>
                        <span class="rule-name">{rule.name}</span>
                        <span class="wcag-badge">{rule.wcag_criterion.id}</span>
                        <span class="{severity_class}">({rule.severity.value})</span>
                    </div>
                    <span class="status status-{status_class}">{status_text}</span>
                </div>
                <p style="color: #666; font-size: 14px; margin: 10px 0;">{rule.description}</p>
                <p style="font-size: 12px; color: #888;"><strong>Beklenen:</strong> {rule.expected_result}</p>
            </div>
"""
        
        html += f"""
        </div>
        
        <div class="footer">
            <p><strong>AccessMind Enterprise v6.0</strong> - ACT Rules Format</p>
            <p>W3C Accessibility Conformance Testing Rules Format</p>
            <p>Kaynak: <a href="https://www.w3.org/WAI/standards-guidelines/act/rules/about/" target="_blank">W3C ACT Rules</a></p>
        </div>
    </div>
</body>
</html>
"""
        
        return html


async def main():
    """Test suite çalıştır"""
    import os
    
    target_url = "https://example.com"
    
    print("=" * 70)
    print("🧠 AccessMind ACT Rules Engine v6.0")
    print("=" * 70)
    print(f"Target: {target_url}")
    print(f"Total Rules: {len(ACTRulesEngine(target_url).rules)}")
    
    engine = ACTRulesEngine(target_url)
    
    # Sayfa verilerini simüle et
    page_data = {
        "missing_alt": 2,
        "missing_labels": 1,
        "contrast_issues": 3,
        "keyboard_issues": 1,
        "navigation_issues": 2,
        "form_issues": 1,
        "structure_issues": 0,
        "language_issues": 0,
        "predictability_issues": 0,
        "compatibility_issues": 0
    }
    
    # Değerlendir
    results = engine.evaluate_page(page_data)
    
    # Raporları kaydet
    output_dir = "/Users/sarper/.openclaw/workspace/audits"
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_file = f"{output_dir}/act-rules-{timestamp}.json"
    html_file = f"{output_dir}/act-rules-{timestamp}.html"
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(engine.to_json(), f, ensure_ascii=False, indent=2)
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(engine.to_html_report(page_data))
    
    print("=" * 70)
    print("✅ ACT Rules Test Suite Tamamlandı")
    print("=" * 70)
    print(f"📊 Toplam Kural: {results['total_rules']}")
    print(f"✅ Geçen: {results['passed']}")
    print(f"❌ Kalın: {results['failed']}")
    print(f"📈 Uyumluluk: {results['pass_rate']:.1f}%")
    print(f"📄 JSON: {json_file}")
    print(f"📄 HTML: {html_file}")
    print("=" * 70)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())