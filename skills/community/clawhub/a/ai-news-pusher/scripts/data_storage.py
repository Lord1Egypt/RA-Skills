#!/usr/bin/env python3
"""
数据持久化模块 - 存储待阅池、标记数据和反馈
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional


class DataStorage:
    """数据存储管理器"""
    
    def __init__(self, data_dir: Optional[str] = None):
        """
        初始化数据存储
        
        Args:
            data_dir: 数据存储目录，默认为项目根目录下的 data 文件夹
        """
        if data_dir is None:
            script_dir = Path(__file__).parent.absolute()
            data_dir = str(script_dir.parent / 'data')
        
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.gray_zone_file = self.data_dir / 'gray_zone.json'
        self.feedback_file = self.data_dir / 'feedback.json'
        self.filtered_file = self.data_dir / 'filtered.json'
        self.pushed_file = self.data_dir / 'pushed.json'
        self.config_file = self.data_dir / 'config.json'
        
        self._init_files()
    
    def _init_files(self):
        """初始化数据文件"""
        for file_path in [self.gray_zone_file, self.feedback_file, 
                         self.filtered_file, self.pushed_file]:
            if not file_path.exists():
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump([], f)
        
        if not self.config_file.exists():
            default_config = {
                'auto_push_threshold': 80,
                'gray_zone_min': 60,
                'gray_zone_max': 80,
                'created_at': datetime.now().isoformat()
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, ensure_ascii=False, indent=2)
    
    def _load_json(self, file_path: Path) -> List[Dict]:
        """加载JSON文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def _save_json(self, file_path: Path, data: List[Dict]):
        """保存JSON文件"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _get_news_id(self, news: Dict) -> str:
        """获取新闻唯一ID（使用URL）"""
        return news.get('url', '') or f"{news.get('title', '')}_{news.get('source', '')}"
    
    def save_to_gray_zone(self, news: Dict):
        """
        保存新闻到待阅池
        
        Args:
            news: 新闻字典（已评分）
        """
        gray_zone = self._load_json(self.gray_zone_file)
        
        news_id = self._get_news_id(news)
        existing = next((n for n in gray_zone if self._get_news_id(n) == news_id), None)
        
        if not existing:
            news['saved_at'] = datetime.now().isoformat()
            news['reviewed'] = False
            gray_zone.append(news)
            self._save_json(self.gray_zone_file, gray_zone)
    
    def batch_save_gray_zone(self, news_list: List[Dict]):
        """批量保存到待阅池"""
        for news in news_list:
            self.save_to_gray_zone(news)
    
    def get_gray_zone(self, limit: Optional[int] = None, only_unreviewed: bool = True) -> List[Dict]:
        """
        获取待阅池新闻
        
        Args:
            limit: 限制返回数量
            only_unreviewed: 只返回未审核的
        
        Returns:
            新闻列表
        """
        gray_zone = self._load_json(self.gray_zone_file)
        
        if only_unreviewed:
            gray_zone = [n for n in gray_zone if not n.get('reviewed', False)]
        
        gray_zone.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        if limit:
            gray_zone = gray_zone[:limit]
        
        return gray_zone
    
    def review_gray_zone_news(self, news_id: str, action: str, manual_score: Optional[int] = None, 
                              notes: str = "") -> bool:
        """
        审核待阅池新闻
        
        Args:
            news_id: 新闻ID
            action: 操作类型 (approve, reject, escalate)
            manual_score: 人工评分
            notes: 备注
        
        Returns:
            是否成功
        """
        gray_zone = self._load_json(self.gray_zone_file)
        
        news_index = None
        for i, news in enumerate(gray_zone):
            if self._get_news_id(news) == news_id:
                news_index = i
                break
        
        if news_index is None:
            return False
        
        news = gray_zone.pop(news_index)
        news['reviewed'] = True
        news['review_action'] = action
        news['reviewed_at'] = datetime.now().isoformat()
        news['manual_score'] = manual_score
        news['review_notes'] = notes
        
        if action == 'approve':
            self._append_to_list(self.pushed_file, news)
            if manual_score is not None:
                self.save_feedback(news_id, news.get('score', 0), manual_score, notes)
        elif action == 'reject':
            self._append_to_list(self.filtered_file, news)
        elif action == 'escalate':
            news['score'] = manual_score if manual_score else news.get('score', 0) + 20
            self._append_to_list(self.pushed_file, news)
            if manual_score is not None:
                self.save_feedback(news_id, news.get('score', 0), manual_score, notes)
        
        self._save_json(self.gray_zone_file, gray_zone)
        return True
    
    def _append_to_list(self, file_path: Path, item: Dict):
        """向列表文件追加数据"""
        data = self._load_json(file_path)
        data.append(item)
        self._save_json(file_path, data)
    
    def save_feedback(self, news_id: str, original_score: int, manual_score: int, notes: str = ""):
        """保存反馈数据"""
        feedback = self._load_json(self.feedback_file)
        feedback.append({
            'news_id': news_id,
            'original_score': original_score,
            'manual_score': manual_score,
            'notes': notes,
            'timestamp': datetime.now().isoformat()
        })
        self._save_json(self.feedback_file, feedback)
    
    def get_feedback(self, limit: Optional[int] = None) -> List[Dict]:
        """获取反馈数据"""
        feedback = self._load_json(self.feedback_file)
        feedback.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        if limit:
            feedback = feedback[:limit]
        return feedback
    
    def save_filtered(self, news_list: List[Dict]):
        """保存被过滤的新闻"""
        for news in news_list:
            news['filtered_at'] = datetime.now().isoformat()
            self._append_to_list(self.filtered_file, news)
    
    def get_filtered(self, days: int = 7, limit: Optional[int] = None) -> List[Dict]:
        """获取被过滤的新闻（用于抽检）"""
        filtered = self._load_json(self.filtered_file)
        
        cutoff_date = datetime.now() - datetime.timedelta(days=days)
        recent_filtered = [
            n for n in filtered 
            if datetime.fromisoformat(n.get('filtered_at', '2000-01-01')) > cutoff_date
        ]
        
        recent_filtered.sort(key=lambda x: x.get('filtered_at', ''), reverse=True)
        
        if limit:
            recent_filtered = recent_filtered[:limit]
        
        return recent_filtered
    
    def save_pushed(self, news_list: List[Dict]):
        """保存已推送的新闻"""
        for news in news_list:
            news['pushed_at'] = datetime.now().isoformat()
            self._append_to_list(self.pushed_file, news)
    
    def get_pushed(self, days: int = 7, limit: Optional[int] = None) -> List[Dict]:
        """获取已推送的新闻"""
        pushed = self._load_json(self.pushed_file)
        
        cutoff_date = datetime.now() - datetime.timedelta(days=days)
        recent_pushed = [
            n for n in pushed 
            if datetime.fromisoformat(n.get('pushed_at', '2000-01-01')) > cutoff_date
        ]
        
        recent_pushed.sort(key=lambda x: x.get('pushed_at', ''), reverse=True)
        
        if limit:
            recent_pushed = recent_pushed[:limit]
        
        return recent_pushed
    
    def get_stats(self) -> Dict:
        """获取统计数据"""
        return {
            'gray_zone_count': len(self._load_json(self.gray_zone_file)),
            'pushed_count': len(self._load_json(self.pushed_file)),
            'filtered_count': len(self._load_json(self.filtered_file)),
            'feedback_count': len(self._load_json(self.feedback_file))
        }
    
    def get_config(self) -> Dict:
        """获取配置"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def update_config(self, config_updates: Dict):
        """更新配置"""
        config = self.get_config()
        config.update(config_updates)
        config['updated_at'] = datetime.now().isoformat()
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    
    def clear_old_data(self, days: int = 30):
        """清理旧数据"""
        cutoff_date = datetime.now() - datetime.timedelta(days=days)
        
        for file_path in [self.pushed_file, self.filtered_file]:
            data = self._load_json(file_path)
            date_field = 'pushed_at' if file_path == self.pushed_file else 'filtered_at'
            
            filtered_data = [
                item for item in data
                if datetime.fromisoformat(item.get(date_field, '2000-01-01')) > cutoff_date
            ]
            
            self._save_json(file_path, filtered_data)
