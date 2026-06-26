---
name: meeting-assistant
description: AI meeting assistant for agenda generation, minute taking, and action item tracking using Manager-Worker pattern.
---

# Meeting Assistant

AI-powered meeting assistant that helps you organize, conduct, and follow up on meetings efficiently.

---

## Features

### 📋 Agenda Generation

- Automatic agenda creation from meeting topic
- Time allocation for each item
- Participant preparation checklist

### 📝 Minute Taking

- Real-time transcription support
- Key point extraction
- Decision recording

### ✅ Action Item Tracking

- Extract action items from discussion
- Assign owners and deadlines
- Follow-up reminders

---

## Usage

```javascript
const assistant = new MeetingAssistant();

// 创建会议议程
const agenda = await assistant.createAgenda({
  topic: '产品评审会议',
  duration: 60,
  participants: 5,
  goals: ['评审新功能', '确定上线时间']
});

// 生成会议纪要
const minutes = await assistant.generateMinutes({
  transcript: meetingTranscript,
  keyDecisions: ['决定上线时间'],
  actionItems: ['张三负责测试']
});
```

---

## Installation

```bash
clawhub install meeting-assistant
```

---

## License

MIT

---

## Version

1.0.0

---

## Created

2026-04-02
