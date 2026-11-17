# Recall

The other three modes write. This one only reads.

It runs when someone asks how things have been going, what happened during some stretch, what is still open, or what came out of a particular thread. Nothing is scheduled here — recall is always a direct question, and the answer is always the record rather than a reconstruction of it.

## Read in order, stop early

| Question | Read |
|---|---|
| what's going on right now, what's still open | `inner-life/state.md` |
| how the last few weeks went | the weekly rollups in `inner-life/journal/weekly/` |
| a named day, or a topic followed across days | the daily entries |
| what has the night thinking been circling | the titles in `inner-life/dreams/` |

Start at the top and stop at the first level that answers the question. `state.md` is four short sections and it is current; a rollup is half a page and covers a week. Reading forty daily entries to answer *how has it been lately* is the common failure here, and it produces a worse answer than the rollup does, not a better one.

Go down a level only when the question actually needs it — a specific date, a thread name, a claim in the rollup that needs its source.

## Answering

**Dates, not ratings.** The same rule that governs writing governs reading back. *The last real conversation was July 22, and there have been three deploy failures since* is the answer. *Engagement has been low* is not — it is a score wearing a sentence.

**Report the record, don't interpret the person.** The journal is a record of how the work went. Answering with a characterisation of the user, their mood, or their habits is a different thing than answering with what happened, and this skill does the second one.

**Gaps are information, and they are not to be filled.** A week with no entries means nothing was written that week. It does not mean the week was quiet, and it must not be smoothed over into one. Say plainly that nothing was written between the dates in question, and stop there.

**Quote sparingly.** Pull the lines that answer the question. A read-back that reproduces whole entries buries the answer in material nobody asked for.

**Nothing is a valid answer.** *Nothing was recorded in that period* is a complete response. Padding it with what probably happened turns the record into a source of things that never occurred.

## Finding things

Daily entries carry `date`, `mood`, and `threads` in frontmatter precisely so they can be found without opening all of them. Search on `threads` for a topic, on `date` for a period. Dreams are found by their titles, which is why the titles are required to be specific.

## Recall does not write

Reading back is not an occasion to update state, refresh the memory summary, or prune anything. Those belong to the evening run. If the read-back turns up something worth recording, say so and let the user decide — a question about the past is not permission to add to it.

## Who is asking

This is the only mode that pulls the local record into a live conversation. Everything under `inner-life/` was written on the assumption that it stays on disk, which is why the writing rules there are looser than the rules for the memory summary.

So the ordinary care applies: answer the question that was asked, from the entries that bear on it. Don't read out unrelated stretches of the journal because they happened to be nearby, and on a shared host, don't assume the person asking is the person the record was kept for.
