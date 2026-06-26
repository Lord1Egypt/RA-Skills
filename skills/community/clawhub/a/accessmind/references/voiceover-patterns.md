# VoiceOver Navigasyon Desenleri

VoiceOver, macOS'un yerleşik ekran okuyucusudur. Bu belge, VoiceOver navigasyon desenlerini ve test tekniklerini içerir.

## VoiceOver Tuşları

| Tuş | Fonksiyon | Element Tipleri |
|-----|-----------|-----------------|
| H | Sonraki Başlık | h1-h6, [role="heading"] |
| U | Sonraki Link | a[href], [role="link"] |
| B | Sonraki Buton | button, [role="button"] |
| F | Sonraki Form | input, select, textarea, [role="form"] |
| D | Sonraksi Landmark | main, nav, header, footer, [role="region"] |
| T | Sonraki Tablo | table, [role="table"] |
| G | Sonraki Görsel | img, [role="img"] |
| L | Sonraki Liste | ul, ol, [role="list"] |
| X | Sonraki Checkbox | input[type="checkbox"], [role="checkbox"] |
| R | Sonraki Radio | input[type="radio"], [role="radio"] |

## Navigation Loop Algoritması

```python
def navigation_loop(page_url: str) -> List[ElementReport]:
    """
    Sayfadaki tüm elementleri gezerek eksiksiz erişilebilirlik analizi
    """
    
    results = []
    visited_elements = set()
    dynamic_content_elements = []
    
    # 1. Browser'ı hazırla
    browser = prepare_browser(page_url)
    
    # 2. Sayfayı yükle
    load_page(browser, page_url)
    
    # 3. Skip link'i kontrol et
    skip_links = find_skip_links(browser)
    for skip_link in skip_links:
        results.append(analyze_skip_link(skip_link))
    
    # 4. Landmark'ları bul
    landmarks = find_landmarks(browser)
    for landmark in landmarks:
        results.append(analyze_landmark(landmark))
    
    # 5. Ana navigasyon döngüsü
    end_of_page = False
    focusable_elements = get_all_focusable_elements(browser)
    
    while not end_of_page:
        element = get_next_focusable(focusable_elements, visited_elements)
        
        if element is None:
            end_of_page = True
            continue
        
        visited_elements.add(element.id)
        
        # Elementi analiz et
        report = analyze_element(element)
        results.append(report)
        
        # Eğer interaktif ise, etkileşimi simüle et
        if element.is_interactive():
            interaction_result = simulate_interaction(element)
            
            if interaction_result.content_changed:
                live_region = capture_live_region(element)
                dynamic_content_elements.append(live_region)
                results.append(analyze_live_region(live_region))
        
        # Dinamik içerik kontrolü
        if dynamic_content_changed(browser):
            capture_live_region(browser)
        
        store_result(element, report)
    
    # 6. Dinamik içerik elementlerini analiz et
    for dynamic_element in dynamic_content_elements:
        results.append(analyze_dynamic_content(dynamic_element))
    
    # 7. Sonuçları birleştir ve skorla
    final_report = generate_final_report(results)
    
    return final_report
```

## Focusable Element Bulma

```python
def get_all_focusable_elements(browser) -> List[Element]:
    """
    Sayfadaki tüm focusable elementleri bul
    """
    
    focusable_selectors = [
        'a[href]',           # Linkler
        'button',             # Butonlar
        'input',              # Form input'ları
        'select',             # Dropdown'lar
        'textarea',           # Metin alanları
        '[tabindex]',         # Tab index olanlar
        '[role="button"]',    # ARIA butonlar
        '[role="link"]',      # ARIA linkler
        '[role="checkbox"]',  # Checkbox'lar
        '[role="radio"]',     # Radyo düğmeleri
        '[role="tab"]',       # Tab'lar
        '[role="menuitem"]',  # Menü öğeleri
        '[role="combobox"]',  # Combobox'lar
        '[role="listbox"]',   # Listbox'lar
        '[role="slider"]',    # Slider'lar
    ]
    
    elements = []
    for selector in focusable_selectors:
        found = browser.find_elements(selector)
        elements.extend(found)
    
    return deduplicate_elements(elements)
```

## VoiceOver Simülasyonu

```python
class VoiceOverSimulator:
    """VoiceOver navigasyonunu simüle et"""
    
    def __init__(self, browser):
        self.browser = browser
        self.current_element = None
        self.announcements = []
    
    def press_key(self, key: str) -> dict:
        """VoiceOver tuşuna bas"""
        
        key_map = {
            'H': 'heading',
            'U': 'link',
            'B': 'button',
            'F': 'form',
            'D': 'landmark',
            'T': 'table',
            'G': 'graphic',
            'L': 'list',
            'X': 'checkbox',
            'R': 'radio'
        }
        
        element_type = key_map.get(key)
        if not element_type:
            return {'error': f'Unknown key: {key}'}
        
        # Sonraki elementi bul
        next_element = self.find_next(element_type)
        
        if next_element:
            self.current_element = next_element
            announcement = self.generate_announcement(next_element)
            self.announcements.append(announcement)
            return {
                'element': next_element,
                'announcement': announcement
            }
        else:
            return {
                'element': None,
                'announcement': f'Sonraki {element_type} bulunamadı'
            }
    
    def find_next(self, element_type: str) -> Optional[Element]:
        """Sonraki elementi bul"""
        
        selector_map = {
            'heading': 'h1, h2, h3, h4, h5, h6, [role="heading"]',
            'link': 'a[href], [role="link"]',
            'button': 'button, [role="button"]',
            'form': 'input, select, textarea, [role="form"]',
            'landmark': 'main, nav, header, footer, aside, section, [role="region"]',
            'table': 'table, [role="table"]',
            'graphic': 'img, [role="img"]',
            'list': 'ul, ol, [role="list"]',
            'checkbox': 'input[type="checkbox"], [role="checkbox"]',
            'radio': 'input[type="radio"], [role="radio"]'
        }
        
        selector = selector_map.get(element_type)
        elements = self.browser.find_elements(selector)
        
        # Mevcut elementten sonrakini bul
        if self.current_element:
            current_index = elements.index(self.current_element)
            if current_index < len(elements) - 1:
                return elements[current_index + 1]
        elif elements:
            return elements[0]
        
        return None
    
    def generate_announcement(self, element: Element) -> str:
        """VoiceOver duyurusu oluştur"""
        
        element_type = element.get_attribute('role') or element.tag_name.lower()
        
        # Element tipine göre duyuru
        announcements = {
            'heading': f"{element.text}, başlık seviyesi {element.get_attribute('aria-level') or '1'}",
            'link': f"{element.text or element.get_attribute('aria-label')}, link",
            'button': f"{element.text or element.get_attribute('aria-label')}, button",
            'graphic': f"{element.get_attribute('alt') or 'grafik'}, grafik",
            'checkbox': f"{element.get_attribute('aria-label') or element.text}, {'seçili' if element.get_attribute('checked') else 'seçili değil'}, onay kutusu",
            'radio': f"{element.get_attribute('aria-label') or element.text}, {'seçili' if element.get_attribute('checked') else 'seçili değil'}, radyo düğmesi",
        }
        
        return announcements.get(element_type, element.text or 'element')
```

