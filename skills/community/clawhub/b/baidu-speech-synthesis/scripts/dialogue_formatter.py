#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对话文本格式化模块
将原始对话文本转换为SSML格式，支持多角色音色映射
"""

import re
import xml.etree.ElementTree as ET
from typing import Dict, List, Tuple, Optional
from xml.dom import minidom

class VoiceMapper:
    """音色映射管理器"""
    
    # 百度音色代码表（部分常用音色）
    VOICE_CODES = {
        # 标准音色
        0: "度小美",      # 女声，情感丰富
        1: "度小宇",      # 男声，成熟稳重
        3: "度逍遥",      # 男声，亲切自然
        4: "度丫丫",      # 女声，可爱童声
        5: "度小娇",      # 女声，活泼俏皮
        
        # 精品音色
        103: "度米朵",    # 女声，温柔知性
        106: "度博文",    # 男声，磁性播音
        110: "度小童",    # 童声，天真活泼
        111: "度小萌",    # 女声，甜美可爱
        5003: "度小鹿",   # 女声，清新自然
        5118: "度小乐",   # 男声，阳光活力
    }
    
    # 默认角色映射
    DEFAULT_ROLE_MAP = {
        "小明": 1,      # 度小宇
        "小红": 0,      # 度小美
        "老师": 106,    # 度博文
        "爸爸": 3,      # 度逍遥
        "妈妈": 0,      # 度小美
        "孩子": 4,      # 度丫丫
        "男孩": 1,      # 度小宇
        "女孩": 0,      # 度小美
        "男": 1,        # 度小宇
        "女": 0,        # 度小美
    }
    
    @classmethod
    def get_voice_name(cls, code: int) -> str:
        """获取音色名称"""
        return cls.VOICE_CODES.get(code, f"未知音色({code})")
    
    @classmethod
    def get_voice_code(cls, name: str) -> Optional[int]:
        """通过音色名称获取代码（模糊匹配）"""
        name = name.strip()
        
        # 精确匹配
        for code, voice_name in cls.VOICE_CODES.items():
            if voice_name == name:
                return code
        
        # 模糊匹配
        for code, voice_name in cls.VOICE_CODES.items():
            if name in voice_name or voice_name in name:
                return code
        
        # 尝试解析数字
        try:
            code = int(name)
            if code in cls.VOICE_CODES:
                return code
        except ValueError:
            pass
        
        return None
    
    @classmethod
    def list_voices(cls) -> List[Tuple[int, str]]:
        """列出所有可用音色"""
        return [(code, name) for code, name in sorted(cls.VOICE_CODES.items())]

class DialogueFormatter:
    """对话格式化器"""
    
    def __init__(self):
        self.voice_mapper = VoiceMapper()
    
    def parse_dialogue_lines(self, text: str) -> List[Tuple[str, str]]:
        """
        解析对话文本，提取角色和台词
        
        Args:
            text: 原始对话文本，如:
                小明：你好吗？
                小红：我很好，谢谢！
                
        Returns:
            List[(角色, 台词)]
        """
        lines = []
        
        # 支持多种分隔符：中文冒号、英文冒号、破折号等
        for line in text.strip().split('\n'):
            line = line.strip()
            if not line:
                continue
            
            # 尝试匹配 "角色：台词" 格式
            match = re.match(r'^([^：:]+)[：:]\s*(.+)$', line)
            if match:
                role = match.group(1).strip()
                dialogue = match.group(2).strip()
                lines.append((role, dialogue))
                continue
            
            # 尝试匹配 "角色 - 台词" 格式
            match = re.match(r'^([^-]+)-\s*(.+)$', line)
            if match:
                role = match.group(1).strip()
                dialogue = match.group(2).strip()
                lines.append((role, dialogue))
                continue
            
            # 如果没有明确角色，使用默认角色
            lines.append(("未命名", line))
        
        return lines
    
    def text_to_ssml(self, text: str, voice_map: Dict[str, int] = None) -> str:
        """
        将对话文本转换为SSML格式
        
        Args:
            text: 原始对话文本
            voice_map: 角色->音色代码映射，如 {"小明": 1, "小红": 0}
            
        Returns:
            SSML格式字符串
        """
        if voice_map is None:
            voice_map = VoiceMapper.DEFAULT_ROLE_MAP
        
        lines = self.parse_dialogue_lines(text)
        
        # 创建XML根元素
        root = ET.Element("speak", version="1.0", xmlns="http://www.w3.org/2001/10/synthesis")
        root.set("xml:lang", "zh-CN")
        
        for i, (role, dialogue) in enumerate(lines):
            # 确定音色代码
            voice_code = voice_map.get(role)
            if voice_code is None:
                # 尝试使用默认映射
                voice_code = VoiceMapper.DEFAULT_ROLE_MAP.get(role, 0)
            
            # 获取音色名称
            voice_name = VoiceMapper.get_voice_name(voice_code)
            
            # 创建voice元素
            voice_elem = ET.SubElement(root, "voice", name=voice_name)
            voice_elem.text = f"{role}：{dialogue}"
            
            # 如果不是最后一行，添加停顿
            if i < len(lines) - 1:
                # 根据标点符号判断停顿长度
                if dialogue.endswith(("。", "！", "？")):
                    pause_time = "500ms"
                elif dialogue.endswith(("，", "；")):
                    pause_time = "300ms"
                else:
                    pause_time = "300ms"
                
                ET.SubElement(root, "break", time=pause_time)
        
        # 转换为格式化的XML字符串
        rough_string = ET.tostring(root, encoding="utf-8")
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="  ", encoding="utf-8")
        
        return pretty_xml.decode("utf-8")
    
    def parse_ssml_segments(self, ssml_text: str) -> List[Tuple[str, str, int]]:
        """
        解析SSML，提取分段信息（用于回退方案）
        
        Args:
            ssml_text: SSML格式文本
            
        Returns:
            List[(文本内容, 音色名称, 音色代码)]
        """
        segments = []
        
        try:
            # 解析XML
            root = ET.fromstring(ssml_text)
            
            # 遍历所有元素
            for elem in root.iter():
                if elem.tag.endswith('}voice') or elem.tag == 'voice':
                    # 获取音色名称
                    voice_name = elem.get("name", "度小美")
                    
                    # 获取音色代码
                    voice_code = VoiceMapper.get_voice_code(voice_name)
                    if voice_code is None:
                        voice_code = 0  # 默认度小美
                    
                    # 提取文本
                    text = elem.text or ""
                    
                    # 移除可能包含的角色前缀（格式：角色：台词）
                    if "：" in text:
                        # 保留完整文本，因为API需要整个文本
                        pass
                    
                    if text.strip():
                        segments.append((text.strip(), voice_name, voice_code))
                
                elif elem.tag == "break":
                    # 停顿标记，可以在这里添加静音段
                    # 目前只记录，合并时处理
                    pass
        
        except ET.ParseError:
            # 如果XML解析失败，尝试简单提取
            # 查找<voice>标签
            voice_pattern = r'<voice\s+name="([^"]+)"[^>]*>([^<]+)</voice>'
            matches = re.findall(voice_pattern, ssml_text, re.DOTALL)
            
            for voice_name, text in matches:
                voice_code = VoiceMapper.get_voice_code(voice_name)
                if voice_code is None:
                    voice_code = 0
                
                text = text.strip()
                if text:
                    segments.append((text, voice_name, voice_code))
        
        return segments
    
    def create_simple_ssml(self, text: str, voice_code: int = 0) -> str:
        """
        创建简单的SSML（单音色）
        
        Args:
            text: 要合成的文本
            voice_code: 音色代码
            
        Returns:
            简单SSML字符串
        """
        voice_name = VoiceMapper.get_voice_name(voice_code)
        
        ssml = f'''<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="zh-CN">
  <voice name="{voice_name}">
    {text}
  </voice>
</speak>'''
        
        return ssml
    
    def validate_ssml(self, ssml_text: str) -> Tuple[bool, str]:
        """
        验证SSML格式
        
        Args:
            ssml_text: SSML文本
            
        Returns:
            (是否有效, 错误信息)
        """
        # 检查长度（百度限制1024字节）
        byte_length = len(ssml_text.encode("utf-8"))
        if byte_length > 1024:
            return False, f"SSML 超过 1024 字节限制（当前: {byte_length}）。建议拆分长对话或使用分段合并模式（--merge）。"
        
        # 检查XML格式
        try:
            ET.fromstring(ssml_text)
            return True, f"SSML格式有效（{byte_length}字节）"
        except ET.ParseError as e:
            return False, f"XML解析错误: {e}"
    
    def _split_voice_element(self, voice_elem, max_bytes: int, root_attrs: dict):
        """
        拆分单个voice元素，如果其文本内容过长
        
        Args:
            voice_elem: voice XML元素
            max_bytes: 最大字节数
            root_attrs: 根元素属性
            
        Returns:
            拆分后的voice元素列表
        """
        # 提取原始属性
        voice_attrs = {k: v for k, v in voice_elem.attrib.items()}
        original_text = voice_elem.text or ""
        
        # 如果文本为空，直接返回原元素
        if not original_text.strip():
            return [voice_elem]
        
        # 计算voice标签本身的字节数（不包括文本）
        voice_start = f'<voice'
        for k, v in voice_attrs.items():
            voice_start += f' {k}="{v}"'
        voice_start += '>'
        voice_end = '</voice>'
        tag_bytes = len((voice_start + voice_end).encode('utf-8'))
        
        # 可用于文本的最大字节数
        max_text_bytes = max_bytes - tag_bytes
        
        # 如果标签本身已经超过限制，无法处理
        if tag_bytes >= max_bytes:
            print(f"错误: voice标签本身 ({tag_bytes} 字节) 已超过最大限制 {max_bytes}，无法拆分")
            return [voice_elem]
        
        # 按句子拆分文本
        sentences = self._split_text_by_sentences(original_text, max_text_bytes)
        
        voice_elements = []
        for sentence in sentences:
            # 创建新的voice元素
            new_elem = ET.Element("voice", voice_attrs)
            new_elem.text = sentence
            voice_elements.append(new_elem)
        
        print(f"已将voice元素拆分为 {len(voice_elements)} 个部分")
        return voice_elements
    
    def _split_text_by_sentences(self, text: str, max_bytes_per_sentence: int):
        """
        按句子拆分文本，确保每句不超过最大字节数
        
        Args:
            text: 原始文本
            max_bytes_per_sentence: 每句最大字节数
            
        Returns:
            句子列表
        """
        if len(text.encode('utf-8')) <= max_bytes_per_sentence:
            return [text]
        
        # 中文句子分隔符
        sentence_delimiters = ['。', '！', '？', '；', ';', '.', '!', '?']
        
        sentences = []
        current_sentence = ""
        
        for char in text:
            current_sentence += char
            
            # 检查当前句子是否超过限制
            if len(current_sentence.encode('utf-8')) > max_bytes_per_sentence:
                # 如果已经积累了一些内容，先保存
                if len(current_sentence[:-1].encode('utf-8')) > 0:
                    sentences.append(current_sentence[:-1])
                    current_sentence = char  # 从当前字符重新开始
                else:
                    # 单个字符就超过限制了（罕见情况），强制拆分
                    sentences.append(char)
                    current_sentence = ""
            
            # 检查句子结束符
            elif char in sentence_delimiters:
                sentences.append(current_sentence)
                current_sentence = ""
        
        # 添加剩余部分
        if current_sentence:
            sentences.append(current_sentence)
        
        # 如果拆分后仍有句子过长，进一步按逗号拆分
        final_sentences = []
        for sentence in sentences:
            if len(sentence.encode('utf-8')) > max_bytes_per_sentence:
                # 按逗号进一步拆分
                sub_sentences = self._split_text_by_commas(sentence, max_bytes_per_sentence)
                final_sentences.extend(sub_sentences)
            else:
                final_sentences.append(sentence)
        
        return final_sentences
    
    def _split_text_by_commas(self, text: str, max_bytes_per_segment: int):
        """
        按逗号拆分文本
        
        Args:
            text: 文本
            max_bytes_per_segment: 每段最大字节数
            
        Returns:
            段落列表
        """
        if len(text.encode('utf-8')) <= max_bytes_per_segment:
            return [text]
        
        # 中文逗号分隔符
        comma_delimiters = ['，', ',', '、']
        
        segments = []
        current_segment = ""
        
        for char in text:
            current_segment += char
            
            if len(current_segment.encode('utf-8')) > max_bytes_per_segment:
                if len(current_segment[:-1].encode('utf-8')) > 0:
                    segments.append(current_segment[:-1])
                    current_segment = char
                else:
                    segments.append(char)
                    current_segment = ""
            
            elif char in comma_delimiters:
                segments.append(current_segment)
                current_segment = ""
        
        if current_segment:
            segments.append(current_segment)
        
        # 如果仍有段落过长，按长度硬拆分
        final_segments = []
        for segment in segments:
            if len(segment.encode('utf-8')) > max_bytes_per_segment:
                # 硬拆分为固定长度
                hard_split = self._split_text_hard(segment, max_bytes_per_segment)
                final_segments.extend(hard_split)
            else:
                final_segments.append(segment)
        
        return final_segments
    
    def _split_text_hard(self, text: str, max_bytes_per_segment: int):
        """
        硬拆分文本为固定长度
        
        Args:
            text: 文本
            max_bytes_per_segment: 每段最大字节数
            
        Returns:
            文本段列表
        """
        encoded = text.encode('utf-8')
        segments = []
        
        for i in range(0, len(encoded), max_bytes_per_segment):
            segment_bytes = encoded[i:i + max_bytes_per_segment]
            segment = segment_bytes.decode('utf-8', errors='ignore')
            segments.append(segment)
        
        return segments
    
    def _create_speak_segment(self, elements, root_attrs: dict):
        """
        创建完整的speak片段
        
        Args:
            elements: 元素列表
            root_attrs: 根元素属性
            
        Returns:
            格式化的SSML字符串
        """
        # 创建根元素
        root = ET.Element("speak", root_attrs)
        
        # 添加所有元素
        for elem in elements:
            root.append(elem)
        
        # 转换为格式化的XML
        rough_string = ET.tostring(root, encoding="utf-8")
        
        # 使用minidom美化输出
        try:
            from xml.dom import minidom
            reparsed = minidom.parseString(rough_string)
            pretty_xml = reparsed.toprettyxml(indent="  ", encoding="utf-8")
            return pretty_xml.decode("utf-8")
        except Exception:
            return rough_string.decode("utf-8")  # Fallback on XML formatting error
    
    def _split_long_ssml_fallback(self, ssml_text: str, max_bytes: int = 1024):
        """
        回退方法：使用正则表达式拆分SSML
        
        Args:
            ssml_text: 原始SSML文本
            max_bytes: 最大字节数
            
        Returns:
            SSML片段列表
        """
        print("使用回退方法拆分SSML")
        
        if len(ssml_text.encode("utf-8")) <= max_bytes:
            return [ssml_text]
        
        segments = []
        
        # 提取所有voice元素内容
        voice_pattern = r'(<voice[^>]*>.*?</voice>)'
        voice_matches = list(re.finditer(voice_pattern, ssml_text, re.DOTALL))
        
        current_segment = '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="zh-CN">\n'
        
        for match in voice_matches:
            voice_tag = match.group(0)
            
            # 如果添加这个voice_tag会超长，则开始新片段
            temp_segment = current_segment + voice_tag + "\n</speak>"
            if len(temp_segment.encode("utf-8")) > max_bytes:
                # 结束当前片段
                if current_segment.count("<voice") > 0:
                    current_segment += "</speak>"
                    segments.append(current_segment)
                
                # 开始新片段
                current_segment = '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="zh-CN">\n'
            
            current_segment += voice_tag + "\n"
        
        # 添加最后一个片段
        if current_segment.count("<voice") > 0:
            current_segment += "</speak>"
            segments.append(current_segment)
        
        print(f"回退方法拆分成 {len(segments)} 个片段")
        return segments
    
    def split_long_ssml(self, ssml_text: str, max_bytes: int = 1024) -> List[str]:
        """
        拆分过长的SSML为多个片段
        
        Args:
            ssml_text: 原始SSML文本
            max_bytes: 最大字节数
            
        Returns:
            SSML片段列表
        """
        original_bytes = len(ssml_text.encode("utf-8"))
        if original_bytes <= max_bytes:
            return [ssml_text]
        
        print(f"开始拆分SSML: 原始大小 {original_bytes} 字节，目标最大 {max_bytes} 字节")
        
        segments = []
        try:
            # 解析XML
            root = ET.fromstring(ssml_text)
            
            # 检查根元素是否为speak（处理命名空间）
            if not root.tag.endswith('}speak') and root.tag != 'speak':
                raise ValueError("SSML必须以<speak>根元素开始")
            
            # 提取根元素属性
            root_attrs = {k: v for k, v in root.attrib.items()}
            
            current_segment_elements = []
            current_size = 0
            
            # 遍历所有子元素
            for i, elem in enumerate(list(root)):
                elem_str = ET.tostring(elem, encoding="utf-8").decode("utf-8").strip()
                elem_bytes = len(elem_str.encode("utf-8"))
                
                print(f"处理元素 {i+1}: {elem.tag} ({elem_bytes} 字节)")
                
                # 如果单个元素已经超过最大限制
                if elem_bytes > max_bytes and (elem.tag.endswith('}voice') or elem.tag == 'voice'):
                    print(f"警告: 单个<voice>元素超过最大限制 ({elem_bytes} > {max_bytes})，尝试拆分内部文本")
                    
                    # 尝试拆分voice元素内部的文本
                    voice_segments = self._split_voice_element(elem, max_bytes, root_attrs)
                    
                    for j, voice_segment in enumerate(voice_segments):
                        voice_segment_str = ET.tostring(voice_segment, encoding="utf-8").decode("utf-8").strip()
                        voice_segment_bytes = len(voice_segment_str.encode("utf-8"))
                        
                        # 如果当前片段加上这个voice会超长，则创建新片段
                        if current_size + voice_segment_bytes > max_bytes and current_segment_elements:
                            # 完成当前片段
                            segment = self._create_speak_segment(current_segment_elements, root_attrs)
                            segments.append(segment)
                            print(f"创建片段 {len(segments)}: {len(segment.encode('utf-8'))} 字节，包含 {len(current_segment_elements)} 个元素")
                            
                            # 重置
                            current_segment_elements = []
                            current_size = 0
                        
                        current_segment_elements.append(voice_segment)
                        current_size += voice_segment_bytes
                        print(f"添加拆分的voice子元素 {j+1}/{len(voice_segments)} ({voice_segment_bytes} 字节)")
                else:
                    # 检查添加当前元素是否会超长
                    if current_size + elem_bytes > max_bytes and current_segment_elements:
                        # 完成当前片段
                        segment = self._create_speak_segment(current_segment_elements, root_attrs)
                        segments.append(segment)
                        print(f"创建片段 {len(segments)}: {len(segment.encode('utf-8'))} 字节，包含 {len(current_segment_elements)} 个元素")
                        
                        # 重置
                        current_segment_elements = []
                        current_size = 0
                    
                    current_segment_elements.append(elem)
                    current_size += elem_bytes
            
            # 添加最后一个片段
            if current_segment_elements:
                segment = self._create_speak_segment(current_segment_elements, root_attrs)
                segments.append(segment)
                print(f"创建片段 {len(segments)}: {len(segment.encode('utf-8'))} 字节，包含 {len(current_segment_elements)} 个元素")
                
        except ET.ParseError as e:
            print(f"XML解析失败，使用回退方法: {e}")
            # 回退到原始简单方法
            return self._split_long_ssml_fallback(ssml_text, max_bytes)
        
        print(f"拆分完成: 共 {len(segments)} 个片段，总字节数 {sum(len(s.encode('utf-8')) for s in segments)}")
        return segments

def main():
    """命令行测试"""
    import argparse
    
    parser = argparse.ArgumentParser(description="对话文本格式化工具")
    parser.add_argument("--input", "-i", required=True, help="输入文本文件")
    parser.add_argument("--output", "-o", help="输出SSML文件（默认: 输出到控制台）")
    parser.add_argument("--map", "-m", nargs="+", help="角色映射，如 '小明:1' '小红:0'")
    parser.add_argument("--list-voices", action="store_true", help="列出所有可用音色")
    
    args = parser.parse_args()
    
    if args.list_voices:
        print("可用音色列表:")
        for code, name in VoiceMapper.list_voices():
            print(f"  {code:4d}: {name}")
        return
    
    # 读取输入文件
    with open(args.input, "r", encoding="utf-8") as f:
        text = f.read()
    
    # 创建格式化器
    formatter = DialogueFormatter()
    
    # 解析角色映射
    voice_map = {}
    if args.map:
        for mapping in args.map:
            if ":" in mapping:
                role, voice = mapping.split(":", 1)
                try:
                    voice_map[role.strip()] = int(voice.strip())
                except ValueError:
                    print(f"警告: 无效音色代码 '{voice}'")
    
    # 转换为SSML
    ssml = formatter.text_to_ssml(text, voice_map)
    
    # 验证
    is_valid, message = formatter.validate_ssml(ssml)
    print(f"验证: {message}")
    
    # 输出
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(ssml)
        print(f"SSML已保存到: {args.output}")
    else:
        print("\n生成的SSML:")
        print("=" * 50)
        print(ssml)
        print("=" * 50)

if __name__ == "__main__":
    main()