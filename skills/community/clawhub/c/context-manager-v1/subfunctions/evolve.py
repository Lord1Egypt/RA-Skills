#!/usr/bin/env python3
"""
Evolve Function - 知识发芽功能

生成 5 种高价值产出：灵光/心智模型/跨界/微习惯/潜意识
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional


class EvolveFunction:
    """知识发芽功能实现"""
    
    def __init__(self, config: dict):
        self.config = config
        self.base_path = Path(config.get("base_path", "~/kb")).expanduser()
        self.output_path = self.base_path / "outputs" / "sparks"
        self.output_path.mkdir(parents=True, exist_ok=True)
    
    def execute(self, 
                note_id: str, 
                evolve_type: str = "spark",
                context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        执行知识发芽功能
        
        Args:
            note_id: 笔记 ID
            evolve_type: 发芽类型 (spark|model|cross|habit|subconscious)
            context: 可选上下文
        
        Returns:
            发芽结果
        """
        if evolve_type == "spark":
            return self._generate_spark(note_id, context)
        elif evolve_type == "model":
            return self._generate_model(note_id, context)
        elif evolve_type == "cross":
            return self._generate_cross(note_id, context)
        elif evolve_type == "habit":
            return self._generate_habit(note_id, context)
        elif evolve_type == "subconscious":
            return self._generate_subconscious(note_id, context)
        else:
            raise ValueError(f"不支持的发芽类型：{evolve_type}")
    
    def _generate_spark(self, note_id: str, context: Optional[Dict] = None) -> Dict:
        """生成灵光闪现"""
        evolve_id = f"spark-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        content = f"""---
type: 灵光闪现
source_note: [[{note_id}]]
tags: [#知识发芽，#灵光闪现]
created: {datetime.now().isoformat()}
---

# 💡 灵光闪现

**触发笔记**：[[{note_id}]]

## 💡 核心洞察

> （待 AI 生成核心洞察）

## 🔗 洞察链条

1. 表面问题 → ...
2. 深层原因 → ...
3. 本质规律 → ...

## 🔀 跨界联想

- 领域 A：...
- 领域 B：...

## 📤 未来产出

- [ ] 公众号文章片段
- [ ] 周报洞察
"""
        
        output_file = self.output_path / f"{evolve_id}.md"
        output_file.write_text(content)
        
        return {
            "evolve_id": evolve_id,
            "evolve_type": "spark",
            "content": content,
            "output_path": str(output_file),
            "status": "evolved",
            "created_at": datetime.now().isoformat()
        }
    
    def _generate_model(self, note_id: str, context: Optional[Dict] = None) -> Dict:
        """生成心智模型解读"""
        evolve_id = f"model-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        # 类似 spark 的实现
        return {"evolve_id": evolve_id, "evolve_type": "model", "status": "evolved"}
    
    def _generate_cross(self, note_id: str, context: Optional[Dict] = None) -> Dict:
        """生成跨界视角"""
        evolve_id = f"cross-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        return {"evolve_id": evolve_id, "evolve_type": "cross", "status": "evolved"}
    
    def _generate_habit(self, note_id: str, context: Optional[Dict] = None) -> Dict:
        """生成微习惯"""
        evolve_id = f"habit-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        return {"evolve_id": evolve_id, "evolve_type": "habit", "status": "evolved"}
    
    def _generate_subconscious(self, note_id: str, context: Optional[Dict] = None) -> Dict:
        """生成潜意识调整"""
        evolve_id = f"subcon-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        return {"evolve_id": evolve_id, "evolve_type": "subconscious", "status": "evolved"}
