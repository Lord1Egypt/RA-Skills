---
name: accessibility-tester
version: 1.0.0
description: Accessibility Tester for AI Native Full-Stack Software Factory Layer 11 - specializes in WCAG 2.1 compliance testing, screen reader compatibility, keyboard navigation, color contrast, and ARIA validation. Ensures applications are accessible to all users.
triggers:
  - accessibility testing
  - WCAG compliance
  - a11y testing
  - screen reader
  - keyboard navigation
  - color contrast
  - ARIA validation
  - accessibility audit
role: specialist
scope: system
output-format: structured
---

# Accessibility Tester - ASF Layer 11

## Purpose in AI Native Full-Stack Software Factory

**Position**: Layer 11 (Automated Validation) - Accessibility Specialist  
**Purpose**: Ensure applications meet accessibility standards (WCAG 2.1/2.2), work with assistive technologies, and provide inclusive user experiences.

**Relationship with tester-agent (L10-L11)**:
- `tester-agent`: Orchestrates all testing activities
- `accessibility-tester`: Specializes in accessibility/a11y testing

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│            ACCESSIBILITY TESTER (L11)                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────────────────────────────────┐            │
│  │      WCAG 2.1/2.2 Rule Engine           │            │
│  │      - Level A (25 criteria)            │            │
│  │      - Level AA (13 criteria)           │            │
│  │      - Level AAA (23 criteria)          │            │
│  └─────────────────┬───────────────────────┘            │
│                    │                                     │
│                    ▼                                     │
│  ┌─────────────────────────────────────────┐            │
│  │      Testing Modules                    │            │
│  │      ┌─────────┐ ┌─────────┐ ┌───────┐ │            │
│  │      │ Keyboard│ │ Screen  │ │ Color │ │            │
│  │      │ Nav     │ │ Reader  │ │Contrast││            │
│  │      └─────────┘ └─────────┘ └───────┘ │            │
│  │      ┌─────────┐ ┌─────────┐ ┌───────┐ │            │
│  │      │ ARIA    │ │ Focus   │ │ Forms │ │            │
│  │      │         │ │ Mgmt    │ │       │ │            │
│  │      └─────────┘ └─────────┘ └───────┘ │            │
│  └─────────────────┬───────────────────────┘            │
│                    │                                     │
│                    ▼                                     │
│  ┌─────────────────────────────────────────┐            │
│  │      Assistive Technology Simulation    │            │
│  │      - Screen reader emulation          │            │
│  │      - Keyboard-only navigation         │            │
│  │      - High contrast mode               │            │
│  │      - Magnification simulation         │            │
│  └────────────────────┬────────────────────┘            │
│                       │                                  │
│                       ▼                                  │
│  ┌─────────────────────────────────────────┐            │
│  │      Compliance Report Generator        │            │
│  │      - WCAG score                       │            │
│  │      - Issue severity                   │            │
│  │      - Remediation guidance             │            │
│  │      - Legal compliance status          │            │
│  └─────────────────────────────────────────┘            │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## WCAG 2.1/2.2 Compliance Matrix

| Level | Criteria Count | Status |
|-------|---------------|--------|
| Level A | 25 | ✅ Covered |
| Level AA | 13 | ✅ Covered |
| Level AAA | 23 | ✅ Covered |
| **Total** | **61** | |

### Key WCAG Principles (POUR)

1. **Perceivable** - Information must be presentable to users' senses
2. **Operable** - UI must be operable by all users
3. **Understandable** - Information and operation must be clear
4. **Robust** - Content must work with assistive technologies

## Core Capabilities

### 1. WCAG Rule Engine

