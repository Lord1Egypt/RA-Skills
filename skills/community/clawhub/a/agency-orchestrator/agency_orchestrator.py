#!/usr/bin/env python3
"""
Agency Orchestrator - ClawX 集成模块
提供多 Agent 协作调度能力
"""

import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Optional, Any

class AgencyOrchestrator:
    """ClawX 集成的 Agent 调度器"""
    
    def __init__(self):
        self.agency_dir = os.path.expanduser("~/.openclaw/agency-agents-zh")
        self.agents = self.scan_agents()
        self.learning_log = []
    
    def scan_agents(self) -> Dict:
        """扫描所有可用 Agent"""
        agents = {}
        categories = [
            'design', 'engineering', 'marketing', 'sales', 'product',
            'finance', 'testing', 'support', 'hr', 'project-management',
            'specialized', 'academic', 'legal', 'strategy'
        ]
        
        for category in categories:
            cat_path = os.path.join(self.agency_dir, category)
            if os.path.isdir(cat_path):
                agents[category] = []
                for file in os.listdir(cat_path):
                    if file.endswith('.md'):
                        agent_name = file[:-3]
                        agents[category].append({
                            'name': agent_name,
                            'category': category,
                            'file': file,
                            'path': os.path.join(cat_path, file)
                        })
        
        total = sum(len(v) for v in agents.values())
        print(f"[Agency] 已加载 {total} 个 Agent，覆盖 {len(agents)} 个分类")
        return agents
    
    def analyze_task(self, task: str) -> Dict:
        """分析任务需求"""
        keywords = {
            'design': ['design', 'ui', 'ux', 'visual', 'brand', '设计', '界面', '视觉'],
            'engineering': ['code', 'dev', 'api', 'database', '代码', '开发', '工程', '编程'],
            'marketing': ['marketing', 'content', 'seo', 'social', '营销', '内容', '推广'],
            'sales': ['sales', 'customer', 'discovery', '销售', '客户'],
            'product': ['product', 'roadmap', 'feature', '产品', '功能'],
            'finance': ['finance', 'budget', 'analysis', '财务', '预算', '分析'],
            'testing': ['test', 'qa', 'quality', '测试', '质量'],
            'support': ['support', 'help', 'service', '支持', '帮助'],
        }
        
        task_lower = task.lower()
        needed = []
        
        for category, kws in keywords.items():
            if any(kw in task_lower for kw in kws):
                needed.append(category)
        
        return {
            'task': task,
            'needed_categories': needed or ['general'],
            'complexity': 'medium' if len(task) > 50 else 'simple',
            'timestamp': datetime.now().isoformat()
        }
    
    def select_agents(self, task_analysis: Dict) -> List[Dict]:
        """选择最佳 Agent"""
        selected = []
        needed = task_analysis['needed_categories']
        
        for category in needed:
            if category in self.agents and self.agents[category]:
                # 选择前 3 个 Agent
                selected.extend(self.agents[category][:3])
        
        if not selected and 'specialized' in self.agents:
            selected.extend(self.agents['specialized'][:2])
        
        return selected
    
    def coordinate(self, task: str) -> Dict:
        """协调 Agent 完成任务"""
        # 分析任务
        analysis = self.analyze_task(task)
        
        # 选择 Agent
        selected_agents = self.select_agents(analysis)
        
        # 记录
        self.log_interaction(task, selected_agents)
        
        return {
            'status': 'ready',
            'task': task,
            'analysis': analysis,
            'selected_agents': selected_agents,
            'agent_count': len(selected_agents),
            'message': f"已选择 {len(selected_agents)} 个 Agent 准备执行任务"
        }
    
    def log_interaction(self, task: str, agents: List[Dict]):
        """记录交互日志"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'task': task,
            'agents': [a['name'] for a in agents],
            'categories': list(set(a['category'] for a in agents))
        }
        
        log_file = os.path.join(self.agency_dir, 'logs', 'clawx_integration.json')
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        try:
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            else:
                logs = []
            logs.append(log_entry)
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[Warning] 保存日志失败：{e}")
    
    def get_agent_list(self, category: str = None) -> Dict:
        """获取 Agent 列表"""
        if category:
            return {
                'category': category,
                'agents': self.agents.get(category, []),
                'count': len(self.agents.get(category, []))
            }
        else:
            return {
                'total': sum(len(v) for v in self.agents.values()),
                'categories': {
                    cat: len(agents) 
                    for cat, agents in self.agents.items()
                }
            }

# ClawX 工具接口
def clawx_execute(task: str) -> Dict:
    """ClawX 工具执行接口"""
    orchestrator = AgencyOrchestrator()
    return orchestrator.coordinate(task)

def clawx_list_agents(category: str = None) -> Dict:
    """ClawX 获取 Agent 列表接口"""
    orchestrator = AgencyOrchestrator()
    return orchestrator.get_agent_list(category)

# CLI 入口
if __name__ == "__main__":
    if len(sys.argv) > 1:
        task = " ".join(sys.argv[1:])
        result = clawx_execute(task)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("用法：python agency_orchestrator.py <任务描述>")
