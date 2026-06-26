---
name: feishu-sheet-tabs
description: Create and organize multiple tabs (worksheets/pages) inside an existing Feishu sheet when the normal feishu_sheet API cannot create new worksheet tabs. Use when the user wants one spreadsheet split into categories/pages/tabs, asks for pagination inside a sheet, or wants separate worksheet tabs such as 总览 / Skills / Workflows / Templates / Content. Prefer this skill only after confirming feishu_sheet API lacks tab-creation support.
---

# Feishu Sheet Tabs

Use this skill to add worksheet tabs inside an existing Feishu sheet by browser automation when `feishu_sheet` API can create/read/write spreadsheets but cannot create worksheet tabs.

## Core conclusion

Current `feishu_sheet` API supports spreadsheet-level actions like:
- create
- info
- read
- write
- append
- find
- export

It can target an existing sheet via `sheet_id`, but it does **not** expose a direct action for creating worksheet tabs/pages.

When the user explicitly wants tabs/pages inside one spreadsheet, switch to browser automation.

## Preconditions

Before using browser automation, ensure all of the following:

1. The target spreadsheet URL/token is known.
2. The user is logged into Feishu in a browser tab.
3. Prefer using the user's real Chrome tab via Browser Relay when available.
4. If Browser Relay is not attached, isolated browser may work only if it has a valid Feishu login state.

## Preferred operating mode

### Mode A: User's Chrome tab (preferred)
Use `browser` with `profile="chrome"` if the user has attached the tab via OpenClaw Browser Relay.

Why:
- stable login state
- real user session
- fewer auth surprises

### Mode B: OpenClaw managed browser
Use `profile="openclaw"` only if it is already logged into Feishu.

## Reliable workflow

### Step 1: Verify API limitation first
Do **not** claim “can’t do it” without checking.

Confirm from tool docs / current tool signature that `feishu_sheet` has no `add_sheet` / `create_worksheet` / `add_tab` action.

### Step 2: Open the spreadsheet in browser
Use browser automation to open the spreadsheet.

### Step 3: Inspect runtime objects
Feishu Sheets exposes internal JS objects on the page. In practice, these were found useful:
- `window.spread`
- `window.spreadApp`

Relevant methods discovered from runtime introspection:
- `spread.addSheet(name)`
- `spread.renameSheet(sheetId, name)`
- `spread.copySheet(...)`
- `spread.moveSheet(...)`
- `spread.hideSheet(...)`

### Step 4: Read current sheet ids/names
Use page evaluation to inspect current sheets before mutation.

Pattern:

```js
window.spread.sheets.map((s,i)=>({
  i,
  id: s.id?.() ?? s._id ?? s.sheetId ?? null,
  name: s.name?.() ?? s._name ?? null
}))
```

### Step 5: Rename default first tab if needed
Typical pattern:
- rename `Sheet1` → `总览`

### Step 6: Add tabs with `spread.addSheet(name)`
For example:
- Skills
- Workflows
- Templates
- Content

### Step 7: Fill each tab with `feishu_sheet write`
After tabs exist and their `sheet_id`s are known, return to `feishu_sheet` for structured writes. This is more stable than trying to type cell-by-cell in browser automation.

## Proven pattern from this workspace

For spreadsheet:
- `https://bytedance.larkoffice.com/sheets/Bf6qsMV9fhqrD6tPE6TcQhF7nEe`

The following sequence worked:

1. Inspect `window.spread`
2. Discover `spread.addSheet` and `spread.renameSheet`
3. Read current sheet list and ids
4. Rename `Sheet1` to `总览`
5. Create:
   - `Skills`
   - `Workflows`
   - `Templates`
   - `Content`
6. Use `feishu_sheet write` with returned sheet ids to populate each tab

## Example evaluation snippets

### Discover methods

```js
function protoMethods(obj,name){
  if(!obj) return [];
  const out=[];
  let p=Object.getPrototypeOf(obj);
  let depth=0;
  while(p && depth<4){
    for(const k of Object.getOwnPropertyNames(p)){
      if(k==='constructor') continue;
      if(/sheet|tab|workbook|insert|create|add|page|name|rename/i.test(k)) out.push(`${name}.${k}`);
    }
    p=Object.getPrototypeOf(p); depth++;
  }
  return [...new Set(out)];
}
```

### Rename + create tabs

```js
async () => {
  const spread = window.spread;
  const results = [];

  const current = spread.sheets.map(s => ({
    id: s.id?.() ?? s._id ?? null,
    name: s.name?.() ?? s._name ?? null
  }));

  const first = current[0];
  if (first?.name === 'Sheet1') {
    results.push(await spread.renameSheet(first.id, '总览'));
  }

  for (const name of ['Skills','Workflows','Templates','Content']) {
    const names = spread.sheets.map(s => s.name?.() ?? s._name);
    if (!names.includes(name)) {
      results.push(await spread.addSheet(name));
    }
  }

  return spread.sheets.map((s,i)=>({
    i,
    id: s.id?.() ?? s._id ?? null,
    name: s.name?.() ?? s._name ?? null
  }));
}
```

## Important caveats

1. **Prefer internal methods over brittle UI clicking**
   Clicking `+` in the UI was less reliable than runtime JS calls.

2. **Do not assume a visible plus button is the right entry**
   In this case, one nearby button turned out to be a template entry, not “new tab”.

3. **Use browser only for the tab creation step**
   Once tabs are created, switch back to `feishu_sheet write`.

4. **Inspect current ids before writing**
   New tabs get generated `sheet_id`s such as `GxGIGa`, `9dJYiB`, etc. Use actual returned ids.

5. **Avoid blind UI automation first**
   Inspect runtime objects and methods before pixel-clicking.

## When to use this skill

Use this skill when the user says things like:
- “把这个表做成分页”
- “按类别分开 sheet”
- “给这张飞书表加几个页签”
- “我就想分页，你想办法解决”

## Output expectation

When done, report:
- which tabs were created/renamed
- which tab ids were found
- whether data filling was also completed
- whether browser login / relay was required
