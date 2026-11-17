---
name: build-report
description: "Turn aggregated findings — news, monitoring, research — into a report someone will actually read: a chat digest, a Markdown doc, or a self-contained HTML dashboard. Use when a task ends with a pile of data and the risk that nobody reads the writeup."
version: 1.0.0
license: MIT
metadata:
  tags: [reporting, dashboard, digest, news, data-aggregation, html, markdown]
---

# Turning aggregated findings into a report people read

Collecting the data is the easy half. A report nobody reads is worth less than
no report at all — it teaches whoever assigned it that they don't need to
check the next one either. What follows is what decides whether the second
one gets read.

## Before writing anything: what actually changed

The single biggest failure mode of a recurring report is repeating what's
stable and burying what's new inside it. Before drafting:

- Diff against the last version, not the raw source. If a section hasn't
  changed, say "unchanged" in one line — do not re-describe it at the same
  length as something new.
- Sort by what the reader needs to act on, not by source or chronology. A
  reader skims top to bottom once; the first three lines are the only ones
  guaranteed to be read.
- If there's nothing worth reporting, say that in one line. A padded report
  trains the reader to skim past all of them, including the ones that
  matter.

## Pick the format for where it's read, not for what looks impressive

Three shapes, in order of how often each is actually the right one:

1. **A chat message.** Five to seven lines, plain text, one clear point per
   line. Correct for anything read on a phone between other things — which
   is most recurring reports. Do not reach for HTML because it exists.
2. **A Markdown document.** For something that needs headings, a table, or
   links, and will be opened deliberately rather than glanced at — a weekly
   roundup, a comparison. Still short: a table beats three paragraphs
   describing the same numbers.
3. **A self-contained HTML page.** Only when something genuinely benefits
   from layout — several data series, or something meant to be shared as a
   link. Single file, inline CSS, no external requests: a page that depends
   on a CDN being reachable is a page that's sometimes blank. Template
   below.

Reaching for the fanciest format by default is the second most common
failure, right after skipping the diff.

## Every claim needs a source, in the report itself

Not "sources available on request" — the specific link or file sits next to
the specific line. A number with nowhere it came from is not a finding, it's
a guess wearing a finding's clothes. If a source can't be reached, say the
section is thin rather than filling it with something plausible-sounding.

## Separate what happened from what you make of it

The two are different kinds of claim and erode trust differently if mixed:
"the API raised its price 40%" is a fact; "they're betting nobody
re-benchmarks" is a read on it. Label the second explicitly — a reader who
can't tell which is which stops trusting either.

## A self-contained HTML dashboard, minimal and dependency-free

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{{ report title }}</title>
<style>
  :root { color-scheme: light dark; }
  body { font: 15px/1.5 -apple-system, system-ui, sans-serif; max-width: 720px;
         margin: 2rem auto; padding: 0 1rem; }
  h1 { font-size: 1.3rem; margin-bottom: .25rem; }
  .meta { color: #888; font-size: .85rem; margin-bottom: 1.5rem; }
  .stat-row { display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 1.5rem; }
  .stat { border: 1px solid #8883; border-radius: 8px; padding: .75rem 1rem; }
  .stat b { display: block; font-size: 1.4rem; }
  .stat span { font-size: .8rem; color: #888; }
  .item { border-top: 1px solid #8883; padding: .75rem 0; }
  .item .src { font-size: .8rem; color: #888; }
  .unchanged { opacity: .55; font-size: .85rem; }
</style>
</head>
<body>
  <h1>{{ report title }}</h1>
  <p class="meta">{{ date }} · covers {{ window, e.g. "last 24h" }}</p>
  <div class="stat-row">
    <div class="stat"><b>{{ number }}</b><span>{{ what it counts }}</span></div>
  </div>
  <div class="item">
    <div>{{ what happened, one line }}</div>
    <div class="src"><a href="{{ url }}">{{ source name }}</a></div>
  </div>
  <p class="unchanged">{{ what stayed the same, one line, not expanded }}</p>
</body>
</html>
```

No JS, no charting library, no font import — each is something that can fail
silently when the page is opened somewhere without internet, and a dashboard
nobody can open is worse than the chat message it replaced.

## What goes wrong

**The report grows every cycle and gets read less each time.** Almost always
means the diff-against-last-time step was skipped — stable sections
re-described in full instead of collapsed to "unchanged."

**A number with no source next to it.** The most common way a report stops
being trusted. If you can't find where a number came from, cut the number
rather than keep it unsourced.

**A stat with no unit, or a chart with no axis label.** Obvious in the source
data, meaningless on the page once separated from it. If a number needs the
surrounding sentence to mean anything, put the unit on the number itself.

**Opinion presented as if it were the finding.** "X is concerning" is not a
finding; "X changed by this much, for this reason we could confirm" is. Say
which one is being given.

## Getting it to the reader

A report that exists only inside the agent's session was never delivered. How
this works is engine-specific; the pattern below is Hermes, checked on a
running pod rather than read from documentation.

**See what you can actually deliver to, first.**

```
hermes send --list
```

If it answers "no messaging platforms configured", nothing can be delivered
yet — a channel has to be connected before any of the rest of this matters.
Checking first turns a silent non-delivery into a clear one.

**Send the report as the message.**

```
hermes send --to telegram --file /opt/data/workspace/report.md
hermes send --to discord:#ops --subject "[weekly]" --file report.md
```

Targets are `platform`, `platform:chat_id`, or `platform:#channel-name`. For
bot-token platforms this needs neither a model nor a running gateway, so it
works from a cron job — which is what a recurring report usually is.

**Send a file as an attachment.**

```
hermes send --to telegram "MEDIA:/opt/data/workspace/dashboard.html"
```

`--file` reads the message *text* from a path; `MEDIA:<path>` in the message
attaches the file itself. Mixing these two up sends the raw HTML of your
dashboard into the chat as a wall of text.

**Keep the file on the persistent disk**, not in `/tmp`. `/opt/data` survives
restarts, and the previous report is what the next one diffs against — the
first section of this skill is impossible without somewhere to keep it.

**One thing to know before promising a link:** on a pod like this there is no
public URL for a file you write. The only HTTP surface is the dashboard, and
it sits behind authentication. A report that must be shareable as a link needs
somewhere else to host it; an attachment is what actually works out of the box.

## What this skill doesn't cover

The delivery commands above are Hermes. Other engines have their own way, and
this file does not attempt to guess at them — an invented command is worse
than an absent one. Find the equivalent of `send --list` for whatever you are
running before designing around delivery.

Scheduling — how the report gets triggered daily or weekly — is also outside
this file.

One trap worth naming even though it belongs to scheduling: a report headed
"today" is written in the pod's timezone, which is often not the reader's. A
daily digest that arrives at 07:00 for the agent and 23:00 the previous day
for the person reading it is wrong in a way nobody reports as a bug — they
just stop trusting the dates. Set the pod's timezone to the reader's, or put
the offset in the report itself.
