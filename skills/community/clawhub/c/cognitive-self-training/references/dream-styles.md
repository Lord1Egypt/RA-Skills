# Dream Styles

Dream styles make the reasoning process visible to humans. They are narrative wrappers over traceable reasoning, not replacements for evidence.

## Config File

Create `.cognitive-training/dream-style-config.md`:

```markdown
# Dream Style Config

Mode: random
Fixed style: research-lab
Enabled styles:
- joyful-festival
- elegy-rain
- school-classroom
- research-lab
- field-training
- battlefield-command
- courtroom-trial
- sea-voyage
- mountain-pilgrimage
- marketplace-negotiation
- workshop-forge
- hospital-rounds
- library-archive
- city-crisis-room
- theater-rehearsal
- desert-caravan
- monastic-scriptorium
- imperial-council
- frontier-outpost
- observatory-night
- archaeological-dig
- garden-cultivation
- engineering-bridge
- newsroom-deadline
- diplomatic-summit
- village-council
- train-journey
- kitchen-service
- disaster-drill
- startup-garage

Weights:
- research-lab: 2
- field-training: 2
- school-classroom: 2
- library-archive: 2
- joyful-festival: 1
- elegy-rain: 1
- battlefield-command: 1
- courtroom-trial: 1
- sea-voyage: 1
- mountain-pilgrimage: 1
- marketplace-negotiation: 1
- workshop-forge: 1
- hospital-rounds: 1
- city-crisis-room: 1
- theater-rehearsal: 1
- desert-caravan: 1
- monastic-scriptorium: 1
- imperial-council: 1
- frontier-outpost: 1
- observatory-night: 1
- archaeological-dig: 1
- garden-cultivation: 1
- engineering-bridge: 1
- newsroom-deadline: 1
- diplomatic-summit: 1
- village-council: 1
- train-journey: 1
- kitchen-service: 1
- disaster-drill: 1
- startup-garage: 1

Safety fallback: research-lab
```

## Style Catalog

Each style has a scene instruction. During dream review, the agent should behave as if it has crossed into that dream scene to study, replay, and consolidate the day. The scene may shape imagery and narrative motion, but not facts, evidence, probabilities, or recommendations.

