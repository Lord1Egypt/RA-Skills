# Common E-commerce Popup Patterns

## Cookie Consent Popups

### German Market (DE)
```python
german_popup_selectors = [
    'button:has-text("Alle akzeptieren")',
    'button:has-text("Alle annehmen")',
    'button:has-text("Akzeptieren")',
    'button:has-text("Zustimmen")',
    'button:has-text("Einverstanden")',
    'button:has-text("OK")',
    'button:has-text("Verstanden")',
]
```

### English/International
```python
english_popup_selectors = [
    'button:has-text("Accept all")',
    'button:has-text("Accept")',
    'button:has-text("I agree")',
    'button:has-text("OK")',
    'button:has-text("Agree")',
]
```

### Universal Selectors (ID/Class-based)
```python
universal_selectors = [
    'button[id*="accept"]',
    'button[class*="accept"]',
    'button[id*="cookie"]',
    'button[class*="cookie"]',
    '#onetrust-accept-btn-handler',
    '.cookie-consent-accept',
    '[data-testid="uc-accept-all-button"]',
    '[data-testid="cookie-accept-all"]',
]
```

## Close Buttons

```python
close_button_selectors = [
    'button[aria-label*="close"]',
    'button[aria-label*="Close"]',
    'button[aria-label*="schließen"]',  # German
    'button[aria-label*="Schließen"]',
    'button.close',
    'button[class*="close"]',
    '[class*="close-button"]',
    'button:has-text("×")',
    'button:has-text("✕")',
]
```

## Newsletter/Marketing Popups

```python
dismiss_selectors = [
    'button:has-text("Nein")',  # No (German)
    'button:has-text("Später")',  # Later (German)
    'button:has-text("Nicht jetzt")',  # Not now (German)
    'button:has-text("No thanks")',
    'button:has-text("Maybe later")',
    'button:has-text("Not now")',
]
```

## Region/Country Selectors

### Common Patterns
```python
# Detect country selection popup
country_popup_patterns = [
    'button:has-text("Germany")',
    'button:has-text("Deutschland")',
    'select[name="country"]',
    '[data-testid="country-selector"]',
]
```

### Example: Vinted
```python
# Vinted-specific
germany_button = page.locator('button:has-text("Germany")').first
if await germany_button.is_visible(timeout=3000):
    await germany_button.click()
```

## Platform-Specific Selectors

### Kleinanzeigen.de
```python
'.uc-deny-all-button'
'#sp_message_iframe_953358'
```

### Generic E-commerce
```python
'.gdpr-accept',
'.cookie-banner-accept',
'#cookie-accept',
'.consent-accept-all',
```

## Multi-Round Detection Strategy

```python
async def close_popups_multi_round(page):
    """Close popups with multiple detection rounds"""
    # Round 1: Immediate popups
    await close_popups(page)
    await asyncio.sleep(1)

    # Round 2: Delayed popups
    await close_popups(page)
    await asyncio.sleep(2)

    # Final stabilization
```

## Timeout Strategy

- **Initial wait**: 2000ms per selector
- **Visibility check**: Use `is_visible(timeout=2000)` before clicking
- **Post-click wait**: 1 second to allow animation to complete
