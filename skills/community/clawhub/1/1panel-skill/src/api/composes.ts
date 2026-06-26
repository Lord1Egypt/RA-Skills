import { BaseAPI } from "./base.js";

export class ComposeAPI extends BaseAPI {
  async list(): Promise<any> {
    return this.post("/api/v2/containers/compose/search", { page: 1, pageSize: 100 });
  }

  async create(name: string, content: string, path?: string): Promise<any> {
    return this.post("/api/v2/containers/compose", { name, content, path });
  }

  async remove(id: number): Promise<any> {
    return this.post("/api/v2/containers/compose/del", { id });
  }

  async start(id: number): Promise<any> {
    return this.post("/api/v2/containers/compose/operate", { id, operation: "start" });
  }

  async stop(id: number): Promise<any> {
    return this.post("/api/v2/containers/compose/operate", { id, operation: "stop" });
  }

  async restart(id: number): Promise<any> {
    return this.post("/api/v2/containers/compose/operate", { id, operation: "restart" });
  }

  async update(id: number, content: string): Promise<any> {
    return this.post("/api/v2/containers/compose/update", { id, content });
  }

  async test(content: string): Promise<any> {
    return this.post("/api/v2/containers/compose/test", { content });
  }

  async getEnv(id: number): Promise<any> {
    return this.post("/api/v2/containers/compose/env", { id });
  }

  async cleanLog(id: number): Promise<any> {
    return this.post("/api/v2/containers/compose/clean/log", { id });
  }
}
