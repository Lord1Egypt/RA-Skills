"""
English Version - Translated for international release
Date: 2026-02-27
Translator: AetherClaw Night Market Intelligence
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 - AetherClawSkill v2.0
 context-optimizer 
2026214 16:20 GMT+8
AetherClaw
context-optimizer (3.431)
、、、
"""
import re
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from enum import Enum
class CompactionStrategy(Enum):
    """"""
    MERGE = "merge"          # 
    SUMMARIZE = "summarize"  # 
    EXTRACT = "extract"      # 
    AUTO = "auto"           # 
@dataclass
class CompactionResult:
    """"""
    success: bool
    original_content: str
    compacted_content: str
    strategy_used: CompactionStrategy
    compression_rate: float
    metadata: Dict[str, Any]
    error: str = None
class AutoCompactionSystem:
    """
     context-optimizer 
    1. 
    2. 
    3. 
    4. 
    """
    def __init__(self):
        self.strategies = {
            CompactionStrategy.MERGE: self._merge_strategy,
            CompactionStrategy.SUMMARIZE: self._summarize_strategy,
            CompactionStrategy.EXTRACT: self._extract_strategy
        }
        # 
        self.config = {
            'max_summary_length': 300,
            'min_similarity_threshold': 0.7,
            'key_point_count': 5,
            'merge_window_size': 3
        }
        # 
        self.stats = {
            'total_compactions': 0,
            'successful_compactions': 0,
            'strategy_usage': {strategy.value: 0 for strategy in CompactionStrategy},
            'total_bytes_saved': 0,
            'avg_compression_rate': 0.0
        }
        print("⚡ AutoCompactionSystem ")
        print("   : 、、、")
    def compact_content(self, content: str, strategy: CompactionStrategy = CompactionStrategy.AUTO) -> CompactionResult:
        """
            content: 
            strategy: 
            CompactionResult 
        """
        self.stats['total_compactions'] += 1
        try:
            # 
            if strategy == CompactionStrategy.AUTO:
                strategy = self._select_best_strategy(content)
            # 
            compacted_content, metadata = self.strategies[strategy](content)
            # 
            original_size = len(content.encode('utf-8'))
            compacted_size = len(compacted_content.encode('utf-8'))
            if original_size == 0:
                compression_rate = 0.0
            else:
                compression_rate = 100 - (compacted_size * 100 / original_size)
            # 
            self.stats['successful_compactions'] += 1
            self.stats['strategy_usage'][strategy.value] += 1
            self.stats['total_bytes_saved'] += (original_size - compacted_size)
            self.stats['avg_compression_rate'] = (
                (self.stats['avg_compression_rate'] * (self.stats['successful_compactions'] - 1) + compression_rate) 
                / self.stats['successful_compactions']
            )
            return CompactionResult(
                success=True,
                original_content=content,
                compacted_content=compacted_content,
                strategy_used=strategy,
                compression_rate=compression_rate,
                metadata=metadata
            )
        except Exception as e:
            self.stats['strategy_usage']['error'] = self.stats['strategy_usage'].get('error', 0) + 1
            return CompactionResult(
                success=False,
                original_content=content,
                compacted_content=content,
                strategy_used=strategy,
                compression_rate=0.0,
                metadata={'error': str(e)},
                error=f": {str(e)}"
            )
    def _select_best_strategy(self, content: str) -> CompactionStrategy:
        """"""
        content_length = len(content)
        lines = content.split('\n')
        line_count = len(lines)
        # 
        if content_length > 5000:
            # 
            return CompactionStrategy.SUMMARIZE
        elif line_count > 50:
            # 
            return CompactionStrategy.MERGE
        elif self._has_clear_structure(content):
            # 
            return CompactionStrategy.EXTRACT
        else:
            # 
            return CompactionStrategy.MERGE
    def _merge_strategy(self, content: str) -> Tuple[str, Dict[str, Any]]:
        """"""
        lines = content.split('\n')
        merged_lines = []
        metadata = {
            'original_lines': len(lines),
            'merged_lines': 0,
            'similarity_groups': 0
        }
        i = 0
        while i < len(lines):
            current_line = lines[i].strip()
            if not current_line:
                merged_lines.append('')
                i += 1
                continue
            # 
            similar_lines = [current_line]
            j = i + 1
            while j < len(lines) and j - i < self.config['merge_window_size']:
                next_line = lines[j].strip()
                if next_line and self._lines_are_similar(current_line, next_line):
                    similar_lines.append(next_line)
                    j += 1
                else:
                    break
            # 
            if len(similar_lines) > 1:
                merged_line = self._merge_similar_lines(similar_lines)
                merged_lines.append(merged_line)
                metadata['similarity_groups'] += 1
                i = j  # 
            else:
                merged_lines.append(current_line)
                i += 1
        merged_content = '\n'.join(merged_lines)
        metadata['merged_lines'] = len(merged_lines)
        return merged_content, metadata
    def _summarize_strategy(self, content: str) -> Tuple[str, Dict[str, Any]]:
        """"""
        metadata = {
            'summary_method': 'smart_extraction',
            'key_sections_found': 0,
            'important_points': []
        }
        # 
        important_parts = []
        # 1. 
        headings = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
        if headings:
            important_parts.extend(headings[:3])
            metadata['key_sections_found'] += len(headings[:3])
        # 2. 
        list_items = re.findall(r'^[-*]\s+(.+)$', content, re.MULTILINE)
        if list_items:
            important_parts.extend(list_items[:5])
            metadata['important_points'].extend(list_items[:5])
        # 3. 
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        if paragraphs:
            # 
            if len(paragraphs) >= 2:
                important_parts.append(paragraphs[0])
                important_parts.append(paragraphs[-1])
            else:
                important_parts.append(paragraphs[0])
        # 
        if important_parts:
            summary = '\n'.join(important_parts)
            if len(summary) > self.config['max_summary_length']:
                summary = summary[:self.config['max_summary_length']] + '...'
        else:
            # 
            summary = content[:self.config['max_summary_length']]
            if len(content) > self.config['max_summary_length']:
                summary += '...'
        metadata['summary_length'] = len(summary)
        return summary, metadata
    def _extract_strategy(self, content: str) -> Tuple[str, Dict[str, Any]]:
        """"""
        metadata = {
            'key_points_extracted': 0,
            'extraction_method': 'pattern_based'
        }
        key_points = []
        # 1. 
        number_patterns = [
            r'(\d+%)',  # 
            r'(\$\d+)',  # 
            r'(\d+\.\d+)',  # 
            r'(\d+/\d+)',  # 
        ]
        for pattern in number_patterns:
            matches = re.findall(pattern, content)
            if matches:
                key_points.extend(matches[:2])
        # 2. 
        important_phrases = re.findall(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b', content)
        if important_phrases:
            key_points.extend(important_phrases[:3])
        # 3. 
        emphasis_patterns = [
            r'\*\*(.+?)\*\*',  # 
            r'__(.+?)__',      # 
            r'`(.+?)`',        # 
        ]
        for pattern in emphasis_patterns:
            matches = re.findall(pattern, content)
            if matches:
                key_points.extend(matches[:2])
        # 
        unique_points = []
        seen = set()
        for point in key_points:
            if point not in seen and len(point) > 3:  # 
                seen.add(point)
                unique_points.append(point)
        key_points = unique_points[:self.config['key_point_count']]
        metadata['key_points_extracted'] = len(key_points)
        # 
        if key_points:
            extracted_content = ":\n" + "\n".join(f"• {point}" for point in key_points)
        else:
            extracted_content = ""
        return extracted_content, metadata
    def _lines_are_similar(self, line1: str, line2: str) -> bool:
        """"""
        # 
        words1 = set(line1.lower().split())
        words2 = set(line2.lower().split())
        if not words1 or not words2:
            return False
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        similarity = len(intersection) / len(union)
        return similarity >= self.config['min_similarity_threshold']
    def _merge_similar_lines(self, lines: List[str]) -> str:
        """"""
        if not lines:
            return ""
        # 
        return max(lines, key=len)
    def _has_clear_structure(self, content: str) -> bool:
        """"""
        # 
        has_headings = bool(re.search(r'^#+\s+', content, re.MULTILINE))
        # 
        has_lists = bool(re.search(r'^[-*]\s+', content, re.MULTILINE))
        # 
        has_code_blocks = bool(re.search(r'```', content))
        # 
        paragraphs = [p for p in content.split('\n\n') if p.strip()]
        has_multiple_paragraphs = len(paragraphs) >= 3
        return has_headings or has_lists or has_code_blocks or has_multiple_paragraphs
    def get_statistics(self) -> Dict[str, Any]:
        """"""
        return {
            'total_compactions': self.stats['total_compactions'],
            'success_rate': (
                self.stats['successful_compactions'] / self.stats['total_compactions'] * 100
                if self.stats['total_compactions'] > 0 else 0
            ),
            'strategy_usage': self.stats['strategy_usage'],
            'total_bytes_saved': self.stats['total_bytes_saved'],
            'avg_compression_rate': f"{self.stats['avg_compression_rate']:.1f}%",
            'config': self.config
        }
    def update_config(self, new_config: Dict[str, Any]):
        """"""
        self.config.update(new_config)
        print("⚙️ ")
    def reset_statistics(self):
        """"""
        self.stats = {
            'total_compactions': 0,
            'successful_compactions': 0,
            'strategy_usage': {strategy.value: 0 for strategy in CompactionStrategy},
            'total_bytes_saved': 0,
            'avg_compression_rate': 0.0
        }
        print("📊 ")
# Testing
def test_auto_compaction_system():
    """"""
    print("🧪 Testing AutoCompactionSystem")
    print("=" * 50)
    compactor = AutoCompactionSystem()
    # Testing
    test_content = """
# 
## 
## 
1.  - token
2.  - 
3.  - 
4.  - 
## Performance
- : 70-80%
- : 80-90%
- : 100%
## 
- SmartFileLoader v2.0
- AutoCompactionSystem
- HierarchicalMemorySystem
- AdaptiveLearningEngine
## 
AIAI
AIAI
AIAI
"""
    print("📄 Testing:", len(test_content), "")
    print()
    # Testing
    strategies = [
        CompactionStrategy.AUTO,
        CompactionStrategy.MERGE,
        CompactionStrategy.SUMMARIZE,
        CompactionStrategy.EXTRACT
    ]
    for strategy in strategies:
        print(f"📋 Testing: {strategy.value}")
        result = compactor.compact_content(test_content, strategy)
        if result.success:
            print(f"  ✅ ")
            print(f"     : {result.compression_rate:.1f}%")
            print(f"     : {len(result.original_content.encode('utf-8'))} bytes")
            print(f"     : {len(result.compacted_content.encode('utf-8'))} bytes")
            # 
            if 'original_lines' in result.metadata:
                print(f"     : {result.metadata['original_lines']}")
                print(f"     : {result.metadata['merged_lines']}")
            if 'summary_length' in result.metadata:
                print(f"     : {result.metadata['summary_length']} ")
            if 'key_points_extracted' in result.metadata:
                print(f"     : {result.metadata['key_points_extracted']} ")
            # 
            preview = result.compacted_content[:100] + "..." if len(result.compacted_content) > 100 else result.compacted_content
            print(f"     : {preview}")
        else:
            print(f"  ❌ : {result.error}")
        print()
    # 
    print("📊 :")
    stats = compactor.get_statistics()
    for key, value in stats.items():
        if key != 'config':
            print(f"   {key}: {value}")
    print("\n" + "=" * 50)
    print("🎯 AutoCompactionSystem TestingComplete")
if __name__ == "__main__":
    test_auto_compaction_system()