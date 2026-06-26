#!/usr/bin/env node

import {
  DEFAULT_TIMEOUT_MS,
  buildSuccessPageUrl,
  FIXED_API_BASE,
  SUPPORTED_REPORT_TYPES,
  type CheckoutType,
  type ReportType,
  fail,
  parseArgs,
  requestApiEnvelope,
} from "./common.ts";

type CliOptions = {
  profileId: string;
};

type ReportData = {
  id: string;
  type: string;
  profileIds?: string[];
  version?: {
    id?: string;
    status?: string;
    locale?: string;
    content?: unknown;
  };
  createdAt?: string;
  updatedAt?: string;
};

type SearchReportsData = {
  results: ReportData[];
  pagination?: {
    limit: number;
    offset: number;
    total: number;
  };
};

type GetProfileData = {
  id?: string;
};

const DEEP_REPORT_TYPES: ReadonlySet<ReportType> = new Set(["LIFE", "LOVE", "WEALTH", "CAREER"]);

function printUsage(): void {
  console.log(`\nGet bazi report status by profileId.\n\nAPI base is fixed to: ${FIXED_API_BASE}\n\nUsage:\n  node scripts/getReport.ts --profile-id <profileId>\n`);
}

function buildOptions(raw: Record<string, string>): CliOptions {
  const allowedKeys = new Set(["profile-id"]);
  for (const key of Object.keys(raw)) {
    if (!allowedKeys.has(key)) {
      fail(`Unknown option: --${key}`);
    }
  }

  const profileId = raw["profile-id"];
  if (!profileId) {
    fail("--profile-id is required.");
  }

  return { profileId };
}

async function searchReportsByProfileId(profileId: string, timeoutMs: number) {
  return requestApiEnvelope<SearchReportsData>(
    `${FIXED_API_BASE}/reports/search`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        filter: {
          profileIds: {
            $in: [profileId],
          },
        },
        pagination: {
          offset: 0,
          limit: 50,
        },
      }),
    },
    timeoutMs,
  );
}

async function getProfilePaidStatus(profileId: string, timeoutMs: number): Promise<boolean> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(`${FIXED_API_BASE}/profiles/${encodeURIComponent(profileId)}`, {
      method: "GET",
      signal: controller.signal,
    });

    const text = await response.text();
    let parsed: unknown = null;
    if (text) {
      try {
        parsed = JSON.parse(text);
      } catch {
        fail(`Get profile response is not valid JSON. Status=${response.status}, body=${text}`);
      }
    }

    if (!parsed || typeof parsed !== "object") {
      fail("Get profile returned empty or invalid JSON payload.");
    }

    const result = parsed as {
      code?: unknown;
      message?: unknown;
      msg?: unknown;
      error?: unknown;
      errorMessage?: unknown;
      data?: GetProfileData;
    };

    if (typeof result.code !== "number") {
      fail(`Get profile returned invalid business code. Status=${response.status}, body=${text}`);
    }

    if (result.code === 1) {
      return true;
    }

    if (result.code === 404) {
      return false;
    }

    fail(
      `Get profile business error. code=${result.code}, message=${result.errorMessage ?? result.message ?? result.msg ?? result.error ?? "unknown"}, body=${text}`,
    );
  } catch (error) {
    if (error instanceof Error && error.name === "AbortError") {
      fail(`Get profile timeout after ${timeoutMs}ms.`);
    }

    fail(`Get profile failed: ${error instanceof Error ? error.message : String(error)}`);
  } finally {
    clearTimeout(timer);
  }
}

function resolveCheckoutTypeForDownloadUrl(reports: ReportData[]): CheckoutType {
  const knownTypes = new Set(
    reports
      .map((report) => report.type)
      .filter((value): value is ReportType =>
        (SUPPORTED_REPORT_TYPES as readonly string[]).includes(value),
      ),
  );

  if ([...knownTypes].some((type) => DEEP_REPORT_TYPES.has(type))) {
    return "DEEP";
  }

  if (knownTypes.has("YEAR2026")) {
    return "YEAR2026";
  }

  return "DEEP";
}

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  if (args.length === 0 || args.includes("--help")) {
    printUsage();
    return;
  }

  const raw = parseArgs(args);
  const options = buildOptions(raw);
  const paid = await getProfilePaidStatus(options.profileId, DEFAULT_TIMEOUT_MS);

  if (!paid) {
    console.log(
      JSON.stringify(
        {
          paid: false,
          readyToDownload: false,
          profileId: options.profileId,
          locale: "zh",
          downloadPageUrl: null,
        },
        null,
        2,
      ),
    );
    return;
  }

  const searchResult = await searchReportsByProfileId(options.profileId, DEFAULT_TIMEOUT_MS);
  const reports = searchResult.data.results ?? [];
  const readyToDownload = reports.some((report) => report.version?.status === "SUCCESS");
  const preferredLocale =
    reports.find((report) => typeof report.version?.locale === "string" && report.version.locale.length > 0)?.version
      ?.locale ?? "zh";
  const downloadPageUrl = buildSuccessPageUrl(
    preferredLocale,
    resolveCheckoutTypeForDownloadUrl(reports),
    options.profileId,
  );

  console.log(
    JSON.stringify(
      {
        paid,
        readyToDownload,
        profileId: options.profileId,
        locale: preferredLocale,
        downloadPageUrl,
      },
      null,
      2,
    ),
  );
}

await main();
