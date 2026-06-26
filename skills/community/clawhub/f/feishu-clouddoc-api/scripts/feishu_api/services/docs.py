from __future__ import annotations

import hashlib
import uuid
from pathlib import Path
from typing import Any

from lark_oapi.api.docx.v1 import (
    BatchDeleteDocumentBlockChildrenRequest,
    BatchDeleteDocumentBlockChildrenRequestBody,
    Block,
    Caption,
    CreateDocumentBlockChildrenRequest,
    CreateDocumentBlockChildrenRequestBody,
    CreateDocumentRequest,
    CreateDocumentRequestBody,
    GetDocumentRequest,
    GetDocumentBlockChildrenRequest,
    Image,
    ListDocumentBlockRequest,
    RawContentDocumentRequest,
    Table,
    TableProperty,
    Text,
    TextElement,
    TextElementStyle,
    TextRun,
    TextStyle,
    UpdateBlockRequest,
    UpdateTextElementsRequest,
    PatchDocumentBlockRequest,
)
from lark_oapi.api.drive.v1 import UploadAllMediaRequest, UploadAllMediaRequestBody
from lark_oapi.core.model.request_option import RequestOption

from ..client import create_client
from ..config import get_settings
from ..models import (
    AppendBlocksResult,
    BlockSummary,
    CreateDocResult,
    DocumentMeta,
    DocumentReadResult,
    TextElementSummary,
    UploadImageResult,
)
from ..errors import FeishuRequestError
from ..token_store import TOKEN_EXPIRED_CODES, needs_preemptive_refresh, refresh_user_access_token
from .base import BaseService


