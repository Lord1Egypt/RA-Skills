"""
setup_text_model.py - 从 ModelScope 下载 OpenVINO/DeepSeek-R1-Distill-Qwen-1.5B-int4-cw-ov，
                      并部署到 <SKILL_DIR>/models/ 目录下。

输出路径：<SKILL_DIR>/models/<DEFAULT_MODEL_NAME>/
  - 默认输出子目录名 = DeepSeek-R1-Distill-Qwen-1.5B-int4-cw-ov
  - ModelScope 官方组织 @OpenVINO 已托管该模型（仓库名与 HuggingFace 相同）

用法：
    # 基础（默认从 ModelScope 下载，国内直连快，无需科学上网）
    python setup_text_model.py

    # 指定其他 ModelScope 模型 ID（例如切回 OpenVINO/qwen2.5-1.5b-instruct-int4-ov）
    python setup_text_model.py --model-id OpenVINO/qwen2.5-1.5b-instruct-int4-ov

    # 指定模型目录（替换为你的实际路径）
    python setup_text_model.py --model-dir <your_model_dir>

    # 示例（Windows / Linux / macOS 三种风格）
    #   Windows: --model-dir "D:\\path\\to\\models\\DeepSeek-R1-Distill-Qwen-1.5B-int4-cw-ov"
    #   Linux:   --model-dir "/home/you/models/DeepSeek-R1-Distill-Qwen-1.5B-int4-cw-ov"
    #   macOS:   --model-dir "/Users/you/models/DeepSeek-R1-Distill-Qwen-1.5B-int4-cw-ov"

    # 强制重新下载（即使目录已存在）
    python setup_text_model.py --force

    # 只校验已有模型是否存在，不执行下载
    python setup_text_model.py --check-only

    # 断点续传（已下载文件保留在 <model_dir>.partial/，重新运行会继续下载未完成文件并最终原子重命名）
    python setup_text_model.py --continue

说明：
    脚本会优先确保并复用 <SKILL_DIR>/.venv，
    依赖安装以 requirements.txt 为准（已改用 modelscope 取代 huggingface_hub）。
    本脚本对应 video-editing-skills-main/scripts/setup_ov_model.py，
    模型从 VLM(Qwen2.5-VL-7B) 换成纯文本推理模型(DeepSeek-R1-1.5B)，下载源改为 ModelScope。
"""


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
import os
import shutil
import sys
from pathlib import Path

from skill_runtime import (
    DEFAULT_MODEL_DIR,
    DEFAULT_MODEL_NAME,
    ensure_skill_requirements,
    maybe_reexec_in_skill_venv,
)

log = get_logger("setup_model")

# ModelScope 模型 ID（已转换好的 OpenVINO INT4 文本推理模型）
# 说明：ModelScope 官方组织 @OpenVINO 已同步托管该模型（仓库名与 HuggingFace 相同），
#       DeepSeek-R1 蒸馏模型自带思维链，且 int4-cw 权重针对 Intel 酷睿 Ultra NPU 优化，
#       符合本技能「NPU 优先调度 + 端侧重计算」架构。
MODEL_SCOPE_ID = "OpenVINO/DeepSeek-R1-Distill-Qwen-1.5B-int4-cw-ov"


# ---------------------------------------------------------------------------
# 模型目录检查
# ---------------------------------------------------------------------------

# OpenVINO 模型目录完整性阈值（与 video-editing setup_ov_model.py 保持一致）
MODEL_MIN_XML_FILES    = 1
MODEL_MIN_BIN_FILES    = 1
MODEL_MIN_TOTAL_ENTRIES = 27


