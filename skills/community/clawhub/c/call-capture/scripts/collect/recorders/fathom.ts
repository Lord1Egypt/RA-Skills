/**
 * Fathom. Written from the vendor's own API reference, not yet run against a
 * live workspace: check it with `--dry-run` before you deploy it.
 *
 * The API is on every plan including the free one, which makes this the
 * cheapest of the recorders here to try the pipeline against.
 *
 * Auth is `X-Api-Key`, not `Authorization` — a Bearer header fails as
 * unauthenticated however correct the key is. And the rate limit is two
 * limits: 60 requests a minute in general but 30 for "heavy" ones, which is
 * every `/recordings/…` call, hence the 2s pace floor below rather than the
 * pipeline's default second.
 *
 * Docs: https://developers.fathom.ai/quickstart
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
import { pickString, pickTimestamp } from "./fields";
import { renderTurns, type Turn } from "./turns";

const API = "https://api.fathom.ai/external/v1";

// Every /recordings endpoint counts against the heavy limit of 30/minute.
const HEAVY_PACE_MS = Math.max(PACE_MS, 2000);

const headers = (): Record<string, string> => ({
  "X-Api-Key": recorderKey(),
});

type Meeting = Record<string, unknown> & {
  recording_id?: number | string;
  calendar_invitees?: { name?: string; email?: string }[] | null;
};

// Documented as filtering on `created_at`; which timestamp the meeting object
// itself carries is not in the reference, so the recording's own start is
// preferred and the schedule and the creation time are the fallbacks.
const START_KEYS = [
  "recording_start_time",
  "scheduled_start_time",
  "started_at",
  "start_time",
  "created_at",
] as const;

const TITLE_KEYS = ["title", "meeting_title", "name", "subject"] as const;

export const fathom: Recorder = {
  provider: "fathom",

  async listReady(from, to) {
    const meetings: Meeting[] = [];
    const guard = pageGuard("fathom");
    let cursor: string | null = null;

    do {
      guard();
      const query = new URLSearchParams({
        created_after: `${from}T00:00:00Z`,
        created_before: `${to}T23:59:59Z`,
      });
      if (cursor !== null) query.set("cursor", cursor);

      const page: { items?: Meeting[]; next_cursor?: string | null } =
        await fetchJson(`${API}/meetings?${query}`, { headers: headers() });

      meetings.push(...(page.items ?? []));
      cursor = page.next_cursor ?? null;
      if (cursor !== null) await sleep(PACE_MS);
    } while (cursor !== null);

    // No page size is exposed, so a busy window is several round trips.
    // include_transcript and include_summary would inline the bodies but make
    // the whole request heavy, and are refused for OAuth-connected apps.
    const calls: Call[] = [];
    for (const meeting of meetings) {
      const id = meeting.recording_id;
      if (id === undefined || id === null) continue;

      const startAt = pickTimestamp(meeting, START_KEYS);
      if (startAt === undefined) {
        console.error(
          `skip recording ${String(id)}: no start timestamp on the meeting ` +
            `(none of ${START_KEYS.join(", ")}) — see references/recorder-apis.md`,
        );
        continue;
      }

      calls.push({
        // An integer in the response, a string everywhere here: it round-trips
        // through the `source:` line, and that makes it text.
        id: String(id),
        startAt,
        subject: pickString(meeting, TITLE_KEYS) ?? "call",
        // `is_external` on each invitee is a real flag and is passed over:
        // the pipeline's one domain rule decides, or two recorders end up
        // disagreeing about what an internal call is.
        attendees: (meeting.calendar_invitees ?? []).map((invitee) => ({
          name: invitee.name,
          email: invitee.email,
        })),
      });
    }

    // No readiness flag. A still-processing transcript comes back null, which
    // the overlapping window picks up tomorrow.
    return calls;
  },

  async transcript(id) {
    await sleep(HEAVY_PACE_MS);

    let payload: {
      transcript?: {
        speaker?: { display_name?: string | null } | null;
        text?: string;
      }[];
    };
    try {
      payload = await fetchJson(`${API}/recordings/${id}/transcript`, {
        headers: headers(),
      });
    } catch (error) {
      if (error instanceof HttpError) {
        console.error(`transcript ${id} unavailable (${error.status})`);
        return null;
      }
      throw error;
    }

    // `?destination_url=` on this endpoint flips it to async delivery and
    // returns nothing useful inline. Never pass it here.
    const turns: Turn[] = [];
    for (const segment of payload.transcript ?? []) {
      if (typeof segment.text !== "string") continue;
      turns.push({
        speaker: segment.speaker?.display_name ?? undefined,
        text: segment.text,
      });
    }

    return renderTurns(turns);
  },

  async notes(id) {
    await sleep(HEAVY_PACE_MS);

    let payload: {
      summary?: { markdown_formatted?: string | null } | null;
    };
    try {
      payload = await fetchJson(`${API}/recordings/${id}/summary`, {
        headers: headers(),
      });
    } catch (error) {
      if (error instanceof HttpError) {
        console.error(`notes ${id} unavailable (${error.status})`);
        return null;
      }
      throw error;
    }

    // Always English, whatever language the call was in. Worth knowing before
    // you reorder the fallback so notes are preferred over transcripts.
    return payload.summary?.markdown_formatted ?? null;
  },
};
