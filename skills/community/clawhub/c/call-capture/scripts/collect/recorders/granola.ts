/**
 * Granola. Written from the vendor's own OpenAPI document, not yet run against
 * a live workspace: check it with `--dry-run` before you deploy it.
 *
 * `GET /v1/notes` returns id, title and timestamps and no attendees, so
 * `listReady` fetches each note's detail to get them — a request per note per
 * run, which is why the summary that detail carries is kept for `notes()`
 * rather than fetched again. Attendees are not optional: the pipeline decides
 * internal-versus-customer from their domains, so a note without them files as
 * internal.
 *
 * `?include=transcript` looks cheaper than the paged endpoint and answers
 * `TRANSCRIPT_TOO_LARGE` on exactly the long calls most worth scribing, so the
 * paged one is walked from the start.
 *
 * Plan and space visibility: `references/recorder-apis.md`.
 * Docs: https://docs.granola.ai · spec: https://docs.granola.ai/openapi.json
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
import { renderTurns, type Turn } from "./turns";

const API = "https://public-api.granola.ai/v1";

// 30 is the documented ceiling; the default is 10, and taking it would triple
// the round trips for a three-day window.
const PAGE_SIZE = 30;

const headers = (): Record<string, string> => ({
  Authorization: `Bearer ${recorderKey()}`,
});

type Attendee = { name?: string; email?: string };

type NoteSummary = {
  id: string;
  title?: string;
  created_at?: string;
};

type NoteDetail = NoteSummary & {
  attendees?: Attendee[] | null;
  summary_markdown?: string | null;
  summary_text?: string | null;
  calendar_event?: {
    invitees?: Attendee[] | null;
    organiser?: Attendee | null;
  } | null;
};

// Filled by listReady from the detail fetch it has to make anyway. notes()
// reads it rather than spending a second request on data already in hand.
const summaries = new Map<string, string | null>();

export const granola: Recorder = {
  provider: "granola",

  async listReady(from, to) {
    const notes: NoteSummary[] = [];
    const guard = pageGuard("granola");
    let cursor: string | null = null;

    do {
      guard();
      const query = new URLSearchParams({
        created_after: `${from}T00:00:00Z`,
        created_before: `${to}T23:59:59Z`,
        page_size: String(PAGE_SIZE),
      });
      if (cursor !== null) query.set("cursor", cursor);

      const page: {
        notes?: NoteSummary[];
        hasMore?: boolean;
        cursor?: string | null;
      } = await fetchJson(`${API}/notes?${query}`, { headers: headers() });

      notes.push(...(page.notes ?? []));
      cursor = page.hasMore === true ? (page.cursor ?? null) : null;
    } while (cursor !== null);

    const calls: Call[] = [];
    for (const note of notes) {
      await sleep(PACE_MS);

      let detail: NoteDetail;
      try {
        detail = await fetchJson(`${API}/notes/${note.id}`, {
          headers: headers(),
        });
      } catch (error) {
        if (error instanceof HttpError) {
          console.error(`note ${note.id} unreadable (${error.status})`);
          continue;
        }
        throw error;
      }

      summaries.set(
        note.id,
        detail.summary_markdown ?? detail.summary_text ?? null,
      );

      // `attendees` carries emails; `calendar_event.invitees` is the fallback
      // for a note whose meeting was never on a calendar the key can read.
      const attendees = [
        ...(detail.attendees ?? []),
        ...(detail.calendar_event?.invitees ?? []),
      ];

      const startAt = detail.created_at ?? note.created_at;
      if (startAt === undefined) {
        // Documented as always present. Filing it under the window's end
        // instead would put the call in the wrong day's log for good.
        console.error(`skip ${note.id}: no created_at on the note`);
        continue;
      }

      calls.push({
        id: note.id,
        startAt,
        subject: detail.title ?? note.title ?? "call",
        attendees,
      });
    }

    // No readiness signal at all, and a null `summary_markdown` is not
    // documented as a proxy for one. So the window comes back whole and a null
    // `transcript()` is what the overlapping window retries tomorrow.
    return calls;
  },

  async transcript(id) {
    const turns: Turn[] = [];
    const guard = pageGuard("granola");
    let cursor: string | null = null;

    do {
      guard();
      await sleep(PACE_MS);
      const query = new URLSearchParams({ page_size: "100" });
      if (cursor !== null) query.set("cursor", cursor);

      let page: {
        transcript?: {
          speaker?: {
            name?: string | null;
            diarization_label?: string | null;
            attribution?: string | null;
          } | null;
          text?: string;
        }[];
        hasMore?: boolean;
        cursor?: string | null;
      };
      try {
        page = await fetchJson(`${API}/notes/${id}/transcript?${query}`, {
          headers: headers(),
        });
      } catch (error) {
        if (error instanceof HttpError) {
          console.error(`transcript ${id} unavailable (${error.status})`);
          return null;
        }
        throw error;
      }

      for (const segment of page.transcript ?? []) {
        if (typeof segment.text !== "string") continue;
        // `name` only appears once a speaker has been identified;
        // `diarization_label` ("Speaker A") is what is always there.
        const speaker =
          segment.speaker?.name ??
          segment.speaker?.diarization_label ??
          undefined;
        turns.push({ speaker: speaker ?? undefined, text: segment.text });
      }

      cursor = page.hasMore === true ? (page.cursor ?? null) : null;
    } while (cursor !== null);

    return renderTurns(turns);
  },

  async notes(id) {
    const held = summaries.get(id);
    if (held !== undefined) return held;

    // Only reached when notes() is called without listReady having run — a
    // one-off by hand, not the pipeline.
    await sleep(PACE_MS);
    try {
      const detail: NoteDetail = await fetchJson(`${API}/notes/${id}`, {
        headers: headers(),
      });
      return detail.summary_markdown ?? detail.summary_text ?? null;
    } catch (error) {
      if (error instanceof HttpError) {
        console.error(`notes ${id} unavailable (${error.status})`);
        return null;
      }
      throw error;
    }
  },
};
