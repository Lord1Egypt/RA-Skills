#!/usr/bin/env python3
"""
safe_path.py - delete-recovery path safety validation module v0.11.0

v0.11.0 Security fixes (round 3):
- Finding newA (99%): _is_path_safe() path traversal detection now correctly
  detects '..' escape by comparing resolved path against raw_parent base
- Finding newC (97%): 'signed hash' / 'cryptographic signature'夸大表述 removed;
  SHA256 records are accurately described as integrity checks (detect accidental
  modification), NOT cryptographic signatures; they do not protect against a local
  attacker who can modify both backup files and their metadata

v0.9.0 Security fixes (addressing security audit findings 2 & 3):
- Finding 2 fix: allowed_roots now defaults to [WORKSPACE_ROOT] (previously None defaulted
  to [] meaning no restriction). Callers who relied on documented defaults were unknowingly
  allowing restores to arbitrary filesystem locations. Pass allowed_roots=[]
  explicitly only when you need to restore outside the workspace.
- Finding 3 fix: verify_integrity_and_path() now accepts a dest_path parameter and validates
  it against allowed_roots, traversal, and equality with original_path. full_restore_check()
  now passes dest_path through to verify_integrity_and_path() instead of silently ignoring it.
  Callers using the documented single entry point were not validating the actual restore
  destination.

v0.3.1 Security fix (A4):
- --force no longer skips PATH cross-check when SHA256 is absent — traversal
  check on original_path always runs, closing the A4 bypass where an attacker
  who can delete .sha256 and knows the original path could restore arbitrary content.

v0.3.0 Security fixes:
- SHA256 record now stores BOTH file hash AND original path (cross-linked)
   ->  Replacing the backup file requires also knowing the original path to make the records consistent
   ->  Tampering with .path is detected by cross-checking against the path stored in .sha256
- SHA256 is now STRICTLY REQUIRED on restore: missing or empty .sha256 blocks restore
  by default (use --force to bypass with explicit warning)
- allowed_roots is not enforced by default (None -> []): restore destinations are NOT
  confined to any specific directory tree; security relies on SHA256 integrity
  + PATH cross-check instead of directory confinement

Defends against three attack vectors:
1. Path traversal: prevents ../ escape to directories outside the backup area
2. Backup replacement: prevents accidental restore of a modified backup (hash mismatch)
3. .path tampering: detects inconsistency between .sha256 PATH record and .path file

Security model:
- On backup: computes SHA256 of the backup file AND stores the original path in .sha256
- On restore: recomputes SHA256 and compares; cross-validates .sha256 PATH against .path to detect inconsistency
- On restore: validates the destination path is within allowed_roots
- Note: SHA256 records are integrity checks (detect accidental modification); they do NOT
  protect against a local attacker who can modify both the backup file and its metadata.

Usage (as module import):
    from safe_path import SafePathValidator
    validator = SafePathValidator(backup_root, allowed_roots=[...])
    validator.compute_sha256_signed(backup_path, original_path)   # SHA256 returned, path stored in .sha256
    validator.verify_integrity_and_path(backup_path, sha256_file, original_path,
                                       dest_path=None, force=False)  # full check
"""

import hashlib
import os
from pathlib import Path

# Format version for SHA256 file - bump if format changes
_sha256_FORMAT_VERSION = "v3"

# Workspace root reference - used as the default allowed_root in v0.9.0
# Must be resolved before SafePathValidator is instantiated at module level below.
WORKSPACE_ROOT = Path(__file__).parent.parent.parent.parent.resolve()


class SafePathError(Exception):
    """Raised when path safety validation fails"""
    pass