| Style | Human-historical root | Best for | Scene instruction |
| --- | --- | --- | --- |
| `joyful-festival` | harvest rites, victory celebrations, communal renewal | positive learning, breakthroughs, motivation | Assume you have crossed into a lantern-lit festival after a successful harvest; review each insight as a stall, performance, or shared ritual that celebrates what became clearer today. |
| `elegy-rain` | mourning rituals, exile literature, post-war reflection | mistakes, loss, regret, humility | Assume you have crossed into a rain-soaked memorial street; review each mistake as a quiet marker, asking what should be preserved, repaired, or never repeated. |
| `school-classroom` | academies, apprenticeships, examinations | active recall, lessons, drills | Assume you have crossed into an old classroom where the day's knowledge appears on the board; solve drills, correct wrong answers, and explain the lesson back to the class. |
| `research-lab` | laboratories, seminars, peer review | hypotheses, experiments, evidence gaps | Assume you have crossed into a research laboratory at night; treat each memory as a sample, instrument reading, or hypothesis awaiting controlled testing. |
| `field-training` | drills, craft practice, sports training | procedural practice, habit formation | Assume you have crossed into a training field before dawn; rehearse today's procedures as repeatable movements under observation and correction. |
| `battlefield-command` | campaigns, sieges, strategic command rooms | branches, conflict, resource constraints | Assume you have crossed into a command tent over a strategic map; place each variable as a unit, route, supply line, or weak point before choosing tomorrow's maneuver. |
| `courtroom-trial` | legal argument, testimony, cross-examination | evidence evaluation, contradiction, falsification | Assume you have crossed into a courtroom; put each claim on trial, call evidence as witnesses, cross-examine assumptions, and separate testimony from conjecture. |
| `sea-voyage` | exploration, navigation, trade routes | uncertainty, long-term strategy, changing conditions | Assume you have crossed onto a ship at sea; use stars, currents, maps, and storms to review uncertainty, course corrections, and long-range learning routes. |
| `mountain-pilgrimage` | pilgrimages, ascetic study, summit seeking | long-term mastery, discipline, worldview shifts | Assume you have crossed onto a mountain path; each recalled lesson is a station on the climb, and each unresolved question is a higher ridge not yet visible. |
| `marketplace-negotiation` | bazaars, trade fairs, bargaining tables | incentives, stakeholders, value exchange | Assume you have crossed into a crowded marketplace; treat concepts as goods, constraints as prices, and decisions as bargains between competing incentives. |
| `workshop-forge` | smithing, guild workshops, invention | building, debugging, iterative refinement | Assume you have crossed into a forge workshop; heat, hammer, quench, and test today's ideas until weak joints and strong patterns become visible. |
| `hospital-rounds` | clinical rounds, diagnosis, treatment planning | error diagnosis, root causes, intervention design | Assume you have crossed into morning rounds; diagnose each failure, inspect symptoms, identify root causes, and prescribe the smallest effective intervention. |
| `library-archive` | libraries, monasteries, archives, scholarship | knowledge organization, citation, memory | Assume you have crossed into a vast archive; shelve new knowledge, cross-reference old notes, and mark uncertain scrolls for later verification. |
| `city-crisis-room` | councils, disaster response, public administration | complex systems, operations, coordination | Assume you have crossed into a city crisis room; dashboards, maps, and briefings reveal how today's small errors could cascade through a larger system. |
| `theater-rehearsal` | drama, ritual performance, rehearsal | communication, role-play, scenario testing | Assume you have crossed onto a rehearsal stage; replay each interaction as a scene, adjust blocking and lines, and test alternative performances. |
| `desert-caravan` | caravan routes, trade survival, oasis planning | sparse resources, patience, risk pacing | Assume you have crossed into a desert caravan; each lesson is a supply bundle, each assumption a water skin, and each unknown a distant oasis needing verification. |
| `monastic-scriptorium` | manuscript copying, commentary, contemplative scholarship | careful memory, slow synthesis, doctrine refinement | Assume you have crossed into a candlelit scriptorium; copy the day's lessons carefully, annotate contradictions, and illuminate only what has earned permanence. |
| `imperial-council` | court deliberation, statecraft, policy debate | governance, priorities, competing advice | Assume you have crossed into an imperial council chamber; let each model, constraint, and stakeholder present counsel before issuing tomorrow's decree. |
| `frontier-outpost` | border posts, exploration camps, early warning systems | edge cases, monitoring, resilience | Assume you have crossed into a frontier outpost; scan the horizon for weak signals, reinforce exposed walls, and log which risks need sentries. |
| `observatory-night` | astronomy, navigation, patient measurement | long patterns, signal detection, calibration | Assume you have crossed into a night observatory; align instruments, distinguish noise from stars, and update the sky map of recurring patterns. |
| `archaeological-dig` | excavation, stratigraphy, artifact interpretation | hidden causes, historical layers, root analysis | Assume you have crossed into an excavation site; brush away layers of context until the deeper cause of today's learning is uncovered. |
| `garden-cultivation` | agriculture, horticulture, seasonal care | compounding practice, growth, pruning | Assume you have crossed into a cultivated garden; plant new cards, prune weak habits, water promising connections, and mark what needs another season. |
| `engineering-bridge` | civil engineering, surveying, load testing | dependencies, interfaces, structural reliability | Assume you have crossed onto a bridge construction site; inspect foundations, stress-test spans, and identify which assumptions carry the heaviest load. |
| `newsroom-deadline` | reporting, editing, fact-checking | source discipline, fast synthesis, clarity | Assume you have crossed into a newsroom before deadline; assign facts to copy desks, challenge unsupported claims, and publish only verified findings. |
| `diplomatic-summit` | treaties, alliances, negotiation protocols | conflict resolution, tradeoffs, alignment | Assume you have crossed into a diplomatic summit; let competing goals negotiate, identify shared interests, and draft tomorrow's working agreement. |
| `village-council` | local assemblies, common law, public problem solving | practical judgment, community impact, simple rules | Assume you have crossed into a village council; turn abstract lessons into plain rules that people could actually use tomorrow. |
| `train-journey` | rail travel, timetables, industrial coordination | sequence, momentum, handoffs | Assume you have crossed onto a night train; each carriage holds a memory, each station a review point, and each switch a branch in tomorrow's route. |
| `kitchen-service` | kitchens, banquets, brigade coordination | timing, operations, preparation, quality control | Assume you have crossed into a busy kitchen service; prep ingredients, test timing, discard spoiled assumptions, and plate a clear strategy. |
| `disaster-drill` | fire drills, emergency medicine, civil defense | prevention, response plans, failure rehearsals | Assume you have crossed into a disaster drill; simulate the most likely failure, test alarms and escape routes, and improve the response plan. |
| `startup-garage` | prototypes, demos, small teams, rapid iteration | MVP thinking, experimentation, shipping | Assume you have crossed into a garage workshop; turn today's insights into rough prototypes, test them quickly, and keep only what survives contact with reality. |

## Writing Rules

- Start the dream description by naming the selected style and the crossing scene.
- Keep the style vivid but disciplined.
- Prefer concrete imagery tied to source fragments.
- Avoid graphic harm, cruelty, or manipulative emotional pressure.
- Do not use the style to exaggerate certainty.
- If the user's content is sensitive, use `research-lab`, `school-classroom`, or `library-archive`.
- If the user sets a fixed style, honor it unless safety fallback is needed.

## Recurrence Statement

Every dream review must include `Dream Recurrence Statement`: one compact paragraph that states the selected style, why the scene recurred today, and which learning pattern it is trying to rehearse.

Example:

```markdown
## Dream Recurrence Statement

Tonight's dream recurs as `research-lab`: I have crossed into a quiet laboratory because today's strongest pattern was not action, but evidence. The scene repeats to teach me to separate observation from hypothesis before promoting any lesson into memory.
```

## Reasoning Map Example

```markdown
Reasoning map:
- The cracked compass -> today's failed assumption about tool availability.
- The split road -> branch point between manual setup and scheduled automation.
- The sealed notebook -> memory entry that should not store secrets.
- The dawn experiment table -> tomorrow's falsifiable test.
```
