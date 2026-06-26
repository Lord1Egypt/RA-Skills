import { CliError, ExitCode } from "./config.ts";

export type CommandName = "info" | "year" | "batch" | "next";

interface CommandFlagMap {
  info: {
    date: string;
  };
  year: {
    year: string;
  };
  batch: {
    dates: string;
  };
  next: {
    date: string;
    type: "Y" | "N";
  };
}

export type ValidatedFlags<K extends CommandName> = CommandFlagMap[K];

export interface CommandHelp {
  usage: string;
  description: string;
}

export const COMMAND_HELP_MAP: Record<CommandName, CommandHelp> = {
  info: {
    usage: "info --date <YYYY-MM-DD>",
    description: "Check if a specific date is a holiday, workday, or 调休.",
  },
  year: {
    usage: "year [--year <YYYY>]",
    description: "List all holidays and 调休 for a year (default: current year).",
  },
  batch: {
    usage: "batch --dates <YYYY-MM-DD,YYYY-MM-DD,...>",
    description: "Check multiple dates at once.",
  },
  next: {
    usage: "next --date <YYYY-MM-DD> [--type <Y|N>]",
    description: "Find the next holiday (Y) or workday (N) after a date.",
  },
};

export const COMMAND_ORDER: CommandName[] = ["info", "year", "batch", "next"];

const COMMAND_NAME_SET = new Set<string>(COMMAND_ORDER);

const ALLOWED_FLAG_NAMES: Record<CommandName, readonly string[]> = {
  info: ["date"],
  year: ["year"],
  batch: ["dates"],
  next: ["date", "type"],
};

function throwInvalidFlags(command: CommandName, message: string): never {
  throw new CliError(`Invalid flags for ${command}: ${message}`, ExitCode.PARAM_OR_CONFIG);
}

function ensureNoUnknownFlags(command: CommandName, rawFlags: Record<string, string>): void {
  const allowed = new Set(ALLOWED_FLAG_NAMES[command]);
  const unknownFlags: string[] = [];

  for (const key of Object.keys(rawFlags)) {
    if (!allowed.has(key)) {
      unknownFlags.push(`--${key}`);
    }
  }

  if (unknownFlags.length > 0) {
    throwInvalidFlags(command, `unknown flags: ${unknownFlags.join(", ")}`);
  }
}

function normalizeOptionalString(command: CommandName, rawFlags: Record<string, string>, key: string): string | undefined {
  const value = rawFlags[key];
  if (value === undefined) {
    return undefined;
  }

  const normalized = value.trim();
  if (normalized.length === 0) {
    throwInvalidFlags(command, `${key}: must be a non-empty string`);
  }

  return normalized;
}

function normalizeRequiredString(command: CommandName, rawFlags: Record<string, string>, key: string): string {
  const normalized = normalizeOptionalString(command, rawFlags, key);
  if (!normalized) {
    throwInvalidFlags(command, `${key}: is required`);
  }
  return normalized;
}

function validateDate(command: CommandName, key: string, value: string): string {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) {
    throwInvalidFlags(command, `${key}: must be in YYYY-MM-DD format`);
  }

  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    throwInvalidFlags(command, `${key}: invalid date "${value}"`);
  }

  return value;
}

function validateYear(command: CommandName, key: string, value: string): string {
  if (!/^\d{4}$/.test(value)) {
    throwInvalidFlags(command, `${key}: must be in YYYY format`);
  }

  const year = Number(value);
  if (year < 2000 || year > 2100) {
    throwInvalidFlags(command, `${key}: year out of range (2000-2100)`);
  }

  return value;
}

function validateDates(command: CommandName, key: string, value: string): string {
  const dates = value.split(",").map((d) => d.trim());
  if (dates.length === 0) {
    throwInvalidFlags(command, `${key}: must provide at least one date`);
  }

  for (const d of dates) {
    validateDate(command, key, d);
  }

  return dates.join(",");
}

export function isCommandName(value: string): value is CommandName {
  return COMMAND_NAME_SET.has(value);
}

export function validateCommandFlags<K extends CommandName>(
  command: K,
  rawFlags: Record<string, string>,
): ValidatedFlags<K> {
  ensureNoUnknownFlags(command, rawFlags);

  switch (command) {
    case "info": {
      const date = validateDate(command, "date", normalizeRequiredString(command, rawFlags, "date"));
      return { date } as ValidatedFlags<K>;
    }
    case "year": {
      const yearRaw = normalizeOptionalString(command, rawFlags, "year")
        ?? new Date().getFullYear().toString();
      const year = validateYear(command, "year", yearRaw);
      return { year } as ValidatedFlags<K>;
    }
    case "batch": {
      const dates = validateDates(command, "dates", normalizeRequiredString(command, rawFlags, "dates"));
      return { dates } as ValidatedFlags<K>;
    }
    case "next": {
      const date = validateDate(command, "date", normalizeRequiredString(command, rawFlags, "date"));
      const typeRaw = normalizeOptionalString(command, rawFlags, "type") ?? "Y";
      if (typeRaw !== "Y" && typeRaw !== "N") {
        throwInvalidFlags(command, `type: must be Y (holiday) or N (workday)`);
      }
      return { date, type: typeRaw } as ValidatedFlags<K>;
    }
    default: {
      const unhandled: never = command;
      throwInvalidFlags(command, `unsupported command: ${String(unhandled)}`);
    }
  }
}
