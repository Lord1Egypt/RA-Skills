# 钉钉日历 & 通讯录 MCP 工具速查

## 日历 MCP

MCP 名称：`dingtalk-calendar`（mcpId=1050，注册方式见 SKILL.md 初始化流程）

---

### 日程管理

#### create_calendar_event
创建新的日程，支持完整功能。

- **必填**：`summary`（标题，≤2048 字符）、`startDateTime`（ISO-8601）、`endDateTime`（ISO-8601）
- **可选**：`description`（≤5000 字符）、`richTextDescription`（HTML）、`location`、`timeZone`（默认 Asia/Shanghai）、`freeBusy`（busy/free，默认 busy）、`attendees`（userId 列表，≤500 人）、`openDingTalkIds`、`roomIds`（≤5 个会议室）、`calendarId`（默认 primary）、`recurrence`（循环规则）
- **循环规则 recurrence**：
  - `range`：`{type: "noEnd"|"endDate"|"numbered", endDate, numberOfOccurrences}`
  - `pattern`：`{type: "daily"|"weekly"|"absoluteMonthly"|"relativeMonthly"|"absoluteYearly", interval, dayOfMonth, daysOfWeek, firstDayOfWeek, index}`
- 返回：完整日程详情（id、时间、状态、参与人、会议室等）

#### update_calendar_event
修改现有日程，需组织者权限。**修改参与人请用 add/remove_calendar_participant**。

- **必填**：`eventId`
- **可选**：`summary`、`description`、`richTextDescription`、`startDateTime`、`endDateTime`、`freeBusy`、`location`、`timeZone`、`recurrence`、`calendarId`（默认 primary）

#### delete_calendar_event
删除日程。组织者删除通知所有参与者，参与者删除仅从自己日历移除。

- **必填**：`eventId`
- **可选**：`calendarId`（默认 primary）
- **执行前必须获得用户确认**

#### respond
作为参会人设置响应状态（接受/拒绝/暂定）。

- **必填**：`eventId`、`responseStatus`（`needsAction`/`accepted`/`declined`/`tentative`）
- **可选**：`calendarId`（默认 primary）

---

### 日程查询

#### list_calendar_events
列出指定时间范围内的日程，使用**毫秒级时间戳**。

- **可选**：`calendarId`（默认 primary）、`startTime`（毫秒时间戳）、`endTime`（毫秒时间戳）、`cursor`（分页游标）、`limit`（≤100，默认 100）
- 返回：`events[]`、`hasMore`、`nextCursor`

#### get_calendar_detail
获取日程完整详情。

- **必填**：`eventId`
- **可选**：`calendarId`（默认 primary）
- 返回：id、时间、状态、summary、location、attendees、organizer、reminders、categories、recurrence、meetingRooms、onlineMeetingInfo、description 等

#### get_calendar_participants
获取日程参与人列表及响应状态。

- **必填**：`eventId`
- **可选**：`calendarId`（默认 primary）
- 返回：`attendees[]`（self、optional、displayName、responseStatus）

---

### 参会人管理

#### add_calendar_participant
向日程添加参与人，支持批量。

- **必填**：`eventId`、`attendeesToAdd`（userId 列表）
- **可选**：`optional`（是否为可选参与人，默认 false）、`calendarId`（默认 primary）

#### remove_calendar_participant
从日程移除参与人，支持批量。

- **必填**：`eventId`、`attendeesToRemove`（userId 列表）
- **可选**：`calendarId`（默认 primary）

---

### 会议室管理

#### add_meeting_room
为日程预定会议室。

- **必填**：`eventId`、`roomIds`（roomId 列表，≤5 个）
- **可选**：`calendarId`（默认 primary）

#### delete_meeting_room
移除日程中的会议室并释放预定。

- **必填**：`eventId`、`roomIds`
- **可选**：`calendarId`（默认 primary）

#### query_available_meeting_room
查询指定时间段内空闲会议室（整个时段须空闲且当前用户可预定）。使用**毫秒级时间戳**。

- **必填**：`startTime`（毫秒时间戳）、`endTime`（毫秒时间戳）
- **可选**：`groupId`（会议室分组 ID）、`roomName`
- 返回：`result[]`（roomId、roomName、groupId、capacity、labels、needApproval、fullGroupPath、supportRecurring）

#### list_meeting_room_groups
查询企业会议室分组列表。

- **可选**：`pageSize`（≤100，默认 100）、`pageIndex`（默认 0）
- 返回：`groupList[]`（groupId、parentId、groupName）、hasMore、nextCursor