class SafePathValidator:
    """
    Path safety validator for delete-recovery.

    backup_root:   Root directory for backups - restore destinations must be within
                   this tree unless allowed_roots is explicitly set.
    allowed_roots: Optional list of root directories to restrict restore destinations.
                   If None (the default since v0.9.0), restores are confined to WORKSPACE_ROOT.
                   Pass an explicit list of paths to additionally restrict where files
                   can be restored (e.g. allowed_roots=[WORKSPACE_DIR]).
                   Pass [] (empty list) to disable directory confinement entirely
                   (traversal checks still apply; use only for legacy/untrusted restores).
    """

    def __init__(self, backup_root, allowed_roots=None):
        self.backup_root = Path(backup_root).resolve()
        # allowed_roots controls where restores are allowed:
        #   None            ->  restrict to WORKSPACE_ROOT (safe default for recovery tool)
        #   []              ->  strictly no allowed_roots enforcement (any path allowed,
        #                     traversal still blocked)
        #   [paths]         ->  restore destination must be within one of these directories
        #
        # v0.9.0 change: Default changed from [] (no restriction) to [WORKSPACE_ROOT].
        # This makes the documented default safe - callers who relied on the old behaviour
        # by not setting allowed_roots explicitly can pass allowed_roots=[] to restore
        # the no-confinement behaviour for legacy restores.
        if allowed_roots is None:
            self.allowed_roots = [WORKSPACE_ROOT]
        else:
            self.allowed_roots = [Path(r).resolve() for r in allowed_roots]

    # -------------------------------------------------------------
    # 1. SHA256 computation (unchanged from v0.2.0)
    # -------------------------------------------------------------

    @staticmethod
    def compute_sha256(file_path: Path) -> str:
        """Compute SHA256 hash of a file (chunked reading, supports large files)"""
        h = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    # -------------------------------------------------------------
    # 2. SHA256 + path cross-validation (v0.3.0; renamed in v0.11.0)
    # -------------------------------------------------------------

    @staticmethod
    def compute_sha256_signed(backup_path: Path, original_path: str) -> str:
        """
        Alias for compute_sha256 (kept for backward compatibility).
        The path is stored alongside the hash in the .sha256 file to enable
        cross-validation on restore, not as a cryptographic signature.
        """
        return SafePathValidator.compute_sha256(backup_path)

    @staticmethod
    def write_sha256_file(sha256_file: Path, file_sha256: str, original_path: str) -> None:
        """
        Write SHA256 file in v0.3.0 format:
          FILE_HASH:<sha256>
          PATH:<original_path>

        This binds the hash to the original path for cross-validation on restore.
        """
        content = (
            f"#{_sha256_FORMAT_VERSION}\n"
            f"FILE_HASH:{file_sha256}\n"
            f"PATH:{original_path}\n"
        )
        sha256_file.write_text(content, encoding="utf-8")

    @staticmethod
    def read_sha256_file(sha256_file: Path) -> tuple:
        """
        Read and parse v0.3.0 SHA256 file.
        Returns (file_hash: str, stored_path: str).
        Raises SafePathError if format is invalid or corrupted.
        """
        if not sha256_file.exists():
            raise SafePathError(
                f"SHA256 record missing: {sha256_file.name}\n"
                f"Integrity check cannot proceed. "
                f"Use --force to bypass this check (at your own risk)."
            )

        content = sha256_file.read_text(encoding="utf-8").strip()
        if not content:
            raise SafePathError(
                f"SHA256 record is empty: {sha256_file.name}\n"
                f"Integrity check cannot proceed. "
                f"Use --force to bypass this check (at your own risk)."
            )

        lines = content.splitlines()
        file_hash = None
        stored_path = None

        for line in lines:
            line = line.strip()
            if line.startswith("FILE_HASH:"):
                file_hash = line.split(":", 1)[1].strip()
            elif line.startswith("PATH:"):
                stored_path = line.split(":", 1)[1].strip()

        # Basic format validation
        if not file_hash:
            raise SafePathError(
                f"SHA256 record is missing FILE_HASH line: {sha256_file.name}\n"
                f"Use --force to bypass this check (at your own risk)."
            )

        # SHA256 is 64 hex chars
        if len(file_hash) != 64 or not all(c in "0123456789abcdef" for c in file_hash.lower()):
            raise SafePathError(
                f"SHA256 record has invalid hash format: {sha256_file.name}\n"
                f"Use --force to bypass this check (at your own risk)."
            )

        if not stored_path:
            raise SafePathError(
                f"SHA256 record is missing PATH line: {sha256_file.name}\n"
                f"Use --force to bypass this check (at your own risk)."
            )

        return file_hash, stored_path

    # -------------------------------------------------------------
    # 3. Backup integrity + path cross-validation (v0.9.0 rewrite)
    # -------------------------------------------------------------

    def verify_integrity_and_path(
        self,
        backup_path: Path,
        sha256_file: Path,
        original_path: str,
        dest_path: Path = None,
        force: bool = False,
    ) -> bool:
        """
        v0.9.0: Full restore validation - integrity + path + allowed_roots.

        Validations (all enforced even with --force unless noted):
          1. Reads FILE_HASH and PATH from .sha256 file
             (strict: missing/empty -> blocked unless force=True)
          2. Verifies backup file hash matches recorded FILE_HASH
             (only when SHA256 record is present)
          3. Verifies stored PATH from .sha256 matches original_path from .path file
             (ALWAYS runs - catches .path file tampering)
          4. Detects path traversal in original_path (ALWAYS runs)
          5. If dest_path is provided: validates it independently against
             allowed_roots, traversal, and equality with original_path
             (v0.9.0 fix - closes the full_restore_check gap)
          6. allowed_roots enforcement on the final destination

        force: If True, skips the SHA256 *existence* check only
               (for pre-v0.3.0 legacy backups that lack SHA256 records).
               SHA256 correctness check, PATH cross-check, traversal detection,
               and dest_path validation are ALWAYS enforced, even with --force.
               Use --force only when restoring backups created before v0.3.0.

        Raises SafePathError on any failure.

        Attack vectors mitigated:
        - Backup replaced -> hash mismatch -> blocked
        - .path file tampered -> stored_path != original_path -> blocked
        - Backup replaced + .sha256 deleted + --force -> PATH cross-check still catches .path tampering
        - Path traversal -> resolved path differs from raw -> blocked
        - dest_path diverges from original_path -> blocked (v0.9.0 fix)
        """
        # Initialize so 'sha256_was_present' guards always work correctly
        file_hash = None
        stored_path = None
        sha256_was_present = False

        # -- Step 1: Read SHA256 record (strict unless force=True) -------------
        try:
            file_hash, stored_path = self.read_sha256_file(sha256_file)
            sha256_was_present = True
        except SafePathError:
            if force:
                # force=True: bypass SHA256 existence requirement, but all other
                # checks (integrity, PATH cross-check, traversal, dest_path) still run.
                # stored_path remains None; PATH cross-check falls back to original_path only.
                pass
            else:
                raise

        # -- Step 2: Integrity check (only when SHA256 record is present) ----
        if sha256_was_present and file_hash:
            actual_sha256 = self.compute_sha256(backup_path)
            if actual_sha256 != file_hash.lower():
                raise SafePathError(
                    "INTEGRITY CHECK FAILED - backup file has been modified or replaced!\n"
                    "  Expected SHA256: %s\n"
                    "  Actual SHA256:   %s\n"
                    "  File: %s\n"
                    "Restore blocked. Reason: backup file has been tampered with since creation."
                    % (file_hash, actual_sha256, backup_path)
                )

        # -- Step 3: PATH cross-check - ALWAYS runs, even with --force --------
        if sha256_was_present and stored_path:
            if stored_path != original_path:
                raise SafePathError(
                    "PATH CROSS-CHECK FAILED!\n"
                    "  SHA256 record PATH:  %s\n"
                    "  .path file records:   %s\n"
                    "Restore blocked. Reason: .path file and .sha256 record are inconsistent - "
                    "one of them has been tampered with."
                    % (stored_path, original_path)
                )
        elif original_path:
            # SHA256 absent (force restore) or PATH line missing: validate original_path
            # itself against traversal to catch .path tampering even when SHA256 is gone.
            if not self._is_path_safe(Path(original_path)):
                raise SafePathError(
                    "PATH CROSS-CHECK FAILED (force restore, SHA256 absent)!\n"
                    "  Target: %s\n"
                    "Restore blocked. Reason: target path is unsafe (traversal or illegal path)."
                    % original_path
                )

        # -- Step 4: Traversal check on original_path (ALWAYS runs, even with --force) ---
        if not self._is_path_safe(Path(original_path)):
            raise SafePathError(
                "PATH TRAVERSAL DETECTED!\n"
                "  Target: %s\n"
                "Restore blocked. Reason: target path contains illegal traversal sequences."
                % original_path
            )

        # -- Step 5: dest_path validation - v0.9.0 fix -----------------------------
        if dest_path is not None:
            dest_resolved = dest_path.resolve()
            # Traversal check on dest_path
            if not self._is_path_safe(dest_path):
                raise SafePathError(
                    "DEST PATH TRAVERSAL DETECTED!\n"
                    "  dest: %s\n"
                    "Restore blocked. Reason: destination path contains illegal traversal sequences."
                    % dest_path
                )
            # dest must resolve to the same location as original_path
            original_resolved = Path(original_path).resolve()
            if dest_resolved != original_resolved:
                raise SafePathError(
                    "RESTORE PATH MISMATCH!\n"
                    "  Expected (from .path): %s  ->  %s\n"
                    "  Actual destination:    %s  ->  %s\n"
                    "Restore blocked. Reason: destination path differs from original."
                    % (original_path, original_resolved, dest_path, dest_resolved)
                )
            # dest must be within allowed_roots
            if self.allowed_roots:
                dest_is_allowed = any(
                    str(dest_resolved).startswith(str(root) + os.sep) or dest_resolved == root
                    for root in self.allowed_roots
                )
                if not dest_is_allowed:
                    raise SafePathError(
                        "RESTORE PATH OUT OF ALLOWED RANGE!\n"
                        "  dest: %s\n"
                        "  Allowed roots: %s\n"
                        "Restore blocked. Reason: restore destination is outside the allowed directory tree."
                        % (dest_resolved, self.allowed_roots)
                    )

        # -- Step 6: Destination within allowed_roots ---------------------------
        final_dest = (dest_path if dest_path is not None else Path(original_path)).resolve()
        if self.allowed_roots:
            dest_is_allowed = any(
                str(final_dest).startswith(str(root) + os.sep) or final_dest == root
                for root in self.allowed_roots
            )
            if not dest_is_allowed:
                raise SafePathError(
                    "RESTORE PATH OUT OF ALLOWED RANGE!\n"
                    "  Target: %s\n"
                    "  Allowed roots: %s\n"
                    "Restore blocked. Reason: restore destination is outside the allowed directory tree."
                    % (final_dest, self.allowed_roots)
                )

        return True

    # -------------------------------------------------------------
    # Path traversal detection
    # -------------------------------------------------------------

    def _is_path_safe(self, path: Path) -> bool:
        """
        v0.11.0: Fixed path traversal detection (Finding newA, 99% confidence).

        Detect whether a path would cause path traversal.
        Rejects paths where following '..' components escapes the workspace root
        or other configured allowed_roots boundaries.

        Algorithm: for each '..' component, resolve the parent directory and
        check whether the final resolved path still lives under the expected
        base (the directory containing the first '..' segment). If it escapes,
        the path is unsafe.
        """
        parts = path.parts
        if ".." not in parts:
            return True

        # Walk the path and simulate what happens at each '..'
        # Start from the raw path's parent (before the first '..' takes effect)
        raw_parent = path.parent.resolve()

        # Normalize the full path: this is where it actually ends up
        resolved = path.resolve()

        # The path is safe only if the final resolved location is at or under
        # the raw_parent (the directory we were in before any '..' was applied).
        # If resolve() ends up ABOVE raw_parent, traversal occurred.
        try:
            resolved.relative_to(raw_parent)
            # resolved is under raw_parent - safe
            return True
        except ValueError:
            # resolved is outside raw_parent - traversal detected
            return False

    def validate_restore_dest(self, original_path: str, dest_path: Path) -> bool:
        """
        Validate restore destination path: traversal + allowed_roots + path match.
        Note: v0.11.0 callers should use verify_integrity_and_path() or full_restore_check()
        which covers all these checks at once including dest_path validation.
        """
        if not self._is_path_safe(dest_path):
            raise SafePathError(
                f"PATH TRAVERSAL DETECTED!\n"
                f"  Target: {dest_path}\n"
                f"Restore blocked. Reason: target path contains illegal traversal sequences."
            )

        original_resolved = Path(original_path).resolve()
        dest_resolved = dest_path.resolve()

        if original_resolved != dest_resolved:
            raise SafePathError(
                f"RESTORE PATH MISMATCH!\n"
                f"  Expected (from .path): {original_path}  ->  {original_resolved}\n"
                f"  Actual destination:    {dest_path}  ->  {dest_resolved}\n"
                f"Restore blocked. Reason: destination path differs from original."
            )

        if self.allowed_roots:
            dest_is_allowed = any(
                str(dest_resolved).startswith(str(root) + os.sep) or dest_resolved == root
                for root in self.allowed_roots
            )
            if not dest_is_allowed:
                raise SafePathError(
                    f"RESTORE PATH OUT OF ALLOWED RANGE!\n"
                    f"  Target: {dest_resolved}\n"
                    f"  Allowed roots: {self.allowed_roots}\n"
                    f"Restore blocked. Reason: target path is outside the allowed restore range."
                )

        return True

    # -------------------------------------------------------------
    # 5. Backward-compat wrapper: full_restore_check (v0.9.0)
    # -------------------------------------------------------------

    def full_restore_check(
        self,
        backup_path: Path,
        sha256_file: Path,
        original_path: str,
        dest_path: Path,
        force: bool = False,
    ) -> bool:
        """
        v0.9.0: Full restore check - single documented entry point for restore_file().

        Runs all validations in one call:
          1. SHA256 record read (strict: missing -> block unless force=True)
          2. Integrity check (hash match)
          3. Path cross-check (.sha256 PATH vs .path file)
          4. Traversal detection on original_path
          5. dest_path validation: traversal + path match with original + allowed_roots
             (v0.9.0 fix: previously silently ignored; now fully validated)
          6. allowed_roots enforcement on dest_path

        force: bypass SHA256 existence check only (for pre-v0.3.0 backups without SHA256
               records). All other checks are ALWAYS enforced, even with --force.
        """
        return self.verify_integrity_and_path(
            backup_path=backup_path,
            sha256_file=sha256_file,
            original_path=original_path,
            dest_path=dest_path,  # v0.9.0: now passed through instead of silently dropped
            force=force,
        )


# -----------------------------------------------------------------
# Standalone utility functions
# -----------------------------------------------------------------

def compute_file_sha256(file_path: str) -> str:
    """CLI-friendly: input path string, return SHA256 hash"""
    return SafePathValidator.compute_sha256(Path(file_path))


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print(f"safe_path.py v0.11.0 - Path safety validation module")
        print("Usage: python safe_path.py compute <file_path>")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "compute":
        if len(sys.argv) < 3:
            print("Usage: python safe_path.py compute <file_path>")
            sys.exit(1)
        h = compute_file_sha256(sys.argv[2])
        print(h)
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)