# 详细参考 - block-monitor-tool-pro

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (python)

```python
#!/usr/bin/env python3
"""专业版语义级内容分析引擎"""

import json
import re
from datetime import datetime
from collections import defaultdict

class SemanticContentAnalyzer:
    """语义级内容分析器"""

    RISK_CATEGORIES = {
        "harmful_content": {
            "label": "有害内容",
            "indicators": [
                "暴力", "伤害", "攻击", "危险行为",
                "歧视", "仇恨言论", "骚扰"
            ],
            "severity": "HIGH"
        },
        "misinformation": {
            "label": "虚假信息",
            "indicators": [
                "绝对有效", " guaranteed", "包治百病",
                "内幕消息", "稳赚不赔"
            ],
            "severity": "HIGH"
        },
        "privacy_violation": {
            "label": "隐私违规",
            "patterns": [
                (r'\b\d{17}[\dXx]\b', "身份证号"),
                (r'\b\d{16}\b', "信用卡号"),
                (r'\b\d{3}-\d{2}-\d{4}\b', "SSN"),
                (r'phone[:\s]*\d{11}', "手机号"),
            ],
            "severity": "CRITICAL"
        },
        "inappropriate_content": {
            "label": "不当内容",
            "indicators": [
                "色情", "赌博", "毒品", "非法"
            ],
            "severity": "CRITICAL"
        },
        "professional_concerns": {
            "label": "职业伦理",
            "indicators": [
                "内幕交易", "利益冲突", "保密协议违反"
            ],
            "severity": "HIGH"
        }
    }

    def __init__(self):
        self.custom_rules = []
        self.audit_log = []

    def analyze(self, content, context=None):
        """语义分析内容"""
        analysis = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "content_length": len(content),
            "language": self._detect_language(content),
            "risk_score": 0,
            "categories": [],
            "recommendation": "ALLOW"
        }

        content_lower = content.lower()

        for category_id, config in self.RISK_CATEGORIES.items():
            findings = []

            for indicator in config.get("indicators", []):
                if indicator.lower() in content_lower:
                    findings.append({
                        "type": "indicator",
                        "match": indicator,
                        "position": content_lower.index(indicator.lower())
                    })

            for pattern, desc in config.get("patterns", []):
                matches = re.finditer(pattern, content)
                for match in matches:
                    findings.append({
                        "type": "pattern",
                        "description": desc,
                        "match": match.group()[:50],
                        "position": match.start()
                    })

            if findings:
                severity = config["severity"]
                score = {"CRITICAL": 40, "HIGH": 20, "MEDIUM": 10, "LOW": 5}[severity]
                analysis["risk_score"] += score * len(findings)

                analysis["categories"].append({
                    "category": category_id,
                    "label": config["label"],
                    "severity": severity,
                    "findings": findings,
                    "finding_count": len(findings)
                })

        if context:
            analysis["context"] = context
        if analysis["risk_score"] >= 80:
            analysis["recommendation"] = "BLOCK"
        elif analysis["risk_score"] >= 40:
            analysis["recommendation"] = "REVIEW"
        else:
            analysis["recommendation"] = "ALLOW"

        self.audit_log.append({
            "timestamp": analysis["timestamp"],
            "content_hash": hash(content),
            "risk_score": analysis["risk_score"],
            "recommendation": analysis["recommendation"],
            "categories": [c["category"] for c in analysis["categories"]]
        })

        return analysis

    def _detect_language(self, content):
        """简单语言检测"""
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', content))
        ascii_chars = len(re.findall(r'[a-zA-Z]', content))

        if chinese_chars > ascii_chars:
            return "zh"
        elif ascii_chars > chinese_chars:
            return "en"
        return "mixed"

    def get_audit_trail(self, limit=100):
        """获取审计轨迹"""
        return self.audit_log[-limit:]

if __name__ == "__main__":
    analyzer = SemanticContentAnalyzer()

    test_content = "这个产品的效果绝对有效,包治百病。用户身份证号: 110101199001011234"
    result = analyzer.analyze(test_content)
    print(json.dumps(result, indent=2, ensure_ascii=False))
```

## 代码示例 (python)

