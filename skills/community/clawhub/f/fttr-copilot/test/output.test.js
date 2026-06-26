import assert from "node:assert/strict";
import test from "node:test";

import { fail, ok } from "../src/output.js";

test("ok uses stable envelope", () => {
  assert.deepEqual(ok({ title: "标题", summary: "摘要", data: { value: 1 } }), {
    ok: true,
    title: "标题",
    summary: "摘要",
    data: { value: 1 },
    suggestions: [],
    trace: [],
  });
});

test("fail maps known error fields", () => {
  const error = new Error("认证失败");
  error.code = "unauthenticated";
  error.procedure = "/service/method";
  error.status = 401;

  assert.deepEqual(fail(error), {
    ok: false,
    error: {
      code: "unauthenticated",
      message: "认证失败",
      procedure: "/service/method",
      status: 401,
    },
  });
});
