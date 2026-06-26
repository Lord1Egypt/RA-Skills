#!/usr/bin/env python3
"""
ClawValue 日志解析模块
解析 OpenClaw 的日志文件、技能目录和配置文件
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


class LogParser:
    """OpenClaw 日志解析器"""
    
    # OpenClaw 日志路径（按官方文档）
    OPENCLAW_LOG_DIR = '/tmp/openclaw'
    
    def __init__(self, openclaw_home: str = None):
        if openclaw_home is None:
            openclaw_home = str(Path.home() / '.openclaw')
        self.openclaw_home = openclaw_home
        self.logs_dir = self.OPENCLAW_LOG_DIR
    
    def parse_jsonl_file(self, filepath: str) -> List[dict]:
        """解析 JSONL 日志文件（OpenClaw 官方格式）"""
        results = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        # 解析 OpenClaw 日志格式
                        parsed = self._parse_openclaw_log(data)
                        if parsed:
                            results.append(parsed)
                    except json.JSONDecodeError:
                        continue
        except FileNotFoundError:
            pass
        return results
    
    def _parse_openclaw_log(self, data: dict) -> Optional[dict]:
        """解析 OpenClaw 日志条目格式"""
        try:
            # OpenClaw 日志格式: {"0": "message", "_meta": {...}, "time": "..."}
            message = data.get('0', '') or data.get('message', '')
            meta = data.get('_meta', {})
            
            return {
                'message': message,
                'level': meta.get('logLevelName', 'INFO'),
                'timestamp': data.get('time', ''),
                'subsystem': self._extract_subsystem(message),
                'type': self._classify_log(message),
                'raw': data
            }
        except Exception:
            return None
    
    def _extract_subsystem(self, message: str) -> str:
        """从消息中提取子系统"""
        if message.startswith('['):
            end = message.find(']')
            if end > 0:
                return message[1:end]
        return 'unknown'
    
    def _classify_log(self, message: str) -> str:
        """分类日志消息"""
        msg_lower = message.lower()
        
        # 过滤掉非关键错误
        if 'error' in msg_lower or 'failed' in msg_lower:
            # 这些不是真正的错误
            if any(x in msg_lower for x in ['enoent', 'eisdir', 'deprecation', 'punycode', 'todo.md']):
                return 'noise'
            return 'error'
        elif 'session' in msg_lower:
            return 'session'
        elif 'tool' in msg_lower or 'skill' in msg_lower:
            return 'tool'
        elif 'model' in msg_lower or 'token' in msg_lower or 'llm' in msg_lower:
            return 'model'
        elif 'webhook' in msg_lower or 'message' in msg_lower:
            return 'message'
        else:
            return 'other'
    
    def parse_text_log(self, filepath: str) -> List[dict]:
        """解析文本格式的日志文件（gateway.log 等）"""
        results = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # 解析日志格式: 2026-03-07T14:15:22.112Z [gateway] message
                    try:
                        if line.startswith('20'):
                            parts = line.split(' ', 2)
                            if len(parts) >= 3:
                                timestamp = parts[0]
                                source = parts[1].strip('[]')
                                message = parts[2] if len(parts) > 2 else ''
                                
                                log_entry = {
                                    'message': message,
                                    'level': 'INFO',
                                    'timestamp': timestamp,
                                    'subsystem': source,
                                    'type': self._classify_log(message)
                                }
                                results.append(log_entry)
                    except Exception:
                        continue
        except FileNotFoundError:
            pass
        return results
    
    def get_all_logs(self) -> List[dict]:
        """获取所有日志"""
        all_logs = []
        
        # 优先读取 /tmp/openclaw/ 目录（官方日志位置）
        if os.path.exists(self.OPENCLAW_LOG_DIR):
            for filename in os.listdir(self.OPENCLAW_LOG_DIR):
                if filename.endswith('.log') and filename.startswith('openclaw-'):
                    filepath = os.path.join(self.OPENCLAW_LOG_DIR, filename)
                    all_logs.extend(self.parse_jsonl_file(filepath))
        
        # 兼容旧路径
        old_logs_dir = os.path.join(self.openclaw_home, 'logs')
        if os.path.exists(old_logs_dir):
            for filename in os.listdir(old_logs_dir):
                filepath = os.path.join(old_logs_dir, filename)
                if filename.endswith('.jsonl'):
                    all_logs.extend(self.parse_jsonl_file(filepath))
                elif filename.endswith('.log'):
                    all_logs.extend(self.parse_text_log(filepath))
        
        return all_logs
    
    def extract_session_stats(self, logs: List[dict]) -> Dict:
        """从日志中提取会话统计"""
        stats = {
            'total_messages': 0,
            'total_tokens': 0,
            'tool_calls': 0,
            'errors': 0,
            'connections': 0,
            'log_entries': 0,
            'model_calls': 0,
            'info_count': 0,
            'warn_count': 0,
            'error_count': 0,
            'session_count': 0  # 真实会话数
        }
        
        session_ids = set()  # 用于去重会话
        
        for log in logs:
            stats['log_entries'] += 1
            
            # 统计日志级别
            level = log.get('level', 'INFO')
            if level == 'ERROR':
                stats['error_count'] += 1
            elif level == 'WARN':
                stats['warn_count'] += 1
            else:
                stats['info_count'] += 1
            
            # 按类型统计
            log_type = log.get('type', 'other')
            if log_type == 'error':
                stats['errors'] += 1
            elif log_type == 'tool':
                stats['tool_calls'] += 1
            elif log_type == 'model':
                stats['model_calls'] += 1
            elif log_type == 'connection':
                stats['connections'] += 1
            elif log_type == 'session':
                stats['session_count'] += 1
            
            # 从原始数据中提取更多信息
            raw = log.get('raw', {})
            if raw:
                # 提取 token 使用信息
                msg = str(raw.get('0', ''))
                # 匹配 token 使用模式
                import re
                token_match = re.search(r'(\d+)\s*tokens?', msg, re.IGNORECASE)
                if token_match:
                    stats['total_tokens'] += int(token_match.group(1))
                
                # 提取会话 ID
                if 'session' in msg.lower():
                    sid_match = re.search(r'session[=:\s]*([a-zA-Z0-9-]+)', msg, re.IGNORECASE)
                    if sid_match:
                        session_ids.add(sid_match.group(1))
        
        # 如果没有从日志中提取到会话数，使用估算
        if stats['session_count'] == 0:
            # 根据工具调用和模型调用估算活跃会话
            stats['session_count'] = max(1, (stats['tool_calls'] + stats['model_calls']) // 10)
        
        # 加上从消息中提取的会话数
        stats['session_count'] = max(stats['session_count'], len(session_ids))
        
        # 清理不能序列化的字段
        if 'sessions' in stats:
            del stats['sessions']
        
        return stats


class SkillScanner:
    """OpenClaw 技能扫描器"""
    
    def __init__(self, workspace: str = None):
        if workspace is None:
            workspace = str(Path.home() / '.openclaw' / 'workspace')
        self.workspace = workspace
        self.skills_dir = os.path.join(workspace, 'skills')
    
    def parse_skill_md(self, filepath: str) -> Optional[dict]:
        """解析 SKILL.md 文件"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析 YAML frontmatter
            metadata = {}
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    yaml_content = parts[1].strip()
                    # 简单解析 YAML（不用 PyYAML）
                    for line in yaml_content.split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            metadata[key] = value
            
            # 解析 metadata.clawdbot 部分（如果有）
            clawdbot = {}
            if 'metadata:' in content and 'clawdbot:' in content:
                # 提取 clawdbot 配置
                try:
                    # 尝试解析 JSON 格式的 metadata
                    json_match = re.search(r'metadata:\s*(\{.*?\})', content, re.DOTALL)
                    if json_match:
                        metadata_json = json.loads(json_match.group(1))
                        clawdbot = metadata_json.get('clawdbot', {})
                except:
                    pass
            
            return {
                'name': metadata.get('name', os.path.basename(os.path.dirname(filepath))),
                'description': metadata.get('description', ''),
                'version': metadata.get('version', '1.0.0'),
                'author': metadata.get('author', ''),
                'is_custom': True,  # 自定义技能
                'is_high_risk': 'voice-call' in metadata.get('name', '') or 
                               '1password' in metadata.get('name', ''),
                'category': self._guess_category(metadata.get('description', '')),
                'filepath': filepath
            }
        except FileNotFoundError:
            return None
    
    def _guess_category(self, description: str) -> str:
        """根据描述猜测技能类别"""
        desc_lower = description.lower()
        
        if any(kw in desc_lower for kw in ['搜索', 'search', '查询', 'web']):
            return 'Search & Research'
        elif any(kw in desc_lower for kw in ['devops', '部署', 'ci/cd', 'docker']):
            return 'DevOps & Cloud'
        elif any(kw in desc_lower for kw in ['mcp', '工具', 'tool']):
            return 'Tools & Utilities'
        elif any(kw in desc_lower for kw in ['消息', 'message', '通知', 'notify']):
            return 'Communication'
        elif any(kw in desc_lower for kw in ['数据库', 'database', 'sql', '存储']):
            return 'Data & Storage'
        elif any(kw in desc_lower for kw in ['媒体', 'media', '图片', 'image', '视频']):
            return 'Media & Content'
        else:
            return 'Other'
    
    def scan_all_skills(self) -> List[dict]:
        """扫描所有技能"""
        skills = []
        
        if not os.path.exists(self.skills_dir):
            return skills
        
        for skill_name in os.listdir(self.skills_dir):
            skill_path = os.path.join(self.skills_dir, skill_name)
            if not os.path.isdir(skill_path):
                continue
            
            skill_md = os.path.join(skill_path, 'SKILL.md')
            if os.path.exists(skill_md):
                skill_data = self.parse_skill_md(skill_md)
                if skill_data:
                    skills.append(skill_data)
        
        return skills


