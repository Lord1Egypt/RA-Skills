# Accessibility Auditor — Code Examples

## Example 1

```javascript
// tests/accessibility/a11y-test-suite.js
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

class AccessibilityTester {
  constructor(page) {
    this.page = page;
    this.violations = [];
  }

  async runFullAudit(url, options = {}) {
    await this.page.goto(url);
    
    const axeBuilder = new AxeBuilder({ page: this.page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa'])
      .exclude(options.exclude || [])
      .include(options.include || []);

    if (options.disableRules) {
      axeBuilder.disableRules(options.disableRules);
    }

    const results = await axeBuilder.analyze();
    this.violations = results.violations;

    return {
      violations: results.violations,
      passes: results.passes,
      incomplete: results.incomplete,
      inapplicable: results.inapplicable,
      summary: this.generateSummary(results)
    };
  }

  async testKeyboardNavigation() {
    const violations = [];
    
    // Test tab navigation
    const focusableElements = await this.page.locator(
      'a, button, input, textarea, select, [tabindex]:not([tabindex="-1"])'
    ).all();

    // Check tab order
    await this.page.keyboard.press('Tab');
    let previousTabIndex = -1;

    for (let i = 0; i < Math.min(focusableElements.length, 20); i++) {
      const focusedElement = await this.page.locator(':focus').first();
      
      if (await focusedElement.count() === 0) {
        violations.push(`No element focused at tab step ${i + 1}`);
        break;
      }

      const tabIndex = await focusedElement.getAttribute('tabindex');
      const currentTabIndex = tabIndex ? parseInt(tabIndex) : 0;

      if (currentTabIndex > 0 && currentTabIndex <= previousTabIndex) {
        violations.push(`Tab order violation: tabindex ${currentTabIndex} after ${previousTabIndex}`);
      }

      previousTabIndex = currentTabIndex;
      await this.page.keyboard.press('Tab');
    }

    // Test escape key functionality
    const modals = await this.page.locator('[role="dialog"], .modal').all();
    for (const modal of modals) {
      if (await modal.isVisible()) {
        await this.page.keyboard.press('Escape');
        if (await modal.isVisible()) {
          violations.push('Modal does not close with Escape key');
        }
      }
    }

    return violations;
  }

  async testColorContrast() {
    const violations = [];
    
    const textElements = await this.page.locator('p, h1, h2, h3, h4, h5, h6, span, a, button, label').all();
    
    for (const element of textElements.slice(0, 50)) { // Limit for performance
      try {
        const styles = await element.evaluate(el => {
          const computedStyle = window.getComputedStyle(el);
          return {
            color: computedStyle.color,
            backgroundColor: computedStyle.backgroundColor,
            fontSize: computedStyle.fontSize,
            fontWeight: computedStyle.fontWeight
          };
        });

        const textContent = await element.textContent();
        if (!textContent || textContent.trim().length === 0) continue;

        // This is a simplified check - in practice, use a proper contrast calculator
        const contrastRatio = await this.calculateContrastRatio(styles.color, styles.backgroundColor);
        
        const fontSize = parseFloat(styles.fontSize);
        const isLargeText = fontSize >= 18 || (fontSize >= 14 && styles.fontWeight >= 700);
        
        const requiredRatio = isLargeText ? 3 : 4.5;
        
        if (contrastRatio < requiredRatio) {
          violations.push({
            element: await element.getAttribute('outerHTML'),
            contrastRatio: contrastRatio,
            requiredRatio: requiredRatio,
            isLargeText: isLargeText
          });
        }
      } catch (error) {
        // Skip elements that can't be analyzed
      }
    }

    return violations;
  }

  async testScreenReaderCompatibility() {
    const violations = [];

    // Check for proper heading structure
    const headings = await this.page.locator('h1, h2, h3, h4, h5, h6').all();
    let previousLevel = 0;

    for (const heading of headings) {
      const tagName = await heading.evaluate(el => el.tagName.toLowerCase());
      const currentLevel = parseInt(tagName.substring(1));

      if (currentLevel > previousLevel + 1) {
        violations.push(`Heading level skip: jumped from h${previousLevel} to h${currentLevel}`);
      }

      const text = await heading.textContent();
      if (!text || text.trim().length === 0) {
        violations.push(`Empty heading: ${tagName}`);
      }

      previousLevel = currentLevel;
    }

    // Check for alt text on images
    const images = await this.page.locator('img').all();
    for (const img of images) {
      const alt = await img.getAttribute('alt');
      const role = await img.getAttribute('role');
      
      if (alt === null && role !== 'presentation') {
        violations.push('Image missing alt text');
      }
    }

    // Check for form labels
    const inputs = await this.page.locator('input, textarea, select').all();
    for (const input of inputs) {
      const id = await input.getAttribute('id');
      const ariaLabel = await input.getAttribute('aria-label');
      const ariaLabelledby = await input.getAttribute('aria-labelledby');
      
      let hasLabel = false;
      
      if (id) {
        const label = await this.page.locator(`label[for="${id}"]`).count();
        hasLabel = label > 0;
      }
      
      if (!hasLabel && !ariaLabel && !ariaLabelledby) {
        violations.push(`Form input missing label: ${await input.getAttribute('outerHTML')}`);
      }
    }

    // Check for proper button text
    const buttons = await this.page.locator('button, [role="button"]').all();
    for (const button of buttons) {
      const text = await button.textContent();
      const ariaLabel = await button.getAttribute('aria-label');
      
      if ((!text || text.trim().length === 0) && !ariaLabel) {
        violations.push('Button missing accessible text');
      }
    }

    return violations;
  }

  async calculateContrastRatio(foreground, background) {
    // Simplified contrast calculation - use a proper library in production
    return await this.page.evaluate(([fg, bg]) => {
      // This would need a proper color contrast calculation implementation
      // For now, return a placeholder value
      return 4.5; // Placeholder
    }, [foreground, background]);
  }

  generateSummary(results) {
    const criticalCount = results.violations.filter(v => v.impact === 'critical').length;
    const seriousCount = results.violations.filter(v => v.impact === 'serious').length;
    const moderateCount = results.violations.filter(v => v.impact === 'moderate').length;
    const minorCount = results.violations.filter(v => v.impact === 'minor').length;

    return {
      totalViolations: results.violations.length,
      criticalCount,
      seriousCount,
      moderateCount,
      minorCount,
      passCount: results.passes.length,
      incompleteCount: results.incomplete.length
    };
  }

  generateReport(auditResults) {
    const { violations, summary } = auditResults;
    
    let report = `
