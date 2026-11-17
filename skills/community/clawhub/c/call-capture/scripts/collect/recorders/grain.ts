/**
 * Grain. Written from the vendor's own developer reference, not yet run
 * against a live workspace: check it with `--dry-run` before you deploy it.
 *
 * Two headers, and `Public-Api-Version` is not optional: omit it and the
 * request is rejected rather than defaulted. It is pinned below on purpose,
 * since a floating version would change response shapes under a pipeline
 * nobody is watching. The list is a POST despite being a read, and `include`
 * decides whether participants come back at all — without their emails the
 * pipeline files every call as internal.
 *
 * Grain's reference transposes `before_datetime` and `after_datetime` against
 * what their names say. They are used here the way the names read, so if
 * `--dry-run` lists a window you did not ask for, swap the two values.
 *
 * Token scope and plan requirements: `references/recorder-apis.md`.
 * Docs: https://developers.grain.com/
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

const API = "https://api.grain.com/_/public-api/v2";

// Pinned, not floating: this is the contract the field names below were read
// against.
const API_VERSION = "2025-10-31";

const headers = (): Record<string, string> => ({
  Authorization: `Bearer ${recorderKey()}`,
  "Public-Api-Version": API_VERSION,
  "Content-Type": "application/json",
});

type Recording = {
  id?: string;
  title?: string;
  start_datetime?: string;
  participants?:
    { name?: string | null; email?: string | null; scope?: string }[] | null;
  ai_summary?: { text?: string | null } | null;
};

const summaries = new Map<string, string | null>();

export const grain: Recorder = {
  provider: "grain",

  async listReady(from, to) {
    const calls: Call[] = [];
    const guard = pageGuard("grain");
    let cursor: string | null = null;

    do {
      guard();
      const body: Record<string, unknown> = {
        filter: {
          after_datetime: `${from}T00:00:00Z`,
          before_datetime: `${to}T23:59:59Z`,
        },
        // `participants` is what makes the internal-domain filter work at all
        // and `ai_summary` is the notes fallback — both free here, where a
        // second request per call would not be. `attendance` and
        // `private_notes` are personal-token only.
        include: { participants: true, ai_summary: true },
      };
      if (cursor !== null) body["cursor"] = cursor;

      const page: { recordings?: Recording[]; cursor?: string | null } =
        await fetchJson(`${API}/recordings`, {
          method: "POST",
          headers: headers(),
          body: JSON.stringify(body),
        });

      for (const recording of page.recordings ?? []) {
        if (
          recording.id === undefined ||
          recording.start_datetime === undefined
        )
          continue;

        summaries.set(recording.id, recording.ai_summary?.text ?? null);
        calls.push({
          id: recording.id,
          startAt: recording.start_datetime,
          subject: recording.title ?? "call",
          // `scope` is internal | external | unknown and is deliberately not
          // read: that judgement stays with the pipeline's own domain check.
          attendees: (recording.participants ?? []).map((participant) => ({
            name: participant.name ?? undefined,
            email: participant.email ?? undefined,
          })),
        });
      }

      cursor = page.cursor ?? null;
      if (cursor !== null) await sleep(PACE_MS);
    } while (cursor !== null);

    // No readiness flag. A null `transcript` is what "still processing" looks
    // like, and tomorrow's overlapping window is the retry.
    return calls;
  },

  async transcript(id) {
    await sleep(PACE_MS);

    let segments: {
      speaker?: string | null;
      text?: string | null;
    }[];
    try {
      // A BARE ARRAY, no envelope. The `.txt`, `.vtt` and `.srt` variants of
      // this path return formatted text instead, which is not what this wants.
      segments = await fetchJson(`${API}/recordings/${id}/transcript`, {
        headers: headers(),
      });
    } catch (error) {
      if (error instanceof HttpError) {
        console.error(`transcript ${id} unavailable (${error.status})`);
        return null;
      }
      throw error;
    }

    if (!Array.isArray(segments)) return null;

    const turns: Turn[] = [];
    for (const segment of segments) {
      if (typeof segment.text !== "string") continue;
      // `speaker` is the name directly — one of the few recorders that does
      // not make you join against a participant id.
      turns.push({ speaker: segment.speaker ?? undefined, text: segment.text });
    }

    return renderTurns(turns);
  },

  async notes(id) {
    // Included on the list response, so this is a read of what listReady
    // already holds.
    return summaries.get(id) ?? null;
  },
};