#### list_org_room_labels
查询企业会议室标签集，无需入参。

- 返回：`labels[]`（labelId、labelName）

---

### 闲忙查询与时间推荐

#### query_busy_status
查询用户或会议室在指定时间段的闲忙状态。使用**毫秒级时间戳**。

- **必填**：`startTime`（毫秒时间戳）、`endTime`（毫秒时间戳）
- **可选**：`userIds`（≤20）、`roomIds`
- 返回：`result[]`（userId/roomId、scheduleItems[]{start、end、status: BUSY/TENTATIVE}）

#### list_suggested_event_times
根据参会人空闲情况推荐日程时间。

- **可选**：`attendeeUserIds`、`durationMinutes`（默认 30）、`start`（ISO-8601，默认当前）、`end`（ISO-8601，默认次日 18 点）、`timeZone`（默认 Asia/Shanghai）
- 返回：`recommendEventTimes[]`（startTime、endTime）、`timeConflictAttendees[]`、`recommendReason`

---

### 日历本管理

#### list_calendars
查询用户所有日历（主日历 id="primary"，name="我的日历"），无需入参。

#### get_calendar
查询指定日历本信息。

- **必填**：`calendarId`
- 返回：type（primary/subscribed/shared）、summary、privilege、calendarId、description

#### search_calendar
按名称模糊搜索日历本。

- **必填**：`query`
- 返回：`result[]`（type、summary、privilege、calendarId、description）

#### update_calendar
更新日历本信息（需 owner 权限，主日历和他人共享的日历不可更新）。

- **必填**：`calendarId`
- **可选**：`summary`、`description`

---

### 日历权限（ACL）

#### add_acl
将日历共享给其他用户。

- **必填**：`userId`、`privilege`（`free_busy_reader`/`title_reader`/`reader`/`writer`）
- **可选**：`sendNotification`（默认 true）
- 返回：aclId、scope、privilege、success

#### delete_acl
删除已授予的日历访问权限。

- **必填**：`aclId`（通过 list_acls 获取）

#### list_acls
查询主日历的访问控制列表（共享情况），无需入参。

- 返回：`acls[]`（aclId、scope{name、type}、privilege）

---

### 附件

#### add_attachments
为日程添加附件，需先将文件上传到钉盘获取 fileId。

- **必填**：`eventId`、`attachments`（`[{id: "钉盘fileId", name: "文件名"}]`）
- **可选**：`calendarId`（默认 primary）

---

## 通讯录 MCP（辅助）

MCP 名称：`dingtalk-contacts`（mcpId=2400）

用于按姓名/手机号查找参会人的 userId，配合日历 MCP 使用。

### 常用工具

#### search_user_by_key_word
按关键词搜索组织内成员，返回 userId 列表。

- **必填**：`keyWord`
- 返回：按匹配度排序的 `userId[]`

#### search_user_by_mobile
按手机号查找成员 userId 和名称。

- **必填**：`mobile`
- 返回：`userId`、`orgUserName`

#### get_user_info_by_user_ids
根据 userId 列表获取成员详情。

- **必填**：`user_id_list`（userId 列表）
- 返回：`result[]`（orgUserId、orgUserName、orgTitle、jobNumber、depts、orgMasterDisplayName 等）

#### search_contact_by_key_word
按关键词搜索好友和同事（含花名、昵称、职位）。

- **必填**：`keyword`
- 返回：`result[]`（name、nick、title、userId、flowerName、openDingTalkId）

#### get_current_user_profile
获取当前登录用户详情，无需入参。

- 返回：userId、orgUserName、orgUserMobile、depts、orgMasterDisplayName、isAdmin 等

#### search_dept_by_keyword
按关键词搜索部门。

- **必填**：`query`
- 返回：`deptList[]`（deptId、deptName）、totalCount、hasMore

#### get_dept_members_by_deptId
获取部门下所有成员。

- **必填**：`deptIds`（部门 ID 数组）
- 返回：`deptUserList[]`（userInfo{name、userId}）

#### get_dept_info_by_dept_id
查询部门详情。

- **必填**：`deptId`
- 返回：deptId、deptName、memberCount

#### get_sub_depts_by_dept_id
获取子部门列表。

- **必填**：`deptId`
- 返回：`result[]`（deptId、deptName）

#### list_my_followings
获取特别关注列表，无需入参。

#### query_self_qr_code_info
获取个人钉钉二维码信息，无需入参。
