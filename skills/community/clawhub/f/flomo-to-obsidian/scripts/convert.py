#!/usr/bin/env python3
"""
Flomo to Obsidian Converter
将 flomo 导出的 HTML 文件转换为 Obsidian markdown 格式
"""

import argparse
import json
import logging
import re
import sys
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

try:
    from bs4 import BeautifulSoup
    import markdownify
except ImportError:
    print("错误：缺少依赖库。请运行: pip install beautifulsoup4 markdownify")
    sys.exit(1)


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('conversion.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class FlomoNote:
    """Flomo 笔记数据结构"""
    def __init__(self, timestamp: str, content: str, tags: List[str] = None, 
                 attachments: List[Dict[str, str]] = None, html_content: str = ''):
        self.timestamp = timestamp
        self.content = content
        self.tags = tags or []
        self.attachments = attachments or []  # [{'type': 'image'/'audio', 'src': 'path', 'new_path': 'obsidian_path'}]
        self.html_content = html_content  # 保留原始 HTML 用于解析附件
        self.datetime = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    
    def __repr__(self):
        return f"FlomoNote(timestamp={self.timestamp}, tags={self.tags}, attachments={len(self.attachments)})"


class FlomoParser:
    """解析 Flomo HTML 导出文件"""
    
    def __init__(self, html_path: str, encoding: str = 'utf-8'):
        self.html_path = Path(html_path)
        self.html_dir = self.html_path.parent  # HTML 文件所在目录
        self.encoding = encoding
        self.notes: List[FlomoNote] = []
    
    def parse(self) -> List[FlomoNote]:
        """解析 HTML 文件并提取所有笔记"""
        logger.info(f"开始解析文件: {self.html_path}")
        
        try:
            with open(self.html_path, 'r', encoding=self.encoding) as f:
                html_content = f.read()
        except Exception as e:
            logger.error(f"读取文件失败: {e}")
            raise
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 查找所有笔记
        memo_divs = soup.find_all('div', class_='memo')
        
        if not memo_divs:
            logger.warning("未找到任何笔记，请检查 HTML 文件格式")
            return []
        
        logger.info(f"找到 {len(memo_divs)} 条笔记")
        
        for memo in memo_divs:
            try:
                # 提取时间
                time_div = memo.find('div', class_='time')
                if not time_div:
                    logger.warning("笔记缺少时间信息，跳过")
                    continue
                timestamp = time_div.text.strip()
                
                # 提取内容
                content_div = memo.find('div', class_='content')
                if not content_div:
                    logger.warning(f"笔记 {timestamp} 缺少内容，跳过")
                    continue
                
                # 转换为 Markdown
                content_html = str(content_div)
                markdown_content = markdownify.markdownify(content_html, heading_style="ATX")
                
                # 清理内容
                markdown_content = self._clean_content(markdown_content)
                
                # 提取标签
                tags = self._extract_tags(markdown_content)
                
                note = FlomoNote(timestamp, markdown_content, tags)
                self.notes.append(note)
                
            except Exception as e:
                logger.error(f"解析笔记时出错: {e}")
                continue
        
        logger.info(f"成功解析 {len(self.notes)} 条笔记")
        return self.notes
    
    def _clean_content(self, content: str) -> str:
        """清理内容中的多余空格和格式"""
        # 移除多余的空行
        content = re.sub(r'\n{3,}', '\n\n', content)
        # 移除首尾空白
        content = content.strip()
        return content
    
    def _extract_tags(self, content: str) -> List[str]:
        """从内容中提取标签"""
        # 匹配 #tag 格式
        tags = re.findall(r'#([^\s#]+)', content)
        return list(set(tags))  # 去重


class ObsidianConverter:
    """将 Flomo 笔记转换为 Obsidian 格式"""
    
    def __init__(
        self,
        output_dir: str,
        mode: str = 'by-date',
        tag_prefix: str = '',
        preserve_time: bool = False
    ):
        self.output_dir = Path(output_dir)
        self.mode = mode
        self.tag_prefix = tag_prefix
        self.preserve_time = preserve_time
        
        # 创建输出目录
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def convert(self, notes: List[FlomoNote]) -> Dict[str, int]:
        """转换笔记并保存到文件"""
        logger.info(f"开始转换 {len(notes)} 条笔记，模式: {self.mode}")
        
        stats = {'files': 0, 'notes': 0, 'errors': 0}
        
        if self.mode == 'by-date':
            stats = self._convert_by_date(notes)
        elif self.mode == 'individual':
            stats = self._convert_individual(notes)
        elif self.mode == 'single':
            stats = self._convert_single(notes)
        else:
            logger.error(f"未知的转换模式: {self.mode}")
            return stats
        
        logger.info(f"转换完成: {stats}")
        return stats
    
    def _convert_by_date(self, notes: List[FlomoNote]) -> Dict[str, int]:
        """按日期组织笔记（一天一个文件）"""
        # 按日期分组
        notes_by_date = {}
        for note in notes:
            date_key = note.datetime.strftime('%Y-%m-%d')
            if date_key not in notes_by_date:
                notes_by_date[date_key] = []
            notes_by_date[date_key].append(note)
        
        stats = {'files': 0, 'notes': 0, 'errors': 0}
        
        for date_key, date_notes in sorted(notes_by_date.items()):
            try:
                filename = f"{date_key}.md"
                filepath = self.output_dir / filename
                
                # 生成文件内容
                content = self._generate_daily_note(date_key, date_notes)
                
                # 写入文件
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                stats['files'] += 1
                stats['notes'] += len(date_notes)
                logger.info(f"创建文件: {filename} ({len(date_notes)} 条笔记)")
                
            except Exception as e:
                logger.error(f"创建日期文件 {date_key} 失败: {e}")
                stats['errors'] += 1
        
        return stats
    
    def _convert_individual(self, notes: List[FlomoNote]) -> Dict[str, int]:
        """每条笔记创建单独文件"""
        stats = {'files': 0, 'notes': 0, 'errors': 0}
        
        for i, note in enumerate(notes):
            try:
                # 生成文件名
                if self.preserve_time:
                    timestamp_str = note.datetime.strftime('%Y-%m-%d-%H%M%S')
                    filename = f"flomo-{timestamp_str}.md"
                else:
                    timestamp_str = note.datetime.strftime('%Y-%m-%d')
                    # 如果同一天有多条，加序号
                    base_filename = f"flomo-{timestamp_str}"
                    filename = f"{base_filename}.md"
                    counter = 1
                    while (self.output_dir / filename).exists():
                        filename = f"{base_filename}-{counter}.md"
                        counter += 1
                
                filepath = self.output_dir / filename
                
                # 生成文件内容
                content = self._generate_individual_note(note)
                
                # 写入文件
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                stats['files'] += 1
                stats['notes'] += 1
                
                if (i + 1) % 100 == 0:
                    logger.info(f"已处理 {i + 1}/{len(notes)} 条笔记")
                
            except Exception as e:
                logger.error(f"创建笔记文件失败: {e}")
                stats['errors'] += 1
        
        logger.info(f"创建了 {stats['files']} 个文件")
        return stats
    
    def _convert_single(self, notes: List[FlomoNote]) -> Dict[str, int]:
        """所有笔记合并到一个文件"""
        stats = {'files': 0, 'notes': 0, 'errors': 0}
        
        try:
            filename = "flomo-all-notes.md"
            filepath = self.output_dir / filename
            
            # 生成文件内容
            content = self._generate_single_file(notes)
            
            # 写入文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            stats['files'] = 1
            stats['notes'] = len(notes)
            logger.info(f"创建文件: {filename} ({len(notes)} 条笔记)")
            
        except Exception as e:
            logger.error(f"创建合并文件失败: {e}")
            stats['errors'] += 1
        
        return stats
    
    def _generate_daily_note(self, date: str, notes: List[FlomoNote]) -> str:
        """生成每日笔记内容"""
        # Frontmatter
        all_tags = set()
        for note in notes:
            all_tags.update(note.tags)
        
        tags_list = [f"{self.tag_prefix}{tag}" for tag in sorted(all_tags)]
        tags_list.insert(0, 'flomo')  # 添加来源标签
        
        content = f"""---
date: {date}
source: flomo
tags: [{', '.join(tags_list)}]
note_count: {len(notes)}
---

# Flomo Notes - {date}

"""
        
        # 添加每条笔记
        for note in sorted(notes, key=lambda x: x.datetime):
            content += f"## {note.timestamp}\n\n"
            content += f"{note.content}\n\n"
            content += "---\n\n"
        
        return content
    
    def _generate_individual_note(self, note: FlomoNote) -> str:
        """生成单条笔记内容"""
        tags_list = [f"{self.tag_prefix}{tag}" for tag in sorted(note.tags)]
        tags_list.insert(0, 'flomo')
        
        content = f"""---
created: {note.timestamp}
source: flomo
tags: [{', '.join(tags_list)}]
---

{note.content}
"""
        return content
    
    def _generate_single_file(self, notes: List[FlomoNote]) -> str:
        """生成单个合并文件内容"""
        all_tags = set()
        for note in notes:
            all_tags.update(note.tags)
        
        tags_list = [f"{self.tag_prefix}{tag}" for tag in sorted(all_tags)]
        tags_list.insert(0, 'flomo')
        
        content = f"""---
title: Flomo All Notes
source: flomo
total_notes: {len(notes)}
tags: [{', '.join(tags_list)}]
export_date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
---

# Flomo All Notes

Total: {len(notes)} notes

---

"""
        
        # 按时间排序添加所有笔记
        for note in sorted(notes, key=lambda x: x.datetime):
            content += f"## {note.timestamp}\n\n"
            content += f"{note.content}\n\n"
            content += "---\n\n"
        
        return content


class IncrementalSync:
    """增量同步管理"""
    
    def __init__(self, state_file: str):
        self.state_file = Path(state_file)
        self.processed_notes = set()
        self._load_state()
    
    def _load_state(self):
        """加载同步状态"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.processed_notes = set(data.get('processed_notes', []))
                logger.info(f"加载状态: 已处理 {len(self.processed_notes)} 条笔记")
            except Exception as e:
                logger.warning(f"加载状态文件失败: {e}")
    
    def save_state(self):
        """保存同步状态"""
        try:
            data = {
                'processed_notes': list(self.processed_notes),
                'last_sync': datetime.now().isoformat()
            }
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"保存状态: {len(self.processed_notes)} 条已处理笔记")
        except Exception as e:
            logger.error(f"保存状态文件失败: {e}")
    
    def filter_new_notes(self, notes: List[FlomoNote]) -> List[FlomoNote]:
        """过滤出新笔记"""
        new_notes = []
        for note in notes:
            note_id = f"{note.timestamp}_{hash(note.content)}"
            if note_id not in self.processed_notes:
                new_notes.append(note)
                self.processed_notes.add(note_id)
        
        logger.info(f"筛选出 {len(new_notes)} 条新笔记 (总共 {len(notes)} 条)")
        return new_notes


def main():
    parser = argparse.ArgumentParser(
        description='将 Flomo 导出的 HTML 转换为 Obsidian markdown 格式'
    )
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Flomo HTML 文件路径'
    )
    parser.add_argument(
        '--output', '-o',
        required=True,
        help='Obsidian vault 中的输出目录'
    )
    parser.add_argument(
        '--mode', '-m',
        choices=['by-date', 'individual', 'single'],
        default='by-date',
        help='组织模式: by-date(按日期), individual(单独文件), single(合并文件)'
    )
    parser.add_argument(
        '--tag-prefix',
        default='',
        help='标签前缀，如 "flomo/" 会将 #工作 转换为 #flomo/工作'
    )
    parser.add_argument(
        '--preserve-time',
        action='store_true',
        help='在文件名中保留时间（仅 individual 模式）'
    )
    parser.add_argument(
        '--encoding',
        default='utf-8',
        help='HTML 文件编码 (默认: utf-8)'
    )
    parser.add_argument(
        '--incremental',
        action='store_true',
        help='增量同步模式（仅处理新笔记）'
    )
    parser.add_argument(
        '--state-file',
        default='.flomo-sync-state.json',
        help='状态文件路径（增量模式）'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='显示详细日志'
    )
    
    args = parser.parse_args()
    
    # 设置日志级别
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    try:
        # 解析 Flomo HTML
        parser_obj = FlomoParser(args.input, args.encoding)
        notes = parser_obj.parse()
        
        if not notes:
            logger.error("没有找到可转换的笔记")
            return 1
        
        # 增量同步处理
        if args.incremental:
            sync = IncrementalSync(args.state_file)
            notes = sync.filter_new_notes(notes)
            if not notes:
                logger.info("没有新笔记需要同步")
                return 0
        
        # 转换为 Obsidian 格式
        converter = ObsidianConverter(
            args.output,
            args.mode,
            args.tag_prefix,
            args.preserve_time
        )
        stats = converter.convert(notes)
        
        # 保存增量同步状态
        if args.incremental:
            sync.save_state()
        
        # 输出统计信息
        print(f"\n转换完成！")
        print(f"  创建文件: {stats['files']}")
        print(f"  转换笔记: {stats['notes']}")
        print(f"  错误数量: {stats['errors']}")
        print(f"  输出目录: {args.output}")
        
        return 0
        
    except Exception as e:
        logger.error(f"转换失败: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