class ConfigAnalyzer:
    """OpenClaw 配置分析器"""
    
    def __init__(self, openclaw_home: str = None):
        if openclaw_home is None:
            openclaw_home = str(Path.home() / '.openclaw')
        self.openclaw_home = openclaw_home
        self.config_file = os.path.join(openclaw_home, 'openclaw.json')
    
    def parse_config(self) -> Optional[dict]:
        """解析 openclaw.json 配置文件"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                # JSON5 支持（简单处理注释）
                content = f.read()
                # 移除单行注释
                content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
                # 移除多行注释
                content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
                
                config = json.loads(content)
                return self._extract_key_info(config)
        except FileNotFoundError:
            return None
        except json.JSONDecodeError:
            return None
    
    def _extract_key_info(self, config: dict) -> dict:
        """提取关键配置信息"""
        agents_config = config.get('agents', {})
        defaults = agents_config.get('defaults', {})
        
        return {
            'primary_model': defaults.get('model', {}).get('primary', 'unknown'),
            'heartbeat_interval': defaults.get('heartbeat', {}).get('every', 0),
            'sandbox_enabled': config.get('sandbox', {}).get('enabled', False),
            'tools_profile': config.get('tools', {}).get('profile', 'default'),
            'agent_count': len(agents_config.get('instances', [])) or 1,
            'channels': list(config.get('channels', {}).keys()),
            'subagents_config': defaults.get('subagents', {})
        }


class DataCollector:
    """数据采集器 - 整合所有数据源"""
    
    def __init__(self, openclaw_home: str = None, workspace: str = None):
        self.log_parser = LogParser(openclaw_home)
        self.skill_scanner = SkillScanner(workspace)
        self.config_analyzer = ConfigAnalyzer(openclaw_home)
    
    def collect_all(self) -> dict:
        """采集所有数据"""
        # 解析日志
        logs = self.log_parser.get_all_logs()
        session_stats = self.log_parser.extract_session_stats(logs)
        
        # 扫描技能
        skills = self.skill_scanner.scan_all_skills()
        
        # 解析配置
        config = self.config_analyzer.parse_config()
        
        # 计算使用天数（基于最早的会话）
        usage_days = 1
        
        return {
            'collected_at': datetime.now().isoformat(),
            'sessions': session_stats,
            'skills': skills,
            'config': config,
            'usage_days': usage_days,
            'total_sessions': session_stats.get('session_count', 0),
            'total_skills': len(skills),
            'total_tokens': session_stats.get('total_tokens', 0),
            'total_messages': session_stats.get('total_messages', 0),
            'tool_calls': session_stats.get('tool_calls', 0),
            'errors': session_stats.get('errors', 0)
        }


if __name__ == '__main__':
    # 测试数据采集
    collector = DataCollector()
    data = collector.collect_all()
    
    print("📊 采集结果:")
    print(f"  - 技能数量: {data['total_skills']}")
    print(f"  - 会话数量: {data['total_sessions']}")
    print(f"  - Token 消耗: {data['total_tokens']}")
    print(f"  - 消息总数: {data['total_messages']}")
    print(f"  - 工具调用: {data['tool_calls']}")
    
    if data['config']:
        print(f"  - 主模型: {data['config'].get('primary_model', 'unknown')}")
        print(f"  - Agent 数量: {data['config'].get('agent_count', 1)}")
    
    if data['skills']:
        print(f"\n📋 技能列表:")
        for skill in data['skills'][:10]:
            print(f"  - {skill['name']}: {skill['description'][:50]}...")