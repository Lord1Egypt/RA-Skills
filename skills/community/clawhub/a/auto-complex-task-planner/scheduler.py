#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto Complex Task Planner - 自动复杂任务规划器

自动判断任务复杂度，创建子 agent 执行复杂任务，管理任务生命周期。
支持任务优先级队列、模板系统、进度追踪、增强质量审核。

版本：v2.0（已实现所有改进建议）
"""

import json
import re
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import deque
import uuid

# ============== 配置 ==============
CONFIG = {
    "quality_threshold": 0.7,
    "max_retries": 3,
    "timeout": 600,  # 秒
    "parallel": {
        "enabled": True,
        "max_concurrent": 5
    },
    "cleanup": {
        "auto_kill": True,
        "daily_check": True
    },
    "priority": {
        "enabled": True,
        "high_keywords": ["紧急", "优先", "马上", "立刻", "急"],
        "low_keywords": ["有空", "不急", "慢慢", "方便时"]
    }
}

# ============== 关键词库 ==============
COMPLEX_KEYWORDS = [
    '调研', '搜集', '分析', '对比', '研究', '调查',  # 调研类
    '开发', '编写', '创建', '实现', '构建', '制作',  # 开发类
    '批量', '全部', '所有', '删除', '处理', '整理',  # 批量类
    '报告', '文档', '方案', '总结', '整理', '生成',  # 文档类
    '搜索', '查找', 'Google', '百度', '爬取',  # 搜索类
]

SIMPLE_KEYWORDS = [
    '天气', '时间', '日期', '状态', '配置',  # 查询类
    '修改', '设置', '更新', '调整',  # 配置类
    '你好', '谢谢', '再见', '在吗',  # 聊天类
    '发送', '通知', '提醒', '消息',  # 通知类
]

# ============== 任务模板库 ==============
TASK_TEMPLATES = {
    "research": {
        "title": "调研任务",
        "template": "调研 [topic]：\n\n" +
                    "## 任务目标\n" +
                    "全面搜集和分析 [topic] 相关信息。\n\n" +
                    "## 执行步骤\n" +
                    "1. 搜索 [channel1] 相关内容（如小红书、知乎）\n" +
                    "2. 搜索 [channel2] 相关内容（如官方网站、行业报告）\n" +
                    "3. 整理 [info_points]（至少 5 个关键信息点）\n" +
                    "4. 分析 [analysis_dimensions]（市场、成本、风险等）\n" +
                    "5. 给出实用建议和结论\n\n" +
                    "## 交付要求\n" +
                    "- 结构化报告（Markdown 格式）\n" +
                    "- 包含数据来源和引用\n" +
                    "- 提供可操作建议\n\n" +
                    "## 保存位置\n" +
                    "/home/admin/.openclaw/workspace/temp/[output_filename].md"
    },
    "development": {
        "title": "开发任务",
        "template": "开发 [feature_name]：\n\n" +
                    "## 任务目标\n" +
                    "[feature_description]\n\n" +
                    "## 技术要求\n" +
                    "1. [tech_requirement1]\n" +
                    "2. [tech_requirement2]\n" +
                    "3. [tech_requirement3]\n\n" +
                    "## 开发步骤\n" +
                    "1. 需求分析和设计\n" +
                    "2. 编写核心代码\n" +
                    "3. 添加错误处理和日志\n" +
                    "4. 编写使用说明\n" +
                    "5. 测试基本功能\n\n" +
                    "## 交付物\n" +
                    "- [ ] 可执行的代码/脚本\n" +
                    "- [ ] 使用说明文档\n" +
                    "- [ ] 测试结果报告\n\n" +
                    "## 保存位置\n" +
                    "/home/admin/.openclaw/workspace/[output_path]/"
    },
    "documentation": {
        "title": "文档生成",
        "template": "生成 [doc_name]：\n\n" +
                    "## 内容要求\n" +
                    "1. [chapter1]\n" +
                    "2. [chapter2]\n" +
                    "3. [chapter3]\n\n" +
                    "## 格式要求\n" +
                    "- 格式：[format]（Word/PDF/Markdown）\n" +
                    "- 字数：[word_count]\n" +
                    "- 包含：表格、图表、案例\n" +
                    "- 风格：[style]（专业/通俗/技术）\n\n" +
                    "## 质量要求\n" +
                    "- 内容准确无误\n" +
                    "- 结构清晰完整\n" +
                    "- 格式规范统一\n\n" +
                    "## 保存位置\n" +
                    "/home/admin/.openclaw/workspace/temp/[output_filename].[ext]"
    },
    "batch": {
        "title": "批量处理",
        "template": "批量处理 [task_name]：\n\n" +
                    "## 任务目标\n" +
                    "[task_description]\n\n" +
                    "## 处理要求\n" +
                    "1. 支持批量操作（一次处理多个）\n" +
                    "2. 添加进度显示（百分比或计数）\n" +
                    "3. 错误处理和日志记录\n" +
                    "4. 跳过失败项，继续处理\n\n" +
                    "## 交付物\n" +
                    "- [ ] 可执行的脚本/程序\n" +
                    "- [ ] 处理结果报告\n" +
                    "- [ ] 错误日志（如有）\n\n" +
                    "## 保存位置\n" +
                    "/home/admin/.openclaw/workspace/temp/[output_path]/"
    }
}

# ============== 优先级队列 ==============
class PriorityTaskQueue:
    """任务优先级队列"""
    
    def __init__(self):
        self.high_priority = deque()
        self.normal_priority = deque()
        self.low_priority = deque()
    
    def add_task(self, task: Dict, priority: str = "normal"):
        """添加任务到队列"""
        task['created_at'] = datetime.now().isoformat()
        
        if priority == "high":
            self.high_priority.append(task)
        elif priority == "low":
            self.low_priority.append(task)
        else:
            self.normal_priority.append(task)
    
    def get_next_task(self) -> Optional[Dict]:
        """获取下一个任务"""
        if self.high_priority:
            return self.high_priority.popleft()
        if self.normal_priority:
            return self.normal_priority.popleft()
        if self.low_priority:
            return self.low_priority.popleft()
        return None
    
    def get_stats(self) -> Dict:
        """获取队列统计"""
        return {
            "high": len(self.high_priority),
            "normal": len(self.normal_priority),
            "low": len(self.low_priority),
            "total": len(self.high_priority) + len(self.normal_priority) + len(self.low_priority)
        }


# ============== 任务分析器 ==============
class TaskAnalyzer:
    """任务分析器（增强版）"""
    
    @staticmethod
    def analyze_task(task: str) -> Dict:
        """
        分析任务复杂度
        
        Returns:
            {
                "complexity": "main" | "subagent",
                "score": 0-100,
                "type": "research" | "development" | "documentation" | "batch" | "simple",
                "priority": "high" | "normal" | "low",
                "estimated_time": 分钟
            }
        """
        score = 0
        task_type = "simple"
        priority = "normal"
        
        # 1. 任务长度分 (0-30)
        length_score = min(len(task) / 2, 30)
        score += length_score
        
        # 2. 步骤数量分 (0-30)
        steps = TaskAnalyzer.count_steps(task)
        steps_score = min(steps * 10, 30)
        score += steps_score
        
        # 3. 关键词分 (0-20)
        keyword_score = TaskAnalyzer.check_keywords(task)
        score += keyword_score
        
        # 4. 时间估算分 (0-20)
        time_estimate = TaskAnalyzer.estimate_time(task)
        time_score = min(time_estimate / 3, 20)
        score += time_score
        
        # 5. 优先级判断
        priority = TaskAnalyzer.detect_priority(task)
        
        # 判断任务类型
        task_type = TaskAnalyzer.detect_task_type(task)
        
        # 决策
        complexity = "subagent" if score > 30 else "main"
        
        return {
            "complexity": complexity,
            "score": round(score, 1),
            "type": task_type,
            "priority": priority,
            "estimated_time": time_estimate
        }
    
    @staticmethod
    def detect_priority(task: str) -> str:
        """检测任务优先级"""
        task_lower = task.lower()
        
        # 高优先级关键词
        for kw in CONFIG["priority"]["high_keywords"]:
            if kw in task_lower:
                return "high"
        
        # 低优先级关键词
        for kw in CONFIG["priority"]["low_keywords"]:
            if kw in task_lower:
                return "low"
        
        return "normal"
    
    @staticmethod
    def detect_task_type(task: str) -> str:
        """检测任务类型"""
        task_lower = task.lower()
        
        if any(kw in task_lower for kw in ['调研', '搜集', '分析', '研究', '调查']):
            return "research"
        elif any(kw in task_lower for kw in ['开发', '编写', '创建', '实现', '构建']):
            return "development"
        elif any(kw in task_lower for kw in ['报告', '文档', '方案', '总结']):
            return "documentation"
        elif any(kw in task_lower for kw in ['批量', '全部', '所有']):
            return "batch"
        else:
            return "simple"
    
    @staticmethod
    def count_steps(task: str) -> int:
        """计算任务步骤数"""
        # 检查换行
        lines = task.split('\n')
        if len(lines) > 1:
            return len(lines)
        
        # 检查序号
        numbered = re.findall(r'\d+[\.、]', task)
        if numbered:
            return len(numbered)
        
        # 检查连接词
        connectors = ['首先', '然后', '接着', '最后', '第一步', '第二步']
        for conn in connectors:
            if conn in task:
                return 2  # 至少有 2 步
        
        return 1
    
    @staticmethod
    def check_keywords(task: str) -> int:
        """检查关键词"""
        score = 0
        
        # 复杂关键词
        for kw in COMPLEX_KEYWORDS:
            if kw in task:
                score += 2
        
        # 简单关键词（减分）
        for kw in SIMPLE_KEYWORDS:
            if kw in task:
                score -= 1
        
        return max(0, min(score, 20))
    
    @staticmethod
    def estimate_time(task: str) -> int:
        """估算任务时间（分钟）"""
        # 基于长度
        base_time = len(task) / 10
        
        # 基于步骤
        steps = TaskAnalyzer.count_steps(task)
        step_time = steps * 3
        
        # 基于关键词
        if any(kw in task for kw in ['调研', '搜索', '分析']):
            base_time += 10
        elif any(kw in task for kw in ['开发', '编写']):
            base_time += 15
        elif any(kw in task for kw in ['报告', '文档']):
            base_time += 10
        
        return round(base_time + step_time)


# ============== 任务调度器 ==============
class TaskScheduler:
    """任务调度器（增强版）"""
    
    def __init__(self):
        self.analyzer = TaskAnalyzer()
        self.queue = PriorityTaskQueue()
        self.memory_path = Path("/home/admin/.openclaw/workspace/memory")
        self.temp_path = Path("/home/admin/.openclaw/workspace/temp")
        self.tasks_path = self.memory_path / "tasks.json"
        
        # 确保目录存在
        self.memory_path.mkdir(parents=True, exist_ok=True)
        self.temp_path.mkdir(parents=True, exist_ok=True)
        
        # 加载任务历史
        self.tasks_history = self.load_tasks_history()
    
    def schedule_task(self, task: str, user_id: str = "default") -> Dict:
        """
        调度任务（增强版）
        
        Returns:
            {
                "action": "main" | "subagent",
                "subagents": [...],
                "priority": "high" | "normal" | "low",
                "task_id": "uuid",
                "memory_updated": True,
                "estimated_time": 分钟
            }
        """
        # 1. 分析任务
        analysis = self.analyzer.analyze_task(task)
        
        # 生成任务 ID
        task_id = str(uuid.uuid4())[:8]
        
        result = {
            "action": analysis["complexity"],
            "analysis": analysis,
            "task_id": task_id,
            "memory_updated": False,
            "estimated_time": analysis["estimated_time"]
        }
        
        if analysis["complexity"] == "subagent":
            # 2. 使用模板生成任务描述
            subagent_tasks = self.generate_subagent_tasks_with_template(
                task, 
                analysis["type"]
            )
            
            # 3. 创建子 agent（并行）
            subagents = []
            for i, subtask in enumerate(subagent_tasks):
                label = f"{analysis['type']}-{task_id}-{i}"
                subagent = {
                    "label": label,
                    "task": subtask,
                    "runtime": "subagent",
                    "mode": "run",
                    "priority": analysis["priority"]
                }
                subagents.append(subagent)
            
            result["subagents"] = subagents
            
            # 4. 记录到 Memory（JSON 格式）
            self.record_task_to_json(task, subagents, user_id, task_id, analysis)
            result["memory_updated"] = True
        
        return result
    
    def generate_subagent_tasks_with_template(self, task: str, task_type: str) -> List[str]:
        """使用模板生成子 agent 任务描述"""
        
        if task_type not in TASK_TEMPLATES:
            return [task]
        
        template = TASK_TEMPLATES[task_type]["template"]
        
        # 清理任务描述（去掉"紧急！"等前缀）
        clean_task = re.sub(r'^(紧急 | 马上 | 立刻 | 有空 | 不急)！?', '', task).strip()
        
        # 生成简洁标题
        short_title = clean_task[:30] + "..." if len(clean_task) > 30 else clean_task
        
        # 填充模板变量
        filled = template.replace("[topic]", clean_task)
        filled = filled.replace("[feature_name]", short_title)
        filled = filled.replace("[feature_description]", clean_task)
        filled = filled.replace("[doc_name]", short_title)
        filled = filled.replace("[task_name]", short_title)
        filled = filled.replace("[task_description]", clean_task)
        
        # 默认值
        filled = filled.replace("[channel1]", "小红书")
        filled = filled.replace("[channel2]", "官方网站")
        filled = filled.replace("[info_points]", "关键信息")
        filled = filled.replace("[analysis_dimensions]", "市场、成本、风险")
        filled = filled.replace("[tech_requirement1]", "Python 脚本")
        filled = filled.replace("[tech_requirement2]", "错误处理")
        filled = filled.replace("[tech_requirement3]", "使用说明")
        filled = filled.replace("[chapter1]", "第一章")
        filled = filled.replace("[chapter2]", "第二章")
        filled = filled.replace("[chapter3]", "第三章")
        filled = filled.replace("[format]", "Markdown")
        filled = filled.replace("[word_count]", "3000 字")
        filled = filled.replace("[style]", "专业")
        # 生成文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_name = re.sub(r'[^\w\u4e00-\u9fff]', '_', clean_task[:20])
        filled = filled.replace("[output_filename]", f"{safe_name}_{timestamp}")
        filled = filled.replace("[output_path]", f"temp/{safe_name}_{timestamp}/")
        filled = filled.replace("[ext]", "md")
        
        return [filled]
    
    def record_task_to_json(self, task: str, subagents: List[Dict], user_id: str, task_id: str, analysis: Dict):
        """记录任务到 JSON 文件（增强版）"""
        
        task_record = {
            "id": task_id,
            "task": task,
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "completed_at": None,
            "status": "running",
            "priority": analysis["priority"],
            "type": analysis["type"],
            "estimated_time": analysis["estimated_time"],
            "actual_time": None,
            "subagents": subagents,
            "quality_score": None,
            "feedback": [],
        }
        
        self.tasks_history.append(task_record)
        self.save_tasks_history()
        
        # 同时记录到每日 Memory 文件
        today = datetime.now().strftime("%Y-%m-%d")
        memory_file = self.memory_path / f"{today}.md"
        
        if memory_file.exists():
            content = memory_file.read_text(encoding='utf-8')
        else:
            content = f"# {today} 记忆\n\n"
        
        task_record_md = f"""
