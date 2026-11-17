# Multi-frame & Multiple Links Handling

When the user provides 2+ Figma links, determine the relationship by examining
frame names and user context:

## Same page, different visual states

(e.g. "首页-有banner" and "首页-无banner")

Use `--compare` mode to fetch all and get a diff summary. Generate multi-state
code (conditional visibility, state switching).

## Parent page + overlay/drawer

(e.g. "首页" + "首页-抽屉-xxx")

Generate each as an **independent layout file**. Then tell the user the
relationship:

> Frame 1 ("首页") and Frame 2 ("首页-抽屉") look like a main page + side drawer.
> I've generated two separate layout files. How you wire them together
> (DrawerLayout, Navigation, etc.) depends on your project architecture.

The skill's job is generating UI layout code, not deciding architecture
(Activity vs Fragment vs Navigation).

## Different independent pages

(e.g. "首页" + "设置页" + "个人中心")

Process each independently. Fetch them **one at a time** with a pause between
requests to avoid rate limiting. Present a summary of all pages, then ask which
to convert first (or convert all sequentially).

## Relationship unclear

Ask the user — "These frames look related but I'm not sure how. Are they
different states of the same page, a page with an overlay, or independent pages?"

## Rate limit protection

When fetching multiple nodes, wait 2-3 seconds between requests. Never fire
more than 2 requests in parallel.
