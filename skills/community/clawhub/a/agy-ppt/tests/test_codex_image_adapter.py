#!/usr/bin/env python3
"""Tests for the AGY -> Codex image adapter.

Run with either::

    python3 -m unittest discover -s skills/agy-ppt/tests -t .
    python3 -m pytest skills/agy-ppt/tests/test_codex_image_adapter.py

These tests never launch a real Codex process and never consume Codex/ChatGPT
subscription quota. The Codex turn is faked either by monkeypatching
``run_codex`` or by pointing the adapter at a tiny local stub ``codex`` script
that emits canned JSONL and writes a fake artifact.
"""

from __future__ import annotations

import json
import os
import struct
import sys
import tempfile
import textwrap
import unittest
import zlib
from pathlib import Path
from unittest import mock

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import codex_image_adapter as adapter  # noqa: E402
from codex_image_adapter import (  # noqa: E402
    BACKEND,
    ERROR_ARTIFACT_AMBIGUOUS,
    ERROR_ARTIFACT_NOT_FOUND,
    ERROR_BACKEND_UNAVAILABLE,
    ERROR_CODEX_AUTH_UNAVAILABLE,
    ERROR_CODEX_CLI_UNAVAILABLE,
    ERROR_GENERATION_FAILED,
    ERROR_INVALID_REQUEST,
    ERROR_OUTPUT_INVALID,
    ERROR_OUTPUT_PATH_CONFLICT,
    ERROR_TIMEOUT,
    OP_GENERATE,
    OP_PROBE,
    OP_REGENERATE,
    STATUS_AVAILABLE,
    STATUS_COMPLETED,
    STATUS_ERROR,
    STATUS_UNAVAILABLE,
    AdapterResult,
    CodexImageAdapter,
    CodexRun,
    CodexUnavailableError,
    ImageRequest,
    InvalidRequestError,
    OutputPathError,
    build_probe_prompt,
    build_worker_prompt,
    discover_artifact,
    resolve_output_path,
    sanitize_env,
    sniff_image,
    snapshot_generated_images,
)


def make_png(path: Path, width: int = 1536, height: int = 864) -> None:
    """Write a tiny but structurally valid PNG (IHDR + IDAT + IEND)."""
    path.parent.mkdir(parents=True, exist_ok=True)

    def chunk(tag: bytes, data: bytes) -> bytes:
        body = tag + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body))

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    raw = b"\x00" + b"\x00\x00\x00" * width
    idat = zlib.compress(raw)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", idat) + chunk(b"IEND", b"")
    path.write_bytes(png)


def fake_run(
    *,
    thread_id: str = "thread-xyz",
    agent_text: str = "",
    reported_paths=None,
    returncode: int = 0,
    timed_out: bool = False,
    stderr: str = "",
) -> CodexRun:
    return CodexRun(
        returncode=returncode,
        events=[],
        agent_text=agent_text,
        stderr=stderr,
        timed_out=timed_out,
        thread_id=thread_id,
        reported_paths=list(reported_paths or []),
        command=list(adapter.DEFAULT_COMMAND),
    )


class TempWorkspaceMixin:
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.workspace = Path(self._tmp.name) / "ws"
        self.workspace.mkdir(parents=True)
        self.codex_home = Path(self._tmp.name) / "codex_home"
        self.images_root = self.codex_home / "generated_images"
        self.images_root.mkdir(parents=True)
        self.env_patch = mock.patch.dict(
            os.environ, {"CODEX_HOME": str(self.codex_home)}, clear=False
        )
        self.env_patch.start()

    def tearDown(self) -> None:
        self.env_patch.stop()
        self._tmp.cleanup()

    def make_request(self, **overrides):
        data = {
            "slide_id": "slide_03",
            "operation": OP_GENERATE,
            "prompt": "a clean 16:9 title slide",
            "output_path": "origin_image/slide_03.png",
            "aspect_ratio": "16:9",
            "workspace_root": str(self.workspace),
        }
        data.update(overrides)
        return ImageRequest.from_dict(data)


