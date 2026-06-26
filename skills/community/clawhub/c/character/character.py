#!/usr/bin/env python3
"""
MBTI character skill for OpenClaw.
基于极速数据性格测试（MBTI）API：
https://www.jisuapi.com/api/character/
"""

import json
import os
import sys
from typing import Any

import requests


QUESTIONS_URL = "https://api.jisuapi.com/character/questions"
ANSWER_URL = "https://api.jisuapi.com/character/answer"


def _normalize_version(version: Any) -> str:
    v = (str(version) if version is not None else "").strip().lower()
    return v or "full"


def _call_api(url: str, appkey: str, params: dict = None) -> Any:
    query = {"appkey": appkey}
    if params:
        query.update({k: v for k, v in params.items() if v not in (None, "")})

    try:
        resp = requests.get(url, params=query, timeout=15)
    except Exception as e:
        return {"error": "request_failed", "message": str(e)}

    if resp.status_code != 200:
        return {"error": "http_error", "status_code": resp.status_code, "body": resp.text}

    try:
        data = resp.json()
    except Exception:
        return {"error": "invalid_json", "body": resp.text}

    if data.get("status") != 0:
        return {"error": "api_error", "code": data.get("status"), "message": data.get("msg")}

    return data.get("result")


def get_questions(appkey: str, version: str) -> Any:
    if version not in ("full", "simple"):
        return {"error": "invalid_param", "message": "version must be 'full' or 'simple'"}
    return _call_api(QUESTIONS_URL, appkey, {"version": version})


def get_result(appkey: str, version: str, answer: str) -> Any:
    if version not in ("full", "simple"):
        return {"error": "invalid_param", "message": "version must be 'full' or 'simple'"}
    if not answer:
        return {"error": "missing_param", "message": "answer is required"}
    return _call_api(ANSWER_URL, appkey, {"version": version, "answer": answer})


def _pick_code(question: dict, choice: Any):
    c = (str(choice) if choice is not None else "").strip().lower()
    if c in ("a", "1", "answer1"):
        return question.get("type1")
    if c in ("b", "2", "answer2"):
        return question.get("type2")
    return None


def cmd_questions(appkey: str, req: dict) -> Any:
    version = _normalize_version(req.get("version"))
    return get_questions(appkey, version)


def cmd_answer(appkey: str, req: dict) -> Any:
    version = _normalize_version(req.get("version"))
    answer = req.get("answer")
    answers = req.get("answers")

    if answer in (None, "") and isinstance(answers, list):
        answer = ",".join([str(x) for x in answers if str(x).strip() != ""])
    if answer in (None, ""):
        return {"error": "missing_param", "message": "answer (string) or answers (array) is required"}

    return get_result(appkey, version, str(answer))


def cmd_next(appkey: str, req: dict) -> Any:
    version = _normalize_version(req.get("version"))
    cursor_raw = req.get("cursor", 0)
    choice = req.get("choice")
    picked = req.get("picked", [])

    try:
        cursor = int(cursor_raw)
    except Exception:
        return {"error": "invalid_param", "message": "cursor must be an integer"}
    if cursor < 0:
        return {"error": "invalid_param", "message": "cursor must be >= 0"}

    if not isinstance(picked, list):
        return {"error": "invalid_param", "message": "picked must be an array"}
    picked_codes = [str(x) for x in picked if str(x).strip() != ""]

    questions = get_questions(appkey, version)
    if isinstance(questions, dict) and questions.get("error"):
        return questions
    if not isinstance(questions, list) or len(questions) == 0:
        return {"error": "api_error", "message": "questions list is empty"}

    total = len(questions)
    if cursor >= total:
        answer_str = ",".join(picked_codes)
        result = get_result(appkey, version, answer_str)
        if isinstance(result, dict) and result.get("error"):
            return result
        return {
            "done": True,
            "version": version,
            "total": total,
            "picked": picked_codes,
            "answer": answer_str,
            "result": result,
        }

    current = questions[cursor]

    if choice not in (None, ""):
        code = _pick_code(current, choice)
        if not code:
            return {"error": "invalid_param", "message": "choice must be 'A' or 'B'"}
        picked_codes.append(code)
        cursor += 1

        if cursor >= total:
            answer_str = ",".join(picked_codes)
            result = get_result(appkey, version, answer_str)
            if isinstance(result, dict) and result.get("error"):
                return result
            return {
                "done": True,
                "version": version,
                "total": total,
                "picked": picked_codes,
                "answer": answer_str,
                "result": result,
            }

        current = questions[cursor]

    return {
        "done": False,
        "version": version,
        "cursor": cursor,
        "total": total,
        "picked": picked_codes,
        "question": {
            "id": current.get("id"),
            "number": current.get("number"),
            "question": current.get("question"),
            "answer1": current.get("answer1"),
            "answer2": current.get("answer2"),
        },
    }


def cmd_quiz(appkey: str, req: dict) -> Any:
    version = _normalize_version(req.get("version"))
    questions = get_questions(appkey, version)
    if isinstance(questions, dict) and questions.get("error"):
        return questions
    if not isinstance(questions, list) or len(questions) == 0:
        return {"error": "api_error", "message": "questions list is empty"}

    picked_codes: list[str] = []
    total = len(questions)

    for idx, q in enumerate(questions, start=1):
        print(f"\n[{idx}/{total}] {q.get('question')}")
        print(f"A. {q.get('answer1')}")
        print(f"B. {q.get('answer2')}")

        while True:
            ans = input("请选择 A 或 B：").strip().lower()
            code = _pick_code(q, ans)
            if code:
                picked_codes.append(code)
                break
            print("输入无效，请输入 A 或 B。")

    answer_str = ",".join(picked_codes)
    result = get_result(appkey, version, answer_str)
    if isinstance(result, dict) and result.get("error"):
        return result
    return {
        "done": True,
        "version": version,
        "total": total,
        "picked": picked_codes,
        "answer": answer_str,
        "result": result,
    }


def _read_json_arg() -> dict:
    if len(sys.argv) < 3 or sys.argv[2].strip() == "":
        return {}
    raw = sys.argv[2]
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        sys.exit(1)
    if not isinstance(data, dict):
        print("Error: JSON body must be an object.", file=sys.stderr)
        sys.exit(1)
    return data


def main():
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  character.py questions '{\"version\":\"full\"}'\n"
            "  character.py next '{\"version\":\"full\"}'\n"
            "  character.py next '{\"version\":\"full\",\"cursor\":0,\"picked\":[],\"choice\":\"A\"}'\n"
            "  character.py answer '{\"version\":\"simple\",\"answer\":\"x1,y2,...\"}'\n"
            "  character.py quiz '{\"version\":\"simple\"}'",
            file=sys.stderr,
        )
        sys.exit(1)

    appkey = os.getenv("JISU_API_KEY")
    if not appkey:
        print("Error: JISU_API_KEY must be set in environment.", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1].strip().lower()
    req = _read_json_arg()

    if cmd == "questions":
        result = cmd_questions(appkey, req)
    elif cmd == "next":
        result = cmd_next(appkey, req)
    elif cmd == "answer":
        result = cmd_answer(appkey, req)
    elif cmd == "quiz":
        result = cmd_quiz(appkey, req)
    else:
        print(f"Error: unknown command '{cmd}'", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

