import { describe, it, expect, vi, beforeEach } from "vitest";
import { mkdtempSync, writeFileSync, rmSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";

const scanSkillMock = vi.fn(async () => ({
  skillName: "test-skill",
  status: "complete",
  riskScore: 0,
  riskGrade: "A",
  findingsCount: { critical: 0, high: 0, medium: 0, low: 0 },
  findings: [],
  recommendation: "approve",
}));

vi.mock("@clawvet/shared", () => ({
  scanSkill: scanSkillMock,
}));

describe("CLI semantic flag wiring", () => {
  beforeEach(() => {
    scanSkillMock.mockClear();
  });

  it("passes semantic=true to scanSkill when --semantic is enabled", async () => {
    const { scanCommand } = await import("../../../packages/cli/src/commands/scan.ts");

    const dir = mkdtempSync(join(tmpdir(), "clawvet-semantic-"));
    const skillPath = join(dir, "SKILL.md");
    writeFileSync(skillPath, "---\nname: test\ndescription: test\n---\n");

    try {
      await scanCommand(skillPath, { format: "json", semantic: true });
      expect(scanSkillMock).toHaveBeenCalledTimes(1);
      expect(scanSkillMock).toHaveBeenCalledWith(expect.any(String), { semantic: true });
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
  });
});
