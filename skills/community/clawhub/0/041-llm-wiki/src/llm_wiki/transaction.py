"""
事务化多文件写入

将一次逻辑知识操作(如 ingest = 新页面 + index 更新 + log 追加)
打包为一个可恢复事务:

1. stage 阶段收集所有文件操作(create / update)
2. apply 时先统一校验(路径越界、create 目标已存在、update 的
   expected_sha256 乐观锁),任一失败则不写入任何文件
3. 校验通过后先将受影响文件备份到 journal,再逐个原子写入
   (临时文件 + os.replace)
4. 写入中途失败时自动从 journal 回滚:恢复被更新的文件,
   删除已创建的文件
"""

import difflib
import hashlib
import os
import shutil
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from .agent_logger import get_logger

LOG = get_logger("transaction")

OP_CREATE = "create"
OP_UPDATE = "update"
_VALID_OPS = (OP_CREATE, OP_UPDATE)


class TransactionError(Exception):
    """事务校验或应用失败"""


@dataclass(frozen=True)
class FileOp:
    """单个文件操作。update 必须携带 expected_sha256(起草时读到的内容哈希)。"""

    op: str
    path: Path  # 相对于事务根目录
    content: str
    expected_sha256: str | None = None


@dataclass(frozen=True)
class TxReceipt:
    """事务应用凭证"""

    tx_id: str
    changed: list[Path]  # 相对路径,按 stage 顺序
    journal_dir: Path


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_bundle(manifest_path: Path, root: Path) -> "Transaction":
    """从 YAML manifest 加载事务。

    manifest 格式:
        ops:
          - op: create | update
            path: wiki/NewPage.md        # 相对于 root
            content_path: temp/draft.md  # 草稿文件,相对于 manifest 所在目录
            expected_sha256: "..."       # update 必需(apply 前);dry-run 可省略
    """
    import yaml  # 延迟导入,保持模块轻量

    manifest_path = Path(manifest_path)
    try:
        data = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise TransactionError(f"Malformed manifest YAML: {exc}") from exc

    if not isinstance(data, dict) or not isinstance(data.get("ops"), list):
        raise TransactionError("Manifest must contain an 'ops' list")

    tx = Transaction(root)
    for i, raw in enumerate(data["ops"]):
        if not isinstance(raw, dict):
            raise TransactionError(f"ops[{i}] must be a mapping")
        for key in ("op", "path", "content_path"):
            if key not in raw:
                raise TransactionError(f"ops[{i}] missing required key: {key}")
        content_file = Path(raw["content_path"])
        if not content_file.is_absolute():
            content_file = manifest_path.parent / content_file
        if not content_file.exists():
            raise TransactionError(f"ops[{i}] content file not found: {content_file}")
        expected = raw.get("expected_sha256")
        if expected is not None and not isinstance(expected, str):
            raise TransactionError(
                f"ops[{i}].expected_sha256 must be a quoted string "
                f"(unquoted all-digit hashes are parsed as numbers by YAML)"
            )
        tx.stage(
            FileOp(
                op=str(raw["op"]),
                path=Path(str(raw["path"])),
                content=content_file.read_text(encoding="utf-8"),
                expected_sha256=expected,
            )
        )
    return tx


@dataclass(frozen=True)
class OpCheck:
    """单个操作的 dry-run 软校验结果"""

    op: FileOp
    ok: bool
    detail: str


