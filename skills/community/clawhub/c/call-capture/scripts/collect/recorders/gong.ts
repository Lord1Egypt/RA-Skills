/**
 * Gong. Written from the vendor's own API reference, not yet run against a
 * live workspace: check it with `--dry-run` before you deploy it.
 *
 * `CALL_RECORDER_API_KEY` holds `<accessKey>:<accessKeySecret>`, base64'd into
 * a Basic header here. The base URL is per company: regional instances are
 * `https://<region>.api.gong.io/v2`, so set `CALL_RECORDER_API_BASE` when
 * yours is not the common one.
 *
 * Speaker names are a join, not a field. The transcript carries `speakerId`
 * and never a name, and the mapping lives on the call's `parties`, which only
 * the list request asks for — so `listReady` keeps the party list and
 * `transcript` reads it.
 *
 * Every field under `content` arrives only when its `contentSelector` flag was
 * set AND Gong generated it, so a missing key never means "empty"; Gong also
 * adds JSON fields without warning, so responses are read defensively rather
 * than destructured.
 *
 * Scopes and quotas: `references/recorder-apis.md`.
 * Docs: https://help.gong.io/apidocs/introduction-2
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
import { renderTurns, type Turn } from "./turns";

const API =
  process.env["CALL_RECORDER_API_BASE"]?.replace(/\/+$/, "") ??
  "https://api.gong.io/v2";

const headers = (): Record<string, string> => {
  const [accessKey, secret] = recorderKeyPair("<accessKey>:<accessKeySecret>");
  return {
    Authorization: `Basic ${Buffer.from(`${accessKey}:${secret}`).toString("base64")}`,
    "Content-Type": "application/json",
  };
};

type Party = {
  id?: string;
  name?: string;
  emailAddress?: string;
  speakerId?: string;
  affiliation?: string;
};

type GongCall = {
  metaData?: {
    id?: string;
    started?: string;
    title?: string;
  };
  parties?: Party[];
  content?: Record<string, unknown>;
};

// speakerId -> name, and the AI content, both kept from the list request that
// had to fetch them anyway.
const speakerNames = new Map<string, Map<string, string>>();
const contents = new Map<string, Record<string, unknown>>();

function textsOf(value: unknown): string[] {
  if (typeof value === "string") return [value];
  if (!Array.isArray(value)) return [];
  const out: string[] = [];
  for (const item of value) {
    if (typeof item === "string") {
      out.push(item);
      continue;
    }
    if (item === null || typeof item !== "object") continue;
    const record = item as Record<string, unknown>;
    const text = record["text"] ?? record["title"] ?? record["section"];
    if (typeof text === "string") out.push(text);
    out.push(...textsOf(record["items"]));
  }
  return out;
}

export const gong: Recorder = {
  provider: "gong",

  async listReady(from, to) {
    const calls: Call[] = [];
    const guard = pageGuard("gong");
    let cursor: string | null = null;

    do {
      guard();
      const body: Record<string, unknown> = {
        filter: {
          // Both are required on this endpoint. For web-conference calls the
          // date is the SCHEDULED time, and `toDateTime` is exclusive — which
          // is why the pipeline's `to` is pushed to the end of the day.
          fromDateTime: `${from}T00:00:00Z`,
          toDateTime: `${to}T23:59:59Z`,
        },
        contentSelector: {
          exposedFields: {
            parties: true,
            content: { brief: true, keyPoints: true, outline: true },
            // `media` is not asked for: it needs a third scope, and asking
            // without the grant fails the whole list request.
          },
        },
      };
      if (cursor !== null) body["cursor"] = cursor;

      const page: {
        calls?: GongCall[];
        records?: { cursor?: string | null };
      } = await fetchJson(`${API}/calls/extensive`, {
        method: "POST",
        headers: headers(),
        body: JSON.stringify(body),
      });

      for (const call of page.calls ?? []) {
        const id = call.metaData?.id;
        const started = call.metaData?.started;
        if (id === undefined || started === undefined) continue;

        const names = new Map<string, string>();
        for (const party of call.parties ?? []) {
          // speakerId is present only on parties who actually spoke.
          if (party.speakerId !== undefined && party.name !== undefined) {
            names.set(String(party.speakerId), party.name);
          }
        }
        speakerNames.set(id, names);
        if (call.content !== undefined) contents.set(id, call.content);

        calls.push({
          // A numeric string of up to 20 digits: it overflows a JS number, so
          // it stays a string from here to the `source:` line.
          id: String(id),
          startAt: started,
          subject: call.metaData?.title ?? "call",
          attendees: (call.parties ?? []).map((party) => ({
            name: party.name,
            email: party.emailAddress,
          })),
        });
      }

      // The cursor is PRESENT ONLY WHEN more records exist, so its absence is
      // the end of the window rather than a page of nothing.
      cursor = page.records?.cursor ?? null;
      if (cursor !== null) await sleep(PACE_MS);
    } while (cursor !== null);

    // No readiness flag of any kind, so the window comes back whole and a
    // still-processing call answers `transcript` with nothing.
    return calls;
  },

  async transcript(id) {
    await sleep(PACE_MS);

    let payload: {
      callTranscripts?: {
        callId?: string;
        transcript?: {
          speakerId?: string;
          sentences?: { text?: string }[];
        }[];
      }[];
    };
    try {
      payload = await fetchJson(`${API}/calls/transcript`, {
        method: "POST",
        headers: headers(),
        body: JSON.stringify({ filter: { callIds: [id] } }),
      });
    } catch (error) {
      if (error instanceof HttpError) {
        console.error(`transcript ${id} unavailable (${error.status})`);
        return null;
      }
      throw error;
    }

    const monologues = payload.callTranscripts?.[0]?.transcript ?? [];
    const names = speakerNames.get(id) ?? new Map<string, string>();

    // `transcript[]` is a list of MONOLOGUES, not sentences: one entry is one
    // speaker's turn and holds its own `sentences[]`.
    const turns: Turn[] = monologues.map((monologue) => ({
      speaker:
        monologue.speakerId === undefined
          ? undefined
          : names.get(String(monologue.speakerId)),
      text: (monologue.sentences ?? [])
        .map((sentence) => sentence.text ?? "")
        .join(" "),
    }));

    return renderTurns(turns);
  },

  async notes(id) {
    // No notes endpoint: the AI content arrives on the list request, so this
    // reads what listReady holds and is null if it never ran.
    const content = contents.get(id);
    if (content === undefined) return null;

    const sections: string[] = [];
    const brief = content["brief"];
    if (typeof brief === "string" && brief.trim() !== "") {
      sections.push(brief.trim());
    }
    for (const [key, heading] of [
      ["keyPoints", "Key points"],
      ["outline", "Outline"],
    ] as const) {
      const texts = textsOf(content[key]);
      if (texts.length > 0) {
        sections.push(
          `**${heading}**\n\n${texts.map((text) => `- ${text}`).join("\n")}`,
        );
      }
    }

    return sections.length > 0 ? sections.join("\n\n") : null;
  },
};
