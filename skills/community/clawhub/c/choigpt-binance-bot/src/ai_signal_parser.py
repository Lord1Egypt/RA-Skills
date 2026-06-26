import os
import json
import logging
import requests
from datetime import datetime
from dotenv import load_dotenv
from config.config import GOOGLE_API_KEY, GEMINI_MODEL, GEMINI_API_URL

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("AISignalParser")

# .env 로드
load_dotenv(override=True)

RAW_DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'telegram_raw_messages.json')
PARSED_DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'parsed_expert_signals.json')

class AISignalParser:
    def __init__(self):
        self.api_key = GOOGLE_API_KEY
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY가 설정되지 않았습니다.")

    def parse_new_messages(self):
        """아직 파싱되지 않은 메시지들을 AI로 분석합니다."""
        raw_data = self._load_json(RAW_DATA_FILE)
        if not raw_data:
            logger.info("ℹ️ 분석할 메시지가 없습니다.")
            return 0

        parsed_signals = self._load_json(PARSED_DATA_FILE)
        new_count = 0

        for msg_id, msg_data in raw_data.items():
            if msg_data.get("parsed", False):
                continue

            logger.info(f"🧠 메시지 분석 중: {msg_data['channel']} - {msg_id}")
            
            # AI 분석 시도
            signal = self._analyze_text_with_gemini(msg_data['text'])
            
            if signal and signal.get("is_valid_signal"):
                signal["id"] = msg_id
                signal["original_channel"] = msg_data["channel"]
                signal["original_date"] = msg_data["date"]
                signal["parsed_at"] = datetime.now().isoformat()
                
                parsed_signals[msg_id] = signal
                raw_data[msg_id]["parsed"] = True
                new_count += 1
            else:
                # 유효한 신호가 아니더라도 일단 파싱 시도한 것으로 체크 (반복 분석 방지)
                raw_data[msg_id]["parsed"] = True
                logger.debug(f"ℹ️ 유효한 타점이 아닙니다: {msg_id}")

        if new_count > 0:
            self._save_json(PARSED_DATA_FILE, parsed_signals)
            self._save_json(RAW_DATA_FILE, raw_data)
            logger.info(f"✅ 총 {new_count}개의 새로운 타점 신호를 추출했습니다.")
        
        return new_count

    def _analyze_text_with_gemini(self, text):
        """Gemini API를 사용하여 비정형 텍스트에서 트레이딩 신호를 추출합니다."""
        prompt = f"""
        다음은 트레이딩 전문가 채널의 텔레그램 메시지입니다. 
        이 텍스트에서 구체적인 매매 타점(Signal) 정보를 추출하여 JSON 형식으로 응답하세요.
        반드시 JSON 형식만 출력해야 하며, 분석 결과가 타점이 아닌 경우 is_valid_signal을 false로 하세요.

        [메시지 내용]
        {text}

        [추출 항목 JSON 스키마]
        {{
            "is_valid_signal": boolean (구체적인 진입가, 손절가가 포함된 매매 권유인지 여부),
            "symbol": string (예: BTCUSDT, ETHUSDT),
            "side": string (LONG 또는 SHORT),
            "entry_price": number 또는 [number, number] (진입 가격대),
            "target_prices": [number] (익절가 목표 리스트),
            "stop_loss": number (손절가),
            "rationale": string (SMC, ICT, OB, FVG 등 핵심 분석 근거 요약),
            "confidence": number (말투나 근거의 명확성 기준 0~1 사이의 신뢰도)
        }}
        """

        try:
            url = GEMINI_API_URL.format(model=GEMINI_MODEL, key=self.api_key)
            headers = {'Content-Type': 'application/json'}
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.1,
                    "topP": 0.8,
                    "topK": 40
                }
            }

            response = requests.post(url, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                content = result['candidates'][0]['content']['parts'][0]['text']
                
                # 마크다운 제거 및 JSON 파싱
                cleaned_content = content.replace("```json", "").replace("```", "").strip()
                return json.loads(cleaned_content)
            else:
                logger.error(f"❌ Gemini API 오류: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logger.error(f"❌ 분석 중 오류 발생: {e}")
            return None

    def _load_json(self, file_path):
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _save_json(self, file_path, data):
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"❌ 파일 저장 오류: {e}")

if __name__ == "__main__":
    parser = AISignalParser()
    parser.parse_new_messages()
