#!/usr/bin/env python3
"""补充知识库答案 CLI 入口"""

COMMAND_NAME = "knowledge_answer"
COMMAND_DESC = "补充知识库答案"

import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _output import print_output, print_error
from _risk_guard import emit_confirmation, get_confirmed_payload
from capabilities.knowledge_answer.service import submit_answer


def _truncate(text: str, limit: int = 60) -> str:
    text = text or ""
    return text if len(text) <= limit else text[:limit] + "…"


def main():
    parser = argparse.ArgumentParser(description="补充知识库答案")
    parser.add_argument("--question", "-q", required=True, help="问题内容")
    parser.add_argument("--answer", "-a", required=True, help="答案内容")
    parser.add_argument("--question-id", default=None,
                        help="问题 ID（可选；不传则本地生成 uuid）")
    args = parser.parse_args()

    try:
        # 写入知识库属于商家可感知的业务动作，必须走 BashRiskCheckHook 二次确认，
        # 防止 AI 编造答案不经商家认可直接写入知识库。
        payload = get_confirmed_payload()
        if payload is None:
            msg = "即将向知识库写入答案：Q「{}」→ A「{}」，是否确认？".format(
                _truncate(args.question), _truncate(args.answer))
            emit_confirmation(
                message=msg,
                payload={
                    "question": args.question,
                    "answer": args.answer,
                    "question_id": args.question_id,
                },
                preview_markdown="待商家确认：写入知识库答案",
            )
            return

        # Phase 2：只以 payload 为权威值，不信任命令行参数
        question = (payload.get("question") or "").strip()
        answer = (payload.get("answer") or "").strip()
        question_id = payload.get("question_id")
        if not question or not answer:
            print_output(False, "二次确认 payload 缺少 question / answer，拒绝写入", {})
            return

        result = submit_answer(
            question=question,
            answer=answer,
            question_id=question_id,
        )
        print_output(True, result["markdown"], result["data"])
    except KeyboardInterrupt:
        print_output(False, "用户中断操作", {})
    except Exception as e:
        print_error(e, {})


if __name__ == "__main__":
    main()
