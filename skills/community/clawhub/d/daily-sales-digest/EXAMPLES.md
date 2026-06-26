# 사용 예시

## 일일 업무 플로우

### 1. 아침 루틴 (자동화)

매일 아침 8시, OpenClaw cron이 자동으로 전일 매출을 Discord로 전송합니다.

```bash
# cron 설정 (한 번만 실행)
openclaw cron add \
  --name "daily-sales-digest:daily" \
  --schedule "0 8 * * *" \
  --command "node /Users/mupeng/.openclaw/workspace/skills/daily-sales-digest/scripts/digest.js --date yesterday --deliver discord"
```

Discord에 다음과 같은 메시지가 도착합니다:

```
📊 2026-02-17 매출 요약

💰 총 매출: ₩2,148,161 (↑ 8.9% vs 전일)
🛒 주문 수: 59건 (↑ 0.0% vs 전일)
💳 객단가: ₩36,409 (↑ 8.9% vs 전일)

📈 비교 분석:
  • 전일 대비: ↑ 8.9%
  • 전주 동요일: ↑ 32.4%

🏪 채널별:
  • naver: ₩2,148,161 (59건)
```

### 2. 주간 리포트 (매주 월요일)

```bash
openclaw cron add \
  --name "daily-sales-digest:weekly" \
  --schedule "0 9 * * 1" \
  --command "node /Users/mupeng/.openclaw/workspace/skills/daily-sales-digest/scripts/digest.js --period week --deliver discord,email"
```

### 3. 월간 리포트 (매월 1일)

```bash
openclaw cron add \
  --name "daily-sales-digest:monthly" \
  --schedule "0 9 1 * *" \
  --command "node /Users/mupeng/.openclaw/workspace/skills/daily-sales-digest/scripts/digest.js --period month --deliver email"
```

## 수동 조회

### 특정 날짜 매출 확인

```bash
cd /Users/mupeng/.openclaw/workspace/skills/daily-sales-digest

# 어제
node scripts/digest.js --date yesterday

# 오늘
node scripts/digest.js --date today

# 특정 날짜
node scripts/digest.js --date 2026-02-15
```

### JSON 형식으로 출력 (API 연동용)

```bash
node scripts/digest.js --date yesterday --format json > report.json
```

### 주간 매출 분석

```bash
node scripts/digest.js --period week
```

## 이상 탐지

### 매출 급증/급감 감지

```bash
# 임계값 30% (기본값)
node scripts/alert.js --date yesterday

# 임계값 20%
node scripts/alert.js --date yesterday --threshold 0.2

# 즉시 Discord 알림
node scripts/alert.js --date yesterday --deliver discord
```

이상이 감지되면 다음과 같은 알림이 전송됩니다:

```
🚨 매출 이상 감지!

2026-02-17 매출이 전일 대비 45.3% 급증했습니다.

💰 오늘: ₩3,050,000
💰 어제: ₩2,100,000
📈 증가: +₩950,000 (+45.3%)

원인 분석이 필요합니다.
```

### 자동 이상 탐지 (cron)

```bash
# 매일 오후 9시 이상 탐지 실행
openclaw cron add \
  --name "daily-sales-digest:anomaly" \
  --schedule "0 21 * * *" \
  --command "node /Users/mupeng/.openclaw/workspace/skills/daily-sales-digest/scripts/alert.js --date today --deliver discord"
```

## 데이터 수집

### 자동 수집 (권장)

매일 자정에 당일 데이터를 자동 수집:

```bash
openclaw cron add \
  --name "daily-sales-digest:collect" \
  --schedule "0 0 * * *" \
  --command "node /Users/mupeng/.openclaw/workspace/skills/daily-sales-digest/scripts/collect.js --date today"
```

### 수동 수집

```bash
cd /Users/mupeng/.openclaw/workspace/skills/daily-sales-digest

# 어제 데이터 수집
node scripts/collect.js --date yesterday

# 특정 날짜
node scripts/collect.js --date 2026-02-15

# 이미 데이터가 있어도 덮어쓰기
node scripts/collect.js --date 2026-02-15 --force

# 특정 소스만 수집
node scripts/collect.js --date yesterday --source naver
node scripts/collect.js --date yesterday --source coupang
```

## 채널별 전송

### Discord만

```bash
node scripts/digest.js --date yesterday --deliver discord
```

### 이메일만

```bash
node scripts/digest.js --date yesterday --deliver email
```

### Discord + 이메일

```bash
node scripts/digest.js --date yesterday --deliver discord,email
```

## cron 관리

### 등록된 작업 확인

```bash
openclaw cron list | grep daily-sales
```

### 실행 이력 확인

```bash
openclaw cron runs daily-sales-digest:daily
```

### 작업 삭제

```bash
openclaw cron delete daily-sales-digest:daily
```

### 작업 일시 중지

```bash
# 작업 ID 확인
openclaw cron list

# 중지
openclaw cron pause <job-id>

# 재개
openclaw cron resume <job-id>
```

## 고급 사용법

### 비교 분석 커스터마이징

digest.js 스크립트를 수정하여 비교 기준을 변경할 수 있습니다:

- 전일 대비 (기본)
- 전주 동요일 대비
- 전월 동일 대비
- 지난 30일 평균 대비

### 채널별 분석

특정 채널만 분석하려면 collect.js에서 `--source` 옵션 사용:

```bash
node scripts/collect.js --date yesterday --source naver
node scripts/digest.js --date yesterday
```

### 데이터 아카이빙

90일 이상 오래된 데이터를 압축하여 보관:

```bash
cd ~/.openclaw/workspace/data/sales
tar -czf archive-2025.tar.gz 2025-*.json
rm 2025-*.json
```

## 트러블슈팅

### 데이터가 수집되지 않음

1. 설정 파일 확인:
   ```bash
   cat ~/.openclaw/workspace/config/daily-sales-digest.json
   ```

2. 데이터 소스가 활성화되어 있는지 확인:
   ```json
   "naver": {
     "enabled": true,  // false면 수집 안 됨
     ...
   }
   ```

3. API 키가 올바른지 확인 (실제 API 연동 후)

### Discord 전송 실패

1. 채널 ID 확인:
   ```json
   "discord": {
     "enabled": true,
     "channelId": "1468204132920725535"
   }
   ```

2. OpenClaw Discord 스킬이 설치되어 있는지 확인:
   ```bash
   openclaw message send --help
   ```

### cron 작업이 실행되지 않음

```bash
# OpenClaw gateway 상태 확인
openclaw gateway status

# cron 로그 확인
openclaw cron runs daily-sales-digest:daily
```

## 모범 사례

1. **매일 자동 수집**: 데이터는 가능한 빨리 수집 (자정 또는 익일 새벽)
2. **주기적인 백업**: 데이터 디렉토리를 주기적으로 백업
3. **임계값 조정**: 비즈니스 특성에 맞게 이상 탐지 임계값 조정
4. **로그 모니터링**: cron 실행 이력을 주기적으로 확인
5. **API 키 보안**: 설정 파일을 절대 git에 커밋하지 말 것
