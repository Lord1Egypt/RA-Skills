import type { ScanResult, Finding, Severity } from "@clawvet/shared";

const SEVERITY_TO_SARIF: Record<Severity, string> = {
  critical: "error",
  high: "error",
  medium: "warning",
  low: "note",
};

const SEVERITY_TO_LEVEL: Record<Severity, string> = {
  critical: "9.0",
  high: "7.0",
  medium: "4.0",
  low: "1.0",
};

export function printSarifResult(result: ScanResult): void {
  const rules = new Map<string, { id: string; finding: Finding }>();

  for (const f of result.findings) {
    const ruleId = f.category + "/" + f.title.toLowerCase().replace(/[^a-z0-9]+/g, "-");
    if (!rules.has(ruleId)) {
      rules.set(ruleId, { id: ruleId, finding: f });
    }
  }

  const sarif = {
    $schema: "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/main/sarif-2.1/schema/sarif-schema-2.1.0.json",
    version: "2.1.0",
    runs: [
      {
        tool: {
          driver: {
            name: "clawvet",
            informationUri: "https://github.com/clawvet/clawvet",
            rules: [...rules.values()].map((r) => ({
              id: r.id,
              shortDescription: { text: r.finding.title },
              fullDescription: { text: r.finding.description },
              defaultConfiguration: {
                level: SEVERITY_TO_SARIF[r.finding.severity],
              },
              properties: {
                security_severity: SEVERITY_TO_LEVEL[r.finding.severity],
              },
            })),
          },
        },
        results: result.findings.map((f) => {
          const ruleId = f.category + "/" + f.title.toLowerCase().replace(/[^a-z0-9]+/g, "-");
          return {
            ruleId,
            level: SEVERITY_TO_SARIF[f.severity],
            message: {
              text: f.description + (f.evidence ? ` Evidence: ${f.evidence}` : ""),
              ...(f.fix ? { markdown: `${f.description}\n\n**Fix:** ${f.fix}` } : {}),
            },
            locations: [
              {
                physicalLocation: {
                  artifactLocation: { uri: "SKILL.md" },
                  region: { startLine: f.lineNumber ?? 1 },
                },
              },
            ],
          };
        }),
      },
    ],
  };

  console.log(JSON.stringify(sarif, null, 2));
}
