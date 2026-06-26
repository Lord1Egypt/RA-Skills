import { BaseAPI } from "./base.js";

/**
 * Terminal API
 */
export class TerminalAPI extends BaseAPI {
  /** Exec command */
  async execCommand(command: string, cwd?: string): Promise<any> {
    return this.post("/api/v2/hosts/command", { command, cwd });
  }

  /** Load system terminal setting info */
  async getSettings(): Promise<any> {
    return this.post("/api/v2/core/settings/terminal/search", {});
  }

  /** Update system terminal setting */
  async updateSettings(params: any): Promise<any> {
    return this.post("/api/v2/core/settings/terminal/update", params);
  }
}
