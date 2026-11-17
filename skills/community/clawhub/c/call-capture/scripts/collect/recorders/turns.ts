/**
 * One transcript format, whoever recorded the call: `**Name:** text`, one
 * paragraph per turn, consecutive segments from the same speaker joined.
 *
 * The joining is not cosmetic. Recorders segment wildly differently — Granola
 * and Gong hand back whole monologues, Circleback and Grain hand back
 * sentences — so unjoined, the same call reads as 40 lines from one recorder
 * and 400 from another, and the agent's per-run cap is spent on reading it.
 *
 * Beside the adapters rather than in `recorder.ts` because it is a convenience
 * they share, not part of the contract: an adapter with real reason to render
 * differently does not import it.
 */
export type Turn = {
  speaker?: string | undefined;
  text: string;
};

/** Markdown, or null when nothing had any text in it. */
export function renderTurns(turns: Turn[]): string | null {
  const merged: { speaker: string; parts: string[] }[] = [];

  for (const turn of turns) {
    const text = turn.text.trim();
    if (text === "") continue;
    const speaker =
      turn.speaker !== undefined && turn.speaker.trim() !== ""
        ? turn.speaker.trim()
        : "Speaker";

    const last = merged[merged.length - 1];
    if (last !== undefined && last.speaker === speaker) last.parts.push(text);
    else merged.push({ speaker, parts: [text] });
  }

  if (merged.length === 0) return null;
  return merged
    .map((turn) => `**${turn.speaker}:** ${turn.parts.join(" ")}`)
    .join("\n\n");
}
