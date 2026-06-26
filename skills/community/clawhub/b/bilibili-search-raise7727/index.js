export default function (api) {
  api.registerTool({
    name: "searchBilibili",
    description: "通过指定关键词在B站搜索相关视频。",
    require_approval: "never",
    parameters: {
      type: "object",
      properties: {
        keyword: {
          type: "string",
          description: "需要搜索的精准关键词"
        }
      },
      required: ["keyword"]
    },
    execute: async (args) => {
      const targetUrl = `http://127.0.0.1:8000/api/search_bilibili?keyword=${encodeURIComponent(args.keyword)}`;
      const response = await fetch(targetUrl);
      if (!response.ok) {
        throw new Error(`本地接口调用失败: HTTP ${response.status}`);
      }
      return await response.text();
    }
  });
}