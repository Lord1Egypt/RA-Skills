import { BaseAPI } from "./base.js";

export class ContainerAPI extends BaseAPI {
  // List operations
  async list(): Promise<any> {
    return this.post("/api/v2/containers/search", { page: 1, pageSize: 100, state: "all", orderBy: "name", order: "ascending" });
  }

  async listSimple(): Promise<any> {
    return this.post("/api/v2/containers/list", {});
  }

  async listByImage(image: string): Promise<any> {
    return this.post("/api/v2/containers/list/byimage", { name: image });
  }

  // Info operations
  async get(id: string): Promise<any> {
    return this.post("/api/v2/containers/info", { id });
  }

  async inspect(id: string): Promise<any> {
    return this.post("/api/v2/containers/inspect", { id });
  }

  async getStats(id: string): Promise<any> {
    return this.get(`/api/v2/containers/stats/${id}`);
  }

  async getStatus(): Promise<any> {
    return this.get("/api/v2/containers/status");
  }

  async getUsers(name: string): Promise<any> {
    return this.post("/api/v2/containers/users", { name });
  }

  // Lifecycle operations
  async start(id: string): Promise<any> {
    return this.post("/api/v2/containers/operate", { id, operation: "start" });
  }

  async stop(id: string): Promise<any> {
    return this.post("/api/v2/containers/operate", { id, operation: "stop" });
  }

  async restart(id: string): Promise<any> {
    return this.post("/api/v2/containers/operate", { id, operation: "restart" });
  }

  async pause(id: string): Promise<any> {
    return this.post("/api/v2/containers/operate", { id, operation: "pause" });
  }

  async unpause(id: string): Promise<any> {
    return this.post("/api/v2/containers/operate", { id, operation: "unpause" });
  }

  async kill(id: string): Promise<any> {
    return this.post("/api/v2/containers/operate", { id, operation: "kill" });
  }

  // Management operations
  async create(config: any): Promise<any> {
    return this.post("/api/v2/containers", config);
  }

  async update(id: string, config: any): Promise<any> {
    return this.post("/api/v2/containers/update", { id, ...config });
  }

  async rename(id: string, name: string): Promise<any> {
    return this.post("/api/v2/containers/rename", { id, name });
  }

  async upgrade(id: string, image: string): Promise<any> {
    return this.post("/api/v2/containers/upgrade", { id, image });
  }

  async remove(id: string): Promise<any> {
    return this.post("/api/v2/containers/del", { id });
  }

  async prune(): Promise<any> {
    return this.post("/api/v2/containers/prune", {});
  }

  // Logs
  async getLogs(id: string, tail = 100): Promise<any> {
    return this.post("/api/v2/containers/log", { id, tail });
  }

  async cleanLog(id: string): Promise<any> {
    return this.post("/api/v2/containers/clean/log", { id });
  }

  // Commit
  async commit(id: string, repo: string, tag: string): Promise<any> {
    return this.post("/api/v2/containers/commit", { id, repo, tag });
  }
}
