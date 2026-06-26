from __future__ import annotations

from typing import Any

from lark_oapi.api.sheets.v3 import (
    CreateSpreadsheetRequest,
    Find,
    FindCondition,
    FindSpreadsheetSheetRequest,
    GetSpreadsheetRequest,
    QuerySpreadsheetSheetRequest,
    Replace,
    ReplaceSpreadsheetSheetRequest,
    Spreadsheet,
)

from ..client import create_client
from .base import BaseService


class SheetsService(BaseService):
    def __init__(self, client: Any | None = None) -> None:
        self.client = client or create_client()

    def create_spreadsheet(self, title: str, *, folder_token: str = "") -> dict[str, Any]:
        request = CreateSpreadsheetRequest.builder().request_body(
            Spreadsheet.builder().title(title).folder_token(folder_token).build()
        ).build()
        response = self.client.sheets.v3.spreadsheet.create(request)
        self._raise_for_response(response, "create_spreadsheet")
        sheet = getattr(response.data, "spreadsheet", None)
        return {
            "spreadsheet_token": getattr(sheet, "spreadsheet_token", None),
            "title": getattr(sheet, "title", None),
            "url": getattr(sheet, "url", None),
            "raw": response.raw,
        }

    def get_spreadsheet(self, spreadsheet_token: str) -> dict[str, Any]:
        request = GetSpreadsheetRequest.builder().spreadsheet_token(spreadsheet_token).build()
        response = self.client.sheets.v3.spreadsheet.get(request)
        self._raise_for_response(response, "get_spreadsheet")
        sheet = getattr(response.data, "spreadsheet", None)
        return {
            "spreadsheet_token": getattr(sheet, "spreadsheet_token", None),
            "title": getattr(sheet, "title", None),
            "url": getattr(sheet, "url", None),
            "raw": response.raw,
        }

    def query_sheets(self, spreadsheet_token: str) -> list[dict[str, Any]]:
        request = QuerySpreadsheetSheetRequest.builder().spreadsheet_token(spreadsheet_token).build()
        response = self.client.sheets.v3.spreadsheet_sheet.query(request)
        self._raise_for_response(response, "query_sheets")
        sheets = getattr(response.data, "sheets", None) or []
        return [
            {"sheet_id": getattr(item, "sheet_id", None), "title": getattr(item, "title", None), "index": getattr(item, "index", None), "raw": item}
            for item in sheets
        ]


    def find_in_sheet(self, spreadsheet_token: str, sheet_id: str, text: str, *, cell_range: str = "") -> dict[str, Any]:
        condition = FindCondition.builder().match_case(False)
        if cell_range:
            condition = condition.range(cell_range)
        request = FindSpreadsheetSheetRequest.builder() \
            .spreadsheet_token(spreadsheet_token) \
            .sheet_id(sheet_id) \
            .request_body(
                Find.builder().find(text).find_condition(condition.build()).build()
            ) \
            .build()
        response = self.client.sheets.v3.spreadsheet_sheet.find(request)
        self._raise_for_response(response, "find_in_sheet")
        result = getattr(response.data, "find_result", None)
        return {
            "matched_cells": getattr(result, "matched_cells", None),
            "matched_formula_cells": getattr(result, "matched_formula_cells", None),
            "rows_count": getattr(result, "rows_count", None),
            "raw": response.raw,
        }

    def replace_in_sheet(self, spreadsheet_token: str, sheet_id: str, find_text: str, replacement: str, *, cell_range: str = "") -> dict[str, Any]:
        condition = FindCondition.builder().match_case(False)
        if cell_range:
            condition = condition.range(cell_range)
        request = ReplaceSpreadsheetSheetRequest.builder() \
            .spreadsheet_token(spreadsheet_token) \
            .sheet_id(sheet_id) \
            .request_body(
                Replace.builder()
                .find(find_text)
                .replacement(replacement)
                .find_condition(condition.build())
                .build()
            ) \
            .build()
        response = self.client.sheets.v3.spreadsheet_sheet.replace(request)
        self._raise_for_response(response, "replace_in_sheet")
        result = getattr(response.data, "replace_result", None)
        return {
            "matched_cells": getattr(result, "matched_cells", None),
            "matched_formula_cells": getattr(result, "matched_formula_cells", None),
            "rows_count": getattr(result, "rows_count", None),
            "raw": response.raw,
        }