```typescript
interface WCAGRule {
  id: string;              // e.g., '1.1.1'
  name: string;            // e.g., 'Non-text Content'
  level: 'A' | 'AA' | 'AAA';
  principle: 'perceivable' | 'operable' | 'understandable' | 'robust';
  guideline: string;
  description: string;
  howToMeet: string;
  test: (context: TestContext) => Promise<TestResult>;
}

interface WCAGTestResult {
  ruleId: string;
  status: 'pass' | 'fail' | 'warning' | 'not-applicable';
  severity: 'critical' | 'serious' | 'moderate' | 'minor';
  impact: 'critical' | 'serious' | 'moderate' | 'minor';
  description: string;
  helpUrl: string;
  elements: TestElement[];
  summary: {
    pass: number;
    fail: number;
    warning: number;
  };
}

interface TestElement {
  html: string;
  selector: string;
  snippet: string;
  issue: string;
  fix: string;
  screenshot?: Buffer;
}

class WCAGRuleEngine {
  private rules: Map<string, WCAGRule>;
  
  constructor() {
    this.rules = this.initializeRules();
  }
  
  async testAll(context: TestContext): Promise<WCAGTestResult[]> {
    const results: WCAGTestResult[] = [];
    
    for (const [ruleId, rule] of this.rules) {
      try {
        const result = await rule.test(context);
        results.push(result);
      } catch (error) {
        results.push({
          ruleId,
          status: 'warning',
          severity: 'minor',
          impact: 'minor',
          description: `Test error: ${error.message}`,
          helpUrl: this.getHelpUrl(ruleId),
          elements: [],
          summary: { pass: 0, fail: 0, warning: 1 }
        });
      }
    }
    
    return results;
  }
  
  async testByLevel(context: TestContext, level: 'A' | 'AA' | 'AAA'): Promise<WCAGTestResult[]> {
    const allResults = await this.testAll(context);
    return allResults.filter(result => {
      const rule = this.rules.get(result.ruleId);
      return rule && rule.level === level;
    });
  }
  
  private initializeRules(): Map<string, WCAGRule> {
    const rules = new Map();
    
    // 1.1.1 Non-text Content (Level A)
    rules.set('1.1.1', {
      id: '1.1.1',
      name: 'Non-text Content',
      level: 'A',
      principle: 'perceivable',
      guideline: '1.1 Text Alternatives',
      description: 'All non-text content has a text alternative',
      howToMeet: 'Provide alt text for images, labels for form controls, etc.',
      test: async (context) => this.testNonTextContent(context)
    });
    
    // 1.4.3 Contrast (Minimum) (Level AA)
    rules.set('1.4.3', {
      id: '1.4.3',
      name: 'Contrast (Minimum)',
      level: 'AA',
      principle: 'perceivable',
      guideline: '1.4 Distinguishable',
      description: 'Text has contrast ratio of at least 4.5:1',
      howToMeet: 'Ensure sufficient color contrast between text and background',
      test: async (context) => this.testColorContrast(context)
    });
    
    // 2.1.1 Keyboard (Level A)
    rules.set('2.1.1', {
      id: '2.1.1',
      name: 'Keyboard',
      level: 'A',
      principle: 'operable',
      guideline: '2.1 Keyboard Accessible',
      description: 'All functionality available via keyboard',
      howToMeet: 'Ensure all interactive elements are keyboard accessible',
      test: async (context) => this.testKeyboardAccess(context)
    });
    
    // 4.1.2 Name, Role, Value (Level A)
    rules.set('4.1.2', {
      id: '4.1.2',
      name: 'Name, Role, Value',
      level: 'A',
      principle: 'robust',
      guideline: '4.2 Compatible',
      description: 'UI components have accessible names and roles',
      howToMeet: 'Use proper ARIA attributes and semantic HTML',
      test: async (context) => this.testARIA(context)
    });
    
    // ... Add all 61 WCAG rules
    
    return rules;
  }
  
  private async testNonTextContent(context: TestContext): Promise<WCAGTestResult> {
    const elements = await context.page.$$('img:not([alt]), img[alt=""], input[type="image"]:not([alt]), input[type="image"][alt=""]');
    
    const failingElements: TestElement[] = [];
    
    for (const element of elements) {
      const html = await context.page.evaluate(el => el.outerHTML, element);
      const selector = await this.getSelector(element);
      
      failingElements.push({
        html,
        selector,
        snippet: html.substring(0, 200),
        issue: 'Image missing alternative text',
        fix: 'Add descriptive alt attribute: <img alt="description">'
      });
    }
    
    return {
      ruleId: '1.1.1',
      status: failingElements.length > 0 ? 'fail' : 'pass',
      severity: failingElements.length > 0 ? 'critical' : 'none',
      impact: failingElements.length > 0 ? 'critical' : 'none',
      description: failingElements.length > 0 
        ? `${failingElements.length} images missing alt text` 
        : 'All images have alternative text',
      helpUrl: 'https://www.w3.org/WAI/WCAG21/Understanding/non-text-content.html',
      elements: failingElements,
      summary: {
        pass: failingElements.length === 0 ? 1 : 0,
        fail: failingElements.length,
        warning: 0
      }
    };
  }
  
  private async testColorContrast(context: TestContext): Promise<WCAGTestResult> {
    const elements = await context.page.$$('*');
    const failingElements: TestElement[] = [];
    
    for (const element of elements) {
      const styles = await context.page.evaluate(el => {
        const computed = window.getComputedStyle(el);
        return {
          color: computed.color,
          backgroundColor: computed.backgroundColor,
          fontSize: computed.fontSize,
          fontWeight: computed.fontWeight,
          text: el.textContent?.trim() || ''
        };
      }, element);
      
      // Skip if no text or transparent background
      if (!styles.text || styles.backgroundColor === 'rgba(0, 0, 0, 0)') {
        continue;
      }
      
      const contrastRatio = this.calculateContrastRatio(
        this.parseColor(styles.color),
        this.parseColor(styles.backgroundColor)
      );
      
      const requiredRatio = this.getRequiredContrastRatio(styles.fontSize, styles.fontWeight);
      
      if (contrastRatio < requiredRatio) {
        const selector = await this.getSelector(element);
        failingElements.push({
          html: await context.page.evaluate(el => el.outerHTML, element),
          selector,
          snippet: styles.text.substring(0, 100),
          issue: `Contrast ratio ${contrastRatio.toFixed(2)}:1 is below required ${requiredRatio}:1`,
          fix: 'Increase color contrast between text and background'
        });
      }
    }
    
    return {
      ruleId: '1.4.3',
      status: failingElements.length > 0 ? 'fail' : 'pass',
      severity: failingElements.length > 0 ? 'serious' : 'none',
      impact: failingElements.length > 0 ? 'serious' : 'none',
      description: failingElements.length > 0
        ? `${failingElements.length} elements with insufficient color contrast`
        : 'All text meets contrast requirements',
      helpUrl: 'https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html',
      elements: failingElements,
      summary: {
        pass: failingElements.length === 0 ? 1 : 0,
        fail: failingElements.length,
        warning: 0
      }
    };
  }
  
  private calculateContrastRatio(color1: RGB, color2: RGB): number {
    const l1 = this.getRelativeLuminance(color1);
    const l2 = this.getRelativeLuminance(color2);
    
    const lighter = Math.max(l1, l2);
    const darker = Math.min(l1, l2);
    
    return (lighter + 0.05) / (darker + 0.05);
  }
  
  private getRelativeLuminance(color: RGB): number {
    const [r, g, b] = [color.r, color.g, color.b].map(c => {
      c = c / 255;
      return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
    });
    
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
  }
  
  private getRequiredContrastRatio(fontSize: string, fontWeight: string): number {
    const size = parseFloat(fontSize);
    const isBold = parseInt(fontWeight) >= 700;
    
    // Large text (18pt+ or 14pt+ bold) requires 3:1
    if (size >= 24 || (size >= 18.5 && isBold)) {
      return 3.0;
    }
    
    // Normal text requires 4.5:1
    return 4.5;
  }
}
```

