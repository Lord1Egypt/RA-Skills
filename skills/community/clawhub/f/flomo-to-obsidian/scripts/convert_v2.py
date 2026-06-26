#!/usr/bin/env python3
"""
Flomo to Obsidian Converter V2
改进版：支持附件处理和双链转换
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
from urllib.parse import urlparse, parse_qs

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
                 attachments: List[Dict[str, str]] = None, memo_id: str = None,
                 related_ids: List[str] = None):
        self.timestamp = timestamp
        self.content = content
        self.tags = tags or []
        self.attachments = attachments or []  # [{'type': 'image'/'audio', 'src': 'path', 'obsidian_path': 'new_path'}]
        self.memo_id = memo_id  # flomo 的原始 memo_id
        self.related_ids = related_ids or []  # 关联的其他笔记的 memo_id
        self.datetime = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        # 生成唯一标识（用于 Obsidian 双链）
        self.note_id = self._generate_note_id()
    
    def _generate_note_id(self) -> str:
        """生成笔记的唯一标识"""
        # 格式: flomo-YYYYMMDD-HHMMSS
        return f"flomo-{self.datetime.strftime('%Y%m%d-%H%M%S')}"
    
    def __repr__(self):
        return f"FlomoNote(id={self.note_id}, timestamp={self.timestamp}, attachments={len(self.attachments)}, related={len(self.related_ids)})"


class FlomoParser:
    """解析 Flomo HTML 导出文件"""
    
    def __init__(self, html_path: str, encoding: str = 'utf-8'):
        self.html_path = Path(html_path)
        self.html_dir = self.html_path.parent  # HTML 文件所在目录
        self.encoding = encoding
        self.notes: List[FlomoNote] = []
        # memo_id 到 note 的映射
        self.memo_id_map: Dict[str, FlomoNote] = {}
    
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
                note = self._parse_memo(memo)
                if note:
                    self.notes.append(note)
                    # 如果有 memo_id，建立映射
                    if note.memo_id:
                        self.memo_id_map[note.memo_id] = note
                        
            except Exception as e:
                logger.error(f"解析笔记时出错: {e}")
                continue
        
        logger.info(f"成功解析 {len(self.notes)} 条笔记")
        return self.notes
    
    def _parse_memo(self, memo) -> Optional[FlomoNote]:
        """解析单条笔记"""
        # 提取时间
        time_div = memo.find('div', class_='time')
        if not time_div:
            logger.warning("笔记缺少时间信息，跳过")
            return None
        timestamp = time_div.text.strip()
        
        # 提取内容
        content_div = memo.find('div', class_='content')
        if not content_div:
            logger.warning(f"笔记 {timestamp} 缺少内容，跳过")
            return None
        
        # 解析关联链接（在转换为 markdown 之前）
        related_ids = self._extract_related_ids(content_div)
        
        # 解析附件
        files_div = memo.find('div', class_='files')
        attachments = self._extract_attachments(files_div) if files_div else []
        
        # 转换为 Markdown
        content_html = str(content_div)
        markdown_content = markdownify.markdownify(content_html, heading_style="ATX")
        
        # 清理内容
        markdown_content = self._clean_content(markdown_content)
        
        # 提取标签
        tags = self._extract_tags(markdown_content)
        
        # 尝试从内容中提取 memo_id（如果是被关联的笔记）
        memo_id = None
        # 注意：原始笔记可能没有 memo_id，只有被关联引用时才有
        
        note = FlomoNote(
            timestamp=timestamp,
            content=markdown_content,
            tags=tags,
            attachments=attachments,
            memo_id=memo_id,
            related_ids=related_ids
        )
        
        return note
    
    def _extract_related_ids(self, content_div) -> List[str]:
        """提取关联的笔记 ID"""
        related_ids = []
        
        # 查找所有包含 flomo 链接的文本
        text = content_div.get_text()
        # 匹配: 关联自： https://v.flomoapp.com/mine/?memo_id=XXXXXXX
        pattern = r'关联自[：:]\s*https?://v\.flomoapp\.com/mine/\?memo_id=(\w+)'
        matches = re.findall(pattern, text)
        related_ids.extend(matches)
        
        # 也匹配直接的 flomo 链接
        pattern2 = r'https?://v\.flomoapp\.com/mine/\?memo_id=(\w+)'
        matches2 = re.findall(pattern2, text)
        for match in matches2:
            if match not in related_ids:
                related_ids.append(match)
        
        return related_ids
    
    def _extract_attachments(self, files_div) -> List[Dict[str, str]]:
        """提取附件信息"""
        attachments = []
        
        if not files_div:
            return attachments
        
        # 提取图片
        images = files_div.find_all('img')
        for img in images:
            src = img.get('src', '')
            if src:
                attachments.append({
                    'type': 'image',
                    'src': src,
                    'alt': img.get('alt', 'image')
                })
        
        # 提取音频
        audios = files_div.find_all('audio')
        for audio in audios:
            src = audio.get('src', '')
            if src:
                # 尝试获取音频转写文本
                transcription = ''
                audio_player = audio.find_parent('div', class_='audio-player')
                if audio_player:
                    content_div = audio_player.find('div', class_='audio-player__content')
                    if content_div:
                        transcription = content_div.get_text().strip()
                
                attachments.append({
                    'type': 'audio',
                    'src': src,
                    'transcription': transcription
                })
        
        return attachments
    
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
        flomo_html_dir: str,
        mode: str = 'by-date',
        tag_prefix: str = '',
        preserve_time: bool = False,
        copy_attachments: bool = True,
        convert_to_wikilinks: bool = True
    ):
        self.output_dir = Path(output_dir)
        self.flomo_html_dir = Path(flomo_html_dir)
        self.mode = mode
        self.tag_prefix = tag_prefix
        self.preserve_time = preserve_time
        self.copy_attachments = copy_attachments
        self.convert_to_wikilinks = convert_to_wikilinks
        
        # 创建输出目录
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建附件目录
        if self.copy_attachments:
            self.attachments_dir = self.output_dir / 'attachments'
            self.attachments_dir.mkdir(parents=True, exist_ok=True)
        
        # note_id 到文件名的映射（用于双链）
        self.note_id_to_filename: Dict[str, str] = {}
        # memo_id 到 note_id 的映射
        self.memo_id_to_note_id: Dict[str, str] = {}
    
    def convert(self, notes: List[FlomoNote]) -> Dict[str, int]:
        """转换笔记并保存到文件"""
        logger.info(f"开始转换 {len(notes)} 条笔记，模式: {self.mode}")
        
        # 第一遍：建立 memo_id 到 note_id 的映射
        for note in notes:
            if note.memo_id:
                self.memo_id_to_note_id[note.memo_id] = note.note_id
        
        stats = {'files': 0, 'notes': 0, 'errors': 0, 'attachments': 0}
        
        # 处理附件
        if self.copy_attachments:
            stats['attachments'] = self._process_attachments(notes)
        
        # 转换笔记
        if self.mode == 'by-date':
            conversion_stats = self._convert_by_date(notes)
        elif self.mode == 'individual':
            conversion_stats = self._convert_individual(notes)
        elif self.mode == 'single':
            conversion_stats = self._convert_single(notes)
        else:
            logger.error(f"未知的转换模式: {self.mode}")
            return stats
        
        stats.update(conversion_stats)
        logger.info(f"转换完成: {stats}")
        return stats
    
    def _process_attachments(self, notes: List[FlomoNote]) -> int:
        """处理并复制附件"""
        copied_count = 0
        
        for note in notes:
            for attachment in note.attachments:
                src_path = self.flomo_html_dir / attachment['src']
                
                if not src_path.exists():
                    logger.warning(f"附件不存在: {src_path}")
                    continue
                
                # 生成新的文件名
                filename = src_path.name
                dest_path = self.attachments_dir / filename
                
                # 如果文件已存在，添加时间戳避免冲突
                if dest_path.exists():
                    stem = dest_path.stem
                    suffix = dest_path.suffix
                    timestamp = note.datetime.strftime('%Y%m%d%H%M%S')
                    dest_path = self.attachments_dir / f"{stem}_{timestamp}{suffix}"
                
                try:
                    shutil.copy2(src_path, dest_path)
                    # 更新附件的 Obsidian 路径
                    attachment['obsidian_path'] = f"attachments/{dest_path.name}"
                    copied_count += 1
                    logger.debug(f"复制附件: {src_path.name} -> {dest_path.name}")
                except Exception as e:
                    logger.error(f"复制附件失败 {src_path}: {e}")
        
        logger.info(f"共复制 {copied_count} 个附件")
        return copied_count
    
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
                
                # 记录文件名映射
                for note in date_notes:
                    self.note_id_to_filename[note.note_id] = filename
                
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
        """每条笔记单独创建文件"""
        stats = {'files': 0, 'notes': 0, 'errors': 0}
        
        for note in notes:
            try:
                # 生成文件名
                if self.preserve_time:
                    filename = f"{note.note_id}.md"
                else:
                    filename = f"flomo-{note.datetime.strftime('%Y-%m-%d')}-{stats['files']:04d}.md"
                
                filepath = self.output_dir / filename
                
                # 记录文件名映射
                self.note_id_to_filename[note.note_id] = filename
                
                # 生成文件内容
                content = self._generate_individual_note(note)
                
                # 写入文件
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                stats['files'] += 1
                stats['notes'] += 1
                
            except Exception as e:
                logger.error(f"创建笔记文件失败 {note.note_id}: {e}")
                stats['errors'] += 1
        
        logger.info(f"创建了 {stats['files']} 个文件")
        return stats
    
    def _convert_single(self, notes: List[FlomoNote]) -> Dict[str, int]:
        """所有笔记合并到一个文件"""
        stats = {'files': 0, 'notes': 0, 'errors': 0}
        
        try:
            filename = "flomo-all-notes.md"
            filepath = self.output_dir / filename
            
            # 记录文件名映射
            for note in notes:
                self.note_id_to_filename[note.note_id] = filename
            
            # 生成文件内容
            content = self._generate_single_file(notes)
            
            # 写入文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            stats['files'] = 1
            stats['notes'] = len(notes)
            logger.info(f"创建单个文件: {filename} ({len(notes)} 条笔记)")
            
        except Exception as e:
            logger.error(f"创建单个文件失败: {e}")
            stats['errors'] += 1
        
        return stats
    
    def _generate_daily_note(self, date: str, notes: List[FlomoNote]) -> str:
        """生成每日笔记内容"""
        # 收集所有标签
        all_tags = set()
        for note in notes:
            all_tags.update(note.tags)
        
        # 添加标签前缀
        if self.tag_prefix:
            all_tags = {f"{self.tag_prefix}{tag}" for tag in all_tags}
        
        # 添加默认的 flomo 标签
        if self.tag_prefix:
            all_tags.add(f"{self.tag_prefix}flomo")
        else:
            all_tags.add("flomo")
        
        # Frontmatter
        lines = [
            "---",
            f"date: {date}",
            "source: flomo",
            f"tags: [{', '.join(sorted(all_tags))}]",
            f"note_count: {len(notes)}",
            "---",
            "",
            f"# Flomo Notes - {date}",
            ""
        ]
        
        # 按时间排序笔记
        sorted_notes = sorted(notes, key=lambda n: n.datetime)
        
        for note in sorted_notes:
            lines.extend(self._format_note_content(note))
            lines.append("")
            lines.append("---")
            lines.append("")
        
        return "\n".join(lines)
    
    def _generate_individual_note(self, note: FlomoNote) -> str:
        """生成单个笔记文件内容"""
        # 添加标签前缀
        tags = note.tags.copy()
        if self.tag_prefix:
            tags = [f"{self.tag_prefix}{tag}" for tag in tags]
            tags.append(f"{self.tag_prefix}flomo")
        else:
            tags.append("flomo")
        
        # Frontmatter
        lines = [
            "---",
            f"created: {note.timestamp}",
            "source: flomo",
            f"tags: [{', '.join(tags)}]",
            f"note_id: {note.note_id}",
            "---",
            ""
        ]
        
        lines.extend(self._format_note_content(note))
        
        return "\n".join(lines)
    
    def _generate_single_file(self, notes: List[FlomoNote]) -> str:
        """生成单个文件内容"""
        # 收集所有标签
        all_tags = set()
        for note in notes:
            all_tags.update(note.tags)
        
        # 添加标签前缀
        if self.tag_prefix:
            all_tags = {f"{self.tag_prefix}{tag}" for tag in all_tags}
            all_tags.add(f"{self.tag_prefix}flomo")
        else:
            all_tags.add("flomo")
        
        # Frontmatter
        lines = [
            "---",
            "title: Flomo All Notes",
            "source: flomo",
            f"tags: [{', '.join(sorted(all_tags))}]",
            f"note_count: {len(notes)}",
            "---",
            "",
            "# All Flomo Notes",
            ""
        ]
        
        # 按时间排序笔记
        sorted_notes = sorted(notes, key=lambda n: n.datetime)
        
        for note in sorted_notes:
            lines.append(f"## {note.timestamp}")
            lines.append("")
            lines.extend(self._format_note_content(note, skip_timestamp=True))
            lines.append("")
            lines.append("---")
            lines.append("")
        
        return "\n".join(lines)
    
    def _format_note_content(self, note: FlomoNote, skip_timestamp: bool = False) -> List[str]:
        """格式化单条笔记内容"""
        lines = []
        
        if not skip_timestamp:
            lines.append(f"## {note.timestamp}")
            lines.append("")
        
        # 处理内容中的关联链接
        content = note.content
        
        # 转换关联链接为双链
        if self.convert_to_wikilinks and note.related_ids:
            for memo_id in note.related_ids:
                # 查找对应的 note_id
                related_note_id = self.memo_id_to_note_id.get(memo_id)
                if related_note_id:
                    # 替换 flomo 链接为 Obsidian 双链
                    pattern = rf'关联自[：:]\s*https?://v\.flomoapp\.com/mine/\?memo_id={memo_id}'
                    replacement = f'关联笔记：[[#{related_note_id}]]'
                    content = re.sub(pattern, replacement, content)
                    
                    # 也替换纯链接
                    pattern2 = rf'https?://v\.flomoapp\.com/mine/\?memo_id={memo_id}'
                    replacement2 = f'[[#{related_note_id}]]'
                    content = re.sub(pattern2, replacement2, content)
                else:
                    logger.debug(f"未找到关联笔记的映射: memo_id={memo_id}")
        
        lines.append(content)
        
        # 添加附件
        if note.attachments:
            lines.append("")
            lines.append("### 附件")
            lines.append("")
            
            for attachment in note.attachments:
                if attachment['type'] == 'image':
                    if 'obsidian_path' in attachment:
                        lines.append(f"![[{attachment['obsidian_path']}]]")
                    else:
                        lines.append(f"<!-- 图片附件: {attachment['src']} -->")
                
                elif attachment['type'] == 'audio':
                    if 'obsidian_path' in attachment:
                        lines.append(f"![[{attachment['obsidian_path']}]]")
                        # 如果有转写文本，添加到下方
                        if attachment.get('transcription'):
                            lines.append("")
                            lines.append("**语音转写：**")
                            lines.append("")
                            lines.append(f"> {attachment['transcription']}")
                    else:
                        lines.append(f"<!-- 音频附件: {attachment['src']} -->")
                        if attachment.get('transcription'):
                            lines.append("")
                            lines.append("**语音转写：**")
                            lines.append("")
                            lines.append(f"> {attachment['transcription']}")
                
                lines.append("")
        
        return lines


def main():
    parser = argparse.ArgumentParser(
        description='将 flomo 导出的 HTML 转换为 Obsidian markdown 格式（支持附件和双链）'
    )
    parser.add_argument('--input', '-i', required=True, help='flomo HTML 文件路径')
    parser.add_argument('--output', '-o', required=True, help='Obsidian vault 输出目录')
    parser.add_argument('--mode', '-m', choices=['by-date', 'individual', 'single'],
                       default='by-date', help='组织模式')
    parser.add_argument('--tag-prefix', default='', help='标签前缀（如 "flomo/"）')
    parser.add_argument('--preserve-time', action='store_true', help='在文件名中保留时间')
    parser.add_argument('--no-attachments', action='store_true', help='不复制附件')
    parser.add_argument('--no-wikilinks', action='store_true', help='不转换为双链')
    parser.add_argument('--encoding', default='utf-8', help='HTML 文件编码')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细日志')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # 解析 flomo HTML
        parser = FlomoParser(args.input, encoding=args.encoding)
        notes = parser.parse()
        
        if not notes:
            logger.error("没有找到任何笔记")
            return 1
        
        # 转换为 Obsidian 格式
        html_dir = Path(args.input).parent
        converter = ObsidianConverter(
            output_dir=args.output,
            flomo_html_dir=html_dir,
            mode=args.mode,
            tag_prefix=args.tag_prefix,
            preserve_time=args.preserve_time,
            copy_attachments=not args.no_attachments,
            convert_to_wikilinks=not args.no_wikilinks
        )
        
        stats = converter.convert(notes)
        
        # 输出统计
        print("\n转换完成！")
        print(f"  创建文件: {stats['files']}")
        print(f"  转换笔记: {stats['notes']}")
        print(f"  复制附件: {stats.get('attachments', 0)}")
        print(f"  错误数量: {stats['errors']}")
        print(f"  输出目录: {args.output}")
        
        return 0
        
    except Exception as e:
        logger.error(f"转换失败: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
