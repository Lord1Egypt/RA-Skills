# Priority Classification Rules

This document defines the algorithmic rules for categorizing messages as **Urgent**, **Normal**, or **Spam**.

## Urgent Classification (>70% confidence)

Messages are marked **urgent** when they contain:

### 1. Time-Sensitive Language
- Keywords: "ASAP", "urgent", "immediately", "right now", "deadline", "by [time]"
- Phrases: "Need response", "Please reply", "Can't wait"
- Context: Messages sent close to a deadline

```yaml
urgent_keywords:
  - "asap"
  - "urgent"
  - "immediately"
  - "right now"
  - "deadline"
  - "deadline by"
  - "need response"
  - "please reply"
  - "can't wait"
  - "time-sensitive"
  - "critical"
  - "emergency"
```

### 2. Direct Questions/Requests
- "Can you help me?"
- "What do you think about X?"
- "Do you have time to review?"
- "Please confirm"
- "Need your input"

```yaml
question_patterns:
  - "can you.*help"
  - "do you have time"
  - "please confirm"
  - "need your input"
  - "what do you think"
  - "please let me know"
```

### 3. Known Contacts with Time Constraints
- Messages from: boss, team lead, direct reports
- Subject patterns: "Meeting", "Review", "Approval"
- Timestamps: Business hours (9AM-5PM local time)

```yaml
known_contacts:
  - "Boss"
  - "Manager"
  - "Team Lead"
  - "Supervisor"

time_constraint_days:
  - "meeting"
  - "review"
  - "approval"
  - "deadline"
```

### 4. Specific Time Anchors
- "Tomorrow at 3PM"
- "End of day"
- "By Friday"
- "This week"

```yaml
time_anchors:
  - "tomorrow"
  - "by EOD"
  - "by end of day"
  - "by Friday"
  - "this week"
  - "by noon"
  - "this afternoon"
```

---

## Normal Classification (30-70% confidence)

Messages are marked **normal** when they:

### 1. Information Updates
- "Project updated"
- "Status update"
- "Progress report"
- "FYI"

```yaml
update_patterns:
  - "update"
  - "status"
  - "progress"
  - "FYI"
  - "just letting you know"
```

### 2. Requests with Flexible Timing
- "When you have time"
- "No rush"
- "Whenever you're free"
- "Not urgent"

```yaml
flexible_timing:
  - "when you have time"
  - "no rush"
  - "whenever you're free"
  - "not urgent"
  - "whenever you can"
```

### 3. Routine Communications
- "Hello, how are you?"
- "Hope you're doing well"
- "Just checking in"
- "Quick question" (without urgency markers)

### 4. Follow-ups on Previously Discussed Topics
- Messages that reference ongoing conversations
- Reminders about agreed-upon actions

---

## Spam/Noise Classification (>70% confidence)

Messages are marked **spam** when they contain:

### 1. Promotional Language
- "Special offer"
- "Discount"
- "Sale"
- "Limited time"
- "Subscribe now"

```yaml
promotional_keywords:
  - "special offer"
  - "discount"
  - "sale"
  - "limited time"
  - "subscribe"
  - "unlimited"
  - "free trial"
  - "exclusive deal"
  - "buy now"
```

### 2. Notification/Alert Patterns
- "Your password was changed"
- "Login detected"
- "New device signed in"
- "Account updated"

```yaml
notification_patterns:
  - "password"
  - "login"
  - "signed in"
  - "device"
  - "account"
  - "security alert"
  - "verification code"
```

### 3. Low-Priority Notifications
- "X liked your post"
- "Y commented on Z"
- "Weekly digest"
- "Monthly summary"

```yaml
notification_sources:
  - "liked your"
  - "commented on"
  - "digest"
  - "summary"
  - "weekly"
  - "monthly"
  - "notification"
```

### 4. Unknown Senders with Generic Content
- No personalization
- Generic greeting ("Dear customer")
- Mass-mailing patterns

```yaml
generic_patterns:
  - "Dear customer"
  - "Dear subscriber"
  - "Dear member"
  - "Congratulations"
  - "You've won"
```

---

## Confidence Scoring

```python
def calculate_priority(message):
    score = {
        "urgent": 0,
        "normal": 0,
        "spam": 0
    }
    
    # +3 for each urgent keyword match
    score["urgent"] += len(re.findall(r'\b(asap|urgent|deadline|immediately)\b', 
                                      message.lower())) * 3
    
    # +2 for each spam keyword match  
    score["spam"] += len(re.findall(r'\b(discoun|sale|promo)\b', message.lower())) * 2
    
    # +1 for normal patterns
    score["normal"] += len(message.split()) * 0.1  # Length-based heuristic
    
    # Normalize to 0-100 scale
    total = sum(score.values())
    if total == 0:
        return "unknown"
    
    priorities = {k: v/total for k, v in score.items()}
    
    if priorities["urgent"] > 0.7:
        return "urgent"
    elif priorities["spam"] > 0.7:
        return "spam"
    else:
        return "normal"
```

## Learning from Corrections

Track corrections to improve accuracy:

```yaml
corrections:
  - timestamp: "2026-04-15T12:00:00Z"
    original: "spam"
    corrected_to: "normal"
    reason: "from team member about project deadline"
```

Incremental learning updates priority weights based on correction patterns.