```python
#!/usr/bin/env python3
"""专业版实时内容拦截网关"""

import json
import time
from datetime import datetime

class ContentGateway:
    """实时内容拦截网关"""

    def __init__(self, analyzer, alert_config=None):
        self.analyzer = analyzer
        self.alert_config = alert_config or {
            "webhook_url": None,
            "email": None,
            "min_severity": "HIGH"
        }
        self.stats = {
            "total": 0,
            "allowed": 0,
            "blocked": 0,
            "reviewed": 0
        }

    def process(self, content, context=None):
        """处理内容(实时拦截)"""
        self.stats["total"] += 1

        analysis = self.analyzer.analyze(content, context)

        if analysis["recommendation"] == "BLOCK":
            self.stats["blocked"] += 1
            self._send_alert(analysis, "BLOCKED")
            return {
                "action": "BLOCKED",
                "content": None,
                "reason": "内容违反安全策略",
                "analysis": analysis
            }
        elif analysis["recommendation"] == "REVIEW":
            self.stats["reviewed"] += 1
            return {
                "action": "PENDING_REVIEW",
                "content": content,
                "reason": "内容需要人工审核",
                "analysis": analysis
            }
        else:
            self.stats["allowed"] += 1
            return {
                "action": "ALLOWED",
                "content": content,
                "reason": "内容通过验证",
                "analysis": analysis
            }

    def _send_alert(self, analysis, action):
        """发送告警"""
        alert = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "action": action,
            "risk_score": analysis["risk_score"],
            "categories": [c["label"] for c in analysis["categories"]],
            "severity": max(
                (c["severity"] for c in analysis["categories"]),
                default="LOW"
            )
        }

        print(f"[ALERT] {action}: 风险评分 {alert['risk_score']}")
    def get_stats(self):
        """获取统计信息"""
        return self.stats

if __name__ == "__main__":
    from semantic_analyzer import SemanticContentAnalyzer

    analyzer = SemanticContentAnalyzer()
    gateway = ContentGateway(analyzer)

    contents = [
        "这是一段正常的内容",
        "包治百病的神药,绝对有效!",
        "用户信息: 身份证110101199001011234"
    ]

    for content in contents:
        result = gateway.process(content)
        print(f"\n内容: {content[:30]}...")
        print(f"动作: {result['action']}")
        print(f"原因: {result['reason']}")

    print(f"\n统计: {gateway.get_stats()}")
```

## 代码示例 (python)

```python
#!/usr/bin/env python3
"""专业版内容验证REST API"""

from flask import Flask, request, jsonify
from semantic_analyzer import SemanticContentAnalyzer
from content_gateway import ContentGateway

app = Flask(__name__)
analyzer = SemanticContentAnalyzer()
gateway = ContentGateway(analyzer)

@app.route('/api/v1/verify', methods=['POST'])
def verify_content():
    """验证单个内容"""
    data = request.json
    content = data.get("content", "")
    context = data.get("context")

    result = gateway.process(content, context)
    return jsonify(result)

@app.route('/api/v1/verify/batch', methods=['POST'])
def verify_batch():
    """批量验证"""
    data = request.json
    items = data.get("items", [])

    results = []
    for item in items:
        result = gateway.process(
            item.get("content", ""),
            item.get("context")
        )
        results.append({
            "id": item.get("id"),
            "action": result["action"],
            "risk_score": result["analysis"]["risk_score"]
        })

    return jsonify({"results": results, "count": len(results)})

@app.route('/api/v1/stats', methods=['GET'])
def get_stats():
    """获取统计"""
    return jsonify(gateway.get_stats())

@app.route('/api/v1/audit', methods=['GET'])
def get_audit():
    """获取审计日志"""
    limit = request.args.get("limit", 100, type=int)
    return jsonify(analyzer.get_audit_trail(limit))

if __name__ == '__main__':
    print("内容验证API服务启动: http://localhost:5000")
    print("  POST /api/v1/verify       - 验证单个内容")
    print("  POST /api/v1/verify/batch - 批量验证")
    print("  GET  /api/v1/stats        - 获取统计")
    print("  GET  /api/v1/audit        - 审计日志")
    app.run(host='0.0.0.0', port=5000, debug=False)
```

