import { afterAll, describe, expect, test } from "bun:test";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { hermesEnv, parseMoneyPrefix, toFloat } from "../src/core/env";

const tmp = fs.mkdtempSync(path.join(process.env.TMPDIR ?? os.tmpdir(), "caic-env-"));
const KEY = "CAIC_TEST_KEY_DO_NOT_USE";

afterAll(() => {
  delete process.env.CAIC_TEST_KEY_DO_NOT_USE;
  fs.rmSync(tmp, { recursive: true, force: true });
});

describe("hermesEnv", () => {
  test("reads from $HERMES_HOME/.env when not in process env", () => {
    delete process.env.CAIC_TEST_KEY_DO_NOT_USE;
    fs.writeFileSync(path.join(tmp, ".env"), `${KEY}="from-file-value"\nOTHER=1\n`, "utf8");
    process.env.HERMES_HOME = tmp;
    expect(hermesEnv(KEY)).toBe("from-file-value");
  });

  test("process env takes precedence over .env file", () => {
    process.env.CAIC_TEST_KEY_DO_NOT_USE = "from-process";
    expect(hermesEnv(KEY)).toBe("from-process");
    delete process.env.CAIC_TEST_KEY_DO_NOT_USE;
  });

  test("missing key -> undefined", () => {
    expect(hermesEnv("CAIC_NEVER_SET_ANYWHERE_XYZ")).toBeUndefined();
  });

  test("missing .env file -> undefined, no throw", () => {
    process.env.HERMES_HOME = path.join(tmp, "does-not-exist");
    expect(hermesEnv(KEY)).toBeUndefined();
    delete process.env.HERMES_HOME;
  });
});

describe("toFloat", () => {
  test("money strings and numbers", () => {
    expect(toFloat("$1,234.50 USD")).toBe(1234.5);
    expect(toFloat(12)).toBe(12);
    expect(toFloat("12")).toBe(12);
    expect(toFloat(true)).toBeNull();
    expect(toFloat("not-a-number")).toBeNull();
    expect(toFloat(null)).toBeNull();
  });
});

describe("parseMoneyPrefix", () => {
  test("first numeric run wins", () => {
    expect(parseMoneyPrefix("CN¥6.38 (Paid: CN¥6.38 / Granted: CN¥0.00)")).toBe(6.38);
    expect(parseMoneyPrefix("$9.20 available")).toBe(9.2);
    expect(parseMoneyPrefix(undefined)).toBeNull();
    expect(parseMoneyPrefix("no digits")).toBeNull();
  });
});