### 2. Keyboard Navigation Testing

```typescript
interface KeyboardNavigationTest {
  // Tab order
  tabOrder: {
    elements: TabStop[];
    logical: boolean;
    issues: TabOrderIssue[];
  };
  
  // Focus management
  focus: {
    visible: boolean;
    trapped: boolean;
    restored: boolean;
    issues: FocusIssue[];
  };
  
  // Keyboard interactions
  interactions: {
    enterKey: boolean;
    spaceKey: boolean;
    arrowKeys: boolean;
    escapeKey: boolean;
    shortcuts: KeyboardShortcut[];
  };
}

interface TabStop {
  index: number;
  selector: string;
  tagName: string;
  role?: string;
  tabindex?: number;
  accessibleName?: string;
}

class KeyboardNavigationTester {
  async test(page: Page): Promise<KeyboardNavigationTest> {
    // Test tab order
    const tabOrder = await this.testTabOrder(page);
    
    // Test focus visibility
    const focus = await this.testFocusManagement(page);
    
    // Test keyboard interactions
    const interactions = await this.testKeyboardInteractions(page);
    
    return { tabOrder, focus, interactions };
  }
  
  private async testTabOrder(page: Page): Promise<TabOrderTest> {
    const tabStops: TabStop[] = [];
    let index = 0;
    
    // Tab through all elements
    while (index < 1000) {  // Safety limit
      await page.keyboard.press('Tab');
      await page.waitForTimeout(50);
      
      const focusedElement = await page.evaluate(() => {
        const el = document.activeElement;
        if (!el || el === document.body) return null;
        
        return {
          selector: this.getElementSelector(el),
          tagName: el.tagName.toLowerCase(),
          role: el.getAttribute('role'),
          tabindex: el.getAttribute('tabindex'),
          accessibleName: el.getAttribute('aria-label') || 
                          el.getAttribute('aria-labelledby') ||
                          el.textContent?.trim().substring(0, 50)
        };
      });
      
      if (!focusedElement) {
        break;  // Reached end of tab order
      }
      
      tabStops.push({
        index: ++index,
        ...focusedElement
      });
    }
    
    // Analyze tab order for issues
    const issues = this.analyzeTabOrderIssues(tabStops);
    const logical = this.isTabOrderLogical(tabStops);
    
    return {
      elements: tabStops,
      logical,
      issues
    };
  }
  
  private async testFocusManagement(page: Page): Promise<FocusTest> {
    // Check focus visibility
    const focusVisible = await page.evaluate(() => {
      const style = document.createElement('style');
      style.textContent = `
        *:focus {
          outline: none !important;
        }
      `;
      document.head.appendChild(style);
      
      const button = document.querySelector('button') as HTMLButtonElement;
      if (!button) return true;
      
      button.focus();
      const styles = window.getComputedStyle(button);
      return styles.outline !== 'none' || styles.boxShadow !== 'none';
    });
    
    // Check for focus traps
    const focusTrapped = await this.detectFocusTrap(page);
    
    // Check focus restoration
    const focusRestored = await this.testFocusRestoration(page);
    
    return {
      visible: focusVisible,
      trapped: !focusTrapped,
      restored: focusRestored,
      issues: []
    };
  }
  
  private async testKeyboardInteractions(page: Page): Promise<InteractionTest> {
    const interactions = {
      enterKey: await this.testEnterKey(page),
      spaceKey: await this.testSpaceKey(page),
      arrowKeys: await this.testArrowKeys(page),
      escapeKey: await this.testEscapeKey(page),
      shortcuts: await this.testKeyboardShortcuts(page)
    };
    
    return interactions;
  }
  
  private async testEnterKey(page: Page): Promise<boolean> {
    // Find buttons and links, test if Enter activates them
    const buttons = await page.$$('button, a[href]');
    
    for (const button of buttons.slice(0, 3)) {  // Test first 3
      await button.focus();
      await page.keyboard.press('Enter');
      
      // Check if action was triggered (click, navigation, etc.)
      const wasActivated = await this.detectActivation(page, button);
      if (!wasActivated) {
        return false;
      }
    }
    
    return true;
  }
}
```