# ---------------------------------------------------------------------------
# 1. input schema
# ---------------------------------------------------------------------------
class InputSchemaTests(unittest.TestCase):
    def test_valid_generate_request(self):
        request = ImageRequest.from_dict(
            {
                "slide_id": "slide_01",
                "operation": "generate",
                "prompt": "hello",
                "output_path": "origin_image/slide_01.png",
            }
        )
        self.assertEqual(request.operation, OP_GENERATE)
        self.assertEqual(request.slide_id, "slide_01")
        self.assertEqual(request.command, adapter.DEFAULT_COMMAND)

    def test_operation_defaults_to_generate(self):
        request = ImageRequest.from_dict({"prompt": "x", "output_path": "a/b.png"})
        self.assertEqual(request.operation, OP_GENERATE)

    def test_generate_requires_prompt(self):
        with self.assertRaises(InvalidRequestError):
            ImageRequest.from_dict({"operation": "generate", "output_path": "a.png"})

    def test_generate_requires_output_path(self):
        with self.assertRaises(InvalidRequestError):
            ImageRequest.from_dict({"operation": "generate", "prompt": "x"})

    def test_non_object_request_rejected(self):
        with self.assertRaises(InvalidRequestError):
            ImageRequest.from_dict(["not", "an", "object"])  # type: ignore[arg-type]

    def test_bad_command_type_rejected(self):
        with self.assertRaises(InvalidRequestError):
            ImageRequest.from_dict(
                {"operation": "probe", "command": "codex exec"}  # not a list
            )

    def test_bad_timeout_rejected(self):
        with self.assertRaises(InvalidRequestError):
            ImageRequest.from_dict({"operation": "probe", "timeout_seconds": -1})


# ---------------------------------------------------------------------------
# 2. unsupported operation
# ---------------------------------------------------------------------------
class UnsupportedOperationTests(unittest.TestCase):
    def test_unsupported_operation_rejected(self):
        with self.assertRaises(InvalidRequestError):
            ImageRequest.from_dict({"operation": "delete", "prompt": "x", "output_path": "a.png"})

    def test_edit_is_not_supported_in_v1(self):
        with self.assertRaises(InvalidRequestError):
            ImageRequest.from_dict({"operation": "edit", "prompt": "x", "output_path": "a.png"})


# ---------------------------------------------------------------------------
# 3/4/5/6. output path safety
# ---------------------------------------------------------------------------
class OutputPathTests(TempWorkspaceMixin, unittest.TestCase):
    def test_path_traversal_rejected(self):
        with self.assertRaises(OutputPathError) as ctx:
            resolve_output_path(str(self.workspace), "../escape.png", OP_GENERATE)
        self.assertEqual(ctx.exception.error_code, ERROR_OUTPUT_INVALID)

    def test_absolute_path_outside_workspace_rejected(self):
        with self.assertRaises(OutputPathError) as ctx:
            resolve_output_path(str(self.workspace), "/etc/passwd.png", OP_GENERATE)
        self.assertEqual(ctx.exception.error_code, ERROR_OUTPUT_INVALID)

    def test_valid_relative_path_inside_workspace(self):
        resolved = resolve_output_path(str(self.workspace), "origin_image/s.png", OP_GENERATE)
        self.assertTrue(str(resolved).startswith(str(self.workspace.resolve())))

    def test_output_conflict_on_generate(self):
        target = self.workspace / "origin_image" / "slide_03.png"
        make_png(target)
        with self.assertRaises(OutputPathError) as ctx:
            resolve_output_path(str(self.workspace), "origin_image/slide_03.png", OP_GENERATE)
        self.assertEqual(ctx.exception.error_code, ERROR_OUTPUT_PATH_CONFLICT)

    def test_regenerate_allows_overwrite(self):
        target = self.workspace / "origin_image" / "slide_03.png"
        make_png(target)
        # Must not raise for regenerate.
        resolved = resolve_output_path(
            str(self.workspace), "origin_image/slide_03.png", OP_REGENERATE
        )
        self.assertEqual(resolved, target.resolve() if target.exists() else target)

    def test_directory_target_rejected(self):
        (self.workspace / "adir").mkdir()
        with self.assertRaises(OutputPathError) as ctx:
            resolve_output_path(str(self.workspace), "adir", OP_REGENERATE)
        self.assertEqual(ctx.exception.error_code, ERROR_OUTPUT_INVALID)


