# ARIA Rehberi

## ARIA Nedir?

ARIA (Accessible Rich Internet Applications), HTML elementlerine anlamsal bilgi ekleyerek 
erişilebilirliği artıran bir W3C spesifikasyonudur.

## Altın Kurallar

1. **Native HTML önce**: ARIA yerine semantic HTML kullan
2. **Değiştirme, ekle**: ARIA native anlamı değiştirmez, ekler
3. **Klavye şart**: Interactive ARIA elementler klavye erişilebilir olmalı
4. **Test et**: Gerçek ekran okuyucu ile test et

## Rolleri

### Document Structure Roles

| Role | Açıklama | HTML Alternatifi |
|------|----------|------------------|
| `article` | Bağımsız içerik | `<article>` |
| `banner` | Site başlığı | `<header>` (main dışı) |
| `complementary` | Tamamlayıcı içerik | `<aside>` |
| `contentinfo` | Site alt bilgisi | `<footer>` |
| `main` | Ana içerik | `<main>` |
| `navigation` | Navigasyon | `<nav>` |
| `region` | Bölüm | `<section>` + aria-labelledby |
| `search` | Arama alanı | `<form role="search">` |

### Widget Roles

| Role | Açıklama | Gerekli Özellikler |
|------|----------|-------------------|
| `button` | Buton | `aria-pressed` (toggle) |
| `checkbox` | Onay kutusu | `aria-checked` |
| `dialog` | Dialog/modal | `aria-modal`, `aria-labelledby` |
| `grid` | Tablo grid | `aria-rowcount`, `aria-colcount` |
| `listbox` | Seçim listesi | `aria-activedescendant` |
| `menu` | Menü | `aria-expanded` |
| `menubar` | Yatay menü | Keyboard navigation |
| `menuitem` | Menü öğesi | |
| `option` | Seçenek | `aria-selected` |
| `progressbar` | İlerleme | `aria-valuenow`, `aria-valuemin`, `aria-valuemax` |
| `radio` | Radyo buton | `aria-checked` |
| `radiogroup` | Radyo grubu | `aria-activedescendant` |
| `slider` | Kaydırıcı | `aria-valuenow`, `aria-valuemin`, `aria-valuemax` |
| `spinbutton` | Sayı girişi | `aria-valuenow`, `aria-valuemin`, `aria-valuemax` |
| `tab` | Sekme | `aria-selected`, `aria-controls` |
| `tablist` | Sekme listesi | |
| `tabpanel` | Sekme paneli | `aria-labelledby` |
| `textbox` | Metin kutusu | |
| `toolbar` | Araç çubuğu | |
| `tooltip` | Araç ipucu | |

### Landmark Roles

```html
<!-- Otomatik landmark'lar -->
<header> → role="banner"
<nav> → role="navigation"
<main> → role="main"
<aside> → role="complementary"
<footer> → role="contentinfo"
<form> → role="form" (aria-label ile)
<section> → role="region" (aria-label ile)

<!-- ARIA ile landmark -->
<div role="main">...</div>
<nav aria-label="Ana navigasyon">...</nav>
<aside aria-labelledby="sidebar-title">
  <h2 id="sidebar-title">İlgili İçerikler</h2>
</aside>
```

## States ve Properties

### Global States/Properties

| Özellik | Açıklama | Değerler |
|---------|----------|----------|
| `aria-hidden` | İçeriği gizle | `true`, `false` |
| `aria-label` | Erişilebilir isim | Metin |
| `aria-labelledby` | Referans ile isimlendirme | ID listesi |
| `aria-describedby` | Açıklama referansı | ID listesi |
| `aria-live` | Dinamik içerik duyurusu | `off`, `polite`, `assertive` |
| `aria-atomic` | Tamamı mı duyurulsun | `true`, `false` |
| `aria-relevant` | Hangi değişiklikler | `additions`, `removals`, `text`, `all` |

### Widget States

| Özellik | Açıklama | Kullanım |
|---------|----------|----------|
| `aria-checked` | İşaretli durumu | `true`, `false`, `mixed` |
| `aria-expanded` | Genişletilmiş mi | `true`, `false` |
| `aria-selected` | Seçili mi | `true`, `false` |
| `aria-pressed` | Basılı mı | `true`, `false`, `mixed` |
| `aria-disabled` | Devre dışı mı | `true`, `false` |
| `aria-hidden` | Gizli mi | `true`, `false` |

### Relationship Attributes

| Özellik | Açıklama |
|---------|----------|
| `aria-controls` | Kontrol edilen element ID'si |
| `aria-owns` | Sahip olunan element ID'si |
| `aria-activedescendant` | Aktif alt element ID'si |
| `aria-haspopup` | Popup var mı |

## Yaygın Widget Paternleri

### Accordion

```html
<div class="accordion">
  <h3>
    <button aria-expanded="false" 
            aria-controls="section1"
            id="accordion1">
      Bölüm 1
    </button>
  </h3>
  <div id="section1" 
       aria-labelledby="accordion1"
       aria-hidden="true">
    <p>İçerik...</p>
  </div>
</div>

<script>
function toggleAccordion(button) {
  const expanded = button.getAttribute('aria-expanded') === 'true';
  const panel = document.getElementById(button.getAttribute('aria-controls'));
  
  button.setAttribute('aria-expanded', !expanded);
  panel.setAttribute('aria-hidden', expanded);
}
</script>
```

### Tab Panel

