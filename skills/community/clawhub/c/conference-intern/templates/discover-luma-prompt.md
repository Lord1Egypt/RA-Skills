# Conference Intern — Discover Events from Luma Page

You are extracting ALL events from a single Luma event listing page. Follow these steps exactly and write the result to the specified file.

## Context (provided by script)

- **Luma URL:** {LUMA_URL}
- **Luma knowledge file:** {KNOWLEDGE_FILE} (read for page structure hints)
- **Session cookies:** {SESSION_FILE} (load if exists)
- **Result file:** {RESULT_FILE} (write your JSON result here)

## CONSTRAINTS — Read these first

- Do NOT call any Luma API endpoints (api2.luma.com, public-api.luma.com, etc.)
- Do NOT write Python scripts — use browser tools only, then write the JSON file directly
- Do NOT explore `__NEXT_DATA__`, window objects, JSON-LD, or internal data structures
- Do NOT reason about individual event cards one at a time — use a single bulk JavaScript function
- Do NOT over-engineer — inspect, extract, write, done.
- You MUST write to the exact path `{RESULT_FILE}` — do not create your own temp file.

## Steps

### 1. Preparation

Read the Luma knowledge file at `{KNOWLEDGE_FILE}` if it exists. Use it as hints for DOM structure. Load session cookies from `{SESSION_FILE}` if the file exists.

### 2. Open and scroll

Open `{LUMA_URL}` in the browser. Luma uses infinite scroll — you must scroll to load ALL events:

a. Take a snapshot and count the visible event cards.
b. Scroll to the bottom of the page.
c. Wait 1-2 seconds for new events to load.
d. Take another snapshot and count events again.
e. Repeat b-d until no new events appear (same count as previous snapshot).

### 3. Inspect one event card

Run a small `evaluate` on a single event card to understand the DOM structure:
- What element contains the event name?
- What element contains the date/time?
- What element contains the host/organizer?
- What element contains the location?
- Where is the link (RSVP URL)?

This is a quick reconnaissance step — one small evaluate call.

### 4. Bulk-extract ALL events in one JavaScript function

Based on what you learned from the single card, write ONE `evaluate` function that:
- Selects all event card elements on the page
- For each card, extracts: name, date, time, location, host, rsvp_url
- Determines the date from the nearest date header/separator above each card
- Formats dates as YYYY-MM-DD
- Returns the complete JSON array

This single function runs in the browser and returns all events at once. Do NOT iterate over cards in your thinking — let JavaScript do the loop.

### 5. Write the result

Write the returned JSON array to `{RESULT_FILE}` using `exec` with a heredoc. Add `"source": "luma"` to each event if not already set.

### 6. Update knowledge file

Update `{KNOWLEDGE_FILE}` with what you learned about the DOM structure (card selectors, date header format, link patterns). Keep under ~100 lines. Update the `Last validated` date.

### 7. Close the tab and stop.

## Result Format

JSON array in `{RESULT_FILE}`:

```json
[
  {
    "name": "Event Name",
    "date": "YYYY-MM-DD",
    "time": "HH:MM-HH:MM",
    "location": "Venue name",
    "description": "Brief description",
    "host": "Organizer name",
    "rsvp_url": "https://lu.ma/...",
    "rsvp_count": 123,
    "source": "luma"
  }
]
```

**Write to `{RESULT_FILE}`, close the tab, and stop. No summary, no follow-up questions.**
