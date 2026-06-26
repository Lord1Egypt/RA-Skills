"""
doc_structurer.py - 문서 구조화 스크립트
parsed_results.json을 읽어 문서 유형 분류 + 핵심 정보 추출
"""

import os
import sys
import json
import re
import uuid
from datetime import datetime, timedelta

# --- 문서 유형 분류 ---
CATEGORY_KEYWORDS = {
    "공문": ["수신", "발신", "시행", "문서번호", "관인", "협조", "시행일자", "공문"],
    "계약서": ["계약", "갑", "을", "조항", "위약금", "계약기간", "계약금", "쌍방"],
    "제안서": ["제안", "사업개요", "추진전략", "기대효과", "RFP", "제안요청"],
    "보고서": ["보고", "결과", "분석", "현황", "추진실적", "성과"],
    "회의록": ["회의", "참석자", "안건", "결정사항", "회의일시", "회의록"],
    "기획서": ["기획", "목적", "일정", "예산", "추진방안", "기획서"],
    "견적서": ["견적", "단가", "수량", "합계", "부가세", "공급가", "견적서"],
    "증명서": ["증명", "확인서", "발급", "용도", "증명서"],
}

def classify_document(filename, text):
    """파일명 + 본문 키워드 빈도로 문서 유형 분류"""
    scores = {}

    # 1차: 파일명 키워드 (가중치 3)
    fname_lower = filename.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(3 for kw in keywords if kw in fname_lower)
        scores[category] = score

    # 2차: 본문 키워드 빈도 (가중치 1, 앞 2000자만)
    text_sample = text[:2000] if text else ""
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_sample)
        scores[category] = scores.get(category, 0) + score

    if not scores or max(scores.values()) == 0:
        return "기타", 0.3

    best_category = max(scores, key=scores.get)
    best_score = scores[best_category]
    total_score = sum(scores.values())
    confidence = round(best_score / max(total_score, 1), 2)

    # confidence 보정: 최소 0.3, 최대 0.99
    confidence = min(max(confidence, 0.3), 0.99)

    return best_category, confidence


# --- 날짜 추출 및 정규화 ---
DATE_PATTERNS = [
    (r'(\d{4})\s*년\s*(\d{1,2})\s*월\s*(\d{1,2})\s*일', '%Y-%m-%d'),
    (r'(\d{4})[.\-/](\d{1,2})[.\-/](\d{1,2})', '%Y-%m-%d'),
    (r'(\d{2})[.\-/](\d{1,2})[.\-/](\d{1,2})', '%Y-%m-%d'),  # 2자리 연도
]

DEADLINE_KEYWORDS = ["마감", "기한", "까지", "제출일", "납기", "시한", "만료"]
EVENT_KEYWORDS = ["행사", "개최", "일시", "회의일", "설명회", "공청회"]
START_KEYWORDS = ["시작", "착수", "개시", "계약기간"]
END_KEYWORDS = ["종료", "완료", "만료", "계약기간"]

def extract_dates(text):
    """본문에서 날짜들을 추출하고 유형별로 분류"""
    current_year = datetime.now().year
    dates_found = []

    for pattern, _ in DATE_PATTERNS:
        for match in re.finditer(pattern, text):
            groups = match.groups()
            try:
                year = int(groups[0])
                month = int(groups[1])
                day = int(groups[2])

                if year < 100:
                    year += 2000
                if not (1 <= month <= 12 and 1 <= day <= 31):
                    continue

                date_str = f"{year:04d}-{month:02d}-{day:02d}"
                # 주변 텍스트(±30자)로 유형 판별
                start = max(0, match.start() - 30)
                end = min(len(text), match.end() + 30)
                context = text[start:end]

                date_type = "document_date"
                if any(kw in context for kw in DEADLINE_KEYWORDS):
                    date_type = "deadline"
                elif any(kw in context for kw in EVENT_KEYWORDS):
                    date_type = "event_date"
                elif any(kw in context for kw in START_KEYWORDS):
                    date_type = "start_date"
                elif any(kw in context for kw in END_KEYWORDS):
                    date_type = "end_date"

                dates_found.append({"date": date_str, "type": date_type, "context": context.strip()})

            except (ValueError, IndexError):
                continue

    return dates_found


