#!/usr/bin/env node

import {
  buildCancelPageUrl,
  DEFAULT_TIMEOUT_MS,
  buildSuccessPageUrl,
  expandCheckoutTypeToReportTypes,
  FIXED_API_BASE,
  SUPPORTED_CHECKOUT_TYPES,
  SUPPORTED_PAGE_LOCALES,
  type CheckoutType,
  fail,
  parseArgs,
  requestApiEnvelope,
} from "./common.ts";

type CliOptions = {
  email: string;
  birth: string;
  checkoutType: CheckoutType;
  locale: Locale;
  nickname?: string;
  gender: 0 | 1;
  sect: 1 | 2;
  location?: string;
};

type SolarTime = {
  year: number;
  month: number;
  day: number;
  hour: number;
  minute: number;
  second: number;
};

type AnonymousCheckoutData = {
  checkoutSessionId: string;
  profileId: string;
  payUrl?: string;
};

const SUPPORTED_LOCALES = SUPPORTED_PAGE_LOCALES;
type Locale = (typeof SUPPORTED_LOCALES)[number];

function withCheckoutSuccessUrl(checkoutType: CheckoutType, locale: Locale): string {
  return buildSuccessPageUrl(locale, checkoutType);
}

function withCheckoutCancelUrl(locale: Locale): string {
  return buildCancelPageUrl(locale);
}

function printUsage(): void {
  console.log(`\nCreate anonymous Stripe checkout for bazi report.\n\nAPI base is fixed to: ${FIXED_API_BASE}\nSuccess URL template: https://asset.cantian.ai/public/{locale}/report_paid.html\nCancel URL template: https://asset.cantian.ai/public/{locale}/pay_cancel.html\n\nUsage:\n  node scripts/createCheckout.ts \\\n    --email <user@example.com> \\\n    --birth <YYYY-MM-DDTHH:mm[:ss]> \\\n    --type <DEEP|YEAR2026> \\\n    --gender <0|1> \\\n    [--locale <zh|en|ja|ko|zh-TW>] \\\n    [--nickname <name>] [--sect <1|2>] [--location <text>]\n\nRequired:\n  --email         Receiver email for report delivery\n  --birth         Birth time in local solar format\n  --type          DEEP or YEAR2026\n  --gender        0/1 (0=female, 1=male)\n\nOptional defaults:\n  --locale                zh, allowed: ${SUPPORTED_LOCALES.join(",")}\n  --sect                  2, allowed: 1/2\n`);
}

function parseLocale(input: string): Locale {
  if (input === "zh-TW") {
    return input;
  }

  const normalized = input.toLowerCase();
  const direct = SUPPORTED_LOCALES.find((item) => item.toLowerCase() === normalized);
  if (direct) {
    return direct;
  }

  fail(`Invalid --locale: ${input}. Allowed values: ${SUPPORTED_LOCALES.join(",")}.`);
}

function parseSolarTime(input: string): SolarTime {
  const matched = input.match(/^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})(?::(\d{2}))?$/);
  if (!matched) {
    fail(`Invalid --birth: ${input}. Expected YYYY-MM-DDTHH:mm[:ss].`);
  }

  const [, y, m, d, h, mm, s] = matched;
  const year = Number(y);
  const month = Number(m);
  const day = Number(d);
  const hour = Number(h);
  const minute = Number(mm);
  const second = Number(s ?? "0");

  if (year < 1600 || year > 2400) {
    fail(`Invalid birth year: ${year}. Allowed range: 1600-2400.`);
  }
  if (month < 1 || month > 12) {
    fail(`Invalid birth month: ${month}. Allowed range: 1-12.`);
  }
  if (day < 1 || day > 31) {
    fail(`Invalid birth day: ${day}. Allowed range: 1-31.`);
  }
  if (hour < 0 || hour > 23) {
    fail(`Invalid birth hour: ${hour}. Allowed range: 0-23.`);
  }
  if (minute < 0 || minute > 59) {
    fail(`Invalid birth minute: ${minute}. Allowed range: 0-59.`);
  }
  if (second < 0 || second > 59) {
    fail(`Invalid birth second: ${second}. Allowed range: 0-59.`);
  }

  return { year, month, day, hour, minute, second };
}

