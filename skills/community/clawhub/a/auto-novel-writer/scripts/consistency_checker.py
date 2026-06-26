#!/usr/bin/env python3
"""
一致性检查工具 - 检测剧情偏离、设定冲突、战力崩坏等问题
"""

import sys
import re
from pathlib import Path
from typing import List, Dict, Set, Tuple
from difflib import SequenceMatcher

sys.path.insert(0, str(Path(__file__).parent))
from novel_manager import get_novels_dir, get_recent_summaries


class ConsistencyChecker:
    """一致性检查器"""
    
    def __init__(self, novel_name: str):
        self.novel_name = novel_name
        self.novel_dir = get_novels_dir() / novel_name
        
        if not self.novel_dir.exists():
            raise FileNotFoundError(f"小说 '{novel_name}' 不存在")
        
        self.issues = []
        self.warnings = []
    
    def read_file(self, relative_path: str) -> str:
        """读取文件"""
        file_path = self.novel_dir / relative_path
        if file_path.exists():
            return file_path.read_text(encoding='utf-8')
        return ""
    
    def check_chapter(self, volume: int, chapter: int) -> Dict:
        """
        检查指定章节的一致性
        
        Returns:
            检查结果字典
        """
        chapter_dir = self.novel_dir / "chapters" / f"{volume:02d}-{chapter:03d}"
        
        if not chapter_dir.exists():
            return {"error": f"第{chapter}章不存在"}
        
        content_path = chapter_dir / "content.md"
        if not content_path.exists():
            return {"error": f"第{chapter}章内容文件不存在"}
        
        content = content_path.read_text(encoding='utf-8')
        
        self.issues = []
        self.warnings = []
        
        # 执行各项检查
        self._check_outline_alignment(content, chapter)
        self._check_character_consistency(content)
        self._check_power_system_consistency(content)
        self._check_timeline_consistency(content, volume, chapter)
        self._check_setting_consistency(content)
        self._check_style_issues(content)
        
        return {
            "chapter": chapter,
            "volume": volume,
            "word_count": len(content.replace(' ', '').replace('\n', '')),
            "issues": self.issues,
            "warnings": self.warnings,
            "has_critical": any(i["severity"] == "critical" for i in self.issues),
        }
    
    def _check_outline_alignment(self, content: str, chapter: int):
        """检查是否偏离大纲"""
        outline = self.read_file("outline.md")
        
        # 提取大纲中对该章的规划
        chapter_plan = self._extract_chapter_from_outline(outline, chapter)
        
        if not chapter_plan:
            self.warnings.append({
                "type": "大纲缺失",
                "message": f"第{chapter}章在大纲中没有明确规划",
                "severity": "warning"
            })
            return
        
        # 简单检查：大纲中提到的关键元素是否在内容中体现
        # 提取大纲中的关键词（角色名、地点、事件等）
        keywords = self._extract_keywords(chapter_plan)
        
        missing_keywords = []
        for kw in keywords:
            if kw not in content:
                missing_keywords.append(kw)
        
        if len(missing_keywords) > len(keywords) * 0.5:
            self.issues.append({
                "type": "偏离大纲",
                "message": f"本章内容可能偏离大纲规划，缺失关键元素：{', '.join(missing_keywords[:5])}",
                "severity": "medium",
                "suggestion": "检查是否遗漏了大纲中规划的重要情节"
            })
    
    def _check_character_consistency(self, content: str):
        """检查角色一致性"""
        characters_content = self.read_file("characters/index.md")
        
        # 提取角色名
        character_names = self._extract_character_names(characters_content)
        
        # 检查内容中提到的角色
        mentioned_chars = set()
        for name in character_names:
            if name in content and len(name) >= 2:
                mentioned_chars.add(name)
        
        # 检查是否有未记录的新角色频繁出现
        # 简单启发式：检查大写的称呼或名字
        potential_new_chars = re.findall(r'[\u4e00-\u9fa5]{2,4}(?=大人|公子|小姐|前辈|师兄|师弟|长老|掌门)', content)
        for char in potential_new_chars:
            if char not in character_names and char not in mentioned_chars:
                self.warnings.append({
                    "type": "潜在新角色",
                    "message": f"发现可能的新角色：{char}",
                    "severity": "info",
                    "suggestion": "如果这是新角色，请添加到角色档案"
                })
    
    def _check_power_system_consistency(self, content: str):
        """检查战力/等级体系一致性"""
        cultivation = self.read_file("settings/cultivation.md")
        system = self.read_file("settings/system.md")
        
        # 提取等级名称
        levels = self._extract_cultivation_levels(cultivation)
        
        # 检查内容中的等级描述
        # 查找"突破"、"晋升"、"达到"等关键词
        breakthrough_pattern = r'(突破|晋升|达到|晋级|进阶|升为)[\u4e00-\u9fa5\s]*([\u4e00-\u9fa5]{2,6})'
        matches = re.findall(breakthrough_pattern, content)
        
        for action, level in matches:
            if level not in levels and len(level) >= 2:
                self.warnings.append({
                    "type": "等级检查",
                    "message": f"发现未记录的等级：{level}",
                    "severity": "info",
                    "suggestion": "请确认该等级是否已定义在修炼体系中"
                })
        
        # 检查战力崩坏（简单启发式）
        # 检查是否有跨越大等级的战斗
        battle_pattern = r'(击败|击杀|战胜|碾压)\s*([\u4e00-\u9fa5]{2,8})'
        # 这里可以添加更复杂的战力对比逻辑
    
    def _check_timeline_consistency(self, content: str, volume: int, chapter: int):
        """检查时间线一致性"""
        # 获取前文摘要
        prev_summaries = get_recent_summaries(self.novel_name, 5)
        
        # 提取时间关键词
        time_keywords = ['三天后', '一周后', '一个月后', '一年后', '次日', '第二天', '当晚']
        
        for keyword in time_keywords:
            if keyword in content:
                # 检查前文是否有时间铺垫
                found_in_prev = False
                for summary in prev_summaries:
                    if keyword in summary.get('summary', ''):
                        found_in_prev = True
                        break
                
                if not found_in_prev and keyword in ['三天后', '一周后']:
                    self.warnings.append({
                        "type": "时间跳跃",
                        "message": f"发现时间跳跃：{keyword}",
                        "severity": "info",
                        "suggestion": "确保时间跳跃有合理的过渡或解释"
                    })
    
    def _check_setting_consistency(self, content: str):
        """检查设定一致性"""
        world = self.read_file("settings/world.md")
        items = self.read_file("settings/items.md")
        skills = self.read_file("settings/skills.md")
        
        # 提取已定义的地点
        locations = self._extract_locations(world)
        
        # 检查新地点
        # 简单启发式：XX山、XX城、XX谷等
        new_locations = re.findall(r'[\u4e00-\u9fa5]{2,6}(?:山|城|谷|宗|派|阁|殿|岛|域|境)', content)
        for loc in new_locations:
            if loc not in locations:
                self.warnings.append({
                    "type": "新地点",
                    "message": f"发现新地点：{loc}",
                    "severity": "info",
                    "suggestion": "请确认是否添加到世界观设定"
                })
        
        # 检查道具/技能
        item_names = self._extract_names_from_section(items, "武器|丹药|材料|特殊物品")
        skill_names = self._extract_names_from_section(skills, "技能|功法")
        
        # 检查是否使用了未定义的道具/技能
        for item in item_names:
            if item in content:
                # 已定义，正常
                pass
        
        # 检查新道具
        new_items = re.findall(r'[\u4e00-\u9fa5]{2,6}(?:丹|剑|刀|枪|甲|符|印|珠|镜|塔)', content)
        for item in new_items:
            if item not in item_names and len(item) >= 2:
                self.warnings.append({
                    "type": "新道具",
                    "message": f"发现可能的新道具：{item}",
                    "severity": "info"
                })
    
    def _check_style_issues(self, content: str):
        """检查风格问题"""
        # 检查是否有大段内心独白
        thought_pattern = r'[他想道|心中暗道|心中想|心想][\u4e00-\u9fa5，。]{100,}'
        long_thoughts = re.findall(thought_pattern, content)
        
        if len(long_thoughts) > 3:
            self.warnings.append({
                "type": "内心独白过多",
                "message": f"发现{len(long_thoughts)}处较长内心独白",
                "severity": "low",
                "suggestion": "适当减少内心独白，增加行动和对话"
            })
        
        # 检查解释性内容过多
        explain_pattern = r'[原来|其实|事实上|这是因为|之所以][\u4e00-\u9fa5，。]{80,}'
        long_explains = re.findall(explain_pattern, content)
        
        if len(long_explains) > 3:
            self.warnings.append({
                "type": "解释过多",
                "message": f"发现{len(long_explains)}处较长解释",
                "severity": "low",
                "suggestion": "通过情节展示而非直接解释，保持节奏"
            })
    
    def _extract_chapter_from_outline(self, outline: str, chapter: int) -> str:
        """从大纲中提取指定章节"""
        lines = outline.split('\n')
        for line in lines:
            if re.search(rf'\|\s*{chapter:03d}\s*\|', line) or \
               re.search(rf'第?{chapter}\s*章', line):
                return line.strip()
        return ""
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        # 简单的关键词提取：2-4字的中文词组
        words = re.findall(r'[\u4e00-\u9fa5]{2,4}', text)
        # 过滤常见词
        stop_words = {'本章', '主要', '内容', '情节', '故事', '发展'}
        return [w for w in words if w not in stop_words]
    
    def _extract_character_names(self, content: str) -> Set[str]:
        """提取角色名"""
        names = set()
        # 匹配角色列表中的名字
        # 格式：- 角色名：简介 或 ### 角色名
        patterns = [
            r'[-\*]\s*([\u4e00-\u9fa5]{2,4})[：:]',
            r'###\s*([\u4e00-\u9fa5]{2,4})',
            r'\*\*([\u4e00-\u9fa5]{2,4})\*\*[：:]',
        ]
        for pattern in patterns:
            matches = re.findall(pattern, content)
            names.update(matches)
        return names
    
    def _extract_cultivation_levels(self, content: str) -> Set[str]:
        """提取修炼等级"""
        levels = set()
        # 匹配等级名称
        # 格式：1. 等级名 或 - 等级名
        patterns = [
            r'\d+[\.、]\s*([\u4e00-\u9fa5]{2,6})',
            r'[-\*]\s*([\u4e00-\u9fa5]{2,6})[（(]',
        ]
        for pattern in patterns:
            matches = re.findall(pattern, content)
            levels.update(matches)
        return levels
    
    def _extract_locations(self, content: str) -> Set[str]:
        """提取地点名称"""
        locations = set()
        patterns = [
            r'[-\*]\s*([\u4e00-\u9fa5]{2,6}(?:山|城|谷|宗|派|阁|殿|岛|域))',
            r'###\s*([\u4e00-\u9fa5]{2,6}(?:山|城|谷|宗|派|阁|殿|岛|域))',
        ]
        for pattern in patterns:
            matches = re.findall(pattern, content)
            locations.update(matches)
        return locations
    
    def _extract_names_from_section(self, content: str, section_name: str) -> Set[str]:
        """从特定章节提取名称"""
        names = set()
        # 简单的提取逻辑
        pattern = r'[-\*]\s*([\u4e00-\u9fa5]{2,8})[：:]'
        matches = re.findall(pattern, content)
        names.update(matches)
        return names
    
    def generate_report(self, check_result: Dict) -> str:
        """生成检查报告"""
        lines = []
        lines.append("=" * 60)
        lines.append(f"一致性检查报告 - 第{check_result['chapter']}章")
        lines.append("=" * 60)
        lines.append(f"字数：{check_result['word_count']}")
        lines.append("")
        
        if check_result['issues']:
            lines.append("【发现的问题】")
            for issue in check_result['issues']:
                severity_emoji = "🔴" if issue['severity'] == 'critical' else "🟡"
                lines.append(f"{severity_emoji} [{issue['type']}] {issue['message']}")
                if 'suggestion' in issue:
                    lines.append(f"   建议：{issue['suggestion']}")
                lines.append("")
        else:
            lines.append("✅ 未发现严重一致性问题")
        
        if check_result['warnings']:
            lines.append("\n【提示信息】")
            for warning in check_result['warnings']:
                lines.append(f"ℹ️ [{warning['type']}] {warning['message']}")
        
        lines.append("\n" + "=" * 60)
        
        return '\n'.join(lines)


def main():
    """命令行入口"""
    if len(sys.argv) < 4:
        print("Usage: consistency_checker.py <novel_name> <volume> <chapter>")
        print("       consistency_checker.py <novel_name> --all")
        return
    
    novel_name = sys.argv[1]
    
    if sys.argv[2] == "--all":
        # 检查所有章节
        print("检查所有章节功能待实现")
        return
    
    volume = int(sys.argv[2])
    chapter = int(sys.argv[3])
    
    try:
        checker = ConsistencyChecker(novel_name)
        result = checker.check_chapter(volume, chapter)
        
        if "error" in result:
            print(f"错误：{result['error']}")
        else:
            print(checker.generate_report(result))
    
    except FileNotFoundError as e:
        print(f"错误：{e}")


if __name__ == "__main__":
    main()