# --- 금액 추출 ---
AMOUNT_PATTERN = re.compile(r'(\d[\d,]*)\s*(?:원|₩|KRW|won)', re.IGNORECASE)

def extract_financial(text):
    """금액 정보 추출"""
    amounts = []
    for match in AMOUNT_PATTERN.finditer(text):
        amount_str = match.group(1).replace(',', '')
        try:
            amount = int(amount_str)
            if amount >= 1000:  # 1000원 이상만
                amounts.append(amount)
        except ValueError:
            continue

    if amounts:
        return {"total_amount": max(amounts), "currency": "KRW", "line_items": []}
    return {"total_amount": None, "currency": "KRW", "line_items": []}


# --- 핵심 인물/기관 추출 ---
def extract_entities(text):
    """담당자, 발신기관, 수신처 추출"""
    entities = {"assignee": None, "organization": None, "recipient": None}

    # 수신/발신 패턴
    recv_match = re.search(r'수\s*신\s*[:：]?\s*(.+?)[\n\r]', text)
    if recv_match:
        entities["recipient"] = recv_match.group(1).strip()[:50]

    send_match = re.search(r'발\s*신\s*[:：]?\s*(.+?)[\n\r]', text)
    if send_match:
        entities["organization"] = send_match.group(1).strip()[:50]

    # 담당자 패턴
    assignee_match = re.search(r'(?:담당|작성|기안)\s*(?:자|)\s*[:：]?\s*(.+?)[\n\r\s]', text)
    if assignee_match:
        entities["assignee"] = assignee_match.group(1).strip()[:20]

    return entities


# --- 우선순위 판정 ---
def determine_priority(dates, text, financial):
    """마감일, 키워드, 금액 기반 우선순위 판정"""
    priority = "하"

    # 마감일 기반
    deadline = dates.get("deadline")
    if deadline:
        try:
            dl = datetime.strptime(deadline, '%Y-%m-%d')
            days_left = (dl - datetime.now()).days
            if days_left <= 3:
                priority = "상"
            elif days_left <= 7:
                priority = "중"
        except ValueError:
            pass

    # 키워드 상향
    urgent_keywords = ["긴급", "시급", "즉시", "조속", "긴급공문"]
    if any(kw in text[:500] for kw in urgent_keywords):
        priority = "상"

    # 금액 상향 (1억 이상)
    if financial.get("total_amount") and financial["total_amount"] >= 100_000_000:
        if priority != "상":
            priority = "상"

    return priority


# --- 관련 문서 연결 ---
def find_related_docs(current_filename, all_filenames, text):
    """파일명 유사도 + 본문 참조로 관련 문서 탐지"""
    related = []
    base = os.path.splitext(current_filename)[0]

    for other in all_filenames:
        if other == current_filename:
            continue
        other_base = os.path.splitext(other)[0]

        # 파일명 유사도
        if base[:5] == other_base[:5]:  # 앞 5자 일치
            related.append(other)
        elif other_base in text[:3000]:  # 본문에서 언급
            related.append(other)

    return list(set(related))


# --- 요약 생성 (간이) ---
def generate_summary(text, max_lines=3):
    """본문에서 핵심 문장 추출 (간이 요약)"""
    if not text:
        return ""

    sentences = re.split(r'[.\n。]', text[:1500])
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]

    return ' | '.join(sentences[:max_lines]) if sentences else text[:200]


