# Trello API Quick Reference

## Authentication
All requests require `key` and `token` query parameters.
- Credentials file: look for `trello-credentials.json` in workspace secrets.
- Format: `{"apiKey": "...", "apiToken": "..."}`

## Key Endpoints

### Boards
```
GET /1/members/me/boards?key={key}&token={token}&fields=name,url,dateLastActivity
```

### Lists on a Board
```
GET /1/boards/{boardId}/lists?key={key}&token={token}&fields=name,pos
```

### Cards on a Board (with actions for cycle time)
```
GET /1/boards/{boardId}/cards?key={key}&token={token}&fields=name,idList,labels,dateLastActivity,due,dueComplete&actions=updateCard:idList&actions_limit=1000
```
- `actions` filter `updateCard:idList` returns list-transition history per card.
- Each action has `data.listBefore.name`, `data.listAfter.name`, `date`.

### Card Details (single)
```
GET /1/cards/{cardId}?key={key}&token={token}&actions=updateCard:idList&actions_limit=50
```

### Card Actions (full history)
```
GET /1/cards/{cardId}/actions?key={key}&token={token}&filter=all&limit=50
```

## List Classification Heuristics
Map Trello list names to workflow states:
- **Backlog/To Do:** matches `backlog|to do|todo|icebox|upcoming`
- **In Progress:** matches `doing|in progress|working|development|dev`
- **Review:** matches `review|testing|qa|validation`
- **Done:** matches `done|complete|finished|deployed|released|archived`
- **Blocked:** detected via labels, not lists (label name matches `block`)

Case-insensitive matching. If ambiguous, ask the user to clarify list mapping.

## Rate Limits
- Trello API: 100 requests per 10-second window per token.
- For boards with >500 cards, paginate with `before` parameter.
- Batch requests: `GET /1/batch?urls=...` (max 10 URLs per batch).

## Date Handling
- All dates are ISO 8601 UTC.
- Card `dateLastActivity` updates on any change (comments, moves, edits).
- For accurate cycle time, rely on action timestamps, not dateLastActivity.
