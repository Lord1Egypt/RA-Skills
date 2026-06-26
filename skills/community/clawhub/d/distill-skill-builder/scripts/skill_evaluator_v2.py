#!/usr/bin/env python3
"""
Skill Quality Evaluator v2.0
基于官方文档评估 Skill 质量

评估维度：
1. 触发词覆盖 (Trigger Coverage) - 15分
2. 元数据完整性 (Metadata) - 10分
3. 核心内容深度 (Core Content) - 20分
4. 快速参考实用性 (Quick Reference) - 15分
5. 避坑指南质量 (Pitfalls Guide) - 15分
6. 来源标注规范性 (Source Attribution) - 10分
7. 参考文档覆盖 (Reference Coverage) - 10分
8. 输出格式规范 (Output Format) - 5分
"""

import os
import sys
import re
import yaml
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field

@dataclass
class Dimension:
    name: str
    weight: int
    max_score: int
    description: str

@dataclass
class DimensionResult:
    dimension: Dimension
    score: float
    details: list = field(default_factory=list)

class SkillEvaluatorV2:
    """Skill 质量评估器 v2.0"""
    
    DIMENSIONS = [
        Dimension("触发词覆盖", 15, 15, "检查 trigger 字段数量和质量"),
        Dimension("元数据完整性", 10, 10, "YAML frontmatter 字段完整性"),
        Dimension("核心内容深度", 20, 20, "正文内容丰富度、代码示例、表格"),
        Dimension("快速参考", 15, 15, "表格、代码块、关键数值"),
        Dimension("避坑指南", 15, 15, "常见错误、版本陷阱、设计红线"),
        Dimension("来源标注", 10, 10, "官方文档 URL、更新日期"),
        Dimension("参考文档覆盖", 10, 10, "references 目录文件数和质量"),
        Dimension("输出格式规范", 5, 5, "回复结构、示例、禁用格式"),
    ]
    
    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.name = self.skill_path.name
        self.results: list[DimensionResult] = []
        
    def evaluate(self) -> dict:
        """执行完整评估"""
        skill_md = self.skill_path / 'SKILL.md'
        if not skill_md.exists():
            return {'error': f'SKILL.md not found'}
        
        content = skill_md.read_text(encoding='utf-8')
        frontmatter, body = self._parse_frontmatter(content)
        
        # 执行各项评估
        self._evaluate_triggers(frontmatter)
        self._evaluate_metadata(frontmatter)
        self._evaluate_core_content(body, frontmatter)
        self._evaluate_quick_ref(body)
        self._evaluate_pitfalls(body)
        self._evaluate_sources(body)
        self._evaluate_references()
        self._evaluate_output_format(body)
        
        return self._build_report()
    
    def _parse_frontmatter(self, content: str) -> tuple[Optional[dict], str]:
        """解析 YAML frontmatter"""
        if content.startswith('---'):
            parts = content[3:].split('---', 1)
            if len(parts) == 2:
                try:
                    fm = yaml.safe_load(parts[0])
                    return fm, parts[1].strip()
                except:
                    pass
        return None, content
    
    def _score(self, dim_name: str, score: float, details: list = None):
        """记录评分结果"""
        dim = next(d for d in self.DIMENSIONS if d.name == dim_name)
        self.results.append(DimensionResult(dim, min(score, dim.max_score), details or []))
    
    def _evaluate_triggers(self, fm: Optional[dict]):
        """评估触发词"""
        if not fm or 'trigger' not in fm:
            self._score('触发词覆盖', 0, ['缺少 trigger 字段'])
            return
        
        trigger = fm['trigger']
        if isinstance(trigger, str):
            triggers = [t.strip() for t in trigger.split('|') if t.strip()]
            count = len(triggers)
            
            quality_bonus = 0
            has_chinese = any('\u4e00' <= c <= '\u9fff' for t in trigger for c in t)
            has_english = any(c.isalpha() for t in trigger for c in t)
            if has_chinese and has_english:
                quality_bonus = 3
            
            score = min(15, count * 1.5 + quality_bonus)
            self._score('触发词覆盖', score, [f'触发词数量: {count}', '中英双语' if quality_bonus else ''])
        else:
            self._score('触发词覆盖', 5, ['trigger 格式错误'])
    
    def _evaluate_metadata(self, fm: Optional[dict]):
        """评估元数据"""
        if not fm:
            self._score('元数据完整性', 0, ['缺少 YAML frontmatter'])
            return
        
        score = 0
        details = []
        
        required = ['name', 'description', 'trigger']
        for field in required:
            if field in fm and fm[field]:
                score += 3.3
                details.append(f'✓ {field}')
            else:
                details.append(f'✗ 缺少 {field}')
        
        optional = ['tags', 'version', 'author']
        for field in optional:
            if field in fm and fm[field]:
                score += 0.3
                details.append(f'+ {field}')
        
        self._score('元数据完整性', min(10, score), details)
    
    def _evaluate_core_content(self, body: str, fm: Optional[dict]):
        """评估核心内容"""
        score = 0
        details = []
        
        char_count = len(body)
        if char_count >= 10000:
            score += 8
        elif char_count >= 5000:
            score += 6
        elif char_count >= 2000:
            score += 4
        elif char_count >= 1000:
            score += 2
        details.append(f'字符数: {char_count}')
        
        h1 = len(re.findall(r'^# ', body, re.MULTILINE))
        h2 = len(re.findall(r'^## ', body, re.MULTILINE))
        h3 = len(re.findall(r'^### ', body, re.MULTILINE))
        
        if h1 >= 5 and h2 >= 10:
            score += 6
        elif h1 >= 3 and h2 >= 5:
            score += 4
        elif h1 >= 2:
            score += 2
        details.append(f'标题: H1={h1}, H2={h2}, H3={h3}')
        
        code_blocks = len(re.findall(r'```[\s\S]*?```', body))
        if code_blocks >= 10:
            score += 4
        elif code_blocks >= 5:
            score += 3
        elif code_blocks >= 2:
            score += 1
        details.append(f'代码块: {code_blocks}')
        
        tables = len(re.findall(r'\|.*\|.*\|', body))
        if tables >= 10:
            score += 2
        elif tables >= 5:
            score += 1
        details.append(f'表格: {tables}')
        
        self._score('核心内容深度', min(20, score), details)
    
    def _evaluate_quick_ref(self, body: str):
        """评估快速参考"""
        score = 0
        details = []
        
        tables = len(re.findall(r'\|.*\|.*\|', body))
        if tables >= 5:
            score += 5
        elif tables >= 3:
            score += 3
        elif tables >= 1:
            score += 1
        details.append(f'表格: {tables}')
        
        code_blocks = len(re.findall(r'```', body))
        if code_blocks >= 10:
            score += 5
        elif code_blocks >= 5:
            score += 3
        elif code_blocks >= 2:
            score += 1
        details.append(f'代码块: {code_blocks}')
        
        if re.search(r'#{1,3}\s*快速参考', body):
            score += 3
            details.append('有快速参考章节')
        
        key_values = len(re.findall(r'\d+[ptpx%]+', body))
        if key_values >= 10:
            score += 2
        elif key_values >= 5:
            score += 1
        details.append(f'关键数值: {key_values}')
        
        self._score('快速参考', min(15, score), details)
    
    def _evaluate_pitfalls(self, body: str):
        """评估避坑指南"""
        score = 0
        details = []
        
        if re.search(r'#{1,3}\s*[^#]*避坑', body):
            score += 8
            details.append('有避坑指南章节')
        
        warnings = len(re.findall(r'⚠️|⚠|❌|❗', body))
        if warnings >= 5:
            score += 4
        elif warnings >= 3:
            score += 2
        elif warnings >= 1:
            score += 1
        details.append(f'警告标识: {warnings}')
        
        error_tables = len(re.findall(r'\|.*❌.*✅', body))
        if error_tables >= 3:
            score += 3
        elif error_tables >= 1:
            score += 2
        details.append(f'错误做法表格: {error_tables}')
        
        self._score('避坑指南', min(15, score), details)
    
    def _evaluate_sources(self, body: str):
        """评估来源标注"""
        score = 0
        details = []
        
        urls = re.findall(r'https?://\S+', body)
        official_urls = [u for u in urls if any(domain in u for domain in [
            'developer.apple.com', 'developer.huawei.com',
            'woshipm.com', 'zhouqicf.com', 'umlchina.com',
            'atlassian.com', 'scrumguides.org', 'mermaid.js.org',
            'pmi.org', 'productboard.com', 'aha.io'
        ])]
        if len(official_urls) >= 3:
            score += 4
        elif len(official_urls) >= 1:
            score += 3
        details.append(f'官方URL: {len(official_urls)}')
        
        dates = re.findall(r'\d{4}[-/]\d{2}[-/]\d{2}|\d{4}年\d{1,2}月', body)
        if dates:
            score += 3
            details.append(f'日期: {dates[0]}')
        else:
            details.append('缺少日期')
        
        if re.search(r'来源：|来源:|Source:', body):
            score += 2
            details.append('有来源标注')
        
        if '更新频率' in body or '更新周期' in body:
            score += 1
            details.append('有更新频率说明')
        
        self._score('来源标注', min(10, score), details)
    
    def _evaluate_references(self):
        """评估参考文档"""
        ref_dir = self.skill_path / 'references'
        score = 0
        details = []
        
        if not ref_dir.exists():
            self._score('参考文档覆盖', 0, ['缺少 references 目录'])
            return
        
        files = list(ref_dir.glob('*.md'))
        count = len(files)
        
        if count == 0:
            self._score('参考文档覆盖', 0, ['references 目录为空'])
            return
        
        score = min(5, count * 0.5)
        details.append(f'文件数: {count}')
        
        total_lines = 0
        for f in files:
            lines = len(f.read_text(encoding='utf-8').split('\n'))
            total_lines += lines
        
        avg_lines = total_lines / count if count > 0 else 0
        if avg_lines >= 300:
            score += 3
        elif avg_lines >= 150:
            score += 2
        elif avg_lines >= 50:
            score += 1
        details.append(f'平均行数: {avg_lines:.0f}')
        
        sourced = 0
        for f in files:
            content = f.read_text(encoding='utf-8')
            if re.search(r'来源：|来源:|Source:|https?://', content):
                sourced += 1
        if sourced >= count * 0.8:
            score += 2
            details.append(f'有来源标注: {sourced}/{count}')
        
        self._score('参考文档覆盖', min(10, score), details)
    
    def _evaluate_output_format(self, body: str):
        """评估输出格式"""
        score = 0
        details = []
        
        if re.search(r'#{1,3}\s*[^#]*输出格式', body):
            score += 3
            details.append('有输出格式章节')
        
        if '示例回复' in body or '> ' in body:
            score += 1
            details.append('有示例回复')
        
        if '禁用' in body or '禁止' in body:
            score += 1
            details.append('有禁用格式说明')
        
        if re.search(r'回复结构|结构：|\d\..*回答', body):
            score += 1
            details.append('有回复结构定义')
        
        self._score('输出格式规范', min(5, score), details)
    
    def _build_report(self) -> dict:
        """构建报告"""
        total = sum(r.score for r in self.results)
        max_total = sum(d.max_score for d in self.DIMENSIONS)
        pct = total / max_total * 100
        
        return {
            'name': self.name,
            'path': str(self.skill_path),
            'results': [(r.dimension.name, r.score, r.dimension.max_score, r.details) for r in self.results],
            'total': total,
            'max': max_total,
            'pct': pct,
            'grade': self._calc_grade(pct),
        }
    
    def _calc_grade(self, pct: float) -> str:
        if pct >= 90: return 'A'
        elif pct >= 80: return 'B'
        elif pct >= 70: return 'C'
        elif pct >= 60: return 'D'
        return 'F'
    
    @staticmethod
    def print_report(report: dict):
        """打印报告"""
        print(f"\n{'═'*65}")
        print(f"  📊 Skill Quality Report: {report['name']}")
        print(f"{'═'*65}")
        
        print(f"\n  🏆 综合得分: {report['total']:.1f}/{report['max']} ({report['pct']:.1f}%) — {report['grade']}级")
        
        print(f"\n  {'维度':<18} {'得分':>8} {'权重':>8}")
        print(f"  {'─'*40}")
        
        for name, score, max_s, details in report['results']:
            bar = '█' * int(score / max_s * 10) + '░' * (10 - int(score / max_s * 10))
            print(f"  {name:<16} {score:>5.1f}/{max_s:<5} {bar}")
        
        print(f"\n  {'─'*40}")
        print(f"  {'═'*65}")


