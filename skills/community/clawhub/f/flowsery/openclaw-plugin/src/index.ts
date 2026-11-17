import { Type, type TObject, type TSchema } from "@sinclair/typebox";
import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import { jsonResult } from "openclaw/plugin-sdk/tool-results";
import { callApi, readConfig, type PluginConfig } from "./api.js";

const WebsiteSelector = {
  websiteId: Type.Optional(
    Type.String({ description: "Website id from flowsery_websites. Required unless domain is given." }),
  ),
  domain: Type.Optional(
    Type.String({ description: "Website domain from flowsery_websites, as an alternative to websiteId." }),
  ),
};

const DateRange = {
  startAt: Type.Optional(
    Type.String({
      description: 'ISO 8601 start of the reporting window, date or datetime, for example "2026-01-01". Defaults to 30 days ago.',
    }),
  ),
  endAt: Type.Optional(Type.String({ description: "ISO 8601 end of the reporting window. Defaults to now." })),
  timezone: Type.Optional(
    Type.String({ description: "IANA timezone used to bound and bucket the window. Defaults to the website timezone." }),
  ),
};

const Pagination = {
  limit: Type.Optional(Type.Integer({ minimum: 1, maximum: 1000, description: "Max rows to return. Defaults to 100." })),
  offset: Type.Optional(
    Type.Integer({ minimum: 0, description: "Rows to skip. Compare offset + limit against pagination.total in the response." }),
  ),
};

const FILTER_DIMENSIONS = [
  "country", "region", "city", "device", "browser", "os", "referrer", "ref",
  "source", "via", "utm_source", "utm_medium", "utm_campaign", "utm_term",
  "utm_content", "page", "hostname", "entry_page", "channel", "goal",
] as const;

const Filters: Record<string, TSchema> = Object.fromEntries(
  FILTER_DIMENSIONS.map((dimension) => [
    `filter_${dimension}`,
    Type.Optional(
      Type.String({
        description: `Restrict results to this ${dimension.replace(/_/g, " ")} value, as returned by flowsery_breakdown ("!v" excludes, "~v" contains, "a|b" any of). Filters combine with AND.`,
      }),
    ),
  ]),
);

const BreakdownDimension = Type.Union(
  [
    "device", "page", "entry_page", "exit_link", "hostname", "referrer",
    "channel", "campaign", "goal", "country", "region", "city", "browser",
    "browser_version", "os", "os_version", "utm_source", "utm_medium",
    "utm_campaign", "utm_term", "utm_content", "ref", "source", "via",
    "all_params",
  ].map((value) => Type.Literal(value)),
  {
    description:
      "The dimension to group visitors by. entry_page is the landing page, exit_link the outbound click, campaign the same as utm_campaign, ref, source and via the matching ?ref=, ?source= and ?via= URL parameters, and all_params every tracking parameter at once.",
  },
);

const query = (extra: Record<string, TSchema> = {}): TObject =>
  Type.Object({ ...WebsiteSelector, ...DateRange, ...Pagination, ...Filters, ...extra });

