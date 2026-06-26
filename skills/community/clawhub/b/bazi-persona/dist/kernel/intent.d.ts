import type { PersonaRef, RoutedIntent, SupportedLanguage } from "./types.js";
export declare function normalizeLanguage(value?: string): SupportedLanguage | undefined;
export declare function detectLanguage(input: string): SupportedLanguage | undefined;
export declare function resolveLanguage(input: string, preferred?: "auto" | SupportedLanguage): SupportedLanguage;
export declare function parseArgsWithPositionalInput(argv: string[]): Record<string, string>;
export declare function routeIntent(input: string): RoutedIntent;
export declare function hydrateCreateArgs(args: Record<string, string>, input: string): Record<string, string>;
export declare function resolvePersonaRef(input: string, personas: PersonaRef[]): PersonaRef | undefined;
export declare function extractUpdateFact(input: string): string;
