export class ParsePipelineError extends Error {
  readonly code: string;
  readonly retryable: boolean;
  readonly taskId?: string;

  constructor(input: {
    code: string;
    message: string;
    retryable: boolean;
    taskId?: string;
  }) {
    super(input.message);
    this.name = "ParsePipelineError";
    this.code = input.code;
    this.retryable = input.retryable;
    this.taskId = input.taskId;
  }
}

export type PipelineErrorRecord = {
  code: string;
  message: string;
  retryable: boolean;
};

export function toPipelineErrorRecord(error: unknown): PipelineErrorRecord {
  if (error instanceof ParsePipelineError) {
    return {
      code: error.code,
      message: error.message,
      retryable: error.retryable
    };
  }

  return {
    code: "PARSE_MATERIAL_FAILED",
    message: error instanceof Error ? error.message : "Unknown parse pipeline error",
    retryable: false
  };
}
