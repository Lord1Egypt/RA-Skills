#!/bin/bash
# full-audit.sh - Kapsamlı WCAG 2.2 denetimi
# Tüm kriterleri kontrol eden detaylı analiz

set -e

URL="$1"
LEVEL="${2:-AA}"
OUTPUT_DIR="${3:-./a11y-reports}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

if [ -z "$URL" ]; then
    echo "Kullanım: $0 URL [LEVEL] [OUTPUT_DIR]"
    echo "  LEVEL: A, AA, AAA (varsayılan: AA)"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

echo "════════════════════════════════════════════════════"
echo "  Kapsamlı WCAG 2.2 Denetimi"
echo "════════════════════════════════════════════════════"
echo "URL: $URL"
echo "Seviye: $LEVEL"
echo "Tarih: $(date)"
echo ""

# WCAG tag'leri belirle
case $LEVEL in
    A)
        TAGS="wcag2a"
        ;;
    AA)
        TAGS="wcag2a,wcag2aa,wcag22aa"
        ;;
    AAA)
        TAGS="wcag2a,wcag2aa,wcag2aaa,wcag22aa,wcag22aaa"
        ;;
    *)
        echo "Geçersiz seviye: $LEVEL"
        exit 1
        ;;
esac

# Axe-core kapsamlı tarama
run_axe_full() {
    echo "[1/8] Axe-core kapsamlı tarama..."
    
    npx @axe-core/cli "$URL" \
        --tags "$TAGS" \
        --reporter json \
        --output "$OUTPUT_DIR/axe-full-$TIMESTAMP.json" 2>/dev/null || {
        echo "⚠️ Axe-core CLI çalıştırılamadı"
    }
}

# Pa11y tarama
run_pa11y() {
    echo "[2/8] Pa11y tarama..."
    
    npx pa11y "$URL" \
        --standard "WCAG2$LEVEL" \
        --reporter json \
        --output "$OUTPUT_DIR/pa11y-$TIMESTAMP.json" 2>/dev/null || {
        echo "⚠️ Pa11y çalıştırılamadı"
    }
}

# Lighthouse tarama
run_lighthouse() {
    echo "[3/8] Lighthouse denetimi..."
    
    npx lighthouse "$URL" \
        --only-categories=accessibility \
        --output=json \
        --output-path="$OUTPUT_DIR/lighthouse-$TIMESTAMP.json" \
        --chrome-flags="--headless --no-sandbox" \
        --quiet 2>/dev/null || {
        echo "⚠️ Lighthouse çalıştırılamadı"
    }
}

# HTML Validation
run_html_validation() {
    echo "[4/8] HTML validasyonu..."
    
    # v.Nu ile local validation veya online API
    curl -s -H "Content-Type: text/html" \
        --data-binary @"$OUTPUT_DIR/page-$TIMESTAMP.html" \
        "https://validator.nu/?out=json" \
        > "$OUTPUT_DIR/html-validation-$TIMESTAMP.json" 2>/dev/null || {
        echo "⚠️ HTML validasyonu yapılamadı"
    }
}

# Contrast analizi
run_contrast_analysis() {
    echo "[5/8] Renk kontrastı analizi..."
    
    # Bu genellikle axe sonuçlarında yer alır
    echo "Kontrast analizi Axe sonuçlarında yer alacak"
}

