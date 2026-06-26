import dns from "dns/promises";
import { isIP } from "net";
import FormData from "form-data";
import https from "https";
import http from "http";
import type { IpfsGateway } from "./types.js";

/** Public IPFS gateways — well-known, community-operated. */
const DEFAULT_GATEWAYS: IpfsGateway[] = [
  { host: "ipfs.io", port: 443, protocol: "https:" },
  { host: "dweb.link", port: 443, protocol: "https:" },
];

export class IpfsService {
  private gateways: IpfsGateway[];

  constructor(gateways?: IpfsGateway[]) {
    this.gateways = gateways?.length ? gateways : DEFAULT_GATEWAYS;
  }

  getPrimaryIp(): string {
    return this.gateways[0]?.host ?? "ipfs.io";
  }

  async upload(data: Buffer, fileName: string): Promise<string> {
    let lastError: Error | null = null;
    for (const gw of this.gateways) {
      try {
        return await this.uploadToGateway(gw, data, fileName);
      } catch (err) {
        lastError = err instanceof Error ? err : new Error(String(err));
      }
    }
    throw lastError ?? new Error("No IPFS gateways configured");
  }

  async download(ipfsHash: string, preferredIp?: string): Promise<Buffer> {
    const ordered = await this.orderGateways(preferredIp);
    let lastError: Error | null = null;
    for (const gw of ordered) {
      try {
        return await this.downloadFromGateway(gw, ipfsHash);
      } catch (err) {
        lastError = err instanceof Error ? err : new Error(String(err));
      }
    }
    throw lastError ?? new Error("No IPFS gateways configured");
  }

  /**
   * Check if an IP address is private/reserved (RFC 1918, loopback, link-local, etc.).
   * Handles both IPv4 and IPv6.
   */
  private isPrivateOrReservedIp(ip: string): boolean {
    // IPv4
    const v4Parts = ip.split(".");
    if (v4Parts.length === 4) {
      const octets = v4Parts.map(Number);
      if (octets.some((o) => isNaN(o) || o < 0 || o > 255)) return true;
      const [a, b] = octets;
      if (a === 10 || a === 127 || a === 0) return true;         // 10.0.0.0/8, loopback, 0.0.0.0
      if (a === 172 && b >= 16 && b <= 31) return true;           // 172.16.0.0/12
      if (a === 192 && b === 168) return true;                    // 192.168.0.0/16
      if (a === 169 && b === 254) return true;                    // 169.254.0.0/16 link-local
      return false;
    }
    // IPv6
    const normalized = ip.toLowerCase();
    if (normalized === "::1") return true;                         // loopback
    if (normalized.startsWith("fe80:")) return true;               // link-local
    if (normalized.startsWith("fc") || normalized.startsWith("fd")) return true; // ULA
    if (normalized === "::" || normalized === "::0") return true;  // unspecified
    // IPv4-mapped IPv6 (::ffff:10.0.0.1)
    const v4Mapped = normalized.match(/^::ffff:(\d+\.\d+\.\d+\.\d+)$/);
    if (v4Mapped) return this.isPrivateOrReservedIp(v4Mapped[1]);
    return false;
  }

  /**
   * Resolve a hostname to IP addresses and check that none are private/reserved.
   * Returns true if the host is safe to connect to (all resolved IPs are public).
   */
  private async isPublicHost(host: string): Promise<boolean> {
    // If it's already an IP literal, check directly
    if (isIP(host)) {
      return !this.isPrivateOrReservedIp(host);
    }
    // Resolve DNS and check ALL resolved addresses
    try {
      const addresses = await dns.resolve(host);
      if (addresses.length === 0) return false;
      return addresses.every((addr) => !this.isPrivateOrReservedIp(addr));
    } catch {
      return false; // DNS resolution failed — reject
    }
  }

  private async orderGateways(preferredIp?: string): Promise<IpfsGateway[]> {
    if (!preferredIp) return this.gateways;
    const preferred = this.gateways.filter((g) => g.host === preferredIp);
    const rest = this.gateways.filter((g) => g.host !== preferredIp);
    if (preferred.length === 0) {
      // Ad-hoc gateway from message options — resolve DNS and verify public
      const isPublic = await this.isPublicHost(preferredIp);
      if (!isPublic) {
        console.warn(`[IpfsService] Rejected non-public gateway: ${preferredIp}`);
        return this.gateways;
      }
      return [{ host: preferredIp, port: 80, protocol: "http:" }, ...this.gateways];
    }
    return [...preferred, ...rest];
  }

  private uploadToGateway(gw: IpfsGateway, data: Buffer, fileName: string): Promise<string> {
    const form = new FormData();
    form.append("file", data, { filename: fileName });
    const headers: Record<string, string> = { ...form.getHeaders() };
    if (gw.authHeader) headers["Authorization"] = gw.authHeader;

    return new Promise<string>((resolve, reject) => {
      const client = gw.protocol === "https:" ? https : http;
      const req = client.request(
        { hostname: gw.host, port: gw.port, path: "/api/v0/add", method: "POST", headers },
        (res) => {
          let body = "";
          res.on("data", (chunk: Buffer) => (body += chunk.toString()));
          res.on("end", () => {
            const headerHash = res.headers["ipfs-hash"];
            if (headerHash) {
              resolve(Array.isArray(headerHash) ? headerHash[0] : headerHash);
              return;
            }
            if (res.statusCode && res.statusCode >= 200 && res.statusCode < 300) {
              try {
                const json = JSON.parse(body);
                if (json.Hash) resolve(json.Hash as string);
                else reject(new Error(`No Hash in IPFS response: ${body}`));
              } catch {
                reject(new Error(`Failed to parse IPFS response: ${body}`));
              }
            } else {
              reject(new Error(`IPFS upload failed (${res.statusCode}): ${body}`));
            }
          });
        },
      );
      req.on("error", reject);
      req.setTimeout(30000, () => req.destroy(new Error("IPFS upload timeout")));
      form.pipe(req);
    });
  }

  private downloadFromGateway(gw: IpfsGateway, ipfsHash: string): Promise<Buffer> {
    const headers: Record<string, string> = {};
    if (gw.authHeader) headers["Authorization"] = gw.authHeader;

    return new Promise<Buffer>((resolve, reject) => {
      const client = gw.protocol === "https:" ? https : http;
      const req = client.request(
        {
          hostname: gw.host,
          port: gw.port,
          path: `/api/v0/cat?arg=${encodeURIComponent(ipfsHash)}`,
          method: "POST",
          headers,
        },
        (res) => {
          if (res.statusCode && (res.statusCode < 200 || res.statusCode >= 300)) {
            res.resume();
            reject(new Error(`IPFS download failed (${res.statusCode}) for ${ipfsHash}`));
            return;
          }
          const chunks: Buffer[] = [];
          res.on("data", (chunk: Buffer) => chunks.push(chunk));
          res.on("end", () => resolve(Buffer.concat(chunks)));
        },
      );
      req.on("error", reject);
      req.setTimeout(60000, () => req.destroy(new Error("IPFS download timeout")));
      req.end();
    });
  }
}
