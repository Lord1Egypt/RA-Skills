export type Severity = "critical" | "high" | "medium" | "low";
export type RiskGrade = "A" | "B" | "C" | "D" | "F";
export type ScanStatus = "queued" | "scanning" | "complete" | "failed";
export type SkillSource = "local" | "clawhub" | "url";
export type Recommendation = "block" | "warn" | "approve";
export type Plan = "free" | "pro" | "team";

export interface Finding {
  id?: string;
  category: string;
  severity: Severity;
  title: string;
  description: string;
  evidence?: string;
  lineNumber?: number | null;
  analysisPass: string;
  confidence?: number;
  fix?: string;
}

export interface FindingsCount {
  critical: number;
  high: number;
  medium: number;
  low: number;
}

export interface ScanResult {
  id?: string;
  skillName: string;
  skillVersion?: string;
  skillSource: SkillSource;
  status: ScanStatus;
  riskScore: number;
  riskGrade: RiskGrade;
  findingsCount: FindingsCount;
  findings: Finding[];
  summary?: string;
  recommendation?: Recommendation;
  createdAt?: Date;
  completedAt?: Date;
  cached?: boolean;
}

export interface SkillFrontmatter {
  name?: string;
  description?: string;
  version?: string;
  metadata?: {
    openclaw?: {
      requires?: {
        env?: string[];
        bins?: string[];
      };
    };
  };
  [key: string]: unknown;
}

export interface ParsedSkill {
  frontmatter: SkillFrontmatter;
  body: string;
  codeBlocks: CodeBlock[];
  urls: string[];
  ipAddresses: string[];
  domains: string[];
  rawContent: string;
}

export interface CodeBlock {
  language: string;
  content: string;
  lineStart: number;
  lineEnd: number;
}

export interface ThreatPattern {
  name: string;
  pattern: RegExp;
  severity: Severity;
  category: string;
  title: string;
  description: string;
  codeOnly?: boolean;
  fix?: string;
}