# --- 메인: 구조화 처리 ---
def structure_documents(input_path, output_path=None):
    """parsed_results.json을 읽어 구조화된 데이터로 변환"""
    with open(input_path, 'r', encoding='utf-8') as f:
        parsed_docs = json.load(f)

    all_filenames = [doc["filename"] for doc in parsed_docs]
    results = []
    stats = {"total": 0, "by_type": {}, "low_confidence": 0, "missing_fields": 0}

    for doc in parsed_docs:
        stats["total"] += 1

        # 에러 문서 스킵
        if "error" in doc:
            results.append({
                "doc_id": str(uuid.uuid4()),
                "title": doc["filename"],
                "doc_type": "기타",
                "doc_type_confidence": 0.0,
                "error": doc["error"],
                "raw_metadata": {
                    "filename": doc["filename"],
                    "filepath": doc.get("filepath", ""),
                    "file_type": doc.get("file_type", ""),
                    "page_count": 0,
                    "ocr_applied": False
                }
            })
            continue

        text = doc.get("raw_text", "")
        filename = doc["filename"]

        # 분류
        doc_type, confidence = classify_document(filename, text)
        stats["by_type"][doc_type] = stats["by_type"].get(doc_type, 0) + 1
        if confidence < 0.7:
            stats["low_confidence"] += 1

        # 날짜 추출
        dates_list = extract_dates(text)
        dates = {
            "document_date": None,
            "deadline": None,
            "start_date": None,
            "end_date": None,
            "event_dates": []
        }
        for d in dates_list:
            if d["type"] == "event_date":
                dates["event_dates"].append(d["date"])
            elif d["type"] in dates:
                if dates[d["type"]] is None:
                    dates[d["type"]] = d["date"]

        # 금액
        financial = extract_financial(text)

        # 인물/기관
        entities = extract_entities(text)

        # 우선순위
        priority = determine_priority(dates, text, financial)

        # 관련 문서
        related = find_related_docs(filename, all_filenames, text)

        # 태그 생성
        tags = [doc_type]
        if doc.get("ocr_applied"):
            tags.append("OCR")
        if financial.get("total_amount"):
            tags.append("금액포함")
        if dates.get("deadline"):
            tags.append("마감일있음")

        # 누락 필드 체크
        missing = []
        if not entities.get("assignee"):
            missing.append("담당자")
        if not dates.get("document_date"):
            missing.append("작성일")
        if missing:
            stats["missing_fields"] += 1

        structured = {
            "doc_id": str(uuid.uuid4()),
            "title": os.path.splitext(filename)[0],
            "doc_type": doc_type,
            "doc_type_confidence": confidence,
            "summary": generate_summary(text),
            "assignee": entities.get("assignee"),
            "organization": entities.get("organization"),
            "recipient": entities.get("recipient"),
            "dates": dates,
            "priority": priority,
            "status": "신규",
            "tags": tags,
            "financial": financial,
            "related_docs": related,
            "attachments": doc.get("attachment_list", []),
            "key_items": [],
            "action_items": [],
            "raw_metadata": {
                "filename": filename,
                "filepath": doc.get("filepath", ""),
                "file_type": doc.get("file_type", ""),
                "page_count": doc.get("page_count", 0),
                "ocr_applied": doc.get("ocr_applied", False)
            }
        }
        results.append(structured)

    # 결과 저장
    if output_path is None:
        output_path = os.path.join(os.path.dirname(input_path), "structured_results.json")

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # 요약 출력
    print(f"\n🏗️ 문서 구조화 완료")
    print(f"  - 총 처리: {stats['total']}개")
    type_str = ", ".join(f"{k} {v}" for k, v in stats["by_type"].items())
    print(f"  - 유형 분포: {type_str}")
    print(f"  - 주의 필요: {stats['low_confidence']}개 (낮은 신뢰도), {stats['missing_fields']}개 (누락 필드)")
    print(f"  - 결과 저장: {output_path}")

    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python doc_structurer.py <parsed_results.json 경로> [출력경로]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    structure_documents(input_file, output_file)
