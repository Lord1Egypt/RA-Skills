---
name: data-storycraft
license: MIT-0
description: Applies the Storytelling with Data method (Cole Nussbaumer Knaflic) to turn analysis into clear, decision-driving charts, slides, dashboards and reports. Use when creating, critiquing or redesigning any chart, graph, table, data slide, deck, dashboard page or written report that presents data to an audience, including requests like "plot this", "make this slide clearer", "how should I show these numbers" or "build a deck to get budget approved". Covers audience and Big Idea, chart choice, decluttering, focusing attention with color and emphasis, design, and narrative structure.
---
# Data Storycraft

Inspired by *Storytelling with Data* (Knaflic, 2015). The goal is explanatory communication: one audience, one message, one action. Every element of a visual supports the message, recedes to the background, or goes.

This is for communicating results. While the user is still exploring data, keep charts neutral and complete, because emphasis hides other patterns.

## Workflow

### 1. Context

Before any chart, write this block and put it at the top of the output:

```
Audience:  <specific person or group, ideally the decision maker>
Ask:       <what they must know or do>
Mechanism: <live presentation | sent document | both>
Big Idea:  <one sentence: point of view + what is at stake + the concrete ask, with its amount or date>
```

Infer what the request leaves out and say so; ask only when a wrong guess would make the work unusable. Show the data that supports the Big Idea and acknowledge the data that contradicts it.

Check the source, period, units and denominator before choosing the message. Missing values stay missing, not zero; keep gaps visible and label any supplied estimates. Distinguish percentage-point changes from relative percentage changes. Do not invent amounts, dates or data to complete the Big Idea; leave unsupported claims open.

### 2. Visual

| Need | Default |
|---|---|
| One or two numbers | The number, large, plus one sentence |
| Trend over time or continuous data | Line chart |
| Compare categories | Horizontal bar chart, sorted deliberately |
| Change between two points across categories | Slopegraph |
| Part-to-whole, survey or Likert scale | 100% stacked horizontal bar |
| Lookup by a mixed audience | Light-bordered table, or heatmap with legend |

### 3. Declutter

Remove chart border, background fill, gridlines, default markers, trailing zeros and diagonal text. If readers need exact values, label those values instead of adding gridlines. Replace the legend with a direct label on every series, grey ones included, in its own color. Keep units on numbers ($, %, thousand separators).

### 4. Focus

Start with everything grey, then bring forward only what carries the message: one accent color (default blue; orange for negative), a thicker line, markers and value labels on at most 3 points the message references, bold or larger text. Keep the accent to 10% of the ink at most and to 3 elements at most, put the most important element at the top left, and keep color meanings identical across every visual in a deck or report.

### 5. Design

Title the chart and both axes. Make the chart title an action title that states the takeaway and names the event the user mentioned ("Support tickets doubled after the March release", not "Tickets 2024"). "After" states timing, not cause, so keep the event in the title and put causal caveats in the footnote. Annotate key points on the chart, each label next to the point it describes. Align title, axis titles and legend to the upper left, avoid centered text, and size the visual to its content. Put the data source in a small grey footnote.

### 6. Story

Beginning: context and tension (what is vs what could be). Middle: evidence, options, cost of inaction. End: an explicit call to action. Lead with the ask for busy or trusting audiences; go chronological when credibility or process matters. In a deck, the slide titles alone tell the story, every slide supports its title, and the close restates the ask. Build decks on the skeleton in Output.

## Rules that hold almost always

| Rule | Why |
|---|---|
| Bar charts start at zero | The eye compares lengths; a truncated axis invents differences |
| No pie or donut charts | Angles and arcs are hard to compare; use sorted bars |
| No 3D | Perspective distorts values |
| No secondary y-axis | Label the second series directly, or split into panels sharing the x-axis |
| Consistent time intervals | Uneven spacing misrepresents the trend |
| No distorted scales or hidden contradicting data | One sharp viewer who spots it discards the whole argument |