def main():
    if len(sys.argv) < 2:
        print("用法: python skill_evaluator_v2.py <skill_path> [skill_path2 ...]")
        sys.exit(1)
    
    reports = []
    for path in sys.argv[1:]:
        evaluator = SkillEvaluatorV2(path)
        report = evaluator.evaluate()
        if 'error' in report:
            print(f"❌ Error: {report['error']}")
            continue
        reports.append(report)
        SkillEvaluatorV2.print_report(report)
    
    if len(reports) >= 2:
        print_comparison(reports)


def print_comparison(reports: list):
    """打印对比报告"""
    print(f"\n{'═'*65}")
    print(f"  📊 Skill Comparison")
    print(f"{'═'*65}")
    print(f"\n  {'Skill':<25} {'总分':>10} {'得分率':>10} {'评级':>6}")
    print(f"  {'─'*55}")
    
    for r in reports:
        print(f"  {r['name']:<25} {r['total']:>10.1f} {r['pct']:>10.1f}% {r['grade']:>6}")
    
    print(f"\n  {'─'*55}")
    print(f"  {'维度对比':^55}")
    print(f"  {'─'*55}")
    
    all_dims = set()
    for r in reports:
        for name, *_ in r['results']:
            all_dims.add(name)
    
    header = f"  {{:<20}}".format('维度')
    for r in reports:
        header += f" {r['name'][:12]:>12}"
    print(header)
    print(f"  {'─'*55}")
    
    for dim in sorted(all_dims):
        row = f"  {{:<20}}".format(dim)
        for r in reports:
            score = next((s for n, s, *_, in r['results'] if n == dim), 0)
            row += f" {score:>12.1f}"
        print(row)
    
    print(f"\n{'═'*65}\n")


if __name__ == '__main__':
    main()
