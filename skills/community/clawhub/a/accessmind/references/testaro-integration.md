# Testaro Entegrasyonu

[Testaro](https://github.com/GoogleChromeLabs/testaro), Google Chrome Labs tarafından geliştirilen otomatik erişilebilirlik test framework'üdür. AccessMind ile entegre çalışır.

## Kurulum

```bash
# NPM ile Testaro kurulumu
npm install @axe-core/testaro

# veya Python wrapper
pip install testaro-python
```

## Test Türleri

| Test Adı | Açıklama | WCAG |
|----------|----------|------|
| `focused` | Focusable elementlere odaklanılabilir mi? | 2.1.1 |
| `focusedAway` | Focus göstergesi görünür mü? | 2.4.7 |
| `interactive` | İnteraktif elementler klavye ile aktifleştirilebilir mi? | 2.1.1 |
| `tabOrder` | Tab sırası mantıklı mı? | 2.4.3 |
| `keyboardTrap` | Klavye tuzağı var mı? | 2.1.2 |
| `ariaValid` | ARIA öznitelikleri geçerli mi? | 4.1.2 |
| `focusVisible` | Focus göstergesi var mı? | 2.4.7 |
| `focusSequence` | Focus sırası DOM sırasını takip ediyor mu? | 2.4.3 |
| `elementRole` | Element rolü doğru mu? | 4.1.2 |
| `elementName` | Element ismi var mı? | 4.1.2 |
| `elementState` | Element durumu doğru mu? | 4.1.2 |

## Testaro Kullanımı

```python
from testaro import Testaro

# Testaro başlat
testaro = Testaro(browser='chrome')

# Test çalıştır
results = testaro.run_tests(
    url='https://example.com',
    tests=['focused', 'focusedAway', 'interactive', 'tabOrder', 'keyboardTrap', 'ariaValid']
)

# Sonuçları al
for result in results:
    print(f"{result.test_name}: {result.status}")
    print(f"  Element: {result.element}")
    print(f"  Message: {result.message}")
```

## AccessMind Entegrasyonu

```python
class TestaroIntegration:
    """Testaro erişilebilirlik testlerini AccessMind ile entegre et"""
    
    def __init__(self):
        self.testaro = Testaro()
        self.accessmind = AccessMind()
    
    async def run_full_audit(self, url: str) -> dict:
        """Tam entegre denetim"""
        
        results = {
            'testaro': {},
            'accessmind': {},
            'combined': {}
        }
        
        # 1. Testaro testleri
        testaro_results = await self.testaro.run_all_tests(url)
        results['testaro'] = testaro_results
        
        # 2. AccessMind analizi
        accessmind_results = await self.accessmind.analyze(url)
        results['accessmind'] = accessmind_results
        
        # 3. Sonuçları birleştir
        results['combined'] = self.merge_results(testaro_results, accessmind_results)
        
        return results
```

## Testaro Test Kodları

```javascript
// Focusable Test
testaro.focused = async (page, element) => {
    await element.focus();
    return document.activeElement === element;
};

// Focus Visible Test
testaro.focusedAway = async (page, element) => {
    const styles = getComputedStyle(element, ':focus-visible');
    return styles.outline !== 'none' || styles.boxShadow !== 'none';
};

// Interactive Test
testaro.interactive = async (page, element) => {
    const role = element.getAttribute('role');
    const tagName = element.tagName.toLowerCase();
    const interactiveRoles = ['button', 'link', 'checkbox', 'radio', 'tab', 'menuitem'];
    const interactiveTags = ['a', 'button', 'input', 'select', 'textarea'];
    
    return interactiveRoles.includes(role) || interactiveTags.includes(tagName);
};

// Tab Order Test
testaro.tabOrder = async (page) => {
    const focusableElements = await page.$$('a[href], button, input, select, textarea, [tabindex]');
    const tabIndexes = [];
    
    for (const el of focusableElements) {
        const tabindex = await el.getAttribute('tabindex');
        if (tabindex && tabindex !== '-1') {
            tabIndexes.push(parseInt(tabindex));
        }
    }
    
    // Pozitif tabindex kullanımı kötü
    return tabIndexes.filter(i => i > 0).length === 0;
};

// Keyboard Trap Test
testaro.keyboardTrap = async (page, element) => {
    const role = element.getAttribute('role');
    if (['dialog', 'modal'].includes(role)) {
        const hasCloseButton = await element.$('button[aria-label*="kapat"], button[aria-label*="close"]');
        return hasCloseButton !== null;
    }
    return true;
};

// ARIA Valid Test
testaro.ariaValid = async (page, element) => {
    const ariaAttributes = [...element.attributes].filter(attr => attr.name.startsWith('aria-'));
    
    for (const attr of ariaAttributes) {
        if (attr.name === 'aria-expanded' && !['true', 'false'].includes(attr.value)) {
            return false;
        }
        if (attr.name === 'aria-pressed' && !['true', 'false', 'mixed'].includes(attr.value)) {
            return false;
        }
    }
    
    return true;
};
```

## Navigation Loop Entegrasyonu

```python
async def run_complete_audit(url: str) -> dict:
    """
    Navigation Loop + Testaro entegrasyonu
    """
    
    results = {
        'navigation_loop': [],
        'testaro': {},
        'accessmind': {},
        'combined': {
            'passed': [],
            'failed': [],
            'warnings': []
        }
    }
    
    # 1. Browser'ı hazırla
    browser = prepare_browser(url)
    
    # 2. Testaro testlerini çalıştır
    testaro = TestaroIntegration()
    results['testaro'] = await testaro.run_all_tests(browser)
    
    # 3. Navigation loop
    end_of_page = False
    visited_elements = set()
    focusable_elements = get_all_focusable_elements(browser)
    
    while not end_of_page:
        element = get_next_focusable(focusable_elements, visited_elements)
        
        if element is None:
            end_of_page = True
            continue
        
        visited_elements.add(element.id)
        
        # AccessMind analizi
        accessmind_report = analyze_element(element)
        results['navigation_loop'].append(accessmind_report)
        
        # Testaro testleri
        testaro_results = await testaro.run_element_tests(element)
        
        # Sonuçları birleştir
        if testaro_results['failed']:
            results['combined']['failed'].extend(testaro_results['failed'])
        if testaro_results['warnings']:
            results['combined']['warnings'].extend(testaro_results['warnings'])
        if testaro_results['passed']:
            results['combined']['passed'].extend(testaro_results['passed'])
    
    # 4. Toplu sonuçları üret
    results['accessmind'] = generate_accessmind_report(results['navigation_loop'])
    
    return results
```

## Sonuç Formatı

```javascript
{
    "testaro": {
        "focused": {
            "status": "pass",
            "elements": [
                { "element": "a[href='#main']", "passed": true },
                { "element": "button.submit", "passed": true }
            ]
        },
        "focusedAway": {
            "status": "fail",
            "elements": [
                { 
                    "element": "button.menu",
                    "passed": false,
                    "message": "No focus indicator"
                }
            ]
        },
        "tabOrder": {
            "status": "pass",
            "tabIndexes": []
        },
        "keyboardTrap": {
            "status": "pass",
            "traps": []
        },
        "ariaValid": {
            "status": "pass",
            "invalidAttributes": []
        }
    }
}
```

## Kullanım Senaryoları

### Senaryo 1: Hızlı Tarama

```python
# Sadece kritik testler
results = await testaro.run_tests(
    url='https://example.com',
    tests=['focused', 'keyboardTrap', 'ariaValid']
)

for result in results:
    if result.status == 'fail':
        print(f"❌ {result.test_name}: {result.message}")
```

### Senaryo 2: Kapsamlı Denetim

```python
# Tüm testler + AccessMind
audit = await run_complete_audit('https://example.com')

# Kritik ihlaller
critical = [r for r in audit['combined']['failed'] if r['severity'] == 'critical']

for issue in critical:
    print(f"🔴 {issue['test']}: {issue['message']}")
    print(f"   Element: {issue['element']}")
    print(f"   Fix: {issue['fix']}")
```

### Senaryo 3: Karşılaştırma

```python
# İki sayfayı karşılaştır
page1 = await run_complete_audit('https://site.com/page1')
page2 = await run_complete_audit('https://site.com/page2')

# Skor karşılaştırma
print(f"Page 1 Score: {page1['score']}")
print(f"Page 2 Score: {page2['score']}")

# İyileştirme oranları
improvement = (page2['score'] - page1['score']) / page1['score'] * 100
print(f"Improvement: {improvement}%")
```