from __future__ import annotations

import argparse
import re
import shutil
import unicodedata
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from _common import SkillError, load_json, sha256_file, utc_now, write_json


WORKSPACE_SCHEMA_VERSION = "2.0"
WORKSPACE_ROOT_KIND = "academic-pdf-translation-workspace-root"
BATCH_WORKSPACE_KIND = "academic-pdf-translation-batch"
WORKSPACE_ROOT_NAME = "Workspace"
VISIBLE_DIRECTORIES = {
    "input": "input",
    "output": "output",
}
HIDDEN_WORK_DIRECTORY = ".work"
JOBS_DIRECTORY = ".work/jobs"
ROOT_README = """# PDF 翻译工作区

每次翻译请求对应一个批次文件夹，名称包含创建时间、论文数量和批次标题。

批次内用户只需查看：

- `input/`：本批次原文；
- `output/`：通过所选质量档位验收后的正式译本。

翻译单元、候选文件、检查证据和历史版本位于隐藏的 `.work/`，不要手动移动。

完整规则见上一级 `references/workspace.md`。
"""
ROOT_GITIGNORE = """*
!.gitignore
!README.md
"""


@dataclass(frozen=True)
class TranslationWorkspace:
    container: Path
    root: Path
    input: Path
    output: Path
    work: Path
    jobs: Path
    manifest: Path
    title: str
    source_count: int

    def job_metadata(self) -> dict[str, str | int]:
        return {
            "container": str(self.container),
            "batch": str(self.root),
            "input": str(self.input),
            "output": str(self.output),
            "work": str(self.work),
            "jobs": str(self.jobs),
            "manifest": str(self.manifest),
            "title": self.title,
            "source_count": self.source_count,
        }


def default_workspace_root() -> Path:
    return Path(__file__).resolve().parent.parent / WORKSPACE_ROOT_NAME


def _root_contract() -> dict[str, object]:
    return {
        "schema_version": WORKSPACE_SCHEMA_VERSION,
        "kind": WORKSPACE_ROOT_KIND,
        "batch_naming": "YYYYMMDD-HHMMSS_<count>篇_<title>",
        "batch_directories": {
            **VISIBLE_DIRECTORIES,
            "work": HIDDEN_WORK_DIRECTORY,
            "jobs": JOBS_DIRECTORY,
        },
    }


def _validate_root_manifest(payload: object, manifest: Path) -> None:
    if not isinstance(payload, dict):
        raise SkillError(f"Workspace 根清单不是 JSON 对象: {manifest}")
    expected = _root_contract()
    for key, value in expected.items():
        if payload.get(key) != value:
            raise SkillError(f"Workspace 根目录契约不匹配: {manifest}")


def ensure_workspace_root(root: Path | None = None) -> Path:
    root = (root or default_workspace_root()).expanduser().resolve()
    if root.exists() and not root.is_dir():
        raise SkillError(f"Workspace 路径不是目录: {root}")
    root.mkdir(parents=True, exist_ok=True)

    manifest = root / ".workspace.json"
    if manifest.exists():
        _validate_root_manifest(load_json(manifest), manifest)
    else:
        payload = _root_contract()
        payload["created_at"] = utc_now()
        write_json(manifest, payload)

    readme = root / "README.md"
    if not readme.exists():
        readme.write_text(ROOT_README, encoding="utf-8")
    gitignore = root / ".gitignore"
    if not gitignore.exists():
        gitignore.write_text(ROOT_GITIGNORE, encoding="utf-8")
    return root


def _safe_title(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).strip()
    normalized = re.sub(r"[^\w.-]+", "-", normalized, flags=re.UNICODE)
    normalized = normalized.strip(" .-_")
    if not normalized:
        raise SkillError("批次标题不能为空")
    return normalized[:72].rstrip(" .-_")


def _safe_job_name(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).strip()
    normalized = re.sub(r"[^\w.-]+", "-", normalized, flags=re.UNICODE)
    normalized = normalized.strip(" .-_")
    if not normalized:
        normalized = "document"
    return normalized[:96].rstrip(" .-_") or "document"


