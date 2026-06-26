import crypto from "crypto";
import path from "path";
import os from "os";
import { EventEmitter } from "events";
import { NknClient } from "./client.js";
import { IpfsService } from "./ipfs.js";
import { MediaService } from "./media.js";
import { MessageDb } from "./db.js";
import type {
  BotConfig,
  MessageData,
  MessageOptions,
  MessageContentType,
  IncomingMessage,
  ClientStatus,
  Message,
} from "./types.js";

const DISPLAYABLE_TYPES = new Set<MessageContentType>([
  "text",
  "textExtension",
  "image",
  "audio",
  "file",
]);

/**
 * DchatBot — headless, CLI-friendly P2P bot over NKN.
 *
 * Events:
 *   "message"      — (msg: IncomingMessage) — text, image, audio, or file received
 *   "receipt"       — (from: string, messageId: string) — delivery receipt
 *   "readReceipt"   — (from: string, messageIds: string[]) — read receipt
 *   "connected"     — (status: ClientStatus) — NKN client connected
 *   "disconnected"  — () — NKN client disconnected
 */
export class DchatBot extends EventEmitter {
  private nkn: NknClient;
  private ipfs: IpfsService;
  private media: MediaService;
  private db: MessageDb;
  private config: Required<BotConfig>;
  private seed: string;
  private burnTimer: ReturnType<typeof setInterval> | null = null;

  constructor(config: BotConfig = {}) {
    super();
    this.seed = config.seed ?? NknClient.generateSeed();
    this.config = {
      seed: this.seed,
      dataDir: config.dataDir ?? path.join(os.homedir(), ".dchat-clawhub"),
      ipfsGateways: config.ipfsGateways ?? [],
      numSubClients: config.numSubClients ?? 4,
      autoDownloadMedia: config.autoDownloadMedia ?? true,
    };

    this.nkn = new NknClient(this.config.numSubClients);
    this.ipfs = new IpfsService(this.config.ipfsGateways.length ? this.config.ipfsGateways : undefined);
    this.media = new MediaService(this.ipfs, this.config.dataDir);
    this.db = new MessageDb(this.config.dataDir);

    this.nkn.on("message", (src: string, payload: string) => {
      this.handleIncoming(src, payload).catch((err) =>
        console.error("[dchat-bot] Error handling message:", err),
      );
    });

    this.nkn.on("statusChange", (status: ClientStatus) => {
      if (status.state === "connected") this.emit("connected", status);
      if (status.state === "disconnected") this.emit("disconnected");
    });
  }

  /** Connect to NKN network. Returns bot's NKN address. */
  async start(): Promise<string> {
    const status = await this.nkn.connect(this.seed);
    this.startBurnScheduler();
    return status.address!;
  }

  /** Disconnect and clean up. */
  async stop(): Promise<void> {
    this.stopBurnScheduler();
    await this.nkn.disconnect();
    this.db.close();
  }

  /** Get the bot's NKN address (available after start). */
  get address(): string | undefined {
    return this.nkn.getAddress();
  }

  /** Get the seed (for persistence). */
  getSeed(): string {
    return this.seed;
  }

  // ── Sending ──────────────────────────────────────────────

  /**
   * Send a text message (fire-and-forget). Returns message ID.
   * Use for long-running bots. Delivery confirmation arrives via receipt events.
   */
  sendText(to: string, text: string): string {
    const msg = this.buildMessage("text", text);
    this.sendAndStoreNoReply(to, msg);
    return msg.id;
  }

  /**
   * Send a text message and wait for NKN network to accept it.
   * Use for one-shot CLI sends where the process exits immediately after.
   * Returns message ID. Does NOT wait for recipient ACK — only for relay dispatch.
   * If the recipient is offline, the message is queued by NKN relay nodes.
   */
  async sendTextAwait(to: string, text: string): Promise<string> {
    const msg = this.buildMessage("text", text);
    const myAddress = this.nkn.getAddress()!;
    this.storeOutbound(myAddress, to, msg, "sending");
    try {
      await this.nkn.send(to, JSON.stringify(msg));
      this.db.updateStatusIfNotDelivered(msg.id, "sent");
    } catch (err) {
      const errMsg = err instanceof Error ? err.message : String(err);
      // Any timeout (including "failed to send with any client: ... Message timeout")
      // means the NKN relay accepted the message but recipient didn't ACK (offline).
      // The relay still queues the message for msgHoldingSeconds (1 hour).
      if (errMsg.toLowerCase().includes("timeout")) {
        console.log("[dchat] Recipient offline — message queued by NKN relay (up to 1 hour)");
        this.db.updateStatusIfNotDelivered(msg.id, "sent");
      } else {
        this.db.updateStatus(msg.id, "failed");
        throw err;
      }
    }
    return msg.id;
  }

