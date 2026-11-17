"""Deterministic fake rasterizer for Phase 15.2 contract tests."""

from __future__ import annotations

import hashlib

from pdf_ocr import (
    PDFOCRError,
    PDFOCRErrorCode,
    PDFRasterizer,
    RasterProvenance,
    RasterRequest,
    RasterResult,
)


class FakePDFRasterizer(PDFRasterizer):
    renderer_id = "fake-pdf-rasterizer"
    renderer_version = "1.0.0"
    renderer_engine_version = "fake-engine-1.0.0"
    approved_build_identity = "fake-build-contract-v1"

    def __init__(
        self,
        *,
        width: int = 1200,
        height: int = 1600,
        fail_code: PDFOCRErrorCode | str | None = None,
    ) -> None:
        self.width = width
        self.height = height
        self.fail_code = PDFOCRErrorCode(fail_code) if fail_code is not None else None
        self._calls: list[RasterRequest] = []

    @property
    def calls(self) -> tuple[RasterRequest, ...]:
        return tuple(self._calls)

    def rasterize(self, request: RasterRequest) -> RasterResult:
        self._calls.append(request)
        if self.fail_code is not None:
            raise PDFOCRError("injected deterministic raster failure", self.fail_code)

        config = request.configuration
        seed = "|".join(
            (
                request.source.source_id,
                request.source.source_digest,
                str(request.page.page),
                str(request.page.total_pages),
                config.to_json(),
                str(self.width),
                str(self.height),
            )
        ).encode("utf-8")
        raster_bytes = b"FAKE-PNG\x00" + hashlib.sha256(seed).digest()
        provenance = RasterProvenance(
            renderer_id=self.renderer_id,
            renderer_version=self.renderer_version,
            renderer_engine_version=self.renderer_engine_version,
            approved_build_identity=self.approved_build_identity,
            dpi=config.dpi,
            output_format=config.output_format,
            colorspace=config.colorspace,
            alpha=config.alpha,
            rotation_policy=config.rotation_policy,
            effective_rotation=0,
            box_policy=config.box_policy,
            selected_box="MediaBox",
            box_coordinates=(0.0, 0.0, 612.0, 792.0),
            render_annotations=config.render_annotations,
            semantic_preprocessing=config.semantic_preprocessing,
            width=self.width,
            height=self.height,
            raster_digest=hashlib.sha256(raster_bytes).hexdigest(),
        )
        return RasterResult(raster_bytes=raster_bytes, provenance=provenance)
