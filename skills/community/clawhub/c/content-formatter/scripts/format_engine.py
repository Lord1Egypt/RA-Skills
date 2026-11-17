#!/usr/bin/env python3
"""统一内容排版引擎 - 支持29平台排版规则

4层排版策略:
  L0: 无需转换(Markdown平台)
  L1: 通用HTML(MD→HTML+默认CSS)
  L2: 平台专属(平台专属CSS模板+结构适配)
  L3: 纯文本(去Markdown标记+字符截断)
"""
import sys
import os
import json
import re
import argparse
from pathlib import Path
from typing import Any

# 添加项目根目录到sys.path
_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPT_DIR.parent.parent.parent
# db_logger位于scripts/目录下,需添加scripts/到sys.path(来源:newprod_publisher.py导入模式)
if str(_PROJECT_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT / "scripts"))
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from mcps.shared.db_logger import get_logger
logger = get_logger("skill", source="content-formatter")
from mcps.shared.atomic_write import atomic_read_json

# 加载平台排版规则
_STYLES_FILE = _SCRIPT_DIR / "platform_styles.json"
PLATFORM_STYLES = {}
if _STYLES_FILE.exists():
    _styles_data = atomic_read_json(str(_STYLES_FILE))
    PLATFORM_STYLES = (_styles_data or {}).get("platforms", {})

# format_converter路径(微信公众号专用排版器)
_FORMAT_CONVERTER = _PROJECT_ROOT / "skills" / "_lazy" / "wechat-formatter" / "scripts" / "format_converter.py"


def format_content(content: str, platform: str, target_format: str = "") -> dict[str, Any]:
    """统一排版入口

    Args:
        content: 原始内容(Markdown格式)
        platform: 目标平台名称
        target_format: 目标格式(html/markdown/text, 空则自动判断)

    Returns:
        {success: bool, data: {html, markdown, text, format_used, layer}, error: str|null}
    """
    try:
        style_config = PLATFORM_STYLES.get(platform, {})
        if not style_config:
            # 未知平台，默认L1通用HTML
            style_config = {"format": "html", "layer": "L1", "style": "simple", "inline_css": True, "features": []}
            logger.info(f"未知平台{platform}, 使用默认L1通用HTML排版")

        layer = style_config.get("layer", "L1")
        fmt = target_format or style_config.get("format", "html")

        result = {"html": "", "markdown": content, "text": "", "format_used": fmt, "layer": layer}

        if layer == "L0":
            # L0: 无需转换,保持Markdown
            result["markdown"] = content
            logger.info(f"平台{platform}使用L0(Markdown原生),无需转换")

        elif layer == "L3":
            # L3: 纯文本,去除Markdown标记 + 平台特性优化
            text = _strip_markdown(content)
            features = style_config.get("features", [])
            # V43修复: 实现platform_styles.json中声明的features
            if "short_paragraph" in features:
                text = _apply_short_paragraph(text)
            if "emoji_friendly" in features:
                text = _apply_emoji_friendly(text)
            if "hashtag_optimize" in features:
                text = _apply_hashtag_optimize(text, platform)
            max_len = style_config.get("max_length", 0)
            if max_len > 0 and len(text) > max_len:
                text = text[:max_len]
            result["text"] = text
            logger.info(f"平台{platform}使用L3(纯文本+特性),长度={len(text)},features={features}")

        elif layer == "L2":
            # L2: 平台专属,调用format_converter
            html = _format_via_converter(content, style_config.get("style", "simple"))
            if html:
                result["html"] = html
                logger.info(f"平台{platform}使用L2(平台专属),style={style_config.get('style')}")
            else:
                # 降级到L1
                html = _basic_md_to_html(content, style_config.get("inline_css", True))
                result["html"] = html
                result["layer"] = "L1(fallback)"
                logger.warning(f"平台{platform}L2排版失败,降级到L1")

        elif layer == "L1":
            # L1: 通用HTML
            html = _basic_md_to_html(content, style_config.get("inline_css", True))
            result["html"] = html
            logger.info(f"平台{platform}使用L1(通用HTML)")

        return {"success": True, "data": result, "error": None}

    except Exception as e:
        logger.error(f"排版失败 platform={platform}: {e}")
        return {"success": False, "data": {}, "error": str(e)}


def _strip_markdown(content: str) -> str:
    """去除Markdown标记,转为纯文本"""
    text = content
    text = re.sub(r'```[\s\S]*?```', '', text)  # 代码块
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)  # 图片
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)  # 链接保留文本
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)  # 标题
    text = re.sub(r'[*`>~_-]', '', text)  # Markdown符号
    text = re.sub(r'\n{3,}', '\n\n', text)  # 多余空行
    return text.strip()


