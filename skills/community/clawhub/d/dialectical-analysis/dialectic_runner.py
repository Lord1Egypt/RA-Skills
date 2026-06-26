#!/usr/bin/env python3
"""
辩证商业分析主运行器 V2.0

支持：
- 动态轮次：根据议题复杂度自动调整
- 仲裁者Agent：第三方视角总结
- 知识增强：tavily-search集成
- 实时干预：用户中途注入问题

Usage:
    python dialectic_runner.py --topic "分析主题" --version v2 --enable_search
"""

import json
import os
import sys
import argparse
import uuid
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# 配置路径
SKILL_DIR = Path(__file__).parent
WORKSPACE_DIR = SKILL_DIR / "workspace"
PROMPTS_DIR = SKILL_DIR / "prompts"
TEMPLATES_DIR = SKILL_DIR / "templates"


class ComplexityAnalyzer:
    """议题复杂度分析器"""
    
    # 复杂度关键词映射
    HIGH_COMPLEXITY_KEYWORDS = [
        "市场进入", "收购", "并购", "上市", "ipo", "战略转型",
        "多元化", "全球化", "技术转型", "新市场", "新产品线",
        "人工智能", "自动驾驶", "量子计算", "区块链", "元宇宙"
    ]
    
    MEDIUM_COMPLEXITY_KEYWORDS = [
        "产品开发", "市场扩张", "渠道建设", "品牌升级",
        "运营优化", "组织调整", "合作伙伴", "合资"
    ]
    
    LOW_COMPLEXITY_KEYWORDS = [
        "营销活动", "用户增长", "功能优化", "客服改进",
        "效率提升", "成本控制", "小幅调整"
    ]
    
    @classmethod
    def analyze(cls, topic: str, background: str = "") -> Dict[str, Any]:
        """分析议题复杂度"""
        text = f"{topic} {background}".lower()
        
        # 统计关键词匹配
        high_count = sum(1 for kw in cls.HIGH_COMPLEXITY_KEYWORDS if kw in text)
        medium_count = sum(1 for kw in cls.MEDIUM_COMPLEXITY_KEYWORDS if kw in text)
        low_count = sum(1 for kw in cls.LOW_COMPLEXITY_KEYWORDS if kw in text)
        
        # 计算复杂度得分 (1-10)
        complexity_score = min(10, 1 + high_count * 2 + medium_count * 1 + low_count * 0.5)
        
        # 映射到轮次 (3-8轮)
        if complexity_score >= 7:
            rounds = 7
        elif complexity_score >= 5:
            rounds = 6
        elif complexity_score >= 3:
            rounds = 5
        else:
            rounds = 4
        
        return {
            "score": complexity_score,
            "rounds": rounds,
            "level": "high" if complexity_score >= 7 else "medium" if complexity_score >= 3 else "low",
            "keywords_matched": {
                "high": high_count,
                "medium": medium_count,
                "low": low_count
            }
        }