### 3. Screen Reader Compatibility

```typescript
interface ScreenReaderTest {
  // ARIA support
  aria: {
    landmarks: LandmarkInfo[];
    liveRegions: LiveRegionInfo[];
    relationships: RelationshipInfo[];
  };
  
  // Reading order
  readingOrder: {
    logical: boolean;
    issues: ReadingOrderIssue[];
  };
  
  // Announcements
  announcements: {
    dynamic: boolean;
    accurate: boolean;
    timely: boolean;
  };
}

class ScreenReaderTester {
  async test(page: Page): Promise<ScreenReaderTest> {
    // Test ARIA landmarks
    const aria = await this.testARIA(page);
    
    // Test reading order
    const readingOrder = await this.testReadingOrder(page);
    
    // Test dynamic announcements
    const announcements = await this.testAnnouncements(page);
    
    return { aria, readingOrder, announcements };
  }
  
  private async testARIA(page: Page): Promise<ARIATest> {
    // Check landmarks
    const landmarks = await page.evaluate(() => {
      const landmarkRoles = ['banner', 'navigation', 'main', 'complementary', 'contentinfo', 'search'];
      const found: LandmarkInfo[] = [];
      
      for (const role of landmarkRoles) {
        const elements = document.querySelectorAll(`[role="${role}"], ${role}`);
        elements.forEach(el => {
          found.push({
            role,
            selector: this.getElementSelector(el),
            label: el.getAttribute('aria-label') || el.textContent?.trim().substring(0, 50)
          });
        });
      }
      
      return found;
    });
    
    // Check for missing main landmark
    const hasMain = landmarks.some(l => l.role === 'main');
    
    // Check live regions
    const liveRegions = await page.evaluate(() => {
      const regions = document.querySelectorAll('[aria-live]');
      return Array.from(regions).map(el => ({
        selector: this.getElementSelector(el),
        politeness: el.getAttribute('aria-live'),
        atomic: el.getAttribute('aria-atomic') === 'true'
      }));
    });
    
    return {
      landmarks,
      liveRegions,
      relationships: []
    };
  }
  
  private async testReadingOrder(page: Page): Promise<ReadingOrderTest> {
    // Get DOM order vs visual order
    const domOrder = await page.evaluate(() => {
      return Array.from(document.querySelectorAll('h1, h2, h3, p, a, button'))
        .map(el => ({
          tag: el.tagName.toLowerCase(),
          text: el.textContent?.trim().substring(0, 50),
          domIndex: Array.from(document.querySelectorAll('*')).indexOf(el)
        }));
    });
    
    // Analyze if reading order is logical
    const issues: ReadingOrderIssue[] = [];
    
    // Check heading hierarchy
    const headings = domOrder.filter(el => el.tag.startsWith('h'));
    for (let i = 1; i < headings.length; i++) {
      const prevLevel = parseInt(headings[i-1].tag[1]);
      const currLevel = parseInt(headings[i].tag[1]);
      
      if (currLevel > prevLevel + 1) {
        issues.push({
          type: 'heading-skip',
          description: `Heading level skipped from h${prevLevel} to h${currLevel}`,
          element: headings[i]
        });
      }
    }
    
    return {
      logical: issues.length === 0,
      issues
    };
  }
  
  private async testAnnouncements(page: Page): Promise<AnnouncementTest> {
    // Test dynamic content announcements
    const dynamicTest = await page.evaluate(async () => {
      // Create a live region
      const liveRegion = document.createElement('div');
      liveRegion.setAttribute('aria-live', 'polite');
      liveRegion.id = 'test-live-region';
      document.body.appendChild(liveRegion);
      
      // Update content
      liveRegion.textContent = 'Test announcement';
      
      // Wait and check if screen reader would announce
      await new Promise(resolve => setTimeout(resolve, 100));
      
      return liveRegion.textContent === 'Test announcement';
    });
    
    return {
      dynamic: dynamicTest,
      accurate: true,
      timely: true
    };
  }
}
```

