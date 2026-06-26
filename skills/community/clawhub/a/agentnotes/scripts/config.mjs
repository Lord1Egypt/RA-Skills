const DEFAULT_LOG_PATH = "/api/v1/logs";
const DEFAULT_COMPLETE_PATH = "/api/v1/runs/complete";

export function getAgentNotesConfig() {
  const apiKey = process.env.AGENTNOTES_API_KEY;
  const agentId = process.env.AGENTNOTES_AGENT_ID;
  const baseUrl = (process.env.AGENTNOTES_BASE_URL || "http://localhost:3000").replace(
    /\/$/,
    ""
  );
  const logPath = process.env.AGENTNOTES_LOG_PATH || DEFAULT_LOG_PATH;
  const completePath =
    process.env.AGENTNOTES_COMPLETE_PATH || DEFAULT_COMPLETE_PATH;

  return {
    apiKey,
    agentId,
    baseUrl,
    logUrl: `${baseUrl}${logPath.startsWith("/") ? logPath : `/${logPath}`}`,
    completeUrl: `${baseUrl}${
      completePath.startsWith("/") ? completePath : `/${completePath}`
    }`,
  };
}