export default definePluginEntry({
  id: "flowsery",
  name: "Flowsery",
  description:
    "Read-only queries of Flowsery web analytics over the Flowsery API: visitors, trends, 25 breakdown dimensions, live visitors, and the issues AI found in session recordings. Results can include page URLs, locations and issue titles drawn from real visitor sessions, so share only what the user asked for.",
  register(api) {
    const cfg = (): PluginConfig => readConfig(api as { config?: unknown });

    const get = (path: string, params: unknown, signal?: AbortSignal) =>
      callApi(cfg(), "GET", path, { query: params as Record<string, unknown>, signal });

    api.registerTool({
      name: "flowsery_websites",
      label: "Flowsery: list websites",
      description:
        "List the websites this workspace token can read, with id, domain, timezone, currency, and KPI goal per site. Call this first: every other tool needs a websiteId or domain from this list, and omitting both fails with 'Website ID or domain is required'. Takes no parameters; the token decides the scope.",
      parameters: Type.Object({}),
      async execute(_toolCallId, _params, signal) {
        return jsonResult(await callApi(cfg(), "GET", "/websites", { signal }));
      },
    });

    api.registerTool({
      name: "flowsery_overview",
      label: "Flowsery: site totals",
      description:
        "Get headline totals for one site over a date range as a single row: visitors, sessions, bounce rate, average session duration, revenue, revenue per visitor and conversion rate. Dates default to the last 30 days ending now; timezone defaults to the site setting. Every filter_* argument narrows the whole result, so filter_country plus filter_device answers 'mobile visitors from Germany' in one call. Use flowsery_timeseries for the trend over time and flowsery_breakdown for the split by page, source or geography.",
      parameters: query(),
      async execute(_toolCallId, params, signal) {
        return jsonResult(await get("/overview", params, signal));
      },
    });

    api.registerTool({
      name: "flowsery_timeseries",
      label: "Flowsery: trend over time",
      description:
        "Get the same metrics as flowsery_overview bucketed by hour, day, week or month, plus totals across the whole window. Returns one point per bucket with a timestamp, visitors, sessions, conversion rate, and revenue split into new, renewal and refund. Use this for anything shaped like a trend or a chart; use flowsery_overview for one total and flowsery_breakdown for a split by dimension rather than time. Dates default to the last 30 days and interval to day. Asking for hourly buckets across a year returns thousands of points, so match the interval to the range.",
      parameters: query({
        interval: Type.Optional(
          Type.Union(
            [Type.Literal("hour"), Type.Literal("day"), Type.Literal("week"), Type.Literal("month")],
            { description: "Bucket size. Defaults to day; pick hour only for ranges of a few days." },
          ),
        ),
      }),
      async execute(_toolCallId, params, signal) {
        return jsonResult(await get("/timeseries", params, signal));
      },
    });

    api.registerTool({
      name: "flowsery_breakdown",
      label: "Flowsery: break down by dimension",
      description:
        "Group visitors by any one of 25 dimensions, ranked by visitors descending, for a date range: top pages, referrers, countries, devices, browsers, campaigns, UTM parameters, exit links and more. This one tool replaces the API's per-dimension endpoints. Combine a dimension with filter_* arguments to drill in, for example dimension=page with filter_utm_campaign to see where one campaign's traffic landed. Rows carry value, visitors, revenue and percentage with pagination.total; limit defaults to 100 (max 1000). Dates default to the last 30 days. Use flowsery_overview when you need totals rather than a split.",
      parameters: query({ dimension: BreakdownDimension }),
      async execute(_toolCallId, params, signal) {
        return jsonResult(await get("/breakdown", params, signal));
      },
    });

    api.registerTool({
      name: "flowsery_realtime",
      label: "Flowsery: live visitors",
      description:
        "Count the visitors active on the site in the last five minutes. A point-in-time number with no history: it takes no date, filter or pagination arguments, so it answers 'is anyone on the site now' and nothing about trends. Use flowsery_timeseries with interval hour for those. Returns data[0].visitors. Poll no more than once every 5 seconds.",
      parameters: Type.Object({ ...WebsiteSelector }),
      async execute(_toolCallId, params, signal) {
        return jsonResult(await get("/realtime", params, signal));
      },
    });

    api.registerTool({
      name: "flowsery_issues",
      label: "Flowsery: AI-detected issues",
      description:
        "List the bugs, broken flows and UX problems the AI found while analyzing session recordings, deduplicated across sessions and ranked by severity (or by last seen with sort=recency). Each row has title, severity, status, sessions affected, and first/last seen; the response also carries site-wide open, in-progress and resolved counts plus pagination.total. Use this for 'what is broken'; per-issue sessions, steps to replicate and status changes are only in the Flowsery dashboard, not in this plugin. Suspended issues are hidden unless status=suspended, so an issue that vanished was probably suspended, not deleted. Limit defaults to 100 (max 1000).",
      parameters: Type.Object({
        ...WebsiteSelector,
        ...Pagination,
        status: Type.Optional(
          Type.Union(
            [Type.Literal("open"), Type.Literal("in_progress"), Type.Literal("resolved"), Type.Literal("suspended")],
            { description: "Omit for open, in_progress and resolved together; suspended issues only appear with status=suspended." },
          ),
        ),
        severity: Type.Optional(
          Type.Union([
            Type.Literal("low"),
            Type.Literal("medium"),
            Type.Literal("high"),
            Type.Literal("critical"),
          ]),
        ),
        search: Type.Optional(Type.String({ description: "Match against issue title and description (max 200 characters)." })),
        sort: Type.Optional(
          Type.Union([Type.Literal("severity"), Type.Literal("recency")], {
            description: "Order by severity (default) or recency (last seen).",
          }),
        ),
      }),
      async execute(_toolCallId, params, signal) {
        return jsonResult(await get("/issues", params, signal));
      },
    });
  },
});