Accessibility Audit Report
==========================
Date: ${new Date().toISOString()}

Summary:
--------
Total Violations: ${summary.totalViolations}
- Critical: ${summary.criticalCount}
- Serious: ${summary.seriousCount}
- Moderate: ${summary.moderateCount}
- Minor: ${summary.minorCount}

Passed Tests: ${summary.passCount}
Incomplete Tests: ${summary.incompleteCount}

Detailed Violations:
-------------------
`;

    violations.forEach((violation, index) => {
      report += `
${index + 1}. ${violation.id} (${violation.impact})
   Description: ${violation.description}
   Help: ${violation.help}
   Tags: ${violation.tags.join(', ')}
   Affected Elements: ${violation.nodes.length}
   
   WCAG Guidelines:
   ${violation.tags.filter(tag => tag.startsWith('wcag')).join(', ')}
   
   How to Fix:
   ${violation.helpUrl}
   
   Example Fix:
   ${this.generateFixExample(violation)}
   
-------------------`;
    });

    return report;
  }

  generateFixExample(violation) {
    const examples = {
      'color-contrast': `
// Ensure text has sufficient color contrast
.text-element {
  color: #000000; /* Dark text */
  background-color: #ffffff; /* Light background */
  /* Contrast ratio: 21:1 (WCAG AAA) */
}

// For large text (18px+ or 14px+ bold)
.large-text {
  color: #666666; /* Lighter text acceptable */
  background-color: #ffffff;
  /* Contrast ratio: 5.7:1 (WCAG AA Large Text) */
}`,

      'image-alt': `
<!-- Good: Descriptive alt text -->
<img src="chart.png" alt="Sales increased 25% from Q1 to Q2">

<!-- Good: Decorative image -->
<img src="decoration.png" alt="" role="presentation">

<!-- Good: Complex image with description -->
<img src="complex-chart.png" alt="Q2 Sales Data" aria-describedby="chart-desc">
<div id="chart-desc">Detailed description of the sales chart...</div>`,

      'label': `
<!-- Good: Explicit label -->
<label for="email">Email Address</label>
<input type="email" id="email" name="email">