# Keyboard test simulation
run_keyboard_test() {
    echo "[6/8] Klavye navigasyonu testi..."
    
    cat > "$OUTPUT_DIR/keyboard-test-$TIMESTAMP.md" << 'EOF'
# Klavye Navigasyonu Test Listesi

## Manuel Test Adımları

### 1. Tab Navigation
- [ ] Tab tuşu ile tüm interaktif elementlere erişilebiliyor mu?
- [ ] Shift+Tab ile geri navigasyon çalışıyor mu?
- [ ] Focus sırası mantıklı mı? (DOM sırası ile görsel sıra uyumlu mu?)

### 2. Focus Visibility
- [ ] Focus göstergesi tüm elementlerde görünür mü?
- [ ] Focus rengi yeterli kontrasta sahip mi? (3:1 minimum)

### 3. Focus Trap
- [ ] Modal/dialog açıldığında focus modal içinde mi kalıyor?
- [ ] ESC tuşu ile modal kapatılabiliyor mu?
- [ ] Modal kapandığında focus doğru elemente mi dönüyor?

### 4. Interactive Elements
- [ ] Tüm butonlar Enter/Space ile aktifleştirilebiliyor mu?
- [ ] Linkler Enter ile takip edilebiliyor mu?
- [ ] Form elementleri klavye ile doldurulabiliyor mu?

### 5. Complex Widgets
- [ ] Tab panellerinde Arrow keys çalışıyor mu?
- [ ] Menülerde Arrow keys çalışıyor mu?
- [ ] Accordion'lar Space/Enter ile açılıp kapanabiliyor mu?

### 6. Skip Links
- [ ] İlk Tab'da skip link görünüyor mu?
- [ ] Skip link çalışıyor mu?
- [ ] Ana içeriğe atlıyor mu?

## Test Sonuçları
- Test Eden: _______________
- Tarih: _______________
- Tarayıcı: _______________
- Notlar: _______________
EOF
    echo "Keyboard test şablonu oluşturuldu"
}

# Screen reader simulation
run_sr_simulation() {
    echo "[7/8] Ekran okuyucu simülasyonu..."
    
    cat > "$OUTPUT_DIR/sr-simulation-$TIMESTAMP.md" << 'EOF'
# Ekran Okuyucu Simülasyonu Test Listesi

## NVDA / JAWS Test (Windows)

### Sayfa Yükleme
- [ ] Sayfa başlığı okunuyor mu?
- [ ] Ana landmark tespit ediliyor mu?
- [ ] Sayfa özeti doğru mu?

### Navigasyon
- [ ] H tuşu ile başlıklara erişilebiliyor mu?
- [ ] Başlık seviyeleri doğru okunuyor mu?
- [ ] Tab tuşu ile landmark'lar arası geçiş çalışıyor mu?

### İçerik
- [ ] Görsellerin alt metinleri okunuyor mu?
- [ ] Dekoratif görseller atlanıyor mu?
- [ ] Tablo başlıkları ve hücreler doğru okunuyor mu?

### Formlar
- [ ] Label'lar doğru okunuyor mu?
- [ ] Hata mesajları duyuruluyor mu?
- [ ] Required alanlar belirtiliyor mu?

## VoiceOver Test (macOS/iOS)

### Rotör
- [ ] Rotör ile başlıklara erişilebiliyor mu?
- [ ] Rotör ile linklere erişilebiliyor mu?
- [ ] Rotör ile landmark'lara erişilebiliyor mu?

### Navigasyon
- [ ] VO+Right ile elementler doğru okunuyor mu?
- [ ] VO+Space ile elementler aktifleştirilebiliyor mu?

## Test Sonuçları
- Test Eden: _______________
- Tarih: _______________
- Ekran Okuyucu: _______________
- Versiyon: _______________
- Notlar: _______________
EOF
    echo "Screen reader test şablonu oluşturuldu"
}

