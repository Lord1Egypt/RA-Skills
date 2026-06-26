# Permission Levels - Detailed Guide

Understanding the three permission levels and how to choose the right one.

## Overview

Permission levels control how much autonomy AI has when executing tasks. Think of it as a trust dial:

- **Level 1 (Master)**: Maximum trust, minimum interruption
- **Level 2 (Collaborative)**: Balanced trust and oversight (recommended)
- **Level 3 (Assistant)**: Minimum trust, maximum control

## Level 1: Master Mode

### Philosophy
"I trust AI to make good decisions. Only stop me if it's critical."

### When to Use
- You have high trust in AI capabilities
- You can handle mistakes and rollbacks
- Speed is more important than safety
- You're comfortable with emergent behavior
- You want to see what AI can do unleashed

### What AI Can Do
✅ Write, test, and deploy code  
✅ Install dependencies and tools  
✅ Modify configurations  
✅ Create/update/delete files  
✅ Make architectural decisions  
✅ Research and learn new technologies  
✅ Refactor and optimize  
✅ Run tests and experiments  

### What Requires Confirmation
⚠️ Spending money (API calls, cloud services, domains)  
⚠️ Sending public messages (emails, tweets, blog posts)  
⚠️ Deleting databases or critical data  
⚠️ Restarting production services  

### Example Workflow
```
You: "Build a chat app for my team"

AI: [Analyzes requirements]
AI: [Chooses tech stack: React + Node.js + PostgreSQL]
AI: [Sets up project structure]
AI: [Implements authentication]
AI: [Implements real-time messaging]
AI: [Writes tests]
AI: [Creates deployment config]
AI: "Done. Running on localhost:3000. Want me to deploy to production?"

You: "Yes"

AI: ⚠️ "This will deploy to production and may incur costs. Confirm?"

You: "Confirmed"

AI: [Deploys]
AI: "Live at https://chat.yourteam.com"
```

### Risks
- AI might make decisions you disagree with
- Potential for expensive mistakes (if red lines aren't set properly)
- Harder to understand what AI did (less hand-holding)

### Best For
- Experienced developers who can review code
- Prototyping and experimentation
- Personal projects with low stakes
- Users who embrace "fail fast, learn fast"

---

## Level 2: Collaborative Mode (Default)

### Philosophy
"I trust AI for most things, but want oversight on important operations."

### When to Use
- You want balance between speed and safety
- You're working on a real project (not just experimenting)
- You want to learn from AI's decisions
- You need some guardrails but not micromanagement
- **This is the recommended default for most users**

### What AI Can Do
✅ Write and test code  
✅ Create/update files  
✅ Research and documentation  
✅ Install development dependencies  
✅ Run tests and checks  
✅ Suggest architectural changes  

### What Requires Confirmation
⚠️ Spending money  
⚠️ Sending any external messages  
⚠️ Deleting important files/data  
⚠️ Modifying system configurations  
⚠️ Restarting services  
⚠️ Installing system-level packages  
⚠️ Deploying to production  

### Example Workflow
```
You: "Add user authentication to my app"

AI: "I'll add JWT-based authentication. This requires:
- Installing jsonwebtoken package
- Creating auth middleware
- Adding login/register endpoints
- Updating database schema

Proceed?"

You: "Yes"

AI: [Implements authentication]
AI: "Done. I need to modify the database schema. This will:
- Add users table
- Add password_hash column
- Create indexes

⚠️ This modifies your database. Confirm?"

You: "Confirmed"

AI: [Runs migration]
AI: "Complete. Test at /login and /register"
```

### Risks
- Slightly slower than Master mode (more confirmations)
- AI might ask for confirmation when you'd prefer it just do it

### Best For
- Most users and most projects
- Production applications
- Team projects
- Learning while building
- When you want to stay informed

---

## Level 3: Assistant Mode

### Philosophy
"I want to see and approve everything before it happens."

### When to Use
- You're new to AI-assisted development
- You're learning and want to understand each step
- You're working on high-stakes projects
- You have strict compliance requirements
- You prefer full control

### What AI Can Do
✅ Provide suggestions and explanations  
✅ Show code examples  
✅ Research information  
✅ Explain concepts  

### What Requires Confirmation
⚠️ **Everything else**  
- All file operations  
- All code execution  
- All installations  
- All external calls  

### Example Workflow
```
You: "Add user authentication"

AI: "I suggest JWT-based authentication. Here's the plan:

1. Install jsonwebtoken package
2. Create auth middleware
3. Add login/register endpoints
4. Update database schema

Shall I proceed with step 1?"

You: "Yes"

AI: "Installing jsonwebtoken... Done. Proceed with step 2?"

You: "Yes"

AI: "Here's the auth middleware code:
[shows code]

Shall I create this file?"

You: "Yes"

AI: [Creates file]
AI: "Proceed with step 3?"

[continues...]
```

### Risks
- Much slower workflow
- Can feel tedious for experienced users
- AI might ask for confirmation too often

### Best For
- Beginners learning AI collaboration
- High-stakes or regulated environments
- When you want maximum visibility
- Educational purposes

---

## Choosing Your Level

### Start with Level 2 (Collaborative)
Most users should start here. It provides good balance and you can adjust later.

### Upgrade to Level 1 (Master) when:
- You've worked with AI for a while and trust it
- You're comfortable reviewing code after the fact
- Speed is more important than hand-holding
- You're prototyping or experimenting

### Downgrade to Level 3 (Assistant) when:
- You're new to AI-assisted development
- You're working on something critical
- You want to learn by seeing each step
- You need audit trails for compliance

---

## Customizing Permission Rules

You can customize red/yellow/green lines in `PERMISSION_CONFIG.yaml`:

```yaml
permission_level: 2

# Add custom red lines (always require confirmation)
custom_red_lines:
  - deploy_to_production
  - modify_database_schema
  - send_customer_emails

# Add custom yellow lines (require confirmation at level 2+)
custom_yellow_lines:
  - install_npm_packages
  - modify_env_files
```

---

## Switching Levels

You can change your permission level anytime:

```bash
# Edit PERMISSION_CONFIG.yaml
permission_level: 1  # Change to desired level
```

Or re-run initialization:

```bash
python scripts/init_context.py --permission-level 1
```

---

## Real-World Examples

### Example 1: Startup Founder (Level 1)
"I'm building an MVP. I trust AI to make technical decisions. I just want to review the final product and iterate fast."

### Example 2: Professional Developer (Level 2)
"I'm building a production app. I want AI to handle routine tasks but confirm important changes like database migrations or deployments."

### Example 3: Enterprise Developer (Level 3)
"I'm working on a banking system. I need to review and approve every change for compliance and security."

---

## Tips

1. **Start conservative, then relax**: Begin with Level 2 or 3, upgrade to Level 1 as you gain confidence

2. **Adjust per project**: Use Level 1 for personal projects, Level 2 for work projects

3. **Customize red lines**: Add project-specific operations that always need confirmation

4. **Review regularly**: Check if your permission level still matches your comfort level

5. **Trust but verify**: Even at Level 1, review what AI did after completion
