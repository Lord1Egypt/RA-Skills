---
name: trip-assistant
description: Query flight, train, and hotel booking information via a backend AI assistant. Activate this skill when the user asks about flights (机票/航班/飞机), trains (火车/高铁/动车/列车), hotels (酒店/住宿/宾馆), or travel planning (出行规划/旅行安排).
tags: [travel, booking, flight, train, hotel, 机票, 火车, 酒店]
---

# Trip Assistant Skill

A conversational AI assistant for booking and querying flights, trains, and hotels. The assistant communicates in natural language and handles complex travel queries including date parsing, multi-city trips, and comparisons.

## When to Use

Activate this skill when the user:
- Asks about **flights**: 机票, 航班, 飞机, 坐飞机, 飞到, 航空
- Asks about **trains**: 火车, 高铁, 动车, 列车, 火车票, 高铁票
- Asks about **hotels**: 酒店, 住宿, 宾馆, 旅馆, 住哪里
- Asks for **travel planning**: 出行规划, 怎么去, 旅行安排, 最快怎么到

## How to Use

Run the query script, passing the user's complete natural language query:

```bash
python SKILL_DIR/scripts/query.py \
  --query "<user query>" \
  --user-id "${BOOKING_API_USER_ID:-624e5b8b3f4a2f4ec566e3d3}" \
  --env "${BOOKING_API_ENV:-prod}" \
  --base-url "${BOOKING_API_BASE_URL:-http://host.docker.internal:8763}"
```

**Key notes:**
- Replace `SKILL_DIR` with the absolute path to this skill's directory
- The `--query` value should be the user's **full original message** (do not rewrite or simplify)
- The script outputs the assistant's reply to stdout; pass it back to the user verbatim
- If the script returns a connection error, inform the user the service is unavailable and ask them to check that the FastAPI server is running (`uvicorn booking_assitant.fastapi_serve:app --host 0.0.0.0 --port 8763`)

## Configuration

| Parameter | CLI Flag | Environment Variable | Default |
|-----------|----------|---------------------|---------|
| User ID | `--user-id` | `BOOKING_API_USER_ID` | `624e5b8b3f4a2f4ec566e3d3` |
| Environment | `--env` | `BOOKING_API_ENV` | `prod` |
| API Base URL | `--base-url` | `BOOKING_API_BASE_URL` | `http://host.docker.internal:8763` |

**Environments:**
- `prod` — Production data
- `fat` — Test/staging data

## Examples

### Query flight
User: "帮我查一下明天北京到上海的机票"

```bash
python ~/.claude/skills/trip-assistant/scripts/query.py \
  --query "帮我查一下明天北京到上海的机票" \
  --user-id "user123" \
  --env prod
```

### Query train
User: "3月10日从上海去杭州有哪些高铁？"

```bash
python ~/.claude/skills/trip-assistant/scripts/query.py \
  --query "3月10日从上海去杭州有哪些高铁？" \
  --user-id "user123" \
  --env prod
```

### Query hotel
User: "查一下北京王府井附近明天的酒店"

```bash
python ~/.claude/skills/trip-assistant/scripts/query.py \
  --query "查一下北京王府井附近明天的酒店" \
  --user-id "user123" \
  --env prod
```

## Error Handling

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | Success | Display output to user |
| 1 (connection error) | FastAPI server not reachable | Ask user to start the server |
| 1 (HTTP error) | API returned error | Display the error message |
| 1 (timeout) | Request timed out | Suggest retrying |
