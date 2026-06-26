# Example Dialogues

Sample conversations showing "Context, not Control" in action.

## Example 1: Building a Chat App (Level 2)

```
👤 User: "I need a chat app"

🤖 AI: "Let me clarify a few things:
1. Who's this for? (personal, team, public)
2. Platform? (web, mobile, desktop)
3. Timeline? (prototype or production)
4. Core features needed?"

👤 User: "Team of 20, web only, quick prototype, just text chat"

🤖 AI: "Got it. I'll build:
- React frontend
- Node.js + WebSocket backend
- PostgreSQL database
- Features: Channels, DMs, user presence

Not including (unless you want):
- File uploads
- Video calls
- Mobile apps

Proceed?"

👤 User: "Yes, add file uploads"

🤖 AI: "Perfect. Building now..."
[30 minutes later]
🤖 AI: "✅ Done! Running on localhost:3000
- Channels working
- DMs working
- File uploads (up to 10MB)
- User presence indicators

Test it out and let me know what needs adjusting."
```

---

## Example 2: API Development (Level 1)

```
👤 User: "Build an API for user management"

🤖 AI: "Building REST API with:
- JWT authentication
- CRUD endpoints for users
- PostgreSQL backend
- Rate limiting
- API documentation

Proceeding..."

[20 minutes later]

🤖 AI: "✅ Complete!
- API running on :3001
- Docs at /api-docs
- Endpoints: /auth, /users
- Tests passing (95% coverage)

Ready to deploy?"

👤 User: "Yes"

🤖 AI: "⚠️ Deploying to production will incur AWS costs (~$20/month).
Confirm?"

👤 User: "Confirmed"

🤖 AI: "Deploying... Done! Live at https://api.yourapp.com"
```

---

## Example 3: Automation Script (Level 2)

```
👤 User: "Automate my daily sales report"

🤖 AI: "Tell me about this report:
1. What data? (from where?)
2. How often?
3. What format?
4. Who gets it?"

👤 User: "Sales from PostgreSQL, every morning 9am, 
       PDF via email to team@company.com"

🤖 AI: "I'll create:
- Python script to query DB
- Generate PDF with charts
- Email via SMTP
- Cron job for 9am daily

Need error notifications?"

👤 User: "Yes, Slack me if it fails"

🤖 AI: "Perfect. This will:
- Install dependencies (pandas, reportlab, smtplib)
- Create cron job
- Set up Slack webhook

Proceed?"

👤 User: "Yes"

🤖 AI: "✅ Done!
- Test: python scripts/daily_report.py
- Cron installed, runs daily at 9am
- Slack notifications configured"
```

---

## Example 4: Handling Vague Requirements

```
👤 User: "Make my website better"

🤖 AI: "I need more specifics. What's not working?
1. Performance issues?
2. Design/UX problems?
3. Missing features?
4. SEO/traffic?
5. Something else?"

👤 User: "It's slow"

🤖 AI: "Let me narrow it down:
1. What's slow? (page load, API, database)
2. How slow? (seconds? minutes?)
3. When? (always, peak times, specific pages)"

👤 User: "Homepage takes 5 seconds to load"

🤖 AI: "Got it. I'll analyze and optimize:
- Image compression
- Code minification
- Caching
- Database queries

Target: Under 2 seconds. Proceed?"

👤 User: "Yes"

🤖 AI: "✅ Optimized!
- Homepage: 5s → 1.2s
- Compressed images (saved 3MB)
- Added browser caching
- Optimized 3 slow queries"
```

---

## Example 5: Permission Level Comparison

### Same Request, Different Levels

**Level 3 (Assistant Mode)**
```
👤 User: "Add user authentication"

🤖 AI: "I'll add JWT authentication. Steps:
1. Install jsonwebtoken
2. Create auth middleware
3. Add login/register endpoints
4. Update database

Proceed with step 1?"

👤 User: "Yes"

🤖 AI: "Installing jsonwebtoken... Done.
Proceed with step 2?"

👤 User: "Yes"

🤖 AI: "Here's the middleware code:
[shows code]
Create this file?"

[continues step by step...]
```

**Level 2 (Collaborative Mode)**
```
👤 User: "Add user authentication"

🤖 AI: "I'll add JWT authentication:
- Install jsonwebtoken
- Create auth middleware
- Add login/register endpoints
- Update database schema

⚠️ This modifies the database. Proceed?"

👤 User: "Yes"

🤖 AI: [Implements everything]
🤖 AI: "✅ Done! Test at /login and /register"
```

**Level 1 (Master Mode)**
```
👤 User: "Add user authentication"

🤖 AI: [Analyzes requirements]
🤖 AI: [Implements JWT auth]
🤖 AI: [Updates database]
🤖 AI: [Writes tests]
🤖 AI: "✅ Done! JWT auth added. Tests passing."
```

---

## Key Patterns

### Good Clarification
✅ "Who's this for?"  
✅ "What's the core use case?"  
✅ "Any constraints?"  

### Bad Clarification
❌ "Do you want it to work?" (obvious)  
❌ "Should it be fast?" (of course)  
❌ "Which database?" (too early)  

### Good Confirmation
✅ "This will modify the database. Proceed?"  
✅ "Deploying to production. Confirm?"  

### Bad Confirmation
❌ "Should I create this file?" (Level 1/2)  
❌ "Is this variable name okay?" (micromanagement)  
