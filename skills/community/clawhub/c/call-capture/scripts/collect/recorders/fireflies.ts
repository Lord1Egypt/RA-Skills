/**
 * Fireflies. Written from the vendor's own GraphQL schema docs, not yet run
 * against a live workspace: check it with `--dry-run` before you deploy it.
 *
 * One endpoint, POST only, so there are no paths to get wrong — only field
 * selections.
 *
 * The list selects metadata and readiness, nothing heavy. One query could
 * return every sentence in the window, but that is megabytes re-fetched every
 * morning for calls captured days ago, so sentences are selected per call in
 * `transcript`, after the pipeline has dropped what it has seen.
 *
 * Only `summary_status: processing` counts as not-ready: `failed` and
 * `skipped` describe the SUMMARY, and such a call usually still has a
 * transcript worth scribing.
 *
 * The plan limits are small and per day — see `references/recorder-apis.md`.
 * Docs: https://docs.fireflies.ai/graphql-api/query/transcripts
 */
import {
  fetchJson,
  HttpError,
  PACE_MS,
  pageGuard,
  recorderKey,
  sleep,
  type Call,
  type Recorder,
} from "../recorder";
import { pickTimestamp } from "./fields";
import { renderTurns, type Turn } from "./turns";

const API = "https://api.fireflies.ai/graphql";

// The documented ceiling for one `transcripts` query.
const PAGE_SIZE = 50;

const WINDOW_QUERY = `query Window($fromDate: DateTime, $toDate: DateTime, $limit: Int, $skip: Int) {
  transcripts(fromDate: $fromDate, toDate: $toDate, limit: $limit, skip: $skip) {
    id
    title
    date
    dateString
    meeting_attendees { displayName name email }
    meeting_info { summary_status }
  }
}`;

const TRANSCRIPT_QUERY = `query One($id: String!) {
  transcript(id: $id) {
    sentences { speaker_name text }
    summary { overview notes action_items }
  }
}`;

// The same object without the sentences, for the path where notes() is called
// on a call whose transcript was never fetched. Selecting sentences there
// would pull the whole conversation to render a paragraph of summary.
const SUMMARY_QUERY = `query Summary($id: String!) {
  transcript(id: $id) {
    summary { overview notes action_items }
  }
}`;

type GraphQlResponse<T> = {
  data?: T | null;
  errors?: { message?: string }[];
};

async function graphql<T>(query: string, variables: object): Promise<T> {
  const payload: GraphQlResponse<T> = await fetchJson(API, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${recorderKey()}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query, variables }),
  });

  // GraphQL answers 200 with an `errors` array, so an unchecked call here
  // reads a failure as an empty window — the exact silent-empty-run failure
  // this cookbook keeps warning about.
  if (payload.errors !== undefined && payload.errors.length > 0) {
    throw new Error(
      `fireflies: ${payload.errors.map((error) => error.message ?? "error").join("; ")}`,
    );
  }
  if (payload.data === undefined || payload.data === null) {
    throw new Error("fireflies: response carried no data");
  }
  return payload.data;
}

type Transcript = Record<string, unknown> & {
  id?: string;
  title?: string;
  meeting_attendees?: {
    displayName?: string | null;
    name?: string | null;
    email?: string | null;
  }[];
  meeting_info?: { summary_status?: string | null } | null;
};

const summaries = new Map<string, string | null>();

export const fireflies: Recorder = {
  provider: "fireflies",

  async listReady(from, to) {
    const calls: Call[] = [];
    const guard = pageGuard("fireflies");

    for (let skip = 0; ; skip += PAGE_SIZE) {
      guard();
      const data = await graphql<{ transcripts?: Transcript[] }>(WINDOW_QUERY, {
        fromDate: `${from}T00:00:00.000Z`,
        toDate: `${to}T23:59:59.999Z`,
        limit: PAGE_SIZE,
        skip,
      });
      const page = data.transcripts ?? [];

      for (const transcript of page) {
        if (transcript.id === undefined) continue;
        if (transcript.meeting_info?.summary_status === "processing") continue;

        // `dateString` is the ISO form; `date` is epoch milliseconds.
        const startAt = pickTimestamp(transcript, ["dateString", "date"]);
        if (startAt === undefined) {
          console.error(`skip ${transcript.id}: no date on the transcript`);
          continue;
        }

        calls.push({
          id: transcript.id,
          startAt,
          subject: transcript.title ?? "call",
          attendees: (transcript.meeting_attendees ?? []).map((attendee) => ({
            name: attendee.displayName ?? attendee.name ?? undefined,
            email: attendee.email ?? undefined,
          })),
        });
      }

      // Offset pagination, no cursor: a short page is the last page.
      if (page.length < PAGE_SIZE) break;
      await sleep(PACE_MS);
    }

    return calls;
  },

  async transcript(id) {
    await sleep(PACE_MS);

    let data: {
      transcript?: {
        sentences?: { speaker_name?: string | null; text?: string | null }[];
        summary?: Record<string, unknown> | null;
      } | null;
    };
    try {
      data = await graphql(TRANSCRIPT_QUERY, { id });
    } catch (error) {
      if (error instanceof HttpError) {
        console.error(`transcript ${id} unavailable (${error.status})`);
        return null;
      }
      // A GraphQL-level error on one call — a transcript still processing, a
      // permission on one meeting — is that call's problem, not the run's.
      console.error(
        `transcript ${id} unavailable: ${error instanceof Error ? error.message : String(error)}`,
      );
      return null;
    }

    // The summary comes back in the same request, so notes() spends nothing.
    const summary = data.transcript?.summary ?? null;
    if (summary !== null) {
      const sections: string[] = [];
      for (const key of ["overview", "notes", "action_items"] as const) {
        const value = summary[key];
        // `action_items` and `keywords` are strings here, not arrays.
        if (typeof value === "string" && value.trim() !== "") {
          sections.push(value.trim());
        }
      }
      summaries.set(id, sections.length > 0 ? sections.join("\n\n") : null);
    }

    const turns: Turn[] = [];
    for (const sentence of data.transcript?.sentences ?? []) {
      // `text` is the user-edited sentence; `raw_text` is what the audio
      // produced. The edited one is what the team believes was said.
      if (typeof sentence.text !== "string") continue;
      turns.push({
        speaker: sentence.speaker_name ?? undefined,
        text: sentence.text,
      });
    }

    return renderTurns(turns);
  },

  async notes(id) {
    const held = summaries.get(id);
    if (held !== undefined) return held;

    await sleep(PACE_MS);
    try {
      const data = await graphql<{
        transcript?: { summary?: Record<string, unknown> | null } | null;
      }>(SUMMARY_QUERY, { id });
      const overview = data.transcript?.summary?.["overview"];
      return typeof overview === "string" && overview.trim() !== ""
        ? overview.trim()
        : null;
    } catch (error) {
      console.error(
        `notes ${id} unavailable: ${error instanceof Error ? error.message : String(error)}`,
      );
      return null;
    }
  },
};
