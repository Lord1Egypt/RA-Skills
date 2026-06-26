export const fileTools = [
  { name: "list_files", description: "List files in a directory", inputSchema: { type: "object", properties: { path: { type: "string" }, page: { type: "number" }, pageSize: { type: "number" } }, required: ["path"] } },
  { name: "search_files", description: "Search files with keyword", inputSchema: { type: "object", properties: { path: { type: "string" }, search: { type: "string" }, page: { type: "number" }, pageSize: { type: "number" } }, required: ["path"] } },
  { name: "get_file_content", description: "Get file content", inputSchema: { type: "object", properties: { path: { type: "string" } }, required: ["path"] } },
  { name: "save_file", description: "Save file content", inputSchema: { type: "object", properties: { path: { type: "string" }, content: { type: "string" } }, required: ["path", "content"] } },
  { name: "delete_file", description: "Delete file or directory", inputSchema: { type: "object", properties: { path: { type: "string" }, forceDelete: { type: "boolean" } }, required: ["path"] } },
  { name: "create_dir", description: "Create directory", inputSchema: { type: "object", properties: { path: { type: "string" } }, required: ["path"] } },
  { name: "create_file", description: "Create empty file", inputSchema: { type: "object", properties: { path: { type: "string" } }, required: ["path"] } },
  { name: "compress_files", description: "Compress files/directories", inputSchema: { type: "object", properties: { files: { type: "array", items: { type: "string" } }, dst: { type: "string" }, name: { type: "string" }, type: { type: "string" }, replace: { type: "boolean" }, secret: { type: "string" } }, required: ["files", "dst", "name", "type"] } },
  { name: "decompress_file", description: "Decompress archive", inputSchema: { type: "object", properties: { path: { type: "string" }, dst: { type: "string" }, type: { type: "string" }, secret: { type: "string" } }, required: ["path", "dst", "type"] } },
  { name: "move_file", description: "Move file/directory", inputSchema: { type: "object", properties: { from: { type: "string" }, to: { type: "string" }, overwrite: { type: "boolean" } }, required: ["from", "to"] } },
  { name: "rename_file", description: "Rename file/directory", inputSchema: { type: "object", properties: { path: { type: "string" }, name: { type: "string" } }, required: ["path", "name"] } },
  { name: "chmod_file", description: "Change file permissions", inputSchema: { type: "object", properties: { path: { type: "string" }, mode: { type: "string" }, sub: { type: "boolean" } }, required: ["path", "mode"] } },
  { name: "chown_file", description: "Change file owner", inputSchema: { type: "object", properties: { path: { type: "string" }, user: { type: "string" }, group: { type: "string" }, sub: { type: "boolean" } }, required: ["path", "user", "group"] } },
  { name: "check_file", description: "Check if file exists", inputSchema: { type: "object", properties: { path: { type: "string" } }, required: ["path"] } },
  { name: "get_file_size", description: "Get file size", inputSchema: { type: "object", properties: { path: { type: "string" } }, required: ["path"] } },
  { name: "get_file_tree", description: "Get directory tree", inputSchema: { type: "object", properties: { path: { type: "string" } }, required: ["path"] } },
  { name: "download_file", description: "Get download link", inputSchema: { type: "object", properties: { path: { type: "string" } }, required: ["path"] } },
  { name: "wget_file", description: "Download from URL", inputSchema: { type: "object", properties: { url: { type: "string" }, path: { type: "string" }, ignoreCertificate: { type: "boolean" } }, required: ["url", "path"] } },
];

export async function handleFileTool(client: any, name: string, args: any) {
  switch (name) {
    case "list_files": return await client.listFiles(args?.path, args?.page, args?.pageSize);
    case "search_files": return await client.searchFiles(args);
    case "get_file_content": return await client.getFileContent(args?.path);
    case "save_file": return await client.saveFile(args?.path, args?.content);
    case "delete_file": return await client.deleteFile(args?.path, args?.forceDelete);
    case "create_dir": return await client.createDir(args?.path);
    case "create_file": return await client.createFile(args?.path);
    case "compress_files": return await client.compressFiles(args);
    case "decompress_file": return await client.decompressFile(args);
    case "move_file": return await client.moveFile(args);
    case "rename_file": return await client.renameFile(args);
    case "chmod_file": return await client.chmodFile(args);
    case "chown_file": return await client.chownFile(args);
    case "check_file": return await client.checkFile(args?.path);
    case "get_file_size": return await client.getFileSize(args?.path);
    case "get_file_tree": return await client.getFileTree(args?.path);
    case "download_file": return await client.downloadFile(args?.path);
    case "wget_file": return await client.wgetFile(args?.url, args?.path, args?.ignoreCertificate);
    default: return null;
  }
}
