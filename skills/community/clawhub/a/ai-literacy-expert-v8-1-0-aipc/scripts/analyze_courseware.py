"""
analyze_courseware.py - 阶段 2: 本地文本推理分析课程材料.

对应 video-editing-skills-main/scripts/analyze_video.py, 但把 VLM 视频抽帧理解
重映射为 "DeepSeek-R1-1.5B 文本切片推理".

关键差异(vs video-editing):
  - 使用 openvino_genai.LLMPipeline(非 VLMPipeline)
  - 输入是文本切片(非视频帧)
  - 两阶段提示词: 阶段 1 知识点判定(32 token) → 阶段 2 详细教学建议(约 200 token)
  - 输出 output_reasoning.json(V7 abstract_data 格式, < 10KB)

设备降级(V7 npu-scheduling-guide §2.2):
  NPU → GPU → CPU(requested_device 不可用时自动降级)

mock 模式(--mock-mode):
  不加载真实模型, 使用基于规则的模拟推理, 便于无模型环境测试全链路.

用法:
    python scripts/analyze_courseware.py \\
        --course-dir "<your_course_dir>" \\
        --output "<workspace>/output_reasoning.json" \\
        --theme "机器学习入门" \\
        --device GPU

    # mock 模式(无需模型, 测试用)
    python scripts/analyze_courseware.py --course-dir "<your_course_dir>" --output "<workspace>/output_reasoning.json" --mock-mode

    # 示例: Windows 下 D:\\courses 目录
    #   python scripts/analyze_courseware.py --course-dir "D:\\\\courses" --output "...\\\\output_reasoning.json" --theme "机器学习"
"""
from __future__ import annotations
__version__ = "8.1.0-aipc"  # V8.1-AIPC: 每次工作自动输出本地/云端对比 + 全互动控件完整性门控


# --- UTF-8 stdout/stderr (Windows 中文输出防乱码) -----------------------------
def _configure_stream_encoding(stream):
    reconfigure = getattr(stream, "reconfigure", None)
    if callable(reconfigure):
        reconfigure(encoding="utf-8")

import sys as _sys
_configure_stream_encoding(_sys.stdout)
_configure_stream_encoding(_sys.stderr)
del _sys
# ----------------------------------------------------------------------------

from log_util import get_logger

log = get_logger("analyze")

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Optional

from skill_runtime import DEFAULT_MODEL_DIR

# 鏂囨湰鍒囩墖鍙傛暟
SEGMENT_MAX_CHARS = 800      # 姣忔鏈澶瓧绗暟
SEGMENT_OVERLAP_CHARS = 100  # 娈甸棿閲嶅彔锛堜繚鎸佷笂涓嬫枃杩炶疮锛?

# 涓樁娈垫彁绀鸿瘝 token 棰勭畻
STAGE1_MAX_TOKENS = 32   # 鐭瘑鐐瑰垽瀹?
STAGE2_MAX_TOKENS = 256  # 璇粏鏁欏寤鸿锛堚墺200锛?


# ---------------------------------------------------------------------------
# 鏂囨湰鍒囩墖
# ---------------------------------------------------------------------------

def split_text(text: str, max_chars: int = SEGMENT_MAX_CHARS,
               overlap: int = SEGMENT_OVERLAP_CHARS) -> list[str]:
    """把长文本切成 ~max_chars 字符的段, 段间重叠 overlap 字符.

    优先按双换行(段落)切, 段落过长时按句号切, 再过长按 max_chars 硬切.
    """
    if not text or not text.strip():
        return []
    text = text.strip()

    # 鍏堟寜娈佃惤鍒?
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    segments: list[str] = []
    buf = ""

    def _flush() -> None:
        nonlocal buf
        if buf.strip():
            segments.append(buf.strip())
        buf = ""

    for para in paragraphs:
        if len(para) > max_chars:
            # 娈佃惤杩囬暱锛氬厛 flush锛屽啀鎸夊彞鍙峰垏
            _flush()
            sentences = re.split(r"(?<=[銆傦紒锛?!?\n])", para)
            for sent in sentences:
                if not sent.strip():
                    continue
                if len(buf) + len(sent) > max_chars and buf:
                    segments.append(buf.strip())
                    buf = sent if len(sent) <= max_chars else sent[:max_chars]
                else:
                    buf += sent
                while len(buf) > max_chars:
                    segments.append(buf[:max_chars])
                    buf = buf[max_chars - overlap:]
            _flush()
        elif len(buf) + len(para) + 2 > max_chars:
            _flush()
            buf = para
        else:
            buf = (buf + "\n\n" + para) if buf else para
    _flush()
    return segments


