import {
  type ListLocalFilesData,
  makeToolResult
} from "@caixu/contracts";
import { listLocalFiles } from "./low-level-common.js";

export async function listLocalFilesTool(input: {
  input_root: string;
}) {
  try {
    const files = await listLocalFiles(input.input_root);
    const data: ListLocalFilesData = {
      input_root: input.input_root,
      files
    };
    return makeToolResult("success", data, {
      next_recommended_skill: ["ingest-materials"]
    });
  } catch (error) {
    return makeToolResult<ListLocalFilesData>("failed", undefined, {
      errors: [
        {
          code: "LIST_LOCAL_FILES_FAILED",
          message: error instanceof Error ? error.message : "Failed to list local files",
          retryable: false
        }
      ]
    });
  }
}