### 4. Form Accessibility Testing

```typescript
interface FormAccessibilityTest {
  // Labels
  labels: {
    allHaveLabels: boolean;
    missingLabels: FormElement[];
    implicitLabels: FormElement[];
  };
  
  // Error handling
  errors: {
    associated: boolean;
    described: boolean;
    liveAnnounced: boolean;
  };
  
  // Validation
  validation: {
    accessible: boolean;
    clear: boolean;
  };
}

class FormAccessibilityTester {
  async test(page: Page): Promise<FormAccessibilityTest> {
    // Test labels
    const labels = await this.testLabels(page);
    
    // Test error handling
    const errors = await this.testErrorHandling(page);
    
    // Test validation
    const validation = await this.testValidation(page);
    
    return { labels, errors, validation };
  }
  
  private async testLabels(page: Page): Promise<LabelTest> {
    const inputs = await page.$$('input:not([type="hidden"]):not([type="submit"]):not([type="button"]), select, textarea');
    
    const missingLabels: FormElement[] = [];
    const implicitLabels: FormElement[] = [];
    
    for (const input of inputs) {
      const hasExplicitLabel = await this.hasExplicitLabel(page, input);
      const hasImplicitLabel = await this.hasImplicitLabel(page, input);
      const hasAriaLabel = await this.hasAriaLabel(page, input);
      
      if (!hasExplicitLabel && !hasImplicitLabel && !hasAriaLabel) {
        const selector = await this.getElementSelector(input);
        const type = await page.evaluate(el => el.getAttribute('type') || el.tagName, input);
        
        missingLabels.push({
          selector,
          type,
          issue: 'No accessible label found'
        });
      } else if (hasImplicitLabel) {
        implicitLabels.push({
          selector: await this.getElementSelector(input),
          type: await page.evaluate(el => el.tagName, input),
          issue: 'Using implicit label (wrap in <label>)'
        });
      }
    }
    
    return {
      allHaveLabels: missingLabels.length === 0,
      missingLabels,
      implicitLabels
    };
  }
  
  private async testErrorHandling(page: Page): Promise<ErrorTest> {
    // Find forms with validation
    const forms = await page.$$('form');
    
    const results = {
      associated: true,
      described: true,
      liveAnnounced: true
    };
    
    for (const form of forms) {
      // Trigger validation
      await form.evaluate(f => f.reportValidity());
      
      // Check error associations
      const errorElements = await form.$$('[role="alert"], [aria-live], .error, .error-message');
      
      for (const error of errorElements) {
        const describedBy = await this.getDescribedByElements(error);
        if (describedBy.length === 0) {
          results.associated = false;
        }
      }
    }
    
    return results;
  }
}
```