# ---------------------------------------------------------------------------
# 7. Codex command construction
# ---------------------------------------------------------------------------
class CommandConstructionTests(unittest.TestCase):
    def test_default_command_is_exec_json(self):
        self.assertEqual(
            adapter.DEFAULT_COMMAND,
            ("codex", "exec", "--json", "--skip-git-repo-check"),
        )

    def test_custom_command_preserved(self):
        request = ImageRequest.from_dict(
            {
                "operation": "probe",
                "command": ["codex", "exec", "--json"],
            }
        )
        self.assertEqual(request.command, ("codex", "exec", "--json"))


# ---------------------------------------------------------------------------
# 8. OAuth / API-key env stripping
# ---------------------------------------------------------------------------
class EnvStrippingTests(unittest.TestCase):
    def test_openai_api_key_stripped(self):
        env, removed = sanitize_env(
            {"PATH": "/usr/bin", "OPENAI_API_KEY": "sk-secret", "HOME": "/home/x"}
        )
        self.assertNotIn("OPENAI_API_KEY", env)
        self.assertIn("OPENAI_API_KEY", removed)
        self.assertIn("PATH", env)

    def test_token_pattern_stripped(self):
        env, removed = sanitize_env(
            {"MY_ACCESS_TOKEN": "abc", "SOME_REFRESH_TOKEN": "def", "KEEP": "1"}
        )
        self.assertNotIn("MY_ACCESS_TOKEN", env)
        self.assertNotIn("SOME_REFRESH_TOKEN", env)
        self.assertIn("KEEP", env)
        self.assertEqual(sorted(removed), ["MY_ACCESS_TOKEN", "SOME_REFRESH_TOKEN"])

    def test_removed_reports_names_not_values(self):
        _, removed = sanitize_env({"OPENAI_API_KEY": "sk-supersecret"})
        self.assertEqual(removed, ["OPENAI_API_KEY"])
        self.assertNotIn("sk-supersecret", "".join(removed))

    def test_adapter_records_stripped_env_in_diagnostics(self):
        request = ImageRequest.from_dict(
            {"operation": "probe", "env": {"OPENAI_API_KEY": "sk-x", "PATH": "/bin"}}
        )
        inst = CodexImageAdapter(request)
        self.assertIn("OPENAI_API_KEY", inst.stripped_env)
        self.assertIn("OPENAI_API_KEY", inst.base_diagnostics()["credential_env_stripped"])


# ---------------------------------------------------------------------------
# 9/10/11. prompt boundary
# ---------------------------------------------------------------------------
class PromptBoundaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.request = ImageRequest.from_dict(
            {
                "slide_id": "slide_09",
                "operation": "generate",
                "prompt": "AUTHORITATIVE SLIDE CONTENT",
                "output_path": "origin_image/slide_09.png",
                "aspect_ratio": "16:9",
            }
        )
        self.prompt = build_worker_prompt(self.request)

    def test_prompt_forbids_api_fallback(self):
        self.assertIn("OPENAI_API_KEY", self.prompt)
        self.assertIn("image_gen.py", self.prompt)
        self.assertIn("paid API fallback", self.prompt)

    def test_prompt_requires_builtin_image_gen(self):
        self.assertIn("image_gen", self.prompt)
        self.assertIn("$imagegen", self.prompt)

    def test_prompt_forbids_kiro(self):
        self.assertIn("call Kiro", self.prompt)

    def test_prompt_forbids_coding(self):
        self.assertIn("write, run, or edit code", self.prompt)

    def test_prompt_forbids_content_modification(self):
        self.assertIn("NOT modify slide content", self.prompt)

    def test_prompt_carries_authoritative_content_verbatim(self):
        self.assertIn("AUTHORITATIVE SLIDE CONTENT", self.prompt)

    def test_prompt_single_image_only(self):
        self.assertIn("exactly ONE image", self.prompt)

    def test_prompt_unavailable_instruction(self):
        self.assertIn("IMAGE_BACKEND_UNAVAILABLE", self.prompt)

    def test_probe_prompt_does_not_generate(self):
        probe = build_probe_prompt()
        self.assertIn("Do NOT generate any image", probe)
        self.assertIn("IMAGE_BACKEND_AVAILABLE", probe)
        self.assertIn("IMAGE_BACKEND_UNAVAILABLE", probe)


