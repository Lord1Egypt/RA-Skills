"""
prepare_workspace.py - 阶段 1：验证课程目录、创建工作区并完成统一准备。

对应 video-editing-skills-main/scripts/prepare_workspace.py，但把"视频画幅探测"
重映射为"课程模块分布探测"。

阶段 1 负责：
    1. 检查 / 创建 <SKILL_DIR>/.venv
    2. 按 requirements.txt 安装依赖到统一 .venv
    3. 检查 / 下载 <SKILL_DIR>/bin/ffmpeg.exe 与 ffprobe.exe
    4. 检查 / 下载 <SKILL_DIR>/models/DeepSeek-R1-Distill-Qwen-1.5B-int4-cw-ov
    5. 创建工作区目录，扫描 --course-dir 内教学材料，将 compose_target_module
       写入 runtime_env.json

输入：
    --course-dir    课程材料所在目录（必需）
    --user-request  用户原始请求文本（可选，写入 user_input.txt）

输出：
    成功时最后一行打印工作区绝对路径，退出码 0。
    失败时打印错误信息到 stderr，退出码 1。

用法：
    python scripts/prepare_workspace.py --course-dir "<your_course_dir>" --user-request "高一AI通识第一节"

    # 示例：Windows / Linux / macOS 真实路径
    #   Windows: --course-dir "D:\\courses" 或 "C:\\Users\\you\\courses"
    #   Linux:   --course-dir "/home/you/courses"
    #   macOS:   --course-dir "/Users/you/courses"
"""
from __future__ import annotations


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

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from bootstrap import bootstrap_environment
from skill_runtime import write_runtime_manifest

# 支持的课程材料扩展名（.pdf 读取需运行时尝试导入 pdf 库）
COURSEWARE_EXTENSIONS = {".md", ".txt", ".pdf"}


def find_courseware(course_dir: Path) -> list[Path]:
    """在目录顶层查找课程材料文件（不递归子目录）。"""
    out = []
    for f in sorted(course_dir.iterdir()):
        if f.is_file() and f.suffix.lower() in COURSEWARE_EXTENSIONS:
            out.append(f)
    return out


def infer_compose_target_module(courseware: list[Path]) -> str | None:
    """根据课程材料文件名前缀推断目标教学模块。

    约定文件名前缀：module-a-*.md / module-b-*.md / ... / module-i-*.md
    多数票决定 compose_target_module；无前缀时返回 None。
    """
    counts: dict[str, int] = {}
    for f in courseware:
        name = f.name.lower()
        if name.startswith("module-"):
            parts = name.split("-", 2)
            if len(parts) >= 2:
                tag = f"module-{parts[1]}"
                counts[tag] = counts.get(tag, 0) + 1
    if not counts:
        return None
    return max(counts, key=counts.get)


def main() -> int:
    log = get_logger("prepare")
    parser = argparse.ArgumentParser(description="阶段 1：验证课程目录并创建工作区")
    parser.add_argument("--course-dir", required=True, help="课程材料所在目录")
    parser.add_argument("--user-request", default=None, help="用户原始请求文本")
    parser.add_argument(
        "--skip-model",
        action="store_true",
        help="跳过模型准备（仅调试用）",
    )
    parser.add_argument(
        "--skip-ffmpeg",
        action="store_true",
        help="跳过 ffmpeg 准备（不需要 TTS/字幕合成时）",
    )
    parser.add_argument(
        "--force-requirements",
        action="store_true",
        help="强制重新安装 requirements.txt",
    )
    parser.add_argument(
        "--force-ffmpeg",
        action="store_true",
        help="强制重新下载 ffmpeg / ffprobe",
    )
    parser.add_argument(
        "--force-model",
        action="store_true",
        help="强制重新下载模型",
    )
    args = parser.parse_args()

    course_dir = Path(args.course_dir).resolve()

    # 1. 验证课程目录
    if not course_dir.is_dir():
        log.error(f"错误：课程目录不存在：{course_dir}")
        return 1

    courseware = find_courseware(course_dir)
    if not courseware:
        log.error(f"错误：目录中未找到课程材料：{course_dir}")
        log.error(f"支持的格式：{', '.join(sorted(COURSEWARE_EXTENSIONS))}")
        return 1

    log.info(f"[准备] 找到 {len(courseware)} 个课程材料文件：")
    for f in courseware:
        log.info(f"  {f.name}")

    # 2. 创建工作区
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    workspace = course_dir / f"editing_{timestamp}"
    workspace.mkdir(parents=True, exist_ok=True)
    log.info(f"[准备] 工作区已创建：{workspace}")

    # 3. 保存用户请求
    if args.user_request:
        user_input_file = workspace / "user_input.txt"
        try:
            user_input_file.write_text(args.user_request, encoding="utf-8")
            log.info(f"[准备] 用户请求已保存：{user_input_file}")
        except OSError as e:
            log.error(f"[准备] 警告：无法保存用户请求：{e}")

    # 4. 统一准备运行时
    try:
        log.info("[准备] 开始统一准备 .venv / requirements / ffmpeg / model ...")
        runtime = bootstrap_environment(
            force_requirements=args.force_requirements,
            force_ffmpeg=args.force_ffmpeg,
            force_model=args.force_model,
            skip_ffmpeg=args.skip_ffmpeg,
            skip_model=args.skip_model,
        )
        log.info("[准备] ✓ 运行时准备完成")
        print(json.dumps(runtime, ensure_ascii=False, indent=2))
    except Exception as e:
        log.error(f"[准备] ✗ 运行时准备失败：{e}")
        return 1

    # 5. 探测课程模块分布，供合成阶段读取 runtime_env.json
    target_module = infer_compose_target_module(courseware)
    if target_module:
        log.info(f"[准备] 课程模块分布：compose_target_module={target_module}")
    else:
        log.info("[准备] 未检测到 module-X-* 前缀，compose_target_module 留空（由云端决策指定）")

    # 6. 写入运行时清单
    try:
        manifest_path = write_runtime_manifest(
            workspace,
            merge={
                "compose_target_module": target_module,
                "courseware_count": len(courseware),
                "courseware_files": [str(f) for f in courseware],
            },
        )
        log.info(f"[准备] runtime_env.json 已写入：{manifest_path}")
    except OSError as e:
        log.error(f"[准备] ✗ 无法写入 runtime_env.json：{e}")
        return 1

    # 最后一行输出工作区路径（run.ps1 / 调用方依赖此路径解析）
    print(str(workspace))
    return 0


if __name__ == "__main__":
    sys.exit(main())
