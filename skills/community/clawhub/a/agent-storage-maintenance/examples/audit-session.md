# Worked audit

## What the alert said

A session database crossed its size threshold a day after a rebuild had taken it
to 2.6 GB. The operator noted the agent had not worked long. That observation was
the key: growth without matching work is a defect, not capacity.

## What measurement found

Three separate problems, only one of which the alert named.

**Transcripts held copies.** One session carried 183,768 assistant events for
4,126 distinct responses — 44.5x. Repeat counts landed on 1, 2, 4, 8, 15, 30, 60,
120, 240, with several hundred responses stored 240 times. The same period
recorded over a thousand compactions and several hundred resets.

The consequence beyond disk: summing usage across those events gave 22.5 billion
tokens for one day. Counting each response once gave 611 million — **37x
smaller**. Any transcript-derived cost figure was wrong by the duplication ratio.

**The cache held three dead models.** Of four models present, the live index used
one. The largest dead set was the same model under its old local-path name, 171
MB of vectors recomputed after the reference was renamed.

```
<registry-ref>/<model>-<quant>       13,988 rows   228 MB   live
/<local-path>/<model>-<quant>.gguf   10,497 rows   171 MB   dead: same model
<remote-provider-model>               3,497 rows   109 MB   dead
<other-local-model>                   1,786 rows    39 MB   dead
```

**Abandoned trees held more than everything else combined.** Four failed
migration snapshots taken 30 to 90 minutes apart on one day, each a full
workspace, 143 GB in total. Referenced by nothing.

## What the cascade did

Truncating the two largest sessions to their last 500 lines took transcripts from
1,629 MB to 290 MB. A rebuild then took the file from 4,468 MB to 2,412 MB.

Twenty minutes later the free list had grown back past 1 GB — the index had
pruned its own entries pointing at the transcripts just truncated. The second
rebuild, after the cache prune, returned that space and more: **999 MB**.

One pass would have looked like the rebuild had barely worked.

## What was verified afterwards

Index unchanged at the same file and entry counts, `Dirty: no`, search returning
the same results, integrity check clean, services back up. The evidence that
nothing live was lost is the index counts, not the absence of errors.
