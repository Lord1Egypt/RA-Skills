import type { ScanResult } from "@clawvet/shared";

export function printJsonResult(result: ScanResult): void {
  console.log(JSON.stringify(result, null, 2));
}
