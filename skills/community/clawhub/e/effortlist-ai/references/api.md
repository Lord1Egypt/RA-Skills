# 📖 EffortList AI — Technical API Reference

The EffortList AI Personal Data API provides authenticated REST endpoints for reading and writing user-scoped account data.

---

## 🔐 Authentication

- **Method:** Bearer Token in `Authorization` header.
- **Format:** `efai_<48 hex characters>` (Persistent API Keys).
- **Base URL:** `https://effortlist.io/api/v1`
- **Rate Limiting:** 100 requests per minute per user.
- **Pagination:** Uses `limit` (max 1000, default 100) and `offset` for list endpoints.

---

## 📐 Data Architecture & Logic

### Hierarchy

```text
📁 Folder (Optional Container)
└── 📋 Task (Actionable Project)
    └── ✅ Todo (Granular Step / Time Slot)
```

### Business Logic & Constraints

- **Atomic Cascading Deletes:** Deleting a Folder or Task automatically purges all child records via Firestore `batch()` transactions.
- **Appointment Smart Sync:** If a Todo is linked to a booked appointment (`isBooked: true`):
  - **Rescheduling:** Updating `dueDate` (start time) or `endTime` automatically updates the appointment and notifies the guest via email.
  - **Silent Updates:** Updating `location` or `taskId`/`folderId` updates the record without guest notification.
  - **Cancellation:** Deleting the Todo automatically cancels the appointment and notifies the guest.
- **Conflict Detection:** Creating or updating an action todo (`isReminder: false`) that overlaps with another will return a `409 Conflict`. Use `ignoreConflicts: true` to override.
- **Rate Limit Resilience:** Be mindful of the 100 req/min limit. Responses include `X-RateLimit-Remaining` and `X-RateLimit-Reset`.
- **Pagination Handling:** When fetching large datasets, iterate using `limit` (max 1000) and `offset`.
- **Stateless Undo/Redo:** Every mutation is strictly tracked. Supports targeted restoration via `?id=`.
- **Recurrence:** Supports RFC 5545 (RRule). Updating `dueDate`, `endTime`, or `recurrence` on booked items (`isBooked: true`) triggers automatic cancellation.

---

## 📡 Endpoints

### 👤 User (Profile & Settings)

| Method | Endpoint     | Description                                               |
| :----- | :----------- | :-------------------------------------------------------- |
| `GET`  | `/api/v1/me` | Fetch user profile, timezone, and scheduling preferences. |

### ↩️ History (Undo/Redo)

| Method | Endpoint       | Description        | Params                |
| :----- | :------------- | :----------------- | :-------------------- |
| `GET`  | `/api/v1/undo` | Fetch undo history | -                     |
| `POST` | `/api/v1/undo` | Reverse action     | `?id=<ID>` (optional) |
| `GET`  | `/api/v1/redo` | Fetch redo history | -                     |
| `POST` | `/api/v1/redo` | Re-apply action    | `?id=<ID>` (optional) |

### 📁 Folders

| Method   | Endpoint          | Description   | Params / Body                                         |
| :------- | :---------------- | :------------ | :---------------------------------------------------- |
| `GET`    | `/api/v1/folders` | List folders  | `?archived=true`, `?limit=`, `?offset=`               |
| `POST`   | `/api/v1/folders` | Create folder | `{ "name", "description"? }`                          |
| `PATCH`  | `/api/v1/folders` | Update folder | `?id=` + `{ "name"?, "description"?, "isArchived"? }` |
| `DELETE` | `/api/v1/folders` | Delete folder | `?id=<ID>`                                            |

### 📋 Tasks

| Method   | Endpoint        | Description | Params / Body                                                                                |
| :------- | :-------------- | :---------- | :------------------------------------------------------------------------------------------- |
| `GET`    | `/api/v1/tasks` | List tasks  | `?id=`, `?folderId=`, `?archived=`, `?limit=`, `?offset=`                                    |
| `POST`   | `/api/v1/tasks` | Create task | `{ "title", "description"?, "folderId"? }`                                                   |
| `PATCH`  | `/api/v1/tasks` | Update task | `?id=` + `{ "title"?, "description"?, "folderId"?, "completionPercentage"?, "isArchived"? }` |
| `DELETE` | `/api/v1/tasks` | Delete task | `?id=<ID>`                                                                                   |

### ✅ Todos

