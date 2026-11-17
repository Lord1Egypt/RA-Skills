#!/usr/bin/env python3
"""Phase 18 clean-plate wrapper around the frozen Codex image adapter.

The Phase 12 adapter remains unchanged.  This additive layer validates and
propagates the Phase 18 reserved-zone contract, then records durable evidence
needed to distinguish a live Codex run from a proxy qualification.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from codex_image_adapter import (
    ERROR_INVALID_REQUEST,
    OP_GENERATE,
    STATUS_COMPLETED,
    STATUS_ERROR,
    AdapterResult,
    CodexImageAdapter,
    ImageRequest,
    InvalidRequestError,
)
from phase18_worker_contract import (
    ReservedZonePromptCompliance,
    WorkerContractCompleteness,
    audit_worker_contract,
    classify_qualification_evidence,
    classify_reserved_zone_prompt,
    render_reserved_zone_contract,
)


@dataclass(frozen=True)
class Phase18WorkerRequest:
    image_request: ImageRequest
    visual_plate_job: Mapping[str, Any]
    dispatch_id: str
    job_id: str

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Phase18WorkerRequest":
        if not isinstance(data, Mapping):
            raise InvalidRequestError("Phase 18 worker request must be an object")
        manifest = data.get("visual_plate_job")
        audit = audit_worker_contract(manifest if isinstance(manifest, Mapping) else None)
        if audit.status is not WorkerContractCompleteness.COMPLETE:
            raise InvalidRequestError(
                "visual_plate_job is not dispatch-safe: " + ", ".join(audit.findings)
            )
        slide_id = str(data.get("slide_id") or "").strip()
        if slide_id and manifest.get("slide_id") != slide_id:
            raise InvalidRequestError("visual_plate_job slide_id does not match request slide_id")
        dispatch_id = str(data.get("dispatch_id") or "").strip()
        job_id = str(data.get("job_id") or "").strip()
        prepared = dict(data)
        prepared.pop("visual_plate_job", None)
        prepared.pop("dispatch_id", None)
        prepared.pop("job_id", None)
        prompt = str(prepared.get("prompt") or "").strip()
        if classify_reserved_zone_prompt(prompt, manifest) is not ReservedZonePromptCompliance.CLEARLY_PROPAGATED:
            prepared["prompt"] = prompt + "\n\n" + render_reserved_zone_contract(manifest)
        image_request = ImageRequest.from_dict(prepared)
        return cls(image_request, dict(manifest), dispatch_id, job_id)

    @classmethod
    def from_prepared_job(
        cls,
        job: Mapping[str, Any],
        *,
        workspace_root: str,
        dispatch_id: str,
        operation: str = OP_GENERATE,
    ) -> "Phase18WorkerRequest":
        if not isinstance(job, Mapping):
            raise InvalidRequestError("prepared slide job must be an object")
        try:
            slide_number = int(job["slide"])
        except (KeyError, TypeError, ValueError) as exc:
            raise InvalidRequestError("prepared slide job requires a numeric slide") from exc
        if slide_number < 1:
            raise InvalidRequestError("prepared slide job slide must be positive")
        prompt = str(job.get("prompt") or "").strip()
        out_name = str(job.get("out") or "").strip()
        if not prompt or not out_name:
            raise InvalidRequestError("prepared slide job requires prompt and out")
        payload = json.dumps(job, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
        request = {
            "operation": operation,
            "slide_id": f"slide_{slide_number:02d}",
            "prompt": prompt,
            "output_path": f"origin_image/{Path(out_name).name}",
            "aspect_ratio": "16:9",
            "workspace_root": workspace_root,
            "dispatch_id": dispatch_id,
            "job_id": "slide-job:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()[:20],
            "visual_plate_job": job.get("visual_plate_job"),
        }
        return cls.from_dict(request)


class Phase18CodexWorker:
    """Execute one validated clean-plate job through the frozen adapter."""

    def __init__(self, request: Phase18WorkerRequest) -> None:
        self.request = request

    def run(self) -> AdapterResult:
        result = CodexImageAdapter(self.request.image_request).run()
        diagnostics = result.diagnostics
        audit = audit_worker_contract(self.request.visual_plate_job)
        diagnostics.update({
            "worker_kind": "live_codex",
            "dispatch_id": self.request.dispatch_id,
            "job_id": self.request.job_id,
            "reserved_zone_manifest_sha256": audit.manifest_hash,
            "worker_contract": {
                "completeness": audit.status.value,
                "manifest_sha256": audit.manifest_hash,
                "prompt_compliance": classify_reserved_zone_prompt(
                    self.request.image_request.prompt, self.request.visual_plate_job
                ).value,
            },
        })
        if result.status == STATUS_COMPLETED:
            root = Path(self.request.image_request.workspace_root).resolve()
            output = (root / result.output_path).resolve()
            if output.is_file():
                artifact_hash = hashlib.sha256(output.read_bytes()).hexdigest()
                diagnostics["plate_artifact_sha256"] = artifact_hash
                diagnostics["output_artifact_sha256"] = artifact_hash
            thread_id = str(diagnostics.get("thread_id") or "")
            if thread_id and diagnostics.get("plate_artifact_sha256"):
                identity = "|".join((
                    self.request.dispatch_id,
                    self.request.job_id,
                    thread_id,
                    str(diagnostics["plate_artifact_sha256"]),
                ))
                diagnostics["worker_result_id"] = "codex-result:" + hashlib.sha256(
                    identity.encode("utf-8")
                ).hexdigest()[:20]
            evidence = result.to_dict()
            diagnostics["qualification_evidence"] = classify_qualification_evidence(evidence).value
        return result


def _load_request(path: str | None) -> dict[str, Any]:
    raw = Path(path).read_text(encoding="utf-8") if path and path != "-" else sys.stdin.read()
    if not raw.strip():
        raise InvalidRequestError("empty request")
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise InvalidRequestError(f"request is not valid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise InvalidRequestError("request must be a JSON object")
    return value


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run one Phase 18 clean-plate Codex worker job")
    parser.add_argument("--input", default="-", help="Request JSON path, or - for stdin")
    parser.add_argument("--output", help="Optional result JSON path")
    args = parser.parse_args(argv)
    try:
        request = Phase18WorkerRequest.from_dict(_load_request(args.input))
        result = Phase18CodexWorker(request).run()
    except InvalidRequestError as exc:
        result = AdapterResult(
            status=STATUS_ERROR,
            error_code=ERROR_INVALID_REQUEST,
            error_message=str(exc),
        )
    payload = json.dumps(result.to_dict(), ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    else:
        sys.stdout.write(payload)
    return 0 if result.status == STATUS_COMPLETED else 1


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["Phase18CodexWorker", "Phase18WorkerRequest"]
