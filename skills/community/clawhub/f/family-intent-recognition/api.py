#!/usr/bin/env python3
"""
家庭消费意图识别 API 服务
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from intent_classifier import classify

app = Flask(__name__)
CORS(app)  # 启用跨域支持


@app.route('/intent', methods=['POST'])
def recognize_intent():
    """意图识别接口"""
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({"error": "缺少 text 字段"}), 400
    
    text = data['text']
    result = classify(text)
    
    return jsonify(result)


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})


if __name__ == '__main__':
    print("🚀 家庭消费意图识别 API 启动中...")
    print("📍 http://localhost:5000/intent")
    app.run(host='0.0.0.0', port=5000, debug=False)
