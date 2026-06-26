#!/usr/bin/env bash
# =============================================================================
# efatura_check.sh — GİB E-Fatura Mükellef Sorgulama
# Kaynak: GİB e-Belge Doğrulama Servisleri
# Geliştiren: Finhouse (finhouse.ai)
# =============================================================================

set -euo pipefail

# Renkler
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════╗"
echo "║         E-Fatura Mükellef Sorgulama — GİB            ║"
echo "║              Powered by Finhouse.ai                  ║"
echo "╚══════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Yardım
usage() {
  echo "Kullanım:"
  echo "  $0 --vkn <VKN>          Vergi Kimlik Numarasıyla sorgula"
  echo "  $0 --tc  <TC>           TC Kimlik Numarasıyla sorgula"
  echo "  $0 --name <'Firma Adı'> Firma adıyla sorgula (URL encode gerekir)"
  echo ""
  echo "Örnekler:"
  echo "  $0 --vkn 1234567890"
  echo "  $0 --tc 12345678901"
  echo "  $0 --name 'ACME Teknoloji'"
  exit 1
}

# Parametre parse
MODE=""
QUERY=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --vkn)
      MODE="vkn"
      QUERY="$2"
      shift 2
      ;;
    --tc)
      MODE="tc"
      QUERY="$2"
      shift 2
      ;;
    --name)
      MODE="name"
      QUERY="$2"
      shift 2
      ;;
    -h|--help)
      usage
      ;;
    *)
      echo -e "${RED}Bilinmeyen parametre: $1${NC}"
      usage
      ;;
  esac
done

if [[ -z "$MODE" || -z "$QUERY" ]]; then
  usage
fi

# Validasyon
validate_vkn() {
  if [[ ! "$1" =~ ^[0-9]{10}$ ]]; then
    echo -e "${RED}Hata: VKN 10 haneli olmalıdır.${NC}"
    exit 1
  fi
}

validate_tc() {
  if [[ ! "$1" =~ ^[0-9]{11}$ ]]; then
    echo -e "${RED}Hata: TC Kimlik No 11 haneli olmalıdır.${NC}"
    exit 1
  fi
}

# GİB E-Fatura Mükellef Listesi Sorgulama
# GİB, e-fatura mükelleflerini kamuya açık bir endpoint üzerinden sunar.
# Resmi endpoint: https://efatura.gib.gov.tr/earsivportal/GibIntranetGatewayCont...
# Not: GİB'in bazı endpointleri session/CAPTCHA gerektirir.
# Bu script açık sorgulama endpointini kullanır.

GIB_BASE_URL="https://efatura.gib.gov.tr"
MUKELLEF_KONTROL_URL="${GIB_BASE_URL}/earsivportal/GibIntranetGatewayCont?dispatch=mukellefKontrolEt"

echo -e "${YELLOW}Sorgulanıyor...${NC}"
echo ""

case "$MODE" in
  vkn)
    validate_vkn "$QUERY"
    echo -e "VKN: ${BLUE}${QUERY}${NC}"
    echo ""

    # GİB'in kamuya açık mükellef sorgulama sayfası
    RESPONSE=$(curl -s \
      -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
      --max-time 15 \
      "${GIB_BASE_URL}/efatura" 2>/dev/null) || true

    # Not: GİB'in gerçek API sorgusu için oturum ve token gerektirir.
    # Aşağıda mükellef listesi CSV'si üzerinden kontrol yapılır.
    check_via_public_list "$QUERY" "vkn"
    ;;

  tc)
    validate_tc "$QUERY"
    echo -e "TC Kimlik No: ${BLUE}${QUERY}${NC}"
    echo ""
    check_via_public_list "$QUERY" "tc"
    ;;

  name)
    echo -e "Firma Adı: ${BLUE}${QUERY}${NC}"
    echo ""
    check_via_public_list "$QUERY" "name"
    ;;
esac