def read_courseware(path: Path) -> str:
    """读取课件材料文件内容 (md/.txt 直接读, pdf 尝试导入库)."""
    suffix = path.suffix.lower()
    if suffix in (".md", ".txt"):
        return path.read_text(encoding="utf-8", errors="replace")
    if suffix == ".pdf":
        try:
            import PyPDF2  # type: ignore
        except ImportError:
            try:
                import pdfplumber  # type: ignore
                with pdfplumber.open(path) as pdf:
                    return "\n\n".join((p.extract_text() or "") for p in pdf.pages)
            except ImportError:
                log.warn(f"[analyze] 鈿?璺宠繃 PDF锛堟湭瑁?PyPDF2/pdfplumber锛夛細{path.name}")
                return ""
        text_parts: list[str] = []
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text_parts.append(page.extract_text() or "")
        return "\n\n".join(text_parts)
    return ""


# ---------------------------------------------------------------------------
# 涓樁娈垫彁绀鸿瘝
# ---------------------------------------------------------------------------

def build_topic_judgement_prompt(text: str, theme: str) -> str:
    """阶段 1: 知识点判定 (32 token).

    让模型判断该段文本是否与主题相关, 返回 符合/部分符合/不符合.
    """
    snippet = text[:300] if len(text) > 300 else text
    return (
        f"判断以下教学内容是否与主题 [{theme}] 相关.\n"
        f"只回答: 符合 / 部分符合 / 不符合\n\n"
        f"教学内容: {snippet}\n\n"
        f"回答: "
    )


def build_detail_prompt(text: str, theme: str) -> str:
    """阶段 2: 详细教学建议 (约 200 token).

    让模型输出知识点标签 + 难度等级 + 教学建议.
    """
    return (
        f"你是AI通识课教学专家. 请分析以下教学内容, 输出:\n"
        f"1. 知识点标签 (3~5个, 逗号分隔)\n"
        f"2. 难度等级 (1~5, 1最简单)\n"
        f"3. 教学建议 (适合的教学法、互动方式、注意事项)\n\n"
        f"主题: {theme}\n"
        f"教学内容: {text}\n\n"
        f"请按以下格式输出:\n"
        f"知识点: xxx,xxx,xxx\n"
        f"难度: N\n"
        f"建议: xxx"
    )


# ---------------------------------------------------------------------------
# 鎺悊缁撴灉瑙e瀽
# ---------------------------------------------------------------------------

def parse_detail_response(text: str) -> dict:
    """解析阶段 2 的模型输出, 提取 knowledge_tags / difficulty / pedagogy_suggestion."""
    result: dict[str, Any] = {
        "knowledge_tags": [],
        "difficulty": 2,
        "pedagogy_suggestion": "",
    }
    if not text:
        return result

    # 提取知识点
    m = re.search(r"知识点[：:]\s*(.+)", text)
    if m:
        tags = [t.strip() for t in re.split(r"[,，;；、]", m.group(1)) if t.strip()]
        result["knowledge_tags"] = tags[:5]

    # 提取难度
    m = re.search(r"难度[：:]\s*(\d)", text)
    if m:
        try:
            d = int(m.group(1))
            result["difficulty"] = max(1, min(5, d))
        except ValueError:
            pass

    # 提取建议
    m = re.search(r"建议[：:]\s*(.+)", text, re.DOTALL)
    if m:
        result["pedagogy_suggestion"] = m.group(1).strip()[:500]

    # 如果没提取到建议, 用全文兜底
    if not result["pedagogy_suggestion"]:
        result["pedagogy_suggestion"] = text.strip()[:500]

    return result


def is_topic_relevant(judgement: str) -> bool:
    """判断阶段 1 输出是否表示相关."""
    if not judgement:
        return True  # 无法判断时默认相关（避免漏判）
    j = judgement.strip()
    return "符合" in j and "不符合" not in j


# ---------------------------------------------------------------------------
# Pipeline 初始化（真实模式）
# ---------------------------------------------------------------------------

def init_text_pipeline(model_dir: Path, device: str) -> tuple[Any, str]:
    """加载 OpenVINO LLMPipeline, 设备不可用时自动降级.

    降级链: NPU -> GPU -> CPU (V7 npu-scheduling-guide 2.2).

    V7-AIPC: device="AUTO" 自动调度 NPU/iGPU/CPU (V7.3.2 改进3 升级版).

    Returns:
        (pipeline, actual_device)
    """
    try:
        import openvino_genai  # type: ignore
    except ImportError as e:
        raise RuntimeError(
            f"未安装 openvino-genai, 无法加载模型: {e}\n"
            "请运行 bootstrap.py 安装依赖, 或使用 --mock-mode 测试."
        ) from e

    # V7.3.2 改进3: 自动硬件调度
    if device.upper() == "AUTO":
        try:
            from hardware_probe import auto_select_device
            device = auto_select_device(prefer="GPU")
            log.info(f"[analyze] 自动硬件调度: 选择 {device}")
        except ImportError:
            log.warn("[analyze] hardware_probe 不可用, fallback 到 GPU")
            device = "GPU"

    # 降级链
    devices_to_try = [device]
    for fallback in ("NPU", "GPU", "CPU"):
        if fallback not in devices_to_try:
            devices_to_try.append(fallback)

    last_error: Optional[Exception] = None
    for dev in devices_to_try:
        try:
            pipeline = openvino_genai.LLMPipeline(str(model_dir), dev)
            if dev != device:
                log.error(f"[analyze]  请求设备 {device} 不可用, 降级到 {dev}")
            return pipeline, dev
        except Exception as e:
            last_error = e
            log.error(f"[analyze] 设备 {dev} 不可用: {e}")
            continue

    raise RuntimeError(f"所有设备均不可用: {last_error}")


