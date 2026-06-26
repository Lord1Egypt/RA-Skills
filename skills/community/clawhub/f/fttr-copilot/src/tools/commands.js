import { getDeviceDetail, resolveDevice } from "./devices.js";
import { getNetworkTopology } from "./network.js";

const EXECUTE_CMD = "/bison.device.v1.DeviceService/ExecuteCMD";
const GET_EXECUTE_RESULT = "/bison.device.v1.DeviceService/GetExecuteResult";
const DEFAULT_WAIT_TIMEOUT_MS = 12000;
const DEFAULT_POLL_INTERVAL_MS = 1000;

export async function getMasterGatewayInfo(client, args = {}) {
  return executeNamedCommand(client, args, {
    title: "主网关实时信息",
    cmdType: "CMD_TYPE_GET_FMU_INFO",
    paramName: "getFmuInfo",
    fallback: () => getDeviceDetail(client, args),
  });
}

export async function getSlaveGatewayInfo(client, args = {}) {
  return executeNamedCommand(client, args, {
    title: "从网关实时信息",
    cmdType: "CMD_TYPE_GET_FSU_INFO",
    paramName: "getFsuInfo",
    fallback: () => getNetworkTopology(client, args),
  });
}

export async function getAgentVersion(client, args = {}) {
  return executeNamedCommand(client, args, {
    title: "Agent 版本信息",
    cmdType: "CMD_TYPE_GET_AGENT_VERSION",
    paramName: "getAgentVersion",
    fallback: () => getDeviceDetail(client, args),
  });
}

async function executeNamedCommand(client, args, commandSpec) {
  const resolved = await resolveDevice(client, args.device_identifier);
  const command = {
    cmdType: commandSpec.cmdType,
    [commandSpec.paramName]: {},
  };
  const executeResponse = await client.unary(EXECUTE_CMD, {
    deviceId: resolved.id,
    command,
  });
  const sequenceID = executeResponse.sequenceId || executeResponse.sequence_id || "";
  const waitTimeoutMs = clampNumber(args.wait_timeout_ms, DEFAULT_WAIT_TIMEOUT_MS, 0, 30000);
  const pollIntervalMs = clampNumber(args.poll_interval_ms, DEFAULT_POLL_INTERVAL_MS, 100, 5000);
  const result = await pollExecuteResult(client, resolved.id, sequenceID, waitTimeoutMs, pollIntervalMs);

  if (!result.timed_out) {
    return formatCommandResult(commandSpec.title, resolved, sequenceID, result.response);
  }

  const fallbackResult = await tryFallback(commandSpec.fallback);
  return {
    title: commandSpec.title,
    summary: `${commandSpec.title}命令已下发，但设备尚未在 ${waitTimeoutMs}ms 内返回执行结果。`,
    data: {
      device_identifier: args.device_identifier,
      resolved_device: resolved,
      sequence_id: sequenceID,
      timed_out: true,
      fallback: fallbackResult,
    },
    suggestions: ["可稍后使用相同设备再次查询，或在后台按 sequence_id 追踪命令结果。"],
  };
}

async function pollExecuteResult(client, deviceID, sequenceID, waitTimeoutMs, pollIntervalMs) {
  if (!sequenceID || waitTimeoutMs === 0) {
    return { timed_out: true, response: null };
  }

  const deadline = Date.now() + waitTimeoutMs;
  for (;;) {
    try {
      const response = await client.unary(GET_EXECUTE_RESULT, {
        deviceId: deviceID,
        sequenceId: sequenceID,
      });
      const result = response.result || {};
      if (hasCommandResult(result)) {
        return { timed_out: false, response };
      }
    } catch (error) {
      if (!isPendingResult(error)) {
        throw error;
      }
    }

    if (Date.now() >= deadline) {
      return { timed_out: true, response: null };
    }
    await sleep(Math.min(pollIntervalMs, Math.max(deadline - Date.now(), 0)));
  }
}

function formatCommandResult(title, resolved, sequenceID, response) {
  const result = response.result || {};
  const status = result.status || "STATUS_UNSPECIFIED";

  return {
    title,
    summary: `${title}命令执行状态: ${status}`,
    data: {
      resolved_device: resolved,
      sequence_id: sequenceID,
      timed_out: false,
      status,
      command: response.command || null,
      result,
      raw: response,
    },
    suggestions: status === "STATUS_SUCCESS" || status === "STATUS_SUCCEED"
      ? ["可结合设备详情、拓扑或网络体验继续分析。"]
      : ["如果状态不是成功，建议结合设备在线状态和最近告警判断是否需要重试。"],
  };
}

function hasCommandResult(result) {
  const status = result.status ?? result.Status ?? "";
  return Boolean(status && status !== "STATUS_UNSPECIFIED" && status !== 0);
}

function isPendingResult(error) {
  return error?.code === "invalid_argument" && /记录不存在|not found/i.test(error.message || "");
}

async function tryFallback(fallback) {
  try {
    const result = await fallback();
    return {
      title: result.title,
      summary: result.summary,
      data: result.data,
    };
  } catch (error) {
    return {
      error: {
        code: error.code || "unknown",
        message: error.message,
      },
    };
  }
}

function clampNumber(value, fallback, min, max) {
  if (value === undefined || value === null || value === "") {
    return fallback;
  }
  const parsed = Number.parseInt(String(value), 10);
  if (!Number.isFinite(parsed)) {
    return fallback;
  }
  return Math.min(Math.max(parsed, min), max);
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
