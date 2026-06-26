# Ekran Okuyucu Simülasyonu Paternleri

## Genel Bakış

Ekran okuyucu simülasyonu, gerçek kullanıcı deneyimini anlamak için kritik bir test yöntemidir. 
Bu belge, NVDA, JAWS ve VoiceOver davranışlarını simüle etmeyi açıklar.

## Ana Ekran Okuyucular

| Ekran Okuyucu | Platform | Pazar Payı | Test Önceliği |
|--------------|----------|------------|---------------|
| NVDA | Windows | %40+ | Yüksek |
| JAWS | Windows | %30+ | Yüksek |
| VoiceOver | macOS/iOS | %15+ | Yüksek |
| TalkBack | Android | %10+ | Orta |
| Narrator | Windows | %5+ | Orta |

## Okuma Modları

### Browse Mode (Okuma Modu)
- Sayfa içeriğini okuma
- Klavye kısayolları aktif (H, 1-6, T, F, vb.)
- Sanal imleç hareketi
- Form elementleri salt okunur

### Focus Mode (Form Modu)
- Form elementlerinde etkileşim
- Klavye kısayolları devre dışı
- Gerçek imleç hareketi
- Yazma ve seçim yapılabilir

### Mod Değiştirme
```
NVDA: Space/Shift+Space (toggle)
JAWS: Insert+Z (toggle)
VoiceOver: Control+Option+Shift+Down (interact)
```

## Navigasyon Paternleri

### Temel Navigasyon

| Tuş | NVDA | JAWS | VoiceOver |
|-----|------|------|-----------|
| Sonraki başlık | H | H | H |
| Başlık seviyesi | 1-6 | 1-6 | 1-6 |
| Sonraki link | U | U | VO+U |
| Sonraki form alanı | F | F | VO+J |
| Sonraki tablo | T | T | VO+T |
| Sonraki liste | L | L | VO+L |
| Sonraki buton | B | B | VO+B |
| Sonraki landmark | D | D | VO+U (landmarks) |
| Sonraki grafik | G | G | VO+G |

### İleri/Geri Tarama

```
NVDA:
- Tab: Sonraki interaktif element
- Shift+Tab: Önceki interaktif element
- Arrow keys: Karakter/satır/kelime hareketi
- Ctrl+Home/End: Sayfa başı/sonu

JAWS:
- Insert+F7: Element listesi
- Insert+F6: Başlık listesi
- Insert+Ctrl+Home: Sayfa başı

VoiceOver:
- VO+Right/Left: Sonraki/önceki element
- VO+Shift+Down: İçeriğe gir
- VO+Shift+Up: İçerikten çık
```

## İçerik Okuma Davranışı

### Başlık Okuma
```
HTML:
<h1>Ürün Kataloğu</h1>
<h2>Elektronik</h2>
  <h3>Akıllı Telefonlar</h3>

Ekran Okuyucu:
"Heading level 1, Ürün Kataloğu"
"Heading level 2, Elektronik"
"Heading level 3, Akıllı Telefonlar"
```

### Link Okuma
```
HTML:
<a href="/products">Ürünler</a>
<a href="/help" aria-label="Yardım al">?</a>
<a href="/cart">Sepet <span>3</span></a>

Ekran Okuyucu:
"Link, Ürünler"
"Link, Yardım al"
"Link, Sepet 3"
```

### Görsel Okuma
```
HTML:
<img src="chart.png" alt="2024 Satış Grafiği">
<img src="decoration.png" alt="">
<img src="icon.svg" aria-label="Ara">

Ekran Okuyucu:
"Graphic, 2024 Satış Grafiği"
[Atlanır - dekoratif]
"Graphic, Ara"
```

### Tablo Okuma
```
HTML:
<table>
  <caption>Ürün Listesi</caption>
  <thead>
    <tr><th>Ürün</th><th>Fiyat</th></tr>
  </thead>
  <tbody>
    <tr><td>Telefon</td><td>5000 TL</td></tr>
  </tbody>
</table>

Ekran Okuyucu:
"Table with 2 columns and 1 row, Ürün Listesi"
"Row 1, Ürün, Telefon, Fiyat, 5000 TL"
"Telefon, row 1, column 1"
"5000 TL, row 1, column 2"
```

### Form Okuma
```
HTML:
<label for="name">Ad Soyad</label>
<input type="text" id="name" required>
<span class="error">Bu alan zorunludur</span>

Ekran Okuyucu:
"Ad Soyad, edit, required, invalid data"
"Bu alan zorunludur"
```

## Simülasyon Protokolü

### 1. Sayfa Yükleme
```
1. Sayfa URL'sini aç
2. 3-5 saniye bekle (sayfa yüklenme simülasyonu)
3. İlk odaklanılabilir elemente git
4. Sayfa başlığını oku
5. Landmark'ları tanımla
```

### 2. Genel Tarama
```
1. Başlık hiyerarşisini takip et (H → 1 → 2 → 3...)
2. Ana landmark'ları gez (main, nav, aside)
3. Ana içerik bloklarını tanımla
4. İnteraktif elementleri say
```

