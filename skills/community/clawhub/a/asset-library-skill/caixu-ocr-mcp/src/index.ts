import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import {
  extractParserTextDataSchema,
  extractVisualTextDataSchema,
  listLocalFilesDataSchema,
  localFileSchema,
  readLocalTextFileDataSchema,
  renderPdfPagesDataSchema,
  toolResultSchema
} from "@caixu/contracts";
import { listLocalFilesTool } from "./tools/list-local-files.js";
import { readLocalTextFileTool } from "./tools/read-local-text-file.js";
import { extractParserTextTool } from "./tools/extract-parser-text.js";
import { extractVisualTextTool } from "./tools/extract-visual-text.js";
import { renderPdfPagesTool } from "./tools/render-pdf-pages.js";

const listLocalFilesOutputSchema = toolResultSchema(listLocalFilesDataSchema);
const readLocalTextFileOutputSchema = toolResultSchema(readLocalTextFileDataSchema);
const extractParserTextOutputSchema = toolResultSchema(extractParserTextDataSchema);
const extractVisualTextOutputSchema = toolResultSchema(extractVisualTextDataSchema);
const renderPdfPagesOutputSchema = toolResultSchema(renderPdfPagesDataSchema);

const visualInputItemSchema = z.object({
  file_name: z.string().min(1),
  file_path: z.string().min(1),
  mime_type: z.string().min(1)
});

const server = new McpServer({
  name: "caixu-ocr-mcp",
  version: "0.1.0"
});

server.registerTool(
  "list_local_files",
  {
    description:
      "List local files under an input root and return deterministic local file records with suggested routes.",
    inputSchema: {
      input_root: z.string().min(1)
    },
    outputSchema: listLocalFilesOutputSchema.shape
  },
  async ({ input_root }) => {
    const result = await listLocalFilesTool({ input_root });
    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      structuredContent: result
    };
  }
);

server.registerTool(
  "read_local_text_file",
  {
    description: "Read a local text-like file into raw UTF-8 text.",
    inputSchema: {
      file: localFileSchema
    },
    outputSchema: readLocalTextFileOutputSchema.shape
  },
  async ({ file }) => {
    const result = await readLocalTextFileTool({ file });
    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      structuredContent: result
    };
  }
);

server.registerTool(
  "extract_parser_text",
  {
    description:
      "Use the Zhipu file parser to extract text from PDF/Office files, optionally returning export assets.",
    inputSchema: {
      file: localFileSchema,
      mode: z.enum(["lite", "export"]).optional()
    },
    outputSchema: extractParserTextOutputSchema.shape
  },
  async ({ file, mode }) => {
    const result = await extractParserTextTool({ file, mode });
    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      structuredContent: result
    };
  }
);

server.registerTool(
  "extract_visual_text",
  {
    description:
      "Extract OCR/VLM text from images, PDFs, or parser-exported image assets.",
    inputSchema: {
      engine: z.enum(["ocr", "vlm"]).optional(),
      items: z.array(visualInputItemSchema).min(1)
    },
    outputSchema: extractVisualTextOutputSchema.shape
  },
  async ({ engine, items }) => {
    const result = await extractVisualTextTool({ engine, items });
    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      structuredContent: result
    };
  }
);

server.registerTool(
  "render_pdf_pages",
  {
    description:
      "Render a PDF into PNG page images for downstream page-level visual parsing.",
    inputSchema: {
      file: localFileSchema,
      renderer: z.enum(["pdftoppm", "pdftocairo"]).optional()
    },
    outputSchema: renderPdfPagesOutputSchema.shape
  },
  async ({ file, renderer }) => {
    const result = await renderPdfPagesTool({ file, renderer });
    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
      structuredContent: result
    };
  }
);

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("caixu-ocr-mcp running on stdio");
}

main().catch((error) => {
  console.error("caixu-ocr-mcp failed:", error);
  process.exit(1);
});
