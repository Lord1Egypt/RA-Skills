#!/bin/bash
# daily-sales-digest 테스트 스크립트

set -e

echo "🧪 daily-sales-digest 테스트 시작"
echo ""

SKILL_DIR="/Users/mupeng/.openclaw/workspace/skills/daily-sales-digest"
cd "$SKILL_DIR"

# 1. 설정 파일 확인
echo "1️⃣  설정 파일 확인..."
if [ ! -f ~/.openclaw/workspace/config/daily-sales-digest.json ]; then
  echo "❌ 설정 파일이 없습니다."
  echo "   cp config.template.json ~/.openclaw/workspace/config/daily-sales-digest.json"
  exit 1
fi
echo "✅ 설정 파일 존재"
echo ""

# 2. 데이터 디렉토리 확인
echo "2️⃣  데이터 디렉토리 확인..."
if [ ! -d ~/.openclaw/workspace/data/sales ]; then
  echo "⚠️  데이터 디렉토리 생성 중..."
  mkdir -p ~/.openclaw/workspace/data/sales
fi
echo "✅ 데이터 디렉토리 준비 완료"
echo ""

# 3. 데이터 수집 테스트
echo "3️⃣  데이터 수집 테스트..."
node scripts/collect.js --date yesterday --force
echo ""

# 4. 일일 요약 테스트
echo "4️⃣  일일 요약 테스트..."
node scripts/digest.js --date yesterday --format text
echo ""

# 5. 주간 리포트 테스트 (데이터가 충분할 경우)
echo "5️⃣  주간 리포트 테스트..."
if [ $(ls ~/.openclaw/workspace/data/sales/*.json 2>/dev/null | wc -l) -ge 7 ]; then
  node scripts/digest.js --period week --format text
else
  echo "⚠️  주간 리포트를 위한 데이터가 부족합니다 (7일 이상 필요)"
fi
echo ""

# 6. 이상 탐지 테스트
echo "6️⃣  이상 탐지 테스트..."
node scripts/alert.js --date yesterday --threshold 0.3
echo ""

# 7. JSON 출력 테스트
echo "7️⃣  JSON 출력 테스트..."
node scripts/digest.js --date yesterday --format json | head -20
echo ""

echo "✅ 모든 테스트 완료!"
echo ""
echo "📋 다음 단계:"
echo "  1. config 파일에 실제 API 키 입력"
echo "  2. scripts/collect.js의 TODO 섹션 구현"
echo "  3. cron 스케줄 설정:"
echo "     openclaw cron add --name daily-sales-digest:daily \\"
echo "       --schedule '0 8 * * *' \\"
echo "       --command 'node $SKILL_DIR/scripts/digest.js --date yesterday --deliver discord'"
