# Mobile Accessibility Testing Guide

## iOS Testing

### VoiceOver Testing
```python
from accessmind import IOSAuditor

auditor = IOSAuditor(app="MyApp.ipa")

# VoiceOver commands
vo_commands = [
    "swipe_right",  # Next element
    "swipe_left",   # Previous element
    "double_tap",   # Activate
    "two_finger_swipe_up",  # Read all
    "two_finger_swipe_down", # Stop reading
    "three_finger_swipe_up", # Scroll up
    "three_finger_swipe_down", # Scroll down
]

for cmd in vo_commands:
    result = auditor.test_voiceover(command=cmd)
    print(f"{cmd}: {result.announcement}")
```

### Dynamic Type Testing
```python
# Test text scaling
for size in ["XS", "S", "M", "L", "XL", "XXL", "XXXL"]:
    auditor.set_dynamic_type(size)
    result = auditor.test_layout()
    if result.overflow:
        print(f"⚠️ Layout overflow at {size}")
```

### Switch Control Testing
```python
# Test switch control navigation
auditor.enable_switch_control()

# Navigate through elements
while not auditor.end_of_elements():
    element = auditor.get_current_element()
    print(f"Element: {element.name}, Type: {element.type}")
    auditor.switch_next()
```

## Android Testing

### TalkBack Testing
```python
from accessmind import AndroidAuditor

auditor = AndroidAuditor(apk="MyApp.apk")

# TalkBack gestures
tb_gestures = [
    "swipe_right",  # Next element
    "swipe_left",   # Previous element
    "double_tap",   # Activate
    "swipe_down",   # Next granularity
    "swipe_up",     # Previous granularity
]

for gesture in tb_gestures:
    result = auditor.test_talkback(gesture=gesture)
    print(f"{gesture}: {result.announcement}")
```

### Accessibility Scanner
```python
# Run Accessibility Scanner
scanner_results = auditor.run_accessibility_scanner()

for suggestion in scanner_results.suggestions:
    print(f"⚠️ {suggestion.title}")
    print(f"   {suggestion.description}")
    print(f"   Path: {suggestion.path}")
```

### Switch Access Testing
```python
# Test switch access
auditor.enable_switch_access()

while not auditor.end_of_elements():
    element = auditor.get_current_element()
    print(f"Element: {element.content_description}")
    auditor.switch_next()
```

## Testing Checklist

### iOS Checklist
- [ ] VoiceOver navigation works
- [ ] All elements have accessibility labels
- [ ] Dynamic Type support (XS to XXXL)
- [ ] Switch Control navigation
- [ ] Color contrast (4.5:1 minimum)
- [ ] Touch targets (44x44 minimum)
- [ ] Reduced motion support
- [ ] Bold text support
- [ ] Smart invert support
- [ ] Voice Control compatible

### Android Checklist
- [ ] TalkBack navigation works
- [ ] All elements have content descriptions
- [ ] Text scaling works
- [ ] Switch Access navigation
- [ ] Color contrast (4.5:1 minimum)
- [ ] Touch targets (48x48 minimum)
- [ ] Reduced motion support
- [ ] Font size support
- [ ] Color inversion compatible
- [ ] Voice Access compatible

## Device Matrix

### iOS Devices
| Device | iOS Version | Screen Size | Notes |
|--------|-------------|-------------|-------|
| iPhone 14 Pro | iOS 17 | 6.1" | Dynamic Island |
| iPhone 14 | iOS 17 | 6.1" | Standard |
| iPhone SE (3rd) | iOS 17 | 4.7" | Small screen |
| iPad Pro 12.9" | iPadOS 17 | 12.9" | Tablet |
| iPad Air | iPadOS 17 | 10.9" | Tablet |

### Android Devices
| Device | Android Version | Screen Size | Notes |
|---------|-----------------|-------------|-------|
| Pixel 7 | Android 14 | 6.3" | Stock Android |
| Pixel 6 | Android 14 | 6.4" | Stock Android |
| Samsung S23 | Android 14 | 6.1" | One UI |
| Samsung Tab S8 | Android 14 | 11.0" | Tablet |

## Automated Testing Tools

### XCTest (iOS)
```swift
import XCTest

class AccessibilityTests: XCTestCase {
    func testVoiceOverNavigation() {
        let app = XCUIApplication()
        app.launch()
        
        // Verify all elements are accessible
        for element in app.allElementsBoundByIndex {
            XCTAssertTrue(element.isAccessibilityElement, 
                "Element \(element) should be accessible")
        }
    }
}
```

### Espresso (Android)
```kotlin
import androidx.test.espresso.Espresso
import androidx.test.espresso.accessibility.AccessibilityChecks

@RunWith(AndroidJUnit4::class)
class AccessibilityTests {
    @Test
    fun testAccessibility() {
        AccessibilityChecks.enable()
        
        // Run accessibility checks
        Espresso.onView(ViewMatchers.isRoot())
            .check(AccessibilityViewCheck())
    }
}
```