# ---------------------------------------------------------------------------
# 12/13. timeout & process teardown
# ---------------------------------------------------------------------------
class TimeoutTests(TempWorkspaceMixin, unittest.TestCase):
    def test_timeout_maps_to_codex_timeout(self):
        request = self.make_request()
        with mock.patch.object(adapter, "run_codex", return_value=fake_run(timed_out=True)):
            result = CodexImageAdapter(request).run()
        self.assertEqual(result.status, STATUS_ERROR)
        self.assertEqual(result.error_code, ERROR_TIMEOUT)

    def test_terminate_group_signals_and_kills(self):
        proc = mock.Mock()
        # Alive at first poll, then still alive after SIGTERM wait -> SIGKILL.
        proc.poll.side_effect = [None, None]
        proc.wait.side_effect = [adapter.subprocess.TimeoutExpired("codex", 1), 0]
        with mock.patch.object(adapter, "_signal_group") as signal_group:
            adapter._terminate_group(proc, 1.0)
        # SIGTERM then SIGKILL
        self.assertEqual(signal_group.call_count, 2)


# ---------------------------------------------------------------------------
# 14/15/16. codex missing / auth failure / backend unavailable
# ---------------------------------------------------------------------------
class CodexAvailabilityTests(TempWorkspaceMixin, unittest.TestCase):
    def test_codex_executable_missing(self):
        request = self.make_request()
        with mock.patch.object(
            adapter, "run_codex", side_effect=CodexUnavailableError("codex executable not found")
        ):
            result = CodexImageAdapter(request).run()
        self.assertEqual(result.status, STATUS_ERROR)
        self.assertEqual(result.error_code, ERROR_CODEX_CLI_UNAVAILABLE)

    def test_auth_failure_classified(self):
        request = self.make_request()
        with mock.patch.object(
            adapter, "run_codex", return_value=fake_run(agent_text="Error: Not logged in")
        ):
            result = CodexImageAdapter(request).run()
        self.assertEqual(result.error_code, ERROR_CODEX_AUTH_UNAVAILABLE)

    def test_auth_failure_via_stderr(self):
        request = self.make_request()
        with mock.patch.object(
            adapter,
            "run_codex",
            return_value=fake_run(agent_text="", stderr="401 Unauthorized"),
        ):
            result = CodexImageAdapter(request).run()
        self.assertEqual(result.error_code, ERROR_CODEX_AUTH_UNAVAILABLE)

    def test_backend_unavailable_classified(self):
        request = self.make_request()
        with mock.patch.object(
            adapter, "run_codex", return_value=fake_run(agent_text="IMAGE_BACKEND_UNAVAILABLE")
        ):
            result = CodexImageAdapter(request).run()
        self.assertEqual(result.error_code, ERROR_BACKEND_UNAVAILABLE)


# ---------------------------------------------------------------------------
# 17. fallback suggestion must not be auto-adopted
# ---------------------------------------------------------------------------
class NoAutoFallbackTests(TempWorkspaceMixin, unittest.TestCase):
    def test_fallback_suggestion_does_not_produce_completed(self):
        # Codex text suggests the CLI/API fallback but produces no artifact.
        request = self.make_request()
        text = (
            "The built-in image_gen tool is unavailable. You could use "
            "scripts/image_gen.py with OPENAI_API_KEY instead."
        )
        with mock.patch.object(adapter, "run_codex", return_value=fake_run(agent_text=text)):
            result = CodexImageAdapter(request).run()
        self.assertEqual(result.status, STATUS_ERROR)
        self.assertEqual(result.error_code, ERROR_BACKEND_UNAVAILABLE)
        self.assertFalse(result.diagnostics["api_fallback_used"])

    def test_diagnostics_never_flag_api_fallback_used(self):
        request = self.make_request()
        artifact = self.images_root / "thread-xyz" / "exec-1.png"
        make_png(artifact)
        run = fake_run(reported_paths=[str(artifact)])
        with mock.patch.object(adapter, "run_codex", return_value=run):
            result = CodexImageAdapter(request).run()
        self.assertEqual(result.status, STATUS_COMPLETED)
        self.assertFalse(result.diagnostics["api_fallback_used"])