<!-- Good: Implicit label -->
<label>
  Email Address
  <input type="email" name="email">
</label>

<!-- Good: aria-label -->
<input type="email" aria-label="Email Address" name="email">`,

      'heading-order': `
<!-- Good: Proper heading hierarchy -->
<h1>Main Page Title</h1>
  <h2>Section Title</h2>
    <h3>Subsection Title</h3>
    <h3>Another Subsection</h3>
  <h2>Another Section</h2>

<!-- Bad: Skipped heading level -->
<h1>Main Title</h1>
  <h3>This skips h2!</h3> <!-- Should be h2 -->`,

      'button-name': `
<!-- Good: Button with text -->
<button>Save Changes</button>

<!-- Good: Button with aria-label -->
<button aria-label="Close dialog">×</button>

<!-- Good: Button with accessible text -->
<button>
  <span class="icon" aria-hidden="true">🔒</span>
  Lock Account
</button>`
    };

    return examples[violation.id] || '// No example available for this violation type';
  }
}

// Test implementation
test.describe('Accessibility Audit', () => {
  let accessibilityTester;

  test.beforeEach(async ({ page }) => {
    accessibilityTester = new AccessibilityTester(page);
  });

  test('homepage accessibility audit', async ({ page }) => {
    const results = await accessibilityTester.runFullAudit('/');
    
    // Generate and save report
    const report = accessibilityTester.generateReport(results);
    console.log(report);
    
    // Assert no critical or serious violations
    const criticalViolations = results.violations.filter(v => v.impact === 'critical');
    const seriousViolations = results.violations.filter(v => v.impact === 'serious');
    
    expect(criticalViolations).toHaveLength(0);
    expect(seriousViolations).toHaveLength(0);
  });

  test('keyboard navigation test', async ({ page }) => {
    await page.goto('/');
    const violations = await accessibilityTester.testKeyboardNavigation();
    
    expect(violations).toHaveLength(0);
  });

  test('screen reader compatibility', async ({ page }) => {
    await page.goto('/');
    const violations = await accessibilityTester.testScreenReaderCompatibility();
    
    expect(violations).toHaveLength(0);
  });

  test('color contrast compliance', async ({ page }) => {
    await page.goto('/');
    const violations = await accessibilityTester.testColorContrast();
    
    // Allow minor contrast issues but no major ones
    const majorViolations = violations.filter(v => v.contrastRatio < 3);
    expect(majorViolations).toHaveLength(0);
  });
});

export { AccessibilityTester };
```

## Example 2

