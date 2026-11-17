/**
 * Modjo. Written from the vendor's own OpenAPI document, not yet run against a
 * live workspace: check it with `--dry-run` before you deploy it.
 *
 * The published base URL is wrong: the spec declares
 * `https://api.modjo.ai//v2`, with a double slash, and that path 404s — so a
 * generated client is broken out of the box and the single slash below is what
 * answers.
 *
 * `expand` SWAPS fields rather than adding them: `contactIds` without it,
 * `contacts` with it. It is always passed so the response keeps one shape.
 *
 * An empty `data` array is a call still processing, not a call where nobody
 * spoke, which is why `listReady` filters on `status` and the empty array is
 * retried by the window. A transcript already reaped by retention answers
 * **410 Gone** rather than 404, and that is terminal.
 *
 * Docs: https://api.modjo.ai/v2/docs
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

const API = "https://api.modjo.ai/v2";

// The documented maximum; the default is 25.
const PAGE_SIZE = 100;

const headers = (): Record<string, string> => ({
  Authorization: `Bearer ${recorderKey()}`,
});

type Person = {
  name?: string | null;
  email?: string | null;
  firstName?: string | null;
  lastName?: string | null;
};

type ModjoCall = Record<string, unknown> & {
  id?: number | string;
  contacts?: Person[] | null;
  users?: Person[] | null;
  transcriptRetentionStatus?: string;
  status?: string;
};

const START_KEYS = ["startDate", "start_date", "date", "createdOn"] as const;
const TITLE_KEYS = ["title", "name", "subject"] as const;

function fullName(person: Person): string | undefined {
  if (typeof person.name === "string" && person.name !== "") return person.name;
  const parts = [person.firstName, person.lastName].filter(
    (part): part is string => typeof part === "string" && part !== "",
  );
  return parts.length > 0 ? parts.join(" ") : undefined;
}

export const modjo: Recorder = {
  provider: "modjo",

  async listReady(from, to) {
    const calls: Call[] = [];

    const guard = pageGuard("modjo");

    for (let page = 1; ; page++) {
      guard();
      const query = new URLSearchParams({
        from: `${from}T00:00:00Z`,
        to: `${to}T23:59:59Z`,
        page: String(page),
        size: String(PAGE_SIZE),
        // Always both, always the same two: see the note on `expand` above.
        expand: "contacts,users",
      });

      const body: {
        data?: ModjoCall[];
        pagination?: { page?: number; size?: number; total?: number };
      } = await fetchJson(`${API}/calls?${query}`, { headers: headers() });

      const rows = body.data ?? [];
      for (const call of rows) {
        if (call.id === undefined) continue;
        // The only readiness signal Modjo gives: a transcript already reaped
        // by retention will answer 410, and one still being made answers with
        // an empty array.
        if (call.transcriptRetentionStatus === "deleted") continue;

        const startAt = pickTimestamp(call, START_KEYS);
        if (startAt === undefined) {
          console.error(
            `skip ${String(call.id)}: no start timestamp on the call ` +
              `(none of ${START_KEYS.join(", ")}) — see references/recorder-apis.md`,
          );
          continue;
        }

        // Array membership IS Modjo's internal/external flag: `contacts`
        // external, `users` the team. Both pass through so the pipeline's
        // domain rule decides.
        const attendees = [...(call.contacts ?? []), ...(call.users ?? [])].map(
          (person) => ({
            name: fullName(person),
            email: person.email ?? undefined,
          }),
        );

        calls.push({
          id: String(call.id),
          startAt,
          subject: pickString(call, TITLE_KEYS) ?? "call",
          attendees,
        });
      }

      // An empty page is the end. `pagination.total` is an additional stop
      // when it is there rather than the only one: defaulting it to what this
      // page held ended the walk after page 1 whenever the field was missing
      // or renamed, and a truncated window looks exactly like a quiet one.
      if (rows.length === 0) break;
      const total = body.pagination?.total;
      if (total !== undefined && page * PAGE_SIZE >= total) break;
      await sleep(PACE_MS);
    }

    return calls;
  },

  async transcript(id) {
    await sleep(PACE_MS);

    let payload: {
      data?: {
        content?: string | null;
        speaker?: { name?: string | null; type?: string } | null;
      }[];
    };
    try {
      payload = await fetchJson(`${API}/calls/${id}/transcript`, {
        headers: headers(),
      });
    } catch (error) {
      if (error instanceof HttpError) {
        // 410 Gone is retention, not a transient failure. Reported the same
        // way because the outcome is the same: nothing to capture.
        console.error(`transcript ${id} unavailable (${error.status})`);
        return null;
      }
      throw error;
    }

    const turns: Turn[] = [];
    for (const segment of payload.data ?? []) {
      // The text field is `content`, not `text`.
      if (typeof segment.content !== "string") continue;
      turns.push({
        speaker: segment.speaker?.name ?? undefined,
        text: segment.content,
      });
    }

    // Null rather than an empty string when the array was empty: that is a
    // call still processing, and the pipeline's next run retries it.
    return renderTurns(turns);
  },

  async notes(id) {
    await sleep(PACE_MS);

    let payload: {
      data?: { answer?: string | null; templateTitle?: string | null }[];
    };
    try {
      // One entry per configured summary template, and `answer` is null until
      // that template's summary has been generated.
      payload = await fetchJson(`${API}/calls/${id}/summaries`, {
        headers: headers(),
      });
    } catch (error) {
      if (error instanceof HttpError) {
        console.error(`notes ${id} unavailable (${error.status})`);
        return null;
      }
      throw error;
    }

    const sections: string[] = [];
    for (const summary of payload.data ?? []) {
      if (typeof summary.answer !== "string" || summary.answer.trim() === "")
        continue;
      const heading = summary.templateTitle ?? "Summary";
      sections.push(`**${heading}**\n\n${summary.answer.trim()}`);
    }

    return sections.length > 0 ? sections.join("\n\n") : null;
  },
};
