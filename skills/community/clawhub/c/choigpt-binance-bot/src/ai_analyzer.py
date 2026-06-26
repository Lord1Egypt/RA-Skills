"""
AI 분석 모듈 - Gemini 기반 Pure SMC/ICT 분석 (V6.0: Team Mensa 스타일 통합)
- 대화 이력 유지 (chat_id별 최대 10턴)
- 실계좌 데이터 컨텍스트 주입 (잔고/포지션/승률/손익)
- 인텐트 분류 강화 (ANALYSIS / STATUS / TRADE_REVIEW / CHAT)
- ChoiGPT 페르소나 강화
"""

import requests
import json
import logging
from collections import deque
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────
# 대화 이력 저장소 (chat_id → deque of messages)
# ──────────────────────────────────────────────
_chat_histories: dict[int, deque] = {}
MAX_HISTORY_TURNS = 8  # 최대 8턴 (사용자+AI 각 8개 = 16개 메시지) 유지


def _get_history(chat_id: int) -> deque:
    if chat_id not in _chat_histories:
        _chat_histories[chat_id] = deque(maxlen=MAX_HISTORY_TURNS * 2)
    return _chat_histories[chat_id]


def clear_history(chat_id: int):
    """대화 이력 초기화"""
    _chat_histories[chat_id] = deque(maxlen=MAX_HISTORY_TURNS * 2)


def _add_to_history(chat_id: int, role: str, text: str):
    """대화 이력에 추가 (role: 'user' | 'model')"""
    history = _get_history(chat_id)
    history.append({"role": role, "parts": [{"text": text}]})


# Gemini 설정 (고정 모델 사용으로 복잡성 제거)
GEMINI_MODEL = "gemini-1.5-flash-latest"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"

def _call_gemini(prompt: str, temperature: float = 0.4, max_tokens: int = 600) -> str:
    """Gemini API 단순 호출 (단발 프롬프트)"""
    try:
        from config.config import GOOGLE_API_KEY
        if not GOOGLE_API_KEY:
            # 환경변수에서 시도
            GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyCaXIU9NTdcU0QPe7jLsSM0rQF8b4JD6xA") # 기본키 (규칙 기반)
            
        if not GOOGLE_API_KEY:
            return ""

        url = GEMINI_API_URL.format(model=GEMINI_MODEL, key=GOOGLE_API_KEY)
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
            }
        }
        resp = requests.post(url, json=payload, timeout=12)
        if resp.status_code == 200:
            data = resp.json()
            candidates = data.get('candidates', [])
            if candidates:
                return candidates[0].get('content', {}).get('parts', [{}])[0].get('text', '')
        return ""
    except Exception as e:
        logger.debug(f"Gemini API 호출 실패: {e}")
        return ""