```markdown
# Manual Accessibility Testing Checklist

## 1. Keyboard Navigation Testing

### Tab Navigation
- [ ] All interactive elements are reachable via Tab key
- [ ] Tab order is logical and follows visual layout
- [ ] No keyboard traps (can escape from all elements)
- [ ] Skip links are available and functional
- [ ] Custom interactive elements respond to Enter/Space

### Keyboard Shortcuts
- [ ] Standard shortcuts work (Ctrl+Z, Ctrl+C, etc.)
- [ ] Custom shortcuts are documented
- [ ] Shortcuts don't conflict with screen reader shortcuts
- [ ] Escape key closes modals and dropdowns

## 2. Screen Reader Testing

### NVDA Testing (Windows)
1. Install NVDA (free screen reader)
2. Start NVDA with Ctrl+Alt+N
3. Navigate with:
   - Tab: Next focusable element
   - H: Next heading
   - K: Next link
   - F: Next form field
   - G: Next graphic

### Testing Checklist
- [ ] All content is announced
- [ ] Headings provide good page structure
- [ ] Form labels are clear and associated
- [ ] Error messages are announced
- [ ] Live regions announce updates
- [ ] Images have appropriate alt text

### VoiceOver Testing (macOS)
1. Enable VoiceOver: Cmd+F5
2. Use VoiceOver cursor: Ctrl+Option+Arrow keys
3. Test web navigation: Ctrl+Option+U (Web Rotor)

### Testing Commands
- Ctrl+Option+H: Next heading
- Ctrl+Option+L: Next link
- Ctrl+Option+J: Next form control
- Ctrl+Option+G: Next graphic

## 3. Mobile Accessibility Testing

### iOS VoiceOver
1. Settings > Accessibility > VoiceOver > On
2. Triple-click home button to toggle
3. Swipe right to navigate
4. Double-tap to activate

### Android TalkBack
1. Settings > Accessibility > TalkBack > On
2. Swipe right to navigate
3. Double-tap to activate
4. Two-finger swipe to scroll

### Mobile Checklist
- [ ] Touch targets are at least 44x44 pixels
- [ ] Gestures are accessible
- [ ] Text can be resized to 200%
- [ ] Orientation changes work properly
- [ ] Voice control works

## 4. Visual Accessibility Testing

### Color and Contrast
- [ ] Text contrast meets WCAG AA (4.5:1 normal, 3:1 large)
- [ ] Color is not the only way to convey information
- [ ] Focus indicators are visible and high contrast
- [ ] Error states don't rely only on color

### Visual Design
- [ ] Content is readable at 200% zoom
- [ ] No horizontal scrolling at 320px width
- [ ] Text reflow works properly
- [ ] Important content remains visible when zoomed

## 5. Cognitive Accessibility Testing

### Content and Language
- [ ] Language is clear and simple
- [ ] Instructions are easy to understand
- [ ] Error messages are helpful
- [ ] Consistent navigation and layout
- [ ] No auto-playing audio/video

### Time and Interaction
- [ ] No time limits or they're adjustable
- [ ] Auto-refresh can be paused or disabled
- [ ] Animations can be reduced/disabled
- [ ] Content doesn't flash more than 3 times per second

## 6. Form Accessibility Testing

### Labels and Instructions
- [ ] All form fields have labels
- [ ] Required fields are clearly marked
- [ ] Field format requirements are explained
- [ ] Group related fields with fieldsets

### Error Handling
- [ ] Errors are clearly identified
- [ ] Error messages are helpful and specific
- [ ] Errors are associated with relevant fields
- [ ] Success messages are provided

### Validation
- [ ] Client-side validation is accessible
- [ ] Server-side validation provides accessible feedback
- [ ] Progressive enhancement works without JavaScript
```

## Example 3

```javascript
// jest.config.js - Jest configuration for accessibility testing
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/src/tests/setup.js'],
  testMatch: ['**/__tests__/**/*.test.js', '**/?(*.)+(spec|test).js'],
  collectCoverageFrom: [
    'src/**/*.{js,jsx}',
    '!src/tests/**',
    '!src/stories/**'
  ]
};

// src/tests/setup.js - Test setup with jest-axe
import 'jest-axe/extend-expect';
import { configureAxe } from 'jest-axe';

// Configure axe for testing
const axe = configureAxe({
  rules: {
    // Disable rules that aren't relevant for unit tests
    'document-title': { enabled: false },
    'html-has-lang': { enabled: false },
    'landmark-one-main': { enabled: false },
    'page-has-heading-one': { enabled: false }
  }
});

global.axe = axe;

// src/components/Button/Button.test.js - Component accessibility testing
import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { axe, toHaveNoViolations } from 'jest-axe';
import Button from './Button';

expect.extend(toHaveNoViolations);

describe('Button Accessibility', () => {
  test('should not have accessibility violations', async () => {
    const { container } = render(<Button>Click me</Button>);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  test('should be focusable and clickable via keyboard', async () => {
    const user = userEvent.setup();
    const handleClick = jest.fn();
    
    render(<Button onClick={handleClick}>Click me</Button>);
    
    const button = screen.getByRole('button', { name: /click me/i });
    
    // Focus via keyboard
    await user.tab();
    expect(button).toHaveFocus();
    
    // Click via keyboard
    await user.keyboard('{Enter}');
    expect(handleClick).toHaveBeenCalledTimes(1);
    
    await user.keyboard(' ');
    expect(handleClick).toHaveBeenCalledTimes(2);
  });

  test('should have proper ARIA attributes when disabled', () => {
    render(<Button disabled>Disabled button</Button>);
    
    const button = screen.getByRole('button');
    expect(button).toHaveAttribute('aria-disabled', 'true');
    expect(button).toBeDisabled();
  });

  test('should support ARIA label when needed', async () => {
    const { container } = render(
      <Button aria-label="Close dialog">×</Button>
    );
    
    const button = screen.getByRole('button', { name: /close dialog/i });
    expect(button).toBeInTheDocument();
    
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});

// Storybook accessibility addon configuration
// .storybook/main.js
module.exports = {
  addons: [
    '@storybook/addon-essentials',
    '@storybook/addon-a11y',
    '@storybook/addon-controls'
  ]
};

// .storybook/preview.js
import { INITIAL_VIEWPORTS } from '@storybook/addon-viewport';

export const parameters = {
  a11y: {
    config: {
      rules: [
        {
          id: 'color-contrast',
          enabled: true
        },
        {
          id: 'keyboard-navigation',
          enabled: true
        }
      ]
    },
    options: {
      checks: { 'color-contrast': { options: { noScroll: true } } },
      restoreScroll: true
    }
  },
  viewport: {
    viewports: INITIAL_VIEWPORTS
  }
};
```

