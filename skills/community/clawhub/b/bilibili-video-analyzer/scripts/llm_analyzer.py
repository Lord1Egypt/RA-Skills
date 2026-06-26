"""
LLM 内容分析器

功能:
- 构造结构化分析 prompt
- 与 LLM 交互(交互式或 API)
- 解析和验证 LLM 返回的分析结果
"""

import json
import sys
from typing import Dict, List, Any, Optional
from pathlib import Path


def build_analysis_prompt(video_info: Dict, srt_content: str) -> str:
    """构造 LLM 分析 prompt
    
    Args:
        video_info: 视频信息字典,包含:
                   - title: 标题
                   - owner: UP主信息 {'name': ...}
                   - duration: 时长(秒)
                   - bvid: BV号
        srt_content: 完整 SRT 字幕内容
    
    Returns:
        str: 格式化的分析 prompt
    """
    title = video_info.get('title', '未知标题')
    author = video_info.get('owner', {}).get('name', '未知UP主')
    duration = video_info.get('duration', 0)
    bvid = video_info.get('bvid', '')
    
    # 计算时长的可读格式
    duration_mins = int(duration // 60)
    duration_secs = int(duration % 60)
    duration_str = f"{duration_mins}分{duration_secs}秒"
    
    prompt = f"""你是一位专业的学术内容分析专家。请深度分析以下学术视频的字幕内容,提取关键学术信息。

**视频信息**:
- 标题: {title}
- UP主: {author}
- BV号: {bvid}
- 时长: {duration_str} ({duration}秒)

**完整字幕内容**:
```
{srt_content}
```

**分析要求**:
1. **内容摘要**: 用100-200字概括视频核心内容,使用学术化表述
2. **章节划分**: 根据内容逻辑划分3-6个章节,每章节包含时间范围和内容描述
3. **知识点提取**: 提取10-20个关键知识点,按重要程度排序,包含详细说明
4. **关键截图**: 识别6-10个需要截图的关键时间点(图表、公式、演示、重要概念等)
5. **专业术语**: 提取10-15个重要的专业术语及其定义

**输出格式**: 请严格按照以下 JSON 格式返回分析结果(不要包含任何其他文字):

```json
{{
  "summary": "视频内容摘要,使用专业学术表述,100-200字",
  "chapters": [
    {{
      "title": "章节标题",
      "start_time": 开始时间(秒数,浮点数),
      "end_time": 结束时间(秒数,浮点数),
      "description": "章节内容描述,专业表述"
    }}
  ],
  "knowledge_points": [
    {{
      "title": "知识点标题",
      "content": "知识点详细内容,使用专业术语和学术表达",
      "timestamp": 相关时间戳(秒数,浮点数),
      "importance": "重要程度: high/medium/low"
    }}
  ],
  "key_screenshots": [
    {{
      "timestamp": 时间戳(秒数,浮点数),
      "description": "截图内容说明(图表类型、公式、演示内容等)",
      "reason": "为什么需要截取这个画面(学术价值说明)"
    }}
  ],
  "terms": [
    {{
      "term": "专业术语名称",
      "definition": "术语的学术定义"
    }}
  ]
}}
```

**注意事项**:
- 所有时间戳必须是数字(秒数),不要使用字符串格式
- 知识点按重要程度从高到低排序
- 截图时间点优先选择包含图表、公式、关键概念展示的画面
- 专业术语定义要准确、简洁
- 使用专业学术表述,避免口语化
- 确保JSON格式完全正确,可以被解析

请开始分析并返回标准JSON格式的结果。"""
    
    return prompt


def interactive_analyze(video_info: Dict, srt_content: str) -> Dict[str, Any]:
    """交互式 LLM 分析
    
    由于当前环境无法直接调用 LLM API,采用交互式方式:
    1. 输出分析 prompt
    2. 用户复制 prompt 发送给 LLM
    3. 用户将 LLM 返回的 JSON 粘贴回来
    4. 解析并验证 JSON 结果
    
    Args:
        video_info: 视频信息
        srt_content: 字幕内容
    
    Returns:
        Dict: 解析后的分析结果
    
    Raises:
        ValueError: JSON 格式错误或验证失败
    """
    # 构造 prompt
    prompt = build_analysis_prompt(video_info, srt_content)
    
    # 输出 prompt
    print("\n" + "=" * 70)
    print("📋 LLM 分析 Prompt")
    print("=" * 70)
    print("\n请将以下内容复制并发送给 LLM (如 Claude、GPT-4 等):\n")
    print(prompt)
    print("\n" + "=" * 70)
    print("📥 等待 LLM 响应")
    print("=" * 70)
    print("\n请将 LLM 返回的 JSON 结果粘贴到下方,然后:")
    print("  - macOS/Linux: 按 Ctrl+D 结束输入")
    print("  - Windows: 按 Ctrl+Z 然后回车\n")
    print("提示: 只粘贴 JSON 部分(以 { 开头, } 结尾),不要包含其他文字\n")
    print("开始输入:")
    print("-" * 70)
    
    # 读取用户输入
    lines = []
    try:
        for line in sys.stdin:
            lines.append(line)
    except KeyboardInterrupt:
        print("\n\n❌ 用户取消输入")
        sys.exit(1)
    
    response = ''.join(lines).strip()
    
    if not response:
        raise ValueError("未收到任何输入")
    
    print("-" * 70)
    print(f"\n✅ 已接收 {len(response)} 字符的响应\n")
    
    # 解析 JSON
    result = parse_llm_response(response)
    
    # 验证结果
    validate_analysis_result(result)
    
    # 输出统计信息
    print("✅ 分析结果验证通过")
    print(f"\n📊 分析统计:")
    print(f"  - 章节数: {len(result['chapters'])}")
    print(f"  - 知识点数: {len(result['knowledge_points'])}")
    print(f"  - 关键截图: {len(result['key_screenshots'])}")
    print(f"  - 专业术语: {len(result['terms'])}")
    print()
    
    return result


def parse_llm_response(response: str) -> Dict[str, Any]:
    """解析 LLM 返回的 JSON 响应
    
    Args:
        response: LLM 返回的原始文本
    
    Returns:
        Dict: 解析后的 JSON 对象
    
    Raises:
        ValueError: JSON 格式错误
    """
    # 尝试提取 JSON 部分
    # 可能的格式:
    # 1. 纯 JSON: {...}
    # 2. Markdown代码块: ```json {...} ```
    # 3. 带前后文字的: ...前文... {...} ...后文...
    
    # 移除首尾空白
    response = response.strip()
    
    # 尝试移除 Markdown 代码块标记
    if response.startswith('```'):
        # 移除开头的 ```json 或 ```
        lines = response.split('\n')
        lines = lines[1:]  # 移除第一行
        
        # 移除结尾的 ```
        if lines and lines[-1].strip() == '```':
            lines = lines[:-1]
        
        response = '\n'.join(lines).strip()
    
    # 尝试查找 JSON 对象
    # 从第一个 { 到最后一个 }
    start_idx = response.find('{')
    end_idx = response.rfind('}')
    
    if start_idx == -1 or end_idx == -1 or start_idx >= end_idx:
        raise ValueError(
            "未找到有效的 JSON 对象\n"
            "请确保粘贴的内容包含完整的 JSON (以 { 开头, } 结尾)"
        )
    
    json_str = response[start_idx:end_idx+1]
    
    # 解析 JSON
    try:
        data = json.loads(json_str)
        return data
    except json.JSONDecodeError as e:
        raise ValueError(
            f"JSON 解析失败: {e}\n\n"
            f"请检查 JSON 格式是否正确,可以使用在线工具验证:\n"
            f"https://jsonlint.com/\n\n"
            f"提取的 JSON 内容:\n{json_str[:500]}..."
        )


def validate_analysis_result(result: Dict[str, Any]) -> None:
    """验证分析结果的完整性和正确性
    
    Args:
        result: 分析结果字典
    
    Raises:
        ValueError: 验证失败
    """
    required_fields = ['summary', 'chapters', 'knowledge_points', 'key_screenshots', 'terms']
    
    # 检查必需字段
    for field in required_fields:
        if field not in result:
            raise ValueError(f"缺少必需字段: {field}")
    
    # 验证 summary
    if not isinstance(result['summary'], str) or len(result['summary']) < 50:
        raise ValueError("摘要(summary)长度不足或格式错误")
    
    # 验证 chapters
    if not isinstance(result['chapters'], list) or len(result['chapters']) < 2:
        raise ValueError("章节(chapters)数量不足(至少需要2个)")
    
    for i, chapter in enumerate(result['chapters']):
        required = ['title', 'start_time', 'end_time', 'description']
        for field in required:
            if field not in chapter:
                raise ValueError(f"章节 {i+1} 缺少字段: {field}")
        
        # 验证时间戳为数字
        if not isinstance(chapter['start_time'], (int, float)):
            raise ValueError(f"章节 {i+1} 的 start_time 必须是数字")
        if not isinstance(chapter['end_time'], (int, float)):
            raise ValueError(f"章节 {i+1} 的 end_time 必须是数字")
        
        # 验证时间范围合理
        if chapter['start_time'] >= chapter['end_time']:
            raise ValueError(f"章节 {i+1} 的时间范围不合理")
    
    # 验证 knowledge_points
    if not isinstance(result['knowledge_points'], list) or len(result['knowledge_points']) < 5:
        raise ValueError("知识点(knowledge_points)数量不足(至少需要5个)")
    
    for i, kp in enumerate(result['knowledge_points']):
        required = ['title', 'content', 'timestamp', 'importance']
        for field in required:
            if field not in kp:
                raise ValueError(f"知识点 {i+1} 缺少字段: {field}")
        
        if not isinstance(kp['timestamp'], (int, float)):
            raise ValueError(f"知识点 {i+1} 的 timestamp 必须是数字")
        
        if kp['importance'] not in ['high', 'medium', 'low']:
            raise ValueError(f"知识点 {i+1} 的 importance 必须是 high/medium/low")
    
    # 验证 key_screenshots
    if not isinstance(result['key_screenshots'], list) or len(result['key_screenshots']) < 3:
        raise ValueError("关键截图(key_screenshots)数量不足(至少需要3个)")
    
    for i, screenshot in enumerate(result['key_screenshots']):
        required = ['timestamp', 'description', 'reason']
        for field in required:
            if field not in screenshot:
                raise ValueError(f"截图 {i+1} 缺少字段: {field}")
        
        if not isinstance(screenshot['timestamp'], (int, float)):
            raise ValueError(f"截图 {i+1} 的 timestamp 必须是数字")
    
    # 验证 terms
    if not isinstance(result['terms'], list) or len(result['terms']) < 3:
        raise ValueError("专业术语(terms)数量不足(至少需要3个)")
    
    for i, term in enumerate(result['terms']):
        required = ['term', 'definition']
        for field in required:
            if field not in term:
                raise ValueError(f"术语 {i+1} 缺少字段: {field}")


def save_analysis_result(result: Dict[str, Any], output_path: Path) -> None:
    """保存分析结果为 JSON 文件
    
    Args:
        result: 分析结果
        output_path: 输出文件路径
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 分析结果已保存: {output_path}")


def load_analysis_result(input_path: Path) -> Dict[str, Any]:
    """从 JSON 文件加载分析结果
    
    Args:
        input_path: JSON 文件路径
    
    Returns:
        Dict: 分析结果
    """
    input_path = Path(input_path)
    
    if not input_path.exists():
        raise FileNotFoundError(f"文件不存在: {input_path}")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        result = json.load(f)
    
    # 验证加载的结果
    validate_analysis_result(result)
    
    return result


if __name__ == '__main__':
    # 测试代码
    print("LLM 分析器测试\n")
    
    # 模拟视频信息
    test_video_info = {
        'title': '细胞培养技术详解',
        'owner': {'name': '生物学讲堂'},
        'duration': 600,
        'bvid': 'BV1test123'
    }
    
    test_srt_content = """1
00:00:00,000 --> 00:00:05,000
大家好,今天我们讲解细胞培养的基本技术

2
00:00:05,000 --> 00:00:10,000
首先介绍什么是细胞培养..."""
    
    # 构造 prompt
    prompt = build_analysis_prompt(test_video_info, test_srt_content)
    
    print("生成的 Prompt:")
    print("=" * 70)
    print(prompt)
    print("=" * 70)
