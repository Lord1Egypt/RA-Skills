# API Reference

## RoundtableDB

Storage layer. Manages SQLite connections and CRUD operations.

```python
from roundtable.db import RoundtableDB

db = RoundtableDB(db_path="/path/to/roundtable.db")
conn = db.connect()
```

### Constructor

- `RoundtableDB(db_path=None)` — DB path resolution: explicit → `ROUNDTABLE_DB` env → `~/.roundtable/roundtable.db`

### Discussion CRUD

- `create_discussion(conn, topic, participants, *, context, max_rounds, speech_order, created_by, output_path) → Discussion`
- `get_discussion(conn, discussion_id) → Discussion | None`
- `list_discussions(conn, *, status, limit) → List[Discussion]`
- `conclude_discussion(conn, discussion_id, *, conclusion, convergence_score) → bool`
- `cancel_discussion(conn, discussion_id) → bool`

### Participants

- `get_participants(conn, discussion_id) → List[Participant]`
- `get_active_participant_names(conn, discussion_id) → List[str]`

### Speeches

- `add_speech(conn, discussion_id, participant, content, *, reply_to, round_override) → Speech`
- `get_speeches(conn, discussion_id, *, since_round, participant) → List[Speech]`
- `get_speech_count(conn, discussion_id) → int`

### Findings

- `add_finding(conn, discussion_id, finding_type, content, round_num, related_speeches) → int`
- `get_findings(conn, discussion_id, *, finding_type) → List[Finding]`

### Convergence

- `record_convergence(conn, discussion_id, round_num, score, consensus_count, disagreement_count, new_point_count)`
- `get_convergence_history(conn, discussion_id) → List[ConvergenceRecord]`

---

## RoundtableCore

Business logic layer. All methods return JSON-serializable dicts.

```python
from roundtable.core import RoundtableCore

core = RoundtableCore()  # uses default DB
```

### Methods

- `create_discussion(topic, participants, **kwargs) → dict`
- `speak(discussion_id, participant, content, **kwargs) → dict`
- `read(discussion_id, **kwargs) → dict`
- `status(discussion_id) → dict`
- `summarize(discussion_id) → dict`
- `end_discussion(discussion_id, *, force, conclusion) → dict`
- `list_discussions(**kwargs) → dict`

---

## Data Models

All in `roundtable.models`:

- `Discussion` — id, topic, context, status, max_rounds, current_round, speech_order, created_by, created_at, concluded_at, conclusion, convergence_score, output_path
- `Participant` — discussion_id, participant, role, perspective, display_name, joined_at, is_active
- `Speech` — id, discussion_id, round, participant, content, reply_to, created_at
- `Finding` — id, discussion_id, type, content, round, related_speeches
- `ConvergenceRecord` — discussion_id, round, score, consensus_count, disagreement_count, new_point_count

---

## Exceptions

All in `roundtable.exceptions` (all inherit `ValueError`):

- `RoundtableError` — base
- `DiscussionNotFoundError`
- `DiscussionNotActiveError`
- `InvalidParticipantError`
- `InvalidSpeechOrderError`
- `InvalidFindingTypeError`
- `InvalidReplyToError`
