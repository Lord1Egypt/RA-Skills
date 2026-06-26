import { scanSkill as sharedScanSkill } from "@clawvet/shared";
import type { ScanResult } from "@clawvet/shared";
import { runSemanticAnalysis } from "./semantic-analysis.js";

export interface ScanOptions {
  semantic?: boolean;
}

export async function scanSkill(
  content: string,
  options: ScanOptions = {}
): Promise<ScanResult> {
  return sharedScanSkill(content, {
    semantic: options.semantic,
    semanticAnalyzer: options.semantic ? runSemanticAnalysis : undefined,
  });
}
