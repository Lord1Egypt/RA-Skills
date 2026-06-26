#!/usr/bin/env python3
"""
复盘内容处理器
用于处理、提取和格式化复盘内容
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Optional

class ReviewProcessor:
    """复盘内容处理器"""
    
    # 需要过滤的语气助词
    FILLER_WORDS = ['噢', '哦', '啊', '额', '嗯', '呀', '啦', '嘛', '呢', '哈', '呃', '唉']
    
    def __init__(self):
        self.current_date = datetime.now().strftime('%Y-%m-%d')
        self.current_time = datetime.now().strftime('%H:%M')
    
    def process_text(self, text: str) -> Dict:
        """处理复盘文字内容"""
        
        # 1. 过滤语气助词
        cleaned_text = self._remove_fillers(text)
        
        # 2. 提取主题
        topic = self._extract_topic(cleaned_text)
        
        # 3. 提取亮点
        highlights = self._extract_highlights(cleaned_text)
        
        # 4. 判断心情
        mood = self._detect_mood(cleaned_text)
        
        return {
            'date': self.current_date,
            'time': self.current_time,
            'original_text': text,
            'cleaned_text': cleaned_text,
            'topic': topic,
            'highlights': highlights,
            'mood': mood
        }
    
    def _remove_fillers(self, text: str) -> str:
        """过滤语气助词"""
        result = text
        for word in self.FILLER_WORDS:
            result = result.replace(word, '')
        # 清理多余空白
        result = re.sub(r'\s+', ' ', result).strip()
        return result
    
    def _extract_topic(self, text: str) -> str:
        """提取主题（一句话概括）"""
        # 简单实现：取前20个字作为主题
        # 实际可用 NLP 模型改进
        if len(text) <= 20:
            return text
        return text[:20] + '...'
    
    def _extract_highlights(self, text: str) -> List[str]:
        """提取亮点"""
        # 简单实现：按句号分割，取前3句
        sentences = [s.strip() for s in text.split('。') if s.strip()]
        highlights = sentences[:3]
        
        # 如果句子太长，进一步截断
        return [s[:50] + '...' if len(s) > 50 else s for s in highlights]
    
    def _detect_mood(self, text: str) -> str:
        """检测心情"""
        text_lower = text.lower()
        
        # 关键词匹配
        positive_words = ['开心', '爽', '高兴', '激动', '期待', '成长', '完成', '突破']
        negative_words = ['焦虑', '困惑', '疲惫', '烦恼', '困难', '失败']
        
        positive_count = sum(1 for w in positive_words if w in text)
        negative_count = sum(1 for w in negative_words if w in text)
        
        if positive_count > negative_count:
            return '😊 正面'
        elif negative_count > positive_count:
            return '😟 需要调整'
        else:
            return '😐 中性'
    
    def format_as_markdown(self, data: Dict) -> str:
        """格式化为 Markdown"""
        md = f"""## {data['date']}

### 记录时间
{data['time']}

### 记录内容
{data['cleaned_text']}

### 主题
{data['topic']}

### 内容亮点
"""
        for i, h in enumerate(data['highlights'], 1):
            md += f"{i}. {h}\n"
        
        md += f"\n### 心情\n{data['mood']}\n"
        
        return md
    
    def save_to_file(self, data: Dict, filepath: str):
        """保存到文件"""
        content = self.format_as_markdown(data)
        
        # 追加到文件
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write('\n---\n\n')
            f.write(content)


def main():
    """测试用"""
    processor = ReviewProcessor()
    
    # 测试输入
    test_text = "今天最大的感悟是终于把那个拖延很久的项目搞完了，爽！然后还有就是发现早上跑步的时候思维特别清晰，以后可以多利用这个时间思考问题。"
    
    result = processor.process_text(test_text)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    print('\n--- Markdown 输出 ---\n')
    print(processor.format_as_markdown(result))


if __name__ == '__main__':
    main()