## Reference map

Open only the reference the task needs.

| File | Open when |
|---|---|
| [reference/context.md](reference/context.md) | The brief is vague; need the Big Idea, requester questions or a storyboard |
| [reference/choosing-visuals.md](reference/choosing-visuals.md) | A need the defaults above do not cover, or notes on a default |
| [reference/decluttering.md](reference/decluttering.md) | A chart has more than 5 series or still has a legend; grouping, alignment, contrast |
| [reference/focusing-attention.md](reference/focusing-attention.md) | Color decisions, emphasis nuances, the eyes-drawn test |
| [reference/designing.md](reference/designing.md) | Text emphasis, hierarchy, accessibility, stakeholder pushback |
| [reference/model-visuals.md](reference/model-visuals.md) | A proven recipe for a common chart |
| [reference/storytelling.md](reference/storytelling.md) | Structuring a deck, report or talk |
| [reference/worked-example.md](reference/worked-example.md) | An end-to-end example of all six steps |
| [reference/case-studies.md](reference/case-studies.md) | Dark backgrounds, live vs sent versions, ordering, tangled lines, pie replacements |
| [reference/practice-and-teams.md](reference/practice-and-teams.md) | Iterating, recurring reports, team capability |

## Output

When creating, deliver the context block, the deliverable, and one line on where the eye lands first and why. Slide text goes in one block that ends with the ask, never only in speaker notes.

When structuring a deck, use this skeleton, with the summary bullets copied from the later titles:

```
Slide 1: <Big Idea with the ask>
- <title of slide 2>
- <title of slide 3, and so on: one bullet per later slide, same words, same order>
Slide 2: <action title>
...
Last slide: <the ask, restated>
```

When reviewing, name the single biggest problem before any list:

```
Biggest problem: <one sentence>

| Lesson | Issue | Why it hurts | Fix |
(rows only for lessons with real issues: Context, Visual, Clutter, Focus, Design, Story)

Redesign: <revised visual, or a precise spec of it>
```

## Rendering charts in code

Library defaults reintroduce the clutter this method removes, so override them. A matplotlib starting point:

```python
import matplotlib.pyplot as plt

GREY, DARK, ACCENT = "#A6A6A6", "#404040", "#1F5AA6"

fig, ax = plt.subplots(figsize=(9, 5))
for name, s in df.items():                      # one column per series
    color = ACCENT if name == focus else GREY
    ax.plot(s.index, s.values, color=color, lw=3 if name == focus else 1.5)
    ax.annotate(f" {name}", (s.index[-1], s.values[-1]), color=color, va="center")
ax.spines[["top", "right"]].set_visible(False)
ax.spines[["left", "bottom"]].set_color(GREY)
ax.tick_params(colors=GREY)
ax.grid(False)
ax.set_title("Action title that states the takeaway", loc="left", color=DARK)
ax.set_ylabel("Unit", color=GREY, loc="top")
ax.set_xlabel("Period", color=GREY, loc="left")
```

If another chart skill is also loaded, use its rendering mechanics but keep this skill's emphasis rules where the two conflict.

## Final check

Fix every "no", then check again. Deliver only when all pass.

- Is the Big Idea one sentence with an explicit ask?
- Is this the easiest chart to read for the comparison that matters?
- For each element, can you name the reader question it answers? Remove the ones that answer none.
- Does the eye land first on the point of the message?
- Are the chart and axes titled, with the takeaway and the event the user named stated in the title?
- Is the accent limited, consistent across visuals and readable for colorblind viewers?
- Are elements left-aligned, text horizontal and white space kept?
- In a deck, do the titles alone tell the story, and does the executive summary have one bullet per later slide, matching its title?
- In a review, is the first line the single biggest problem?
- Do the numbers match the data exactly? Recompute every total, saving or growth figure you show from its inputs, and flag any that do not match.
- Are missing values, estimates, units and denominators clear, with percentage changes distinguished from percentage-point changes?
