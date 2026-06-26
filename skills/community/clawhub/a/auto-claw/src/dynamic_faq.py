"""
Dynamic FAQ + Real-time Help Injection — WordPress 动态FAQ与实时帮助系统
支持智能FAQ生成 + 上下文感知帮助注入
"""
import re
import json
import time
import hashlib
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from collections import defaultdict

@dataclass
class FAQItem:
    """FAQ条目"""
    faq_id: str
    question: str
    answer: str
    category: str = ""  # pricing / features / technical / billing
    keywords: List[str] = field(default_factory=list)
    
    # 上下文
    page_url: str = ""  # 关联页面，空=全局
    trigger_conditions: Dict = field(default_factory=dict)  # scroll_depth, time_on_page...
    
    # 统计
    view_count: int = 0
    helpful_count: int = 0
    not_helpful_count: int = 0
    
    @property
    def helpful_pct(self) -> float:
        total = self.helpful_count + self.not_helpful_count
        return self.helpful_count / total if total > 0 else 0.0

@dataclass
class HelpBlock:
    """帮助块配置"""
    block_id: str
    name: str = ""
    
    # 位置
    position: str = "bottom_right"  # bottom_right / floating / inline / sidebar
    
    # 内容
    help_type: str = ""  # quick_tip / chat_trigger / tooltip / walkthrough
    title: str = ""
    content: str = ""
    
    # 触发
    trigger_page: str = ""  # CSS selector or page type
    trigger_event: str = ""  # scroll / click / idle / exit_intent
    trigger_delay: int = 0  # seconds
    
    # 显示
    show_once_per_session: bool = True
    max_shows: int = 3
    dismissible: bool = True
    
    # 统计
    shown_count: int = 0
    clicked_count: int = 0