class DocsService(BaseService):
    BLOCK_TYPE_TEXT = 2
    BLOCK_TYPE_HEADING_1 = 3
    BLOCK_TYPE_HEADING_2 = 4
    BLOCK_TYPE_HEADING_3 = 5
    BLOCK_TYPE_BULLET = 12
    BLOCK_TYPE_TODO = 17
    BLOCK_TYPE_IMAGE = 27
    BLOCK_TYPE_TABLE = 31
    BLOCK_TYPE_TABLE_CELL = 32

    TEXT_COLOR_RED = 4

    def __init__(self, client: Any | None = None, *, use_user_token: bool = False) -> None:
        self.settings = get_settings()
        self.use_user_token = use_user_token
        self.client = client or create_client(enable_set_token=use_user_token)
        self.request_option = self._build_request_option() if use_user_token else None

    def _build_request_option(self) -> RequestOption:
        if self.settings.user_refresh_token and (
            not self.settings.user_access_token or needs_preemptive_refresh(self.settings)
        ):
            self._refresh_user_token()
        if not self.settings.user_access_token:
            raise ValueError(
                "Missing FEISHU_USER_ACCESS_TOKEN; user-owner creation requires user token"
            )
        return RequestOption.builder().user_access_token(self.settings.user_access_token).build()

    def _refresh_user_token(self) -> None:
        result = refresh_user_access_token(self.settings)
        get_settings.cache_clear()
        self.settings = get_settings()
        if not self.settings.user_access_token:
            self.settings.user_access_token = result.access_token
        self.request_option = RequestOption.builder().user_access_token(result.access_token).build()

    def _call(self, method: Any, request: Any) -> Any:
        if self.request_option is not None:
            response = method(request, self.request_option)
            code = getattr(response, "code", None)
            if code in TOKEN_EXPIRED_CODES or str(code) in {str(item) for item in TOKEN_EXPIRED_CODES}:
                self._refresh_user_token()
                response = method(request, self.request_option)
            return response
        return method(request)

    def create_document(self, title: str, folder_token: str = "") -> CreateDocResult:
        request = CreateDocumentRequest.builder().request_body(
            CreateDocumentRequestBody.builder()
            .title(title)
            .folder_token(folder_token)
            .build()
        ).build()

        response = self._call(self.client.docx.v1.document.create, request)
        self._raise_for_response(response, "create_document")

        data = response.data
        document = getattr(data, "document", None)
        return CreateDocResult(
            document_id=getattr(document, "document_id", None),
            title=getattr(document, "title", None),
            raw=response.raw,
        )

    def get_document(self, document_id: str) -> DocumentMeta:
        request = GetDocumentRequest.builder().document_id(document_id).build()
        response = self._call(self.client.docx.v1.document.get, request)
        self._raise_for_response(response, "get_document")

        document = response.data.document
        return DocumentMeta(
            document_id=document.document_id,
            title=document.title,
            revision_id=document.revision_id,
            raw=response.raw,
        )

    def get_raw_content(self, document_id: str) -> str | None:
        request = RawContentDocumentRequest.builder().document_id(document_id).build()
        response = self._call(self.client.docx.v1.document.raw_content, request)
        self._raise_for_response(response, "get_raw_content")
        return getattr(response.data, "content", None)

    def list_blocks(self, document_id: str, page_size: int = 200) -> list[BlockSummary]:
        items: list[BlockSummary] = []
        page_token = None

        while True:
            builder = ListDocumentBlockRequest.builder().document_id(document_id).page_size(page_size)
            if page_token:
                builder = builder.page_token(page_token)
            response = self._call(self.client.docx.v1.document_block.list, builder.build())
            self._raise_for_response(response, "list_blocks")

            body = response.data
            for block in body.items or []:
                items.append(self._to_block_summary(block))

            if not getattr(body, "has_more", False):
                break
            page_token = getattr(body, "page_token", None)
            if not page_token:
                break

        return items

    def read_document(self, document_id: str) -> DocumentReadResult:
        return DocumentReadResult(
            meta=self.get_document(document_id),
            raw_content=self.get_raw_content(document_id),
            blocks=self.list_blocks(document_id),
        )

    def find_blocks_by_text(self, document_id: str, query: str, *, exact: bool = True) -> list[BlockSummary]:
        matches: list[BlockSummary] = []
        for block in self.list_blocks(document_id):
            text = (block.text or "").strip()
            if not text:
                continue
            if exact and text == query:
                matches.append(block)
            elif not exact and query in text:
                matches.append(block)
        return matches

    def find_heading_block(self, document_id: str, heading_text: str, *, exact: bool = True) -> BlockSummary:
        heading_types = {self.BLOCK_TYPE_HEADING_1, self.BLOCK_TYPE_HEADING_2, self.BLOCK_TYPE_HEADING_3}
        matches = [
            block for block in self.find_blocks_by_text(document_id, heading_text, exact=exact)
            if block.block_type in heading_types
        ]
        if not matches:
            raise ValueError(f"Heading not found: {heading_text}")
        if len(matches) > 1:
            raise ValueError(f"Multiple headings matched: {heading_text}")
        return matches[0]

    def append_text(self, document_id: str, text: str) -> AppendBlocksResult:
        return self._append_blocks(document_id, document_id, [self.make_text_block(text)])

    def append_heading(self, document_id: str, text: str, level: int = 1) -> AppendBlocksResult:
        return self._append_blocks(document_id, document_id, [self.make_heading_block(text, level=level)])

    def append_rich_text(self, document_id: str, text: str, *, text_color: int | None = None) -> AppendBlocksResult:
        return self._append_blocks(document_id, document_id, [self.make_text_block(text, text_color=text_color)])

    def append_bullet(self, document_id: str, text: str, *, text_color: int | None = None) -> AppendBlocksResult:
        return self._append_blocks(document_id, document_id, [self.make_bullet_block(text, text_color=text_color)])

    def append_todo(self, document_id: str, text: str, *, checked: bool = False, text_color: int | None = None) -> AppendBlocksResult:
        return self._append_blocks(document_id, document_id, [self.make_todo_block(text, checked=checked, text_color=text_color)])

    def append_table(self, document_id: str, rows: list[list[str]], *, header_row: bool = False) -> AppendBlocksResult:
        return self._append_table(document_id, document_id, rows, header_row=header_row)

    def populate_table(self, document_id: str, table_block_id: str, rows: list[list[str]]) -> None:
        blocks = self.list_blocks(document_id)
        table_block = next((block for block in blocks if block.block_id == table_block_id), None)
        if not table_block or table_block.block_type != self.BLOCK_TYPE_TABLE:
            raise ValueError(f"Table block not found: {table_block_id}")

        cell_ids = list(getattr(getattr(table_block.raw, 'table', None), 'cells', None) or [])
        flat_values = [value for row in rows for value in row]
        if len(cell_ids) != len(flat_values):
            raise ValueError(f"Table cell count mismatch: expected {len(cell_ids)}, got {len(flat_values)}")

        block_map = {block.block_id: block for block in blocks}
        for cell_id, value in zip(cell_ids, flat_values):
            cell_block = block_map.get(cell_id)
            text_block_id = (cell_block.children or [None])[0] if cell_block else None
            if not text_block_id:
                raise ValueError(f"Text block not found for table cell: {cell_id}")
            self.update_block_text(document_id, text_block_id, value)

    def append_image(self, document_id: str, image_token: str, *, width: int, height: int, caption: str = "") -> AppendBlocksResult:
        return self._append_blocks(document_id, document_id, [self.make_image_block(image_token, width=width, height=height, caption=caption)])

    def upload_image(self, path: str | Path, *, file_name: str | None = None) -> UploadImageResult:
        file_path = Path(path)
        size = file_path.stat().st_size
        checksum = hashlib.sha1(file_path.read_bytes()).hexdigest()
        with file_path.open("rb") as f:
            request = UploadAllMediaRequest.builder().request_body(
                UploadAllMediaRequestBody.builder()
                .file_name(file_name or file_path.name)
                .parent_type("docx_image")
                .size(size)
                .checksum(checksum)
                .file(f)
                .build()
            ).build()
            response = self._call(self.client.drive.v1.media.upload_all, request)
        try:
            self._raise_for_response(response, "upload_image")
        except FeishuRequestError as exc:
            if "code=1061004" in str(exc):
                raise FeishuRequestError(
                    "upload_image forbidden | code=1061004 | likely missing Drive/Doc image upload scope for docx_image parent_type"
                ) from exc
            raise
        return UploadImageResult(file_token=response.data.file_token, raw=response.raw)

    def verify_image_upload_support(self, path: str | Path) -> dict[str, Any]:
        try:
            result = self.upload_image(path)
            return {
                "supported": True,
                "file_token": result.file_token,
                "note": "image upload succeeded for docx_image",
            }
        except FeishuRequestError as exc:
            return {
                "supported": False,
                "error": str(exc),
                "likely_missing_scope": "Drive/Doc image upload permission for medias.upload_all with parent_type=docx_image",
            }

    def insert_after_block(self, document_id: str, target_block_id: str, new_block: Block) -> AppendBlocksResult:
        target = next((block for block in self.list_blocks(document_id) if block.block_id == target_block_id), None)
        if not target:
            raise ValueError(f"Target block not found: {target_block_id}")
        parent_id = target.parent_id or document_id
        return self._append_blocks_after(document_id, parent_id, target_block_id, [new_block])

    def insert_text_after_heading(self, document_id: str, heading_text: str, text: str, *, exact: bool = True, text_color: int | None = None) -> AppendBlocksResult:
        heading = self.find_heading_block(document_id, heading_text, exact=exact)
        return self.insert_after_block(document_id, heading.block_id, self.make_text_block(text, text_color=text_color))

    def insert_heading_after_heading(self, document_id: str, heading_text: str, text: str, *, level: int = 1, exact: bool = True) -> AppendBlocksResult:
        heading = self.find_heading_block(document_id, heading_text, exact=exact)
        return self.insert_after_block(document_id, heading.block_id, self.make_heading_block(text, level=level))

    def update_block_text(self, document_id: str, block_id: str, text: str, *, text_color: int | None = None) -> None:
        request = PatchDocumentBlockRequest.builder() \
            .document_id(document_id) \
            .block_id(block_id) \
            .document_revision_id(-1) \
            .client_token(str(uuid.uuid4())) \
            .request_body(
                UpdateBlockRequest.builder()
                .update_text_elements(
                    UpdateTextElementsRequest.builder()
                    .elements(self.make_text_elements(text, text_color=text_color))
                    .build()
                )
                .build()
            ) \
            .build()
        response = self._call(self.client.docx.v1.document_block.patch, request)
        self._raise_for_response(response, "update_block_text")

    def update_text_by_heading(self, document_id: str, heading_text: str, text: str, *, exact: bool = True, text_color: int | None = None) -> None:
        heading = self.find_heading_block(document_id, heading_text, exact=exact)
        blocks = self.list_blocks(document_id)
        siblings = [block for block in blocks if block.parent_id == heading.parent_id]
        sibling_ids = [block.block_id for block in siblings]
        try:
            heading_index = sibling_ids.index(heading.block_id)
        except ValueError as exc:
            raise ValueError(f"Heading sibling scan failed: {heading_text}") from exc

        target = None
        for sibling in siblings[heading_index + 1:]:
            if sibling.block_type in {self.BLOCK_TYPE_HEADING_1, self.BLOCK_TYPE_HEADING_2, self.BLOCK_TYPE_HEADING_3}:
                break
            if sibling.block_type in {self.BLOCK_TYPE_TEXT, self.BLOCK_TYPE_BULLET, self.BLOCK_TYPE_TODO}:
                target = sibling
                break

        if not target:
            raise ValueError(f"No text-like block found under heading: {heading_text}")

        self.update_block_text(document_id, target.block_id, text, text_color=text_color)

    def get_section_range(self, document_id: str, heading_text: str, *, exact: bool = True) -> dict[str, Any]:
        heading = self.find_heading_block(document_id, heading_text, exact=exact)
        blocks = self.list_blocks(document_id)
        siblings = [block for block in blocks if block.parent_id == heading.parent_id]
        sibling_ids = [block.block_id for block in siblings]
        try:
            start_index = sibling_ids.index(heading.block_id)
        except ValueError as exc:
            raise ValueError(f"Heading sibling scan failed: {heading_text}") from exc

        heading_level = self._heading_level_for_block_type(heading.block_type)
        end_index = len(siblings)
        for idx in range(start_index + 1, len(siblings)):
            sibling = siblings[idx]
            sibling_level = self._heading_level_for_block_type(sibling.block_type)
            if sibling_level is not None and sibling_level <= heading_level:
                end_index = idx
                break

        return {
            "heading": heading,
            "parent_id": heading.parent_id,
            "siblings": siblings,
            "start_index": start_index,
            "end_index": end_index,
            "body_blocks": siblings[start_index + 1:end_index],
        }

    def replace_section_by_heading(
        self,
        document_id: str,
        heading_text: str,
        blocks: list[Block],
        *,
        exact: bool = True,
        clear_existing: bool = True,
    ) -> AppendBlocksResult:
        info = self.get_section_range(document_id, heading_text, exact=exact)
        parent_id = info["parent_id"] or document_id
        start_index = info["start_index"]
        end_index = info["end_index"]
        if clear_existing and end_index > start_index + 1:
            self._delete_child_range(document_id, parent_id, start_index + 1, end_index - 1)
        return self._append_blocks(document_id, parent_id, blocks, index=start_index + 1)

    def replace_section_text_by_heading(self, document_id: str, heading_text: str, paragraphs: list[str], *, exact: bool = True) -> AppendBlocksResult:
        blocks = [self.make_text_block(text) for text in paragraphs]
        return self.replace_section_by_heading(document_id, heading_text, blocks, exact=exact)

    def replace_section_mixed_by_heading(self, document_id: str, heading_text: str, items: list[dict[str, Any]], *, exact: bool = True) -> AppendBlocksResult:
        blocks: list[Block] = []
        for item in items:
            item_type = item.get("type", "text")
            text = item.get("text", "")
            if item_type == "text":
                blocks.append(self.make_text_block(text, text_color=item.get("text_color")))
            elif item_type == "bullet":
                blocks.append(self.make_bullet_block(text, text_color=item.get("text_color")))
            elif item_type == "todo":
                blocks.append(self.make_todo_block(text, checked=bool(item.get("checked", False)), text_color=item.get("text_color")))
            elif item_type == "heading":
                blocks.append(self.make_heading_block(text, level=int(item.get("level", 1))))
            else:
                raise ValueError(f"Unsupported mixed block item type: {item_type}")
        return self.replace_section_by_heading(document_id, heading_text, blocks, exact=exact)

    def verify_red_text_support(self) -> dict[str, Any]:
        return {
            "supported": True,
            "method": "TextElementStyle.text_color via docx block create/patch",
            "sdk_signal": "lark_oapi.api.docx.v1.TextElementStyle has text_color:int",
            "recommended_color_value": self.TEXT_COLOR_RED,
            "note": "已通过真实文档回读验证红字 block 的 text_color = 4。",
        }

    def make_text_elements(self, text: str, *, text_color: int | None = None) -> list[TextElement]:
        style_builder = TextElementStyle.builder()
        if text_color is not None:
            style_builder = style_builder.text_color(text_color)
        text_run = TextRun.builder().content(text)
        style = style_builder.build()
        if text_color is not None:
            text_run = text_run.text_element_style(style)
        return [TextElement.builder().text_run(text_run.build()).build()]

    def make_text_block(self, text: str, *, text_color: int | None = None) -> Block:
        return Block.builder().block_type(self.BLOCK_TYPE_TEXT).text(
            Text.builder().elements(self.make_text_elements(text, text_color=text_color)).build()
        ).build()

    def make_bullet_block(self, text: str, *, text_color: int | None = None) -> Block:
        return Block.builder().block_type(self.BLOCK_TYPE_BULLET).bullet(
            Text.builder().elements(self.make_text_elements(text, text_color=text_color)).build()
        ).build()

    def make_todo_block(self, text: str, *, checked: bool = False, text_color: int | None = None) -> Block:
        return Block.builder().block_type(self.BLOCK_TYPE_TODO).todo(
            Text.builder()
            .style(TextStyle.builder().done(checked).build())
            .elements(self.make_text_elements(text, text_color=text_color))
            .build()
        ).build()

    def make_image_block(self, image_token: str, *, width: int, height: int, caption: str = "") -> Block:
        image_builder = Image.builder().token(image_token).width(width).height(height)
        if caption:
            image_builder = image_builder.caption(Caption.builder().content(caption).build())
        return Block.builder().block_type(self.BLOCK_TYPE_IMAGE).image(image_builder.build()).build()

    def make_heading_block(self, text: str, level: int = 1) -> Block:
        level_map = {
            1: (self.BLOCK_TYPE_HEADING_1, "heading1"),
            2: (self.BLOCK_TYPE_HEADING_2, "heading2"),
            3: (self.BLOCK_TYPE_HEADING_3, "heading3"),
        }
        block_type, field_name = level_map.get(level, (self.BLOCK_TYPE_HEADING_1, "heading1"))
        text_data = Text.builder().elements(self.make_text_elements(text)).build()
        builder = Block.builder().block_type(block_type)
        getattr(builder, field_name)(text_data)
        return builder.build()

    def _append_blocks(self, document_id: str, parent_block_id: str, blocks: list[Block], *, index: int | None = None) -> AppendBlocksResult:
        body_builder = CreateDocumentBlockChildrenRequestBody.builder().children(blocks)
        if index is not None:
            body_builder = body_builder.index(index)
        request = CreateDocumentBlockChildrenRequest.builder() \
            .document_id(document_id) \
            .block_id(parent_block_id) \
            .document_revision_id(-1) \
            .client_token(str(uuid.uuid4())) \
            .request_body(body_builder.build()) \
            .build()
        response = self._call(self.client.docx.v1.document_block.children.create, request)
        self._raise_for_response(response, "append_blocks")
        children = getattr(response.data, "children", None) or []
        block_ids = [getattr(block, "block_id", None) for block in children if getattr(block, "block_id", None)]
        return AppendBlocksResult(document_id=document_id, parent_block_id=parent_block_id, block_ids=block_ids, raw=response.raw)

    def _append_table(self, document_id: str, parent_block_id: str, rows: list[list[str]], *, header_row: bool = False) -> AppendBlocksResult:
        if not rows or not rows[0]:
            raise ValueError("rows must be a non-empty 2D array")
        row_size = len(rows)
        column_size = len(rows[0])
        if any(len(row) != column_size for row in rows):
            raise ValueError("all rows must have the same column size")

        table_block = Block.builder().block_type(self.BLOCK_TYPE_TABLE).table(
            Table.builder().property(
                TableProperty.builder().row_size(row_size).column_size(column_size).header_row(header_row).build()
            ).build()
        ).build()

        result = self._append_blocks(document_id, parent_block_id, [table_block])
        if result.block_ids:
            self.populate_table(document_id, result.block_ids[0], rows)
        return result

    def _append_blocks_after(self, document_id: str, parent_block_id: str, after_block_id: str, blocks: list[Block]) -> AppendBlocksResult:
        request = GetDocumentBlockChildrenRequest.builder() \
            .document_id(document_id) \
            .block_id(parent_block_id) \
            .document_revision_id(-1) \
            .page_size(500) \
            .build()
        response = self._call(self.client.docx.v1.document_block.children.get, request)
        self._raise_for_response(response, "get_block_children")
        children = getattr(response.data, "items", None) or []
        child_ids = [getattr(block, "block_id", None) for block in children]
        try:
            target_index = child_ids.index(after_block_id)
        except ValueError as exc:
            raise ValueError(f"Failed to locate target among direct children: {after_block_id}") from exc
        return self._append_blocks(document_id, parent_block_id, blocks, index=target_index + 1)

    def _delete_child_range(self, document_id: str, parent_block_id: str, start_index: int, end_index: int) -> None:
        request = BatchDeleteDocumentBlockChildrenRequest.builder() \
            .document_id(document_id) \
            .block_id(parent_block_id) \
            .document_revision_id(-1) \
            .client_token(str(uuid.uuid4())) \
            .request_body(
                BatchDeleteDocumentBlockChildrenRequestBody.builder()
                .start_index(start_index)
                .end_index(end_index + 1)
                .build()
            ) \
            .build()
        response = self._call(self.client.docx.v1.document_block.children.batch_delete, request)
        self._raise_for_response(response, "delete_child_range")

    def _heading_level_for_block_type(self, block_type: int) -> int | None:
        return {
            self.BLOCK_TYPE_HEADING_1: 1,
            self.BLOCK_TYPE_HEADING_2: 2,
            self.BLOCK_TYPE_HEADING_3: 3,
        }.get(block_type)

    def _to_block_summary(self, block: Any) -> BlockSummary:
        return BlockSummary(
            block_id=getattr(block, "block_id", ""),
            parent_id=getattr(block, "parent_id", None),
            block_type=getattr(block, "block_type", 0),
            text=self._extract_block_text(block),
            children=list(getattr(block, "children", None) or []),
            elements=self._extract_block_elements(block),
            raw=block,
        )

    def _extract_block_elements(self, block: Any) -> list[TextElementSummary] | None:
        text_fields = [
            "page", "text", "heading1", "heading2", "heading3", "heading4", "heading5", "heading6", "heading7", "heading8", "heading9",
            "bullet", "ordered", "code", "quote", "equation", "todo",
        ]
        for field in text_fields:
            data = getattr(block, field, None)
            if not data:
                continue
            elements = getattr(data, "elements", None) or []
            summaries: list[TextElementSummary] = []
            for element in elements:
                text_run = getattr(element, "text_run", None)
                style = getattr(text_run, "text_element_style", None) if text_run else None
                summaries.append(
                    TextElementSummary(
                        content=getattr(text_run, "content", None) if text_run else None,
                        text_color=getattr(style, "text_color", None) if style else None,
                        background_color=getattr(style, "background_color", None) if style else None,
                        bold=getattr(style, "bold", None) if style else None,
                        italic=getattr(style, "italic", None) if style else None,
                        underline=getattr(style, "underline", None) if style else None,
                        strikethrough=getattr(style, "strikethrough", None) if style else None,
                        inline_code=getattr(style, "inline_code", None) if style else None,
                        raw=element,
                    )
                )
            return summaries
        return None

    def _extract_block_text(self, block: Any) -> str | None:
        text_fields = [
            "page", "text", "heading1", "heading2", "heading3", "heading4", "heading5", "heading6", "heading7", "heading8", "heading9",
            "bullet", "ordered", "code", "quote", "equation", "todo",
        ]
        for field in text_fields:
            data = getattr(block, field, None)
            if not data:
                continue
            elements = getattr(data, "elements", None) or []
            parts: list[str] = []
            for element in elements:
                text_run = getattr(element, "text_run", None)
                content = getattr(text_run, "content", None) if text_run else None
                if content:
                    parts.append(content)
            if parts:
                return "".join(parts)
        return None
