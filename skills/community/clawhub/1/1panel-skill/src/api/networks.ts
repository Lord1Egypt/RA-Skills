import { BaseAPI } from "./base.js";

export class NetworkAPI extends BaseAPI {
  async list(): Promise<any> {
    return this.post("/api/v2/containers/network/search", { page: 1, pageSize: 100 });
  }

  async listAll(): Promise<any> {
    return this.get("/api/v2/containers/network");
  }

  async create(name: string, driver = "bridge"): Promise<any> {
    return this.post("/api/v2/containers/network", { name, driver });
  }

  async remove(id: string): Promise<any> {
    return this.post("/api/v2/containers/network/del", { id });
  }
}
