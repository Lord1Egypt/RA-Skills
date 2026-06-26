import logging
import asyncio
import traceback
import subprocess
import shutil
import os
import urllib.request
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession
from contextlib import AsyncExitStack, suppress
import mcp.types as types
import sys

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout,
    force=True
)

# MCP 服务地址
MCP_PORT = 18009
MCP_URL = f"http://localhost:{MCP_PORT}/sse"
MCP_CMD = "x5use-linux-mcp"
LOG_DIR = "/usr/local/qb_logs"
LOG_FILE = os.path.join(LOG_DIR, "mcp_log.log")


def _is_mcp_service_running() -> bool:
    """Check if the MCP service is already running."""
    try:
        req = urllib.request.Request(f"http://localhost:{MCP_PORT}/sse", method="GET")
        urllib.request.urlopen(req, timeout=2)
        return True
    except Exception:
        return False


def ensure_mcp_service_running():
    """Ensure the x5use-linux-mcp service is running. Start it if not."""
    if _is_mcp_service_running():
        logging.info("X5 MCP service is already running.")
        return

    # Check if the command exists
    if shutil.which(MCP_CMD) is None:
        raise RuntimeError(
            f"ERROR: '{MCP_CMD}' command not found. "
            f"Please ensure it is installed and available in PATH."
        )

    # Create log directory
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
    except OSError as e:
        raise RuntimeError(
            f"ERROR: Failed to create log directory {LOG_DIR}: {e}"
        )

    # Start the MCP service in background
    logging.info(f"Starting X5 MCP service on port {MCP_PORT}...")
    with open(LOG_FILE, "a") as log_f:
        proc = subprocess.Popen(
            [MCP_CMD, "--transport", "sse", "--port", str(MCP_PORT), "--log-dir", LOG_DIR],
            stdout=log_f,
            stderr=subprocess.STDOUT,
        )

    # Wait and verify the process is still alive
    import time
    time.sleep(2)
    if proc.poll() is not None:
        raise RuntimeError(
            f"ERROR: {MCP_CMD} failed to start (exit code {proc.returncode}). "
            f"Check logs at {LOG_FILE}"
        )

    logging.info(f"X5 MCP service started successfully (PID: {proc.pid}).")


class MCPClient:
    """MCP 客户端封装，负责连接初始化、工具调用和资源清理"""

    def __init__(self, url: str = MCP_URL):
        self.url = url
        self.session = None
        self.exit_stack = None

    async def initialize(self) -> ClientSession:
        """初始化 SSE 连接并创建会话"""
        # Ensure MCP service is running before connecting
        ensure_mcp_service_running()

        try:
            client = sse_client(
                url=self.url,
                headers={},
                timeout=30,
                sse_read_timeout=10 * 60
            )
            self.exit_stack = AsyncExitStack()
            sse_transport = await self.exit_stack.enter_async_context(client)
            read, write = sse_transport
            session = await self.exit_stack.enter_async_context(ClientSession(read, write))
            await session.initialize()
            self.session = session
            logging.info("MCP 会话初始化成功")
            return session
        except Exception as e:
            logging.error(f"初始化 MCP 客户端失败: {e}")
            if self.exit_stack:
                await self.exit_stack.aclose()
            raise

    async def call_tool(self, name: str, args: dict) -> types.CallToolResult:
        """调用 MCP 工具"""
        if self.session is None:
            raise RuntimeError("客户端未初始化，请先调用 initialize()")

        try:
            result: types.CallToolResult = await asyncio.wait_for(
                self.session.call_tool(name, args),
                timeout=60
            )
            logging.info(f"工具 [{name}] 调用成功")
            return result
        except asyncio.TimeoutError:
            logging.error(f"工具 [{name}] 调用超时")
            raise
        except Exception as e:
            logging.error(f"工具 [{name}] 调用失败: {e}")
            traceback.print_exc()
            raise

    async def close(self):
        """关闭客户端并清理资源"""
        try:
            self.session = None
            exit_stack = self.exit_stack
            self.exit_stack = None
            if exit_stack:
                with suppress(RuntimeError):
                    try:
                        await exit_stack.aclose()
                    except Exception as e:
                        if "Attempted to exit cancel scope in a different task" not in str(e):
                            logging.error(f"清理资源时出错: {e}")
                            traceback.print_exc()
        except Exception as e:
            logging.error(f"关闭客户端时出错: {e}")
            traceback.print_exc()
