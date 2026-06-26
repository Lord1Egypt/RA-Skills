"""
Embedding 提供程序抽象层

支持：
- Ollama（本地）
- OpenAI（远程 API）
- MCP（通过 MCP 服务器调用远程 embedding 服务）
"""

import abc
import asyncio
import json
from typing import Any, Dict, List, Optional

import httpx
import numpy as np


class EmbeddingProvider(abc.ABC):
    """Embedding 提供者抽象基类"""

    @abc.abstractmethod
    def embed(self, texts: List[str]) -> List[List[float]]:
        """对一批文本进行 embedding，返回向量列表"""
        raise NotImplementedError

    def embed_query(self, text: str) -> List[float]:
        """对单个查询文本进行 embedding"""
        return self.embed([text])[0]

    @property
    @abc.abstractmethod
    def dimension(self) -> int:
        """向量维度"""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """提供者标识名，如 ollama:nomic-embed-text"""
        raise NotImplementedError


class OllamaEmbeddingProvider(EmbeddingProvider):
    """通过 Ollama HTTP API 获取 embedding"""

    def __init__(self, model: str, base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self._dimension: Optional[int] = None

    def embed(self, texts: List[str]) -> List[List[float]]:
        embeddings: List[List[float]] = []
        with httpx.Client(timeout=120.0) as client:
            # 先尝试批量 API /api/embed（Ollama 0.1.33+）
            try:
                resp = client.post(
                    f"{self.base_url}/api/embed",
                    json={"model": self.model, "input": texts},
                )
                if resp.status_code == 200:
                    data = resp.json()
                    embeddings = data.get("embeddings", [])
                    if embeddings:
                        self._dimension = len(embeddings[0])
                        return embeddings
            except Exception:
                pass

            # 回退：逐个调用 /api/embeddings
            for text in texts:
                resp = client.post(
                    f"{self.base_url}/api/embeddings",
                    json={"model": self.model, "prompt": text},
                )
                resp.raise_for_status()
                data = resp.json()
                vec = data.get("embedding")
                if vec is None:
                    raise RuntimeError(f"Ollama returned no embedding for text: {text[:50]}")
                embeddings.append(vec)
                self._dimension = len(vec)
        return embeddings

    @property
    def dimension(self) -> int:
        if self._dimension is None:
            self._dimension = len(self.embed_query("test"))
        return self._dimension

    @property
    def name(self) -> str:
        return f"ollama:{self.model}"


class OpenAIEmbeddingProvider(EmbeddingProvider):
    """通过 OpenAI API 获取 embedding"""

    def __init__(self, model: str, api_key: str, base_url: Optional[str] = None):
        try:
            import openai
        except ImportError as exc:
            raise ImportError("openai package is required for OpenAI embedding provider") from exc

        self.model = model
        self.client = openai.OpenAI(api_key=api_key, base_url=base_url)
        self._dimension: Optional[int] = None

    def embed(self, texts: List[str]) -> List[List[float]]:
        embeddings: List[List[float]] = []
        batch_size = 32
        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            resp = self.client.embeddings.create(model=self.model, input=batch)
            batch_embeddings = [item.embedding for item in resp.data]
            embeddings.extend(batch_embeddings)
            if batch_embeddings:
                self._dimension = len(batch_embeddings[0])
        return embeddings

    @property
    def dimension(self) -> int:
        if self._dimension is None:
            self._dimension = len(self.embed_query("test"))
        return self._dimension

    @property
    def name(self) -> str:
        return f"openai:{self.model}"


class McpEmbeddingProvider(EmbeddingProvider):
    """通过 MCP 服务器获取 embedding"""

    def __init__(
        self,
        model: str,
        transport: str,
        command: Optional[str] = None,
        args: Optional[List[str]] = None,
        env: Optional[Dict[str, str]] = None,
        url: Optional[str] = None,
        tool_name: Optional[str] = None,
    ):
        self.model = model
        self.transport = transport
        self.command = command
        self.args = args or []
        self.env = env or {}
        self.url = url
        self.tool_name = tool_name
        self._dimension: Optional[int] = None
        self._resolved_tool_name: Optional[str] = None

    async def _embed_async(self, texts: List[str]) -> List[List[float]]:
        try:
            from mcp import ClientSession, StdioServerParameters
            from mcp.client.stdio import stdio_client
            from mcp.client.sse import sse_client
        except ImportError as exc:
            raise ImportError("mcp package is required for MCP embedding provider") from exc

        if self.transport == "stdio":
            if not self.command:
                raise ValueError("MCP stdio transport requires 'command' in config")
            params = StdioServerParameters(
                command=self.command,
                args=self.args,
                env=self.env or None,
            )
            client_cm = stdio_client(params)
        elif self.transport == "sse":
            if not self.url:
                raise ValueError("MCP sse transport requires 'url' in config")
            client_cm = sse_client(self.url)
        else:
            raise ValueError(f"Unsupported MCP transport: {self.transport}")

        async with client_cm as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()

                tool_name = self.tool_name
                if tool_name is None:
                    tools_result = await session.list_tools()
                    for tool in tools_result.tools:
                        if "embed" in tool.name.lower():
                            tool_name = tool.name
                            break
                    if tool_name is None:
                        available = [t.name for t in tools_result.tools]
                        raise RuntimeError(
                            f"No embedding tool found in MCP server. Available tools: {available}"
                        )
                    self._resolved_tool_name = tool_name

                arguments: Dict[str, Any] = {"texts": texts}
                if self.model:
                    arguments["model"] = self.model

                result = await session.call_tool(tool_name, arguments)

                # 解析 MCP 返回结果
                if result.content:
                    text_content = result.content[0]
                    data = json.loads(text_content.text)
                else:
                    raise RuntimeError("MCP embedding tool returned empty content")

                embeddings = data.get("embeddings")
                if embeddings is None:
                    # 兼容单条返回
                    single = data.get("embedding")
                    if single is not None:
                        embeddings = [single]
                    else:
                        raise RuntimeError(
                            f"MCP embedding tool returned unexpected format: {data.keys()}"
                        )

                if embeddings:
                    self._dimension = len(embeddings[0])
                return embeddings

    def embed(self, texts: List[str]) -> List[List[float]]:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(self._embed_async(texts))
        else:
            return loop.run_until_complete(self._embed_async(texts))

    @property
    def dimension(self) -> int:
        if self._dimension is None:
            self._dimension = len(self.embed_query("test"))
        return self._dimension

    @property
    def name(self) -> str:
        return f"mcp:{self.model}"


def create_provider(config: Dict[str, Any]) -> Optional[EmbeddingProvider]:
    """根据配置创建对应的 EmbeddingProvider"""
    embedding_cfg = config.get("embedding", {})
    if not embedding_cfg.get("enabled", False):
        return None

    provider_type = embedding_cfg.get("provider", "ollama")
    model = embedding_cfg.get("model", "nomic-embed-text")

    if provider_type == "ollama":
        ollama_cfg = embedding_cfg.get("ollama", {})
        return OllamaEmbeddingProvider(
            model=model,
            base_url=ollama_cfg.get("base_url", "http://localhost:11434"),
        )

    if provider_type == "openai":
        openai_cfg = embedding_cfg.get("openai", {})
        api_key = openai_cfg.get("api_key")
        if not api_key:
            raise ValueError("OpenAI embedding provider requires 'embedding.openai.api_key'")
        return OpenAIEmbeddingProvider(
            model=model,
            api_key=api_key,
            base_url=openai_cfg.get("base_url") or None,
        )

    if provider_type == "mcp":
        mcp_cfg = embedding_cfg.get("mcp", {})
        return McpEmbeddingProvider(
            model=model,
            transport=mcp_cfg.get("transport", "stdio"),
            command=mcp_cfg.get("command"),
            args=mcp_cfg.get("args"),
            env=mcp_cfg.get("env"),
            url=mcp_cfg.get("url"),
            tool_name=mcp_cfg.get("tool_name"),
        )

    raise ValueError(f"Unknown embedding provider: {provider_type}")
