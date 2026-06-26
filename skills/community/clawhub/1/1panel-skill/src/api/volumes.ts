import { BaseAPI } from "./base.js";

export class VolumeAPI extends BaseAPI {
  async list(): Promise<any> {
    return this.post("/api/v2/containers/volume/search", { page: 1, pageSize: 100 });
  }

  async listAll(): Promise<any> {
    return this.get("/api/v2/containers/volume");
  }

  async create(name: string): Promise<any> {
    return this.post("/api/v2/containers/volume", { name });
  }

  async remove(id: string): Promise<any> {
    return this.post("/api/v2/containers/volume/del", { id });
  }
}