def _inspect_model_dir(model_dir: Path) -> dict:
    """
    检查 OpenVINO 模型目录的完整性，返回详细报告。

    校验三项硬指标：
      - .xml 文件数 >= 1（OpenVINO 拓扑结构）
      - .bin 文件数 >= 1（OpenVINO 权重）
      - 总条目数 >= 27（含 tokenizer / 分词器 / 分片权重等，确保下载完整）
    """
    if not model_dir.is_dir():
        return {
            "exists": False, "xml_count": 0, "bin_count": 0,
            "total_entries": 0, "valid": False,
            "reason": f"目录不存在：{model_dir}",
        }

    all_entries  = list(model_dir.rglob("*"))
    all_files    = [e for e in all_entries if e.is_file()]
    xml_files    = [f for f in all_files if f.suffix.lower() == ".xml"]
    bin_files    = [f for f in all_files if f.suffix.lower() == ".bin"]
    total_entries = len(all_entries)
    xml_count    = len(xml_files)
    bin_count    = len(bin_files)

    reasons = []
    if xml_count < MODEL_MIN_XML_FILES:
        reasons.append(f".xml 文件数 {xml_count} < 最低要求 {MODEL_MIN_XML_FILES}")
    if bin_count < MODEL_MIN_BIN_FILES:
        reasons.append(f".bin 文件数 {bin_count} < 最低要求 {MODEL_MIN_BIN_FILES}")
    if total_entries < MODEL_MIN_TOTAL_ENTRIES:
        reasons.append(f"总条目数 {total_entries} < 最低要求 {MODEL_MIN_TOTAL_ENTRIES}（下载不完整）")

    valid = len(reasons) == 0
    return {
        "exists": True,
        "xml_count": xml_count,
        "bin_count": bin_count,
        "total_entries": total_entries,
        "valid": valid,
        "reason": "；".join(reasons) if reasons else "",
    }


def _verify_model_dir(model_dir: Path) -> bool:
    """验证 OpenVINO 模型目录是否完整有效。"""
    return _inspect_model_dir(model_dir)["valid"]


def _flatten_nested_model_dir(partial_dir: Path) -> None:
    """规整 ModelScope 下载目录。

    ModelScope 的 ``snapshot_download(model_id, local_dir=...)`` 在不同版本下
    可能将文件直接落在 ``local_dir/`` 顶层，也可能套一层 ``local_dir/<model_name>/``。
    为保证下游 ``LLMPipeline(model_dir)`` 能直接读取 ``openvino_model.xml``，
    这里把「顶层无 .xml 且恰有唯一子目录」的情况做上移压平处理。
    """
    if list(partial_dir.glob("*.xml")):
        return  # 顶层已有 OpenVINO 文件，无需压平

    sub_dirs = [d for d in partial_dir.iterdir() if d.is_dir()]
    files    = [f for f in partial_dir.iterdir() if f.is_file()]
    if files or len(sub_dirs) != 1:
        return  # 结构不可预测，保留原样（校验阶段会给出明确错误）

    inner = sub_dirs[0]
    log.info(f"[model] 检测到 ModelScope 嵌套目录，压平：{inner.name}/ → {partial_dir}/")
    tmp = partial_dir.with_name(partial_dir.name + ".flatten")
    if tmp.exists():
        shutil.rmtree(tmp, ignore_errors=True)
    inner.rename(tmp)
    for child in tmp.iterdir():
        shutil.move(str(child), str(partial_dir / child.name))
    shutil.rmtree(tmp, ignore_errors=True)


# ---------------------------------------------------------------------------
# 模型下载
# ---------------------------------------------------------------------------