# ---------------------------------------------------------------------------
# 18/19/20/21. artifact discovery
# ---------------------------------------------------------------------------
class ArtifactDiscoveryTests(TempWorkspaceMixin, unittest.TestCase):
    def test_explicit_reported_path_preferred(self):
        artifact = self.images_root / "thread-xyz" / "exec-1.png"
        make_png(artifact)
        before = snapshot_generated_images(self.images_root)
        run = fake_run(reported_paths=[str(artifact)])
        discovery = discover_artifact(run, self.images_root, before)
        self.assertEqual(discovery.path, artifact)
        self.assertEqual(discovery.method, "explicit_reported_path")

    def test_before_after_diff_scoped_to_thread(self):
        # A pre-existing artifact should be ignored; only the new one counts.
        old = self.images_root / "other" / "exec-old.png"
        make_png(old)
        before = snapshot_generated_images(self.images_root)
        new = self.images_root / "thread-xyz" / "exec-new.png"
        make_png(new)
        run = fake_run(reported_paths=[])
        discovery = discover_artifact(run, self.images_root, before)
        self.assertEqual(discovery.path, new)
        self.assertEqual(discovery.method, "thread_scoped_diff")
        self.assertFalse(discovery.ambiguous)

    def test_multiple_new_artifacts_return_ambiguous_no_selection(self):
        before = snapshot_generated_images(self.images_root)
        a = self.images_root / "thread-xyz" / "a.png"
        b = self.images_root / "thread-xyz" / "b.png"
        make_png(a)
        make_png(b)
        os.utime(b, (10_000_000_100, 10_000_000_100))
        os.utime(a, (10_000_000_000, 10_000_000_000))
        run = fake_run(reported_paths=[])
        discovery = discover_artifact(run, self.images_root, before)
        # Never guesses: ambiguous, no path chosen, both candidates listed.
        self.assertTrue(discovery.ambiguous)
        self.assertIsNone(discovery.path)
        self.assertEqual(sorted(discovery.candidates), sorted([str(a), str(b)]))

    def test_no_new_artifact_returns_none(self):
        make_png(self.images_root / "thread-xyz" / "exec-old.png")
        before = snapshot_generated_images(self.images_root)
        run = fake_run(reported_paths=[])
        discovery = discover_artifact(run, self.images_root, before)
        self.assertIsNone(discovery.path)

    def test_invalid_image_artifact_ignored_in_diff(self):
        before = snapshot_generated_images(self.images_root)
        bogus = self.images_root / "thread-xyz" / "not-an-image.png"
        bogus.parent.mkdir(parents=True, exist_ok=True)
        bogus.write_text("this is not a png", encoding="utf-8")
        run = fake_run(reported_paths=[])
        discovery = discover_artifact(run, self.images_root, before)
        self.assertIsNone(discovery.path)


class ImageValidationTests(TempWorkspaceMixin, unittest.TestCase):
    def test_sniff_valid_png(self):
        p = self.workspace / "ok.png"
        make_png(p, width=1536, height=864)
        info = sniff_image(p)
        self.assertIsNotNone(info)
        self.assertEqual(info.fmt, "png")
        self.assertEqual((info.width, info.height), (1536, 864))

    def test_sniff_rejects_text_file(self):
        p = self.workspace / "bad.png"
        p.write_text("nope", encoding="utf-8")
        self.assertIsNone(sniff_image(p))

    def test_zero_byte_file_is_invalid(self):
        p = self.workspace / "empty.png"
        p.write_bytes(b"")
        self.assertIsNone(sniff_image(p))

    def test_render_rejects_zero_byte_artifact(self):
        request = self.make_request()
        artifact = self.images_root / "thread-xyz" / "exec-1.png"
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_bytes(b"")
        run = fake_run(reported_paths=[str(artifact)])
        with mock.patch.object(adapter, "run_codex", return_value=run):
            result = CodexImageAdapter(request).run()
        # A zero-byte file is not a valid image, so discovery ignores it.
        self.assertEqual(result.status, STATUS_ERROR)
        self.assertIn(result.error_code, {ERROR_ARTIFACT_NOT_FOUND, ERROR_OUTPUT_INVALID})

    def test_render_rejects_invalid_artifact(self):
        request = self.make_request()
        artifact = self.images_root / "thread-xyz" / "exec-1.png"
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text("garbage", encoding="utf-8")
        run = fake_run(reported_paths=[str(artifact)])
        with mock.patch.object(adapter, "run_codex", return_value=run):
            result = CodexImageAdapter(request).run()
        self.assertEqual(result.status, STATUS_ERROR)