## Example 4

```javascript
// src/components/AccessibleModal/AccessibleModal.jsx
import React, { useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';
import FocusTrap from 'focus-trap-react';

const AccessibleModal = ({ 
  isOpen, 
  onClose, 
  title, 
  children, 
  ariaLabelledby,
  ariaDescribedby 
}) => {
  const modalRef = useRef(null);
  const previousActiveElement = useRef(null);

  useEffect(() => {
    if (isOpen) {
      // Store the previously focused element
      previousActiveElement.current = document.activeElement;
      
      // Prevent body scroll
      document.body.style.overflow = 'hidden';
      
      // Set focus to modal
      if (modalRef.current) {
        modalRef.current.focus();
      }
    } else {
      // Restore body scroll
      document.body.style.overflow = '';
      
      // Return focus to previously focused element
      if (previousActiveElement.current) {
        previousActiveElement.current.focus();
      }
    }

    return () => {
      document.body.style.overflow = '';
    };
  }, [isOpen]);

  // Handle escape key
  useEffect(() => {
    const handleEscape = (event) => {
      if (event.key === 'Escape' && isOpen) {
        onClose();
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const modalContent = (
    <div className="modal-overlay" onClick={onClose}>
      <FocusTrap>
        <div
          ref={modalRef}
          className="modal-content"
          role="dialog"
          aria-modal="true"
          aria-labelledby={ariaLabelledby || 'modal-title'}
          aria-describedby={ariaDescribedby}
          tabIndex={-1}
          onClick={(e) => e.stopPropagation()}
        >
          <div className="modal-header">
            <h2 id="modal-title" className="modal-title">
              {title}
            </h2>
            <button
              className="modal-close"
              onClick={onClose}
              aria-label="Close dialog"
            >
              ×
            </button>
          </div>
          <div className="modal-body">
            {children}
          </div>
        </div>
      </FocusTrap>
    </div>
  );

  return createPortal(modalContent, document.body);
};

// CSS for modal
const modalStyles = `
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  max-width: 90vw;
  max-height: 90vh;
  overflow: auto;
  border-radius: 4px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  outline: none;
}

.modal-content:focus {
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.5);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid #e0e0e0;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.25rem;
  line-height: 1;
  color: #666;
}

.modal-close:hover,
.modal-close:focus {
  color: #000;
  outline: 2px solid #0066cc;
  outline-offset: 2px;
}

.modal-body {
  padding: 1rem;
}

/* Ensure good contrast for focus indicators */
*:focus {
  outline: 2px solid #0066cc;
  outline-offset: 2px;
}

/* Skip link styles */
.skip-link {
  position: absolute;
  top: -40px;
  left: 6px;
  background: #000;
  color: #fff;
  padding: 8px;
  text-decoration: none;
  border-radius: 0 0 4px 4px;
  z-index: 1001;
}

.skip-link:focus {
  top: 0;
}
`;

export default AccessibleModal;
```

## Example 5