# GİB Kamuya Açık Mükellef Listesi Kontrolü
check_via_public_list() {
  local QUERY="$1"
  local MODE="$2"

  # GİB, e-fatura mükellef listesini periyodik olarak günceller
  # Güncel liste: https://efatura.gib.gov.tr/mukellef-listesi
  MUKELLEF_LIST_URL="https://efatura.gib.gov.tr/listeleri/efatura_mf.zip"

  echo -e "${YELLOW}GİB mükellef listesi kontrol ediliyor...${NC}"

  # Geçici dizin
  TMP_DIR=$(mktemp -d)
  trap "rm -rf $TMP_DIR" EXIT

  # Listeyi indir (cache varsa kullan)
  CACHE_FILE="$HOME/.cache/efatura_tr/efatura_mf.csv"
  CACHE_DIR="$HOME/.cache/efatura_tr"
  mkdir -p "$CACHE_DIR"

  CACHE_AGE=0
  if [[ -f "$CACHE_FILE" ]]; then
    CACHE_AGE=$(( $(date +%s) - $(stat -f %m "$CACHE_FILE" 2>/dev/null || stat -c %Y "$CACHE_FILE" 2>/dev/null || echo 0) ))
  fi

  # 24 saatten eskiyse veya yoksa yeniden indir
  if [[ ! -f "$CACHE_FILE" || $CACHE_AGE -gt 86400 ]]; then
    echo -e "${YELLOW}Güncel mükellef listesi indiriliyor (GİB)...${NC}"
    if curl -s -L --max-time 60 -o "$TMP_DIR/list.zip" "$MUKELLEF_LIST_URL" 2>/dev/null; then
      if unzip -q "$TMP_DIR/list.zip" -d "$TMP_DIR/" 2>/dev/null; then
        find "$TMP_DIR" -name "*.csv" -o -name "*.CSV" | head -1 | xargs -I{} cp {} "$CACHE_FILE" 2>/dev/null || true
        echo -e "${GREEN}Liste güncellendi.${NC}"
      else
        echo -e "${YELLOW}ZIP açılamadı, farklı format denenecek.${NC}"
      fi
    else
      echo -e "${RED}GİB listesi indirilemedi. İnternet bağlantısını kontrol edin.${NC}"
    fi
  else
    CACHE_MINS=$(( CACHE_AGE / 60 ))
    echo -e "${GREEN}Cache kullanılıyor (${CACHE_MINS} dakika önce güncellendi).${NC}"
  fi

  echo ""

  if [[ -f "$CACHE_FILE" ]]; then
    case "$MODE" in
      vkn)
        RESULT=$(grep -i "^$QUERY" "$CACHE_FILE" 2>/dev/null || grep -i "$QUERY" "$CACHE_FILE" 2>/dev/null | head -5)
        ;;
      tc)
        RESULT=$(grep -i "$QUERY" "$CACHE_FILE" 2>/dev/null | head -5)
        ;;
      name)
        RESULT=$(grep -i "$QUERY" "$CACHE_FILE" 2>/dev/null | head -10)
        ;;
    esac

    if [[ -n "$RESULT" ]]; then
      echo -e "${GREEN}✅ E-FATURA MÜKELLEFİ BULUNDU${NC}"
      echo ""
      echo -e "${BLUE}Sonuçlar:${NC}"
      echo "$RESULT" | head -10
    else
      echo -e "${YELLOW}⚠️  Mükellef listesinde bulunamadı${NC}"
      echo ""
      echo "Bu durum şu anlama gelebilir:"
      echo "  1. Şirket e-fatura mükellefi değildir (henüz zorunlu had altında olabilir)"
      echo "  2. Şirket GİB Portal üzerinden değil, entegratör üzerinden mükellef olmuştur"
      echo "  3. Kayıt yeni yapılmıştır, liste henüz güncellenmemiştir"
    fi
  else
    echo -e "${YELLOW}Mükellef listesi mevcut değil. Manuel kontrol için:${NC}"
  fi

  echo ""
  echo "═══════════════════════════════════════════════════"
  echo -e "${BLUE}📋 Manuel Kontrol Linkleri:${NC}"
  echo ""
  echo "  🌐 GİB E-Fatura Portal:"
  echo "     https://efatura.gib.gov.tr"
  echo ""
  echo "  🔍 Mükellef Sorgulama (İVD):"
  echo "     https://ivd.gib.gov.tr"
  echo ""
  echo "  📄 E-Belge Mevzuatı:"
  echo "     https://ebelge.gib.gov.tr"
  echo ""
  echo "  📞 GİB ALO 189 Vergi İletişim Merkezi"
  echo "═══════════════════════════════════════════════════"
  echo ""
  echo -e "${BLUE}💡 Finhouse e-fatura entegrasyon danışmanlığı:${NC}"
  echo "   https://finhouse.ai | info@finhouse.ai"
  echo ""
}

# Fonksiyonu çağır (case bloğu içinde tanımlandığı için burada yeniden çağırıyoruz)
case "$MODE" in
  vkn)
    validate_vkn "$QUERY"
    check_via_public_list "$QUERY" "vkn"
    ;;
  tc)
    validate_tc "$QUERY"
    check_via_public_list "$QUERY" "tc"
    ;;
  name)
    check_via_public_list "$QUERY" "name"
    ;;
esac