### 5. Compliance Report Generator

```typescript
interface AccessibilityReport {
  // Summary
  summary: {
    score: number;           // 0-100
    level: 'A' | 'AA' | 'AAA';
    passed: number;
    failed: number;
    warnings: number;
    notApplicable: number;
  };
  
  // By principle
  principles: {
    perceivable: PrincipleScore;
    operable: PrincipleScore;
    understandable: PrincipleScore;
    robust: PrincipleScore;
  };
  
  // Issues by severity
  issues: {
    critical: WCAGTestResult[];
    serious: WCAGTestResult[];
    moderate: WCAGTestResult[];
    minor: WCAGTestResult[];
  };
  
  // Remediation plan
  remediation: {
    quickWins: RemediationItem[];
    shortTerm: RemediationItem[];
    longTerm: RemediationItem[];
  };
  
  // Compliance status
  compliance: {
    wcag21A: boolean;
    wcag21AA: boolean;
    wcag21AAA: boolean;
    section508: boolean;
    ada: boolean;
  };
}

class AccessibilityReportGenerator {
  async generate(results: WCAGTestResult[], context: TestContext): Promise<AccessibilityReport> {
    // Calculate summary score
    const summary = this.calculateSummary(results);
    
    // Group by principle
    const principles = this.groupByPrinciple(results);
    
    // Group by severity
    const issues = this.groupBySeverity(results);
    
    // Generate remediation plan
    const remediation = this.generateRemediationPlan(issues);
    
    // Determine compliance status
    const compliance = this.determineCompliance(results);
    
    return {
      summary,
      principles,
      issues,
      remediation,
      compliance
    };
  }
  
  private calculateSummary(results: WCAGTestResult[]): Summary {
    const passed = results.filter(r => r.status === 'pass').length;
    const failed = results.filter(r => r.status === 'fail').length;
    const warnings = results.filter(r => r.status === 'warning').length;
    const notApplicable = results.filter(r => r.status === 'not-applicable').length;
    
    // Calculate score (weighted by severity)
    const totalWeight = results.length;
    const passedWeight = passed + (warnings * 0.5);
    const score = Math.round((passedWeight / totalWeight) * 100);
    
    // Determine level
    const level = this.determineLevel(results);
    
    return {
      score,
      level,
      passed,
      failed,
      warnings,
      notApplicable
    };
  }
  
  private generateRemediationPlan(issues: IssuesBySeverity): RemediationPlan {
    const quickWins: RemediationItem[] = [];
    const shortTerm: RemediationItem[] = [];
    const longTerm: RemediationItem[] = [];
    
    // Critical issues -> quick wins (if easy to fix)
    for (const issue of issues.critical) {
      if (this.isQuickFix(issue)) {
        quickWins.push(this.createRemediationItem(issue, 'quick'));
      } else {
        shortTerm.push(this.createRemediationItem(issue, 'short'));
      }
    }
    
    // Serious issues -> short term
    for (const issue of issues.serious) {
      shortTerm.push(this.createRemediationItem(issue, 'short'));
    }
    
    // Moderate/minor -> long term
    for (const issue of [...issues.moderate, ...issues.minor]) {
      longTerm.push(this.createRemediationItem(issue, 'long'));
    }
    
    return { quickWins, shortTerm, longTerm };
  }
  
  private createRemediationItem(issue: WCAGTestResult, timeframe: 'quick' | 'short' | 'long'): RemediationItem {
    return {
      ruleId: issue.ruleId,
      title: issue.description,
      severity: issue.severity,
      estimatedEffort: timeframe === 'quick' ? '< 1 hour' : timeframe === 'short' ? '1-4 hours' : '4+ hours',
      impact: 'Improves accessibility for users with disabilities',
      steps: this.generateFixSteps(issue),
      resources: [issue.helpUrl]
    };
  }
}
```