def _source_paths(sources: list[Path]) -> list[Path]:
    if not sources:
        raise SkillError("创建批次工作区时至少需要一份 PDF")
    resolved: list[Path] = []
    seen: set[Path] = set()
    for value in sources:
        source = value.expanduser().resolve()
        if not source.is_file():
            raise SkillError(f"输入 PDF 不存在: {source}")
        if source.suffix.casefold() != ".pdf":
            raise SkillError(f"输入文件不是 PDF: {source}")
        if source in seen:
            raise SkillError(f"同一 PDF 在本批次中重复: {source}")
        seen.add(source)
        resolved.append(source)
    return resolved


def _unique_input_path(input_dir: Path, source: Path) -> Path:
    candidate = input_dir / source.name
    index = 2
    while candidate.exists():
        candidate = input_dir / f"{source.stem}_{index}{source.suffix}"
        index += 1
    return candidate


def _unique_batch_path(container: Path, base_name: str) -> Path:
    candidate = container / base_name
    index = 2
    while candidate.exists():
        candidate = container / f"{base_name}_{index:02d}"
        index += 1
    return candidate


def create_workspace(
    title: str,
    sources: list[Path],
    *,
    container: Path | None = None,
    created_at: datetime | None = None,
) -> TranslationWorkspace:
    container = ensure_workspace_root(container)
    source_paths = _source_paths(sources)
    local_time = created_at or datetime.now().astimezone()
    timestamp = local_time.strftime("%Y%m%d-%H%M%S")
    batch_name = (
        f"{timestamp}_{len(source_paths)}篇_{_safe_title(title)}"
    )
    root = _unique_batch_path(container, batch_name)
    input_dir = root / VISIBLE_DIRECTORIES["input"]
    output_dir = root / VISIBLE_DIRECTORIES["output"]
    work_dir = root / HIDDEN_WORK_DIRECTORY
    jobs_dir = root / JOBS_DIRECTORY
    for path in (input_dir, output_dir, jobs_dir):
        path.mkdir(parents=True, exist_ok=True)

    source_records: list[dict[str, object]] = []
    for sequence, source in enumerate(source_paths, start=1):
        destination = _unique_input_path(input_dir, source)
        shutil.copy2(source, destination)
        source_records.append(
            {
                "sequence": sequence,
                "original_path": str(source),
                "input_path": str(destination),
                "sha256": sha256_file(destination),
            }
        )

    manifest = work_dir / "batch.json"
    write_json(
        manifest,
        {
            "schema_version": WORKSPACE_SCHEMA_VERSION,
            "kind": BATCH_WORKSPACE_KIND,
            "created_at": local_time.isoformat(timespec="seconds"),
            "title": title.strip(),
            "source_count": len(source_records),
            "status": "created",
            "directories": {
                **VISIBLE_DIRECTORIES,
                "work": HIDDEN_WORK_DIRECTORY,
                "jobs": JOBS_DIRECTORY,
            },
            "sources": source_records,
        },
    )
    return open_workspace(root)


def _validate_batch_manifest(payload: object, manifest: Path) -> dict:
    if not isinstance(payload, dict):
        raise SkillError(f"批次工作区清单不是 JSON 对象: {manifest}")
    if payload.get("schema_version") != WORKSPACE_SCHEMA_VERSION:
        raise SkillError(
            f"不支持的批次工作区版本: {payload.get('schema_version')!r}"
        )
    if payload.get("kind") != BATCH_WORKSPACE_KIND:
        raise SkillError(f"目录不是学术 PDF 翻译批次: {manifest.parent.parent}")
    expected_directories = {
        **VISIBLE_DIRECTORIES,
        "work": HIDDEN_WORK_DIRECTORY,
        "jobs": JOBS_DIRECTORY,
    }
    if payload.get("directories") != expected_directories:
        raise SkillError(f"批次工作区目录契约已被修改: {manifest}")
    source_count = payload.get("source_count")
    sources = payload.get("sources")
    if (
        not isinstance(source_count, int)
        or source_count < 1
        or not isinstance(sources, list)
        or len(sources) != source_count
    ):
        raise SkillError(f"批次工作区输入数量记录无效: {manifest}")
    return payload


