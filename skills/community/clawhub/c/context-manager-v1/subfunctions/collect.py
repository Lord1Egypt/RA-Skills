#!/usr/bin/env python3
"""
Collect Function - 收集功能

从各种来源收集知识，统一转成 Markdown 格式
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any


class CollectFunction:
    """收集功能实现"""
    
    def __init__(self, config: dict):
        self.config = config
        self.base_path = Path(config.get("base_path", "~/kb")).expanduser()
        self.inbox_path = self.base_path / "00-Inbox"
        self.inbox_path.mkdir(parents=True, exist_ok=True)
    
    def execute(self, 
                source_type: str, 
                content: str, 
                metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        执行收集功能
        
        Args:
            source_type: 来源类型 (feishu|wechat|url|text)
            content: 内容 (doc_token|URL|文本)
            metadata: 可选元数据
        
        Returns:
            收集结果
        """
        if source_type == "feishu":
            return self._collect_feishu(content, metadata)
        elif source_type == "wechat":
            return self._collect_wechat(content, metadata)
        elif source_type == "url":
            return self._collect_url(content, metadata)
        elif source_type == "text":
            return self._collect_text(content, metadata)
        else:
            raise ValueError(f"不支持的来源类型：{source_type}")
    
    def _collect_feishu(self, doc_token: str, metadata: Optional[Dict] = None) -> Dict:
        """从飞书文档收集"""
        # TODO: 调用飞书 API 读取文档
        # doc_content = feishu_doc(action="read", doc_token=doc_token)
        
        note_id = f"note-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        title = metadata.get("title", f"飞书文档 - {doc_token}") if metadata else f"飞书文档 - {doc_token}"
        
        note_content = f"""---
title: {title}
source: 飞书文档
source_url: https://my.feishu.cn/docx/{doc_token}
tags: [飞书，同步]
created_at: {datetime.now().isoformat()}
---

# {title}

> 本文档从飞书同步而来

---

（待从飞书 API 获取实际内容）

---

## 📤 可以发展成
- [ ] 公众号文章
- [ ] 周报内容
- [ ] 深度报告
- [ ] 只是存档
"""
        
        # 保存到 Inbox
        note_path = self.inbox_path / f"{note_id}.md"
        note_path.write_text(note_content)
        
        return {
            "note_id": note_id,
            "title": title,
            "content": note_content,
            "source": f"feishu:{doc_token}",
            "created_at": datetime.now().isoformat(),
            "status": "collected",
            "path": str(note_path)
        }
    
    def _collect_wechat(self, export_text: str, metadata: Optional[Dict] = None) -> Dict:
        """从微信读书导出收集"""
        import re
        
        # 解析书名
        book_title = metadata.get("title", "未命名书籍")
        if not book_title:
            match = re.search(r'书名：《(.+?)》', export_text)
            book_title = match.group(1) if match else "未命名书籍"
        
        note_id = f"note-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        title = f"📖 {book_title}"
        
        note_content = f"""---
title: {title}
author: {metadata.get('author', '未知')}
tags: [#读书，#笔记，#书/{book_title}]
source: 微信读书
exported_at: {datetime.now().isoformat()}
---

# {title}

**作者**：{metadata.get('author', '未知')}

---

## 📝 划线摘录
（待解析微信读书导出内容）

---

## 🧠 我的思考

### 核心洞察
TODO: 读完后的核心收获是什么？

### 与我现有知识的连接
TODO: 和哪些已有笔记可以建立 [[双链]]？

### 可以应用的地方
TODO: 可以用在什么场景？#场景/?

### 行动建议
TODO: 下一步行动是什么？#行动/?
"""
        
        note_path = self.inbox_path / f"{note_id}.md"
        note_path.write_text(note_content)
        
        return {
            "note_id": note_id,
            "title": title,
            "content": note_content,
            "source": "wechat",
            "created_at": datetime.now().isoformat(),
            "status": "collected",
            "path": str(note_path)
        }
    
    def _collect_url(self, url: str, metadata: Optional[Dict] = None) -> Dict:
        """从 URL 收集"""
        # TODO: 调用 url-to-markdown 脚本
        # markdown = url_to_markdown(url)
        
        note_id = f"note-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        title = metadata.get("title", f"网页 - {url}")
        
        note_content = f"""---
title: {title}
source: 网页
source_url: {url}
tags: [网页，同步]
created_at: {datetime.now().isoformat()}
---

# {title}

> 从网页抓取而来

（待从 URL 抓取实际内容）
"""
        
        note_path = self.inbox_path / f"{note_id}.md"
        note_path.write_text(note_content)
        
        return {
            "note_id": note_id,
            "title": title,
            "content": note_content,
            "source": f"url:{url}",
            "created_at": datetime.now().isoformat(),
            "status": "collected",
            "path": str(note_path)
        }
    
    def _collect_text(self, text: str, metadata: Optional[Dict] = None) -> Dict:
        """从纯文本收集"""
        note_id = f"note-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        title = metadata.get("title", f"笔记 - {note_id}")
        
        note_content = f"""---
title: {title}
source: 手动输入
tags: [笔记]
created_at: {datetime.now().isoformat()}
---

{text}
"""
        
        note_path = self.inbox_path / f"{note_id}.md"
        note_path.write_text(note_content)
        
        return {
            "note_id": note_id,
            "title": title,
            "content": note_content,
            "source": "text",
            "created_at": datetime.now().isoformat(),
            "status": "collected",
            "path": str(note_path)
        }
