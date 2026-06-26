import { OnePanelConfig } from "../types/config.js";
import { generateToken } from "../utils/auth.js";

export class BaseAPI {
  protected config: OnePanelConfig;

  constructor(config: OnePanelConfig) {
    this.config = { protocol: "http", ...config };
  }

  protected async request(path: string, options: RequestInit = {}): Promise<any> {
    const { token, timestamp } = generateToken(this.config.apiKey);
    const url = `${this.config.protocol}://${this.config.host}:${this.config.port}${path}`;

    const response = await fetch(url, {
      ...options,
      headers: {
        "1Panel-Token": token,
        "1Panel-Timestamp": timestamp,
        "Content-Type": "application/json",
        ...options.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`1Panel API error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  protected post(path: string, body: any): Promise<any> {
    return this.request(path, { method: "POST", body: JSON.stringify(body) });
  }

  protected get(path: string): Promise<any> {
    return this.request(path, { method: "GET" });
  }
}