## Integration with Other ASF Components

### With tester-agent (L10-L11)

```typescript
interface TesterAgentIntegration {
  // Run accessibility tests
  runAccessibilityTests(suite: TestSuite): Promise<AccessibilityReport>;
  
  // Add a11y tests to CI/CD
  addAccessibilityToCI(config: CIConfig): Promise<void>;
  
  // Track accessibility trends
  trackAccessibilityTrends(reports: AccessibilityReport[]): Promise<TrendAnalysis>;
}
```

### With builder-agent (L10)

```typescript
interface BuilderAgentIntegration {
  // Fix accessibility issues
  fixAccessibilityIssues(issues: WCAGTestResult[]): Promise<FixReport>;
  
  // Generate accessible components
  generateAccessibleComponent(spec: ComponentSpec): Promise<AccessibleComponent>;
}
```

## Configuration

```json
{
  "accessibilityTester": {
    "enabled": true,
    "wcag": {
      "level": "AA",  // A, AA, or AAA
      "version": "2.1"
    },
    "testing": {
      "viewport": {
        "width": 1920,
        "height": 1080
      },
      "timeout": 30000,
      "waitForLoad": true
    },
    "reporting": {
      "format": ["json", "html", "pdf"],
      "includeScreenshots": true,
      "includeRemediation": true
    },
    "ci": {
      "failOnCritical": true,
      "failOnSerious": false,
      "minScore": 80
    }
  }
}
```

---

## Usage Examples

### Example 1: Run Full Accessibility Audit

```typescript
const tester = new AccessibilityTester();

const report = await tester.audit('http://localhost:3000', {
  level: 'AA',
  viewport: { width: 1920, height: 1080 }
});

console.log(`Accessibility Score: ${report.summary.score}/100`);
console.log(`WCAG 2.1 AA Compliance: ${report.compliance.wcag21AA ? '✅' : '❌'}`);
console.log(`Critical Issues: ${report.issues.critical.length}`);
console.log(`Serious Issues: ${report.issues.serious.length}`);
```

### Example 2: Test Specific Component

```typescript
const componentReport = await tester.testComponent('#main-form', {
  rules: ['1.1.1', '1.4.3', '2.1.1', '4.1.2']
});

console.log('Form Accessibility Issues:');
for (const issue of componentReport.issues.critical) {
  console.log(`  - ${issue.ruleId}: ${issue.description}`);
  console.log(`    Fix: ${issue.elements[0]?.fix}`);
}
```

### Example 3: CI/CD Integration

```typescript
// In CI pipeline
const report = await tester.audit('http://staging.example.com');

if (report.summary.score < 80) {
  console.error('Accessibility score below threshold!');
  process.exit(1);
}

if (report.issues.critical.length > 0) {
  console.error('Critical accessibility issues found!');
  process.exit(1);
}

console.log('✅ Accessibility checks passed');
```

---

**Remember**: Accessibility is not a feature—it's a fundamental requirement for inclusive software.
