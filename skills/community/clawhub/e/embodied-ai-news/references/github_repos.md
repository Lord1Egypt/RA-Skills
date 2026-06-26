# ⭐ GitHub — Embodied AI Open Source Hot Repos

Companion reference for the **GitHub 热门开源仓库** module: how to discover, rank, and present repositories that are most relevant to embodied AI / robot learning (not generic industrial automation or unrelated “robot” tooling).

---

## When to Use This File

Consult during **Phase 1** (gathering) and **Phase 5** (output) when:

- The user asks for **GitHub 热门**、**开源仓库**、**star 最多的机器人项目**，或 explicitly wants a **repo leaderboard**
- The briefing type is **Weekly** or **Monthly** and the user wants **open-source momentum** included
- You are filling the **`## ⭐ GitHub 热门开源（具身智能相关）`** section in `output_templates.md`

**Default**: Do **not** add this section to a **Daily** briefing unless the user asked for it or for “full stack / 含开源”.

---

## Data Sources & Tools

| Source | Tool | Notes |
|--------|------|--------|
| GitHub repository search (sorted) | `WebSearch` + `WebFetch` | Prefer official `github.com` URLs; verify repo still exists |
| GitHub Topics | `WebFetch` | e.g. topic pages for `robotics`, `reinforcement-learning`, `sim2real` |
| Curated lists / “awesome-*” | `WebSearch` | Use to cross-check names; still verify primary repo URL on GitHub |

**Do not** fabricate star counts or “#1 trending” claims. Use numbers **only** if visible on the fetched GitHub page or in search snippets at collection time; otherwise write **“stars: see repo page”** or omit the column.

---

## Relevance Filter (Must Pass)

A repo **qualifies** for this module if it clearly supports **one or more** of:

- **Policies / models**: VLA, diffusion / flow policies, imitation / offline RL, world models for control
- **Data & teleop**: datasets, teleoperation stacks, human demo pipelines
- **Simulation → real**: Isaac / MuJoCo / Habitat-class stacks, domain randomization, sim benchmarks
- **Whole-body / manipulation**: humanoid / quadruped / arm stacks where **learning** or **ML policy** is central
- **Embodied foundation models**: GR00T-class, generalist robot models, cross-embodiment training code

**Deprioritize or exclude** unless the user asks broadly:

- Pure motion planning / classic control with no learning angle
- Arduino / ROS tutorial repos with no embodied-AI focus
- Unmanned vehicles / autopilot-only (unless explicitly in scope)
- Empty forks, archived with no replacement, or name-squatting

---

## Discovery Procedure (Executable)

### Step G1 — Run discovery queries

Use `search_queries.md` → **Section 10.5** and **Recipe F** (`WebSearch`, `return_format`: markdown).

Minimum: **3 queries** from Recipe F (rotate which sub-queries you use if a run returns noise).

### Step G2 — Collect candidates

Target **12–20** candidate repos, then **shortlist 5–8** for the briefing.

### Step G3 — Rank (“热门” definition)

Apply in order (break ties by recency of meaningful commits / releases if visible):

1. **Ecosystem impact**: widely cited stacks (sim, benchmark, policy zoo), de-facto standard tooling
2. **Recent activity**: releases, tags, or default-branch commits in the last **30 days** (if checkable)
3. **Stars**: higher is a weak proxy for popularity — use only as **one** signal
4. **Narrow spikes**: very new repos with explosive stars — label **“Emerging (high velocity)”** if you have evidence

### Step G4 — Verify

For each shortlisted repo:

- Open `https://github.com/{owner}/{repo}` (via `WebFetch` or browser)
- Confirm **description**, **default branch**, **not archived** (or explain if archived but still the canonical fork)
- Copy the **canonical** URL (no deep `/tree/` unless linking to a specific release tag the user needs)

### Step G5 — De-duplicate vs news body

If a repo is **already** the main subject of a story in **Foundation Models & Algorithms** or **Simulation & Infrastructure**, you may **merge**: one line in the GitHub table + “See story above” instead of repeating full paragraphs.

---

## Output Schema (per repo)

Use in markdown table or bullet blocks (see `output_templates.md`):

| Field | Required | Example |
|-------|----------|---------|
| **Repository** | Yes | `org/name` as link |
| **One-line role** | Yes | “VLA training & eval for …” |
| **Category tag** | Yes | From list below |
| **Language** | If visible | Python / C++ / … |
| **Stars** | If verified | `12.4k` or “see repo” |
| **Activity note** | Optional | “Release x.y last week” |

**Category tags** (pick one primary):

`Policy / VLA` · `Sim & Sim2Real` · `Data / Teleop` · `Whole-body / Locomotion` · `Manipulation` · `Benchmark / Eval` · `Hardware / Middleware`

---

## Anchor List (Sanity Check, Not Exhaustive)

Use to avoid missing obvious high-signal projects when search is noisy; **always** re-validate on GitHub:

- NVIDIA: `IsaacLab`, `GR00T` (and related)
- Google DeepMind: `mujoco`, `dm_control`
- Meta FAIR: `habitat-lab`, `PyTorch3D` (when used for embodied / 3D policy research)
- Open Robotics middleware: `ros2` (include only if briefing scope covers **ML-on-ROS** embodied stacks)
- Community: `lerobot`, `robosuite`, `mani_skill`, `ORBIT`, `IsaacGymEnvs` (legacy but still referenced)

If an anchor is **archived** or superseded, prefer the **successor** named in the repo README.

---

## Footnote for Briefings

Append to the GitHub section when star counts or rankings are approximate:

> **Note**: Rankings reflect search-time signals (stars, activity, ecosystem role), not a guaranteed global order. Prefer following the linked repo for authoritative metrics.

---

> **Last Updated**: April 2026  
> **Maintainer cue**: Refresh anchor names and topic URLs quarterly via the Maintenance Proposal workflow (`workflow.md` Part B). Do not modify this file without user approval.