```yaml
# WCAG 2.1 AA Compliance Checklist

# Principle 1: Perceivable
perceivable:
  - guideline_1_1: # Non-text Content
    - success_criterion_1_1_1: # Images of Text
      level: A
      description: "All non-text content has appropriate text alternatives"
      tests:
        - "Images have descriptive alt text"
        - "Decorative images marked with empty alt or role='presentation'"
        - "Complex images have long descriptions"
        - "CAPTCHAs have alternative forms"
  
  - guideline_1_2: # Time-based Media
    - success_criterion_1_2_1: # Audio-only and Video-only (Prerecorded)
      level: A
      description: "Audio-only and video-only content has alternatives"
    - success_criterion_1_2_2: # Captions (Prerecorded)
      level: A
      description: "Captions provided for prerecorded audio content"
    - success_criterion_1_2_3: # Audio Description or Media Alternative
      level: A
      description: "Audio description or full text alternative for video"

  - guideline_1_3: # Adaptable
    - success_criterion_1_3_1: # Info and Relationships
      level: A
      description: "Information structure preserved when presentation changes"
      tests:
        - "Proper heading hierarchy (h1-h6)"
        - "Form labels properly associated"
        - "Table headers identified"
        - "Lists marked up as lists"
    - success_criterion_1_3_2: # Meaningful Sequence
      level: A
      description: "Content order makes sense when linearized"
    - success_criterion_1_3_3: # Sensory Characteristics
      level: A
      description: "Instructions don't rely solely on sensory characteristics"

  - guideline_1_4: # Distinguishable
    - success_criterion_1_4_1: # Use of Color
      level: A
      description: "Color not the only means of conveying information"
    - success_criterion_1_4_2: # Audio Control
      level: A
      description: "Audio that plays automatically can be controlled"
    - success_criterion_1_4_3: # Contrast (Minimum)
      level: AA
      description: "Text has sufficient color contrast (4.5:1 normal, 3:1 large)"
    - success_criterion_1_4_4: # Resize Text
      level: AA
      description: "Text can be resized to 200% without assistive technology"
    - success_criterion_1_4_5: # Images of Text
      level: AA
      description: "Use actual text rather than images of text when possible"

# Principle 2: Operable
operable:
  - guideline_2_1: # Keyboard Accessible
    - success_criterion_2_1_1: # Keyboard
      level: A
      description: "All functionality available via keyboard"
      tests:
        - "All interactive elements reachable via Tab"
        - "All functionality works with keyboard"
        - "No keyboard traps"
    - success_criterion_2_1_2: # No Keyboard Trap
      level: A
      description: "Focus can move away from any component"
    - success_criterion_2_1_4: # Character Key Shortcuts
      level: A
      description: "Single character shortcuts can be turned off or remapped"

  - guideline_2_2: # Enough Time
    - success_criterion_2_2_1: # Timing Adjustable
      level: A
      description: "Time limits can be turned off, adjusted, or extended"
    - success_criterion_2_2_2: # Pause, Stop, Hide
      level: A
      description: "Moving, blinking, or auto-updating content can be controlled"

  - guideline_2_3: # Seizures and Physical Reactions
    - success_criterion_2_3_1: # Three Flashes or Below Threshold
      level: A
      description: "No content flashes more than 3 times per second"

  - guideline_2_4: # Navigable
    - success_criterion_2_4_1: # Bypass Blocks
      level: A
      description: "Skip links or other bypass mechanisms available"
    - success_criterion_2_4_2: # Page Titled
      level: A
      description: "Web pages have descriptive titles"
    - success_criterion_2_4_3: # Focus Order
      level: A
      description: "Focus order is logical and usable"
    - success_criterion_2_4_4: # Link Purpose (In Context)
      level: A
      description: "Link purpose clear from text or context"
    - success_criterion_2_4_5: # Multiple Ways
      level: AA
      description: "Multiple ways to locate web pages"
    - success_criterion_2_4_6: # Headings and Labels
      level: AA
      description: "Headings and labels describe topic or purpose"
    - success_criterion_2_4_7: # Focus Visible
      level: AA
      description: "Keyboard focus indicator is visible"

  - guideline_2_5: # Input Modalities
    - success_criterion_2_5_1: # Pointer Gestures
      level: A
      description: "Multipoint or path-based gestures have single-pointer alternative"
    - success_criterion_2_5_2: # Pointer Cancellation
      level: A
      description: "Functions triggered by single-pointer can be cancelled"
    - success_criterion_2_5_3: # Label in Name
      level: A
      description: "Accessible name contains visible label text"
    - success_criterion_2_5_4: # Motion Actuation
      level: A
      description: "Functions triggered by motion can be turned off"

# Principle 3: Understandable
understandable:
  - guideline_3_1: # Readable
    - success_criterion_3_1_1: # Language of Page
      level: A
      description: "Primary language of page is programmatically determined"
    - success_criterion_3_1_2: # Language of Parts
      level: AA
      description: "Language of content parts is programmatically determined"

  - guideline_3_2: # Predictable
    - success_criterion_3_2_1: # On Focus
      level: A
      description: "Focus doesn't trigger unexpected context changes"
    - success_criterion_3_2_2: # On Input
      level: A
      description: "Input doesn't trigger unexpected context changes"
    - success_criterion_3_2_3: # Consistent Navigation
      level: AA
      description: "Navigation is consistent across pages"
    - success_criterion_3_2_4: # Consistent Identification
      level: AA
      description: "Components with same functionality identified consistently"

  - guideline_3_3: # Input Assistance
    - success_criterion_3_3_1: # Error Identification
      level: A
      description: "Input errors are identified and described in text"
    - success_criterion_3_3_2: # Labels or Instructions
      level: A
      description: "Labels or instructions provided for user input"
    - success_criterion_3_3_3: # Error Suggestion
      level: AA
      description: "Error correction suggestions provided when possible"
    - success_criterion_3_3_4: # Error Prevention (Legal, Financial, Data)
      level: AA
      description: "Important submissions can be reversed, checked, or confirmed"

# Principle 4: Robust
robust:
  - guideline_4_1: # Compatible
    - success_criterion_4_1_1: # Parsing
      level: A
      description: "Content can be parsed reliably by assistive technologies"
    - success_criterion_4_1_2: # Name, Role, Value
      level: A
      description: "UI components have accessible name, role, and value"
    - success_criterion_4_1_3: # Status Messages
      level: AA
      description: "Status messages are programmatically determinable"
```