```html
<div class="tabs">
  <div role="tablist" aria-label="Ayarlar">
    <button role="tab" 
            id="tab1" 
            aria-selected="true" 
            aria-controls="panel1">
      Genel
    </button>
    <button role="tab" 
            id="tab2" 
            aria-selected="false" 
            aria-controls="panel2"
            tabindex="-1">
      Güvenlik
    </button>
  </div>
  
  <div role="tabpanel" 
       id="panel1" 
       aria-labelledby="tab1">
    Genel ayarlar...
  </div>
  <div role="tabpanel" 
       id="panel2" 
       aria-labelledby="tab2"
       hidden>
    Güvenlik ayarları...
  </div>
</div>

<script>
// Klavye navigasyonu: Arrow keys, Home, End
// Tab: Tab panel'e geçiş
</script>
```

### Modal Dialog

```html
<div role="dialog" 
     aria-modal="true"
     aria-labelledby="dialog-title"
     aria-describedby="dialog-desc"
     class="modal">
  <h2 id="dialog-title">Onay</h2>
  <p id="dialog-desc">Bu işlemi onaylıyor musunuz?</p>
  <div class="modal-actions">
    <button onclick="closeModal()">İptal</button>
    <button onclick="confirm()">Onayla</button>
  </div>
</div>

<!-- Arka plan -->
<div aria-hidden="true" class="modal-backdrop"></div>
```

### Menu

```html
<nav aria-label="Ana menü">
  <button aria-haspopup="true" 
          aria-expanded="false"
          aria-controls="menu1">
    Dosya
  </button>
  <ul role="menu" id="menu1" aria-hidden="true">
    <li role="none">
      <button role="menuitem">Yeni</button>
    </li>
    <li role="none">
      <button role="menuitem">Aç</button>
    </li>
    <li role="separator"></li>
    <li role="none">
      <button role="menuitem" aria-disabled="true">Kaydet</button>
    </li>
  </ul>
</nav>
```

### Combobox / Autocomplete

```html
<div class="combobox">
  <label id="search-label">Ülke ara</label>
  <input type="text"
         role="combobox"
         aria-autocomplete="list"
         aria-expanded="false"
         aria-controls="search-list"
         aria-labelledby="search-label"
         aria-activedescendant="">
  <ul role="listbox" id="search-list" aria-hidden="true">
    <li role="option" id="option1">Türkiye</li>
    <li role="option" id="option2">Almanya</li>
  </ul>
</div>
```

### Tree View

```html
<div role="tree" aria-label="Dosya sistemi">
  <div role="treeitem" aria-expanded="false" aria-level="1">
    📁 Belgeler
    <div role="group">
      <div role="treeitem" aria-level="2">📄 Notlar.txt</div>
      <div role="treeitem" aria-level="2">📄 Rapor.pdf</div>
    </div>
  </div>
</div>
```

## Live Regions

### Duyuru Türleri

```html
<!-- Polite: Sırasını bekler -->
<div aria-live="polite">Mesaj gönderildi</div>

<!-- Assertive: Hemen keser -->
<div aria-live="assertive">Hata oluştu!</div>

<!-- Off: Duyurulmaz -->
<div aria-live="off">Geçici bilgi</div>
```

### Atomic

```html
<!-- Tüm içerik duyurulur -->
<div aria-live="polite" aria-atomic="true">
  Sepette <span id="count">3</span> ürün var
</div>
<!-- "Sepette 3 ürün var" olarak duyurulur -->

<!-- Sadece değişen kısım -->
<div aria-live="polite" aria-atomic="false">
  Sepette <span id="count">3</span> ürün var
</div>
<!-- "3" olarak duyurulur -->
```

### Relevant

```html
<div aria-live="polite" 
     aria-relevant="additions removals text">
  <!-- additions: Yeni elementler -->
  <!-- removals: Silinen elementler -->
  <!-- text: Metin değişiklikleri -->
  <!-- all: Hepsi -->
</div>
```

## Yaygın Hatalar

### ❌ Yanlış Kullanımlar

```html
<!-- Gereksiz ARIA -->
<div role="button">Buton</div>  <!-- ❌ -->
<button>Buton</button>           <!-- ✅ -->

<!-- Çelişen roller -->
<button role="link">Buton gibi görünüp link gibi davranır</button>  <!-- ❌ -->

<!-- Gizli ama odaklanılabilir -->
<button aria-hidden="true">Gizli ama tıklanabilir</button>  <!-- ❌ -->
<button aria-hidden="true" tabindex="-1">Doğru gizleme</button>  <!-- ✅ -->

<!-- Duplicate ID -->
<div id="content">...</div>
<div id="content">...</div>  <!-- ❌ -->

<!-- Yanlış live region -->
<div aria-live="assertive">
  <span>Gereksiz assertive duyuru</span>
</div>  <!-- ❌ Sadece önemli uyarılar assertive olmalı -->
```

### ✅ Doğru Kullanımlar

```html
<!-- Semantic HTML + gerekli ARIA -->
<button aria-pressed="false">Toggle</button>

<!-- Focus yönetimi -->
<div role="dialog" aria-modal="true">
  <!-- Focus trap uygulanmış -->
</div>

<!-- Doğru landmark -->
<nav aria-label="Ana menü">
  <ul>...</ul>
</nav>

<!-- Erişilebilir form -->
<label for="email">E-posta</label>
<input type="email" id="email" aria-describedby="email-hint">
<span id="email-hint">Örnek: ornek@site.com</span>
```

## ARIA Denetim Listesi

```
□ Native HTML yeterli mi? ARIA gerekli mi?
□ Interactive elementler klavye erişilebilir mi?
□ aria-hidden="true" elementler odaklanılabilir mi? (olmamalı)
□ Duplicate ID var mı?
□ Role, state, property tutarlı mı?
□ Live regions doğru kullanılmış mı?
□ Focus management doğru mu? (modal, tab panel)
□ Label/labelledby doğru referans veriyor mu?
□ Ekran okuyucu ile test edildi mi?
```