def _call_gemini_with_history(system_prompt: str, history: list,
                              user_message: str, temperature: float = 0.5) -> str:
    """Gemini API 대화형 호출 (system + 이전 대화 + 새 메시지)"""
    try:
        from config.config import GOOGLE_API_KEY
        if not GOOGLE_API_KEY:
            GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyCaXIU9NTdcU0QPe7jLsSM0rQF8b4JD6xA")

        if not GOOGLE_API_KEY:
            return ""

        url = GEMINI_API_URL.format(model=GEMINI_MODEL, key=GOOGLE_API_KEY)

        # system prompt는 첫 번째 user 메시지로 주입 (Gemini 대화 형식)
        contents = []
        # 시스템 프롬프트를 첫 번째 user 메시지로 래핑
        system_injected = False
        for msg in history:
            if not system_injected and msg['role'] == 'user':
                contents.append({
                    "role": "user",
                    "parts": [{"text": system_prompt + "\n\n사용자: " + msg['parts'][0]['text']}]
                })
                system_injected = True
            else:
                contents.append(msg)

        # 현재 메시지 추가
        if not system_injected:
            contents.append({
                "role": "user",
                "parts": [{"text": system_prompt + "\n\n사용자: " + user_message}]
            })
        else:
            contents.append({
                "role": "user",
                "parts": [{"text": user_message}]
            })

        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": 800,
            }
        }
        resp = requests.post(url, json=payload, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            candidates = data.get('candidates', [])
            if candidates:
                return candidates[0].get('content', {}).get('parts', [{}])[0].get('text', '')
        logger.debug(f"Gemini 대화 API 응답 오류: {resp.status_code} {resp.text[:200]}")
        return ""
    except Exception as e:
        logger.debug(f"Gemini 대화형 호출 실패: {e}")
        return ""


# ──────────────────────────────────────────────
# 인텐트 분류 (V5.6: 강화)
# ──────────────────────────────────────────────
def classify_intent(text: str) -> dict:
    """텍스트 의도 분류 (키워드 기반 → 빠르고 안정적)"""
    t = text.lower().strip()

    # 1. 엑시트 전략 (평단/목표가) - 최우선 순위
    exit_keywords = ['평단', '얼마에 파', '어디서 파', '언제 팔', '매도 타점', '목표가', '익절', '손절', '탈출', '언제 털', '어디서 털']
    if any(k in t for k in exit_keywords):
        return {'intent': 'EXIT_STRATEGY'}

    # 2. 거래 전략 및 차트 분석 요청 (V6.5 강화 - 차트 보장 키워드 우선)
    # [주의] '포지션' 단어가 있어도 '분석', '차트', '어때' 등이 있으면 분석으로 분류
    analysis_keywords = ['분석', '어때', '어떻게', '봐줘', '차트', '매수', '매도', 'long', 'short', '롱', '숏', '전망', '갈까', '올라가', '내려가', '보여줘']
    strategy_keywords = ['전략', '시나리오', '진입 라인', '어떻게 매매', '전략 짜', '어디서 진입', '어디서 잡', '방향성', '예측', '어떻게 될까', '관점', '진입가']
    
    if any(k in t for k in strategy_keywords):
        return {'intent': 'TRADE_STRATEGY'}
    
    if any(k in t for k in analysis_keywords) or '?' in t:
        return {'intent': 'ANALYSIS'}

    # 3. 전문가 관점 학습/가져오기 (V6.2 신규)
    learn_keywords = ['학습', '가져와', '가져오기', '텔레그램 관점', '전문가', '뉴스', '동향', '읽어봐', '읽어줘']
    if any(k in t for k in learn_keywords):
        return {'intent': 'LEARN_EXPERTS'}

    # 4. 상태/잔고 (분석 키워드가 없을 때만 상태 확인으로 분류)
    status_keywords = ['잔고', '얼마', '수익', '손익', '현황', '포지션', '상태', '승률', '몇 번', '몇번', '벌었', '까먹']
    if any(k in t for k in status_keywords):
        return {'intent': 'STATUS'}

    # 5. 일반 대화
    return {'intent': 'CHAT'}


def get_symbol_from_text(text: str) -> Optional[str]:
    """텍스트에서 코인명을 찾아 바이낸스 심볼(USDT)로 반환"""
    mapping = {
        '비트': 'BTCUSDT', '비트코인': 'BTCUSDT', 'btc': 'BTCUSDT',
        '이더': 'ETHUSDT', '이더리움': 'ETHUSDT', 'eth': 'ETHUSDT',
        '솔라나': 'SOLUSDT', '솔': 'SOLUSDT', 'sol': 'SOLUSDT',
        '리플': 'XRPUSDT', 'xrp': 'XRPUSDT',
        '도지': 'DOGEUSDT', 'doge': 'DOGEUSDT',
        '에이다': 'ADAUSDT', 'ada': 'ADAUSDT',
        '아발': 'AVAXUSDT', '아발란체': 'AVAXUSDT', 'avax': 'AVAXUSDT',
        '매틱': 'MATICUSDT', '폴리곤': 'MATICUSDT', 'matic': 'MATICUSDT',
        '수이': 'SUIUSDT', 'sui': 'SUIUSDT',
        '세이': 'SEIUSDT', 'sei': 'SEIUSDT',
    }
    t = text.lower()
    for k, v in mapping.items():
        if k in t:
            return v
            
    # 정적 매핑에 없을 경우: 영어 알파벳 1~6자로 된 단어를 찾아서 USDT를 붙여봄 ("aster", "pepe" 등)
    # 한글/영어 혼용 텍스트에서 영어 단어만 추출
    import re
    matches = re.findall(r'\b[a-zA-Z]{1,8}\b', t)
    for word in matches:
        word = word.upper()
        # 일반적으로 쓰이는 보조 단어 필터링 (long, short, usdt 등)
        if word not in ['LONG', 'SHORT', 'USDT', 'BUY', 'SELL', 'THE', 'AND', 'IS', 'IN', 'ON', 'AT']:
            return f"{word}USDT"
            
    return None


# ──────────────────────────────────────────────
# 핵심: 컨텍스트 포함 AI 대화 응답 (V5.6 신규)
# ──────────────────────────────────────────────
def generate_contextual_chat_response(
        text: str,
        chat_id: int,
        account_context: Optional[dict] = None
) -> str:
    """
    실계좌 데이터 + 대화 이력을 포함한 AI 응답 생성 (V5.6 AI 대화버전 핵심)

    account_context 예시:
    {
        'balance': 254.65,
        'available': 230.0,
        'open_positions': [{'symbol': 'BTCUSDT', 'direction': 'SHORT', 'pnl_pct': -3.2}],
        'win_rate': 45.0,
        'total_trades': 18,
        'today_pnl': -6.41,
        'recent_trades': [{'symbol': 'BTCUSDT', 'direction': 'SHORT', 'pnl': -2.1, 'reason': 'SL'}],
        'cycle_count': 120,
    }
    """
    # 대화 이력 가져오기
    history = list(_get_history(chat_id))

    # 계좌 컨텍스트 문자열 구성
    ctx_lines = []
    if account_context:
        bal = account_context.get('balance', 0)
        avail = account_context.get('available', 0)
        positions = account_context.get('open_positions', [])
        win_rate = account_context.get('win_rate', 0)
        total_trades = account_context.get('total_trades', 0)
        today_pnl = account_context.get('today_pnl', 0)
        recent = account_context.get('recent_trades', [])
        cycle = account_context.get('cycle_count', 0)

        ctx_lines.append(f"[실계좌 현황 - {datetime.now().strftime('%H:%M')} 기준]")
        ctx_lines.append(f"잔고: ${bal:.2f} USDT (가용: ${avail:.2f})")
        ctx_lines.append(f"오늘 손익: ${today_pnl:+.2f} USDT")
        ctx_lines.append(f"승률: {win_rate:.1f}% ({total_trades}회 거래)")
        ctx_lines.append(f"스캔 사이클: {cycle}회 완료")

        if positions:
            ctx_lines.append(f"현재 보유 포지션 {len(positions)}개:")
            for p in positions:
                ctx_lines.append(f"  - {p.get('symbol')} {p.get('direction')} | PnL: {p.get('pnl_pct', 0):+.1f}%")
        else:
            ctx_lines.append("현재 보유 포지션: 없음")

        if recent:
            ctx_lines.append(f"최근 거래 {min(3, len(recent))}개:")
            for t in recent[:3]:
                ctx_lines.append(f"  - {t.get('symbol')} {t.get('direction')} → ${t.get('pnl', 0):+.2f} ({t.get('reason', '-')})")

    ctx_str = "\n".join(ctx_lines) if ctx_lines else "계좌 데이터 없음"

    # 시스템 프롬프트
    system_prompt = f"""당신은 바이낸스 선물 자동매매 봇 'ChoiGPT'입니다.
Team Mensa의 순수 SMC(Smart Money Concepts) 및 ICT 방법론 전문가로서, 운영자인 사용자의 수석 매매 파트너입니다.
아래 실계좌 데이터와 분석 결과를 참고하여 솔직하고 전문적인 한국어 답변을 하세요.

{ctx_str}

답변 규칙:
- 2-4문장으로 핵심만 (매우 간결하게)
- 실제 수치 언급 (잔고, 손익 등)
- SMC 핵심 용어(HTF Bias, Liquidity Sweep, MSS, FVG, OB, OTE)를 전문적으로 사용
- 전략적 관점에서 냉철하게 분석
- 이모지 적당히 사용
- [중요] Ross 기법이나 곰젤리 등 레거시 전략은 언급하지 마세요. 오직 ICT/SMC 관점만 유지합니다."""

    # Gemini 대화형 호출
    response = _call_gemini_with_history(system_prompt, history, text, temperature=0.55)

    if not response:
        # 폴백: 단순 호출
        response = _call_gemini(
            f"{system_prompt}\n\n사용자: {text}\nChoiGPT:",
            temperature=0.55, max_tokens=1000
        )

    return response.strip()


def generate_exit_strategy_analysis(symbol: str, entry_price_usdt: float, analysis_result,
                                    curr_price: float = 0.0,
                                    premium_pct: float = 0.0, ex_rate: float = 1400.0) -> str:
    """사용자 평단 기반 고수급 엑시트 전략 제안 (V5.9: curr_price 직접 수신)"""
    try:
        # curr_price는 caller에서 직접 전달받음 (analysis_result에 없는 속성)
        rsi_info = getattr(analysis_result, 'rsi_info', None)
        rsi_val = (rsi_info or {}).get('rsi', 50) if rsi_info else 50
        pd_zone = getattr(analysis_result, 'pd_zone', None) or {}
        zone = pd_zone.get('zone', 'UNKNOWN')
        
        # 저항 구간 추출 (안전하게)
        resistances = []
        try:
            fvgs = getattr(analysis_result, 'fvgs', []) or []
            obs = getattr(analysis_result, 'order_blocks', []) or []
            for f in [f for f in fvgs if not getattr(f, 'is_bullish', True)][-2:]:
                resistances.append(f"{f.bottom:.2f}~{f.top:.2f}")
            for o in [o for o in obs if not getattr(o, 'is_bullish', True)][-1:]:
                resistances.append(f"{o.low:.2f}~{o.high:.2f}")
        except Exception:
            pass
        
        res_str = ", ".join(resistances) if resistances else "주요 저항 확인 중"
        
        # 수익률 계산
        pnl_pct = (curr_price / entry_price_usdt - 1) * 100 if (curr_price > 0 and entry_price_usdt > 0) else 0
        pnl_emoji = "🟢" if pnl_pct >= 0 else "🔴"

        prompt = f"""
당신은 순수 SMC/ICT 전문 트레이더 'ChoiGPT 마스터'입니다.
사용자가 국내 거래소(업비트/빗썸) 평단을 기준으로 '엑시트 전략'을 묻고 있습니다.
아래 실시간 김치 프리미엄 데이터를 반영하여 SMC 관점의 '고수의 조언'을 하세요.

분석 대상: {symbol}
바이낸스 현재가: {curr_price:,.2f} USDT
김치 프리미엄: {premium_pct:.2f}% (적용 환율: {ex_rate:,.1f}원)
사용자 평단(USDT 환산): {entry_price_usdt:,.2f} (현재 {pnl_emoji} {pnl_pct:+.2f}%)

기술적 지표: SMC Bias 및 P/D 존 {zone}
감지된 바이낸스 저항(SMC OB/FVG): {res_str}

답변 규칙:
- "알렉스님,"으로 시작
- 현재 김프 수치를 언급하며 국내 거래소와의 가격 차이를 설명
- 바이낸스 저항 구간(SMC POI)을 **국내 거래소 가격(KRW)**으로 변환하여 구체적 목표가 제시 (목표가 = USDT저항 * 환율 * (1 + 김프/100))
- 3-4문장으로 간결하고 전문적인 SMC 용어(POI, Liquidity)를 사용하여 작성
"""
        response = _call_gemini(prompt, temperature=0.6, max_tokens=1000)
        if response and response.strip():
            return response.strip()

        # ── Gemini 응답 실패 시 로컈 분석 폴백 ──
        pnl_emoji2 = "🟢" if pnl_pct >= 0 else "🔴"
        zone_kr = {
            'PREMIUM': '프리미엄(고가) 오버트', 'DISCOUNT': '디스카운트(저가) 구간', 'EQUILIBRIUM': '중립(%50) 구간'
        }.get(zone, '횡보 중립')
        first_res = resistances[0] if resistances else None
        if first_res and ex_rate > 0:
            try:
                res_lo, res_hi = [float(v) for v in first_res.split('~')]
                t1_krw = round(res_lo * ex_rate * (1 + premium_pct / 100), -2)
                t2_krw = round(res_hi * ex_rate * (1 + premium_pct / 100), -2)
                res_krw_str = f"{t1_krw:,.0f}원 ~ {t2_krw:,.0f}원"
            except Exception:
                res_krw_str = "저항구산 확인 필요"
        else:
            res_krw_str = "저항구산 확인 필요"
        curr_krw = round(curr_price * ex_rate * (1 + premium_pct / 100), -2) if curr_price > 0 else 0
        local_report = (
            f"알렉스님, 현재 {symbol}은 {zone_kr}에 위치해 RSI {rsi_val:.0f} / 현재 빗썸 추정가 약 {curr_krw:,.0f}원입니다. "
            f"평단 대비 {pnl_emoji2} {pnl_pct:+.2f}% 수익구간이며, "
            f"강력한 상방 저항 대를 {res_krw_str or '앞 저항'}으로 분석하고 있습니다. "
            f"해당 구간에서 주의용 캔들이 나오면 분할 익절을 권장하며, "
            f"평단({curr_price * ex_rate:,.0f}원 기준) 아래로 다시 내려오면 본절 로스 설정을 추천합니다."
        )
        return local_report
    except Exception as e:
        logger.error(f"엑시트 전략 생성 실패: {e}")
        return "죄송합니다. 분석 중 오류가 발생했습니다."

def generate_trade_strategy_analysis(symbol: str, analysis_result, curr_price: float = 0.0, user_prompt: str = "") -> str:
    if analysis_result is None: return "현재 {symbol}에 대한 분석 데이터가 부족하여 전략 생성이 불가능합니다."
    """실시간 차트 분석 데이터를 기반으로 최적의 진입/손절 전략 브리핑을 제공합니다 (TRADE_STRATEGY)."""
    try:
        rsi_info = getattr(analysis_result, 'rsi_info', None)
        rsi_val = (rsi_info or {}).get('rsi', 50) if rsi_info else 50
        
        pd_zone = getattr(analysis_result, 'pd_zone', None) or {}
        zone = pd_zone.get('zone', 'UNKNOWN')
        
        htf_trend = getattr(analysis_result.htf_ms, 'trend', 'UNKNOWN') if getattr(analysis_result, 'htf_ms', None) else 'UNKNOWN'
        ltf_trend = getattr(analysis_result.ltf_ms, 'trend', 'UNKNOWN') if getattr(analysis_result, 'ltf_ms', None) else 'UNKNOWN'

        # 지지 / 저항 구간 추출
        supports = []
        resistances = []
        try:
            fvgs = getattr(analysis_result, 'fvgs', []) or []
            obs = getattr(analysis_result, 'order_blocks', []) or []
            # Bullish = Support
            for f in [f for f in fvgs if getattr(f, 'is_bullish', True)][-2:]:
                supports.append(f"FVG {f.bottom:,.2f}~{f.top:,.2f}")
            for o in [o for o in obs if getattr(o, 'is_bullish', True)][-1:]:
                supports.append(f"OB {o.high:,.2f}~{o.low:,.2f}")
                
            # Bearish = Resistance
            for f in [f for f in fvgs if not getattr(f, 'is_bullish', True)][-2:]:
                resistances.append(f"FVG {f.bottom:,.2f}~{f.top:,.2f}")
            for o in [o for o in obs if not getattr(o, 'is_bullish', True)][-1:]:
                resistances.append(f"OB {o.low:,.2f}~{o.high:,.2f}")
        except Exception:
            pass
            
        sup_str = ", ".join(supports) if supports else "뚜렷한 지지선 없음"
        res_str = ", ".join(resistances) if resistances else "뚜렷한 저항선 없음"

        prompt = f"""
당신은 Team Mensa 스타일의 순수 SMC/ICT 전문 트레이더 'ChoiGPT 마스터'입니다.
사용자가 텔레그램에서 '{symbol}' 종목에 대한 **실전 SMC 매매 전략**을 묻고 있습니다.

{f"[사용자 특별 요청/질문]: {user_prompt}" if user_prompt else ""}

[실시간 시장 데이터]
- 종목: {symbol}
- 현재가: {curr_price:,.2f} USDT
- 구조적 타임프레임 추세 (1H/15m): {htf_trend} / {ltf_trend}
- 가격 위치 (Premium/Discount): {zone}
- 과매수/과매도 (RSI): {rsi_val:.1f}
- 핵심 지지대 (롱 진입점/숏 목표가): {sup_str}
- 핵심 저항대 (숏 진입점/롱 목표가): {res_str}

답변 규칙:
1. "안녕하세요, ChoiGPT 마스터입니다."로 시작하지 말고 바로 본론부터 이야기해 주세요.
2. 현재 시장의 거시적 추세(BULLISH/BEARISH/RANGING)와 가격의 유리함을 먼저 짚어주세요. 사용자가 질문에 경제 지표(PPI, CPI, FOMC 등) 등 특정 문맥을 언급했다면 이를 종합하여 단기 시황 예측을 추가해 주세요.
3. 롱(Long) 전략과 숏(Short) 전략 중 현재 더 유리한 방향을 먼저 하나 찍어주세요.
4. 단기 스캘핑/단타 관점뿐만 아니라, **1H나 4H 등 큰 흐름(HTF)을 이용해 저점 매수/고점 매도를 노리는 '중장기 스윙 전략'**도 분리하여 필수적으로 작성해 주세요. (넓은 타점과 목표가로 손익비를 챙기는 관점)
5. 각 전략(단기/스윙)별로 구체적인 '진입 타점(Entry)', '구조적 손절 라인(SL, 이유 포함)', '1차 목표가(TP1)'를 수치와 함께 명확하게 한국어로 제시하세요.
6. 4~5문장으로 전문적이면서도 읽기 편하게 Markdown 볼드체(**)를 적절히 활용하세요.
7. [중요] 사용자가 차트를 그려달라고 해도 절대로 Mermaid나 코드 블록 형태의 가상 차트를 텍스트로 그리지 마세요. 실제 차트 이미지는 봇 시스템이 알아서 첨부할 것입니다.
"""
        response = _call_gemini(prompt, temperature=0.6, max_tokens=1500)
        
        if response and response.strip():
            return response.strip()
            
        return f"현재 {symbol} ({curr_price:,.2f} USDT) 1H 추세는 {htf_trend}에 P/D Zone은 {zone} 위치입니다. 위로는 {res_str[:30]}, 아래로는 {sup_str[:30]} 구간이 열려있습니다. 지지/저항 라인에 도달할 때까지 관망하시는 것을 추천합니다."
    except Exception as e:
        logger.error(f"전략 분석 생성 실패: {e}")
        return "죄송합니다. 전략 분석 중 오류가 발생했습니다."

# ──────────────────────────────────────────────
# 기존 함수 (하위 호환성 유지)
# ──────────────────────────────────────────────
def generate_chat_response(text: str) -> str:
    """채팅 응답 생성 (하위 호환성 - 컨텍스트 없는 버전)"""
    return generate_contextual_chat_response(text, chat_id=0, account_context=None)


def generate_analysis_with_gemini(analysis_result, symbol: str) -> str:
    """ICT 관점 AI 분석 텍스트 생성 (V5.5 유지)"""
    if analysis_result is None:
        return ""
    try:
        ltf_trend = getattr(analysis_result.ltf_ms, 'trend', 'UNKNOWN') if getattr(analysis_result, 'ltf_ms', None) else 'UNKNOWN'
        htf_trend = getattr(analysis_result.htf_ms, 'trend', 'UNKNOWN') if getattr(analysis_result, 'htf_ms', None) else 'UNKNOWN'
        pd_zone = getattr(analysis_result, 'pd_zone', None) or {}
        zone = pd_zone.get('zone', 'UNKNOWN')
        zone_pos = pd_zone.get('current_position', 0.5)
        fvg_count = len(analysis_result.fvgs) if getattr(analysis_result, 'fvgs', None) else 0
        ob_count = len(analysis_result.order_blocks) if getattr(analysis_result, 'order_blocks', None) else 0
        rsi_val = (getattr(analysis_result, 'rsi_info', {}) or {}).get('rsi', 50)
        signal = analysis_result.signal

        if not signal:
            return ""

        smc_steps = getattr(analysis_result, 'smc_steps', {})
        sweep_info = "감지됨" if smc_steps.get(2, -1) > 1 else "미감지"
        mss_info = "발생 (Displacement 확인)" if smc_steps.get(3, -1) > 1 else "미발생"

        prompt = f"""
당신은 Team Mensa 스타일의 순수 SMC/ICT 전문 트레이더입니다.
다음 데이터를 바탕으로 한국어로 3-4문장의 간결한 진입 근거를 작성하세요.
철저하게 1. Bias → 2. Sweep → 3. MSS → 4. Entry 순차적 로직으로 설명하세요.

심볼: {symbol} | 방향: {signal.direction}
전략: {'SMC 스캘핑' if getattr(signal, 'mode', 'NORMAL') == 'SCALP' else 'SMC 스나이퍼'}
1. HTF Bias: {htf_trend}
2. Liquidity Sweep: {sweep_info}
3. MSS/Displacement: {mss_info}
4. POI/Entry: {zone} 구역 OTE/FVG 터치
확신도: {signal.confidence:.0%}

형식: 각 단계를 언급하며 전문적으로 3-4문장 (이모지 사용)
[주의] Ross, 곰젤리, 하모닉 패턴에 대한 언급은 일체 금지합니다.
"""
        result = _call_gemini(prompt)
        return result.strip() if result else ""
    except Exception as e:
        logger.debug(f"AI 분석 생성 실패: {e}")
        return ""


def format_telegram_message(analysis_result, symbol: str, current_price: float, timeframe: str = "1H") -> str:
    """분석 결과를 텔레그램용 메시지로 포맷팅 (V5.5 유지)"""
    ai_text = generate_analysis_with_gemini(analysis_result, symbol)

    if hasattr(analysis_result, 'analysis_text') and analysis_result.analysis_text:
        base_text = analysis_result.analysis_text
    else:
        base_text = f"📊 {symbol} 분석\n⏰ {timeframe}\n💰 현재가: {current_price:.4f} USDT"

    if ai_text:
        return base_text + f"\n\n🤖 <b>AI 판단:</b>\n{ai_text}"
    return base_text