#!/usr/bin/env python
"""
Simple Flask server for FAQ-based auto customer support.
- /webhook: receive {message, sender} and return {reply, confidence, escalate}
- /escalate: mark conversation for human follow-up (stub)
"""
from flask import Flask, request, jsonify
import csv
import os
import argparse
from difflib import SequenceMatcher

app = Flask(__name__)
FAQ = []


def load_faq(path):
    faqs = []
    with open(path, newline='', encoding='utf-8') as f:
        r = csv.DictReader(f)
        for row in r:
            # question_variants stored as | separated text
            variants = [v.strip() for v in row.get('question_variants','').split('|') if v.strip()]
            faqs.append({'intent': row.get('intent',''), 'variants': variants, 'answer': row.get('answer','')})
    return faqs


def best_match(message):
    best = None
    best_score = 0.0
    for item in FAQ:
        for v in item['variants']:
            score = SequenceMatcher(None, message.lower(), v.lower()).ratio()
            if score > best_score:
                best_score = score
                best = item
    return best, best_score


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json() or {}
    message = data.get('message','')
    sender = data.get('sender')
    if not message:
        return jsonify({'error':'missing message'}), 400
    item, score = best_match(message)
    threshold = float(os.environ.get('CONFIDENCE_THRESHOLD', '0.6'))
    if item and score >= threshold:
        reply = item['answer']
        return jsonify({'reply': reply, 'confidence': score, 'escalate': False})
    else:
        # low confidence -> escalate
        return jsonify({'reply':'抱歉，我不确定如何回答。我们会尽快将您的问题转人工处理。', 'confidence': score, 'escalate': True})


@app.route('/escalate', methods=['POST'])
def escalate():
    data = request.get_json() or {}
    # stub: in real integration, create ticket in Zendesk/Feishu/etc.
    return jsonify({'status':'escalated','data':data})


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--faq', default='skills/auto-customer-support/data/faq.csv')
    p.add_argument('--port', type=int, default=5005)
    args = p.parse_args()
    FAQ = load_faq(args.faq)
    app.run(host='0.0.0.0', port=args.port, debug=True)
