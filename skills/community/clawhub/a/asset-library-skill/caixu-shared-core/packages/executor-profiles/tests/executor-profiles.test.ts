import { describe, expect, it } from "vitest";
import { getSubmissionProfile } from "../src/index.js";

describe("@caixu/executor-profiles", () => {
  it("returns the default judge profile", () => {
    const profile = getSubmissionProfile("judge_demo_v1");
    expect(profile.profile_id).toBe("judge_demo_v1");
    expect(profile.file_fields).toContain("materials_zip");
  });
});