class Transaction:
    """一组文件操作的原子应用器"""

    def __init__(self, root: Path, journal_root: Path | None = None):
        self.root = Path(root).resolve()
        self.journal_root = (
            Path(journal_root)
            if journal_root
            else self.root / ".backups" / "transactions"
        )
        self._ops: list[FileOp] = []

    @property
    def ops(self) -> list[FileOp]:
        """已暂存的操作(只读副本)"""
        return list(self._ops)

    def stage(self, op: FileOp) -> None:
        if op.op not in _VALID_OPS:
            raise TransactionError(
                f"Unknown op: {op.op!r} (expected one of {_VALID_OPS})"
            )
        self._ops.append(op)

    def diff(self) -> str:
        """生成所有已暂存操作的 unified diff 预览;不写入任何文件。"""
        chunks: list[str] = []
        for op in self._ops:
            target = self._resolve(op.path)
            old = (
                target.read_text(encoding="utf-8")
                if op.op == OP_UPDATE and target.exists()
                else ""
            )
            old_lines = old.splitlines(keepends=True)
            new_lines = op.content.splitlines(keepends=True)
            chunks.append(
                "".join(
                    difflib.unified_diff(
                        old_lines,
                        new_lines,
                        fromfile=f"a/{op.path.as_posix()}"
                        if op.op == OP_UPDATE
                        else "/dev/null",
                        tofile=f"b/{op.path.as_posix()}",
                    )
                )
            )
        return "\n".join(chunks)

    def check(self) -> list[OpCheck]:
        """逐项软校验,不抛出、不写入。供 dry-run 输出状态与当前哈希。"""
        checks: list[OpCheck] = []
        for op in self._ops:
            try:
                target = self._resolve(op.path)
            except TransactionError as exc:
                checks.append(OpCheck(op, False, str(exc)))
                continue
            if op.op == OP_CREATE:
                if target.exists():
                    checks.append(OpCheck(op, False, "target already exists"))
                else:
                    checks.append(OpCheck(op, True, "new file"))
            else:  # update
                if not target.exists():
                    checks.append(OpCheck(op, False, "target does not exist"))
                    continue
                current = sha256_text(target.read_text(encoding="utf-8"))
                if op.expected_sha256 is None:
                    checks.append(OpCheck(op, True, f"current sha256: {current}"))
                elif current != op.expected_sha256:
                    checks.append(
                        OpCheck(
                            op,
                            False,
                            f"hash mismatch: expected {op.expected_sha256[:12]}..., "
                            f"current {current[:12]}...",
                        )
                    )
                else:
                    checks.append(OpCheck(op, True, "hash verified"))
        return checks

    def apply(self) -> TxReceipt:
        """校验 -> 备份 -> 写入;写入失败自动回滚。"""
        tx_id = f"{datetime.now(UTC).strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:8]}"
        LOG.info("apply: tx=%s ops=%d", tx_id, len(self._ops))
        self._verify_all()

        journal_dir = self.journal_root / tx_id
        journal_dir.mkdir(parents=True, exist_ok=False)
        written: list[FileOp] = []
        try:
            for op in self._ops:
                self._journal(op, journal_dir)
                self._write(op)
                written.append(op)
        except Exception as exc:
            LOG.error("apply failed mid-transaction (%s), rolling back", exc)
            self._rollback(written, journal_dir)
            raise TransactionError(
                f"Transaction {tx_id} failed and was rolled back: {exc}"
            ) from exc

        receipt = TxReceipt(
            tx_id=tx_id, changed=[op.path for op in self._ops], journal_dir=journal_dir
        )
        LOG.info(
            "apply complete: tx=%s changed=%d journal=%s",
            tx_id,
            len(receipt.changed),
            journal_dir,
        )
        return receipt

    # ---- 内部 ----

    def _resolve(self, rel: Path) -> Path:
        target = (self.root / rel).resolve()
        if not target.is_relative_to(self.root):
            raise TransactionError(f"Path escapes transaction root: {rel}")
        return target

    def _verify_all(self) -> None:
        if not self._ops:
            raise TransactionError("Transaction has no staged operations")
        seen = set()
        for op in self._ops:
            if op.path in seen:
                raise TransactionError(f"Duplicate path in transaction: {op.path}")
            seen.add(op.path)
            target = self._resolve(op.path)
            if op.op == OP_CREATE:
                if target.exists():
                    raise TransactionError(f"create target already exists: {op.path}")
            else:  # update
                if op.expected_sha256 is None:
                    raise TransactionError(
                        f"update requires expected_sha256: {op.path}"
                    )
                if not target.exists():
                    raise TransactionError(f"update target does not exist: {op.path}")
                actual = sha256_text(target.read_text(encoding="utf-8"))
                if actual != op.expected_sha256:
                    raise TransactionError(
                        f"Hash mismatch for {op.path}: expected {op.expected_sha256[:12]}..., "
                        f"actual {actual[:12]}... (file changed since draft)"
                    )

    def _journal(self, op: FileOp, journal_dir: Path) -> None:
        """保存更新前的原像;create 记录"原本不存在"标记。"""
        backup = journal_dir / op.path
        backup.parent.mkdir(parents=True, exist_ok=True)
        target = self._resolve(op.path)
        if op.op == OP_UPDATE:
            shutil.copy2(target, backup)
        else:
            marker = journal_dir / f"{op.path}.did-not-exist"
            marker.parent.mkdir(parents=True, exist_ok=True)
            marker.write_text("", encoding="utf-8")

    def _write(self, op: FileOp) -> None:
        target = self._resolve(op.path)
        target.parent.mkdir(parents=True, exist_ok=True)
        tmp = target.with_name(f"{target.name}.tmp-{os.getpid()}")
        tmp.write_text(op.content, encoding="utf-8")
        os.replace(tmp, target)
        LOG.debug("wrote %s (%d bytes)", op.path, len(op.content))

    def _rollback(self, written: list[FileOp], journal_dir: Path) -> None:
        for op in reversed(written):
            target = self._resolve(op.path)
            if op.op == OP_CREATE:
                target.unlink(missing_ok=True)
                LOG.debug("rollback: removed created file %s", op.path)
            else:
                shutil.copy2(journal_dir / op.path, target)
                LOG.debug("rollback: restored %s", op.path)
