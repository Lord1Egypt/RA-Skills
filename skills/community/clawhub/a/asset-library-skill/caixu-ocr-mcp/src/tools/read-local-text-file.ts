import { access, readFile } from "node:fs/promises";
import {
  type ReadLocalTextFileData,
  localFileSchema,
  makeToolResult
} from "@caixu/contracts";

export async function readLocalTextFileTool(input: {
  file: unknown;
}) {
  const parsedFile = localFileSchema.safeParse(input.file);
  if (!parsedFile.success) {
    return makeToolResult<ReadLocalTextFileData>("failed", undefined, {
      errors: [
        {
          code: "READ_LOCAL_TEXT_FILE_INVALID_INPUT",
          message: parsedFile.error.issues
            .map((issue) => `${issue.path.join(".") || "file"}: ${issue.message}`)
            .join("; "),
          retryable: false,
          file_id: null,
          file_name: null
        }
      ]
    });
  }

  const file = parsedFile.data;

  try {
    await access(file.file_path);
    const text = await readFile(file.file_path, "utf8");
    const data: ReadLocalTextFileData = {
      file,
      text,
      text_length: text.length
    };
    return makeToolResult("success", data);
  } catch (error) {
    return makeToolResult<ReadLocalTextFileData>("failed", undefined, {
      errors: [
        {
          code: "READ_LOCAL_TEXT_FILE_FAILED",
          message:
            error instanceof Error
              ? error.message
              : `Failed to read local text file ${file.file_name}`,
          retryable: false,
          file_id: file.file_id,
          file_name: file.file_name
        }
      ]
    });
  }
}