# ---------------------------------------------------------------------------
# 22. structured result + successful placement
# ---------------------------------------------------------------------------
class StructuredResultTests(TempWorkspaceMixin, unittest.TestCase):
    def test_successful_generate_places_artifact(self):
        request = self.make_request()
        artifact = self.images_root / "thread-xyz" / "exec-1.png"
        make_png(artifact, width=1536, height=864)
        run = fake_run(reported_paths=[f"ARTIFACT_PATH: {artifact}"])
        with mock.patch.object(adapter, "run_codex", return_value=run):
            result = CodexImageAdapter(request).run()
        self.assertEqual(result.status, STATUS_COMPLETED, result.error_message)
        self.assertEqual(result.backend, BACKEND)
        self.assertEqual(result.output_path, "origin_image/slide_03.png")
        placed = self.workspace / "origin_image" / "slide_03.png"
        self.assertTrue(placed.is_file())
        self.assertGreater(placed.stat().st_size, 0)

    def test_result_shape(self):
        result = AdapterResult(
            status=STATUS_COMPLETED,
            slide_id="slide_03",
            operation="generate",
            backend=BACKEND,
            output_path="origin_image/slide_03.png",
        )
        payload = result.to_dict()
        self.assertEqual(payload["status"], "completed")
        self.assertEqual(payload["backend"], BACKEND)
        self.assertEqual(payload["control"], "returned_to_agy")
        self.assertEqual(payload["next_step_owner"], "AGY")
        self.assertIn("diagnostics", payload)
        self.assertIn("warnings", payload)

    def test_regenerate_overwrites_existing_output(self):
        target = self.workspace / "origin_image" / "slide_03.png"
        make_png(target, width=800, height=450)
        original_bytes = target.read_bytes()
        request = self.make_request(operation=OP_REGENERATE)
        artifact = self.images_root / "thread-xyz" / "exec-2.png"
        make_png(artifact, width=1536, height=864)
        run = fake_run(reported_paths=[str(artifact)])
        with mock.patch.object(adapter, "run_codex", return_value=run):
            result = CodexImageAdapter(request).run()
        self.assertEqual(result.status, STATUS_COMPLETED, result.error_message)
        self.assertNotEqual(target.read_bytes(), original_bytes)

    def test_generate_conflict_returns_error_before_codex(self):
        target = self.workspace / "origin_image" / "slide_03.png"
        make_png(target)
        request = self.make_request(operation=OP_GENERATE)
        with mock.patch.object(adapter, "run_codex") as run_codex:
            result = CodexImageAdapter(request).run()
        run_codex.assert_not_called()  # must not spend a Codex turn on a conflict
        self.assertEqual(result.error_code, ERROR_OUTPUT_PATH_CONFLICT)

    def test_aspect_ratio_mismatch_warns_not_redraws(self):
        request = self.make_request(aspect_ratio="16:9")
        artifact = self.images_root / "thread-xyz" / "exec-sq.png"
        make_png(artifact, width=1024, height=1024)  # square, not 16:9
        run = fake_run(reported_paths=[str(artifact)])
        with mock.patch.object(adapter, "run_codex", return_value=run):
            result = CodexImageAdapter(request).run()
        self.assertEqual(result.status, STATUS_COMPLETED, result.error_message)
        self.assertTrue(any("aspect ratio" in w for w in result.warnings))

    def test_generation_failed_on_nonzero_exit(self):
        request = self.make_request()
        run = fake_run(returncode=3, agent_text="something broke")
        with mock.patch.object(adapter, "run_codex", return_value=run):
            result = CodexImageAdapter(request).run()
        self.assertEqual(result.error_code, ERROR_GENERATION_FAILED)

    def test_ambiguous_artifacts_return_error_and_do_not_place(self):
        # No explicit path; two valid new artifacts appear *during* the turn.
        request = self.make_request()
        a = self.images_root / "thread-xyz" / "a.png"
        b = self.images_root / "thread-xyz" / "b.png"

        def side_effect(*args, **kwargs):
            make_png(a, width=1536, height=864)
            make_png(b, width=1536, height=864)
            return fake_run(reported_paths=[])

        with mock.patch.object(adapter, "run_codex", side_effect=side_effect):
            result = CodexImageAdapter(request).run()
        self.assertEqual(result.status, STATUS_ERROR)
        self.assertEqual(result.error_code, ERROR_ARTIFACT_AMBIGUOUS)
        # Candidates are reported for AGY, but nothing is placed.
        candidates = result.diagnostics["artifact_discovery"]["candidates"]
        self.assertEqual(sorted(candidates), sorted([str(a), str(b)]))
        self.assertFalse((self.workspace / "origin_image" / "slide_03.png").exists())

    def test_explicit_path_wins_even_with_multiple_new_artifacts(self):
        # If Codex reports one explicit path, ambiguity does not trigger.
        request = self.make_request()
        chosen = self.images_root / "thread-xyz" / "chosen.png"
        other = self.images_root / "thread-xyz" / "other.png"

        def side_effect(*args, **kwargs):
            make_png(chosen, width=1536, height=864)
            make_png(other, width=1536, height=864)
            return fake_run(reported_paths=[str(chosen)])

        with mock.patch.object(adapter, "run_codex", side_effect=side_effect):
            result = CodexImageAdapter(request).run()
        self.assertEqual(result.status, STATUS_COMPLETED, result.error_message)
        self.assertEqual(result.diagnostics["artifact_source"], str(chosen))