def generate(pipeline: Any, prompt: str, max_new_tokens: int) -> str:
    """调用 LLMPipeline.generate (兼容不同 openvino_genai 版本)."""
    try:
        import openvino_genai  # type: ignore
        config = openvino_genai.GenerationConfig()
        config.max_new_tokens = max_new_tokens
        result = pipeline.generate(prompt, config)
        return getattr(result, "text", str(result))
    except ImportError:
        pass
    # 兜底: 直接调 generate
    if hasattr(pipeline, "generate"):
        result = pipeline.generate(prompt)
        return getattr(result, "text", str(result))
    return ""


# ---------------------------------------------------------------------------
# Mock 推理（无模型时测试用）
# ---------------------------------------------------------------------------

_MOCK_KEYWORD_MAP = {
    "机器学习": ["机器学习", "监督学习", "无监督学习", "深度学习", "神经网络"],
    "人工智能": ["人工智能", "AI", "智能", "机器智能"],
    "数据": ["数据", "数据库", "数据分析", "数据挖掘"],
    "算法": ["算法", "排序", "搜索", "递归"],
    "Python": ["Python", "编程", "代码", "函数"],
    "伦理": ["伦理", "隐私", "安全", "偏见", "公平"],
}

_MOCK_PEDAGOGY = {
    1: "建议采用讲授法+实例演示,降低认知门槛",
    2: "建议采用探究式教学,引导学生主动思考",
    3: "建议采用 PBL 项目式学习,结合实际案例",
    4: "建议采用翻转课堂,课前预习+课中深度讨论",
    5: "建议采用 5E 模型,强调创造与评价",
}


