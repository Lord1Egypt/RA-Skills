#!/usr/bin/env python3
"""
AI Email Agent — 电商客服智能邮件自动回复系统

用法:
    python main.py run              # 持续运行 Agent
    python main.py once             # 单次运行 (测试用)
    python main.py stats            # 查看统计
    python main.py dashboard        # 启动监控看板
    python main.py test-send <邮箱>  # 测试邮件配置
    python main.py demo             # 演示模式 (不连真实 IMAP)
"""
import sys
import os
import json
import http.server
import socketserver

# 确保项目根目录在 path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent.config_loader import get_config, load_config
from agent.ticket_db import TicketDB


def cmd_run():
    """持续运行 Agent"""
    from agent.agent_loop import EmailAgent
    agent = EmailAgent()
    agent.run_loop()


def cmd_once():
    """单次运行"""
    from agent.agent_loop import EmailAgent
    agent = EmailAgent()
    stats = agent.run_once()
    print(json.dumps(stats, indent=2, ensure_ascii=False))


def cmd_stats():
    """查看统计"""
    db = TicketDB()
    stats = db.get_stats()
    print(json.dumps(stats, indent=2, ensure_ascii=False))


def cmd_dashboard():
    """启动监控看板"""
    port = 8080
    dashboard_path = os.path.join(os.path.dirname(__file__), "dashboard.html")

    if not os.path.exists(dashboard_path):
        print(f"[ERROR] 看板文件不存在: {dashboard_path}")
        return

    # 启动 API 端点和静态文件服务
    from agent.ticket_db import TicketDB
    from urllib.parse import urlparse, parse_qs

    db = TicketDB()

    class DashboardHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=os.path.dirname(__file__), **kwargs)

        def do_GET(self):
            parsed = urlparse(self.path)

            if parsed.path == "/api/stats":
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                stats = db.get_stats()
                trend = db.get_trend(7)
                stats["trend"] = trend
                self.wfile.write(json.dumps(stats, ensure_ascii=False).encode())
                return

            if parsed.path == "/api/tickets":
                params = parse_qs(parsed.query)
                status = params.get("status", ["all"])[0]
                limit = int(params.get("limit", [50])[0])

                import sqlite3
                conn = sqlite3.connect(db.db_path)
                conn.row_factory = sqlite3.Row

                if status == "all":
                    rows = conn.execute(
                        "SELECT * FROM tickets ORDER BY created_at DESC LIMIT ?", (limit,)
                    ).fetchall()
                else:
                    rows = conn.execute(
                        "SELECT * FROM tickets WHERE status = ? ORDER BY created_at DESC LIMIT ?",
                        (status, limit)
                    ).fetchall()
                conn.close()

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                tickets = [dict(r) for r in rows]
                self.wfile.write(json.dumps(tickets, ensure_ascii=False, default=str).encode())
                return

            # 默认返回看板 HTML
            if parsed.path == "/" or parsed.path == "/dashboard.html":
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                with open(dashboard_path, "r", encoding="utf-8") as f:
                    self.wfile.write(f.read().encode())
                return

            super().do_GET()

        def log_message(self, format, *args):
            pass  # 静默日志

    print(f"\n  📊 监控看板已启动: http://localhost:{port}")
    print(f"  📡 API 端点: http://localhost:{port}/api/stats")
    print(f"  📡 工单列表: http://localhost:{port}/api/tickets")
    print(f"  ⏹️  按 Ctrl+C 停止\n")

    with socketserver.TCPServer(("", port), DashboardHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[INFO] 看板已停止")


def cmd_test_send(email_addr: str):
    """测试邮件发送"""
    from agent.sender import EmailSender
    sender = EmailSender()
    result = sender.send_test(email_addr)
    if result["success"]:
        print(f"✅ 测试邮件发送成功 → {email_addr}")
    else:
        print(f"❌ 发送失败: {result['message']}")


def cmd_demo():
    """演示模式：模拟处理样本邮件，不连真实 IMAP"""
    print("\n" + "=" * 60)
    print("  🎬 AI Email Agent — 演示模式")
    print("  将模拟处理 5 封典型客户邮件")
    print("=" * 60 + "\n")

    from agent.config_loader import get_config
    from agent.preprocessor import Preprocessor
    from agent.classifier import EmailClassifier
    from agent.urgency import UrgencyScorer
    from agent.template_engine import TemplateEngine
    from agent.escalation import EscalationEngine
    from agent.ticket_db import TicketDB
    from agent.knowledge_base import KnowledgeBase
    from agent.email_fetcher import EmailMessage
    from agent.sender import EmailSender

    # 样本邮件
    sample_emails = [
        EmailMessage(
            uid="demo-001", message_id="msg-001@example.com",
            from_addr="sarah@example.com", from_name="Sarah Johnson",
            to_addr="support@shop.com",
            subject="Question about Widget X300 Pro size",
            body_plain="Hi, I'm interested in buying the Widget X300 Pro but I'm not sure about the size. "
                       "Can you tell me the dimensions and weight? Also, do you ship to Canada? Thanks!",
            body_html="", date="2026-06-21T10:00:00", auto_submitted=False,
        ),
        EmailMessage(
            uid="demo-002", message_id="msg-002@example.com",
            from_addr="angry_customer@hotmail.com", from_name="Mike Brown",
            to_addr="support@shop.com",
            subject="BROKEN PRODUCT — I want a refund NOW",
            body_plain="I received my order ORD-20240615-8821 today and the screen is cracked! "
                       "This is completely unacceptable. I paid $49.99 for this and it's damaged. "
                       "I demand an immediate refund. If you don't fix this, I'll post about it on Twitter "
                       "and leave a 1-star review everywhere!",
            body_html="", date="2026-06-21T10:30:00", auto_submitted=False,
        ),
        EmailMessage(
            uid="demo-003", message_id="msg-003@example.com",
            from_addr="tanaka@jp-email.jp", from_name="田中 太郎",
            to_addr="support@shop.com",
            subject="返品について — 注文番号 ORD-20240620-9991",
            body_plain="先日注文した商品(ORD-20240620-9991)が届きましたが、サイズが合いませんでした。"
                       "返品して交換したいのですが、手続きを教えてください。",
            body_html="", date="2026-06-21T11:00:00", auto_submitted=False,
        ),
        EmailMessage(
            uid="demo-004", message_id="msg-004@example.com",
            from_addr="marketing@spam-offers.com", from_name="Cheap Deals",
            to_addr="support@shop.com",
            subject="MAKE MONEY FAST!!! Buy our SEO tool now!!!",
            body_plain="Hurry up! Limited time offer! Buy our SEO tool and make $10,000 per month! "
                       "Click here: http://spam-link.com/buy-now!!!",
            body_html="", date="2026-06-21T11:15:00", auto_submitted=False,
        ),
        EmailMessage(
            uid="demo-005", message_id="msg-005@example.com",
            from_addr="partner@big-retailer.com", from_name="Emily Chen",
            to_addr="support@shop.com",
            subject="Wholesale partnership inquiry — Bulk order",
            body_plain="Hello, I'm the purchasing manager at Big Retailer Inc. "
                       "We're interested in carrying your Widget X300 Pro in our 200+ stores nationwide. "
                       "Could we discuss wholesale pricing and terms? Looking forward to hearing from you.",
            body_html="", date="2026-06-21T12:00:00", auto_submitted=False,
        ),
    ]

    config = get_config()
    preprocessor = Preprocessor(config)
    classifier = EmailClassifier(config)
    ticket_db = TicketDB(config)
    urgency_scorer = UrgencyScorer(ticket_db=ticket_db)
    template_engine = TemplateEngine(config)
    escalation = EscalationEngine(config, ticket_db=ticket_db)
    knowledge_base = KnowledgeBase(config)
    sender = EmailSender(config)

    valid, filtered = preprocessor.process(sample_emails)

    for i, email in enumerate(valid, 1):
        print(f"📧 演示邮件 {i}/{len(valid)}: {email.subject[:50]}...")
        print(f"   发件人: {email.from_name} <{email.from_addr}>")

        # 分类
        result = classifier.classify(email)
        print(f"   分类: {result.category} | 情感: {result.sentiment} | 语言: {result.language}")
        print(f"   置信度: {result.confidence:.2f} | 摘要: {result.summary[:60]}")

        # 紧急度
        urgency = urgency_scorer.calculate(email, result)
        print(f"   紧急度: {urgency.level}/5 ({urgency.level_label}) — {urgency.score}分")
        print(f"   因素: {', '.join(urgency.factors) if urgency.factors else '无'}")

        # 升级检查
        ticket_id = ticket_db.create_ticket(email, result, urgency)
        esc = escalation.evaluate(email, result, urgency, ticket_id)
        if esc["should_escalate"]:
            print(f"   ⚠️ 升级: {esc['level']} — {esc['reason']}")
            ticket_db.escalate(ticket_id, esc["level"], esc["reason"])
        else:
            print(f"   ✅ 自动处理")

        # 知识库
        kb = knowledge_base.search(f"{email.subject} {email.body_plain[:200]}", language=result.language)
        if kb:
            print(f"   📚 知识库命中")

        # 模板渲染
        rma = f"RMA-{ticket_id}" if result.category == "return_refund" else ""
        reply = template_engine.render(email, result, urgency, ticket_id, rma_number=rma, kb_snippet=kb)
        print(f"   回复语言: {reply['language']} | 模式: {reply['mode']}")
        print(f"   回复主题: {reply['subject'][:60]}...")

        # 如果是演示，不实际发送，只打印预览
        print(f"\n   ┌─ 回复预览: {'─' * 40}")
        for line in reply["body"].split("\n")[:8]:
            print(f"   │ {line}")
        print(f"   └{'─' * 50}\n")

    # 汇总
    stats = ticket_db.get_stats()
    print("=" * 60)
    print("  📊 演示汇总")
    print(f"  总计: {stats['overview']['total']}")
    print(f"  自动回复: {stats['overview']['auto_replied']}")
    print(f"  升级: {stats['overview']['escalated']}")
    print(f"  归档: {stats['overview']['archived']}")
    print(f"  分类分布: {stats['category_dist']}")
    print(f"  情感分布: {stats['sentiment_dist']}")
    print("=" * 60)

    print("\n💡 提示:")
    print("  1. 配置 .env 文件中的 LLM_API_KEY 后，可真实调用 LLM 分类")
    print("  2. 配置 IMAP/SMTP 后，运行 'python main.py run' 启动真实 Agent")
    print("  3. 运行 'python main.py dashboard' 查看监控看板")


def print_usage():
    print("""
AI Email Agent — 电商客服智能邮件自动回复系统

用法:
    python main.py run              持续运行 Agent 循环
    python main.py once             单次拉取处理 (测试用)
    python main.py stats            查看工单统计
    python main.py dashboard        启动 Web 监控看板
    python main.py test-send <邮箱>  测试 SMTP 配置
    python main.py demo             演示模式 (模拟样本邮件)
""")


def main():
    if len(sys.argv) < 2:
        print_usage()
        return

    cmd = sys.argv[1]

    if cmd == "run":
        cmd_run()
    elif cmd == "once":
        cmd_once()
    elif cmd == "stats":
        cmd_stats()
    elif cmd == "dashboard":
        cmd_dashboard()
    elif cmd == "test-send":
        if len(sys.argv) < 3:
            print("用法: python main.py test-send <your@email.com>")
            return
        cmd_test_send(sys.argv[2])
    elif cmd == "demo":
        cmd_demo()
    elif cmd in ("-h", "--help", "help"):
        print_usage()
    else:
        print(f"未知命令: {cmd}")
        print_usage()


if __name__ == "__main__":
    main()