def _apply_short_paragraph(content: str, max_chars_per_para: int = 120) -> str:
    """短段落优化: 将长段落拆分为短段落(每段不超过max_chars_per_para字符)

    用于小红书等平台,提升阅读体验
    """
    if not content:
        return content
    paragraphs = content.split('\n\n')
    result = []
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        # 按句子分割长段落
        if len(para) > max_chars_per_para:
            sentences = re.split(r'([。！？.!?])', para)
            current = ""
            for i in range(0, len(sentences) - 1, 2):
                sentence = sentences[i] + (sentences[i + 1] if i + 1 < len(sentences) else "")
                if len(current) + len(sentence) > max_chars_per_para and current:
                    result.append(current.strip())
                    current = sentence
                else:
                    current += sentence
            if current:
                result.append(current.strip())
        else:
            result.append(para)
    return '\n\n'.join(result)


def _apply_emoji_friendly(content: str) -> str:
    """Emoji优化: 根据内容关键词在段落后添加相关emoji

    用于小红书/抖音/快手等平台,提升内容亲和力
    """
    if not content:
        return content
    # 关键词→emoji映射
    EMOJI_MAP = [
        (["科技", "AI", "技术", "智能", "数字", "数据", "互联网", "芯片", "算法"], "💡"),
        (["优惠", "促销", "折扣", "特价", "秒杀", "福利", "降价", "红包"], "🎉"),
        (["生活", "日常", "家居", "美食", "旅行", "健身", "穿搭"], "✨"),
        (["赚钱", "投资", "理财", "创业", "商业", "副业", "收入"], "💰"),
        (["推荐", "好物", "种草", "测评", "对比", "排行榜"], "👍"),
        (["教程", "攻略", "指南", "方法", "技巧", "步骤"], "📝"),
        (["新品", "发布", "上线", "首发", "亮相"], "🚀"),
        (["警告", "注意", "避坑", "风险", "误区", "陷阱"], "⚠️"),
    ]
    paragraphs = content.split('\n\n')
    result = []
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        # 检测是否已有emoji
        has_emoji = any(ord(c) > 0x1F000 for c in para)
        if has_emoji:
            result.append(para)
            continue
        # 匹配关键词添加emoji
        emoji_added = False
        for keywords, emoji in EMOJI_MAP:
            if any(kw in para for kw in keywords):
                # 在段落末尾(最后一个标点后)添加emoji
                if para[-1] in '。！？.!?…':
                    result.append(para + emoji)
                else:
                    result.append(para + ' ' + emoji)
                emoji_added = True
                break
        if not emoji_added:
            result.append(para)
    return '\n\n'.join(result)


def _apply_hashtag_optimize(content: str, platform: str) -> str:
    """标签优化: 在内容末尾添加平台相关热门标签

    用于抖音/快手/小红书/B站/视频号等平台
    """
    if not content:
        return content
    # 检测是否已有标签
    existing_tags = re.findall(r'#(\S+)', content)
    if len(existing_tags) >= 5:
        return content  # 已有5个以上标签,不再添加

    # 平台→默认标签映射
    PLATFORM_TAGS = {
        "douyin": ["#抖音", "#短视频", "#热门", "#知识分享"],
        "kuaishou": ["#快手", "#短视频", "#热门", "#生活"],
        "xiaohongshu": ["#小红书", "#种草", "#好物推荐", "#生活日常"],
        "bilibili": ["#哔哩哔哩", "#干货分享", "#知识区"],
        "shipinhao": ["#视频号", "#微信", "#热门"],
    }
    default_tags = PLATFORM_TAGS.get(platform, [])
    if not default_tags:
        return content

    # 过滤已存在的标签
    new_tags = [tag for tag in default_tags if tag.lstrip('#') not in existing_tags]
    if not new_tags:
        return content

    # 限制总标签数不超过5个
    slots = 5 - len(existing_tags)
    new_tags = new_tags[:slots]

    # 在内容末尾添加标签
    tag_line = ' '.join(new_tags)
    if content.endswith('\n'):
        return content + tag_line + '\n'
    else:
        return content + '\n\n' + tag_line