## Klavye Erişilebilirlik Testleri

### Test 1: Focus Order (2.4.3)

```python
def test_focus_order(browser) -> dict:
    """Tab sırası mantıklı mı?"""
    
    focusable_elements = browser.find_elements('a[href], button, input, select, textarea, [tabindex]')
    focus_order = []
    
    for i, element in enumerate(focusable_elements):
        tabindex = element.get_attribute('tabindex')
        if tabindex and tabindex != '-1':
            # Pozitif tabindex kullanımı kötü
            if int(tabindex) > 0:
                return {
                    'status': 'fail',
                    'message': f'Pozitif tabindex kullanımı: {tabindex}',
                    'element': element
                }
        
        focus_order.append({
            'element': element,
            'order': i + 1
        })
    
    return {
        'status': 'pass',
        'focus_order': focus_order
    }
```

### Test 2: Focus Visible (2.4.7)

```python
def test_focus_visible(browser) -> dict:
    """Focus göstergesi görünür mü?"""
    
    focusable_elements = browser.find_elements('a[href], button, input, select, textarea, [tabindex]')
    issues = []
    
    for element in focusable_elements:
        # Elemente focus ol
        element.focus()
        
        # Focus stilini kontrol et
        styles = browser.evaluate_script('''
            const element = arguments[0];
            const styles = window.getComputedStyle(element, ':focus-visible');
            return {
                outline: styles.outline,
                boxShadow: styles.boxShadow,
                border: styles.border
            };
        ''', element)
        
        if styles['outline'] == 'none' and styles['boxShadow'] == 'none':
            issues.append({
                'element': element,
                'message': 'Focus göstergesi yok'
            })
    
    if issues:
        return {
            'status': 'fail',
            'issues': issues
        }
    
    return {
        'status': 'pass'
    }
```

### Test 3: Keyboard Trap (2.1.2)

```python
def test_keyboard_trap(browser) -> dict:
    """Klavye tuzağı var mı?"""
    
    # Modal ve dialog'ları bul
    modals = browser.find_elements('[role="dialog"], [role="modal"]')
    issues = []
    
    for modal in modals:
        # ESC tuşu ile çıkış var mı?
        has_close = modal.find_elements('button[aria-label*="kapat"], button[aria-label*="close"]')
        
        if not has_close:
            issues.append({
                'element': modal,
                'message': 'Modal ESC ile kapatılamıyor'
            })
    
    if issues:
        return {
            'status': 'fail',
            'issues': issues
        }
    
    return {
        'status': 'pass'
    }
```

## VoiceOver Test Sonuçları

```python
class VoiceOverTestResults:
    """VoiceOver test sonuçları"""
    
    def __init__(self):
        self.heading_test = None
        self.link_test = None
        self.button_test = None
        self.form_test = None
        self.landmark_test = None
        self.graphic_test = None
    
    def to_dict(self) -> dict:
        return {
            'heading': self.heading_test,
            'link': self.link_test,
            'button': self.button_test,
            'form': self.form_test,
            'landmark': self.landmark_test,
            'graphic': self.graphic_test
        }
```

## Dinamik İçerik (Live Regions)

```python
def capture_live_region(browser) -> dict:
    """
    Dinamik içerik değişikliklerini yakala
    
    Live region tipleri:
    - aria-live="polite"
    - aria-live="assertive"
    - aria-live="off"
    - role="status"
    - role="alert"
    - role="log"
    - role="marquee"
    - role="timer"
    """
    
    live_regions = browser.find_elements('[aria-live], [role="status"], [role="alert"], [role="log"], [role="marquee"], [role="timer"]')
    
    results = []
    for region in live_regions:
        aria_live = region.get_attribute('aria-live')
        role = region.get_attribute('role')
        content = region.text
        
        results.append({
            'type': aria_live or role,
            'content': content,
            'announcement': generate_voiceover_announcement(aria_live, content)
        })
    
    return results

def generate_voiceover_announcement(live_type: str, content: str) -> str:
    """Live region duyurusu oluştur"""
    
    if live_type == 'assertive':
        return f"DİKKAT: {content}"
    elif live_type == 'polite':
        return content
    elif role == 'alert':
        return f"UYARI: {content}"
    elif role == 'status':
        return content
    else:
        return content
```