## Example 6

```yaml
# .github/workflows/accessibility.yml
name: Accessibility Testing

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  accessibility-tests:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: 18
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Build application
      run: npm run build
    
    - name: Start application
      run: |
        npm start &
        npx wait-on http://localhost:3000
    
    - name: Install accessibility testing tools
      run: |
        npm install -g @axe-core/cli
        npm install -g pa11y
        npm install -g lighthouse
    
    - name: Run axe-core accessibility tests
      run: |
        axe http://localhost:3000 \
          --tags wcag2a,wcag2aa,wcag21aa \
          --reporter json \
          --output axe-results.json
    
    - name: Run Pa11y accessibility tests
      run: |
        pa11y http://localhost:3000 \
          --standard WCAG2AA \
          --reporter json \
          --output pa11y-results.json
    
    - name: Run Lighthouse accessibility audit
      run: |
        lighthouse http://localhost:3000 \
          --only-categories=accessibility \
          --output=json \
          --output-path=lighthouse-a11y.json \
          --chrome-flags="--headless"
    
    - name: Run Playwright accessibility tests
      run: npx playwright test tests/accessibility/
    
    - name: Generate accessibility report
      run: |
        node scripts/generate-a11y-report.js
    
    - name: Upload accessibility artifacts
      uses: actions/upload-artifact@v3
      with:
        name: accessibility-reports
        path: |
          axe-results.json
          pa11y-results.json
          lighthouse-a11y.json
          accessibility-report.html
        retention-days: 30
    
    - name: Comment PR with accessibility results
      if: github.event_name == 'pull_request'
      uses: actions/github-script@v6
      with:
        script: |
          const fs = require('fs');
          const axeResults = JSON.parse(fs.readFileSync('axe-results.json', 'utf8'));
          
          const violationsCount = axeResults.violations.length;
          const passesCount = axeResults.passes.length;
          
          const comment = `
          ## Accessibility Test Results
          
          - ✅ **Passed**: ${passesCount} tests
          - ❌ **Failed**: ${violationsCount} tests
          
          ${violationsCount > 0 ? `
          ### Violations Found:
          ${axeResults.violations.map(v => `
          - **${v.id}** (${v.impact}): ${v.description}
            - Affected elements: ${v.nodes.length}
            - Help: ${v.helpUrl}
          `).join('')}
          ` : '🎉 No accessibility violations found!'}
          
          [View detailed report](${process.env.GITHUB_SERVER_URL}/${process.env.GITHUB_REPOSITORY}/actions/runs/${process.env.GITHUB_RUN_ID})
          `;
          
          github.rest.issues.createComment({
            issue_number: context.issue.number,
            owner: context.repo.owner,
            repo: context.repo.repo,
            body: comment
          });

  visual-accessibility:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: 18
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Color contrast testing
      run: |
        npm run test:contrast
    
    - name: Focus indicator testing
      run: |
        npm run test:focus-indicators
    
    - name: Text scaling testing
      run: |
        npm run test:text-scaling
```