def _format_via_converter(content: str, style: str) -> str:
    """调用format_converter进行富文本转换"""
    try:
        import subprocess, tempfile
        if not _FORMAT_CONVERTER.exists():
            return ""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write(content)
            tmp_md = f.name

        try:
            result = subprocess.run(
                [sys.executable, str(_FORMAT_CONVERTER), "--input", tmp_md, "--style", style],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                try:
                    data = json.loads(result.stdout)
                    return data.get("data", {}).get("html", "")
                except json.JSONDecodeError as e:
                    # P1-15修复: JSON解析失败需记录(原except:pass)
                    logger.error(f"format_converter输出JSON解析失败: {e}")
        finally:
            os.unlink(tmp_md)
    except Exception as e:
        logger.error(f"format_converter调用失败: {e}")
    return ""


def _basic_md_to_html(content: str, inline_css: bool = True) -> str:
    """基础Markdown→HTML转换"""
    try:
        import markdown as md_lib
        html = md_lib.markdown(content, extensions=['extra', 'codehilite', 'toc'])
        if inline_css:
            # 添加基础内联CSS样式
            html = html.replace('<h1>', '<h1 style="font-size:1.5em;font-weight:bold;margin:1em 0;">')
            html = html.replace('<h2>', '<h2 style="font-size:1.3em;font-weight:bold;margin:1em 0;">')
            html = html.replace('<h3>', '<h3 style="font-size:1.1em;font-weight:bold;margin:1em 0;">')
            html = html.replace('<p>', '<p style="line-height:1.8;margin:0.5em 0;">')
            html = html.replace('<blockquote>', '<blockquote style="border-left:3px solid #ccc;padding-left:1em;color:#666;">')
            html = html.replace('<code>', '<code style="background:#f5f5f5;padding:2px 4px;border-radius:3px;">')
        return html
    except ImportError:
        # 无markdown库,简单替换
        html = content.replace('\n', '<br>\n')
        html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        return html


def main():
    """统一排版入口 - 支持三种调用模式

    模式1(orchestrator): --action format --params '{"content":"...","platform":"..."}' + stdin JSON
    模式2(直接CLI): --content "..." --platform "..." --format html
    模式3(stdin JSON): {"action":"format","content":"...","platform":"..."}
    """
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    try:
        parser = argparse.ArgumentParser(description="统一内容排版引擎")
        parser.add_argument("--content", default=None, help="原始内容(Markdown)")
        parser.add_argument("--platform", default=None, help="目标平台")
        parser.add_argument("--format", default="", help="目标格式(html/markdown/text)")
        parser.add_argument("--content-file", default="", help="内容文件路径(替代--content)")
        parser.add_argument("--action", default=None, help="操作类型(orchestrator传入)")
        parser.add_argument("--params", default=None, help="JSON参数(orchestrator传入)")
        args, _unknown = parser.parse_known_args()

        content = args.content
        platform = args.platform
        fmt = args.format

        # 模式1: orchestrator通过--params传入
        if args.params:
            try:
                params = json.loads(args.params)
                content = content or params.get("content", "")
                platform = platform or params.get("platform", "")
                fmt = fmt or params.get("format", "")
            except json.JSONDecodeError as e:
                logger.debug(f"--params JSON解析失败: {e}")

        # 模式3: stdin JSON(orchestrator同时发送stdin)
        if not content and not sys.stdin.isatty():
            try:
                input_data = json.loads(sys.stdin.read())
                content = input_data.get("content", "")
                platform = platform or input_data.get("platform", "")
                fmt = fmt or input_data.get("format", "")
            except (json.JSONDecodeError, ValueError) as e:
                logger.debug(f"stdin JSON解析失败: {e}")

        # 模式2: content-file fallback
        if args.content_file and os.path.exists(args.content_file):
            with open(args.content_file, "r", encoding="utf-8") as f:
                content = f.read()

        if not content:
            print(json.dumps({"success": False, "data": {}, "error": "content不能为空", "code": "FORMAT_VAL_ERR"}, ensure_ascii=False))
            sys.exit(1)
        if not platform:
            print(json.dumps({"success": False, "data": {}, "error": "platform不能为空", "code": "FORMAT_VAL_ERR"}, ensure_ascii=False))
            sys.exit(1)

        result = format_content(content, platform, fmt)
        print(json.dumps(result, ensure_ascii=False))
    except ValueError as e:
        logger.error(f"content-formatter异常: {e}", exc_info=True)
        print(json.dumps({"success": False, "data": {}, "error": str(e), "code": "FORMAT_VAL_ERR"}, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        logger.error(f"content-formatter异常: {e}", exc_info=True)
        print(json.dumps({"success": False, "data": {}, "error": str(e), "code": "FORMAT_ERR"}, ensure_ascii=False))
        sys.exit(2)


if __name__ == "__main__":
    main()
