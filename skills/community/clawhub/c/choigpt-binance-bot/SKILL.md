# ChoiGPT Binance Trading Bot Skill

이 스킬은 **Sweepzone V1** 전략을 기반으로 바이낸스 선물 시장을 감시하고, 최적의 타점에서 자동 매매를 수행하는 에이전트 도구입니다.

## 🚀 주요 기능

1.  **Sweepzone V1 전략 분석**: 일봉 일목균형표 구름대 돌파 및 20MA 추세 확증 로직을 사용하여 고승률 진입 타점을 포착합니다.
2.  **실시간 시장 감시**: `market_scanner_service.py`를 통해 여러 심볼의 기회를 동시에 탐색합니다.
3.  **위험 관리**: 자산 대비 동적 포지션 사이징(기본 15%), Trailing Stop(1.2%), Kimchi Premium Shield(4%) 기능을 내장하고 있습니다.
4.  **텔레그램 통합**: 매매 신호 및 일일 수익 리포트를 텔레그램으로 실시간 전송합니다.

## 🛠 사용 방법

에이전트는 다음 명령어를 사용하여 봇을 제어하고 분석할 수 있습니다.

### 1. 봇 가동 (Live Mode)
실제 자산으로 자동매매를 시작합니다.
```bash
python src/main.py --mode live
```

### 2. 백테스트 (Backtest Mode)
특정 심볼의 과거 데이터를 기반으로 수익률을 검증합니다.
```bash
python src/main.py --mode backtest --symbol BTCUSDT
```

### 3. 시장 스캐너 실행
현재 매수 기회가 있는 모든 코인을 탐색합니다.
```bash
python scripts/market_scanner_service.py
```

### 4. 실시간 대시보드 확인
현재 포지션 및 누적 수익률을 확인합니다.
```bash
python scripts/dashboard.py
```

## ⚠️ 주의 사항

- **API 설정**: 실행 전 `manifest.json`에 정의된 Binance API Key 및 Telegram 설정이 완료되어야 합니다.
- **환경 변수**: 플랫폼 내 환경 변수 설정을 통해 보안을 유지하십시오.
- **데이터 보존**: `data/` 디렉토리의 상태 파일들이 유지되어야 정확한 수익률 추적이 가능합니다.

---
**Author**: ALEXCHOI21
**Version**: 1.0.0