function buildOptions(raw: Record<string, string>): CliOptions {
  const allowedKeys = new Set([
    "email",
    "birth",
    "type",
    "locale",
    "nickname",
    "gender",
    "sect",
    "location",
  ]);
  for (const key of Object.keys(raw)) {
    if (!allowedKeys.has(key)) {
      fail(`Unknown option: --${key}`);
    }
  }

  const email = raw["email"];
  const birth = raw["birth"];

  if (!email) {
    fail("--email is required.");
  }
  if (!birth) {
    fail("--birth is required.");
  }
  const typeInput = raw["type"];
  if (!typeInput) {
    fail("--type is required. Allowed values: DEEP or YEAR2026.");
  }

  const checkoutTypeRaw = typeInput.trim().toUpperCase();
  if (checkoutTypeRaw.includes(",")) {
    fail(`Invalid --type: ${typeInput}. Use a single value: DEEP or YEAR2026.`);
  }
  if (!(SUPPORTED_CHECKOUT_TYPES as readonly string[]).includes(checkoutTypeRaw)) {
    fail(`Invalid --type: ${typeInput}. Allowed values: ${SUPPORTED_CHECKOUT_TYPES.join("|")}.`);
  }

  const genderRaw = raw["gender"];
  if (!genderRaw) {
    fail("--gender is required. Allowed values: 0 or 1.");
  }
  if (genderRaw !== "0" && genderRaw !== "1") {
    fail(`Invalid --gender: ${genderRaw}. Allowed values: 0 or 1.`);
  }

  const sectRaw = raw["sect"] ?? "2";
  if (sectRaw !== "1" && sectRaw !== "2") {
    fail(`Invalid --sect: ${sectRaw}. Allowed values: 1 or 2.`);
  }

  return {
    email,
    birth,
    checkoutType: checkoutTypeRaw as CheckoutType,
    locale: raw["locale"] ? parseLocale(raw["locale"]) : "zh",
    nickname: raw["nickname"],
    gender: Number(genderRaw) as 0 | 1,
    sect: Number(sectRaw) as 1 | 2,
    location: raw["location"],
  };
}

async function postAnonymousCheckout(options: CliOptions) {
  const reportTypes = expandCheckoutTypeToReportTypes(options.checkoutType);
  const profile = {
    solarTime: parseSolarTime(options.birth),
    gender: options.gender,
    sect: options.sect,
    ...(options.nickname ? { nickname: options.nickname } : {}),
    ...(options.location ? { location: options.location } : {}),
  };

  const payload = {
    email: options.email,
    reportType: options.checkoutType,
    types: reportTypes,
    sendEmailAt: "REPORT_CREATED",
    useShortPayUrl: true,
    successUrl: withCheckoutSuccessUrl(options.checkoutType, options.locale),
    cancelUrl: withCheckoutCancelUrl(options.locale),
    profile,
    metadata: {
      click_source: "openclaw",
    },
  };

  return requestApiEnvelope<AnonymousCheckoutData>(
    `${FIXED_API_BASE}/orders/create-anonymous-checkout`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-locale": options.locale,
      },
      body: JSON.stringify(payload),
    },
    DEFAULT_TIMEOUT_MS,
  );
}

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  if (args.length === 0 || args.includes("--help")) {
    printUsage();
    return;
  }

  const raw = parseArgs(args);
  const options = buildOptions(raw);
  const result = await postAnonymousCheckout(options);

  const profileId = result.data.profileId;

  console.log(
    JSON.stringify(
      {
        code: result.code,
        checkoutSessionId: result.data.checkoutSessionId,
        payUrl: result.data.payUrl ?? null,
        checkoutType: options.checkoutType,
        profileId,
        locale: options.locale,
      },
      null,
      2,
    ),
  );
}

await main();