def mock_analyze_segment(text: str, theme: str) -> dict:
    """基于规则的模拟推理 (mock 模式)."""
    tags: list[str] = []
    text_lower = text.lower()
    for keyword, related in _MOCK_KEYWORD_MAP.items():
        for r in related:
            if r.lower() in text_lower:
                if keyword not in tags:
                    tags.append(keyword)
                break

    if not tags:
        # 无命中时, 取前几个名词作兜底
        words = re.findall(r"[\u4e00-\u9fa5]{2,4}", text)
        tags = list(dict.fromkeys(words))[:3] or ["通识概念"]

    # 难度: 根据文本长度和关键词数量粗估
    difficulty = min(5, max(1, 2 + len(text) // 1000 - len(tags) // 2))
    difficulty = max(1, min(5, difficulty))

    return {
        "knowledge_tags": tags[:5],
        "difficulty": difficulty,
        "pedagogy_suggestion": _MOCK_PEDAGOGY.get(difficulty, _MOCK_PEDAGOGY[2]),
    }


# ---------------------------------------------------------------------------
# 主分析流程
# ---------------------------------------------------------------------------

def analyze_segment(
    pipeline: Any,
    text: str,
    theme: str,
    *,
    mock_mode: bool = False,
) -> dict:
    """分析单段文本, 返回 {knowledge_tags, difficulty, pedagogy_suggestion}.

    两阶段推理(真实模式):
      Stage 1: 主题判定(32 token),若不相关则跳过详细推理
      Stage 2: 详细教学建议(约 200 token)
    """
    if mock_mode:
        return mock_analyze_segment(text, theme)

    # 阶段 1: 主题判定
    if theme:
        j_prompt = build_topic_judgement_prompt(text, theme)
        j_result = generate(pipeline, j_prompt, STAGE1_MAX_TOKENS)
        if not is_topic_relevant(j_result):
            return {
                "knowledge_tags": [],
                "difficulty": 0,
                "pedagogy_suggestion": f"[主题不相关] 模型判定与 [{theme}] 不符合",
            }

    # 阶段 2: 详细教学建议
    d_prompt = build_detail_prompt(text, theme)
    d_result = generate(pipeline, d_prompt, STAGE2_MAX_TOKENS)
    return parse_detail_response(d_result)


def process_courseware(
    courseware_path: Path,
    pipeline: Any,
    theme: str,
    *,
    mock_mode: bool = False,
    seg_id_start: int = 0,
) -> tuple[list[dict], int]:
    """处理单个课程材料文件, 返回 (segments, next_seg_id)."""
    content = read_courseware(courseware_path)
    if not content.strip():
        return [], seg_id_start

    chunks = split_text(content)
    segments: list[dict] = []
    seg_id = seg_id_start

    for chunk in chunks:
        analysis = analyze_segment(pipeline, chunk, theme, mock_mode=mock_mode)
        segments.append({
            "seg_id": seg_id,
            "source_file": str(courseware_path),
            "source_filename": courseware_path.name,
            "seg_text": chunk[:200] + ("..." if len(chunk) > 200 else ""),
            "seg_text_full_length": len(chunk),
            "knowledge_tags": analysis["knowledge_tags"],
            "difficulty": analysis["difficulty"],
            "pedagogy_suggestion": analysis["pedagogy_suggestion"],
        })
        seg_id += 1

    return segments, seg_id


# ---------------------------------------------------------------------------
# CLI 涓诲叆鍙?
# ---------------------------------------------------------------------------

def main() -> int:
    log = get_logger("analyze")
    parser = argparse.ArgumentParser(description="阶段 2: 本地文本推理分析课程材料")
    parser.add_argument("--course-dir", required=True, help="course directory")
    parser.add_argument("--output", required=True, help="output_reasoning.json path")
    parser.add_argument("--theme", default=None, help="teaching theme")
    parser.add_argument("--device", default="GPU", help="device (NPU/GPU/CPU/AUTO)")
    parser.add_argument("--model-dir", default=None, help="model directory")
    parser.add_argument(
        "--mock-mode",
        action="store_true",
        help="use mock mode (no real model)",
    )
    args = parser.parse_args()

    course_dir = Path(args.course_dir).resolve()
    if not course_dir.is_dir():
        log.error(f"错误: 课程目录不存在: {course_dir}")
        return 1

    # 鏀堕泦璇剧鏉愭枡
    exts = {".md", ".txt", ".pdf"}
    courseware = sorted(
        f for f in course_dir.iterdir()
        if f.is_file() and f.suffix.lower() in exts
    )
    if not courseware:
        log.error(f"閿欒锛氱洰褰曚腑鏈壘鍒拌绋嬫潗鏂欙細{course_dir}")
        return 1

    log.info(f"[analyze] 找到 {len(courseware)} 个课件材料")
    if args.theme:
        log.info(f"[analyze] 主题模式: {args.theme}")

    # 初始化 pipeline
    if args.mock_mode:
        log.info("[analyze] mock 模式: 使用基于规则的模拟推理")
        pipeline = None
    else:
        model_dir = Path(args.model_dir) if args.model_dir else DEFAULT_MODEL_DIR
        if not model_dir.exists():
            log.error(f"错误: 模型目录不存在: {model_dir}")
            log.error("请先运行 bootstrap.py, 或使用 --mock-mode 测试.")
            return 1
        log.info(f"[analyze] 加载模型: {model_dir} (设备: {args.device})")
        pipeline, actual_device = init_text_pipeline(model_dir, args.device)
        log.info(f"[analyze] ✓ 模型已加载 (实际设备: {actual_device})")

    # 逐文件处理
    all_segments: list[dict] = []
    processed_docs: list[dict] = []
    seg_id = 0

    for cw in courseware:
        log.info(f"[analyze] 处理: {cw.name}")
        segs, seg_id = process_courseware(
            cw, pipeline, args.theme or "",
            mock_mode=args.mock_mode,
            seg_id_start=seg_id,
        )
        all_segments.extend(segs)
        processed_docs.append({
            "file": str(cw),
            "filename": cw.name,
            "segment_count": len(segs),
            "segment_ids": [s["seg_id"] for s in segs],
        })
        log.info(f"  → {len(segs)} 段)")

    # 构建输出 (保持与 video-editing 字段名兼容: vlm_prompt / processed_documents / segments)
    vlm_prompt = (
        build_detail_prompt(f"主题: {args.theme}", args.theme)
        if args.theme else "无主题 (全量分析模式)"
    )

    output = {
        "vlm_prompt": vlm_prompt[:500],
        "theme": args.theme,
        "device": args.device if not args.mock_mode else "mock",
        "processed_documents": processed_docs,
        "segments": all_segments,
        "total_segments": len(all_segments),
    }

    # 鍐欏嚭
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # V7 4.1 约束: abstract_data < 10KB (如超了给警告)
    size = output_path.stat().st_size
    if size >= 10240:
        log.warn(
            f"[analyze]  output_reasoning.json 大小 {size}B >= 10KB, 端云交换时将被 edge_cloud_dispatch 截断"
        )

    log.info(f"[analyze]  输出: {output_path} (共 {len(all_segments)} 段, {size}B)")
    print(str(output_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())

