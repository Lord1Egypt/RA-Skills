"""
SEO优化模块 - 自动优化文章SEO
"""

import re
from collections import Counter


class SEOOptimizer:
    """SEO优化器"""
    
    def optimize(self, article_data):
        """优化文章SEO"""
        # 生成meta description
        meta_desc = self._generate_meta_description(article_data)
        
        # 提取关键词
        keywords = self._extract_keywords(article_data)
        
        # 优化标题
        optimized_title = self._optimize_title(article_data['title'])
        
        # 更新文章数据
        article_data['meta_description'] = meta_desc
        article_data['keywords'] = keywords
        article_data['optimized_title'] = optimized_title
        
        return article_data
    
    def _generate_meta_description(self, article_data):
        """生成meta description（160字符以内）"""
        body = article_data['body']
        
        # 移除markdown标记
        text = re.sub(r'[#*`\[\]\(\)]', '', body)
        text = re.sub(r'\s+', ' ', text).strip()
        
        # 取前160字符
        desc = text[:157] + '...' if len(text) > 160 else text
        
        return desc
    
    def _extract_keywords(self, article_data, top_n=5):
        """提取关键词"""
        text = article_data['title'] + ' ' + article_data['body']
        
        # 移除markdown和标点
        text = re.sub(r'[#*`\[\]\(\)\n]', ' ', text)
        text = re.sub(r'[^\w\u4e00-\u9fff\s]', '', text)
        
        # 分词（简单实现）
        words = text.lower().split()
        
        # 过滤停用词
        stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', '的', '了', '在', '是'}
        words = [w for w in words if w not in stop_words and len(w) > 1]
        
        # 统计词频
        word_counts = Counter(words)
        
        # 返回top_n关键词
        return [word for word, count in word_counts.most_common(top_n)]
    
    def _optimize_title(self, title):
        """优化标题"""
        # 确保标题长度在30-60字符之间
        if len(title) < 30:
            # 标题太短，添加修饰词
            return f"{title} - 完整指南与实战"
        elif len(title) > 60:
            # 标题太长，截断
            return title[:57] + '...'
        
        return title
    
    def generate_open_graph(self, article_data):
        """生成Open Graph标签"""
        return {
            'og:title': article_data.get('optimized_title', article_data['title']),
            'og:description': article_data.get('meta_description', ''),
            'og:type': 'article',
            'og:image': article_data.get('cover_image', ''),
        }