class DynamicFAQSystem:
    """
    WordPress 动态FAQ与实时帮助引擎
    
    功能：
    1. FAQ条目管理与分类
    2. 基于页面上下文的智能推荐
    3. 实时帮助块注入
    4. "这有帮助吗？"反馈收集
    5. 生成FAQ页面/AMP页面/Structured Data
    6. 聊天触发器集成
    """
    
    def __init__(self):
        self.faqs: Dict[str, FAQItem] = {}
        self.help_blocks: Dict[str, HelpBlock] = {}
        self._setup_default_faqs()
    
    def _setup_default_faqs(self):
        """默认FAQ"""
        defaults = [
            ("pricing", "这个方案包含什么功能？",
             "所有方案都包含：AI内容生成、SEO优化、用户旅程追踪、A/B测试、24/7监控。具体功能差异见对比表。"),
            ("pricing", "有免费试用吗？",
             "是的，提供14天免费试用，无需信用卡。试用期满可随时取消。"),
            ("features", "支持哪些语言？",
             "支持28种语言，包括中文、英语、日语、韩语、法语、德语等。AI生成内容会根据目标市场自动优化语言。"),
            ("technical", "需要技术背景吗？",
             "不需要。Auto-Claw设计为零代码使用，同时提供API供技术团队深度定制。"),
            ("billing", "如何升级或降级方案？",
             "随时在账户设置中更改方案。升级立即生效，按剩余天数比例计费；降级次月生效。"),
        ]
        
        for cat, q, a in defaults:
            self.add_faq(q, a, category=cat)
    
    def add_faq(self, question: str, answer: str, category: str = "",
               page_url: str = "", **kwargs) -> FAQItem:
        faq_id = hashlib.md5(f"{question}{time.time()}".encode()).hexdigest()[:8]
        keywords = self._extract_keywords(question + " " + answer)
        
        faq = FAQItem(
            faq_id=faq_id,
            question=question,
            answer=answer,
            category=category,
            keywords=keywords,
            page_url=page_url,
            **kwargs
        )
        self.faqs[faq_id] = faq
        return faq
    
    def _extract_keywords(self, text: str) -> List[str]:
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        stopwords = {"this", "that", "with", "from", "have", "will", "been", "what", "when", "where", "which", "their", "there"}
        return list(set(w for w in words if w not in stopwords))[:10]
    
    def get_faqs_for_page(self, page_url: str = "", page_type: str = "",
                         query: str = "") -> List[FAQItem]:
        """获取页面相关的FAQ"""
        candidates = list(self.faqs.values())
        
        # 精确URL匹配
        if page_url:
            url_matches = [f for f in candidates if f.page_url == page_url]
            if url_matches:
                return url_matches
        
        # 类型匹配
        if page_type:
            type_matches = [f for f in candidates if f.category == page_type]
            if type_matches:
                return type_matches
        
        # 关键词匹配
        if query:
            query_words = set(query.lower().split())
            scored = []
            for f in candidates:
                score = sum(1 for w in query_words if w in f.keywords)
                if score > 0:
                    scored.append((score, f))
            scored.sort(key=lambda x: -x[0])
            return [f for _, f in scored[:5]]
        
        # 返回全局FAQ
        return [f for f in candidates if not f.page_url][:5]
    
    def add_help_block(self, name: str, help_type: str, title: str,
                      content: str, position: str = "bottom_right",
                      **kwargs) -> HelpBlock:
        block_id = hashlib.md5(f"{name}{time.time()}".encode()).hexdigest()[:8]
        block = HelpBlock(
            block_id=block_id,
            name=name,
            help_type=help_type,
            title=title,
            content=content,
            position=position,
            **kwargs
        )
        self.help_blocks[block_id] = block
        return block
    
    def record_feedback(self, faq_id: str, helpful: bool):
        """记录FAQ有用性反馈"""
        faq = self.faqs.get(faq_id)
        if not faq:
            return
        if helpful:
            faq.helpful_count += 1
        else:
            faq.not_helpful_count += 1
    
    def record_help_block_shown(self, block_id: str):
        self.help_blocks.get(block_id, None)
        for b in self.help_blocks.values():
            if b.block_id == block_id:
                b.shown_count += 1
                break
    
    def generate_faq_page_html(self, faqs: List[FAQItem] = None) -> str:
        """生成FAQ页面HTML"""
        faqs = faqs or list(self.faqs.values())[:10]
        
        categories = defaultdict(list)
        for f in faqs:
            categories[f.category or "其他"].append(f)
        
        html = '''<div class="faq-container" itemscope itemtype="https://schema.org/FAQPage">
'''
        for cat, items in categories.items():
            html += f'  <h2>{cat.upper()}</h2>\n'
            for faq in items:
                html += f'''  <div class="faq-item" itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
    <h3 class="faq-q" itemprop="name">{faq.question}</h3>
    <div class="faq-a" itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">
      <p itemprop="text">{faq.answer}</p>
    </div>
    <div class="faq-feedback">
      <span>这有帮助吗？</span>
      <button class="faq-yes" data-id="{faq.faq_id}">👍 是</button>
      <button class="faq-no" data-id="{faq.faq_id}">👎 否</button>
    </div>
  </div>
'''
        
        html += '''</div>
<style>
.faq-container {{ max-width: 800px; margin: 40px auto; padding: 0 20px; font-family: system-ui, sans-serif; }}
.faq-container h2 {{ color: #333; border-bottom: 2px solid #667eea; padding-bottom: 8px; margin: 32px 0 16px; }}
.faq-item {{ margin-bottom: 24px; border: 1px solid #eee; border-radius: 12px; padding: 20px; background: #fff; }}
.faq-q {{ color: #222; margin-bottom: 12px; font-size: 18px; }}
.faq-a {{ color: #555; line-height: 1.7; }}
.faq-a p {{ margin: 0; }}
.faq-feedback {{ margin-top: 12px; font-size: 13px; color: #999; }}
.faq-feedback button {{ background: #f0f0f0; border: none; padding: 4px 12px; border-radius: 4px; cursor: pointer; margin-right: 8px; }}
.faq-feedback button:hover {{ background: #e0e0e0; }}
</style>
<script>
document.querySelectorAll(".faq-yes, .faq-no").forEach(btn => {{
    btn.addEventListener("click", function() {{
        var id = this.dataset.id;
        var helpful = this.classList.contains("faq-yes");
        // 发送反馈到服务器
        console.log("FAQ feedback:", id, helpful);
        this.parentElement.innerHTML = "<span style='color:#27ae60'>感谢反馈！</span>";
    }});
}});
</script>'''
        return html
    
    def generate_help_widget_html(self, block: HelpBlock) -> str:
        """生成帮助组件HTML"""
        positions = {
            "bottom_right": "bottom: 20px; right: 20px;",
            "bottom_left": "bottom: 20px; left: 20px;",
            "floating": "bottom: 20px; right: 20px; border-radius: 50%;",
        }
        pos = positions.get(block.position, positions["bottom_right"])
        
        if block.help_type == "quick_tip":
            return f'''<!-- Help Widget: {block.name} -->
<div id="help-{block.block_id}" style="position: fixed; {pos} z-index: 9999; display: none;">
  <div style="background: #fff; border-radius: 12px; box-shadow: 0 8px 32px rgba(0,0,0,0.15); padding: 20px; max-width: 300px; border-left: 4px solid #667eea;">
    <div style="font-weight: 700; margin-bottom: 8px;">💡 {block.title}</div>
    <p style="color: #555; font-size: 14px; margin: 0 0 12px;">{block.content}</p>
    {"<button onclick='this.parentElement.parentElement.style.display=\"none\"' style='background:#667eea;color:#fff;border:none;padding:6px 16px;border-radius:6px;cursor:pointer;'>知道了</button>" if block.dismissible else ""}
  </div>
</div>
<script>
(function() {{
    var shown = false;
    var key = "help_{block.block_id}_shown";
    function showTip() {{
        if (shown || sessionStorage.getItem(key)) return;
        shown = true;
        sessionStorage.setItem(key, "1");
        var el = document.getElementById("help-{block.block_id}");
        if (el) {{ el.style.display = "block"; }}
    }}
    window.addEventListener("load", function() {{
        setTimeout(showTip, {block.trigger_delay * 1000});
    }});
}})();
</script>'''
        
        elif block.help_type == "chat_trigger":
            return f'''<!-- Chat Trigger -->
<div id="chat-{block.block_id}" style="position: fixed; {pos} z-index: 9999;">
  <button onclick="window.open('/chat', 'chat', 'width=400,height=600')" style="background: #667eea; color: white; border: none; width: 60px; height: 60px; border-radius: 50%; font-size: 24px; cursor: pointer; box-shadow: 0 4px 16px rgba(102,126,234,0.4);">
    💬
  </button>
</div>'''
        
        return ""
    
    def generate_wp_shortcode(self, faq_ids: List[str] = None) -> str:
        faq_ids = faq_ids or list(self.faqs.keys())[:5]
        ids_str = ",".join(faq_ids)
        return f'''[faq-dynamic ids="{ids_str}" style="accordion"]'''
    
    def generate_report(self) -> Dict[str, Any]:
        total_views = sum(f.view_count for f in self.faqs.values())
        total_helpful = sum(f.helpful_count for f in self.faqs.values())
        total_feedback = sum(f.helpful_count + f.not_helpful_count for f in self.faqs.values())
        
        top_faqs = sorted(self.faqs.values(), key=lambda f: f.view_count, reverse=True)[:5]
        
        return {
            "total_faqs": len(self.faqs),
            "total_views": total_views,
            "feedback_rate": f"{total_feedback / max(1, total_views) * 100:.1f}%",
            "helpful_rate": f"{total_helpful / max(1, total_feedback) * 100:.1f}%" if total_feedback else "N/A",
            "top_faqs": [
                {"question": f.question[:50], "views": f.view_count, "helpful": f"{f.helpful_pct*100:.0f}%"}
                for f in top_faqs
            ],
            "help_blocks": [
                {"name": b.name, "type": b.help_type, "shown": b.shown_count, "clicked": b.clicked_count}
                for b in self.help_blocks.values()
            ]
        }

