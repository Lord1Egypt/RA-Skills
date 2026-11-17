const scenario = process.env.AIVIDEO_TEST_SCENARIO;

globalThis.fetch = async (url, init = {}) => {
  if (String(url).includes("/api/v1/quote/")) {
    return Response.json({
      model: "minimax",
      credits: 15,
      listPriceUsd: 0.15,
      currentBalance: 50,
      affordable: true,
      billable: false,
    });
  }

  if (init.method === "POST") {
    return Response.json({ status: "SUBMITTED", taskId: "task-resumable" });
  }

  if (String(url).endsWith("/status")) {
    return Response.json({ status: scenario === "failed" ? "FAILED" : "PROGRESS" });
  }

  return Response.json({ status: "FAILED", error: "Unexpected test request" }, { status: 500 });
};
