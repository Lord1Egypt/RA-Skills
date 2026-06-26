import { API_BASE_URL, CliError, ExitCode, isRecord } from "./config.ts";
import { getJsonWithRetry, type HttpGetRequest } from "./http.ts";
import type { CommandName } from "./validators.ts";

export interface ExecuteCommandDependencies {
  requestJson?: (request: HttpGetRequest) => Promise<unknown>;
  timeoutMs?: number;
  retries?: number;
}

interface RuntimeContext {
  requestJson: (request: HttpGetRequest) => Promise<unknown>;
  timeoutMs: number | undefined;
  retries: number | undefined;
}

function getRequiredString(flags: Record<string, unknown>, key: string): string {
  const value = flags[key];
  if (typeof value === "string" && value.length > 0) {
    return value;
  }
  throw new CliError(`Missing required argument: --${key}`, ExitCode.INTERNAL);
}

async function runQuery(
  path: string,
  params: Record<string, string | undefined>,
  context: RuntimeContext,
): Promise<unknown> {
  const payload = await context.requestJson({
    url: `${API_BASE_URL}${path}`,
    params,
    timeoutMs: context.timeoutMs,
    retries: context.retries,
  });

  if (!isRecord(payload)) {
    throw new CliError(
      "Unexpected API response format",
      ExitCode.API_BUSINESS,
      { rawResponse: payload },
    );
  }

  if (payload.code !== 0) {
    throw new CliError(
      `API error (code ${payload.code})`,
      ExitCode.API_BUSINESS,
      { rawResponse: payload },
    );
  }

  return payload;
}

export async function executeCommand(
  command: CommandName,
  flags: Record<string, unknown>,
  dependencies: ExecuteCommandDependencies = {},
): Promise<unknown> {
  const context: RuntimeContext = {
    requestJson: dependencies.requestJson ?? getJsonWithRetry,
    timeoutMs: dependencies.timeoutMs,
    retries: dependencies.retries,
  };

  switch (command) {
    case "info": {
      const date = getRequiredString(flags, "date");
      return runQuery(`/info/${date}`, {}, context);
    }
    case "year": {
      const year = getRequiredString(flags, "year");
      return runQuery(`/year/${year}/`, {}, context);
    }
    case "batch": {
      const dates = getRequiredString(flags, "dates");
      return runQuery("/batch", { d: dates }, context);
    }
    case "next": {
      const date = getRequiredString(flags, "date");
      const type = getRequiredString(flags, "type");
      return runQuery(`/next/${date}`, { type }, context);
    }
    default: {
      const unhandled: never = command;
      throw new CliError(`Unsupported command: ${unhandled}`, ExitCode.INTERNAL);
    }
  }
}