# ---------------------------------------------------------------------------
# 23/24. probe
# ---------------------------------------------------------------------------
class ProbeTests(TempWorkspaceMixin, unittest.TestCase):
    def test_probe_available(self):
        request = ImageRequest.from_dict({"operation": "probe"})
        run = fake_run(agent_text="IMAGE_BACKEND_AVAILABLE")
        with mock.patch.object(adapter, "run_codex", return_value=run):
            result = CodexImageAdapter(request).run()
        self.assertEqual(result.status, STATUS_AVAILABLE)
        self.assertEqual(result.backend, BACKEND)

    def test_probe_unavailable(self):
        request = ImageRequest.from_dict({"operation": "probe"})
        run = fake_run(agent_text="IMAGE_BACKEND_UNAVAILABLE")
        with mock.patch.object(adapter, "run_codex", return_value=run):
            result = CodexImageAdapter(request).run()
        self.assertEqual(result.status, STATUS_UNAVAILABLE)
        self.assertEqual(result.error_code, ERROR_BACKEND_UNAVAILABLE)

    def test_probe_codex_missing(self):
        request = ImageRequest.from_dict({"operation": "probe"})
        with mock.patch.object(
            adapter, "run_codex", side_effect=CodexUnavailableError("not found")
        ):
            result = CodexImageAdapter(request).run()
        self.assertEqual(result.status, STATUS_UNAVAILABLE)
        self.assertEqual(result.error_code, ERROR_CODEX_CLI_UNAVAILABLE)

    def test_probe_auth_failure(self):
        request = ImageRequest.from_dict({"operation": "probe"})
        run = fake_run(agent_text="please run codex login")
        with mock.patch.object(adapter, "run_codex", return_value=run):
            result = CodexImageAdapter(request).run()
        self.assertEqual(result.error_code, ERROR_CODEX_AUTH_UNAVAILABLE)

    def test_probe_inconclusive_is_unavailable(self):
        request = ImageRequest.from_dict({"operation": "probe"})
        run = fake_run(agent_text="I am not sure what you mean.")
        with mock.patch.object(adapter, "run_codex", return_value=run):
            result = CodexImageAdapter(request).run()
        self.assertEqual(result.status, STATUS_UNAVAILABLE)
        self.assertEqual(result.error_code, ERROR_BACKEND_UNAVAILABLE)