def open_workspace(root: Path) -> TranslationWorkspace:
    root = root.expanduser().resolve()
    manifest = root / HIDDEN_WORK_DIRECTORY / "batch.json"
    if not manifest.is_file():
        raise SkillError(f"批次工作区清单不存在: {manifest}")
    payload = _validate_batch_manifest(load_json(manifest), manifest)
    input_dir = root / VISIBLE_DIRECTORIES["input"]
    output_dir = root / VISIBLE_DIRECTORIES["output"]
    work_dir = root / HIDDEN_WORK_DIRECTORY
    jobs_dir = root / JOBS_DIRECTORY
    for path in (input_dir, output_dir, work_dir, jobs_dir):
        if not path.is_dir():
            raise SkillError(f"批次工作区标准目录不存在: {path}")
    return TranslationWorkspace(
        container=root.parent,
        root=root,
        input=input_dir,
        output=output_dir,
        work=work_dir,
        jobs=jobs_dir,
        manifest=manifest,
        title=str(payload["title"]),
        source_count=int(payload["source_count"]),
    )


def workspace_job_dir(
    workspace: TranslationWorkspace,
    source: Path,
    source_sha256: str,
    *,
    job_name: str | None = None,
) -> Path:
    if not re.fullmatch(r"[a-f0-9]{64}", source_sha256):
        raise SkillError("原文 SHA-256 格式无效")
    if job_name is not None:
        if (
            not job_name.strip()
            or Path(job_name).name != job_name
            or job_name in {".", ".."}
        ):
            raise SkillError("--job-name 必须是单个有效目录名")
        name = _safe_job_name(job_name)
    else:
        name = f"{_safe_job_name(source.stem)}-{source_sha256[:10]}"
    return workspace.jobs / name


def output_pdfs(workspace: TranslationWorkspace) -> list[Path]:
    return sorted(
        path.resolve()
        for path in workspace.output.iterdir()
        if path.is_file() and path.suffix.casefold() == ".pdf"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="管理 Skill 内部的学术 PDF 翻译批次工作区"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    root_parser = subparsers.add_parser("init", help="初始化 Workspace 根目录")
    root_parser.set_defaults(action="init")

    create_parser = subparsers.add_parser(
        "create",
        help="创建一次翻译请求对应的批次工作区",
    )
    create_parser.add_argument("--title", required=True, help="本批次可读标题")
    create_parser.add_argument("sources", nargs="+", type=Path)
    create_parser.set_defaults(action="create")

    show_parser = subparsers.add_parser(
        "show",
        help="显示一个批次的输入、输出和数量",
    )
    show_parser.add_argument("batch", type=Path)
    show_parser.set_defaults(action="show")

    output_parser = subparsers.add_parser(
        "outputs",
        help="列出一个批次已经交付的 PDF 绝对路径",
    )
    output_parser.add_argument("batch", type=Path)
    output_parser.set_defaults(action="outputs")

    args = parser.parse_args()
    try:
        if args.action == "init":
            root = ensure_workspace_root()
            print(f"Workspace 已就绪: {root}")
            return 0
        if args.action == "create":
            workspace = create_workspace(args.title, args.sources)
            print(f"批次工作区: {workspace.root}")
            print(f"翻译数量: {workspace.source_count}")
            print(f"输入目录: {workspace.input}")
            print(f"输出目录: {workspace.output}")
            return 0

        workspace = open_workspace(args.batch)
        if args.action == "show":
            print(f"批次工作区: {workspace.root}")
            print(f"批次标题: {workspace.title}")
            print(f"翻译数量: {workspace.source_count}")
            print(f"输入目录: {workspace.input}")
            print(f"输出目录: {workspace.output}")
            return 0

        outputs = output_pdfs(workspace)
        print(f"输出目录: {workspace.output}")
        print(f"已交付 PDF: {len(outputs)}")
        for path in outputs:
            print(path)
        return 0
    except SkillError as exc:
        print(f"错误: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
