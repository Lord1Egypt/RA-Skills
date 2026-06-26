export const imageTools = [
  { name: "list_images", description: "List Docker images", inputSchema: { type: "object", properties: {} } },
  { name: "list_all_images", description: "List all Docker images", inputSchema: { type: "object", properties: {} } },
  { name: "search_images", description: "Search images", inputSchema: { type: "object", properties: {} } },
  { name: "pull_image", description: "Pull image", inputSchema: { type: "object", properties: { name: { type: "string" } }, required: ["name"] } },
  { name: "push_image", description: "Push image", inputSchema: { type: "object", properties: { name: { type: "string" } }, required: ["name"] } },
  { name: "remove_image", description: "Remove image", inputSchema: { type: "object", properties: { id: { type: "string" } }, required: ["id"] } },
  { name: "build_image", description: "Build image", inputSchema: { type: "object", properties: { dockerfile: { type: "string" }, name: { type: "string" }, path: { type: "string" } }, required: ["dockerfile", "name", "path"] } },
  { name: "tag_image", description: "Tag image", inputSchema: { type: "object", properties: { id: { type: "string" }, repo: { type: "string" }, tag: { type: "string" } }, required: ["id", "repo", "tag"] } },
  { name: "save_image", description: "Save image", inputSchema: { type: "object", properties: { names: { type: "array", items: { type: "string" } } }, required: ["names"] } },
  { name: "load_image", description: "Load image", inputSchema: { type: "object", properties: { path: { type: "string" } }, required: ["path"] } },
];

export async function handleImageTool(client: any, name: string, args: any) {
  switch (name) {
    case "list_images": return await client.listImages();
    case "list_all_images": return await client.listAllImages();
    case "search_images": return await client.searchImages();
    case "pull_image": return await client.pullImage(args?.name);
    case "push_image": return await client.pushImage(args?.name);
    case "remove_image": return await client.removeImage(args?.id);
    case "build_image": return await client.buildImage(args?.dockerfile, args?.name, args?.path);
    case "tag_image": return await client.tagImage(args?.id, args?.repo, args?.tag);
    case "save_image": return await client.saveImage(args?.names);
    case "load_image": return await client.loadImage(args?.path);
    default: return null;
  }
}
