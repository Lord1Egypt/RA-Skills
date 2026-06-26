#!/usr/bin/env python3
"""
Gemini 文件输出封装脚本。

用途：
1. 调用 Gemini CLI 执行一次性请求。
2. 将结果保存到本 skill 目录下文件。
3. 以 JSON 形式输出：文件绝对路径（必选）与内容（可选）。
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

DEFAULT_MODEL: str = "gemini-3-flash-preview"


@dataclass(frozen=True)
class RunConfig:
    """脚本运行配置。"""

    prompt: str
    model: str | None
    output_format: str
    include_content: bool
    output_dir: Path
    output_file: str | None
    gemini_bin: str


def parse_args() -> RunConfig:
    """解析命令行参数并返回强类型配置。"""
    parser = argparse.ArgumentParser(
        description="Run Gemini CLI, save output to file, and return absolute file path."
    )
    parser.add_argument("--prompt", required=True, help="发送给 Gemini 的提示词。")
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help="Gemini 模型名（默认：gemini-3-flash-preview）。",
    )
    parser.add_argument(
        "--output-format",
        default="text",
        choices=("text", "json"),
        help="Gemini 输出格式。",
    )
    parser.add_argument(
        "--include-content",
        action="store_true",
        help="在标准输出 JSON 中附带生成内容。",
    )
    parser.add_argument(
        "--output-dir",
        default=str(Path(__file__).resolve().parent / "outputs"),
        help="输出目录（默认：skill 下 outputs 目录）。",
    )
    parser.add_argument(
        "--output-file",
        default=None,
        help="输出文件名（可选）。未提供时自动按时间戳生成。",
    )
    parser.add_argument(
        "--gemini-bin",
        default="gemini",
        help="Gemini CLI 可执行文件名或绝对路径。",
    )
    args = parser.parse_args()

    return RunConfig(
        prompt=args.prompt,
        model=args.model,
        output_format=args.output_format,
        include_content=args.include_content,
        output_dir=Path(args.output_dir).expanduser().resolve(),
        output_file=args.output_file,
        gemini_bin=args.gemini_bin,
    )


def build_command(config: RunConfig) -> list[str]:
    """根据配置构建 Gemini CLI 命令。"""
    cmd: list[str] = [config.gemini_bin]
    if config.model is not None and config.model.strip() != "":
        cmd.extend(["--model", config.model.strip()])
    if config.output_format == "json":
        cmd.extend(["--output-format", "json"])
    cmd.append(config.prompt)
    return cmd


def infer_filename(config: RunConfig) -> str:
    """生成输出文件名：优先使用用户指定文件名，否则按时间戳生成。"""
    if config.output_file is not None and config.output_file.strip() != "":
        return config.output_file.strip()

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    extension = "json" if config.output_format == "json" else "txt"
    return f"gemini-output-{timestamp}.{extension}"


def run_gemini(config: RunConfig) -> str:
    """执行 Gemini CLI 并返回标准输出内容。"""
    cmd = build_command(config)
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        error_payload = {
            "ok": False,
            "error": "Gemini CLI execution failed.",
            "stderr": result.stderr.strip(),
            "stdout": result.stdout.strip(),
            "exit_code": result.returncode,
        }
        print(json.dumps(error_payload, ensure_ascii=False))
        sys.exit(result.returncode)
    return result.stdout


def save_output(content: str, config: RunConfig) -> Path:
    """将结果写入文件并返回绝对路径。"""
    config.output_dir.mkdir(parents=True, exist_ok=True)
    file_name = infer_filename(config)
    output_path = (config.output_dir / file_name).resolve()
    output_path.write_text(content, encoding="utf-8")
    return output_path


def main() -> None:
    """程序入口。"""
    config = parse_args()
    content = run_gemini(config)
    output_path = save_output(content, config)

    response = {
        "ok": True,
        "file_path": str(output_path),
    }
    if config.include_content:
        response["content"] = content

    # 统一通过 JSON 返回，便于上层 agent 解析。
    print(json.dumps(response, ensure_ascii=False))


if __name__ == "__main__":
    main()
