from __future__ import annotations

import uuid
from typing import Any

from lark_oapi.api.bitable.v1 import (
    AppTableCreateHeader,
    AppTableField,
    AppTableRecord,
    CreateAppRequest,
    CreateAppTableRequest,
    CreateAppTableRequestBody,
    CreateAppTableRecordRequest,
    GetAppTableRecordRequest,
    ListAppTableFieldRequest,
    ListAppTableRecordRequest,
    ListAppTableRequest,
    ReqApp,
    ReqTable,
    UpdateAppTableFieldRequest,
    UpdateAppTableRecordRequest,
)

from ..client import create_client
from .base import BaseService


class BaseAppService(BaseService):
    FIELD_TYPE_TEXT = 1
    FIELD_TYPE_NUMBER = 2
    FIELD_TYPE_SINGLE_SELECT = 3
    FIELD_TYPE_MULTI_SELECT = 4
    FIELD_TYPE_DATETIME = 5
    FIELD_TYPE_CHECKBOX = 7

    def __init__(self, client: Any | None = None) -> None:
        self.client = client or create_client()

    def create_base(self, name: str, *, folder_token: str = "", time_zone: str = "Asia/Shanghai") -> dict[str, Any]:
        request = CreateAppRequest.builder().request_body(
            ReqApp.builder().name(name).folder_token(folder_token).time_zone(time_zone).build()
        ).build()
        response = self.client.bitable.v1.app.create(request)
        self._raise_for_response(response, "create_base")
        app = getattr(response.data, "app", None)
        return {"app_token": getattr(app, "app_token", None), "name": getattr(app, "name", None), "raw": response.raw}

    def list_tables(self, app_token: str) -> list[dict[str, Any]]:
        request = ListAppTableRequest.builder().app_token(app_token).page_size(200).build()
        response = self.client.bitable.v1.app_table.list(request)
        self._raise_for_response(response, "list_tables")
        items = getattr(response.data, "items", None) or []
        return [
            {"table_id": getattr(item, "table_id", None), "name": getattr(item, "name", None), "raw": item}
            for item in items
        ]

    def create_table(self, app_token: str, name: str, fields: list[dict[str, Any]], *, default_view_name: str = "默认视图") -> dict[str, Any]:
        headers = [
            AppTableCreateHeader.builder()
            .field_name(field["field_name"])
            .type(field["type"])
            .build()
            for field in fields
        ]
        request = CreateAppTableRequest.builder() \
            .app_token(app_token) \
            .request_body(
                CreateAppTableRequestBody.builder()
                .table(
                    ReqTable.builder()
                    .name(name)
                    .default_view_name(default_view_name)
                    .fields(headers)
                    .build()
                )
                .build()
            ) \
            .build()
        response = self.client.bitable.v1.app_table.create(request)
        self._raise_for_response(response, "create_table")
        table = getattr(response.data, "table", None)
        return {"table_id": getattr(table, "table_id", None), "name": getattr(table, "name", None), "raw": response.raw}

    def list_fields(self, app_token: str, table_id: str) -> list[dict[str, Any]]:
        request = ListAppTableFieldRequest.builder() \
            .app_token(app_token) \
            .table_id(table_id) \
            .page_size(200) \
            .build()
        response = self.client.bitable.v1.app_table_field.list(request)
        self._raise_for_response(response, "list_fields")
        items = getattr(response.data, "items", None) or []
        return [
            {
                "field_id": getattr(item, "field_id", None),
                "field_name": getattr(item, "field_name", None),
                "type": getattr(item, "type", None),
                "raw": item,
            }
            for item in items
        ]

    def list_records(self, app_token: str, table_id: str, *, page_size: int = 200) -> list[dict[str, Any]]:
        request = ListAppTableRecordRequest.builder() \
            .app_token(app_token) \
            .table_id(table_id) \
            .page_size(page_size) \
            .build()
        response = self.client.bitable.v1.app_table_record.list(request)
        self._raise_for_response(response, "list_records")
        items = getattr(response.data, "items", None) or []
        return [
            {"record_id": getattr(item, "record_id", None), "fields": getattr(item, "fields", None), "raw": item}
            for item in items
        ]

    def get_record(self, app_token: str, table_id: str, record_id: str) -> dict[str, Any]:
        request = GetAppTableRecordRequest.builder() \
            .app_token(app_token) \
            .table_id(table_id) \
            .record_id(record_id) \
            .build()
        response = self.client.bitable.v1.app_table_record.get(request)
        self._raise_for_response(response, "get_record")
        record = getattr(response.data, "record", None)
        return {"record_id": getattr(record, "record_id", None), "fields": getattr(record, "fields", None), "raw": response.raw}

    def create_record(self, app_token: str, table_id: str, fields: dict[str, Any]) -> dict[str, Any]:
        request = CreateAppTableRecordRequest.builder() \
            .app_token(app_token) \
            .table_id(table_id) \
            .client_token(str(uuid.uuid4())) \
            .request_body(AppTableRecord.builder().fields(fields).build()) \
            .build()
        response = self.client.bitable.v1.app_table_record.create(request)
        self._raise_for_response(response, "create_record")
        record = getattr(response.data, "record", None)
        return {"record_id": getattr(record, "record_id", None), "fields": getattr(record, "fields", None), "raw": response.raw}

    def update_record(self, app_token: str, table_id: str, record_id: str, fields: dict[str, Any]) -> dict[str, Any]:
        request = UpdateAppTableRecordRequest.builder() \
            .app_token(app_token) \
            .table_id(table_id) \
            .record_id(record_id) \
            .request_body(AppTableRecord.builder().fields(fields).build()) \
            .build()
        response = self.client.bitable.v1.app_table_record.update(request)
        self._raise_for_response(response, "update_record")
        record = getattr(response.data, "record", None)
        return {"record_id": getattr(record, "record_id", None), "fields": getattr(record, "fields", None), "raw": response.raw}

    def update_field(self, app_token: str, table_id: str, field_id: str, *, field_name: str, field_type: int | None = None) -> dict[str, Any]:
        builder = AppTableField.builder().field_name(field_name)
        if field_type is not None:
            builder = builder.type(field_type)
        request = UpdateAppTableFieldRequest.builder() \
            .app_token(app_token) \
            .table_id(table_id) \
            .field_id(field_id) \
            .request_body(builder.build()) \
            .build()
        response = self.client.bitable.v1.app_table_field.update(request)
        self._raise_for_response(response, "update_field")
        field = getattr(response.data, "field", None)
        return {"field_id": getattr(field, "field_id", None), "field_name": getattr(field, "field_name", None), "type": getattr(field, "type", None), "raw": response.raw}
