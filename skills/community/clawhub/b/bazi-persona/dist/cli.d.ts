#!/usr/bin/env node
import type { SupportedLanguage } from "./kernel/types.js";
export declare function inspectPersona(args: Record<string, string>): string;
export declare function deleteStoredPersona(args: Record<string, string>): string;
export declare function renderCliHelp(language?: SupportedLanguage): string;
export declare function main(argv?: string[]): Promise<void>;
