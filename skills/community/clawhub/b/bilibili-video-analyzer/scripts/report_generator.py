"""
Markdown 报告生成器（清洁版学习笔记风格）

功能:
- 生成 📌 知识点卡片式学习笔记
- 包含核心概念、详细说明、关键要点
- 配合截图，简洁专业
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


def format_duration(seconds: float) -> str:
    """格式化时长为可读字符串
    
    Args:
        seconds: 秒数
    
    Returns:
        str: 格式化字符串,如 "10分35秒" 或 "1小时05分20秒"
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours}小时{minutes:02d}分{secs:02d}秒"
    else:
        return f"{minutes}分{secs:02d}秒"


def generate_markdown(
    video_info: Dict,
    analysis: Dict[str, Any],
    screenshots: Dict[float, Path],
    srt_content: str,
    output_dir: Path,
    template: Optional[str] = None
) -> Path:
    """生成完整的 Markdown 报告（清洁版学习笔记风格）
    
    Args:
        video_info: 视频信息
        analysis: LLM 分析结果，包含:
            - summary: 内容摘要
            - knowledge_points: 知识点列表，每个包含:
                - title: 标题
                - core_concept: 核心概念（一句话）
                - details: 详细说明（Markdown格式）
                - key_points: 关键要点列表
                - timestamp: 时间戳（秒）
            - knowledge_framework: 核心知识框架（可选）
            - practical_value: 实践价值（可选）
            - learning_suggestions: 学习建议列表（可选）
        screenshots: 时间戳到截图路径的映射
        srt_content: 完整字幕内容（未使用）
        output_dir: 输出目录
        template: 自定义模板(可选)
    
    Returns:
        Path: 生成的报告文件路径
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成报告文件名
    title = video_info.get('title', 'video')
    
    # 清理文件名中的非法字符
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_', '(', ')', '，', '。', '"', '"'))
    safe_title = safe_title.strip()[:50]  # 限制长度
    
    report_filename = f"{safe_title}_学习笔记.md"
    report_path = output_dir / report_filename
    
    # 截图目录(假设在 output_dir/screenshots)
    screenshots_dir = output_dir / "screenshots"
    
    # 构建 Markdown 内容
    lines = []
    
    # === 标题 ===
    lines.append(f"# 《{title}》学习笔记")
    lines.append("")
    
    # === 视频信息概览 ===
    duration = video_info.get('duration', 0)
    duration_str = format_duration(duration)
    kp_count = len(analysis.get('knowledge_points', []))
    
    lines.append(f"**视频时长**: {duration_str} | **知识点**: {kp_count} 个")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # === 知识点卡片 ===
    knowledge_points = analysis.get('knowledge_points', [])
    
    for i, kp in enumerate(knowledge_points, 1):
        title_kp = kp.get('title', f'知识点 {i}')
        core_concept = kp.get('core_concept', kp.get('content', ''))
        details = kp.get('details', '')
        key_points = kp.get('key_points', [])
        timestamp = kp.get('timestamp')
        
        # 📌 知识点标题
        lines.append(f"## 📌 {i}. {title_kp}")
        lines.append("")
        
        # 核心概念
        lines.append(f"**核心概念**: {core_concept}")
        lines.append("")
        lines.append("")
        lines.append("")
        
        # 查找对应截图
        closest_screenshot = None
        min_diff = 10.0  # 误差范围10秒
        
        if timestamp:
            for sc_time, sc_path in screenshots.items():
                diff = abs(sc_time - timestamp)
                if diff < min_diff:
                    min_diff = diff
                    closest_screenshot = sc_path
        
        # 插入截图
        if closest_screenshot:
            rel_path = Path(closest_screenshot).relative_to(output_dir)
            lines.append(f'<img src="{rel_path}" width="600" alt="知识点配图"/>')
            lines.append("")
            lines.append("")
        
        # 📖 详细说明
        if details:
            lines.append("### 📖 详细说明")
            lines.append("")
            lines.append(details)
            lines.append("")
        
        # 🔑 关键要点
        if key_points:
            lines.append("### 🔑 关键要点")
            lines.append("")
            for point in key_points:
                lines.append(f"- {point}")
            lines.append("")
        
        lines.append("---")
        lines.append("")
    
    # === 全文总结 ===
    lines.append("## 📚 全文总结")
    lines.append("")
    
    # 核心知识框架
    if 'knowledge_framework' in analysis and analysis['knowledge_framework']:
        lines.append("### 核心知识框架")
        lines.append("")
        lines.append(analysis['knowledge_framework'])
        lines.append("")
    
    # 实践价值
    if 'practical_value' in analysis and analysis['practical_value']:
        lines.append("### 实践价值")
        lines.append("")
        lines.append(analysis['practical_value'])
        lines.append("")
    
    # 学习建议
    if 'learning_suggestions' in analysis and analysis['learning_suggestions']:
        lines.append("### 学习建议")
        lines.append("")
        for i, suggestion in enumerate(analysis['learning_suggestions'], 1):
            lines.append(f"{i}. {suggestion}")
        lines.append("")
    
    # === 页脚 ===
    lines.append("---")
    lines.append("")
    lines.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d')}")
    lines.append("**优化版本**: LLM深度重写版 ✨")
    lines.append("")
    
    # 合并并写入文件
    content = '\n'.join(lines)
    report_path.write_text(content, encoding='utf-8')
    
    print(f"\n✅ 学习笔记已生成: {report_path}")
    
    # 输出统计信息
    file_size = report_path.stat().st_size / 1024  # KB
    print(f"\n📊 报告统计:")
    print(f"  - 文件大小: {file_size:.2f} KB")
    print(f"  - 字符数: {len(content)}")
    print(f"  - 知识点数: {kp_count}")
    print(f"  - 截图数: {len(screenshots)}")
    
    return report_path


if __name__ == '__main__':
    # 测试代码
    print("Markdown 报告生成器测试（清洁版）\n")
    
    # 模拟数据
    test_video_info = {
        'title': '细胞培养技术详解',
        'bvid': 'BV1test123',
        'owner': {'name': '生物学讲堂', 'mid': '12345'},
        'duration': 1128  # 18分48秒
    }
    
    test_analysis = {
        'summary': '本视频系统讲解了细胞培养的基本原理和操作技术。',
        'knowledge_points': [
            {
                'title': '细胞三种基本形态分类',
                'core_concept': '培养细胞按形态特征分为成纤维样、上皮样、淋巴样三类',
                'details': '''细胞培养中存在三种基本形态类型:

1. **成纤维样细胞**: 细胞呈梭形或星形,边界清晰
2. **上皮样细胞**: 细胞呈多边形或铺路石状
3. **淋巴样细胞**: 细胞呈圆形或椭圆形,悬浮生长

**临床意义**: 异常形态提示交叉污染或细胞病变的可能性。''',
                'key_points': [
                    '所有培养细胞必属于三种基本形态之一',
                    '形态分类是判断细胞健康状态的首要依据',
                    '异常形态提示交叉污染或病变可能'
                ],
                'timestamp': 90
            }
        ],
        'knowledge_framework': '''本视频系统讲解了细胞培养中的"视觉质控"体系:

**基础层 - 形态分类**: 三种基本细胞形态
**标准层 - 健康特征**: 形态规则、立体感强
**诊断层 - 异常识别**: 边界模糊、扁平化''',
        'practical_value': '- **质量控制**: 建立细胞形态档案\n- **问题诊断**: 快速识别异常',
        'learning_suggestions': [
            '**多观察**: 积累大量正常细胞图像的视觉记忆',
            '**勤对比**: 同一细胞系不同状态的对比观察',
            '**善记录**: 拍照记录并建立形态学数据库'
        ]
    }
    
    test_screenshots = {
        90.0: Path('./screenshots/screenshot_90.jpg')
    }
    
    # 生成报告
    output_path = generate_markdown(
        video_info=test_video_info,
        analysis=test_analysis,
        screenshots=test_screenshots,
        srt_content="",
        output_dir=Path('./test_output')
    )
    
    print(f"\n✅ 测试报告已生成: {output_path}")
