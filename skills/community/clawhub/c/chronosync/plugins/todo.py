"""
待办同步插件

功能：
- 识别任务项（"我要..."、"记得..."）
- 追踪任务状态
- 跨会话提醒
"""

import os
import re
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

# 从 plugin_base 导入 Plugin 基类
sys.path.insert(0, str(Path(__file__).parent.parent))
from plugin_base import Plugin


class TodoPlugin(Plugin):
    """待办同步插件"""
    
    name = "todo"
    enabled = True
    
    # 任务识别模式
    TODO_PATTERNS = [
        r"我要(.*)",
        r"记得(.*)",
        r"需要(.*)",
        r"应该(.*)",
        r"计划(.*)",
        r"目标(.*)",
        r"待办[：:](.*)",
        r"TODO[：:](.*)",
    ]
    
    # 完成关键词
    DONE_KEYWORDS = [
        "完成了", "做完了", "搞定了", "已解决", "已处理",
        "finish", "done", "completed", "resolved"
    ]
    
    def __init__(self):
        # 从环境变量或默认位置获取
        openclaw_dir = Path(os.environ.get("OPENCLAW_STATE_DIR", Path.home() / ".openclaw"))
        self.output_dir = openclaw_dir / "workspace" / "memory" / "sync" / "todos"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.todos_file = self.output_dir / "active.json"
    
    def on_sync(self, messages: List[Dict]) -> Dict[str, Any]:
        """处理消息，提取和更新任务"""
        new_todos = []
        completed_todos = []
        
        for msg in messages:
            content = msg.get("content", "")
            role = msg.get("role", "")
            
            # 提取新任务
            if role == "user":
                todos = self._extract_todos(content)
                for todo in todos:
                    new_todos.append({
                        "content": todo,
                        "created_at": msg.get("timestamp", datetime.now().isoformat()),
                        "status": "active",
                        "source": "user"
                    })
            
            # 检测完成的任务
            completed = self._detect_completed(content)
            if completed:
                completed_todos.extend(completed)
        
        # 更新任务状态
        all_todos = self._load_todos()
        
        # 添加新任务
        all_todos.extend(new_todos)
        
        # 标记完成任务
        for completed in completed_todos:
            for todo in all_todos:
                if todo["status"] == "active" and self._is_match(completed, todo["content"]):
                    todo["status"] = "completed"
                    todo["completed_at"] = datetime.now().isoformat()
        
        # 保存
        self._save_todos(all_todos)
        self._export_markdown(all_todos)
        
        active_count = len([t for t in all_todos if t["status"] == "active"])
        completed_count = len([t for t in all_todos if t["status"] == "completed"])
        
        return {
            "new_todos": len(new_todos),
            "completed_todos": len(completed_todos),
            "active_total": active_count,
            "completed_total": completed_count
        }
    
    def _extract_todos(self, content: str) -> List[str]:
        """从消息中提取任务"""
        todos = []
        for pattern in self.TODO_PATTERNS:
            matches = re.findall(pattern, content, re.IGNORECASE)
            todos.extend([m.strip() for m in matches if m.strip()])
        return todos
    
    def _detect_completed(self, content: str) -> List[str]:
        """检测完成的任务"""
        completed = []
        for keyword in self.DONE_KEYWORDS:
            if keyword in content:
                # 提取完成的任务描述（简化处理）
                completed.append(content)
                break
        return completed
    
    def _is_match(self, completed_text: str, todo_content: str) -> bool:
        """判断完成文本是否匹配任务"""
        # 简化匹配：关键词重叠
        completed_words = set(completed_text.lower().split())
        todo_words = set(todo_content.lower().split())
        overlap = completed_words & todo_words
        return len(overlap) >= 2  # 至少2个词重叠
    
    def _load_todos(self) -> List[Dict]:
        """加载现有任务"""
        if self.todos_file.exists():
            try:
                with open(self.todos_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def _save_todos(self, todos: List[Dict]):
        """保存任务"""
        with open(self.todos_file, 'w', encoding='utf-8') as f:
            json.dump(todos, f, indent=2, ensure_ascii=False)
    
    def _export_markdown(self, todos: List[Dict]):
        """导出 Markdown 格式"""
        md_file = self.output_dir / "todos.md"
        
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write("# 待办任务\n\n")
            
            # 活跃任务
            f.write("## 进行中\n\n")
            active = [t for t in todos if t["status"] == "active"]
            for i, todo in enumerate(active, 1):
                f.write(f"{i}. [ ] {todo['content']}\n")
                f.write(f"   - 创建于: {todo['created_at']}\n\n")
            
            if not active:
                f.write("*暂无进行中任务*\n\n")
            
            # 已完成任务
            f.write("## 已完成\n\n")
            completed = [t for t in todos if t["status"] == "completed"]
            for i, todo in enumerate(completed[-10:], 1):  # 只显示最近10个
                f.write(f"{i}. [x] {todo['content']}\n")
                f.write(f"   - 完成于: {todo.get('completed_at', '未知')}\n\n")
            
            if not completed:
                f.write("*暂无已完成任务*\n\n")


# 实例化
plugin = TodoPlugin()
