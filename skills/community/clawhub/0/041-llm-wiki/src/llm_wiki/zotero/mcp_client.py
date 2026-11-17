"""Programmatic client for the configured 54yyyu/zotero-mcp server."""

from __future__ import annotations

import asyncio
import json
import os
import re
from collections.abc import Iterable, Mapping, Sequence
from contextlib import AsyncExitStack
from pathlib import Path
from typing import Any, Self

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

_ITEM_KEY_PATTERN = re.compile(
    "^- " + chr(96) + "([A-Z0-9]{8})" + chr(96), re.MULTILINE
)
_COLLECTION_NAME_PATTERN = re.compile(
    r"^# Items in Collection: (.+?) \(\d+ items\)$", re.MULTILINE
)


class ZoteroMCPError(RuntimeError):
    """Raised when the Zotero MCP server rejects or cannot complete a call."""


class ZoteroMCPClient:
    """Narrow MCP client used by the one-shot enrichment worker."""

    def __init__(
        self,
        config_path: Path,
        *,
        server_name: str = "zotero",
        quiet: bool = True,
    ) -> None:
        self.config_path = Path(config_path)
        self.server_name = server_name
        self.quiet = quiet
        self._stack: AsyncExitStack | None = None
        self._session: ClientSession | None = None

    async def __aenter__(self) -> Self:
        raw_text = await asyncio.to_thread(self.config_path.read_text, encoding="utf-8")
        raw = json.loads(raw_text)
        servers = raw.get("mcpServers", raw)
        server = servers.get(self.server_name)
        if not isinstance(server, Mapping):
            raise ZoteroMCPError(
                f"MCP server {self.server_name!r} is not configured in {self.config_path}"
            )
        command = str(server.get("command") or "").strip()
        if not command:
            raise ZoteroMCPError(f"MCP server {self.server_name!r} has no command")

        env = {**os.environ}
        env.update(
            {str(key): str(value) for key, value in (server.get("env") or {}).items()}
        )
        params = StdioServerParameters(
            command=command,
            args=[str(value) for value in (server.get("args") or [])],
            env=env,
        )

        self._stack = AsyncExitStack()
        await self._stack.__aenter__()
        errlog = None
        if self.quiet:
            errlog = self._stack.enter_context(
                Path(os.devnull).open("w", encoding="utf-8")  # noqa: ASYNC230, SIM115 - managed by AsyncExitStack
            )
        streams = await self._stack.enter_async_context(
            stdio_client(params, errlog=errlog) if errlog else stdio_client(params)
        )
        self._session = await self._stack.enter_async_context(ClientSession(*streams))
        await self._session.initialize()
        return self

    async def __aexit__(self, exc_type: object, exc: object, traceback: object) -> None:
        if self._stack is not None:
            await self._stack.__aexit__(exc_type, exc, traceback)
        self._stack = None
        self._session = None

    async def _call(self, tool_name: str, arguments: Mapping[str, Any]) -> Any:
        if self._session is None:
            raise ZoteroMCPError("Zotero MCP client is not connected")
        result = await self._session.call_tool(tool_name, dict(arguments))
        payload = result.model_dump(exclude_none=True)
        if payload.get("isError"):
            raise ZoteroMCPError(f"{tool_name} failed: {self._result_text(payload)}")
        structured = payload.get("structuredContent")
        if isinstance(structured, Mapping) and "result" in structured:
            return structured["result"]
        return self._result_text(payload)

    @staticmethod
    def _result_text(payload: Mapping[str, Any]) -> str:
        parts: list[str] = []
        for content in payload.get("content") or []:
            if isinstance(content, Mapping) and content.get("type") == "text":
                parts.append(str(content.get("text") or ""))
        return "\n".join(parts)

    async def get_collection_item_keys(
        self,
        collection_key: str,
        *,
        limit: int = 500,
    ) -> tuple[str, list[str]]:
        text = str(
            await self._call(
                "zotero_get_collection_items",
                {
                    "collection_key": collection_key,
                    "detail": "keys_only",
                    "limit": limit,
                },
            )
        )
        name_match = _COLLECTION_NAME_PATTERN.search(text)
        collection_name = name_match.group(1).strip() if name_match else collection_key
        keys = _ITEM_KEY_PATTERN.findall(text)
        return collection_name, keys

    async def get_item_metadata(self, item_key: str) -> dict[str, Any]:
        text = await self._call(
            "zotero_get_item_metadata",
            {
                "item_key": item_key,
                "format": "json",
                "include_abstract": False,
            },
        )
        try:
            payload = json.loads(str(text))
        except json.JSONDecodeError as exc:
            raise ZoteroMCPError(f"Invalid metadata JSON for {item_key}") from exc
        data = payload.get("data")
        if not isinstance(data, dict):
            raise ZoteroMCPError(f"Metadata response for {item_key} has no data object")
        return data

    async def get_items(
        self,
        item_keys: Sequence[str],
        *,
        concurrency: int = 4,
    ) -> list[dict[str, Any]]:
        items, failures = await self.get_items_tolerant(
            item_keys, concurrency=concurrency
        )
        if failures:
            key, message = failures[0]
            raise ZoteroMCPError(f"metadata load failed for {key}: {message}")
        return items

    async def get_items_tolerant(
        self,
        item_keys: Sequence[str],
        *,
        concurrency: int = 4,
    ) -> tuple[list[dict[str, Any]], list[tuple[str, str]]]:
        """逐条容错加载:成功项保持输入顺序,失败项降级为 (key, error) 记录。

        单个失效 key(如 Zotero 条目合并/删除后悬空的旧 key)不再导致
        整个批次崩溃;调用方负责把 failures 降级为待修复记录。
        """
        semaphore = asyncio.Semaphore(max(1, concurrency))

        async def load(item_key: str) -> dict[str, Any]:
            async with semaphore:
                return await self.get_item_metadata(item_key)

        results = await asyncio.gather(
            *(load(key) for key in item_keys), return_exceptions=True
        )
        items: list[dict[str, Any]] = []
        failures: list[tuple[str, str]] = []
        for key, result in zip(item_keys, results):
            if isinstance(result, BaseException):
                failures.append((key, str(result)))
            else:
                items.append(result)
        return items, failures

    async def write_safe_mutation(
        self,
        item_key: str,
        *,
        set_keys: Mapping[str, Any] | None = None,
        add_tags: Iterable[str] = (),
        remove_tags: Iterable[str] = (),
        fields: Mapping[str, Any] | None = None,
    ) -> None:
        normalized_keys = {
            str(key): str(value)
            for key, value in (set_keys or {}).items()
            if value is not None
        }
        add_list = sorted({str(tag) for tag in add_tags if str(tag).strip()})
        remove_list = sorted({str(tag) for tag in remove_tags if str(tag).strip()})
        if normalized_keys or add_list or remove_list:
            arguments: dict[str, Any] = {"item_keys": [item_key]}
            if normalized_keys:
                arguments["set_keys"] = normalized_keys
            if add_list:
                arguments["add_tags"] = add_list
            if remove_list:
                arguments["remove_tags"] = remove_list
            await self._call("zotero_batch_update", arguments)

        if fields:
            await self._call(
                "zotero_update_item",
                {"item_key": item_key, "fields": dict(fields)},
            )
