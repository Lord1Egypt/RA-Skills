#!/usr/bin/env python3
"""
DeepSeek Bridge —轻量级 HTTP 桥接程序
用法: python deepseek_bridge.py
启动后监听 http://127.0.0.1:8080/ask
"""
from flask import Flask, request, jsonify
import requests
import os
import sys

# Add openclaw-data to path for db_shared
sys.path.insert(0, r"D:\openclaw-data")
from db_shared import save_question, update_answer

app = Flask(__name__)

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY") or ""
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"


@app.route('/health', methods=['GET'])
def health():
    if DEEPSEEK_API_KEY:
        return jsonify({"status": "ok", "model": "deepseek-chat"})
    return jsonify({"status": "error", "message": "DEEPSEEK_API_KEY not set"}), 500


@app.route('/ask', methods=['POST'])
def ask_deepseek():
    if not DEEPSEEK_API_KEY:
        return jsonify({"error": "DEEPSEEK_API_KEY not configured"}), 500

    data = request.json or {}
    question = data.get('question', '')

    if not question:
        return jsonify({"error": "question is required"}), 400

    # Save question to shared DB first
    record_id = save_question(question)

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": question}],
        "stream": False,
    }

    try:
        response = requests.post(DEEPSEEK_URL, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        answer = response.json()["choices"][0]["message"]["content"]
        # Update answer in shared DB
        update_answer(record_id, answer, "completed")
        return jsonify({"answer": answer})
    except requests.exceptions.Timeout:
        update_answer(record_id, "DeepSeek API timeout", "error")
        return jsonify({"error": "DeepSeek API timeout"}), 504
    except requests.exceptions.HTTPError as e:
        update_answer(record_id, f"HTTP {e.response.status_code}: {e.response.text}", "error")
        return jsonify({"error": f"DeepSeek API error: {e.response.status_code} {e.response.text}"}), 502
    except Exception as e:
        update_answer(record_id, str(e), "error")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)