  /** Send an image file. Returns message ID. */
  async sendImage(to: string, filePath: string): Promise<string> {
    const result = await this.media.uploadImage(filePath);
    const msg = this.buildMessage("image", result.content, result.options);
    this.sendAndStoreNoReply(to, msg, result.localFilePath);
    return msg.id;
  }

  /** Send an audio file. Returns message ID. */
  async sendAudio(to: string, filePath: string, durationSeconds?: number): Promise<string> {
    const result = await this.media.uploadAudio(filePath, durationSeconds);
    const msg = this.buildMessage("audio", result.content, result.options);
    this.sendAndStoreNoReply(to, msg, result.localFilePath);
    return msg.id;
  }

  /** Send a generic file. Returns message ID. */
  async sendFile(to: string, filePath: string): Promise<string> {
    const result = await this.media.uploadFile(filePath);
    const msg = this.buildMessage("file", result.content, result.options);
    this.sendAndStoreNoReply(to, msg, result.localFilePath);
    return msg.id;
  }

  /** Send a delivery receipt for a received message. */
  sendReceipt(to: string, messageId: string): void {
    const msg: MessageData = {
      id: crypto.randomUUID(),
      contentType: "receipt",
      targetID: messageId,
      timestamp: Date.now(),
    };
    this.nkn.sendNoReply(to, JSON.stringify(msg));
  }

  /** Send read receipts for received messages. */
  sendReadReceipt(to: string, messageIds: string[]): void {
    const msg: MessageData = {
      id: crypto.randomUUID(),
      contentType: "read",
      readIds: messageIds,
      timestamp: Date.now(),
    };
    this.nkn.sendNoReply(to, JSON.stringify(msg));
  }

  // ── History ──────────────────────────────────────────────

  /** Get message history with a peer. */
  getMessages(peerAddress: string, limit = 50, before?: number): Message[] {
    return this.db.getMessages(peerAddress, limit, before);
  }

  // ── Internal ─────────────────────────────────────────────

  private buildMessage(
    contentType: MessageContentType,
    content: string,
    options?: MessageOptions,
  ): MessageData {
    return {
      id: crypto.randomUUID(),
      contentType,
      content,
      options,
      timestamp: Date.now(),
    };
  }

  private async sendAndStore(to: string, msg: MessageData, localFilePath?: string): Promise<void> {
    const myAddress = this.nkn.getAddress()!;
    this.storeOutbound(myAddress, to, msg, "sending", localFilePath);
    try {
      await this.nkn.send(to, JSON.stringify(msg));
      // Only upgrade status — don't downgrade if already "delivered" (self-echo race)
      this.db.updateStatusIfNotDelivered(msg.id, "sent");
    } catch (err) {
      this.db.updateStatus(msg.id, "failed");
      throw err;
    }
  }

  private sendAndStoreNoReply(to: string, msg: MessageData, localFilePath?: string): void {
    const myAddress = this.nkn.getAddress()!;
    this.storeOutbound(myAddress, to, msg, "sent", localFilePath);
    this.nkn.sendNoReply(to, JSON.stringify(msg));
  }

  private storeOutbound(
    from: string,
    to: string,
    msg: MessageData,
    status: "sending" | "sent",
    localFilePath?: string,
  ): void {
    this.db.insertMessage({
      id: msg.id,
      sender: from,
      receiver: to,
      contentType: msg.contentType,
      content: msg.content ?? "",
      status,
      isOutbound: true,
      options: msg.options ? JSON.stringify(msg.options) : undefined,
      localFilePath,
      createdAt: msg.timestamp,
    });
  }

