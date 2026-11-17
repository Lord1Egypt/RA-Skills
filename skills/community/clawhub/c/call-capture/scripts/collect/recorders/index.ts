/**
 * The recorders this cookbook ships, and how one gets chosen.
 *
 * `RECORDER` in `../config.ts` names one of the keys below, and
 * `--recorder=<slug>` overrides it for a single run. An entry is the only
 * place that knows a vendor exists.
 *
 * Two properties are load-bearing.
 *
 * **The key IS the provider slug**, and `resolve` refuses an entry where the
 * two disagree. `provider` is written into every capture's `source:` line and
 * compiled into the regex that reads those lines back, so a drift would
 * re-capture the whole window every morning, producing files and never
 * erroring.
 *
 * **`written` is a claim about evidence.** `live` means run against a real
 * workspace; `docs` means written from the vendor's specification and
 * compiles, and nothing more. Move an entry to `live` in the same commit that
 * reports the `--dry-run` it passed.
 *
 * Adding one: write the adapter beside the others and add an entry — the CLI,
 * the error messages and `--list` pick it up. `references/providers.md` is the
 * procedure, `references/recorder-apis.md` the endpoints, including five that
 * deliberately do not ship and why.
 */
import { RECORDER } from "../config";
import { ConfigError, type Recorder } from "../recorder";
import { avoma } from "./avoma";
import { clari } from "./clari";
import { fathom } from "./fathom";
import { fireflies } from "./fireflies";
import { gong } from "./gong";
import { grain } from "./grain";
import { granola } from "./granola";
import { modjo } from "./modjo";
import { tldv } from "./tldv";

export type RecorderEntry = {
  recorder: Recorder;
  /** The vendor's own spelling of its name, for the messages a human reads. */
  label: string;
  /**
   * `live`: run against a real workspace, response shapes confirmed.
   * `docs`: written from the vendor's specification and compiles. Verify it
   * with `--dry-run` before you deploy it, and say which you did.
   */
  written: "live" | "docs";
  /** What `CALL_RECORDER_API_KEY` has to hold for this one. */
  credential: string;
  docs: string;
};

export const RECORDERS = {
  avoma: {
    recorder: avoma,
    label: "Avoma",
    written: "live",
    credential: "API key",
    docs: "https://api.avoma.com/docs",
  },
  clari: {
    recorder: clari,
    label: "Clari Copilot",
    written: "docs",
    credential: "<apiKey>:<apiPassword>",
    docs: "https://api-doc.copilot.clari.com/",
  },
  fathom: {
    recorder: fathom,
    label: "Fathom",
    written: "docs",
    credential: "API key",
    docs: "https://developers.fathom.ai/quickstart",
  },
  fireflies: {
    recorder: fireflies,
    label: "Fireflies.ai",
    written: "docs",
    credential: "API key",
    docs: "https://docs.fireflies.ai/",
  },
  gong: {
    recorder: gong,
    label: "Gong",
    written: "docs",
    credential: "<accessKey>:<accessKeySecret>",
    docs: "https://help.gong.io/apidocs/introduction-2",
  },
  grain: {
    recorder: grain,
    label: "Grain",
    written: "docs",
    credential: "personal or workspace access token",
    docs: "https://developers.grain.com/",
  },
  granola: {
    recorder: granola,
    label: "Granola",
    written: "docs",
    credential: "API key (Business or Enterprise plan)",
    docs: "https://docs.granola.ai/",
  },
  modjo: {
    recorder: modjo,
    label: "Modjo",
    written: "docs",
    credential: "API key",
    docs: "https://api.modjo.ai/v2/docs",
  },
  tldv: {
    recorder: tldv,
    label: "tl;dv",
    written: "docs",
    credential: "API key",
    docs: "https://doc.tldv.io/",
  },
  // `satisfies`, not an annotation: it keeps the keys as literals, which is
  // what makes `RECORDER` in ../config.ts compiler-checked.
} satisfies Record<string, RecorderEntry>;

/** Every slug the compiler accepts for `RECORDER` in `../config.ts`. */
export type RecorderSlug = keyof typeof RECORDERS;

// The same registry, indexable by a string a human typed at a terminal.
const BY_SLUG: Record<string, RecorderEntry | undefined> = RECORDERS;

export const RECORDER_SLUGS = Object.keys(RECORDERS).sort();

/** The table `--list` prints, and the tail of every selection error. */
export function recorderTable(): string {
  const headings = ["slug", "recorder", "CALL_RECORDER_API_KEY holds", "state"];
  const cells = RECORDER_SLUGS.map((slug) => {
    const entry = BY_SLUG[slug]!;
    return [
      slug,
      entry.label,
      entry.credential,
      entry.written === "live"
        ? "verified against a live workspace"
        : "written from vendor docs, verify with --dry-run",
    ];
  });

  // Widths from the content: a hard-coded column is a column that stops
  // lining up the moment someone registers a tenth recorder.
  const widths = headings.map((heading, column) =>
    Math.max(heading.length, ...cells.map((row) => row[column]!.length)),
  );
  const line = (row: string[]): string =>
    `  ${row.map((cell, column) => cell.padEnd(widths[column]!)).join("  ")}`.trimEnd();

  return [
    "recorders this collector ships:",
    "",
    line(headings),
    ...cells.map(line),
    "",
    "the selection is RECORDER in scripts/call-capture/collect/config.ts;",
    "--recorder=<slug> overrides it for one run. Anything else is a new adapter",
    "in scripts/call-capture/collect/recorders/ plus an entry in its index.ts",
    "— see references/providers.md.",
    "",
    "deployed, CALL_RECORDER_API_KEY is a workspace environment variable the",
    "harness inherits: cargo-ai workspaceManagement envVar create --key",
    "CALL_RECORDER_API_KEY --secret. Export it to run this by hand.",
  ].join("\n");
}

/**
 * The selected recorder: `RECORDER` from `../config.ts`, unless
 * `--recorder=<slug>` overrode it for this run. Only the flag can name
 * something unknown — the constant is typed against the keys above.
 */
export function resolve(argv: readonly string[] = process.argv.slice(2)): {
  recorder: Recorder;
  entry: RecorderEntry;
} {
  const flag = argv
    .find((argument) => argument.startsWith("--recorder="))
    ?.slice("--recorder=".length);
  const slug = (flag ?? RECORDER).trim().toLowerCase();

  const entry = BY_SLUG[slug];
  if (entry === undefined) {
    throw new ConfigError(`Unknown recorder "${slug}".\n\n${recorderTable()}`);
  }

  // The one check that stops the deduplication key drifting away from what is
  // on disk — see the note at the top of this file.
  if (entry.recorder.provider !== slug) {
    throw new ConfigError(
      `Registry mismatch: "${slug}" is filed under a recorder whose provider is ` +
        `"${entry.recorder.provider}". One of the two is wrong, and until they ` +
        `agree the collector cannot recognise what it has already captured.`,
    );
  }

  return { recorder: entry.recorder, entry };
}