class KnowledgeEnhancer:
    """知识增强器 - 内置搜索实现（不依赖外部Skill）"""
    
    def __init__(self):
        # 内置搜索，无外部依赖
        pass
    
    def search(self, query: str, count: int = 5) -> List[Dict]:
        """执行内置搜索（不依赖外部Skill）"""
        import urllib.parse
        import urllib.request
        
        # 1. 尝试 Tavily API
        api_key = os.environ.get("TAVILY_API_KEY")
        if api_key:
            try:
                import requests
                url = "https://api.tavily.com/search"
                payload = {"query": query, "api_key": api_key, "max_results": count}
                resp = requests.post(url, json=payload, timeout=15)
                if resp.status_code == 200:
                    data = resp.json()
                    results = []
                    for item in data.get("results", [])[:count]:
                        results.append({
                            "title": item.get("title", ""),
                            "url": item.get("url", ""),
                            "description": item.get("content", "")
                        })
                    if results:
                        return results
            except Exception as e:
                print(f"[知识增强] Tavily API失败: {e}", file=sys.stderr)
        
        # 2. Fallback: Brave Search API
        api_key = os.environ.get("BRAVE_API_KEY")
        if api_key:
            try:
                import requests
                url = "https://api.search.brave.com/res/v1/web/search"
                headers = {"X-Subscription-Token": api_key, "Accept": "application/json"}
                params = {"q": query, "count": min(count, 10)}
                resp = requests.get(url, headers=headers, params=params, timeout=15)
                if resp.status_code == 200:
                    data = resp.json()
                    results = []
                    for item in data.get("web", {}).get("results", [])[:count]:
                        results.append({
                            "title": item.get("title", ""),
                            "url": item.get("url", ""),
                            "description": item.get("description", "")
                        })
                    if results:
                        return results
            except Exception as e:
                print(f"[知识增强] Brave Search失败: {e}", file=sys.stderr)
        
        # 3. 最终Fallback: 免费的DuckDuckGo HTML搜索
        try:
            url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}&b={count}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as response:
                html = response.read().decode("utf-8")
            # 简单解析HTML标题和链接
            import re
            results = []
            for match in re.finditer(r'<a class="result__a" href="(.*?)">(.*?)</a>.*?<a class="result__c" href=".*?">(.*?)</a>', html, re.DOTALL):
                url, title, desc = match.groups()
                results.append({"title": title.strip(), "url": url, "description": desc.strip()[:200]})
                if len(results) >= count:
                    break
            if results:
                return results
        except Exception as e:
            print(f"[知识增强] DuckDuckGo fallback失败: {e}", file=sys.stderr)
        
        return [{"error": "无可用搜索服务（请配置TAVILY_API_KEY或BRAVE_API_KEY）", "query": query}]
    
    def enhance_topic(self, topic: str, constraints: List[str] = None) -> Dict[str, Any]:
        """增强主题知识"""
        search_queries = [topic]
        
        # 添加约束相关查询
        if constraints:
            for c in constraints:
                if "预算" in c:
                    # 提取金额
                    match = re.search(r'(\d+[万亿]?)', c)
                    if match:
                        amount = match.group(1)
                        search_queries.append(f"{topic} {amount} 投资回报")
                if "市场" in c:
                    search_queries.append(f"{topic} 市场规模 竞争格局")
        
        results = {}
        for q in search_queries[:3]:  # 最多3个查询
            results[q] = self.search(q)
        
        return {
            "topic": topic,
            "search_results": results,
            "timestamp": datetime.now().isoformat()
        }