# ---------------------------------------------------------------------------
# End-to-end via a local stub codex (still no real quota consumed)
# ---------------------------------------------------------------------------
class StubCodexEndToEndTests(TempWorkspaceMixin, unittest.TestCase):
    """Exercises the real run_codex() subprocess path against a fake codex."""

    def _write_stub(self, thread_id: str, artifact_rel: str) -> Path:
        artifact = self.images_root / thread_id / artifact_rel
        make_png(artifact, width=1536, height=864)
        stub = Path(self._tmp.name) / "codex"
        script = textwrap.dedent(
            f"""\
            #!/usr/bin/env python3
            import sys, json
            _ = sys.stdin.read()  # consume the prompt
            print(json.dumps({{"type": "thread.started", "thread_id": "{thread_id}"}}))
            print(json.dumps({{"type": "turn.started"}}))
            msg = "done. ARTIFACT_PATH: {artifact}"
            print(json.dumps({{"type": "item.completed",
                               "item": {{"id": "i0", "type": "agent_message", "text": msg}}}}))
            print(json.dumps({{"type": "turn.completed", "usage": {{}}}}))
            """
        )
        stub.write_text(script, encoding="utf-8")
        stub.chmod(0o755)
        return stub

    def test_full_pipeline_with_stub_codex(self):
        stub = self._write_stub("01a05213-stub", "exec-stub.png")
        request = self.make_request(command=[sys.executable, str(stub)])
        result = CodexImageAdapter(request).run()
        self.assertEqual(result.status, STATUS_COMPLETED, result.error_message)
        self.assertEqual(result.diagnostics["thread_id"], "01a05213-stub")
        placed = self.workspace / "origin_image" / "slide_03.png"
        self.assertTrue(placed.is_file())
        self.assertIsNotNone(sniff_image(placed))

    def test_stub_pipeline_never_uses_api_key(self):
        stub = self._write_stub("01a05213-stub2", "exec-stub2.png")
        request = self.make_request(
            command=[sys.executable, str(stub)],
            env={"OPENAI_API_KEY": "sk-should-be-stripped", "PATH": os.environ.get("PATH", "")},
        )
        inst = CodexImageAdapter(request)
        self.assertNotIn("OPENAI_API_KEY", inst.env)
        result = inst.run()
        self.assertEqual(result.status, STATUS_COMPLETED, result.error_message)
        self.assertFalse(result.diagnostics["api_fallback_used"])


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------
class CliEntryPointTests(TempWorkspaceMixin, unittest.TestCase):
    def test_invalid_request_json_returns_exit_2(self):
        req_file = Path(self._tmp.name) / "bad.json"
        req_file.write_text("{ not json", encoding="utf-8")
        out_file = Path(self._tmp.name) / "out.json"
        rc = adapter.main(["--input", str(req_file), "--output", str(out_file)])
        self.assertEqual(rc, 2)
        payload = json.loads(out_file.read_text(encoding="utf-8"))
        self.assertEqual(payload["error_code"], ERROR_INVALID_REQUEST)

    def test_probe_via_cli(self):
        req_file = Path(self._tmp.name) / "probe.json"
        req_file.write_text(json.dumps({"operation": "probe"}), encoding="utf-8")
        out_file = Path(self._tmp.name) / "out.json"
        run = fake_run(agent_text="IMAGE_BACKEND_AVAILABLE")
        with mock.patch.object(adapter, "run_codex", return_value=run):
            rc = adapter.main(["--input", str(req_file), "--output", str(out_file)])
        self.assertEqual(rc, 0)
        payload = json.loads(out_file.read_text(encoding="utf-8"))
        self.assertEqual(payload["status"], STATUS_AVAILABLE)


if __name__ == "__main__":
    unittest.main(verbosity=2)
