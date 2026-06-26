export function ok(result) {
  return {
    ok: true,
    suggestions: [],
    trace: [],
    ...result,
  };
}

export function fail(error) {
  return {
    ok: false,
    error: {
      code: error?.code || "unknown",
      message: error?.message || "未知错误",
      procedure: error?.procedure || undefined,
      status: error?.status || undefined,
    },
  };
}

export function printJson(payload) {
  process.stdout.write(`${JSON.stringify(payload, null, 2)}\n`);
}
