import crypto from "crypto";
import { EventEmitter } from "events";
import nkn from "nkn-sdk";
import type { ClientStatus } from "./types.js";

const NKN_SEED_RPC_SERVERS = [
  "http://seed.nkn.org:30003",
  "http://mainnet-seed-0001.nkn.org:30003",
  "http://mainnet-seed-0002.nkn.org:30003",
  "http://mainnet-seed-0003.nkn.org:30003",
];

export class NknClient extends EventEmitter {
  private client: nkn.MultiClient | null = null;
  private status: ClientStatus = { state: "disconnected" };
  private numSubClients: number;

  constructor(numSubClients = 4) {
    super();
    this.numSubClients = numSubClients;
  }

  getStatus(): ClientStatus {
    return { ...this.status };
  }

  getAddress(): string | undefined {
    return this.status.address;
  }

  /**
   * Generate a new random NKN seed (hex-encoded Ed25519 private key).
   */
  static generateSeed(): string {
    return crypto.randomBytes(32).toString("hex");
  }

  /**
   * Derive the NKN address from a seed without connecting to the network.
   */
  static deriveAddress(seed: string): string {
    const kp = nkn.crypto.keyPair(seed);
    return Buffer.from(kp.publicKey).toString("hex");
  }

  async connect(seed: string): Promise<ClientStatus> {
    if (this.client) await this.disconnect();
    this.updateStatus({ state: "connecting" });

    try {
      this.client = new nkn.MultiClient({
        seed,
        numSubClients: this.numSubClients,
        originalClient: false,
        rpcServerAddr: NKN_SEED_RPC_SERVERS[0],
      });

      await new Promise<void>((resolve, reject) => {
        const timeout = setTimeout(() => reject(new Error("Connection timeout after 30s")), 30000);
        this.client!.onConnect(() => {
          clearTimeout(timeout);
          resolve();
        });
      });

      this.updateStatus({
        state: "connected",
        address: this.client.addr,
        publicKey: this.client.getPublicKey(),
      });

      this.client.onMessage(({ src, payload }: { src: string; payload: Uint8Array | string }) => {
        const data = payload instanceof Uint8Array ? new TextDecoder().decode(payload) : payload;
        this.emit("message", src, data);
      });

      return this.getStatus();
    } catch (err) {
      this.updateStatus({ state: "disconnected" });
      this.client = null;
      throw err;
    }
  }

  async disconnect(): Promise<void> {
    if (this.client) {
      try {
        this.client.close();
      } catch {
        // ignore
      }
      this.client = null;
    }
    this.updateStatus({ state: "disconnected" });
  }

  async send(dest: string, data: string): Promise<void> {
    this.assertConnected();
    await this.client!.send(dest, data, { msgHoldingSeconds: 3600 });
  }

  sendNoReply(dest: string, data: string): void {
    this.assertConnected();
    // NKN SDK send() returns a promise even with noReply — catch to prevent
    // unhandled rejection when client disconnects before delivery completes.
    const p = this.client!.send(dest, data, { noReply: true, msgHoldingSeconds: 3600 });
    if (p && typeof p.catch === "function") {
      p.catch((err: unknown) => {
        console.error("[nkn] send failed (non-blocking):", err instanceof Error ? err.message : err);
      });
    }
  }

  private assertConnected(): void {
    if (!this.client || this.status.state !== "connected") {
      throw new Error("NKN client not connected");
    }
  }

  private updateStatus(status: ClientStatus): void {
    this.status = status;
    this.emit("statusChange", status);
  }
}