## 子 agent 任务

### 📋 任务：{task[:50]}...
- **任务 ID**: {task_id}
- **创建时间**: {datetime.now().strftime("%Y-%m-%d %H:%M")}
- **用户**: {user_id}
- **优先级**: {analysis['priority']}
- **类型**: {analysis['type']}
- **子 agent 数量**: {len(subagents)}
- **状态**: 进行中
- **预计完成**: {analysis['estimated_time']} 分钟

---
"""
        
        content += task_record_md
        memory_file.write_text(content, encoding='utf-8')
    
    def load_tasks_history(self) -> List[Dict]:
        """加载任务历史"""
        if self.tasks_path.exists():
            try:
                with open(self.tasks_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_tasks_history(self):
        """保存任务历史"""
        with open(self.tasks_path, 'w', encoding='utf-8') as f:
            json.dump(self.tasks_history, f, ensure_ascii=False, indent=2)
    
    def get_task_progress(self, task_id: str) -> Dict:
        """获取任务进度（新增功能）"""
        for task in self.tasks_history:
            if task['id'] == task_id:
                progress = {
                    "task_id": task_id,
                    "status": task["status"],
                    "created_at": task["created_at"],
                    "completed_at": task["completed_at"],
                    "priority": task["priority"],
                    "type": task["type"],
                    "subagents": [],
                    "overall_progress": 0
                }
                
                # 获取子 agent 状态
                for subagent in task["subagents"]:
                    # 这里应该调用 subagents list 获取真实状态
                    # 简化处理，假设都在运行
                    progress["subagents"].append({
                        "label": subagent["label"],
                        "status": "running" if task["status"] == "running" else task["status"],
                        "progress": 100 if task["status"] == "completed" else 50
                    })
                
                # 计算整体进度
                if progress["subagents"]:
                    avg_progress = sum(s["progress"] for s in progress["subagents"]) / len(progress["subagents"])
                    progress["overall_progress"] = round(avg_progress)
                
                return progress
        
        return {"error": "Task not found"}
    
    def review_result(self, result: Dict, task_id: str) -> Dict:
        """审核子 agent 结果（增强版）"""
        checklist = [
            '任务是否完成',
            '交付物是否齐全',
            '内容是否准确',
            '格式是否规范',
            '是否有遗漏',
        ]
        
        score = 0
        feedback = []
        
        # 1. 检查交付物存在性
        if 'file_path' in result:
            if not Path(result['file_path']).exists():
                return {
                    "passed": False,
                    "score": 0,
                    "feedback": ["❌ 交付物文件不存在"]
                }
            score += 1
            feedback.append("✅ 交付物文件存在")
        
        # 2. 检查任务完成状态
        if 'completed' in result and result['completed']:
            score += 1
            feedback.append("✅ 任务完成")
        else:
            feedback.append("❌ 任务未完成")
        
        # 3. 检查交付物
        if 'deliverables' in result and len(result['deliverables']) > 0:
            score += 1
            feedback.append("✅ 交付物齐全")
        else:
            feedback.append("❌ 缺少交付物")
        
        # 4. 简单内容质量检查（可以扩展为调用 LLM）
        if 'content' in result and len(result['content']) > 100:
            score += 1
            feedback.append("✅ 内容长度合理")
        else:
            feedback.append("⚠️ 内容可能过短")
        
        # 5. 幻觉检测（简化版）
        if self.detect_hallucination(result):
            feedback.append("⚠️ 检测到可能的幻觉内容")
        else:
            feedback.append("✅ 未发现明显幻觉")
        
        # 计算质量分
        quality_score = score / len(checklist)
        
        # 更新任务记录
        self.update_task_result(task_id, quality_score, feedback)
        
        return {
            "passed": quality_score >= CONFIG["quality_threshold"],
            "score": round(quality_score, 2),
            "feedback": feedback
        }
    
    def detect_hallucination(self, result: Dict) -> bool:
        """检测幻觉内容（简化版）"""
        # 检查是否有明显的虚假信息
        if 'content' in result:
            content = result['content']
            # 检查是否有具体数字但没有来源
            if re.search(r'\d+%', content) and '来源' not in content and 'data' not in content.lower():
                return True
        return False
    
    def update_task_result(self, task_id: str, quality_score: float, feedback: List[str]):
        """更新任务结果"""
        for task in self.tasks_history:
            if task['id'] == task_id:
                task['completed_at'] = datetime.now().isoformat()
                task['status'] = 'completed'
                task['quality_score'] = quality_score
                task['feedback'] = feedback
                self.save_tasks_history()
                break
    
    def get_daily_stats(self, date: str = None) -> Dict:
        """获取每日统计（新增功能）"""
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        tasks = [t for t in self.tasks_history 
                if t['created_at'].startswith(date)]
        
        if not tasks:
            return {"date": date, "total": 0}
        
        completed = [t for t in tasks if t['status'] == 'completed']
        failed = [t for t in tasks if t['status'] == 'failed']
        
        avg_quality = sum(t.get('quality_score', 0) for t in completed) / len(completed) if completed else 0
        avg_time = sum(t.get('actual_time', t.get('estimated_time', 0)) for t in completed) / len(completed) if completed else 0
        
        return {
            "date": date,
            "total": len(tasks),
            "completed": len(completed),
            "failed": len(failed),
            "completion_rate": round(len(completed) / len(tasks) * 100, 1) if tasks else 0,
            "avg_quality": round(avg_quality, 2),
            "avg_time": round(avg_time, 1),
            "by_priority": {
                "high": len([t for t in tasks if t['priority'] == 'high']),
                "normal": len([t for t in tasks if t['priority'] == 'normal']),
                "low": len([t for t in tasks if t['priority'] == 'low']),
            },
            "by_type": {
                "research": len([t for t in tasks if t['type'] == 'research']),
                "development": len([t for t in tasks if t['type'] == 'development']),
                "documentation": len([t for t in tasks if t['type'] == 'documentation']),
                "batch": len([t for t in tasks if t['type'] == 'batch']),
            }
        }


# ============== 主函数 ==============
def main():
    """主函数（测试用）"""
    scheduler = TaskScheduler()
    
    # 测试任务
    test_tasks = [
        "今天天气怎么样",  # 简单任务
        "紧急！帮我调研北京新发地农产品市场",  # 高优先级调研
        "开发一个小红书批量删除笔记的功能",  # 开发任务
        "有空的时候生成一份 OpenClaw 商业化调研报告",  # 低优先级文档
    ]
    
    print("=== Auto Complex Task Planner 测试 ===\n")
    
    for task in test_tasks:
        print(f"任务：{task}")
        result = scheduler.schedule_task(task)
        print(f"分析结果：{json.dumps(result, ensure_ascii=False, indent=2)}")
        print("-" * 50)
    
    # 显示统计
    print("\n=== 今日统计 ===")
    stats = scheduler.get_daily_stats()
    print(json.dumps(stats, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