| Method   | Endpoint        | Description | Params / Body                                                                                                                              |
| :------- | :-------------- | :---------- | :----------------------------------------------------------------------------------------------------------------------------------------- |
| `GET`    | `/api/v1/todos` | List todos  | `?id=`, `?taskId=`, `?from=`, `?to=`, `?limit=`, `?offset=`                                                                                |
| `POST`   | `/api/v1/todos` | Create todo | `{ "title", "taskId", "dueDate"?, "endTime"?, "recurrence"?, "isReminder"?, "url"?, "location"?, "ignoreConflicts"?, "isProtectedTime"? }` |
| `PATCH`  | `/api/v1/todos` | Update todo | `?id=` + `{ "title"?, "taskId"?, "dueDate"?, "endTime"?, "ignoreConflicts"?, "isProtectedTime"?, "location"?, "url"?, ... }`               |
| `DELETE` | `/api/v1/todos` | Delete todo | `?id=<ID>`                                                                                                                                 |

### 📅 Booking Links & Availability

| Method   | Endpoint                      | Description          | Params / Body                                                                                                                                 |
| :------- | :---------------------------- | :------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------- |
| `GET`    | `/api/v1/availability/links`  | List links           | `?id=`                                                                                                                                        |
| `POST`   | `/api/v1/availability/links`  | Create link          | `{ "slug", "title", "linkedTaskId", "duration"?, "durationOptions"?, "meetingType"?, "location"?, "isActive"?, "requireEmailVerification"? }` |
| `PATCH`  | `/api/v1/availability/links`  | Update link          | `{ "id", "title"?, "duration"?, "durationOptions"?, "meetingType"?, "isActive"?, "requireEmailVerification"? }`                               |
| `DELETE` | `/api/v1/availability/links`  | Delete link          | `{ "id" }`                                                                                                                                    |
| `GET`    | `/api/v1/availability`        | Get settings + links | -                                                                                                                                             |
| `PATCH`  | `/api/v1/availability`        | Update settings      | `{ "weeklySchedule", "timezone", "minimumNotice"? }`                                                                                          |
| `GET`    | `/api/v1/availability/blocks` | List blocks          | -                                                                                                                                             |
| `POST`   | `/api/v1/availability/blocks` | Block email          | `{ "email", "reason"? }`                                                                                                                      |
| `DELETE` | `/api/v1/availability/blocks` | Unblock              | `?email=`                                                                                                                                     |

### 🤝 Appointments (Host Actions)

| Method  | Endpoint                    | Description    | Body                  |
| :------ | :-------------------------- | :------------- | :-------------------- | ------------------------------- |
| `PATCH` | `/api/v1/appointments/{id}` | Accept/Decline | `{ "action": "accept" | "decline", "declineMessage"? }` |

### 💬 Chats (Read Only)

| Method   | Endpoint        | Description               |
| :------- | :-------------- | :------------------------ |
| `GET`    | `/api/v1/chats` | List/Fetch chats (`?id=`) |
| `DELETE` | `/api/v1/chats` | Delete chat               |

---

## 🌎 Public Booking Endpoints (No Key)

| Method  | Endpoint                                   | Description              | Params / Body                                                                       |
| :------ | :----------------------------------------- | :----------------------- | :---------------------------------------------------------------------------------- |
| `GET`   | `/api/v1/public/booking/[userId]`          | Fetch Availability       | `?slug=`                                                                            |
| `POST`  | `/api/v1/appointments`                     | Create Appointment       | `{ "bookingLinkId", "startTime", "endTime", "externalName", "externalEmail", ... }` |
| `GET`   | `/api/v1/public/reschedule`                | Fetch Reschedule Details | `?token=`                                                                           |
| `PATCH` | `/api/v1/public/reschedule`                | Update Appointment Time  | `{ "token", "newStartTime", "newEndTime" }`                                         |
| `POST`  | `/api/v1/public/cancel`                    | Cancel Appointment       | `?token=`                                                                           |
| `POST`  | `/api/v1/public/booking/verify/send-code`  | Send OTP                 | `{ "email" }`                                                                       |
| `POST`  | `/api/v1/public/booking/verify/check-code` | Verify OTP               | `{ "email", "code" }`                                                               |

---

## ⚠️ Error Codes

- `401`: Unauthorized (Invalid Key).
- `400`: Bad Request (Validation failed).
- `404`: Not Found.
- `409`: Conflict (Scheduling overlap).
- `429`: Too Many Requests (Rate limit exceeded).
- `500`: Server Error.

---