# Rapor oluştur
generate_full_report() {
    echo "[8/8] Kapsamlı rapor oluşturuluyor..."
    
    local report="$OUTPUT_DIR/full-audit-report-$TIMESTAMP.md"
    
    cat > "$report" << EOF
# Kapsamlı WCAG 2.2 Erişilebilirlik Denetim Raporu

## Denetim Bilgileri

| Özellik | Değer |
|---------|-------|
| URL | $URL |
| Denetim Tarihi | $(date +"%d/%m/%Y %H:%M") |
| WCAG Seviyesi | $LEVEL |
| Denetim Aracı | a11y-auditor v1.0 |
| Denetim Türü | Kapsamlı |

## Özet Sonuçlar

EOF

    # Axe sonuçlarını ekle
    if [ -f "$OUTPUT_DIR/axe-full-$TIMESTAMP.json" ]; then
        echo "### Axe-core Bulguları" >> "$report"
        echo "" >> "$report"
        node -e "
            const fs = require('fs');
            try {
                const data = JSON.parse(fs.readFileSync('$OUTPUT_DIR/axe-full-$TIMESTAMP.json', 'utf8'));
                const violations = data.violations || [];
                const incomplete = data.incomplete || [];
                const passes = data.passes || [];
                
                console.log('| Kategori | Sayı |');
                console.log('|----------|------|');
                console.log('| İhlaller | ' + violations.length + ' |');
                console.log('| İncelenecek | ' + incomplete.length + ' |');
                console.log('| Geçen | ' + passes.length + ' |');
                console.log('');
                
                if (violations.length > 0) {
                    console.log('### İhlal Detayları');
                    console.log('');
                    violations.forEach(v => {
                        console.log('#### ' + v.id);
                        console.log('');
                        console.log('- **Etki:** ' + v.impact);
                        console.log('- **Açıklama:** ' + v.description);
                        console.log('- **Yardım:** ' + v.helpUrl);
                        console.log('- **Etkilenen Element:** ' + v.nodes.length);
                        console.log('');
                    });
                }
            } catch (e) {
                console.log('Sonuçlar işlenemedi');
            }
        " >> "$report" 2>/dev/null || echo "Sonuçlar işlenemedi" >> "$report"
    fi
    
    # Lighthouse skorunu ekle
    if [ -f "$OUTPUT_DIR/lighthouse-$TIMESTAMP.json" ]; then
        echo "" >> "$report"
        echo "### Lighthouse Erişilebilirlik Skoru" >> "$report"
        echo "" >> "$report"
        node -e "
            const fs = require('fs');
            try {
                const data = JSON.parse(fs.readFileSync('$OUTPUT_DIR/lighthouse-$TIMESTAMP.json', 'utf8'));
                const score = Math.round((data.categories?.accessibility?.score || 0) * 100);
                console.log('**Skor:** ' + score + '/100');
            } catch (e) {
                console.log('Skor alınamadı');
            }
        " >> "$report" 2>/dev/null || echo "Skor alınamadı" >> "$report"
    fi
    
    # Öneriler
    cat >> "$report" << EOF

## Öneriler ve Düzeltme Öncelikleri

### Kritik (Hemen Düzeltilmeli)
- Eksik alt metinler
- Yetersiz renk kontrastı
- Klavye erişilebilirliği sorunları
- Form etiketleme eksiklikleri

### Önemli (Kısa Vadeli)
- Başlık hiyerarşisi düzeltmeleri
- ARIA kullanımı iyileştirmeleri
- Focus visibility iyileştirmeleri
- Skip link eklenmesi

### İyileştirici (Uzun Vadeli)
- Dokümantasyon güncellemeleri
- Erişilebilirlik eğitimleri
- Sürekli izleme süreçleri

## Test Dosyaları

- Axe-core: \`axe-full-$TIMESTAMP.json\`
- Pa11y: \`pa11y-$TIMESTAMP.json\`
- Lighthouse: \`lighthouse-$TIMESTAMP.json\`
- Klavye Testi: \`keyboard-test-$TIMESTAMP.md\`
- Ekran Okuyucu Testi: \`sr-simulation-$TIMESTAMP.md\`

## Kaynaklar

- [WCAG 2.2 Kriterleri](https://www.w3.org/TR/WCAG22/)
- [WAI-ARIA Yazarlık Uygulamaları](https://www.w3.org/WAI/ARIA/apg/)
- [WebAIM WCAG 2 Checklist](https://webaim.org/standards/wcag/checklist)

---
*Rapor a11y-auditor tarafından oluşturuldu - $(date)*
EOF

    echo "✅ Rapor oluşturuldu: $report"
}

# Ana akış
main() {
    run_axe_full
    run_pa11y
    run_lighthouse
    run_html_validation
    run_contrast_analysis
    run_keyboard_test
    run_sr_simulation
    generate_full_report
    
    echo ""
    echo "════════════════════════════════════════════════════"
    echo "  Kapsamlı denetim tamamlandı!"
    echo "════════════════════════════════════════════════════"
    echo "Rapor: $OUTPUT_DIR/full-audit-report-$TIMESTAMP.md"
}

main