class DialecticRunnerV2:
    """辩证分析主运行器 V2.0"""
    
    def __init__(self, session_id: Optional[str] = None):
        self.session_id = session_id or str(uuid.uuid4())[:8]
        self.workspace = WORKSPACE_DIR / self.session_id
        self.state_file = self.workspace / "state.json"
        self.input_file = self.workspace / "input.json"
        self.intervention_file = self.workspace / "interventions.json"
        
        # V2 新增组件
        self.complexity_analyzer = ComplexityAnalyzer()
        self.knowledge_enhancer = KnowledgeEnhancer()
        
    def initialize(self, topic: str, background: str = "", 
                   focus_questions: List[str] = None, 
                   constraints: List[str] = None,
                   max_rounds: int = None,
                   version: str = "v2",
                   enable_search: bool = True,
                   dimensions: List[str] = None) -> Dict[str, Any]:
        """初始化工作空间和状态"""
        # 创建工作目录
        self.workspace.mkdir(parents=True, exist_ok=True)
        (self.workspace / "pro_agent").mkdir(exist_ok=True)
        (self.workspace / "con_agent").mkdir(exist_ok=True)
        (self.workspace / "arbitrator").mkdir(exist_ok=True)
        
        # 动态计算轮次
        if max_rounds is None:
            complexity = self.complexity_analyzer.analyze(topic, background)
            max_rounds = complexity["rounds"]
            print(f"[复杂度分析] 得分: {complexity['score']}, 推荐轮次: {max_rounds}")
        
        # 知识增强
        knowledge_data = {}
        if enable_search and version in ["v2", "v3"]:
            print(f"[知识增强] 搜索相关信息...")
            knowledge_data = self.knowledge_enhancer.enhance_topic(topic, constraints)
        
        # 准备输入数据
        input_data = {
            "topic": topic,
            "background": background,
            "focus_questions": focus_questions or [],
            "constraints": constraints or [],
            "max_rounds": max_rounds,
            "version": version,
            "enable_search": enable_search,
            "dimensions": dimensions or [],
            "knowledge_data": knowledge_data,
            "created_at": datetime.now().isoformat()
        }
        
        # 写入输入文件
        with open(self.input_file, 'w', encoding='utf-8') as f:
            json.dump(input_data, f, ensure_ascii=False, indent=2)
        
        # 初始化状态
        state = {
            "session_id": self.session_id,
            "current_round": 0,
            "max_rounds": max_rounds,
            "version": version,
            "convergence": {
                "status": "initialized",
                "pro_acceptance": 0.0,
                "con_acceptance": 0.0,
                "consensus_topics": [],
                "disputed_topics": []
            },
            "interventions": [],
            "last_update": datetime.now().isoformat()
        }
        
        self._save_state(state)
        print(f"[DialecticRunner V2] 初始化完成，会话ID: {self.session_id}")
        print(f"[DialecticRunner V2] 版本: {version}, 轮次: {max_rounds}")
        
        return state
    
    def add_intervention(self, question: str) -> Dict[str, Any]:
        """用户实时干预"""
        state = self._load_state()
        
        intervention = {
            "id": len(state.get("interventions", [])),
            "question": question,
            "round": state["current_round"],
            "timestamp": datetime.now().isoformat()
        }
        
        state.setdefault("interventions", []).append(intervention)
        self._save_state(state)
        
        print(f"[实时干预] 第{intervention['round']}轮注入问题: {question}")
        
        return intervention
    
    def _save_state(self, state: Dict[str, Any]):
        """保存状态到文件"""
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    
    def _load_state(self) -> Dict[str, Any]:
        """加载状态"""
        with open(self.state_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _load_prompt(self, filename: str) -> str:
        """加载Prompt文件"""
        prompt_path = PROMPTS_DIR / filename
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _load_template(self, filename: str) -> str:
        """加载模板文件"""
        template_path = TEMPLATES_DIR / filename
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _save_debate_file(self, agent: str, round_num: int, content: Dict[str, Any]):
        """保存辩论文件"""
        filename = f"round_{round_num}.json"
        filepath = self.workspace / agent / filename
        content['round'] = round_num
        content['agent'] = agent
        content['timestamp'] = datetime.now().isoformat()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
        
        return filepath
    
    def _load_debate_file(self, agent: str, round_num: int) -> Optional[Dict[str, Any]]:
        """加载辩论文件"""
        filename = f"round_{round_num}.json"
        filepath = self.workspace / agent / filename
        
        if not filepath.exists():
            return None
            
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _check_convergence(self, pro_content: Dict, con_content: Dict, current_round: int, max_rounds: int) -> Dict[str, Any]:
        """检查收敛条件"""
        convergence = {
            "status": "debating",
            "reason": ""
        }
        
        # 条件1: 达到最大轮次
        if current_round >= max_rounds:
            convergence["status"] = "max_round"
            convergence["reason"] = "达到最大辩论轮次"
            return convergence
        
        # 条件2: 双方互认对方观点有效
        pro_acknowledges = pro_content.get("content", {}).get("acknowledges_con", False)
        con_acknowledges = con_content.get("content", {}).get("acknowledges_pro", False)
        
        if pro_acknowledges and con_acknowledges:
            convergence["status"] = "mutual_acknowledgment"
            convergence["reason"] = "双方互认对方观点有效"
            return convergence
        
        # 条件3: 一方被说服
        if pro_content.get("content", {}).get("persuaded", False):
            convergence["status"] = "persuasion"
            convergence["reason"] = "正向Agent被说服"
            return convergence
        
        if con_content.get("content", {}).get("persuaded", False):
            convergence["status"] = "persuasion"
            convergence["reason"] = "反向Agent被说服"
            return convergence
        
        # 条件4: 检查是否有实质分歧（通过新论点数量判断）
        pro_new_points = pro_content.get("content", {}).get("new_points_count", 0)
        con_new_points = con_content.get("content", {}).get("new_points_count", 0)
        
        if pro_new_points == 0 and con_new_points == 0:
            convergence["status"] = "diminishing_returns"
            convergence["reason"] = "连续无新论点"
            return convergence
        
        return convergence
    
    def run_debate_round(self, round_num: int) -> Dict[str, Any]:
        """执行单轮辩论"""
        state = self._load_state()
        input_data = self._load_input()
        
        # 检查是否有干预问题
        interventions = state.get("interventions", [])
        active_intervention = None
        for iv in interventions:
            if iv.get("round") == round_num:
                active_intervention = iv
                break
        
        # 准备辩论上下文
        debate_context = {
            "topic": input_data["topic"],
            "background": input_data["background"],
            "focus_questions": input_data["focus_questions"],
            "constraints": input_data["constraints"],
            "round": round_num,
            "max_rounds": state["max_rounds"],
            "version": input_data.get("version", "v2"),
            "knowledge_data": input_data.get("knowledge_data", {}),
            "intervention": active_intervention
        }
        
        # 添加前一轮观点（如果有）
        if round_num > 0:
            pro_prev = self._load_debate_file("pro_agent", round_num - 1)
            con_prev = self._load_debate_file("con_agent", round_num - 1)
            
            if pro_prev:
                debate_context["pro_previous"] = pro_prev.get("content", {})
            if con_prev:
                debate_context["con_previous"] = con_prev.get("content", {})
        
        print(f"\n[DialecticRunner V2] ===== 第 {round_num} 轮辩论 =====")
        if active_intervention:
            print(f"[实时干预] 正在处理: {active_intervention['question']}")
        
        return {
            "status": "ready_for_agents",
            "round": round_num,
            "debate_context": debate_context,
            "state": state
        }
    
    def _load_input(self) -> Dict[str, Any]:
        """加载输入数据"""
        with open(self.input_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def record_agent_response(self, agent: str, round_num: int, content: Dict[str, Any]):
        """记录Agent的响应"""
        self._save_debate_file(agent, round_num, content)
    
    def update_state_after_round(self, round_num: int, convergence: Dict[str, Any]):
        """更新状态"""
        state = self._load_state()
        state["current_round"] = round_num
        state["convergence"] = convergence
        state["last_update"] = datetime.now().isoformat()
        self._save_state(state)
    
    def is_converged(self) -> bool:
        """检查是否已收敛"""
        state = self._load_state()
        convergence_status = state.get("convergence", {}).get("status", "debating")
        return convergence_status != "debating"
    
    def generate_arbitrator_summary(self) -> Dict[str, Any]:
        """生成仲裁者总结"""
        state = self._load_state()
        input_data = self._load_input()
        
        # 收集所有轮次
        pro_rounds = []
        con_rounds = []
        
        for r in range(state["current_round"] + 1):
            pro_data = self._load_debate_file("pro_agent", r)
            con_data = self._load_debate_file("con_agent", r)
            if pro_data:
                pro_rounds.append(pro_data)
            if con_data:
                con_rounds.append(con_data)
        
        # 提取关键信息
        all_pro_arguments = []
        all_con_arguments = []
        
        for r in pro_rounds:
            content = r.get("content", {})
            all_pro_arguments.extend(content.get("main_arguments", []))
        
        for r in con_rounds:
            content = r.get("content", {})
            all_con_arguments.extend(content.get("main_arguments", []))
        
        # 生成仲裁者分析
        summary = {
            "topic": input_data["topic"],
            "total_rounds": state["current_round"] + 1,
            "pro_arguments_count": len(all_pro_arguments),
            "con_arguments_count": len(all_con_arguments),
            "convergence_status": state.get("convergence", {}).get("status", "unknown"),
            "pro_key_points": [a.get("point", "")[:100] for a in all_pro_arguments[:5]],
            "con_key_points": [a.get("point", "")[:100] for a in all_con_arguments[:5]],
            "consensus": state.get("convergence", {}).get("consensus_topics", []),
            "disputes": state.get("convergence", {}).get("disputed_topics", []),
            "timestamp": datetime.now().isoformat()
        }
        
        # 保存仲裁者总结
        arbitrator_file = self.workspace / "arbitrator" / "summary.json"
        with open(arbitrator_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        return summary
    
    def generate_final_report(self) -> str:
        """生成最终报告 V2.0"""
        state = self._load_state()
        input_data = self._load_input()
        
        # 收集所有轮次
        pro_rounds = []
        con_rounds = []
        
        for r in range(state["current_round"] + 1):
            pro_data = self._load_debate_file("pro_agent", r)
            con_data = self._load_debate_file("con_agent", r)
            if pro_data:
                pro_rounds.append(pro_data)
            if con_data:
                con_rounds.append(con_data)
        
        # 生成仲裁者总结
        arbitrator_summary = self.generate_arbitrator_summary()
        
        # 加载模板
        template = self._load_template("v2_report.md")
        
        # 渲染报告
        report = template.format(
            topic=input_data["topic"],
            background=input_data.get("background", "未提供"),
            focus_questions="\n".join([f"- {q}" for q in input_data.get("focus_questions", [])]),
            constraints="\n".join([f"- {c}" for c in input_data.get("constraints", [])]),
            rounds=state["current_round"],
            convergence_status=state.get("convergence", {}).get("status", "unknown"),
            convergence_reason=state.get("convergence", {}).get("reason", ""),
            consensus_topics="\n".join([f"- {t}" for t in arbitrator_summary.get("consensus", [])]) or "暂无明确共识",
            disputed_topics="\n".join([f"- {t}" for t in arbitrator_summary.get("disputes", [])]) or "暂无明显分歧",
            pro_rounds_summary=self._summarize_rounds(pro_rounds),
            con_rounds_summary=self._summarize_rounds(con_rounds),
            arbitrator_summary=self._format_arbitrator_summary(arbitrator_summary),
            session_id=self.session_id,
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            knowledge_enhancement=self._format_knowledge_data(input_data.get("knowledge_data", {}))
        )
        
        # 保存报告
        report_file = self.workspace / "final_report.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return report
    
    def _format_arbitrator_summary(self, summary: Dict) -> str:
        """格式化仲裁者总结"""
        lines = [
            f"## 仲裁者总结",
            f"",
            f"- 辩论轮次: {summary.get('total_rounds', 0)}轮",
            f"- 正向论点: {summary.get('pro_arguments_count', 0)}个",
            f"- 批判论点: {summary.get('con_arguments_count', 0)}个",
            f"- 收敛状态: {summary.get('convergence_status', 'unknown')}",
            f"",
            f"### 关键共识",
        ]
        
        consensus = summary.get("consensus", [])
        if consensus:
            for c in consensus:
                lines.append(f"- {c}")
        else:
            lines.append("暂无明确共识")
        
        lines.append(f"")
        lines.append(f"### 主要分歧")
        
        disputes = summary.get("disputes", [])
        if disputes:
            for d in disputes:
                lines.append(f"- {d}")
        else:
            lines.append("暂无明显分歧")
        
        return "\n".join(lines)
    
    def _format_knowledge_data(self, knowledge_data: Dict) -> str:
        """格式化知识增强数据"""
        if not knowledge_data or not knowledge_data.get("search_results"):
            return "无补充数据"
        
        lines = ["## 知识增强数据", ""]
        
        for query, results in knowledge_data.get("search_results", {}).items():
            lines.append(f"### {query}")
            for r in results[:3]:
                title = r.get("title", r.get("url", ""))
                content = r.get("content", r.get("snippet", ""))[:200]
                if title:
                    lines.append(f"- **{title}**: {content}...")
            lines.append("")
        
        return "\n".join(lines)
    
    def _summarize_rounds(self, rounds: List[Dict]) -> str:
        """汇总轮次内容"""
        if not rounds:
            return "无内容"
        
        summaries = []
        for r in rounds:
            round_num = r.get("round", "?")
            content = r.get("content", {})
            main_args = content.get("main_arguments", [])
            
            if main_args:
                args_summary = "\n".join([f"  - {arg.get('point', '')}" for arg in main_args[:3]])
                summaries.append(f"**第{round_num}轮**: \n{args_summary}")
        
        return "\n\n".join(summaries) if summaries else "无实质论点"


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="辩证商业分析运行器 V2.0")
    parser.add_argument("--topic", "-t", required=True, help="分析主题")
    parser.add_argument("--background", "-b", default="", help="背景信息")
    parser.add_argument("--focus_questions", "-f", default="", help="关注问题（逗号分隔）")
    parser.add_argument("--constraints", "-c", default="", help="约束条件（逗号分隔）")
    parser.add_argument("--max_rounds", "-r", type=int, default=None, help="最大辩论轮次（默认自动）")
    parser.add_argument("--version", "-v", default="v2", choices=["v1", "v2", "v3"], help="版本")
    parser.add_argument("--enable_search", "-s", default=True, help="启用知识增强")
    parser.add_argument("--dimensions", "-d", default="", help="多维分析维度（逗号分隔，V3）")
    parser.add_argument("--session_id", "-i", default=None, help="会话ID")
    parser.add_argument("--add_intervention", "-a", default="", help="添加实时干预问题")
    
    return parser.parse_args()


def main():
    """主函数"""
    args = parse_args()
    
    # 解析列表参数
    focus_questions = [q.strip() for q in args.focus_questions.split(",") if q.strip()]
    constraints = [c.strip() for c in args.constraints.split(",") if c.strip()]
    dimensions = [d.strip() for d in args.dimensions.split(",") if d.strip()]
    
    # 创建运行器
    runner = DialecticRunnerV2(session_id=args.session_id)
    
    # 初始化
    runner.initialize(
        topic=args.topic,
        background=args.background,
        focus_questions=focus_questions,
        constraints=constraints,
        max_rounds=args.max_rounds,
        version=args.version,
        enable_search=args.enable_search,
        dimensions=dimensions if dimensions else None
    )
    
    # 处理实时干预
    if args.add_intervention:
        runner.add_intervention(args.add_intervention)
    
    print(f"\n[DialecticRunner V2] 辩证分析系统已就绪")
    print(f"[DialecticRunner V2] 工作目录: {runner.workspace}")
    
    return runner


if __name__ == "__main__":
    main()