  private async handleIncoming(src: string, payload: string): Promise<void> {
    let msgData: MessageData;
    try {
      msgData = JSON.parse(payload);
    } catch {
      // Try base64 decode (nMobile sometimes sends base64)
      try {
        msgData = JSON.parse(Buffer.from(payload, "base64").toString("utf-8"));
      } catch {
        return; // Unparseable — ignore
      }
    }

    if (!msgData.id || !msgData.contentType) return;

    // Handle receipts
    if (msgData.contentType === "receipt" && msgData.targetID) {
      this.db.updateStatus(msgData.targetID, "delivered");
      this.emit("receipt", src, msgData.targetID);
      return;
    }

    if (msgData.contentType === "read" && msgData.readIds) {
      for (const id of msgData.readIds) {
        this.db.updateStatus(id, "read");
      }
      this.emit("readReceipt", src, msgData.readIds);
      return;
    }

    // Skip non-displayable control messages
    if (!DISPLAYABLE_TYPES.has(msgData.contentType)) return;

    const myAddress = this.nkn.getAddress()!;
    const isSelfMessage = src === myAddress;

    // Dedup — but allow self-echo (outbound already stored, inbound is the echo)
    if (this.db.hasMessage(msgData.id)) {
      if (!isSelfMessage) return;
      // Self-echo: update outbound status to delivered, emit event, but don't re-store
      this.db.updateStatus(msgData.id, "delivered");
    } else {
      // Store inbound message
      this.db.insertMessage({
        id: msgData.id,
        sender: src,
        receiver: myAddress,
        contentType: msgData.contentType,
        content: msgData.content ?? "",
        status: "delivered",
        isOutbound: false,
        options: msgData.options ? JSON.stringify(msgData.options) : undefined,
        createdAt: msgData.timestamp || Date.now(),
      });
    }

    // Track peer (skip self)
    if (!isSelfMessage) this.db.upsertPeer(src);

    // Send delivery receipt (skip self — avoids receipt loop)
    if (!isSelfMessage) this.sendReceipt(src, msgData.id);

    // Build event payload
    const incoming: IncomingMessage = {
      id: msgData.id,
      from: src,
      contentType: msgData.contentType,
      content: msgData.content ?? "",
      options: msgData.options,
      timestamp: msgData.timestamp || Date.now(),
    };

    // Auto-download media
    if (this.config.autoDownloadMedia && msgData.options) {
      try {
        const localPath = await this.downloadMediaFromOptions(
          msgData.id,
          msgData.contentType,
          msgData.content ?? "",
          msgData.options,
        );
        if (localPath) {
          incoming.localFilePath = localPath;
          this.db.updateLocalFilePath(msgData.id, localPath);
        }
      } catch (err) {
        console.error(`[dchat-bot] Failed to download media for ${msgData.id}:`, err);
      }
    }

    this.emit("message", incoming);
  }

  private async downloadMediaFromOptions(
    messageId: string,
    contentType: MessageContentType,
    content: string,
    options: MessageOptions,
  ): Promise<string | null> {
    // Inline audio (base64 data-URI)
    if (contentType === "audio" && content.startsWith("![audio]")) {
      return this.media.saveInlineAudio(messageId, content, (options.fileExt as string) ?? "aac");
    }

    // IPFS media
    if (options.ipfsHash && options.ipfsEncryptKeyBytes) {
      return this.media.downloadMedia(
        options.ipfsHash,
        options.ipfsEncryptKeyBytes,
        options.ipfsEncryptNonceSize ?? 12,
        (options.fileExt as string) ?? "bin",
        options.ipfsIp,
      );
    }

    return null;
  }

  private startBurnScheduler(): void {
    if (this.burnTimer) return;
    this.burnTimer = setInterval(() => {
      try {
        this.db.burnExpired();
      } catch (err) {
        console.error("[dchat-bot] Burn scheduler error:", err);
      }
    }, 5000);
  }

  private stopBurnScheduler(): void {
    if (this.burnTimer) {
      clearInterval(this.burnTimer);
      this.burnTimer = null;
    }
  }
}
