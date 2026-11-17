from __future__ import annotations

from .base import BuilderAdapter
from .custom_adapter import CustomAdapter
from .html_svg_adapter import HtmlSvgAdapter
from .officecli_adapter import OfficeCliAdapter
from .pptxgenjs_adapter import PptxGenJsAdapter
from .python_pptx_adapter import PythonPptxAdapter

_REGISTRY: dict[str, BuilderAdapter] = {}


def register_builder(adapter_id: str, adapter: BuilderAdapter) -> None:
    _REGISTRY[adapter_id] = adapter


def get_builder(adapter_id: str) -> BuilderAdapter | None:
    return _REGISTRY.get(adapter_id)


def list_builders() -> dict[str, BuilderAdapter]:
    return dict(_REGISTRY)


def _register_defaults() -> None:
    for adapter in [
        OfficeCliAdapter(),
        PptxGenJsAdapter(),
        PythonPptxAdapter(),
        HtmlSvgAdapter(),
        CustomAdapter(),
    ]:
        register_builder(adapter.name, adapter)


_register_defaults()
