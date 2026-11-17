import { describe, expect, test } from "bun:test";
import { stress, type Scenario } from "./stress";
const fixture: Scenario = {
  collateralBase: "10000000000", debtBase: "4000000000", extraDebtBase: "1000000000",
  liquidationThresholdBps: "8000", collateralFactorBps: "8000", debtFactorBps: "10500", minimumHealthFactorWad: "1300000000000000000",
};
describe("fixed-point risk budget", () => {
  test("worked borrow passes current but fails stressed floor", () => {
    const result = stress(fixture);
    expect(result.currentHealthFactorWad).toBe("2000000000000000000");
    expect(result.proposedHealthFactorWad).toBe("1600000000000000000");
    expect(result.stressedHealthFactorWad).toBe("1219047619047619047");
    expect(result.passesStressFloor).toBe(false);
    expect(result.additionalDebtBudgetBase).toBe("688644688");
  });
  test("budget remains within floor after conservative debt rounding", () => {
    for (let amount = 1; amount < 100; amount++) {
      const scenario = { ...fixture, collateralBase: String(amount), debtBase: "0", extraDebtBase: "0" };
      const budget = stress(scenario).additionalDebtBudgetBase;
      expect(stress({ ...scenario, extraDebtBase: budget }).passesStressFloor).toBe(true);
    }
  });
  test("no debt has no finite health factor", () => {
    expect(stress({ ...fixture, debtBase: "0", extraDebtBase: "0" }).stressedHealthFactorWad).toBeNull();
  });
  test("preserves precision above Number.MAX_SAFE_INTEGER", () => {
    const result = stress({ ...fixture, collateralBase: "100000000000000000000000000", debtBase: "40000000000000000000000000", extraDebtBase: "10000000000000000000000000" });
    expect(result.stressedHealthFactorWad).toBe("1219047619047619047");
  });
  test("rejects ambiguous decimals, signed integers and invalid factors", () => {
    for (const debtBase of ["1.1", "-1", "1e6", " 10", "01"]) expect(() => stress({ ...fixture, debtBase })).toThrow();
    expect(() => stress({ ...fixture, debtFactorBps: "0" })).toThrow();
    expect(() => stress({ ...fixture, liquidationThresholdBps: "10001" })).toThrow();
  });
  test("conservative rounding cannot improve health", () => {
    expect(stress({ ...fixture, collateralBase: "3", debtBase: "1", extraDebtBase: "0", liquidationThresholdBps: "5000", collateralFactorBps: "9000" }).passesStressFloor).toBe(false);
  });
});