def _download_model(
    model_id: str,
    output_dir: Path,
    partial_dir: Path | None = None,
) -> bool | str:
    """使用 modelscope.snapshot_download 将整个模型仓库快照下载到 partial_dir（安全下载模式）。

    下载流程（遵循 local-ai-skill-authoring-main 规范）：
      1. 下载到 partial_dir（<model_dir>.partial/）
      2. 验证 required_files 完整性
      3. 原子重命名 partial_dir → output_dir

    若 partial_dir 为 None，则直接下载到 output_dir（向后兼容）。
    """
    try:
        from modelscope import snapshot_download
    except ImportError:
        log.error(
            "[model] 未找到 modelscope，请先安装：\n"
            "  pip install modelscope"
        )
        return False

    # 安全下载模式：下载到 .partial 目录
    download_dir = partial_dir if partial_dir is not None else output_dir

    try:
        log.info(f"[model] 正在从 ModelScope 下载 {model_id} ...")
        log.info(f"[model] 下载目录：{download_dir}")
        if partial_dir is not None:
            log.info(f"[model] 最终目录：{output_dir}（下载完成后原子重命名）")
        log.info("[model] 下载文件较大（约 1~2 GB，1.5B 蒸馏模型），请耐心等待。")
        print()

        download_dir.mkdir(parents=True, exist_ok=True)

        # local_dir 指定后，文件直接保存到该目录。
        snapshot_download(
            model_id=model_id,
            local_dir=str(download_dir),
        )

        # 规整 ModelScope 可能的嵌套目录
        _flatten_nested_model_dir(download_dir)
        return True
    except (TimeoutError, ConnectionError) as e:
        log.error(f"[model] 下载中断（网络）：{e}")
        log.error(f"[model]   可使用 --continue 续传：python setup_text_model.py --continue")
        return "continue"
    except Exception as e:
        msg = str(e).lower()
        if "timeout" in msg or "connection" in msg or "reset" in msg or "interrupted" in msg:
            log.error(f"[model] 下载中断（网络）：{e}")
            log.error(f"[model]   可使用 --continue 续传：python setup_text_model.py --continue")
            return "continue"
        log.error(f"[model] 下载失败：{e}")
        return False


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def setup_text_model(
    model_dir: Path,
    model_id: str,
    force: bool,
    check_only: bool,
    continue_download: bool = False,
) -> bool | str:
    """从 ModelScope 下载 OpenVINO 文本推理模型并部署到指定目录。

    返回值：
      True  — 成功（含「已存在跳过」）
      False — 硬失败（参数错误/权限不足/仓库不存在）
      "continue" — 下载中断，需用 --continue 续传
    """
    log.info(f"  模型目录 : {model_dir}")
    print()

    # 仅校验模式
    if check_only:
        report = _inspect_model_dir(model_dir)
        if report["valid"]:
            log.info(f"[model] ✓ 模型目录完整有效：{model_dir}")
            log.info(f"[model]   .xml={report['xml_count']}  .bin={report['bin_count']}  总条目={report['total_entries']}")
            return True
        else:
            log.info(f"[model] ✗ 模型目录不完整：{model_dir}")
            log.info(f"[model]   .xml={report['xml_count']}  .bin={report['bin_count']}  总条目={report['total_entries']}")
            if report["reason"]:
                log.info(f"[model]   原因：{report['reason']}")
            log.info(f"[model]   建议：python setup_text_model.py --force")
            return False

    # 检查已有目录的完整性
    if not force:
        report = _inspect_model_dir(model_dir)
        if report["valid"]:
            log.warn(f"[model] 模型已存在且完整，跳过下载。（{model_dir}）")
            log.info(f"[model]   .xml={report['xml_count']}  .bin={report['bin_count']}  总条目={report['total_entries']}")
            return True
        elif report["exists"]:
            if continue_download:
                log.info(f"[model] --continue 模式：保留不完整目录，尝试断点续传。（总条目={report['total_entries']}）")
            else:
                log.warn(f"[model] ⚠ 模型目录存在但不完整（总条目={report['total_entries']} < {MODEL_MIN_TOTAL_ENTRIES}），将清除后重新下载。")
                if report["reason"]:
                    log.info(f"[model]   原因：{report['reason']}")
                shutil.rmtree(model_dir, ignore_errors=True)
                log.info(f"[model]   已清除不完整目录：{model_dir}")
                log.info(f"[model]   提示：若下载中断，可使用 --continue 续传而非重新下载。")

    if force and model_dir.exists():
        log.info(f"[model] --force 模式：删除已有目录 {model_dir}")
        shutil.rmtree(model_dir, ignore_errors=True)

    model_dir.parent.mkdir(parents=True, exist_ok=True)

    # 安全下载模式：先下载到 .partial 目录，验证后原子重命名
    partial_dir = model_dir.with_suffix(model_dir.suffix + ".partial")
    if partial_dir.exists():
        if continue_download:
            log.info(f"[model] --continue 模式：保留已有 .partial 目录，尝试断点续传。")
        else:
            log.info(f"[model] 清理残留的 .partial 目录：{partial_dir}")
            shutil.rmtree(partial_dir, ignore_errors=True)

    download_result = _download_model(
        model_id=model_id,
        output_dir=model_dir,
        partial_dir=partial_dir,
    )

    if download_result == "continue":
        return "continue"
    if download_result is not True:
        return False

    # 验证 .partial 目录中的模型完整性
    if not _verify_model_dir(partial_dir):
        log.error(
            f"[model] 下载完成，但 .partial 目录验证失败：{partial_dir}\n"
            "  请检查上方日志是否有错误。"
        )
        return False

    # 原子重命名 .partial → 最终目录
    try:
        log.info(f"[model] 验证通过，原子重命名 {partial_dir} → {model_dir}")
        partial_dir.rename(model_dir)
    except OSError as e:
        log.error(f"[model] 原子重命名失败：{e}")
        return False

    log.info(f"\n[model] ✓ 模型下载完成：{model_dir}")
    return True


