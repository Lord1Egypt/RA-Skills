/**
 * websocket.ts — WebSocket 备选传输通道
 *
 * 提供 WebSocket 作为 SSE + HTTP POST 的备选方案。
 * 适用于不支持 SSE 的客户端环境，或需要更低延迟的场景。
 *
 * 端点：ws://host:port/ws?token=<api_token>
 *
 * WebSocket 客户端接收的事件格式与 SSE 相同（JSON payload），
 * 发送的消息格式为 { type: "message", to: "...", content: "..." }
 *
 * 与 SSE 共存：pushToAgent 优先使用 SSE，WebSocket 作为 fallback。
 */

import type { Server as HttpServer } from "http";
import { WebSocketServer, WebSocket as WsSocket } from "ws";
import { verifyToken } from "./security.js";
import { logger } from "./logger.js";

// ─── WebSocket 客户端连接池 ────────────────────────────────
const wsClients = new Map<string, WsSocket>();

/**
 * 创建 WebSocket 服务器并挂载到 HTTP 服务器
 * @param httpServer 已有的 HTTP 服务器实例
 */
export function createWebSocketServer(httpServer: HttpServer): WebSocketServer {
  const wss = new WebSocketServer({ server: httpServer, path: "/ws" });

  wss.on("connection", (ws, req) => {
    // 从 URL query 提取 token
    const url = new URL(req.url ?? "/", `http://${req.headers.host}`);
    const token = url.searchParams.get("token");

    // 认证
    if (!token) {
      ws.send(JSON.stringify({ event: "auth_error", message: "Missing token parameter" }));
      ws.close(4001, "Missing token");
      return;
    }

    const authContext = verifyToken(token);
    if (!authContext) {
      ws.send(JSON.stringify({ event: "auth_error", message: "Invalid or expired token" }));
      ws.close(4001, "Invalid token");
      return;
    }

    const agentId = authContext.agentId;

    // 关闭已有的同 ID 连接（Agent 重连场景）
    const existing = wsClients.get(agentId);
    if (existing) {
      try {
        existing.close(1000, "Replaced by new connection");
      } catch { /* ignore */ }
    }

    wsClients.set(agentId, ws);
    logger.info("ws_client_connected", { module: "websocket", agent_id: agentId });

    // 发送连接确认
    ws.send(JSON.stringify({ event: "connected", agent_id: agentId, role: authContext.role }));

    // 处理客户端发来的消息
    ws.on("message", (raw) => {
      try {
        const data = JSON.parse(raw.toString());
        logger.info("ws_message_received", { module: "websocket", agent_id: agentId, type: data.type });
        // 消息由 Client SDK 通过 HTTP POST 发送到 /mcp 端点
        // WebSocket 收到的消息可以回显确认
        ws.send(JSON.stringify({ event: "ack", type: data.type }));
      } catch {
        ws.send(JSON.stringify({ event: "error", message: "Invalid JSON" }));
      }
    });

    // 断线处理
    ws.on("close", () => {
      wsClients.delete(agentId);
      logger.info("ws_client_disconnected", { module: "websocket", agent_id: agentId });
    });

    ws.on("error", (err) => {
      logger.error("ws_client_error", { module: "websocket", agent_id: agentId, error: String(err) });
      wsClients.delete(agentId);
    });
  });

  logger.info("ws_server_created", { module: "websocket", path: "/ws" });
  return wss;
}

/**
 * 向 WebSocket 客户端推送事件
 * @returns true=已推送, false=该 Agent 无 WebSocket 连接
 */
export function pushToWebSocket(agentId: string, event: object): boolean {
  const ws = wsClients.get(agentId);
  if (!ws || ws.readyState !== WsSocket.OPEN) {
    return false;
  }
  try {
    ws.send(JSON.stringify(event));
    return true;
  } catch {
    wsClients.delete(agentId);
    return false;
  }
}

/**
 * 检查 Agent 是否有连线的 WebSocket
 */
export function isWebSocketConnected(agentId: string): boolean {
  const ws = wsClients.get(agentId);
  return !!ws && ws.readyState === WsSocket.OPEN;
}

/**
 * 获取 WebSocket 在线 Agent 列表
 */
export function wsOnlineAgents(): string[] {
  const agents: string[] = [];
  for (const [id, ws] of wsClients) {
    if (ws.readyState === WsSocket.OPEN) {
      agents.push(id);
    }
  }
  return agents;
}

/**
 * 优雅关闭所有 WebSocket 连接
 */
export function drainWsClients(): void {
  for (const [agentId, ws] of wsClients) {
    try {
      ws.send(JSON.stringify({ event: "hub_shutdown", message: "Server shutting down" }));
      ws.close(1001, "Server shutdown");
    } catch { /* ignore */ }
  }
  wsClients.clear();
}