### 3. Görev Odaklı Test
```
Senaryo: "Ürün ara ve sepete ekle"

1. Search landmark'a git (Ctrl+F "ara")
2. Arama formunu doldur
3. Sonuçları tara
4. Ürün detayına git
5. "Sepete ekle" butonunu bul ve tıkla
6. Onay mesajını dinle
7. Sepet sayısının güncellendiğini doğrula
```

### 4. Form Testi
```
1. Tab ile form alanlarına git
2. Her alan için: label, type, required, error mesajı
3. Hata durumunda: aria-invalid, aria-describedby
4. Submit sonrası: başarı/hata mesajı
```

## Yaygın Ekran Okuyucu Davranışları

### Duyurulacak İçerikler
```
✅ Duyurulur:
- Başlıklar (H1-H6)
- Linkler ve butonlar
- Form elementleri ve label'ları
- Landmark'lar
- Tablo başlıkları ve içeriği
- ARIA live regions
- hata mesajları

❌ Duyurulmaz (aria-hidden):
- Dekoratif elementler
- Gizli içerik
- aria-hidden="true" olan her şey
```

### Otomatik Duyurular
```
- Sayfa başlığı
- Landmark değişimi
- Liste başlangıcı/sonu
- Tablo boyutu
- Form durumu (required, invalid)
- Hata mesajları (aria-live)
```

### Focus Değişimi
```
Focus değiştiğinde duyurulur:
- Element türü (link, button, edit)
- Element ismi (label, aria-label, içeriği)
- Durum (expanded, selected, checked)
- Grup bilgisi (menü öğesi, liste öğesi)
```

## Test Scriptleri

### NVDA Simülasyonu
```python
def simulate_nvda_navigation(page):
    """NVDA benzeri sayfa taraması"""
    results = {
        'headings': [],
        'links': [],
        'forms': [],
        'landmarks': [],
        'images': []
    }
    
    # Başlık navigasyonu
    for h in page.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        level = int(h.name[1])
        text = h.get_text().strip()
        results['headings'].append({
            'level': level,
            'text': text,
            'announcement': f"Heading level {level}, {text}"
        })
    
    # Link navigasyonu
    for link in page.find_all('a'):
        text = link.get_text().strip() or link.get('aria-label', '')
        results['links'].append({
            'text': text,
            'href': link.get('href', ''),
            'announcement': f"Link, {text}"
        })
    
    return results
```

### VoiceOver Simülasyonu
```python
def simulate_voiceover_landmarks(page):
    """VoiceOver landmark navigasyonu"""
    landmarks = {
        'banner': page.find('header'),
        'navigation': page.find('nav'),
        'main': page.find('main'),
        'complementary': page.find('aside'),
        'contentinfo': page.find('footer'),
        'search': page.find(attrs={'role': 'search'})
    }
    
    announcements = []
    for role, element in landmarks.items():
        if element:
            label = element.get('aria-label', '')
            announcements.append(f"{role} landmark{', ' + label if label else ''}")
    
    return announcements
```

## Ekran Okuyucu Testi Kontrol Listesi

```
□ Sayfa başlığı anlamlı mı?
□ H1 var ve tek mi?
□ Başlık hiyerarşisi doğru mu?
□ Tüm linklerin anlamlı metni var mı?
□ Tüm görsellerin alt metni var mı?
□ Form etiketleri doğru mu?
□ Hata mesajları duyuruluyor mu?
□ Skip link var ve çalışıyor mu?
□ Landmark'lar doğru tanımlanmış mı?
□ Tablo başlıkları okunuyor mu?
□ Live regions çalışıyor mu?
□ Modal açıldığında focus doğru yere mi gidiyor?
□ Klavye kısayolları çalışıyor mu?
```

## Hızlı Test Yöntemleri

### 1. Linearize Test
```javascript
// Sayfa içeriğini linearize et
function linearizeContent() {
  const walker = document.createTreeWalker(
    document.body,
    NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT,
    null
  );
  
  let content = '';
  while (walker.nextNode()) {
    const node = walker.currentNode;
    if (node.nodeType === Node.TEXT_NODE && node.textContent.trim()) {
      content += node.textContent.trim() + '\n';
    } else if (node.nodeType === Node.ELEMENT_NODE) {
      const tag = node.tagName.toLowerCase();
      const role = node.getAttribute('role');
      // Landmark ve heading duyuruları ekle
    }
  }
  return content;
}
```

### 2. Focus Order Test
```javascript
// Focus sırası analizi
function analyzeFocusOrder() {
  const focusable = document.querySelectorAll(
    'a[href], button, input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  
  const order = [];
  focusable.forEach((el, i) => {
    order.push({
      index: i,
      tag: el.tagName,
      text: el.textContent?.trim().slice(0, 50),
      tabindex: el.getAttribute('tabindex'),
      isVisible: el.offsetParent !== null
    });
  });
  
  return order;
}
```

### 3. Heading Outline Test
```javascript
// Başlık dış hat analizi
function analyzeHeadingOutline() {
  const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
  const outline = [];
  let prevLevel = 0;
  
  headings.forEach(h => {
    const level = parseInt(h.tagName[1]);
    const text = h.textContent.trim();
    
    if (level - prevLevel > 1) {
      console.warn(`Heading skip: h${prevLevel} → h${level}`, h);
    }
    
    outline.push({
      level,
      text,
      skip: level - prevLevel > 1
    });
    
    prevLevel = level;
  });
  
  return outline;
}
```