# ---------------------------------------------------------------------------
# 命令行入口
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="从 ModelScope 下载 OpenVINO 文本推理模型到 SKILL_DIR/models/ 目录",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument(
        "--model-dir",
        dest="model_dir",
        default=None,
        metavar="PATH",
        help=(
            f"模型存放目录。未指定时默认为 <SKILL_DIR>/models/{DEFAULT_MODEL_NAME} "
            f"(当前: {DEFAULT_MODEL_DIR})"
        ),
    )
    parser.add_argument(
        "--model-id",
        dest="model_id",
        default=MODEL_SCOPE_ID,
        metavar="ID",
        help=f"ModelScope 模型 ID（默认：{MODEL_SCOPE_ID}）",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="强制重新下载（即使目标目录已存在）",
    )
    parser.add_argument(
        "--check-only",
        dest="check_only",
        action="store_true",
        help="仅校验模型目录是否已存在，不执行下载",
    )
    parser.add_argument(
        "--continue",
        dest="continue_download",
        action="store_true",
        help="断点续传：恢复上次中断的下载（modelscope 原生支持，自动跳过已完整文件）",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        ensure_skill_requirements(force=False)
        maybe_reexec_in_skill_venv(Path(__file__).resolve())
    except Exception as exc:
        log.error(f"[venv] ✗ 统一虚拟环境准备失败：{exc}")
        return 1

    # 确定模型目录
    if args.model_dir:
        model_dir = Path(args.model_dir)
    else:
        model_dir = DEFAULT_MODEL_DIR

    log.info("=" * 60)
    log.info("OpenVINO 文本推理模型下载脚本（ModelScope 源）")
    log.info(f"模型 ID    : {args.model_id}")
    log.info(f"模型目录   : {model_dir}")
    log.info("=" * 60)
    print()

    result = setup_text_model(
        model_dir=model_dir,
        model_id=args.model_id,
        force=args.force,
        check_only=args.check_only,
        continue_download=args.continue_download,
    )

    print()
    if result is True:
        log.info("✓ 完成。")
        return 0
    elif result == "continue":
        log.error("⏳ 下载未完成，请使用 --continue 续传：")
        log.error(f"   python setup_text_model.py --continue")
        return 3
    else:
        log.error("✗ 失败，请查看上方错误信息。")
        return 1


if __name__ == "__main__":
    sys.exit(main())