def demo():
    faq_system = DynamicFAQSystem()
    
    # 添加自定义FAQ
    faq_system.add_faq(
        "Auto-Claw和雇佣全职SEO专家哪个更划算？",
        "按3年周期计算：全职SEO年薪约$80K+；Auto-Claw企业版月费$999，年费$9,999，节省90%以上。同时AI 7×24工作，永不疲倦。",
        category="pricing",
        page_url=""
    )
    
    # 添加帮助块
    tip = faq_system.add_help_block(
        name="新手引导",
        help_type="quick_tip",
        title="快速开始",
        content="上传你的产品列表，AI自动分析SEO问题并生成优化建议。平均10分钟完成初始设置。",
        position="bottom_right",
        trigger_delay=15,
        dismissible=True
    )
    
    chat = faq_system.add_help_block(
        name="在线客服",
        help_type="chat_trigger",
        title="需要帮助？",
        content="",
        position="bottom_right"
    )
    
    # 模拟反馈
    for i, faq in enumerate(list(faq_system.faqs.values())[:3]):
        faq.view_count = 100 + i * 20
        faq.helpful_count = int(faq.view_count * (0.8 - i * 0.1))
        faq.not_helpful_count = int(faq.view_count * 0.1)
    
    # 获取pricing相关FAQ
    pricing_faqs = faq_system.get_faqs_for_page(page_type="pricing")
    print(f"\n📋 Pricing相关FAQ ({len(pricing_faqs)}条):")
    for f in pricing_faqs:
        print(f"   Q: {f.question[:40]}...")
    
    # 报告
    report = faq_system.generate_report()
    print(f"\n📊 FAQ系统报告:")
    print(f"   FAQ总数: {report['total_faqs']}")
    print(f"   总浏览: {report['total_views']}")
    print(f"   有用率: {report['helpful_rate']}")
    print(f"   帮助块: {len(report['help_blocks'])}")
    
    # 生成FAQ页面
    html = faq_system.generate_faq_page_html()
    with open("/tmp/faq_page.html", "w") as f:
        f.write(html)
    print(f"\n✅ FAQ页面已生成: /tmp/faq_page.html")
    print(f"   短代码: {faq_system.generate_wp_shortcode()}")

if __name__ == "__main__":
    demo()
