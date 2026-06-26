#!/bin/bash
# check-criteria.sh - Belirli WCAG kriterlerini kontrol et

set -e

URL="$1"
CRITERIA="${2:-}"
OUTPUT_DIR="${3:-./a11y-reports}"

if [ -z "$URL" ]; then
    echo "Kullanım: $0 URL [CRITERIA] [OUTPUT_DIR]"
    echo "  CRITERIA: Virgülle ayrılmış kriterler (örn: 1.1.1,1.4.3,2.1.1)"
    echo ""
    echo "Örnekler:"
    echo "  $0 https://example.com 1.1.1"
    echo "  $0 https://example.com 1.1.1,1.4.3,2.1.1,4.1.2"
    exit 1
fi

# WCAG kriter -> Axe rule eşlemesi
declare -A WCAG_TO_AXE=(
    ["1.1.1"]="image-alt image-redundant-alt"
    ["1.3.1"]="heading-order list landmark label landmark-unique region"
    ["1.3.2"]="meaningful-sequence"
    ["1.4.1"]="color-contrast-enhanced color-contrast"
    ["1.4.3"]="color-contrast"
    ["1.4.4"]="meta-viewport"
    ["1.4.10"]="css-orientation-lock"
    ["1.4.11"]="color-contrast color-contrast-enhanced"
    ["1.4.12"]="line-height letter-spacing word-spacing"
    ["2.1.1"]="keyboard"
    ["2.1.2"]="no-keyboard-trap"
    ["2.4.1"]="bypass"
    ["2.4.2"]="document-title"
    ["2.4.3"]="focus-order"
    ["2.4.4"]="link-name link-in-text-block"
    ["2.4.5"]="bypass"
    ["2.4.6"]="label link-name"
    ["2.4.7"]="focus-visible"
    ["2.4.11"]="focus-visible"
    ["2.5.5"]="target-size"
    ["2.5.8"]="target-size"
    ["3.1.1"]="html-lang"
    ["3.1.2"]="html-lang-valid"
    ["3.2.1"]="no-onchange"
    ["3.2.2"]="no-autoplay-audio"
    ["3.3.1"]="aria-required-children aria-required-parent"
    ["3.3.2"]="label"
    ["4.1.2"]="aria-allowed-attr aria-hidden-body aria-hidden-focus aria-input-field-name aria-required-attr aria-required-children aria-required-parent aria-roledescription aria-valid-attr aria-valid-attr-value button-name duplicate-id-aria landmark-unique role-img-alt"
    ["4.1.3"]="status-messages"
)

echo "════════════════════════════════════════════════════"
echo "  WCAG Kriter Kontrolü"
echo "════════════════════════════════════════════════════"
echo "URL: $URL"
echo "Kriterler: $CRITERIA"
echo ""

# Kriterleri parse et
IFS=',' read -ra CRITERIA_ARRAY <<< "$CRITERIA"

# Axe rule'ları topla
RULES=""
for criterion in "${CRITERIA_ARRAY[@]}"; do
    criterion=$(echo "$criterion" | tr -d ' ')
    if [ -n "${WCAG_TO_AXE[$criterion]}" ]; then
        if [ -n "$RULES" ]; then
            RULES="$RULES,${WCAG_TO_AXE[$criterion]}"
        else
            RULES="${WCAG_TO_AXE[$criterion]}"
        fi
    else
        echo "⚠️ Bilinmeyen kriter: $criterion"
    fi
done

if [ -z "$RULES" ]; then
    echo "❌ Geçerli kriter bulunamadı"
    exit 1
fi

echo "Kontrol edilecek Axe kuralları: $RULES"
echo ""

# Axe-core çalıştır
echo "Axe-core çalıştırılıyor..."
npx @axe-core/cli "$URL" \
    --rules "$RULES" \
    --reporter json \
    2>/dev/null | tee "$OUTPUT_DIR/criteria-check-$$.json" | \
    node -e "
        const fs = require('fs');
        let input = '';
        process.stdin.on('data', chunk => input += chunk);
        process.stdin.on('end', () => {
            try {
                const data = JSON.parse(input);
                const violations = data.violations || [];
                const passes = data.passes || [];
                
                console.log('');
                console.log('════════════════════════════════════════════════════');
                console.log('  Sonuçlar');
                console.log('════════════════════════════════════════════════════');
                console.log('');
                
                if (violations.length > 0) {
                    console.log('❌ İHLALLER BULUNDU');
                    console.log('');
                    violations.forEach(v => {
                        console.log('■ ' + v.id);
                        console.log('  Etki: ' + v.impact);
                        console.log('  Açıklama: ' + v.description);
                        console.log('  Etkilenen element: ' + v.nodes.length);
                        if (v.nodes.length > 0) {
                            console.log('  Örnek: ' + v.nodes[0].html?.slice(0, 100));
                        }
                        console.log('');
                    });
                }
                
                if (passes.length > 0) {
                    console.log('✅ GEÇEN KURALLAR');
                    console.log('');
                    passes.forEach(p => {
                        console.log('✓ ' + p.id);
                    });
                }
                
                console.log('');
                console.log('Toplam: ' + violations.length + ' ihlal, ' + passes.length + ' geçen');
            } catch (e) {
                console.log('Sonuçlar işlenemedi:', e.message);
            }
        });
    "