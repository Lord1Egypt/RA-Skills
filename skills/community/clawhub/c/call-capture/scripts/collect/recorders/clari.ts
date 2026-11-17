/**
 * Clari Copilot, formerly Wingman. Written from the vendor's own OpenAPI
 * document, not yet run against a live workspace: check it with `--dry-run`
 * before you deploy it.
 *
 * Two values, neither of them `Authorization`: `CALL_RECORDER_API_KEY` holds
 * `<key>:<password>` for the `X-Api-Key` and `X-Api-Password` headers.
 *
 * `status` is a real readiness signal, and filtering on the two values that
 * mean "there is something to read" rather than excluding the twelve failures
 * survives Clari adding a thirteenth. Transcripts are not on the list, but
 * `/call-details` carries the transcript, the summary AND the participant
 * arrays, so one request per call serves both methods.
 *
 * The full status list and the weekly request cap are in
 * `references/recorder-apis.md`.
 * Docs: https://api-doc.copilot.clari.com/
 */
import {
  fetchJson,
  HttpError,
  PACE_MS,
  pageGuard,
  recorderKeyPair,
  sleep,
  type Call,
  type Recorder,
} from "../recorder";
import { pickString, pickTimestamp } from "./fields";
import { renderTurns, type Turn } from "./turns";

const API = "https://rest-api.copilot.clari.com";

// The documented maximum; the default is 25.
const PAGE_SIZE = 100;

const READY = new Set(["PROCESSED", "POST_PROCESSING_DONE"]);

const headers = (): Record<string, string> => {
  const [key, password] = recorderKeyPair("<apiKey>:<apiPassword>");
  return { "X-Api-Key": key, "X-Api-Password": password };
};

type Participant = {
  name?: string | null;
  email?: string | null;
  userEmail?: string | null;
  personId?: number | string | null;
};

type CopilotCall = Record<string, unknown> & {
  id?: string;
  status?: string;
  users?: Participant[] | null;
  externalParticipants?: Participant[] | null;
  joinedParticipants?: Participant[] | null;
};

type CallDetail = {
  call?: CopilotCall & {
    transcript?: { text?: string | null; personId?: number | string | null }[];
    summary?: { full_summary?: string | null } | null;
  };
};

const START_KEYS = [
  "time",
  "startTime",
  "start_time",
  "scheduled_start_time",
  "call_time",
] as const;

const TITLE_KEYS = ["title", "name", "subject"] as const;

const details = new Map<string, CallDetail["call"]>();

function participantsOf(call: CopilotCall): Participant[] {
  return [
    ...(call.users ?? []),
    ...(call.externalParticipants ?? []),
    ...(call.joinedParticipants ?? []),
  ];
}

async function detail(id: string): Promise<CallDetail["call"] | null> {
  const held = details.get(id);
  if (held !== undefined) return held;

  await sleep(PACE_MS);
  try {
    const payload: CallDetail = await fetchJson(
      `${API}/call-details?id=${encodeURIComponent(id)}`,
      { headers: headers() },
    );
    const call = payload.call;
    if (call === undefined) return null;
    details.set(id, call);
    return call;
  } catch (error) {
    if (error instanceof HttpError) {
      console.error(`call ${id} unavailable (${error.status})`);
      return null;
    }
    throw error;
  }
}

export const clari: Recorder = {
  provider: "clari",

  async listReady(from, to) {
    const calls: Call[] = [];
    const guard = pageGuard("clari");

    for (let skip = 0; ; skip += PAGE_SIZE) {
      guard();
      const query = new URLSearchParams({
        filterTimeGt: `${from}T00:00:00Z`,
        filterTimeLt: `${to}T23:59:59Z`,
        limit: String(PAGE_SIZE),
        skip: String(skip),
        includePagination: "true",
      });

      const body: {
        calls?: CopilotCall[];
        pagination?: { hasMore?: boolean; nextPageSkip?: number };
      } = await fetchJson(`${API}/calls?${query}`, { headers: headers() });

      for (const call of body.calls ?? []) {
        if (call.id === undefined) continue;
        if (!READY.has(call.status ?? "")) continue;

        const startAt = pickTimestamp(call, START_KEYS);
        if (startAt === undefined) {
          console.error(
            `skip ${call.id}: no start timestamp on the call ` +
              `(none of ${START_KEYS.join(", ")}) — see references/recorder-apis.md`,
          );
          continue;
        }

        // The split between the three arrays is Clari's own internal/external
        // judgement. All three are passed through so the pipeline's one domain
        // rule decides, not a vendor's.
        calls.push({
          id: call.id,
          startAt,
          subject: pickString(call, TITLE_KEYS) ?? "call",
          attendees: participantsOf(call).map((participant) => ({
            name: participant.name ?? undefined,
            email: participant.email ?? participant.userEmail ?? undefined,
          })),
        });
      }

      // Private calls are excluded unless `includePrivate=true`, which is
      // deliberately not passed: a call someone marked private is not one to
      // commit to a repository.
      if (body.pagination?.hasMore !== true) break;
      await sleep(PACE_MS);
    }

    return calls;
  },

  async transcript(id) {
    const call = await detail(id);
    if (call === undefined || call === null) return null;

    // `personId` is an integer, never a name. The mapping is the participant
    // arrays on this same response, which is why one request serves both.
    const names = new Map<string, string>();
    for (const participant of participantsOf(call)) {
      if (
        participant.personId !== undefined &&
        participant.personId !== null &&
        typeof participant.name === "string"
      ) {
        names.set(String(participant.personId), participant.name);
      }
    }

    const turns: Turn[] = [];
    for (const segment of call.transcript ?? []) {
      if (typeof segment.text !== "string") continue;
      turns.push({
        speaker:
          segment.personId === undefined || segment.personId === null
            ? undefined
            : names.get(String(segment.personId)),
        text: segment.text,
      });
    }

    return renderTurns(turns);
  },

  async notes(id) {
    const call = await detail(id);
    const summary = call?.summary?.full_summary;
    return typeof summary === "string" && summary.trim() !== ""
      ? summary.trim()
      : null;
  },
};
