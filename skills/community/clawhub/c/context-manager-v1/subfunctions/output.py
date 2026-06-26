#!/usr/bin/env python3
"""
Output Function - 产出功能

将发芽内容变成可发布的内容（文章/周报/月报）
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional


class OutputFunction:
    """产出功能实现"""
    
    def __init__(self, config: dict):
        self.config = config
        self.base_path = Path(config.get("base_path", "~/kb")).expanduser()
        self.output_path = self.base_path / "outputs" / "reports"
        self.output_path.mkdir(parents=True, exist_ok=True)
    
    def execute(self, 
                evolve_id: str, 
                output_type: str = "article",
                style: Optional[Dict] = None) -> Dict[str, Any]:
        """
        执行产出功能
        
        Args:
            evolve_id: 发芽内容 ID
            output_type: 产出类型 (article|weekly|monthly)
            style: 可选样式配置
        
        Returns:
            产出结果
        """
        if output_type == "article":
            return self._generate_article(evolve_id, style)
        elif output_type == "weekly":
            return self._generate_weekly(evolve_id, style)
        elif output_type == "monthly":
            return self._generate_monthly(evolve_id, style)
        else:
            raise ValueError(f"不支持的产出类型：{output_type}")
    
    def _generate_article(self, evolve_id: str, style: Optional[Dict] = None) -> Dict:
        """生成公众号文章"""
        output_id = f"article-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        content = f"""# 文章标题

> 基于知识发芽内容生成

---

## 问题

（待 AI 生成）

## 探索

（待 AI 生成）

## 方案

（待 AI 生成）

## 行动

（待 AI 生成）

---

## 📌 关于本文

本文是**燃冰**和**小蚂蚁**共同协作的产物。

一人 CEO，不是一个人干所有事。

是用工具和 AI，放大个人能力。

🔗
"""
        
        output_file = self.output_path / f"{output_id}.md"
        output_file.write_text(content)
        
        return {
            "output_id": output_id,
            "output_type": "article",
            "content": content,
            "output_path": str(output_file),
            "word_count": len(content),
            "status": "generated",
            "created_at": datetime.now().isoformat()
        }
    
    def _generate_weekly(self, evolve_id: str, style: Optional[Dict] = None) -> Dict:
        """生成周报"""
        output_id = f"weekly-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        return {"output_id": output_id, "output_type": "weekly", "status": "generated"}
    
    def _generate_monthly(self, evolve_id: str, style: Optional[Dict] = None) -> Dict:
        """生成月报"""
        output_id = f"monthly-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        return {"output_id": output_id, "output_type": "monthly", "status": "generated"}
