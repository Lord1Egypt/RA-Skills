"""
主 Agent 循环 — 邮件处理编排器
"""
import time
import signal
import sys
from datetime import datetime
from typing import Optional

from .config_loader import get_config, reload_config
from .email_fetcher import EmailFetcher, EmailMessage
from .preprocessor import Preprocessor
from .classifier import EmailClassifier, ClassificationResult
from .urgency import UrgencyScorer, UrgencyResult
from .template_engine import TemplateEngine
from .sender import EmailSender
from .escalation import EscalationEngine
from .ticket_db import TicketDB
from .knowledge_base import KnowledgeBase


class EmailAgent:
    """
    AI 邮件自动回复 Agent — 主编排器

    处理流程:
        IMAP 拉取 → 预处理 → LLM 分类 → 紧急度评分 → 决策路由 → 回复/升级
    """

    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.config = get_config(config_path)

        # 初始化各模块
        self.fetcher = EmailFetcher(self.config)
        self.preprocessor = Preprocessor(self.config)
        self.classifier = EmailClassifier(self.config)
        self.ticket_db = TicketDB(self.config)
        self.urgency_scorer = UrgencyScorer(ticket_db=self.ticket_db)
        self.template_engine = TemplateEngine(self.config)
        self.sender = EmailSender(self.config)
        self.escalation = EscalationEngine(self.config, ticket_db=self.ticket_db)
        self.knowledge_base = KnowledgeBase(self.config)

        self.running = False
        self.stats = {
            "total_fetched": 0,
            "auto_replied": 0,
            "escalated": 0,
            "archived": 0,
            "errors": 0,
            "started_at": datetime.now().isoformat(),
        }

    def run_once(self) -> dict:
        """执行一轮邮件处理，返回本轮统计"""
        round_stats = {"fetched": 0, "auto_replied": 0, "escalated": 0, "archived": 0, "errors": 0}

        # ===== 阶段 0: 拉取邮件 =====
        try:
            emails = self.fetcher.fetch_unread(limit=50)
        except Exception as e:
            print(f"[ERROR] 邮件拉取失败: {e}")
            round_stats["errors"] += 1
            return round_stats

        if not emails:
            return round_stats

        round_stats["fetched"] = len(emails)
        print(f"[INFO] 拉取到 {len(emails)} 封未读邮件")

        # ===== 阶段 1: 预处理 =====
        valid_emails, filtered = self.preprocessor.process(emails)

        for reason, filtered_list in filtered.items():
            for em in filtered_list:
                # 垃圾邮件 → 学习特征
                if reason in ("blacklist_domain", "blacklist_keyword", "spam"):
                    self.ticket_db.add_spam_feature(
                        domain=self.preprocessor.extract_domain(em.from_addr)
                    )
                # 归档
                ticket_id = self.ticket_db.create_ticket(em, ClassificationResult(
                    category="spam", confidence=0.99, sentiment="neutral",
                    sentiment_score=0, urgency_raw=1, language="en",
                    language_confidence=0.5
                ), UrgencyResult(score=0, level=1, level_label="低", factors=[], sla_minutes=0))
                self.ticket_db.archive(ticket_id, reason)
                self.fetcher.mark_read(em.uid)
                round_stats["archived"] += 1

        print(f"[INFO] 有效邮件: {len(valid_emails)} | 过滤: {len(emails) - len(valid_emails)}")

        # ===== 阶段 2-5: 逐封处理 =====
        for email in valid_emails:
            try:
                result = self._process_email(email)
                if result == "auto_replied":
                    round_stats["auto_replied"] += 1
                elif result == "escalated":
                    round_stats["escalated"] += 1
                elif result == "archived":
                    round_stats["archived"] += 1
            except Exception as e:
                print(f"[ERROR] 处理邮件失败 {email.uid}: {e}")
                round_stats["errors"] += 1
                # 失败时标记为已读避免死循环
                try:
                    self.fetcher.mark_read(email.uid)
                except Exception:
                    pass

        # 更新全局统计
        for key in round_stats:
            self.stats[key] += round_stats[key]
        self.stats["total_fetched"] += round_stats["fetched"]

        return round_stats

    def _process_email(self, email: EmailMessage) -> str:
        """
        处理单封邮件，返回处理结果标签
        """
        print(f"\n{'='*60}")
        print(f"[处理] {email.from_addr} | {email.subject[:60]}")

        # ===== 阶段 2: LLM 分类 =====
        classification = self.classifier.classify(email)
        print(f"  ├─ 分类: {classification.category} (置信度: {classification.confidence:.2f})")
        print(f"  ├─ 情感: {classification.sentiment} ({classification.sentiment_score:+.2f})")
        print(f"  ├─ 语言: {classification.language}")
        print(f"  ├─ 实体: {classification.entities}")

        # ===== 阶段 3: 紧急度评分 =====
        urgency = self.urgency_scorer.calculate(email, classification)
        print(f"  ├─ 紧急度: {urgency.level}/5 ({urgency.level_label}) — {urgency.score}分")
        if urgency.factors:
            print(f"  ├─ 触发因素: {', '.join(urgency.factors)}")

        # 创建工单
        ticket_id = self.ticket_db.create_ticket(email, classification, urgency)

        # ===== 阶段 4: 升级检查 =====
        esc_result = self.escalation.evaluate(email, classification, urgency, ticket_id)

        if esc_result["should_escalate"]:
            print(f"  ├─ ⚠️ 升级: {esc_result['level']} — {esc_result['reason']}")

            # 发送升级通知
            self.escalation.notify(
                email, classification, urgency,
                ticket_id, esc_result["level"], esc_result["reason"]
            )

            # 更新工单状态
            self.ticket_db.escalate(ticket_id, esc_result["level"], esc_result["reason"])

            # 即使是升级，如果是合作类/投诉类也先发自动回复
            if classification.category == "cooperation":
                reply = self.template_engine.render(
                    email, classification, urgency, ticket_id,
                    kb_snippet="",
                )
                self._send_reply(email, reply, ticket_id)
                print(f"  └─ ✅ 自动回复 (合作转接) + 升级")

            elif classification.category == "complaint" and urgency.level <= 2:
                reply = self.template_engine.render(
                    email, classification, urgency, ticket_id,
                    kb_snippet="",
                )
                self._send_reply(email, reply, ticket_id)
                print(f"  └─ ✅ 安抚回复 + 升级")

            self.fetcher.mark_read(email.uid)
            return "escalated"

        # ===== 阶段 5: 决策路由 =====
        category = classification.category

        if category == "spam":
            # 垃圾邮件 → 静默归档
            self.ticket_db.archive(ticket_id, "SPAM")
            self.ticket_db.add_spam_feature(
                domain=self.preprocessor.extract_domain(email.from_addr)
            )
            self.fetcher.mark_read(email.uid)
            print(f"  └─ 🗑️ 垃圾邮件归档")
            return "archived"

        elif category == "cooperation":
            # 合作类 → 升级 (已在上面处理，这里兜底)
            self.ticket_db.escalate(ticket_id, "P2", "商务合作类邮件")
            reply = self.template_engine.render(email, classification, urgency, ticket_id)
            self._send_reply(email, reply, ticket_id)
            self.fetcher.mark_read(email.uid)
            print(f"  └─ 📩 合作转接")
            return "escalated"

        elif classification.confidence < 0.7:
            # 低置信度 → 升级人工
            self.ticket_db.escalate(ticket_id, "P2", f"分类置信度过低 ({classification.confidence:.2f})")
            self.fetcher.mark_read(email.uid)
            print(f"  └─ ⚠️ 低置信度升级")
            return "escalated"

        elif category in ("consultation", "complaint", "return_refund"):
            # RAG 检索知识库
            kb_snippet = self.knowledge_base.search(
                f"{email.subject} {email.body_plain[:200]}",
                language=classification.language,
                top_k=2,
            )

            # 生成 RMA 编号
            rma_number = ""
            if category == "return_refund" and classification.entities.get("order_id"):
                rma_number = f"RMA-{ticket_id}"

            # 渲染回复
            reply = self.template_engine.render(
                email, classification, urgency, ticket_id,
                rma_number=rma_number,
                kb_snippet=kb_snippet,
            )

            # 发送回复
            send_result = self._send_reply(email, reply, ticket_id)

            if send_result["success"]:
                self.fetcher.mark_read(email.uid)
                mode = reply.get("mode", "native")
                print(f"  └─ ✅ 自动回复 ({mode})")
                return "auto_replied"
            else:
                print(f"  └─ ❌ 发送失败: {send_result['message']}")
                return "auto_replied"  # 仍标记为已处理

        else:
            # 兜底：未知分类 → 升级
            self.ticket_db.escalate(ticket_id, "P2", f"未知分类: {category}")
            self.fetcher.mark_read(email.uid)
            print(f"  └─ ⚠️ 未知分类升级")
            return "escalated"

    def _send_reply(self, email: EmailMessage, reply: dict, ticket_id: str) -> dict:
        """发送回复邮件并更新工单"""
        result = self.sender.send(
            to_email=email.from_addr,
            subject=reply["subject"],
            body=reply["body"],
            in_reply_to=email.message_id,
            references=email.message_id,
        )

        if result["success"]:
            self.ticket_db.update_reply(ticket_id, reply["subject"], reply["body"])

        return result

    def run_loop(self):
        """持续运行 Agent 循环"""
        self.running = True
        poll_interval = self.config.get("imap", {}).get("poll_interval_seconds", 120)

        print(f"\n{'='*60}")
        print(f"  🤖 AI Email Agent 已启动")
        print(f"  📧 监控邮箱: {self.config['imap']['username']}")
        print(f"  ⏱️  轮询间隔: {poll_interval}s")
        print(f"  🕐 启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")

        # 优雅退出
        def handle_exit(sig, frame):
            print("\n[INFO] 收到退出信号，正在关闭...")
            self.running = False

        signal.signal(signal.SIGINT, handle_exit)
        signal.signal(signal.SIGTERM, handle_exit)

        while self.running:
            try:
                round_stats = self.run_once()
                if round_stats["fetched"] > 0:
                    print(f"\n[本轮统计] 获取: {round_stats['fetched']} | "
                          f"自动回复: {round_stats['auto_replied']} | "
                          f"升级: {round_stats['escalated']} | "
                          f"归档: {round_stats['archived']} | "
                          f"错误: {round_stats['errors']}")
                    print(f"[累计统计] 总数: {self.stats['total_fetched']} | "
                          f"自动回复: {self.stats['auto_replied']} | "
                          f"升级: {self.stats['escalated']}")

                # 等待下一轮
                if self.running:
                    time.sleep(poll_interval)

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"[ERROR] Agent 循环异常: {e}")
                if self.running:
                    time.sleep(30)  # 异常后等待 30s 再重试

        # 清理
        try:
            self.fetcher.disconnect()
        except Exception:
            pass
        print("[INFO] Agent 已停止")

    def get_stats(self) -> dict:
        """获取运行统计 + 数据库统计"""
        db_stats = self.ticket_db.get_stats()
        return {
            "agent": self.stats,
            "database": db_stats,
            "uptime": str(datetime.now() - datetime.fromisoformat(self.stats["started_at"])),
        }
