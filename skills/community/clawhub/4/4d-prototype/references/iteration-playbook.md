# P7 Iterating on feedback: feedback patterns, structural changes and data migration

After delivery the user gives feedback round after round, sometimes a single sentence per round. Two things matter in this phase: read the need behind the sentence, and update every affected view — not just the one in front of the user.

## 1. Handling each round

1. **Break it down**: split the user's words into verifiable requirements, and record the original wording in `memory-bank/specs.md` (with date and milestone number). If the user also asked side questions, note them separately and answer after the changes.
2. **Understand the real need**: for vague requests, consider several readings and explain your interpretation in the report. When the user adds to or corrects the request midway (e.g. "it doesn't have to be bigger fonts everywhere"), the corrected meaning wins; update specs.
3. **Judge the size**:
   - Small adjustment: just do it.
   - New capability: make it a milestone.
   - Structural change: tag first. Linear to DAG, merging or deleting modules, and changing a data source all count.
4. **List the blast radius**: wherever a concept appears, it must change in sync. For "step": workflow definition, director, navigator, DAG views (overview, dock, thumbnail), swimlanes, capsule, page-header tags, overview cards, docs, assumption register, tests. Count references with grep before editing.
5. **Implement, verify, commit**: run the full "loop for every milestone" from SKILL.md.
6. **Report**: first what changed and where to see it, then measured evidence and trade-offs, then answers to side questions.

## 2. Feedback patterns from the original project (reuse by analogy)

The table comes from the original project (a data audit + RPA + agent prototype). These requests target the time axis (the 4D orchestration layer) and the way of discussing, not the business domain, so approval, integration, admin and reporting projects mostly receive the same kinds: tie the whole flow together, show data changes, separate actors, turn it into a DAG, control playback, show original formats, label required vs optional, switch steps freely, adjust business definitions.

| User's words (summary) | Need behind it | Response | Verification |
|---|---|---|---|
| Tie everything together in business order, add a one-click run, add a global floating navigator showing the current step (with sub-steps) | Watch the whole business without clicking anything, and always know where we are | Workflow definition (phase / step / sub-step) + director + every page wired with `useFlowStep` + bottom-left floating navigator + "this page in the whole flow" tags | Full run in the browser (all steps), time recorded; jumps; pause on leaving the page |
| Show data structures and how they change in more depth | Business and engineering align on "what the data looks like and where it changes" | Data object catalog + per-record lineage (how each field changed) | Lineage unit tests assert stages and field changes |
| Distinguish actors and timing (RPA bot, front-line staff, admins, backend batch) | Who does what, when | Actor catalog + swimlanes + time of day and trigger + actor labels on pipeline stages | Screenshots |
| Anything else that helps understand the requirements and the agent scenarios | Expects proactive additions | Agent intervention vs human checkpoint table, human–AI loop via case library, data object catalog; all registered as new assumptions | — |
| Turn the flow into a DAG; tag before changing | Steps depend on each other rather than just following each other; and rollback must be possible | tag → EDGES (data on edges) + dependency scheduling + branch choice in step mode + "assumed done" | DAG invariant tests; scheduling from a middle step |
| Add a mouse position and click animation; speed adjustable at any time | See a "person" operating; control the pace | Demo cursor + virtual clock (every delay goes through it) | Mid-step speed change takes effect; cursor visible above dialogs |
| Show file / data formats | See what real files look like | formats + preview, reusing the export model | Screenshots |
| Make the fonts bigger overall → not necessarily bigger, but a more comfortable overall structure | Readability, not font size | 12px minimum, darker secondary text, looser line height, sticky section nav, content moves aside when panels expand | Contrast values, screenshots |
| During playback, keep showing the current file / table format and a more detailed DAG in a separate window; you decide where | See "what data is in use now" without switching pages | Bottom dock (part of the layout), `data` on every sub-step, table samples | Screenshots of each step; the dock follows the demo |
| Show files in their original look, not JSON; resizable window; big control buttons inside it; clicking a node while paused stays paused; Space to pause / resume; speeds 0.25–2; and by the way, "is the nightly merge step required?" | Smooth demo control; files that look real; clarity on what is essential in the flow | Original-look rendering (official document / sheet / review panel / trace), drag and maximize, big buttons, keepPaused, Space in capture phase; finally answer in business language which step is required and why | Click a node while paused, wait 5 s, nothing changes; dock height before / after dragging |
| Mark two steps as "prototype addition · optional" and one as "required by the spec" | The answer belongs in the prototype | `necessity` + `basis`, shown in every view | Test: non-optional steps don't depend on optional ones |
| Center the playback controls, with nothing taking space on either side | Less occlusion | Centered floating capsule; collapsed dock height 0 | `--flow-dock-h` = 0 when collapsed |
| Every node must be switchable, including after the flow finishes; move the demo organization to my region | Jump to any step during discussions; demo data close to the user's own context | Remove redirects, pages supply their own data; replay after finishing; migrate all data and bump the store version | Click 5 nodes in turn after finishing; the old organization name no longer appears |
| A nine-point redesign (per-organization config, single data source via upload, remove a module, rule categories, natural-language maintenance + diff, auto export, result retention, dashboard, roles) | The business definition changed | See §3 | Full test suite, every page, one-click run |

## 3. Steps for a structural change

1. Tag the current version (and push it, if pushing is authorized), e.g. `git tag -a v0.15-pre-redesign -m "…"`.
2. Read the new reference material, e.g. the section structure of a rule document, and settle the new categories and bases.
3. Change bottom-up: types → rules / engine → domain (roles, permissions, mapping tables) → state (config stores, versions, retention) → pages → workflow definition (reordered steps) → data objects and formats → lineage → overview / tour → assumption register. Run `typecheck` after each layer to see what still doesn't compile.
4. **Delete completely**: a module the user says to remove goes away together with its pages, mocks, state, routes and copy; the old version stays in the tag. Afterwards grep for leftovers of old routes, roles and terms.
5. Rewrite tests for the new model: print actual hits with a probe first, confirm, then write assertions; add tests for new capabilities, e.g. independent configs, matching by user, publishing only confirmed changes, data scope, new worksheets.
6. Assumption register: add a group "key points and assumptions of this redesign", delete entries that no longer apply, and update the document.
7. Regression: sweep every page + one-click run + manual scenarios for the new capabilities.

## 4. Global data migration (e.g. "move the demo organization to my region")

1. Measure the scope first: `grep -rn "<old name>\|<old code prefix>\|…" src | wc -l`. In the original project there were about 190 occurrences across mocks, organizations, rules, state and tests.
2. Build one consistent mapping table: organization codes, code prefixes, external-system accounts, company names, phone area codes, ownership of locality rules, supervising departments, file names, narration. Migrate the existing data wholesale and keep the original organization as "other organizations" in statistics, so organization-wide numbers stay plausible.
3. Old data in the browser: bump the store `version` so a new storage key is used and the old one cleared; after a reload the user sees the new data. Say in the report that changes the user made during demos are cleared as well.
4. Verify:
   - A test that every demo role belongs to the new organization.
   - Grep that no page copy still contains the old name.
   - Write old-version data, reload, confirm it was cleared.

## 5. Answering side questions

- Finish the requested changes first, then answer — in business language, with the basis, e.g. "section 2.4 requires … and the data warehouse is T+1 …".
- Distinguish three things: required by the spec, a prototype addition (optional), and merely how the diagram is drawn. Example from the original project: "the merge node is just how it is drawn; it doesn't mean the daytime work is done again".
- If the answer exposes an ambiguity in the prototype, offer to label it in the prototype. The user usually asks for exactly that in the next round.
