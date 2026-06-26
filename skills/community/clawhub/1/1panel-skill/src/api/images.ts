import { BaseAPI } from "./base.js";

export class ImageAPI extends BaseAPI {
  async list(): Promise<any> {
    return this.get("/api/v2/containers/image");
  }

  async listAll(): Promise<any> {
    return this.get("/api/v2/containers/image/all");
  }

  async search(): Promise<any> {
    return this.post("/api/v2/containers/image/search", { page: 1, pageSize: 100, orderBy: "name", order: "ascending" });
  }

  async pull(name: string): Promise<any> {
    return this.post("/api/v2/containers/image/pull", { name });
  }

  async push(name: string): Promise<any> {
    return this.post("/api/v2/containers/image/push", { name });
  }

  async remove(id: string): Promise<any> {
    return this.post("/api/v2/containers/image/remove", { id });
  }

  async build(dockerfile: string, name: string, path: string): Promise<any> {
    return this.post("/api/v2/containers/image/build", { dockerfile, name, path });
  }

  async tag(id: string, repo: string, tag: string): Promise<any> {
    return this.post("/api/v2/containers/image/tag", { id, repo, tag });
  }

  async save(names: string[]): Promise<any> {
    return this.post("/api/v2/containers/image/save", { names });
  }

  async load(path: string): Promise<any> {
    return this.post("/api/v2/containers/image/load", { path });
  }
}
